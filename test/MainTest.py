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
'''

import copy
import unittest
import mox
from hammerclient import Client
from hammer import Hammer, HammerStats
from test.mock import MockHammer
import test
import hammers.mongo

class TestClient(mox.MoxTestBase):
    
    def  setUp(self):
        self.args1 = "-l 20 -t 3 ".split()
    def tearDown(self):
        #for later modification
        pass
    
    def test_NeedsHammer(self):
        """
        Test that we throw an error if the hammer is not specified
        """
        
        #specify the configuration file to read
        args = copy.deepcopy(self.args1)
        for value in ('-c testHammer.cfg'.split()):
            args.append(value)
        
        print 'running checking for hammer.'
        print 'current args:' + str(args)
        try:
            Client(args)
            self.assertTrue(False)
        except KeyError:
            pass
    
    def test_FullyConfigured(self):
        """
        Test that the configuration can be fully handled via a single configuration file
        """
        args = copy.deepcopy(self.args1)
        for value in ('-c testHammer1.cfg'.split()):
            args.append(value)
        client = Client(args)
        
        conf = client.conf
        self.assertEquals(20, conf.getMaxLatency())
        self.assertEquals(3, conf.getNumThreads())
        #make sure that we don't overwrite default values
        self.assertEquals(10, conf.getNumIterations())
    
    def test_ImportHammerClass(self):
        #test getting top level class
        dict = ({'hammer':'hammers.mongo.MongoHammer'})
        client  = Client(['-c', 'testHammer1.cfg'])
        hammerImport =  Client._getHammerClass(client, dict, None)
        print "Imported:"+str(hammerImport)
        self.assertEquals(hammerImport, hammers.mongo.MongoHammer)
        
        #test getting a nested class
        dict.setdefault('hammer', 'test.mock.MockHammer')
        hammerImport =  Client._getHammerClass(client, dict, None)
        self.assertEquals(MockHammer, hammerImport)
        
        
class TestHammerStats(mox.MoxTestBase):

    def test_HandleStatus(self):
        '''
        Test that we don't throw errors when handling a bunch of hammer stats
        '''
        histories = HammerStats()
        
        #test just one history
        histories.append(self._getHammerHistory())
        histories.printStats()
        
        #test with two histories
        histories.append(self._getHammerHistory())
        histories.printStats()
        
    def _getHammerHistory(self):
        #create a generic hammer - should not do anything
        mockConf = self.mox.CreateMockAnything(description="Mock a specific configuration instance")
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
    
    
def FakeClient(Client):
    """Just a fake client so we can test the useful methods in client
    """
    def __init__():
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()