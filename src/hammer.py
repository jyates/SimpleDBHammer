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

from threading import Thread, Timer
import random
import datetime
import pp
from statlib import stats

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
        if clearHistory:
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
        self.counter += 1
    
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


class HammerThread(Thread):
    
    def __init__(self, conf, hammer):
        """
        Create tool to run the hammering on the database.
        Args:
            conf: Configuration to use
            hammer: do the actual writing to the database
        """
        #makes sure the thread gets initialized
        super(HammerThread, self).__init__()
        
        #setup the rest of the values
        self.conf = conf
        self.hammer = hammer
        self.hammer.connect()
    
    def run(self):
        '''
        Do the hammering
        '''
        freq = self.conf.getMaxLatency()
        times = self.conf.getNumIterations()
        print "Thread " + self.name + " info: \n Freq:" + str(freq) + "\n Times:" + str(times) + "\n"
        #If times <0, run forever. 
        #otherwise, just run it the specified number of times
        count = 0
        while times < 0 or count < times:
            print "Thread " + self.name + " write number:" + str(count + 1)
            #this might be an issue with random - if all threads are using the same random, could cause issues
            sleep = random.uniform(0, freq)
            print "Thread " + self.name + " sleeping for " + str(sleep)
            #after the sleep time, do a new put into the database
            timer = Timer(sleep, self.hammer.write)
            timer.start()
            #wait for the timer to finish
            timer.join()
            #and increment the counter!
            count += 1
        self.hammer.disconnect()

class HammerRunner(object):
    """
    Do all the actual work of running each of the hammers and then returning back results
    """
    def __init__(self, numHammers, hammerClazz, hammerConf):
        self.numHammers = numHammers
        self.hammerClass = hammerClazz
        self.conf = hammerConf
    
    def start(self):
        """
        Run all the hammers and then return their stats as a HammerStat.
        This method should be implemented by subclasses 
        """
        pass

class InProcessRunner(HammerRunner):
    
    def __init__(self, numHammers, hammerClazz, hammerConf):
        #store the values
        super(InProcessRunner, self).__init__(numHammers, hammerClazz, hammerConf)
        
        #setup the hammers to run
        self.hammers = []
        for i in range(numHammers):
            #create the hammer
            h = self.hammerClass(self.conf)
            print "Instantiated hammer:" + str(h)
            #add it to the runner
            #here is where we do the switch on the configuration value for if it is parallel or not
            runner = HammerThread(self.conf, h)
            self.hammers.append(runner)
    
    """
    Run all the hammer threads in the same processes. This could be an issue with the GIL, but it depends on the amount of I/O contentiona
    """
    def start(self):
        #iterate through each of the hammers and run them
        for runner in self.hammers:
            #start running the hammer
            runner.start()
        
        #just join on each thread in turn - ensures that we stop when all threads have stopped running
        histories = HammerStats()
        for hammer in self.hammers:
            hammer.join()
            histories.append(hammer.hammer.history)
        return histories

class ForkedRunner(HammerRunner):
    """
    Run all the hammer threads in the same processes. This could be an issue with the GIL, but it depends on the amount of I/O contentiona
    """
    
    def __init__(self, numHammers, hammerClazz, hammerConf):
        super(ForkedRunner, self).__init__(numHammers, hammerClazz, hammerConf)
         # tuple of all parallel python servers to connect with

        ppservers = ()
          # Creates jobserver with the number of workers = # hammers 
        if numHammers >= 0:
            self.job_server = pp.Server(int(numHammers), ppservers=ppservers)
        else:
            # Creates jobserver with automatically detected number of workers
            self.job_server = pp.Server(ppservers=ppservers)
            
        print "Starting pp with", self.job_server.get_ncpus(), "workers"
        
    def start(self):  
    # run_hammer - the function
    # (clazz, conf) - tuple with arguments for sum_primes
    # () - tuple with functions on which the function depends
    # (hammerClass) - tuple with module names which must be imported before sum_primes execution
    # Execution starts as soon as one of the workers will become available
        jobs = []
        for i in range(self.numHammers):
            jobs.append(self.job_server.submit(run_hammer, (self.hammerClass, self.conf), (), ("hammer",self.getHammerPackage(self.conf.getHammerClass()))))
        
        #get each of the stats
        histories = HammerStats()
        for job in jobs:
            histories.append(job())
        return histories
    
    def getHammerPackage(self, hammerClassName):
        pathSpec = str(hammerClassName).split(".")
        print "hammer class path spec:"+ str(pathSpec)
        return ".".join(pathSpec[:-1])
    
def run_hammer(hammerClass, conf):
    """
    Run a single hammer
    """
    singleRunner = hammer.InProcessRunner(1, hammerClass, conf)
    return singleRunner.start()    
    
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
        allTimes = []
        print "----------------------------\n Per Hammer stats:\n----------------------------"
        #print out the stats for each hammer
        i = 0
        data = (datetime.timedelta(0), 0)
        for history in self.histories:
            point = self._printStat(i, history, allTimes)
            data = (data[0] + point[0], data[1] + point[1])
            print '\n'
            i += 1
            
        #print out general statistics
        print "------------------------------\n General Stats:\n------------------------------"
        print 'Total writes:\t', data[1]
        print 'Total time spent writing:\t', str(data[0])
        print 'Mean time spent writing:\t', str(data[0] / data[1])
        #We could add more information here about the stats, now that all the times are gathered
        print 'Standard deviation:\t\t', stats.stdev(allTimes)

            
    def _printStat(self, index, history, allTimes):
        print 'Hammer ', str(index), ':'
        count = 0
        totalDiff = datetime.timedelta(0)
        keys = history.keys()
        for key in keys:
            if key == 'done':
                print 'Finished at :', str(history[key])
            else:
                time = history[key]
#                print "class:"+str(time.__class__.name)+"time:"+time
                allTimes.append(time.total_seconds())
                print 'Write ', str(key), ' took: ', str(time)
                count += 1
                totalDiff += history[key]
        return (totalDiff, count)
    
        pass

class FakeHammer(Hammer):
    """
    Fake hammer used for testing. 
    It acts just like a real hammer, only it doesn't do anything.
    """
    def __init__(self, conf):
        super(FakeHammer, self).__init__(conf)
        self.connection = FakeConnection()
        
class FakeConnection(object):
    """
    An fake connection to a database. Doesn't actually do anything but provide an interface
    """
    def disconnect(self):
        pass