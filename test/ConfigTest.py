__author__ = 'jyates'

import unittest
from configuration import  ExecConfiguration, MongoConfiguration

class ExecConfigurationTest(unittest.TestCase):
    """Test the execution configuration"""
    
    def test_NoSectionsReadInFile(self):
        '''
        If the input configuration file doesn't have the basic section set, want to make sure that they get added first
        '''
        conf = ExecConfiguration('')
        conf.setMaxLatency(10)
        self.assertEquals(10, conf.getMaxLatency())
    
    def setUp(self):
        self.conf = ExecConfiguration("testHammer.cfg")
    
    def test_LoadThreads(self):
        self.assertEqual(1, self.conf.getNumThreads())
    
    def test_SettingValues(self):
        self.conf.setExecutionValues(dict(thing=1))
        self.assertEquals(1, int(self.conf.parser.get('exec', 'thing')))
    
    def test_SetThreads(self):
        self.conf.setNumThreads(10)
        self.assertEqual(10, self.conf.getNumThreads())
        
class MongoConfigurationTest(unittest.TestCase):
    """Test the MongoDB configuration reader"""
    
    def setUp(self):
        self.conf = MongoConfiguration("testHammer.cfg")
    
    def test_MongoIP(self):
        self.assertEquals("localhost", self.conf.getMongoHostIP())
    
    def test_MongoPort(self):
        self.assertEquals(27017, self.conf.getMongoHostPort())