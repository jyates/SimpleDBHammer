'''
Created on Sep 25, 2011

@author: jyates

Test all aspects of the hammer utility
'''

from hammer import Hammer, HammerRunner
from configuration import ExecConfiguration
import mox


class TestHammerRunner(mox.MoxTestBase):
    """
    Test the hammer runner.
    Essentially, just check that it runs the expected number of times
    """

    def testRunCount(self):
        #setup objs to pass into the runner
        mockHammer = self.mox.CreateMock(Hammer)
        mockConf = self.mox.CreateMock(ExecConfiguration)
        
        #record calls on the hammer
        mockHammer.connect()
        mockHammer.write().MultipleTimes()
        mockHammer.disconnect()
        
        #record calls on the configuration
        mockConf.getMaxLatency().AndReturn(10)
        mockConf.getNumIterations().AndReturn(2)
        
        self.mox.ReplayAll()
        runner = HammerRunner(mockConf, mockHammer)
        runner.run()
        
        #verify the test
        self.mox.VerifyAll()
        
class TestHammer(mox.MoxTestBase):
    """
    Test that the hammer will write the connect, disconnect, and write the correct values to the database
    """
    
    def test_History(self):
        #create a generic hammer - should not do anything
        mockConf = self.mox.CreateMock(ExecConfiguration)
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