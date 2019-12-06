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
    pathsFromStart = nx.single_source_dijkstra(nodedict.get(start), node for node in nodedict.keys())
     #{v: k for k, v in my_map.items()}
    pathsFromStart = {dist: node for node, dist in pathsFromStart.items()}
    decreasingDist = pathsfromStart.sort().reverse()

    mst = nx.compose_all(graphs)
    leaves = [x for x in mst.nodes() if mst.degree(x) == 1]
    #dfsdict = nx.dfs_successors(mst, nodedict.get(start))
    visited = []
     drive = []
    adjlist = mst._adj
    distance = []
    startnode = nodedict.get(start)
    tour = traverse(startnode, visited, leaves, drive, adjlist, nodedict)
    startnode = nodedict.get(start)
    adjlist = mst.nodes._adj
    # counter = 0
    # while counter < len(nodedict):
    mstNodes = list(mst)
    traversalPath = []

    while mstNodes:
        path_so_far = adjlist
        if node in leaves:

    return paths

dir = "C:/Users/Shawn/Desktop/CS 170/project/inputs"
files = get_files_with_extension(dir, 'in')
for inputfile in files:
    paths = findtour(inputfile)


    
