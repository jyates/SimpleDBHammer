'''
Created on Sep 25, 2011

@author: jyates

Do the actual hammering on MongoDB
'''
from threading import Thread, Timer
import random
from pymongo import Connection

class Hammer(object):
    """
        Connect to and then write to MongoDB
    """
    def __init__(self, conf):
        self.conf = conf
        
    
    def connect(self):
        """
        Connect to the database. Must be called before actually using the hammer.
        Since each connection to MongoDB runs over a different connection pool, each hammer writes to its own port (ensuring that we actually get parallel writes)
        """
        self.connection = Connection(self.conf.getMongoHostIP(), self.conf.getMongoHostPort())
        self.database = self.connection[self.conf.getMongoDatabaseName()]
    
    def write(self):
        """
        Do the write specified in the configuration to the database
        """
        pass
    
    def disconnect(self):
        """Disconnect the hammer from the database. Should be called when finished with the hammer.
        """
        self.connection.disconnect()

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
        times = self.conf.setNumIterations()
        
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