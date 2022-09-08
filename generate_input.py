#This script allows to randomly generate the input points
#The generated file is "input.txt"
# example: python generate_input.py 20 100     generates 20 random point (all different) in the range (0-100, 0-100)

def generateInput(numPoints, max):
    import random
    l = []
    while(len(l) < numPoints):
        x = random.randint(0, max)
        y = random.randint(0, max)
        el = str(x)+','+str(y)+'\n'
        if el not in l:
            l.append(el)  

    l[-1] = l[-1][:-1]
    with open('input.txt', 'w') as f:
        for elem in l:
            f.write(elem)

#Validate command line input
def is_intstring(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

#generate input using parameters given from command line
import sys
if(len(sys.argv) == 3):
    for arg in sys.argv[1:]:
        if not is_intstring(arg):
            sys.exit("All arguments must be integers!")
else:
    sys.exit("Wrong number of arguments!\nGive the following: numPoints, maxCoordinate")
    
l = [int(arg) for arg in sys.argv[1:]]
generateInput(l[0], l[1])
