'''
   Copyright 2011 Jesse Yates

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
__author__ = 'jyates'

import argparse
from hammer import  HammerThread, HammerStats, InProcessRunner
from configuration import ExecConfiguration, Configuration

DEFAULT_CONF ='hammer.cfg'
 
class Client(): 
    
    def __init__(self, args):
        #create the parser
        parser = self._setupParser()
        print args
        #parse the arguments sent to the client
        varDict = vars(parser.parse_args(args))
        
        self.hammerClass = self._getHammerClass(varDict, varDict['conf'])
        #create the configuration specified by the conf or on the command line
        self.conf = self._createConfiguration(varDict.pop('conf'), self.hammerClass)
        
        #if there are configuration values, then update the exection conf with values from the command line
        if len(varDict) > 0:
            self._updateConfiguration(self.conf, varDict)
    
    
    def _setupParser(self):
        parser = argparse.ArgumentParser(description='Hammer on a MongoDB installation. Options specified on the command line will override those set in the configuration file')
        parser.add_argument('-c', '--conf', default=DEFAULT_CONF, metavar='ConfFile', 
                           help='name of the configuration file to use. (Defaults to: hammer.cfg)')
        parser.add_argument('-m', '--hammer', help='Fully specified hammer class to use. eg. hammer.MongoHammer', default=argparse.SUPPRESS)
        parser.add_argument('-t', '--threads', help='Number of threads to use (degree of parallelism', default=argparse.SUPPRESS)
        parser.add_argument('-i', '--iter', help='Number of iterations to go through, If -1, go until manual shutdown.', default=argparse.SUPPRESS)
        parser.add_argument('-l', '--latency', help='Maximum amount of time to wait between iterations.', default=argparse.SUPPRESS)
        parser.add_argument('-f', '--forked',help="Enable forking of each hammer to do 'true' parallelization", default=argparse.SUPPRESS)
        return parser
    
    
    def _getHammerClass(self, dict,confFile):
        """
        Dynamically Get the hammer class specified in the hammer
        Args:
            hammer: fully specified name of the hammer
        """
        try:
            name = dict.pop('hammer')
        except KeyError:
            #didn't find the hammer from the command line, so check to see if it was specified in the root configuration
            confReader = ExecConfiguration(confFile)
            name = confReader.getHammerClass()
            if not name:
                raise KeyError("No hammer class specified - cannot run the hammer. Please specify on the command line or in the configuration file")
        
        #first get the full path spec for the class to load
        pathSpec = name.split(".")
        print "actual path spec:"+ str(pathSpec)
        
        return self._importClass(pathSpec)
        
    
    def _importClass(self, fullySpecPath):
        ''' Import the fully specified class'''
        
        module = ".".join(fullySpecPath[:-1])
        #print "importing:" +str(module)
        # get the final class
        clazz = fullySpecPath[len(fullySpecPath)-1]
        
        #import the full class
        m = __import__(module, fromlist=[clazz])
        #print "imported module: "+str(m)
        
        return getattr(m, clazz)
    
    def _createConfiguration(self, confFile, hammerClass):
        """
        Create the specified configuration from the hammer class
        """
        hammerConf = hammerClass.getConfigurationParser()
        return hammerConf(confFile)
 
 
    def _updateConfiguration(self, conf, kvDict):  
        '''
        Do the configuration setting based on the passed in arguments.
        '''
        #this is a bit of a pain since we separate our mongo options from execution options
        #this was done for ease of extensibility an avoiding potential namespace clashes in the future
        if 'threads' in kvDict:
            conf.setNumThreads(kvDict['threads'])
        if 'iter' in kvDict:
            conf.setNumIterations(kvDict['iter'])
        if 'latency' in kvDict:
            conf.setMaxLatency(kvDict['latency'])
        if 'forked' in kvDict:
            conf.setForked(kvDict['forked'])

    
    def start(self, printStats=True):
        """
        Run the hammer. 
        Args:
            printStats: if not specified, just prints out the final stats of the execution
        Return:
             the HammerStats from the execution
        """
        #do the setting up of each of the hammer threads
        threads = self.conf.getNumThreads()
        #Helpful updates of status
        print 'Setting up ', threads, ' hammers on the database'
        
        # figure out if which runner we need to use. Simple version, since we don't need to expect to have more than 1 type
        if self.conf.enableMultiProcess():
            runner = ForkedRunner(threads, self.hammerClass, self.conf)
        else:
            runner = InProcessRunner(threads, self.hammerClass, self.conf)
        
        histories = runner.start()
            
        #Shutdown message
        print 'All hammers have finished hammering.'
        if printStats:
            histories.printStats()
            
        return histories