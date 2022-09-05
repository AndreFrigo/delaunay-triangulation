#triangle: [[x1,y1], [x2,y2], [x3,y3]]
#special points: [-1,-1] and [-2,-2] that are used just to run the algorithm and then removed 
from utils import readInput, addTriangle
from utils import findTrianglesPoint
from utils import legalizeEdge
from utils import pointLinePosition
import random
import utils
import sys

random.seed(1)

dag = {}
triangulation = []
input = readInput()

#highest point p
p = input[0]
for elem in input:
    if utils.pointGreater(elem, p):
        p=elem
input.remove(p)

addTriangle((p, (-1,-1), (-2,-2)), triangulation)
dag[(p, (-1,-1), (-2,-2))] = []

i=0
while(len(input)>0):
    i=i+1
    print("EXECUTION "+str(i))
    print("TRIANGULATION: "+str(triangulation))
    print("DAG: "+str(dag))
    #random choose a point
    p = input.pop(random.randrange(len(input)))
    print("POINT: "+str(p))
    #find the triangle (or 2 triangles) containing p
    triangles = findTrianglesPoint(p, dag, [list(dag.keys())[0]], [])
    #if "triangles" contains only one triangle then p is inside that triangle, otherwise it is in the common edge between the two triangles in the list "triangles"
    if len(triangles)==1:
        #add the three new triangles in the triangulation
        t = triangles[0]
        print("Removing "+str(t))
        triangulation.remove(t)
        print("Appending "+str((p,t[0],t[1]))+", and "+str((p,t[1],t[2]))+", and "+str((p,t[2],t[0])))
        addTriangle((p, t[0], t[1]), triangulation)
        addTriangle((p, t[1], t[2]), triangulation)
        addTriangle((p, t[2], t[0]), triangulation)
        dag[t] = [(p, t[0], t[1]), (p, t[1], t[2]), (p, t[2], t[0])]
        dag[(p, t[0], t[1])] = []
        dag[(p, t[1], t[2])] = []
        dag[(p, t[2], t[0])] = []
        #legalize the edges
        print("MAIN -> TRIANGULATION: "+str(triangulation))
        legalizeEdge(p, (t[0], t[1]), dag, triangulation)
        legalizeEdge(p, (t[1], t[2]), dag, triangulation)
        legalizeEdge(p, (t[2], t[0]), dag, triangulation)
    elif len(triangles) == 2:
        #find the edge where p resides
        e = None
        for edge in triangles[0]:
            if pointLinePosition(p, edge) == 0 and edgeOfTriangle(edge, triangles[1]):
                e = edge
        if e==None:
            sys.exit("ERROR in main algorithm when point is on an edge of two triangles (1)\n")

        #other point of the first triangle
        pk = None
        for point in triangles[0]:
            if(point != e[0] and point != e[1]):
                pk = point
        #other point of the second triangle
        pl = None
        for point in triangles[0]:
            if(point != e[0] and point != e[1]):
                pl = point
        if not pk or not pl:
            sys.exit("ERROR in main algorithm when point is on an edge of two triangles (2)\n")

        for t in triangles:
            triangulation.remove(t)
            if pk in t:
                dag[t].append((e[0], pk, p))
                dag[t].append((e[1], pk, p))
                addTriangle((e[0], pk, p), triangulation)
                addTriangle((e[1], pk, p), triangulation)

            else:
                dag[t].append((e[0], pl, p))
                dag[t].append((e[1], pl, p))
                addTriangle((e[0], pl, p), triangulation)
                addTriangle((e[1], pl, p), triangulation)
        dag[(e[0], pk, p)] = []
        dag[(e[1], pk, p)] = []
        dag[(e[0], pl, p)] = []
        dag[(e[1], pl, p)] = []

    print("\n----------\n----------\n")
print("Triangulation with "+str(len(triangulation))+" triangles\n")
for elem in triangulation:
    print(elem)


            



