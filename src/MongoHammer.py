__author__ = 'jyates'

from configuration import Configuration
import argparse
from hammer import Hammer, HammerRunner
import datetime
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
    histories = []
    for hammer in hammers:
        hammer.join()
        histories.append(hammer.history)
        
    #Shutdown message
    print 'All hammers have finished hammering.'
    printStats(histories)
 
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
    

def printStats(histories):
    """
    Print the stats for each of the hammers, and do some on the fly general stats
    """
    print "----------------------------\n Per Hammer stats:\n----------------------------"
    #print out the stats for each hammer
    i = 0
    data = (datetime.timedelta(0),0)
    for history in histories:
        point = _printStat(i, history)
        data = (data[0]+point[0], data[1]+point[1])
        print '\n'
        i+=1
        
    #print out general statistics
    print "------------------------------\n General Stats:\n------------------------------"
    print 'Total writes:\t', data[1]
    print 'Total time spent writing:\t', str(data[0])
    print 'Average time spent writing:\t', str(data[0]/data[1])
        
def _printStat(index, history):
    print 'Hammer ', str(index), ':'
    count = 0
    totalDiff = datetime.timedelta(0)
    keys = history.keys()
    for key in keys:
        if key == 'done':
            print 'Finished at :', str(history[key])
        else:
            print 'Write ',  str(key), ' took: ', str(history[key])
            count+= 1
            totalDiff += history[key]
    return (totalDiff, count)
if __name__=='__main__':
    main()