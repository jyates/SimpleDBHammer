
class Thing(object):
    value = 1
    
    def doWork(self):
        print "Do work"
     
def parrot(voltage, state = 'a stiff', action = 'voom', type = 'Norwegian Blue'):
    print "-- This parrot wouldn't ", action, 
    print "if you put ", voltage, "Volts through it."
    print "-- Lovelly plumage, the ", type
    print "--It's, ", state, "!"

def println():
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

def main():
    parrot(1000)
    println()
    parrot(action='VOOOM', voltage = 200)
    println()
    parrot('a thousand', state = 'pushing up daisies')
    println()
    parrot('a million', 'berefet of life', 'jump')
    println()
    
    obj = Thing()
    obj.doWork()
    
if __name__ == "__main__":
    main()


