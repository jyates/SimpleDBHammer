'''
Created on Sep 25, 2011

@author: jyates

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