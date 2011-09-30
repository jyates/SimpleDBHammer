FullNeptune - A General Purpose Utility Database Testing

Names:
Fierce Anaconda
Stormy Kangeroo
Restless Warhouse
Forsaken Hammer
Electron burst
Bitter Boa
DBStomp

## Overview: What the heck is this all about?
Often times people need to hammer on their database installation. This can often be a tedious process, raequiring you to specially create a 'hammer' to fine tune your installation. This requires a myriad a moving parts, including multi-threading, randomizing queries, varying record types, etc. - all of which can be complex, annoying or easily implemented incorrectly.

{Name} is a very flexible, python based database 'hammer' library/tool. We provide easy mechanisms for specifying the amount of parallelism, frequency, run statistics, and specifying the types of records.

## Usage: Do do I use it?
Running it:
The client can be wrapped with a command line utility or one can be adapted from the various provided main classes (see src/main/run). The specific records to write to the database can be specified via the records.cfg file, though this value is configurable.

Configuring records:
Record types are configurable via the a configuration file (records.cfg). They are specified via a JSON-esque style. See the examples in the src/main/examples folder.

## Dependencies: What else do I need to get?
### General
python 2.7
(mox 0.5.3)[http://code.google.com/p/pymox/]

### Database Dependent
#### MongoDB
(pymongo 2.0.1)[http://api.mongodb.org/python/current/]

## Extension: What if you don't have the database I need?
If we don't have the database type you are looking for, it is very easy to add. Merely you just subclass the Hammer class (see src/main/hammer.py) and implement a handful of methods. We are also actively developing this tool, so you can also check back often. This can be 

## License
The use and distribution terms of the software covered by the Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0.html), the full context of which can be found at License.html at the root of this distribution. By using this software, you are agreeing to all terms and conditions of the aforementioned license.

## Developers:
Jesse Yates([@jesse_yates] (http://twitter.com/jesse_yates))

##Corporate Sponoship:
This was originally developed for use by GoChime to hammer on their MongoDB installation. Please visit them at www.gochime.com
