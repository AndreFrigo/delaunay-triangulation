#triangle: [[x1,y1], [x2,y2], [x3,y3]]
#special points: [-1,-1] and [-2,-2] that are used just to run the algorithm and then removed 
from utils import readInput, addTriangle, pointOnTriangle, edgeOfTriangle, pointInTriangle
from utils import findTrianglesPoint, dagAppend, dagLeaf
from utils import legalizeEdge, pointGreater
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
    if pointGreater(elem, p):
        p=elem
input.remove(p)

addTriangle((p, (-1,-1), (-2,-2)), triangulation)
dag[(p, (-1,-1), (-2,-2))] = []
minPoint = p
maxPoint = p
i=0
x = None
while(len(input)>0):
    i=i+1
    # print("EXECUTION "+str(i))
    # print("TRIANGULATION: "+str(triangulation))
    # print("DAG: "+str([elem for elem in list(dag.keys()) if dag[elem]==[]]))
    # plotDebug(i, triangulation)
    # print("DAG: "+str(dag))
    #random choose a point TODO
    # p = input.pop(random.randrange(len(input)))
    p = input.pop(0)
    if pointGreater(p, maxPoint): maxPoint = p
    elif pointGreater(minPoint, p): minPoint = p
    # print("POINT: "+str(p)+", minPoint: "+str(minPoint)+", maxPoint: "+str(maxPoint))
    #find the triangle (or 2 triangles) containing p
    triangles = findTrianglesPoint(p, dag, list(dag.keys())[0], [])
    # print("----------TRIANGLES: "+str(triangles))
    # for k in dag.keys():
    #     if dag[k] == []: print(k)
    # print("----------NEW TRIANGLES: "+str(x))
    # if len(x)>2:
    #     sys.exit("ERROR! MORE THAN 2 TRIANGLES CONTAINING p: "+str(p)+" -> "+str(x))
    # print(triangulation)
    # # triangles = x
    # #TODO: fix dag
    # if len(triangles)==0:
    #     triangles.append(x[0])
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
            # print("MAIN -> POINT ON EDGE "+str(edge))
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
                # print("Removing "+str(t))
                triangulation.remove(t)
                if pk in t:
                    dagAppend(dag, t, (edge[0], pk, p))
                    dagAppend(dag, t, (edge[1], pk, p))
                    # print("Appending "+str((edge[0], pk, p)))
                    # print("Appending "+str((edge[1], pk, p)))
                    addTriangle((edge[0], pk, p), triangulation)
                    addTriangle((edge[1], pk, p), triangulation)

                else:
                    dagAppend(dag, t, (edge[0], pl, p))
                    dagAppend(dag, t, (edge[1], pl, p))
                    # print("Appending "+str((edge[0], pl, p)))
                    # print("Appending "+str((edge[1], pl, p)))
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
    
    if edge==None:
        #add the three new triangles in the triangulation
        t = triangles[0]
        # print("Removing "+str(t))
        triangulation.remove(t)
        # print("Appending "+str((p,t[0],t[1]))+", and "+str((p,t[1],t[2]))+", and "+str((p,t[2],t[0])))
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
    # plotDebug(i-1, triangulation)




# print("Triangulation with "+str(len(triangulation))+" triangles\n")
# for elem in triangulation:
#     print(elem)

plotDebug("triangulation", triangulation)





            



