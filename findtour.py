import networkx as nx
import matplotlib.pyplot as plt
from utils import get_files_with_extension, read_file
from student_utils import data_parser, adjacency_matrix_to_graph


def traverse(node, visited, leaves, drive, distances, adjlist, nodedict, disttonode, nodetodist):
    adjnodes = adjlist.get(node)
    for adjnode in adjnodes:
        if adjnode in leaves:
            visited += [adjnode]
            adjnodes.remove(adjnode)
            leafdist = nodetodist.pop(adjnode)
            disttonode.remove(leafdist)
    if not adjnodes:
        visited += [node]
        drive += [node]
        keys = adjnodes.keys()
        nextnode = adjnodes.get(keys[0])
        i = 1
        while nextnode in visited:
            nextnode = adjnodes.get(keys[i])
            i += 1
        return traverse(nextnode, visited, leaves, drive, distances, adjlist, nodedict, disttonode, nodetodist)
    else:
        visited += [node]
        drive += [node]
        fardist = distances.pop()
        farnode = disttonode.pop(fardist)
        return traverse(farnode, visited, leaves, drive, distances, adjlist, nodedict, disttonode, nodetodist)
    return


def findtour(inputfile):
    data = read_file(inputfile)
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
        distances += (distance)
        disttonode[distance] = homenode
        nodetodist[homenode] = distance
    distances.sort(reverse = True)
    mst = nx.compose_all(graphs)
    leaves = [x for x in mst.nodes() if mst.degree(x) == 1]
    visited = []
    drive = []
    adjlist = mst._adj
    startnode = nodedict.get(start)
    tour = traverse(startnode, visited, leaves, drive, distances, adjlist, nodedict, disttonode, nodetodist)

    return paths


dir = "C:/Users/Shawn/Desktop/CS 170/project/inputs"
files = get_files_with_extension(dir, 'in')
for inputfile in files:
    paths = findtour(inputfile)
