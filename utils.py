#Checks whether point1 is greater than point2
def pointGreater(point1, point2):
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

#return 1 if the point is in the left, -1 if it is in the right, 0 if it is inside. Returns -2 if considering the wrong line direction
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
    # Check if p is inside
    return (p[0] - cx)**2 + (p[1] - cy)**2 <= radius**2


#legalize the edge if it is illegal 
#params: the point inserted 'p', the edge to control and maybe legalize 'e' and the actual triangulation 't'
def legalizeEdge(p,e,t):
    #let d be the (possible) vertex of the triangle e[0]-e[1]-v, check if d exists and finds its coordinates
    v=None
    for triangle in t:
        if(e[0] in triangle and e[1] in triangle and p not in triangle):
            v = triangle.copy()
            v.remove(e[0])
            v.remove(e[1])
            v = v[0]
    
    #check if e is illegal
    if (not isInsideCircle(p, [e[0], e[1], v])):
        #TODO replace e with p-d in all the triangles containing the edge e (only 2, get from the graph)
        legalizeEdge(p, (e[0], v), t)
        legalizeEdge(p, (e[1], v), t)
    return
    
#returns the triangle containing point p, given the point, the dag and the node of the dag where to look
def findTriangle(p, dag, start):
    if(start not in dag): 
        return start
    for elem in dag[start]:
        if pointInTriangle(p, elem):
            return findTriangle(p, dag, elem)


# legalizeEdge((5,0), ((5,3),(1,0)), [[(5,3), (1,0), (2,3)]])