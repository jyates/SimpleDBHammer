'''
Created on Sep 25, 2011

@author: jyates

Do the actual hammering on MongoDB
'''
from threading import Thread, Timer
import random
from pymongo import Connection
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
        
class MongoHammer(Hammer):
    """
    Connect/disconnect from a mongoDB installation.
    Subclasses should be used for handling specific write cases.
    The connection must have a disconnect() method or subclass must implement their own disconnect() method
    """
    
    def connect(self, clearHistory=True):
        """
        Since each connection to MongoDB runs over a different connection pool, each hammer writes to its own port (ensuring that we actually get parallel writes)
        """
        super(Hammer).connect(clearHistory)
        self.connection = Connection(self.conf.getMongoHostIP(), self.conf.getMongoHostPort())
        self.database = self.connection[self.conf.getMongoDatabaseName()]
    

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