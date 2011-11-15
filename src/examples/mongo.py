'''
Created on Nov 15, 2011

@author: jyates

Description: Example class to use for running mongo
'''

import hammerclient 
import sys
def main():
    client = hammerclient.Client(sys.argv)
    client.start()
    
if __name__=='__main__':
    main()
    
import hammers
    
class SimpleMongoHammer(hammers.mongo.MongoHammer):
    
    # Adapted from Python docs for Mongo: http://api.mongodb.org/python/2.0.1/tutorial.html
    record = {"author": "Mike","text": "My first blog post!","tags": ["mongodb", "python", "pymongo"]}
    
    def doWrite(self):
        self.collection.insert(self.record)
        