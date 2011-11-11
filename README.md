SimpleDBHammer - A General Purpose Utility Database Testing

## Overview: What the heck is this all about?
Often times people need to hammer on their database installation. This can often be a tedious process, raequiring you to specially create a 'hammer' to fine tune your installation. This requires a myriad a moving parts, including multi-threading, randomizing queries, varying record types, etc. - all of which can be complex, annoying or easily implemented incorrectly.

SimpleDBHammer is a very flexible, python based database 'hammer' library/tool. We provide easy mechanisms for specifying the amount of parallelism, frequency, run statistics, and specifying the types of records. Its a starting place for figuring out where things are starting to slow down, not the end-all, be-all of testing. It was written over a weekend, come on.

## Usage: Do do I use it?
The client can be wrapped with a command line utility or one can be adapted from the various provided main classes (see src/run). The specific hammer to type to use is dynamically loaded and can be specified either on the command line or in the configuration file.

A starter configuration is provided in src/hammer.cfg. This is also the default configuration file that will be read. All the options specified in this file will be overwritten by options passed to the client. 

The actual writer specified is the one that will determine which kinds of records will be used to write to the database. See examples in src/examples for various types of hammers that can be created.

## Dependencies: What else do I need to get?
### General
python 2.7
(mox 0.5.3)[http://code.google.com/p/pymox/]

### Database Dependent
#### MongoDB
(pymongo 2.0.1)[http://api.mongodb.org/python/current/]

## Extension: What if you don't have the database I need?
If we don't have the database type you are looking for, it is very easy to add. Merely you just subclass the Hammer class (see src/hammer.py) and implement a handful of methods. We are also actively developing this tool, so you can also check back often. If you are interested in extending this tool to new databases, look into src/hammers for an example of how to do this.

## License
The use and distribution terms of the software covered by the Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0.html), the full context of which can be found at License.html at the root of this distribution. By using this software, you are agreeing to all terms and conditions of the aforementioned license.

## Developers:
Jesse Yates([@jesse_yates] (http://twitter.com/jesse_yates))

## Thanks:
This was originally developed for use by GoChime to hammer on their MongoDB installation.
