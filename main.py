#triangle: [[x1,y1], [x2,y2], [x3,y3]]
#special points: [-1,-1] and [-2,-2] that are used just to run the algorithm and then removed 
from utils import readInput, addTriangle, pointOnTriangle, edgeOfTriangle, pointInTriangle
from utils import findTrianglesPoint
from utils import legalizeEdge
from utils import pointLinePosition
from plot import plot, plotDebug
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
x = None
while(len(input)>0):
    i=i+1
    print("EXECUTION "+str(i))
    print("TRIANGULATION: "+str(triangulation))
    plotDebug(i, triangulation)
    # print("DAG: "+str(dag))
    #random choose a point TODO
    # p = input.pop(random.randrange(len(input)))
    p = input.pop(0)
    print("POINT: "+str(p))
    #find the triangle (or 2 triangles) containing p
    triangles = findTrianglesPoint(p, dag, list(dag.keys())[0], [])
    #TODO prova
    x = []
    for elem in triangulation:
        if pointInTriangle(p, elem): x.append(elem)
    print("----------TRIANGLES: "+str(triangles))
    for k in dag.keys():
        if dag[k] == []: print(k)
    print("----------NEW TRIANGLES: "+str(x))
    print(triangulation)
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
            print("MAIN -> POINT ON EDGE "+str(edge))
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
                print("Removing "+str(t))
                triangulation.remove(t)
                if pk in t:
                    dag[t].append((edge[0], pk, p))
                    dag[t].append((edge[1], pk, p))
                    print("Appending "+str((edge[0], pk, p)))
                    print("Appending "+str((edge[1], pk, p)))
                    addTriangle((edge[0], pk, p), triangulation)
                    addTriangle((edge[1], pk, p), triangulation)

                else:
                    dag[t].append((edge[0], pl, p))
                    dag[t].append((edge[1], pl, p))
                    print("Appending "+str((edge[0], pl, p)))
                    print("Appending "+str((edge[1], pl, p)))
                    addTriangle((edge[0], pl, p), triangulation)
                    addTriangle((edge[1], pl, p), triangulation)
            dag[(edge[0], pk, p)] = []
            dag[(edge[1], pk, p)] = []
            dag[(edge[0], pl, p)] = []
            dag[(edge[1], pl, p)] = []
            legalizeEdge(p, (edge[0], pl), dag, triangulation)
            legalizeEdge(p, (pl, edge[1]), dag, triangulation)
            legalizeEdge(p, (edge[1], pk), dag, triangulation)
            legalizeEdge(p, (pk, edge[0]), dag, triangulation)
    
    if edge==None:
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
        # print("MAIN -> TRIANGULATION: "+str(triangulation))
        legalizeEdge(p, (t[0], t[1]), dag, triangulation)
        legalizeEdge(p, (t[1], t[2]), dag, triangulation)
        legalizeEdge(p, (t[2], t[0]), dag, triangulation)

    print("\n----------\n----------\n")
print("Triangulation with "+str(len(triangulation))+" triangles\n")
for elem in triangulation:
    print(elem)

print(triangulation)
print("bsn")
plotDebug(i+1, triangulation)





            



