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

import ConfigParser
from ConfigParser import NoOptionError

#section header
executionSection = "exec"

#execution configuration keys
THREADS_KEY = "threads"
LATENCY_KEY = "latency"
REPEAT_KEY = "iterations"
HAMMER_CLASS_KEY = "hammer.class"
ENABLE_FORKING = "forked"

# Execution defaults
defaultThreads = 1
defaultLatency = 10     # seconds
defaultRepeat = 10      #do 10 writes
defaultEnabledForking = False

class Configuration(object):
    """
        Load values from the configuration.
        Provides easy, aliased accessed to values from the configuration.
        Does lookups dynamically into the configuration. Can be optimized later for caching values
    """
    
    def __init__(self, location):
        self.parser = ConfigParser.SafeConfigParser()
        self.parser.read(location)
            
    def _setKeyValues(self, section, keyValues):
        #make sure that we add the section, if it isn't present
        if not self.parser.has_section(section):
            self.parser.add_section(section)
            
        #add the key/values to the specified section  
        keys= keyValues.keys()
        for key in keys:
            print 'Setting ', section, ':', str(key) , ' to ', str(keyValues[key])
            self.parser.set(section, str(key), str(keyValues[key]))
    
    #internal methods for making it easier to do configuration lookups
    def _configurationLookup(self, section):
        '''
        Do a configuration lookup in the specified section.
        '''
        return lambda option: self.parser.get(section, option)
    
    def _getConfWithDefault(self, getFunction, default):
        """
        Call the specified conf lookup function with the given value.
         If the option is not present in the configuration, the default value is returned. None is returned otherwise.
        """
        try:
            return getFunction()
        except NoOptionError:
            print "No option found - using default", default
            return default

class ExecConfiguration(Configuration):
    """
    Configuration for doing general execution
    """

    def getNumThreads(self):
        return int(self.execLookup(THREADS_KEY, defaultThreads))
    
    def setNumThreads(self, numThreads):
        self.setExecutionValues(dict(threads=numThreads))
    
    def getMaxLatency(self):
        return long(self.execLookup(LATENCY_KEY, defaultLatency))
    
    def setMaxLatency(self, timeout):
        self.setExecutionValues(dict(latency=timeout))
   
    def getNumIterations(self):
        return long(self.execLookup(REPEAT_KEY, defaultRepeat))
    
    def setNumIterations(self, count):
        self.setExecutionValues(dict(iterations=count))
    
    def getHammerClass(self):
        return (self.execLookup(HAMMER_CLASS_KEY, None))
    
    def enableMultiProcess(self):
        return (self.execLookup(ENABLE_FORKING, defaultEnabledForking))
    
    def setForked(self, fork):
        self.setExecutionValues(dict(forked=fork))
    
    def execLookup(self, option, default):
        return self._getConfWithDefault(lambda: self.parser.get(executionSection, option), default)
    
    #Setting values in the configuration - for use with the command line
    def setExecutionValues(self, keyValues):
        self._setKeyValues(executionSection, keyValues)


        
    