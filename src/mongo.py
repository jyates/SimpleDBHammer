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

   Description: Example class for running mongo
'''

from hammerclient import Client

def main():
    """To run this example:
        1) start mongod on the localhost, running on port 27017
        2) Add a database to mongo named "test"
        3) Run: "./python mongo.py"
    """
    
    # Kind of cheating here by just setting the arguments you should be passing in
    client = Client(["-c", "examples/mongo_example_hammer.cfg"])
    client.start()
    
if __name__=='__main__':
    main()
        