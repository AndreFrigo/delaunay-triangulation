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

#return 1 if the point is on the left of the line, -1 if it is on the right, 0 if it is inside.
# the line can also contain one or two special points, the point instead has to be real 
def pointLinePosition(point, line):
    #check if the line is made by the two special points
    if (line == ((-2,-2), (-1,-1))):
        return 1
    if (line == ((-1,-1), (-2,-2))): 
        return -1
    a, b = line
    #conditions for special points in the line
    if((-1,-1) in line or (-2,-2) in line):
        if (b==(-1,-1) and pointGreater(point, a)): return 1
        if (a==(-2,-2) and pointGreater(point, b)): return 1
        if (a==(-1,-1) and pointGreater(b, point)): return 1
        if (b==(-2,-2) and pointGreater(a, point)): return 1
        return -1
    #condition for normal points
    ret = (b[0] - a[0])*(point[1] - a[1]) - (b[1] - a[1])*(point[0] - a[0])
    #count for floating point approximation
    ret = round(ret, 3)
    if ret > 0: return 1
    if ret < 0: return -1
    return 0



# Reads the input file and stores all the points
# returns a list of tuples representing points
def readInput(inputFile):
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
# returns true if p is inside the circle, works only with normal points
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
#params: the point inserted 'p', the edge to control and maybe legalize 'e', the DAG dag and the actual triangulation 't', minPoint and maxPoint are the actual min and max point
def legalizeEdge(p, e, dag, t, minPoint, maxPoint):
    #get the triangles that have edge e
    firstTriangle = list(dag.keys())[0]
    triangles = findTrianglesEdge(e,t)

    #if the edge is an edge of the first triangle (p0, p-1, p-2) then the edge is legal
    if edgeOfTriangle(e, firstTriangle):
        return

    # k is the point of the triangle adjacent to (p, e[0], e[1]), by definition this point has to exist if the edge is not one of the first triangle
    k = None
    for triangle in triangles:
        for point in triangle:
            if(point != p and point != e[0] and point != e[1]):
                k = point

    #if the 4 points are all real points (no p-1 or p-2) then the normal algorithm has to be executed
    if p[0] >= 0 and e[0][0] >= 0 and e[1][0] >= 0 and k and k[0] >= 0:

        #the edge is illegal if p is inside the circle made by e[0], e[1] and k
        if isInsideCircle(p, [e[0], e[1], k]):
            #replace the triangles
            for triangle in triangles:
                t.remove(triangle)
                dagAppend(dag, triangle, (p,k,e[0]))
                dagAppend(dag, triangle, (p,k,e[1]))
            addTriangle((p,k,e[0]), t)
            addTriangle((p,k,e[1]), t)
            dagLeaf(dag, (p,k,e[0]))
            dagLeaf(dag, (p,k,e[1]))
            legalizeEdge(p, (e[0], k), dag, t, minPoint, maxPoint)
            legalizeEdge(p, (e[1], k), dag, t, minPoint, maxPoint)
        return
        
    # handle special points
    if k:
        
        #check if the qudrilateral made from the 4 points is convex, if it is not then the edge is legal
        if not isConvex(p, k, e):
            return 
        
        #both the highest and the lowest points have to be connected to both the special points, do not swap if this condition gets broken
        #the condition can appear if one point of the edge is special (they cannot be both special because of previous conditions)
        if (e[0][0]<0 or e[1][0]<0):
            
            pswap = e[0] if e[0][0]>=0 else e[1]
            if (minPoint==pswap or maxPoint==pswap):
                #save actual state and try to swap, check if the condition has been broken
                backuptriangulation = t[:]
                for triangle in triangles:
                    backuptriangulation.remove(triangle)
                addTriangle((p,k,e[0]), backuptriangulation)
                addTriangle((p,k,e[1]), backuptriangulation)
                #check if the condition has been broken, if it is broken do not swap, otherwise continue with normal execution and possible swap
                p_1 = False
                p_2 = False
                for triangle in backuptriangulation:
                    if pswap in triangle:
                        if (-1, -1) in triangle:
                            p_1 = True
                        if (-2, -2) in triangle:
                            p_2 = True
                if p_1 == False or p_2 == False:
                    return

        # condition for one or two special points (not both in the edge, already handled this case)
        if(min(p[0], k[0]) >= min(e[0][0], e[1][0])):
            #illegal edge           
            #replace the triangles
            for triangle in triangles:
                t.remove(triangle)
                dagAppend(dag, triangle, (p,k,e[0]))
                dagAppend(dag, triangle, (p,k,e[1]))
            addTriangle((p,k,e[0]), t)
            addTriangle((p,k,e[1]), t)
            dagLeaf(dag, (p,k,e[0]))
            dagLeaf(dag, (p,k,e[1]))
            legalizeEdge(p, (e[0], k), dag, t, minPoint, maxPoint)
            legalizeEdge(p, (e[1], k), dag, t, minPoint, maxPoint)

        return
    return  
    
#returns a list containing the triangles that contain point p, given the point, the dag and the node of the dag where to look
def findTrianglesPoint(p, dag, start, ret=None):
    if ret == None:
        ret = []

    #ret contains the leafs of the DAG that represents triangles containing p (at most 2)
    # for construction every point must be inside the triangle P0,P-1,P-2
    
    if(dag[start] == []): 
        ret.append(start)
    #starting nodes for recursive iteration
    if start not in ret:
        for t in dag[start]:
            if pointInTriangle(p, t):
                findTrianglesPoint(p, dag, t, ret)
    return ret

#return True if "edge" is an edge of the triangle
def edgeOfTriangle(edge, triangle):
    p0 = triangle[0]
    p1 = triangle[1]
    p2 = triangle[2]
    return (p0 in edge and p1 in edge) or (p1 in edge and p2 in edge) or (p2 in edge and p0 in edge)


#returns one or two triangles that have the edge e, given the edge and the triangulation
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

#checks if the quadrilateral made by two adjacent triangles is convex or not
#function used only if at least there is a special point
def isConvex(p0, p1, e):
    e0 = e[0]
    e1 = e[1]
    #by construction, two triangles have an edge in common, one of the 2 triangles has a special vertex, the quadrilateral has to be convex
    if (p0[0]<0 or p1[0]<0) and (e0[0]>= 0 and e1[0] >= 0):
        return True
    #two special points, by constructions they cannot be both in the edge
    if (e0[0]<0 or e1[0]<0) and (p0[0]<0 or p1[0]<0):
        
        if e0==(-2,-2) and p0[0]<0:
            return pointGreater(p1, e1)
        if e0==(-2,-2) and p1[0]<0:
            return pointGreater(p0, e1)
        if e1==(-2,-2) and p0[0]<0:
            return pointGreater(p1, e0)
        if e1==(-2,-2) and p1[0]<0:
            return pointGreater(p0, e0)
        
        if e0==(-1,-1) and p1[0]<0:
            return pointGreater(e1, p0)
        if e0==(-1,-1) and p0[0]<0:
            return pointGreater(e1, p1)
        if e1==(-1,-1) and p1[0]<0:
            return pointGreater(e0, p0)
        if e1==(-1,-1) and p0[0]<0:
            return pointGreater(e0, p1)

    #one point of the edge is a special point, all the others are real
    if (e0[0]<0 or e1[0]<0) and (p0[0]>=0 and p1[0]>=0):
        line = (p0, p1) if pointGreater(p1,p0) else (p1,p0)
        if e0[0]>=0:
            #e1 is a special point
            if e1==(-2,-2) and pointLinePosition(e0, line)==1: return False
            if e1==(-1,-1) and pointLinePosition(e0, line)==-1: return False
        elif e1[0]>=0:
            #e0 is a special point
            if e0==(-2,-2) and pointLinePosition(e1, line)==1: return False
            if e0==(-1,-1) and pointLinePosition(e1, line)==-1: return False
        return True


#add an element to the children of a node of the dag
def dagAppend(dag, node, triangle):
    append = True
    if len(dag[node]) > 0:
        for elem in dag[node]:
            if isSameTriangle(elem, triangle): append = False
    if append:
        dag[node].append(triangle)
    return


#add a new node to the dag
def dagLeaf(dag, triangle):
    found = False
    for k in dag.keys():
        if isSameTriangle(k, triangle): found = True
    if not found:
        dag[triangle] = []
    return