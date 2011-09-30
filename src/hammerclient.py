__author__ = 'jyates'

import argparse
from hammer import Hammer, HammerRunner, HammerStats

DEFAULT_CONF ='hammer.cfg'
 
class Client(): 
    
    def __init__(self, *args):
        #create the parser
        parser = self._setupParser()
        #parse the arguments sent to the client
        varDict = vars(parser.parse_args(args))
        
        hammerClass = self._getHammerClass(varDict.pop('hammer'))
        #create the configuration specified by the conf or on the command line
        self.conf = self._createConfiguration(varDict.pop('conf'), hammerClass)
        
        #if there are configuration values, then update the exection conf with values from the command line
        if len(varDict) > 0:
            self._updateConfiguration(self.conf, varDict)
            
        self.hammer = hammerClass(self.conf)
    
    
    def _setupParser(self):
        parser = argparse.ArgumentParser(description='Hammer on a MongoDB installation. Options specified on the command line will override those set in the configuration file')
        parser.add_argument('-c', '--conf', default=DEFAULT_CONF, metavar='ConfFile', 
                           help='name of the configuration file to use. (Defaults to: hammer.cfg)')
        parser.add_argument('-m', '--hammer', help='Fully specified hammer class to use. eg. hammer.MongoHammer', default=argparse.SUPPRESS)
        parser.add_argument('-t', '--threads', help='Number of threads to use (degree of parallelism', default=argparse.SUPPRESS)
        parser.add_argument('-i', '--iter', help='Number of iterations to go through, If -1, go until manual shutdown.', default=argparse.SUPPRESS)
        parser.add_argument('-l', '--latency', help='Maximum amount of time to wait between iterations.', default=argparse.SUPPRESS)
        return parser
    
    
    def _getHammerClass(self, name):
        """
        Dynamically Get the hammer class specified in the hammer
        Args:
            hammer: fully specified name of the hammer
        """
        if not name:
            raise ValueError("No hammer class specified - cannot run the hammer. Please specify on the command line or in the configuration file")
        
        mod = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod
    
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
        hammers = []
        for i in range(threads):
            #create the hammer
            h = Hammer(self.conf)
            #add it to the runner
            runner = HammerRunner(self.conf, h)
            hammers.append(runner)
            
            #start running the hammer
            runner.start()
            
            #more helpful debugging
            print 'Starting hammer ', i
            
        
        #just join on each thread in turn - ensures that we stop when all threads have stopped running
        histories = HammerStats()
        for hammer in hammers:
            hammer.join()
            histories.append(hammer.history)
            
        #Shutdown message
        print 'All hammers have finished hammering.'
        if printStats:
            histories.printStats()
            
        return histories