import numpy as np
from utils import readInput, pointGreater
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import sys

inputFile = None
if(len(sys.argv) == 2):
    inputFile = str(sys.argv[1])
else:
    sys.exit("Wrong number of arguments!\nGive the following: inputFile")
i = 0
input = readInput(inputFile)
p = []
points = None
#highest point p0
p0 = input[0]
for elem in input:
    if pointGreater(elem, p0):
        p0=elem
input.remove(p0)
p.append(p0)


#To debug each stage of the execution
# while(i<len(input)):
#     p.append(input[i])
    # print("EXEC. "+str(i+1)+", points: "+str(p))
    # points = np.array(p)
    # try:
    #     tri = Delaunay(points)
    #     print(points[tri.simplices])
    #     plt.triplot(points[:,0], points[:,1], tri.simplices)
    #     plt.plot(points[:,0], points[:,1], 'o')
    #     plt.show()
    #     plt.savefig("plots/compare"+str(i)+".png")
    #     plt.clf()
    # except:
    #     print("ERROR EXECUTION: "+str(i))
    # i+=1

p = p + input
points = np.array(p)
tri = Delaunay(points)
plt.triplot(points[:,0], points[:,1], tri.simplices)
plt.plot(points[:,0], points[:,1], 'o')
plt.show()
plt.savefig("plots/compare.png")
plt.clf()
