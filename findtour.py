import networkx as nx 
import matplotlib.pyplot as plt
from utils import get_files_with_extension, read_file
from student_utils import data_parser, adjacency_matrix_to_graph

def traverse(node, visited, leaves, drive, distance, adjlist, nodedict):
    node = nodedict.get(nodename)
    adjnodes = adjlist.get(node)
    for adjnode in adjnodes:
        if adjnode in leaves:
            visited += [adjnode]
            adjnodes.remove(adjnode)
    if not adjnodes:

        keys = adjnodes.keys()
        return traverse()
    else:

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
    for home in listh:
        shortestpath = nx.dijkstra_path(G, nodedict.get(home), nodedict.get(start))
        paths += [shortestpath]
        shortestgraph = nx.path_graph(shortestpath)
        graphs += [shortestgraph]
    mst = nx.compose_all(graphs)
    leaves = [x for x in mst.nodes() if mst.degree(x) == 1]
    visited = []
    drive = []
    adjlist = mst._adj
    distance = []
    startnode = nodedict.get(start)
    tour = traverse(startnode, visited, leaves, drive, adjlist, nodedict)
        
    return paths

dir = "C:/Users/Shawn/Desktop/CS 170/project/inputs"
files = get_files_with_extension(dir, 'in')
for inputfile in files:
    paths = findtour(inputfile)


    
