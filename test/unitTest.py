'''
Created on Sep 25, 2011

@author: jyates
'''
import unittest
import ConfigTest
import HammerTest
import sys
    
def load(module):
    return unittest.TestLoader().loadTestsFromModule(module)

def main():
    #unittest.TestLoader().loadTestsFromTestCase(
    suite = []
    suite.append(load(ConfigTest))
    suite.append(load(HammerTest))
    allTests = unittest.TestSuite(suite)
    
    result = unittest.TextTestRunner(verbosity=2).run(allTests)
    print "Number errors:"+str(len(result.errors))
    sys.exit( len(result.errors))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    main()