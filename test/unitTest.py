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

Run all the unit tests. 
Useful for when nosetests isn't playing nice.
'''
import unittest
import ConfigTest
import HammerTest
import MainTest
import MongoTest
import ForkedTest
import sys
    
def load(module):
    return unittest.TestLoader().loadTestsFromModule(module)

def main():
    #unittest.TestLoader().loadTestsFromTestCase(
    suite = []
    suite.append(load(ConfigTest))
    suite.append(load(HammerTest))
    suite.append(load(MainTest))
    suite.append(load(MongoTest))
    suite.append(load(ForkedTest))
    allTests = unittest.TestSuite(suite)
    
    result = unittest.TextTestRunner(verbosity=2).run(allTests)
    print "Number of errors:"+str(len(result.errors))
    sys.exit( len(result.errors))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    main()