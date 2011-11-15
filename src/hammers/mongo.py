__author__='jyates'

from hammer import Hammer
from configuration import ExecConfiguration
from pymongo import Connection

class MongoHammer(Hammer):
    """
    Connect/disconnect from a mongoDB installation.
    Subclasses should be used for handling specific write cases.
    Subclasses should implement void doWrite() to write to the database.
    """
    
    def connect(self, clearHistory=True):
        """
        Since each connection to MongoDB runs over a different connection pool, each hammer writes to its own port (ensuring that we actually get parallel writes)
        """
        super(Hammer).connect(clearHistory)
        self.connection = Connection(self.conf.getMongoHostIP(), self.conf.getMongoHostPort())
        database = self.connection[self.conf.getMongoDatabaseName()]
        self.collection = database[self.conf.getMongoCollectionName()]
    
    @classmethod
    def getConfigurationParser(cls):
        """
        Get the configuration parser associated with this hammer.
        """
        return MongoConfiguration
    
#section header
mongoSection = "mongo"

#mongo configuration keys
HOST_KEY = "ip"
PORT_KEY = "port"
DATABASE_KEY = "db"
COLLECTION_KEY = "collection"

# Mongo Defaults
defaultHost = "127.0.0.1"
defaultPort = "27017"

class MongoConfiguration(ExecConfiguration):
    """
    Configure the connection to a mongo database
    """
        
    def getMongoHostIP(self):
        return self.mongoLookup(HOST_KEY, defaultHost)
    
    def setMongoHostIP(self, host):
        self.setMongoValues(dict(ip=host))
    
    def getMongoHostPort(self):
        return int(self.mongoLookup(PORT_KEY, defaultPort))
            
    def setMongoHostPort(self, Port):
        self.setMongoValues(dict(port=Port))
    
    def setMongoValues(self, keyValues):
        self._setKeyValues(mongoSection, keyValues)
    
    def mongoLookup(self, option, default):
        return self._getConfWithDefault(lambda: self.parser.get(mongoSection, option), default)
    
    def getMongoDatabaseName(self):
        return self.mongoLookup(DATABASE_KEY, None)
    
    def getMongoCollectionName(self):
        return self.mongoLookup(COLLECTION_KEY, None)