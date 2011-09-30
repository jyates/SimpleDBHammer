'''
Created on Sep 25, 2011

@author: jyates
'''
import unittest
import mox
from client import setupParser, updateConfiguration, printStats
from configuration import MongoConfiguration
from hammer import Hammer

class TestParser(unittest.TestCase):


    def setUp(self):
        # specifying host, latency, num threads, overriding port,
        self.args1 = "-o 128.10.2.1:50 -p 25 -l 20 -t 3".split()
        pass

    def tearDown(self):
        #for later modification
        pass

    def test_ParsingAndSetting(self):
        parser = setupParser()
        args = vars(parser.parse_args(self.args1))
        #create an empty config
        conf = MongoConfiguration('')
        updateConfiguration(conf, args)
        #check that we update the values as specified
        self.assertEquals(25, conf.getMongoHostPort())
        self.assertEquals('128.10.2.1', conf.getMongoHostIP())
        self.assertEquals(20, conf.getMaxLatency())
        self.assertEquals(3, conf.getNumThreads())
        #make sure that we don't overwrite default values
        self.assertEquals(10, conf.getNumIterations())
  
class TestStats(mox.MoxTestBase):
    """
     Test writing/getting stats at the end of a run
    """  
    
    def test_HandleStatus(self):
        '''
        Test that we don't throw errors when handling a bunch of hammers
        '''
        #test just one history
        printStats([self._getHammerHistory()])
        #test with two histories
        histories = [self._getHammerHistory()]
        histories.append(self._getHammerHistory())
        printStats(histories)
        
    def _getHammerHistory(self):
        #create a generic hammer - should not do anything
        mockConf = self.mox.CreateMock(MongoConfiguration)
        mockConn = self.mox.CreateMockAnything(description='Mock a connection to a generic database. Just needs a disconnect() method.')
        mockConn.disconnect()
        self.mox.ReplayAll()
        
        #run the test
        hammer = Hammer(mockConf)
        hammer.connection = mockConn
        hammer.connect()
        hammer.write()
        hammer.write()
        hammer.write()
        hammer.disconnect()
        
        #verify calls and history
        self.mox.VerifyAll()
        history = hammer.history
        self.assertEquals(4, len(history))
        return history
    
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()