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

Test the hammer utility
'''

from hammer import Hammer, HammerThread, ForkedRunner
from configuration import ExecConfiguration
import mox
from hammers.mongo import SimpleMongoHammer


class TestHammerThread(mox.MoxTestBase):
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
        runner = HammerThread(mockConf, mockHammer)
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