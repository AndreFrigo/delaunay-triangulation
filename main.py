#triangle: [[x1,y1], [x2,y2], [x3,y3]]
#special points: [-1,-1] and [-2,-2] that are used just to run the algorithm and then removed 
from utils import readInput
from utils import findTriangle
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
    #find the triangle (or 2 triangles) containing p
    triangles = findTriangle(p, dag, [(p, (-1,-1), (-2,-2))])
    #if "triangles" contains only one triangle then p is inside that triangle, otherwise it is in the common edge between the two triangles in the list "triangles"
    if len(triangles)==1:
        #add the three new triangles in the triangulation
        t = triangles[0]
        dag[t] = [(p, t[0], t[1]), (p, t[1], t[2]), (p, t[2], t[0])]
        dag[(p, t[0], t[1])] = []
        dag[(p, t[1], t[2])] = []
        dag[(p, t[2], t[0])] = []
        #legalize the edges
        #TODO


