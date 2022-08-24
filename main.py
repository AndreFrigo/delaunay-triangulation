#triangle: [[x1,y1], [x2,y2], [x3,y3]]
#special points: [-1,-1] and [-2,-2] that are used just to run the algorithm and then removed 
from utils import readInput
import random
import utils


dag = {}
input = readInput()

#highest point p
p = input[0]
for elem in input:
    if utils.pointGreater(elem, p):
        p=elem
input.remove(p)

dag[(p, (-1,-1), (-2,-2))] = []



while(len(input)>0):
    #random choose a point
    p = input.pop(random.randrange(len(input)))

