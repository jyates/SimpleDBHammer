__author__ = 'jyates'

from configuration import Configuration
import argparse
from hammer import Hammer, HammerRunner
DEFAULT_CONF ='hammer.cfg'
 
def main():
    parser = argparse.ArgumentParser(description='Hammer on a MongoDB installation. Options specified on the command line will override those set in the configuration file')
    parser.add_argument( '--conf', default=DEFAULT_CONF, metavar='ConfFile', 
                       help='name of the configuration file to use. (Defaults to: hammer.cfg)')
    
    varDict = vars(parser.parse_args())
    conf = Configuration(varDict['conf'])
    
    threads = conf.getNumThreads()
    hammers = []
    for i in range(threads):
        #create the hammer
        h = Hammer(conf)
        #add it to the runner
        runner = HammerRunner(conf, h)
        hammers.append(runner)
        
        #start running the hammer
        runner.start()
        i+=1
    
    #just join on each thread in turn - ensures that we stop when all threads have stopped running
    for hammer in hammers:
        hammer.join()
    
    

if __name__=='__main__':
    main()