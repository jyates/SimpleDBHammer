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
__author__ = 'jyates'

import unittest
from configuration import  ExecConfiguration

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