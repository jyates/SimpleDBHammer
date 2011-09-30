'''
Created on Sep 25, 2011

@author: jyates

Do the actual hammering on MongoDB
'''
from threading import Thread, Timer
import random
import datetime

class Hammer(object):
    """
        Connect to and then write to an output.
        The hammer is completely reusable between different connect/disconnect calls.
        Subclasses must specify self.connection that has a disconnect() method
    """
    def __init__(self, conf):
        self.conf = conf
        self.counter = 0
        self.history = dict()
    
    def connect(self, clearHistory=True):
        """
        Connect to the database. Must be called before actually using the hammer.
        Args:
            clearHistory: defaults to true. Remove any previous history associated with this hammer.
        """
        self.history = dict()
        pass

    def write(self):
        """
        Do the write specified in the configuration to the database.
        Keeps track of timing stats.
        """
        #get the current time
        startWrite = datetime.datetime.now()
        #do the write
        self.doWrite()
        #get the time difference
        diffWrite = datetime.datetime.now() - startWrite
        #store it in the history
        self.history.setdefault(self.counter, diffWrite)
        self.counter+=1
    
    def doWrite(self):
        """
        Subclasses should implement this method. Should do the actual write to the database
        """
        pass
    
    def disconnect(self):
        """Disconnect the hammer from the database. Should be called when finished with the hammer.
        """
        self.connection.disconnect()
        #store the done time
        self.history['done'] = datetime.datetime.now()
        
    

class HammerRunner(Thread):
    
    def __init__(self, conf, hammer):
        """
        Create tool to run the hammering on the database.
        Args:
            conf: Configuration to use
            hammer: do the actual writing to the database
        """
        super(Thread, self).__init__()
        self.conf = conf
        self.hammer = hammer
        self.hammer.connect()
    
    def run(self):
        '''
        Do the hammering
        '''
        freq = self.conf.getMaxLatency()
        times = self.conf.getNumIterations()
        
        #If times <0, run forever. 
        #otherwise, just run it the specified number of times
        count =0
        while times <0 or count < times:
            #this might be an issue with random - if all threads are using the same random, could cause issues
            sleep = random.uniform(0, freq)
            
            #after the sleep time, do a new put into the database
            timer = Timer(sleep, self.hammer.write())
            timer.start()
            count+=1
        self.hammer.disconnect()
        
class HammerStats(object):
    """
    Statistics about how a set of hammers ran
    Args:
        hammers: list of histories (which are themselves dictionaries) from hammers
    """
    histories = []
    
    def append(self, stat):
        self.histories.append(stat)
    
    def printStats(self):
        """
        Print the stats for each of the hammers, and do some on the fly general stats
        """
        print "----------------------------\n Per Hammer stats:\n----------------------------"
        #print out the stats for each hammer
        i = 0
        data = (datetime.timedelta(0),0)
        for history in self.histories:
            point = self._printStat(i, history)
            data = (data[0]+point[0], data[1]+point[1])
            print '\n'
            i+=1
            
        #print out general statistics
        print "------------------------------\n General Stats:\n------------------------------"
        print 'Total writes:\t', data[1]
        print 'Total time spent writing:\t', str(data[0])
        print 'Average time spent writing:\t', str(data[0]/data[1])
            
    def _printStat(self, index, history):
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
    
        pass