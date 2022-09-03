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

# Checks whether a point is on a line 
# point has the following format: (x,y)
# line has the following format: (point0, point1), where point0 and point1 are points
# the function returns true if the points is on the line, false otherwise
def pointOnLine(point, line):
    slope = (line[1][1] - line[0][1]) / (line[1][0] - line[0][0])
    on = (point[1] - line[0][1]) == slope * (point[0] - line[0][0])
    between = (min(line[0][0], line[1][0]) <= point[0] <= max(line[0][0], line[1][0])) and (min(line[0][1], line[1][1]) <= point[1] <= max(line[0][1], line[1][1]))
    return (on and between)


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
    triangles = findTrianglesEdge(e, dag, firstTriangle)
    # k is the point of the triangle adjacent to (p, e[0], e[1])
    k = None
    for triangle in triangles:
        for point in triangle:
            if(point != p and point != e[0] and point != e[1]):
                k = point

    #if the edge is an edge of the first triangle (p0, p-1, p-2) then the edge is legal
    if edgeOfTriangle(e, firstTriangle):
        return
    
    #if the 4 points are all real points (no p-1 or p-2) then the normal algorithm has to be executed
    if p[0] >= 0 and e[0][0] >= 0 and e[1][0] >= 0 and k and k[0] >= 0:
        #the edge is illegal if p is inside the circle made by e[0], e[1] and k
        if isInsideCircle(p, [e[0], e[1], k]):
            #replace the triangles
            for triangle in triangles:
                t.remove(triangle)
                dag[triangle].append((p,k,e[0]), (p,k,e[1]))
            t.append((p,k,e[0]))
            t.append((p,k,e[1]))
            dag[(p,k,e[0])] = []
            dag[(p,k,e[1])] = []
            legalizeEdge(p, (e[0], k), dag, t)
            legalizeEdge(p, (e[1], k), dag, t)
        return
        
    
    # legal iff min(p, k) < min(e[0], e[1])
    if k:
        min1 = p if not pointGreater(p, k) else k
        min2 = e[0] if not pointGreater(e[0], e[1]) else e[1]
        if pointGreater(min2, min1):
            #illegal edge
            #replace the triangles
            for triangle in triangles:
                t.remove(triangle)
                dag[triangle].append((p,k,e[0]), (p,k,e[1]))
            t.append((p,k,e[0]))
            t.append((p,k,e[1]))
            dag[(p,k,e[0])] = []
            dag[(p,k,e[1])] = []
            legalizeEdge(p, (e[0], k), dag, t)
            legalizeEdge(p, (e[1], k), dag, t)
            return
        return
    sys.exit("ERROR in legalizeEdge\n")
    return  
    
#returns a list containing the triangle (or 2 triangles in case of point in a shared edge) containing point p, given the point, the dag and a list of nodes of the dag where to look
def findTrianglesPoint(p, dag, start, ret=[]):
    #ret contains the leafs of the DAG that represents triangles containing p (at most 2)
    # for construction every point must be inside the triangle P0,P-1,P-2
    for elem in start:
        if(dag[elem] == []): 
            ret.append(elem)
    #starting nodes for recursive iteration
    newstart=[]
    for s in [item for item in start if item not in ret]:  
        for t in dag[s]:
            if pointInTriangle(p, t):
                newstart.append(t)
    if newstart != []:
        findTrianglesPoint(p, dag, newstart, ret)
    return ret

#return True if "edge" is an edge of the triangle
def edgeOfTriangle(edge, triangle):
    p0 = triangle[0]
    p1 = triangle[1]
    p2 = triangle[2]
    return (p0 in edge and p1 in edge) or (p1 in edge and p2 in edge) or (p2 in edge and p0 in edge)


#returns one or two triangles that have the edge e, given the edge, the dag and a list of nodes of the dag where to look
def findTrianglesEdge(edge, dag, start, ret=[]):
    #ret contains the leafs of the DAG that represents triangles containing edge (at most 2)
    for elem in start:
        if(dag[elem] == []): 
            ret.append(elem)
    #starting nodes for recursive iteration
    newstart=[]
    for s in [item for item in start if item not in ret]:  
        for t in dag[s]:
            if edgeOfTriangle(edge, t):
                newstart.append(t)
    if newstart != []:
        findTrianglesEdge(edge, dag, newstart, ret)
    return ret
