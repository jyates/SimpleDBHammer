__author__ = 'jyates'

from configuration import Configuration
import argparse
from hammer import Hammer, HammerRunner
DEFAULT_CONF ='hammer.cfg'
 
def main():
    #get the parser
    parser = setupParser()
    #do the parsing
    varDict = vars(parser.parse_args())
    #setup the configuration
    conf = Configuration(varDict['conf'])
    #update the configuration with arguments from the cmd line
    updateConfiguration(conf, varDict)
    
    #do the setting up of each of the hammer threads
    threads = conf.getNumThreads()
    #Helpful updates of status
    print 'Setting up ', threads, ' hammers on the database'
    hammers = []
    for i in range(threads):
        #create the hammer
        h = Hammer(conf)
        #add it to the runner
        runner = HammerRunner(conf, h)
        hammers.append(runner)
        
        #start running the hammer
        runner.start()
        
        #more helpful debugging
        print 'Starting hammer ', i
        
    
    #just join on each thread in turn - ensures that we stop when all threads have stopped running
    for hammer in hammers:
        hammer.join()
        
    #Shutdown message
    print 'All hammers have finished hammering. '
 
def setupParser():
    parser = argparse.ArgumentParser(description='Hammer on a MongoDB installation. Options specified on the command line will override those set in the configuration file')
    parser.add_argument('-c', '--conf', default=DEFAULT_CONF, metavar='ConfFile', 
                       help='name of the configuration file to use. (Defaults to: hammer.cfg)')
    parser.add_argument('-t', '--threads', help='Number of threads to use (degree of parallelism', default=argparse.SUPPRESS)
    parser.add_argument('-i', '--iter', help='Number of iterations to go through, If -1, go until manual shutdown.', default=argparse.SUPPRESS)
    parser.add_argument('-l', '--latency', help='Maximum amount of time to wait between iterations.', default=argparse.SUPPRESS)
    parser.add_argument('-o', '--host', help='[IP]:[port] of the database. Simplification on specifying ip and port separately. If IP or Port are specified, it will overwrite these values.', default=argparse.SUPPRESS)
    parser.add_argument('-a', '--ip', help='Specify the IP Address where the database is running.', default=argparse.SUPPRESS)
    parser.add_argument('-p', '--port', help='Specify the Port where the database is running.', default=argparse.SUPPRESS)
    return parser

def updateConfiguration(conf, kvDict):  
    '''
    Do the configuration setting based on the passed in arguments.
    '''
    #this is a bit of a pain since we separate our mongo options from execution options
    #this was done for ease of extensibility an avoiding potential namespace clashes in the future
    if 'threads' in kvDict:
        conf.setNumThreads(kvDict['threads'])
    if 'iter' in kvDict:
        conf.setNumIterations(kvDict['iter'])
    if 'latency' in kvDict:
        conf.setMaxLatency(kvDict['latency'])
    if 'host' in kvDict:
        fullSpec = kvDict['host']
        (ip, port) = str(fullSpec).split(':')
        conf.setMongoHostIP(ip)
        conf.setMongoHostPort(port)
    if 'ip' in kvDict:
        conf.setMongoHostIP(kvDict['ip'])
    if 'port' in kvDict:
        conf.setMongoHostPort(kvDict['port'])
    

if __name__=='__main__':
    main()