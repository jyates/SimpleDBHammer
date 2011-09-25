__author__ = 'jyates'

import unittest
from configuration import Configuration

class ConfigurationTestCase(unittest.TestCase):
    
    def setUp(self):
        self.conf = Configuration("testHammer.cfg")
    
    def test_LoadThreads(self):
        self.assertEqual(1, self.conf.getNumThreads())
    
    def test_MongoIP(self):
        self.assertEquals("localhost", self.conf.getMongoHostIP())
    
    def test_MongoPort(self):
        self.assertEquals(27017, self.conf.getMongoHostPort())
        
    def test_SettingValues(self):
        self.conf.setExecutionValues(dict(thing=1))
        self.assertEquals(1, int(self.conf.parser.get('exec', 'thing')))