# plot a set of points and lines
def plot(points, lines = [], figname = "plot"):
    import matplotlib.pyplot as plt
    # plot points
    px = [elem[0] for elem in points]
    py = [elem[1] for elem in points]
    plt.scatter(px, py, color = 'black')
    # plot lines
    for line in lines:
        x = [line[0][0], line[1][0]]
        y = [line[0][1], line[1][1]]
        plt.plot(x, y, linewidth=2, color = 'black')
    
    plt.show()
    plt.savefig("plots/"+figname+".png")


# This script can be used also to plot points from a txt file
import sys
from utils import readInput
if(len(sys.argv) == 2):
    plot(readInput(sys.argv[1]))
else:
    sys.exit("Wrong number of arguments!\nGive the following: inputFile")
    