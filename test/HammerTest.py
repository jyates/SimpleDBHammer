'''
Created on Sep 25, 2011

@author: jyates
'''
import unittest
from hammer import Hammer, HammerRunner
from configuration import Configuration
import mox


class TestHammerRunner(mox.MoxTestBase):
    """
    Test the hammer runner.
    Essentially, just check that it runs the expected number of times
    """

    def testRunCount(self):
        #setup objs to pass into the runner
        mockHammer = self.mox.CreateMock(Hammer)
        mockConf = self.mox.CreateMock(Configuration)
        
        #record calls on the hammer
        mockHammer.connect()
        mockHammer.write().MultipleTimes()
        mockHammer.disconnect()
        
        #record calls on the configuration
        mockConf.getMaxLatency().AndReturn(10)
        mockConf.setNumIterations().AndReturn(2)
        
        self.mox.ReplayAll()
        runner = HammerRunner(mockConf, mockHammer)
        runner.run()
        
class TestHammer(unittest.TestCase):
    """
    Test that the hammer will write the connect, disconnect, and write the correct values to the database
    """
    pass
