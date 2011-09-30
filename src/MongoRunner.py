'''
Run a hammer against a mongo database.
Various hammer types can be specified via the configuration file or via the command line
'''

import hammerclient 
import sys
def main():
    client = hammerclient.Client(sys.argv)
    client.start()
    
if __name__=='__main__':
    main()