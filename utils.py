import sys

#Checks whether point1 is greater than point2
def pointGreater(point1, point2):
    if point1 == (-2,-2):
        return True
    if point1 == (-1,-1):
        return False
    if point2 == (-2,-2):
        return False
    if point2 == (-1,-1):
        return True
    if(point1[1] > point2[1]):
        return True
    elif(point1[1] == point2[1]):
        return point1[0]>point2[0]
    else:
        return False



# Checks whether a point is inside a triangle (also on the edges)
# point has the following format: (x,y)
# triangle has the following format: (p1, p2, p3), where p1, p2, p3 are the vertices 
def pointInTriangle(point, triangle):
    l1 = (triangle[0], triangle[1])
    l2 = (triangle[1], triangle[2])
    l3 = (triangle[2], triangle[0])
    ret = [pointLinePosition(point, l1), pointLinePosition(point, l2), pointLinePosition(point, l3)]    
    if(1 in ret and -1 in ret):
        return False
    else:
        return True

#check whether a point is on an edge of the triangle, if it is the case returns the edge, otherwise return None
def pointOnTriangle(point, triangle):
    for edge in [(triangle[0], triangle[1]), (triangle[1], triangle[2]), (triangle[2], triangle[0])]:
        if pointLinePosition(point, edge)==0: return edge
    return None

#return 1 if the point is in the left, -1 if it is in the right, 0 if it is inside.
def pointLinePosition(point, line):
    #check if the line is made by the two special points
    if (line == ((-2,-2), (-1,-1))):
        return 1
    if (line == ((-1,-1), (-2,-2))): 
        return -1
    a, b = line
    #conditions for special points
    if((-1,-1) in line or (-2,-2) in line):
        if (b==(-1,-1) and pointGreater(point, a)): return 1
        if (a==(-2,-2) and pointGreater(point, b)): return 1
        if (a==(-1,-1) and pointGreater(b, point)): return 1
        if (b==(-2,-2) and pointGreater(a, point)): return 1
        return -1
    ret = (b[0] - a[0])*(point[1] - a[1]) - (b[1] - a[1])*(point[0] - a[0])
    #count for floating point approximation
    ret = round(ret, 3)
    if ret > 0: return 1
    if ret < 0: return -1
    return 0



# Reads the input file and stores all the points
# returns a list of tuples representing points
def readInput(inputFile="input.txt"):
    lines = []
    ret = []
    with open(inputFile) as f:
        lines = f.readlines()
    for line in lines:
        s = line.rstrip()
        s = s.split(',')
        ret.append((int(s[0]), int(s[1])))
    return ret

# Checks if a point 'p' is inside the circle made from the points of the triangle 'triangle'
# returns true if p is inside the circle
def isInsideCircle(p, triangle):
    b,c,d=triangle
    temp = c[0]**2 + c[1]**2
    bc = (b[0]**2 + b[1]**2 - temp) / 2
    cd = (temp - d[0]**2 - d[1]**2) / 2
    det = (b[0] - c[0]) * (c[1] - d[1]) - (c[0] - d[0]) * (b[1] - c[1])

    if abs(det) < 1.0e-10:
        return None

    # Center of circle
    cx = (bc*(c[1] - d[1]) - cd*(b[1] - c[1])) / det
    cy = ((b[0] - c[0]) * cd - (c[0] - d[0]) * bc) / det
    # Radius
    radius = ((cx - b[0])**2 + (cy - b[1])**2)**.5
    # Check if p is inside, the round is to count for floating point approximation (approximating for 3 decimals)
    return (p[0] - cx)**2 + (p[1] - cy)**2 < round(radius**2, 3)


#legalize the edge if it is illegal 
#params: the point inserted 'p', the edge to control and maybe legalize 'e' the DAG dag and the actual triangulation 't'
def legalizeEdge(p, e, dag, t):
    #get the triangles that have edge e
    firstTriangle = list(dag.keys())[0]
    triangles = findTrianglesEdge(e,t)
    print("legalizeEdge-> p: "+str(p)+", edge: "+str(e)+"  -> EDGE: "+str(e)+", TRIANGLES: "+str(triangles))
    # print("legalizeEdge-> p: "+str(p)+", edge: "+str(e)+"  -> EDGE: "+str(e)+", TRIANGULATION: "+str(t))

    #if the edge is an edge of the first triangle (p0, p-1, p-2) then the edge is legal
    if edgeOfTriangle(e, firstTriangle):
        print("legalizeEdge-> p: "+str(p)+", edge: "+str(e)+"  -> EDGE OF THE FIRST TRIANGLE, RETURN")
        return

    #if the edge belongs only to a triangle then it cannot be flipped and it is by definition legal
    if len(triangles)==1:
        print("legalizeEdge-> p: "+str(p)+", edge: "+str(e)+"  -> THE EDGE BELONGS ONLY TO A TRIANGLE, SO IT IS LEGAL, RETURN")
        return

    # k is the point of the triangle adjacent to (p, e[0], e[1])
    k = None
    position = pointLinePosition(p, e)
    for triangle in triangles:
        for point in triangle:
            if(point != p and point != e[0] and point != e[1] and pointLinePosition(point,e)!=position):
                k = point

    #if the 4 points are all real points (no p-1 or p-2) then the normal algorithm has to be executed
    #TODO: tested, ok
    if p[0] >= 0 and e[0][0] >= 0 and e[1][0] >= 0 and k and k[0] >= 0:
        print("legalizeEdge-> p: "+str(p)+", k: "+str(k)+", edge: "+str(e)+"  -> ALL THE POINTS ARE REAL, NORMAL ALGORITHM")
        #the edge is illegal if p is inside the circle made by e[0], e[1] and k
        if isInsideCircle(p, [e[0], e[1], k]):
            #replace the triangles
            print("legalizeEdge-> p: "+str(p)+", k: "+str(k)+", edge: "+str(e)+"  -> SWAP EDGE")
            for triangle in triangles:
                print("REMOVING: "+str(triangle))
                t.remove(triangle)
                dag[triangle].append((p,k,e[0]))
                dag[triangle].append((p,k,e[1]))
            print("Appending "+str((p,k,e[0]))+", and "+str((p,k,e[1])))
            addTriangle((p,k,e[0]), t)
            addTriangle((p,k,e[1]), t)
            dag[(p,k,e[0])] = []
            dag[(p,k,e[1])] = []
            legalizeEdge(p, (e[0], k), dag, t)
            legalizeEdge(p, (e[1], k), dag, t)
        return
        
    
    # legal iff min(p, k) < min(e[0], e[1]), they cannot be equal (because at least one is negative)
    if k:
        print("legalizeEdge-> p: "+str(p)+", k: "+str(k)+", edge: "+str(e)+"  -> THE POINT OF THE TRIANGLE ADJACENT EXISTS, CHECKS FOR THE NON REAL POINTS")
        if min(p[0], k[0]) > min(e[0][0], e[1][0]) :
            #illegal edge
            #replace the triangles
            print("legalizeEdge-> p: "+str(p)+", k: "+str(k)+", edge: "+str(e)+"  -> SWAP EDGE")
            # print("Triangles: "+str(triangles))
            # print("K: "+str(k))
            for triangle in triangles:
                # print(triangle)
                # print("---------------")
                # for elem in t: print(elem)
                print("REMOVING: "+str(triangle))
                t.remove(triangle)

                dag[triangle].append((p,k,e[0])) 
                dag[triangle].append((p,k,e[1]))
            print("Appending "+str((p,k,e[0]))+", and "+str((p,k,e[1])))
            addTriangle((p,k,e[0]), t)
            addTriangle((p,k,e[1]), t)
            dag[(p,k,e[0])] = []
            dag[(p,k,e[1])] = []
            legalizeEdge(p, (e[0], k), dag, t)
            legalizeEdge(p, (e[1], k), dag, t)
            return
        return
    sys.exit("ERROR in legalizeEdge, k="+str(k)+"\n")
    return  
    
#returns a list containing the triangles that contain point p, given the point, the dag and the node of the dag where to look
def findTrianglesPoint(p, dag, start, ret=None):
    if ret == None:
        ret = []
    print("findTrianglesPoint -> START: "+str(start))
    print("findTrianglesPoint -> ret: "+str(ret))

    #ret contains the leafs of the DAG that represents triangles containing p (at most 2)
    # for construction every point must be inside the triangle P0,P-1,P-2
    
    if(dag[start] == []): 
        print("findTrianglesPoint -> LEAF: "+str(start))
        ret.append(start)
    #starting nodes for recursive iteration
    if start not in ret:
        for t in dag[start]:
            if pointInTriangle(p, t):
                print("NEWSTART APPEND: "+str(t))
                findTrianglesPoint(p, dag, t, ret)
    # print("findTrianglesPoint -> RETURN: "+str(ret))
    return ret

#return True if "edge" is an edge of the triangle
def edgeOfTriangle(edge, triangle):
    p0 = triangle[0]
    p1 = triangle[1]
    p2 = triangle[2]
    return (p0 in edge and p1 in edge) or (p1 in edge and p2 in edge) or (p2 in edge and p0 in edge)


#returns one or two triangles that have the edge e, given the edge, the dag and a list of nodes of the dag where to look
def findTrianglesEdge(edge, triangulation):
    ret = []
    for t in triangulation:
        if edgeOfTriangle(edge, t): ret.append(t)
    return ret
    

#add a triangle in the triangulation structure
def addTriangle(triangle, triangulation):
    check = False
    for elem in triangulation:
        if isSameTriangle(triangle, elem): check=True
    if not check: triangulation.append(triangle)
    return

#checks if two triangles are the same
def isSameTriangle(t1, t2):
    return t1[0] in t2 and t1[1] in t2 and t1[2] in t2