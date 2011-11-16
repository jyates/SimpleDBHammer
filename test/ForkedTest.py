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

   Description: Test running the forked hammer
'''
import mox


from hammer import ForkedRunner, FakeHammer
from configuration import ExecConfiguration

class TestForkedRunner(mox.MoxTestBase):
    """
    Test that we properly fork processes
    """
    def testGeneralRunning(self):
        
        #record calls on the configuration
#        mockConf.getMaxLatency().AndReturn(10)
#        mockConf.getNumIterations().AndReturn(2)
        
#        self.mox.ReplayAll()
        try:
            runner = ForkedRunner(1, FakeHammer,ExecConfiguration("forkedHammer.cfg") )
            runner.start()
        except Exception as e:
            self.fail("Recieved an error message - that shouldn't have happened...\n"+str(e))