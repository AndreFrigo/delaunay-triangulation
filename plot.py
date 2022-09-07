# plot a set of points and lines
def plot(points, lines = [], figname = "plot"):
    import matplotlib.pyplot as plt
    plt.clf()
    # plot points
    px = [elem[0] for elem in points]
    py = [elem[1] for elem in points]
    plt.scatter(px, py, color = 'black')
    # plot lines
    for line in lines:
        x = [line[0][0], line[1][0]]
        y = [line[0][1], line[1][1]]
        plt.plot(x, y, linewidth=1, color = 'black')
    
    plt.savefig("plots/"+figname+".png")
    return

def plotDebug(name, triangulation):
    p=[]
    edges=[]
    for elem in triangulation:
        # print("ELEM: "+str(elem))
        p.append(elem[0])
        p.append(elem[1])
        p.append(elem[2])
        edges.append((elem[0],elem[1]))
        edges.append((elem[0],elem[2]))
        edges.append((elem[2],elem[1]))
    
    edges = [elem for elem in edges if (-1,-1) not in elem and (-2,-2) not in elem]

    plot(list(set([e for e in p if e!= (-1,-1) and e!= (-2,-2)])), edges, str(name))
    return


# # This script can be used also to plot points from a txt file
# import sys
# from utils import readInput
# if(len(sys.argv) == 2):
#     plot(readInput(sys.argv[1]))
# else:
#     sys.exit("Wrong number of arguments!\nGive the following: inputFile")
    