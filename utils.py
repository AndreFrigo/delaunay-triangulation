# Checks whether a point is on a line 
# point has the following format: (x,y)
# line has the following format: (point0, point1), where point0 and point1 are points
# the function returns true if the points is on the line, false otherwise
def pointOnLine(point, line):
    slope = (line[1][1] - line[0][1]) / (line[1][0] - line[0][0])
    on = (point[1] - line[0][1]) == slope * (point[0] - line[0][0])
    between = (min(line[0][0], line[1][0]) <= point[0] <= max(line[0][0], line[1][0])) and (min(line[0][1], line[1][1]) <= point[1] <= max(line[0][1], line[1][1]))
    return (on and between)

# Calculates the area of a triangle
# triangle has the following format: (p1, p2, p3), where p1, p2, p3 are the vertices 
def area(triangle):
    x1, y1 = triangle[0]
    x2, y2 = triangle[1]
    x3, y3 = triangle[2]
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

# Checks whether a point is inside a triangle (also on the edges)
# point has the following format: (x,y)
# triangle has the following format: (p1, p2, p3), where p1, p2, p3 are the vertices 
def pointInTriangle(point, triangle):
    A = area (triangle)
    A1 = area ((point, triangle[1], triangle[2]))
    A2 = area ((point, triangle[0], triangle[2]))
    A3 = area ((point, triangle[0], triangle[1]))
    if(A == A1 + A2 + A3):
        return True
    else:
        return False
