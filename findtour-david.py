import networkx as nx
import matplotlib.pyplot as plt
from utils import get_files_with_extension, read_file
from student_utils import data_parser, adjacency_matrix_to_graph
import os.path

# path as a tour, dict =  {node [dest]}
# Soda Dwinelle Campanile Barrows Soda
# 3
# Soda Cory
# Dwinelle Wheeler RSF
# Campanile Campanile
def output(inputFileName, tour, dropDict):
    output = inputFileName.replace(".in", ".out")
    output = output.replace("/Users/panerdavid/Desktop/170/inputs_copy/", "")
    savePath = "/Users/panerdavid/Desktop/170/outputs/"
    completeName = os.path.join(savePath, output)
    print(completeName)
    f = open(completeName, "w+")
    for location in tour:
        f.write(location + " ")
    f.write("\n")
    f.write(str(len(dropDict)) + "\n")
    
    for dropoff in dropDict:
        f.write(dropoff)
        for home in dropDict[dropoff]:
            f.write(" " + home)
        f.write("\n")

    f.close()

def output(inputFileName, tour, dropDict):
    output = inputFileName.replace(".in", ".out")
    output = output.replace("/Users/panerdavid/Desktop/170/inputs_copy/", "")
    savePath = "/Users/panerdavid/Desktop/170/outputs/"
    completeName = os.path.join(savePath, output)
    print(completeName)
    f = open(completeName, "w+")
    for location in tour:
        f.write()
    f.close()


def traverse(node, visited, leaves, drive, distances, adjlist, nodedict, disttonode, nodetodist, G, startnode, MST, dropoff_locations, homes):
    adjnodes = adjlist.get(node)
    popleaf = []
    dropLoc = []
    if node in homes:
        dropLoc.append(node)
    for adjnode in adjnodes:
        if adjnode in leaves:
            visited += [adjnode]
            dropLoc.append(node)
            popleaf += [adjnode]
            leafdist = nodetodist.pop(adjnode)
            value = disttonode.pop(leafdist)
            disttonode[leafdist] = value[1:]
            distances.remove(leafdist)
    for pop in popleaf:
        adjnodes.pop(pop)
    visited += [node]
    drive += [node]
    currdist = nodetodist.pop(node)
    value = disttonode.pop(currdist)
    disttonode[currdist] = value[1:]
    distances.remove(currdist)
    if not adjnodes:
        if len(distances) == 0:
            backpath = nx.dijkstra_path(MST, node, startnode)
            return drive + backpath
        else:
            fardist = distances.pop()
            value = disttonode.pop(fardist)
            disttonode[fardist] = value[1:]
            farnode = value[0]
            pathbetween = nx.dijkstra_path(G, node, farnode)
            drive += pathbetween
            dropoff_locations += dropLoc
            return traverse(farnode, visited, leaves, drive, distances, adjlist, nodedict, disttonode, nodetodist, G, startnode, MST, dropoff_locations, homes)
    else:
        keys = adjnodes.keys()
        i = 0
        nextnode = adjnodes.get(keys[i])
        while nextnode in visited:
            i += 1
            if i == MST.degree(node):
                if len(visited) == nx.number_of_nodes(MST):
                    backpath = nx.dijkstra_path(MST, node, startnode)
                    return drive + backpath
                else:
                    fardist = distances.pop()
                    value = disttonode.pop(fardist)
                    disttonode[fardist] = value[1:]
                    farnode = value[0]
                    pathbetween = nx.dijkstra_path(G, node, farnode)
                    drive += pathbetween
                    dropoff_locations += dropLoc
                    return traverse(farnode, visited, leaves, drive, distances, adjlist, nodedict, disttonode, nodetodist, G, startnode, MST, dropoff_locations, homes)
            nextnode = adjnodes.get(keys[i])
        return traverse(nextnode, visited, leaves, drive, distances, adjlist, nodedict, disttonode, nodetodist, G, startnode, MST, dropoff_locations, homes)


def findtour(inputfile):
    data = read_file(inputfile)
    # need this to create output file
    name = inputfile.name
    numl, numh, listl, listh, start, matrix = data_parser(data)
    G, message = adjacency_matrix_to_graph(matrix)
    nodes = G.__iter__()
    nodedict = {}
    for i in range(numl):
        nodedict[listl[i]] = next(nodes)
    paths = []
    graphs = []
    distances = []
    disttonode = {}
    nodetodist = {}
    for home in listh:
        homenode = nodedict.get(home)
        distance, shortestpath = nx.single_source_dijkstra(
            G, homenode, nodedict.get(start))
        paths += [shortestpath]
        shortestgraph = nx.path_graph(shortestpath)
        graphs += [shortestgraph]
        distances.append(distance)
        # fix duplicate keys
        if not distance in disttonode:
            disttonode[distance] = [homenode]
        else:
            disttonode[distance].append(homenode)
        nodetodist[homenode] = distance
    distances.sort(reverse=True)
    mst = nx.compose_all(graphs)
    leaves = [x for x in mst.nodes() if mst.degree(x) == 1]
    visited = []
    drive = []
    adjlist = mst._adj
    startnode = nodedict.get(start)
    tour = traverse(startnode, visited, leaves, drive, distances,
                    adjlist, nodedict, disttonode, nodetodist, G, startnode, mst, [], listh)
    return tour


dir = "C:/Users/Shawn/Desktop/CS 170/project/inputs"
files = get_files_with_extension(dir, 'in')
for inputfile in files:
    paths = findtour(inputfile)


