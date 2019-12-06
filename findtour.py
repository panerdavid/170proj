import networkx as nx
import matplotlib.pyplot as plt
from utils import get_files_with_extension, read_file
from student_utils import data_parser, adjacency_matrix_to_graph


def traverse(node, visited, leaves, drive, distances, adjlist, nodedict, dist2node, node2dist, G, startnode, MST, homes, dropdict):
    adjnodes = adjlist.get(node)
    popleaf = []
    dropLoc = []
    if node in homes:
        dropLoc.append(node)
    for adjnode in adjnodes:
        if adjnode in leaves:
            visited += [adjnode]
            dropLoc.append(adjnode)
            popleaf += [adjnode]
            leafdist = node2dist.pop(adjnode)
            value = dist2node.pop(leafdist)
            dist2node[leafdist] = value[1:]
            distances.remove(leafdist)
    for pop in popleaf:
        adjnodes.pop(pop)
    dropdict[node] = dropLoc
    visited += [node]
    drive += [node]
    #starting node not included in node2dist (101_100)
    currdist = node2dist.pop(node)
    value = dist2node.pop(currdist)
    dist2node[currdist] = value[1:]
    distances.remove(currdist)
    if not adjnodes:
        if len(distances) == 0:
            backpath = nx.dijkstra_path(MST, node, startnode)
            return drive + backpath, dropdict
        else:
            fardist = distances.pop()
            value = dist2node.pop(fardist)
            dist2node[fardist] = value[1:]
            farnode = value[0]
            pathbetween = nx.dijkstra_path(G, node, farnode)
            drive += pathbetween
            return traverse(farnode, visited, leaves, drive, distances, adjlist, nodedict, 
                dist2node, node2dist, G, startnode, MST, homes, dropdict)
    else:
        keys = adjnodes.keys()
        i = 0
        nextnode = adjnodes.get(keys[i])
        while nextnode in visited:
            i += 1
            if i == MST.degree(node):
                if len(visited) == nx.number_of_nodes(MST):
                    backpath = nx.dijkstra_path(MST, node, startnode)
                    return drive + backpath, dropdict
                else:
                    fardist = distances.pop()
                    value = dist2node.pop(fardist)
                    dist2node[fardist] = value[1:]
                    farnode = value[0]
                    pathbetween = nx.dijkstra_path(G, node, farnode)
                    drive += pathbetween
                    return traverse(farnode, visited, leaves, drive, distances, adjlist, nodedict, 
                        dist2node, node2dist, G, startnode, MST, homes, dropdict)
            nextnode = adjnodes.get(keys[i])
        return traverse(nextnode, visited, leaves, drive, distances, adjlist, nodedict, 
            dist2node, node2dist, G, startnode, MST, homes, dropdict)


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
    dropdict = {}
    tour, dropdict = traverse(startnode, visited, leaves, drive, distances,
                    adjlist, nodedict, disttonode, nodetodist, G, startnode, mst, listh, dropdict)
    if len(tour) == 2:
        return tour[0], dropdict
    else:
        return tour, dropdict


dir = "C:/Users/Shawn/Desktop/CS 170/project/inputs"
files = get_files_with_extension(dir, 'in')
for inputfile in files:
    tour, dropdict = findtour(inputfile)
