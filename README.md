# SimpleDBHammer - A General Purpose Utility For Database Testing

## Overview: What the heck is this all about?
Often times people need to hammer on their database installation. This can often be a tedious process, raequiring you to specially create a 'hammer' to fine tune your installation. This requires a myriad a moving parts, including multi-threading, randomizing queries, varying record types, etc. - all of which can be complex, annoying or easily implemented incorrectly.

SimpleDBHammer is a very flexible, python based database 'hammer' library/tool. We provide easy mechanisms for specifying the amount of parallelism, frequency, run statistics, and specifying the types of records. Its a starting place for figuring out where things are starting to slow down, not the end-all, be-all of testing. It was written over a weekend, come on.

## Usage: Do do I use it?
The client can be wrapped with a command line utility or one can be adapted from the various provided main classes (see src/run). The specific hammer to type to use is dynamically loaded and can be specified either on the command line or in the configuration file.

A starter configuration is provided in src/hammer.cfg. This is also the default configuration file that will be read. All the options specified in this file will be overwritten by options passed to the client. 

The actual writer specified is the one that will determine which kinds of records will be used to write to the database. See examples in src/examples for various types of hammers that can be created.
re

Example client usage can be found at:

* src/mongo.py

### Configuration Options: What can I fiddle with? 
These configuration options and general usage can be see by just running 'python 

#### General Execution

* hammer.class - Fully qualified class name to load as the hammer class (which actually does the writes). This is the only value that needs to be set.

	Defaults to: None

#####Optional Values

* threads - Number of threads/processes to run
	
	Defaults to: 1
* iterations - Number of writes to make to the system

	Defaults to: 10
* latency - Maximum amount of time to wait between writes on a given thread. This interval to actually wait is uniformly chosen at random between 0 - {latency} seconds

	Defaults to: 10

	
#### Parallelism (Advanced Usage)
 * forked - The simplest way to run the tool is to just the use default configuration combined with a db specific configuration (see examples). However, the default model to use is to basic threads in Python. This _should_ work in the general case, where it is expected that the writer threads will be blocked writign to the database and is spending minimal time figuring out what the next value that should be written. This is combined with the fact that the degree of randomness in the waits between writes to help avoid the ([Global Interpreter Lock](http://en.wikipedia.org/wiki/Global_Interpreter_Lock)). However, if you find that threads are not getting the expected parallelism, you can also enable the use of pp (ParallelPython) to fork out each writer as its own process. This has implications for the number of processes running on a system, so it is should be used with care. If you don't specify the number of threads/processes then ParallelPython will handle that for you and it will be the number of cores in the system

	Defaults to: false

* threads - If this is set to -1, the number of threads will be determined by ParallelPython and correspond closely to the number of processors available on the machine

## Dependencies: What else do I need to get?
### General
* python 2.7
* Mox ([mox 0.5.3] (http://code.google.com/p/pymox/))
* ParallelPython ([pp] (http://www.parallelpython.com/)) 

### Database Dependent
#### MongoDB
* Pymongo ([pymongo 2.0.1] (http://api.mongodb.org/python/current/))

## Extension: What if you don't have the database I need?
If we don't have the database type you are looking for, it is very easy to add. Merely you just subclass the Hammer class (see src/hammer.py) and implement a handful of methods. We are also actively developing this tool, so you can also check back often. If you are interested in extending this tool to new databases, look into src/hammers for an example of how to do this.

## Roadmap

There are currently several things on the short-term roadmap (recommendations are also welcome):

1. Add support for more metrics (mean, median, std deviation)
2. Add dumping of data to a graphable format to make it easier to see trends over time.
3. Add support for more databases
4. Add a setup.py or easyinstall for easy usage
4. Look into adding a ForkingClient rather than a fork runner (or doing some cleanup there)
4. Add support for just a single command line file to launch, rather than having to wrap the client in a simple function.
5. Add cluster integration

## License
The use and distribution terms of the software covered by the Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0.html), the full context of which can be found at License.html at the root of this distribution. By using this software, you are agreeing to all terms and conditions of the aforementioned license.

## Developers
Jesse Yates([@jesse_yates] (http://twitter.com/jesse_yates))

## Thanks
This was originally developed for use by GoChime to hammer on their MongoDB installation.
