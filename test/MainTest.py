'''
Created on Sep 25, 2011

@author: jyates
'''
import unittest
from MongoHammer import setupParser, updateConfiguration
from configuration import Configuration


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
        conf = Configuration('')
        updateConfiguration(conf, args)
        #check that we update the values as specified
        self.assertEquals(25, conf.getMongoHostPort())
        self.assertEquals('128.10.2.1', conf.getMongoHostIP())
        self.assertEquals(20, conf.getMaxLatency())
        self.assertEquals(3, conf.getNumThreads())
        #make sure that we don't overwrite default values
        self.assertEquals(10, conf.getNumIterations())
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()