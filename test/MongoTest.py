from mongo import MongoConfiguration
import unittest
class MongoConfigurationTest(unittest.TestCase):
    """Test the MongoDB configuration reader"""
    
    def setUp(self):
        self.conf = MongoConfiguration("testMongoHammer.cfg")
    
    def test_MongoIP(self):
        self.assertEquals("localhost", self.conf.getMongoHostIP())
    
    def test_MongoPort(self):
        self.assertEquals(27017, self.conf.getMongoHostPort())