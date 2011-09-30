__author__ = 'jyates'

import ConfigParser
from ConfigParser import NoOptionError

#section header
executionSection = "exec"

#execution configuration keys
THREADS_KEY = "threads"
LATENCY_KEY = "latency"
REPEAT_KEY = "iterations"

# Exection defaults
defaultThreads = 1
defaultLatency = 10 # seconds
defaultRepeat = 10 #do 10 writes

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
    
    def execLookup(self, option, default):
        return self._getConfWithDefault(lambda: self.parser.get(executionSection, option), default)
    
    #Setting values in the configuration - for use with the command line
    def setExecutionValues(self, keyValues):
        self._setKeyValues(executionSection, keyValues)


        
    