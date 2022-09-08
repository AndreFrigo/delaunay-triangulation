#triangle: ((x1,y1), (x2,y2), (x3,y3))
#special points: (-1,-1) and (-2,-2) that are used just to run the algorithm and then removed 
from utils import readInput, addTriangle, pointOnTriangle, edgeOfTriangle, findTrianglesPoint
from utils import dagAppend, dagLeaf, legalizeEdge, pointGreater
from plot import plotDebug
import random
import sys

inputFile = None
if(len(sys.argv) == 2):
    inputFile = str(sys.argv[1])
else:
    sys.exit("Wrong number of arguments!\nGive the following: inputFile")

dag = {}
triangulation = []
input = readInput(inputFile)
#highest point p
p = input[0]
for elem in input:
    if pointGreater(elem, p):
        p=elem
input.remove(p)

addTriangle((p, (-1,-1), (-2,-2)), triangulation)
dag[(p, (-1,-1), (-2,-2))] = []
minPoint = p
maxPoint = p
i=0
while(len(input)>0):
    i=i+1
    p = input.pop(0)
    if pointGreater(minPoint, p): minPoint = p
    
    #find the triangle (or 2 triangles) containing p
    triangles = findTrianglesPoint(p, dag, list(dag.keys())[0])
    
    #if "triangles" contains more than one triangle it could be that the point is on a shared edge
    #edge containing the point (if a point is on an edge, the edge must be shared between two triangles)
    edge = None
    if len(triangles)>1:
        t1 = None
        t2 = None
        k = 0
        while (k<len(triangles) and not edge):
            edge = pointOnTriangle(p, triangles[k])
            k+=1
        if edge:
            t1 = triangles[k-1]
            while (k<len(triangles)):
                if edgeOfTriangle(edge, triangles[k]): 
                    t2 = triangles[k]
                    k += len(triangles)
                k+=1
        
            #other point of the first triangle
            pk = None
            for point in t1:
                if(point != edge[0] and point != edge[1]):
                    pk = point
            #other point of the second triangle
            pl = None
            for point in t2:
                if(point != edge[0] and point != edge[1]):
                    pl = point
            
            for t in [t1,t2]:
                triangulation.remove(t)
                if pk in t:
                    dagAppend(dag, t, (edge[0], pk, p))
                    dagAppend(dag, t, (edge[1], pk, p))
                    addTriangle((edge[0], pk, p), triangulation)
                    addTriangle((edge[1], pk, p), triangulation)

                else:
                    dagAppend(dag, t, (edge[0], pl, p))
                    dagAppend(dag, t, (edge[1], pl, p))
                    addTriangle((edge[0], pl, p), triangulation)
                    addTriangle((edge[1], pl, p), triangulation)
            dagLeaf(dag, (edge[0], pk, p))
            dagLeaf(dag, (edge[1], pk, p))
            dagLeaf(dag, (edge[0], pl, p))
            dagLeaf(dag, (edge[1], pl, p))
            legalizeEdge(p, (edge[0], pl), dag, triangulation, minPoint, maxPoint)
            legalizeEdge(p, (pl, edge[1]), dag, triangulation, minPoint, maxPoint)
            legalizeEdge(p, (edge[1], pk), dag, triangulation, minPoint, maxPoint)
            legalizeEdge(p, (pk, edge[0]), dag, triangulation, minPoint, maxPoint)
    
    #the point is inside a triangle, not in an edge shared between two triangles
    if edge==None:
        #add the three new triangles in the triangulation
        t = triangles[0]
        triangulation.remove(t)
        addTriangle((p, t[0], t[1]), triangulation)
        addTriangle((p, t[1], t[2]), triangulation)
        addTriangle((p, t[2], t[0]), triangulation)
        dagAppend(dag, t, (p, t[0], t[1]))
        dagAppend(dag, t, (p, t[1], t[2]))
        dagAppend(dag, t, (p, t[2], t[0]))
        dagLeaf(dag, (p, t[0], t[1]))
        dagLeaf(dag, (p, t[1], t[2]))
        dagLeaf(dag, (p, t[2], t[0]))
        #legalize the edges
        legalizeEdge(p, (t[0], t[1]), dag, triangulation, minPoint, maxPoint)
        legalizeEdge(p, (t[1], t[2]), dag, triangulation, minPoint, maxPoint)
        legalizeEdge(p, (t[2], t[0]), dag, triangulation, minPoint, maxPoint)
    # for debugging each stage of the execution
    # plotDebug("triangulation"+str(i-1), triangulation)

plotDebug("triangulation", triangulation)





            



