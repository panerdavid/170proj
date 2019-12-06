import networkx as nx
import matplotlib.pyplot as plt
from utils import get_files_with_extension, read_file
from student_utils import data_parser, adjacency_matrix_to_graph

# add inputs to keep track of dropoff locations and homes


def traverse(node, visited, leaves, drive, distances, adjlist, nodedict, disttonode, nodetodist, G, startnode, MST, dropoff_locations, homes):
    adjnodes = adjlist.get(node)
    popleaf = []
    dropLoc = []
    if node in homes:
        dropLoc.append(node)
    for adjnode in adjnodes:
        if adjnode in leaves:
            # add current location to dropoff for leaf homes
            dropLoc.append(node)
            visited += [adjnode]
            popleaf += [adjnode]
            leafdist = nodetodist.pop(adjnode)
            disttonode.pop(leafdist)
            distances.remove(leafdist)
    for pop in popleaf:
        adjnodes.pop(pop)
    visited += [node]
    drive += [node]
    currdist = nodetodist.pop(node)
    disttonode.pop(currdist)
    distances.remove(currdist)
    if not adjnodes:
        if len(distances) == 0:
            backpath = nx.dijkstra_path(MST, node, startnode)
            return drive + backpath
        else:
            fardist = distances.pop()
            farnode = disttonode.pop(fardist)
            pathbetween = nx.dijkstra_path(G, node, farnode)
            drive += pathbetween
            dropoff_locations += dropLoc
            return traverse(farnode, visited, leaves, drive, distances, adjlist, nodedict, disttonode, nodetodist, G, startnode, MST, dropLoc, homes)
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
                    farnode = disttonode.pop(fardist)
                    pathbetween = nx.dijkstra_path(G, node, farnode)
                    drive += pathbetween
                    dropoff_locations += dropLoc

                    return traverse(farnode, visited, leaves, drive, distances, adjlist, nodedict, disttonode, nodetodist, G, startnode, MST, dropLoc, homes)
            nextnode = adjnodes.get(keys[i])
        return traverse(nextnode, visited, leaves, drive, distances, adjlist, nodedict, disttonode, nodetodist, G, startnode, MST, dropLoc, homes)
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
        distances.append(distance)
        # fix duplicate keys
        disttonode[distance] = homenode
        nodetodist[homenode] = distance
    distances.sort(reverse=True)
    mst = nx.compose_all(graphs)
    leaves = [x for x in mst.nodes() if mst.degree(x) == 1]
    visited = []
    drive = []
    adjlist = mst._adj
    startnode = nodedict.get(start)
    tour = traverse(startnode, visited, leaves, drive, distances,
                    adjlist, nodedict, disttonode, nodetodist, G, startnode, mst, [], homes)

    return paths


dir = "C:/Users/Shawn/Desktop/CS 170/project/inputs"
files = get_files_with_extension(dir, 'in')
for inputfile in files:
    paths = findtour(inputfile)
