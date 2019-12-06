import networkx as nx
import matplotlib.pyplot as plt
from utils import get_files_with_extension, read_file
from student_utils import data_parser, adjacency_matrix_to_graph
import os.path

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

def traverse(node, visited, leaves, drive, distances, adjlist, nodedict, dist2node, node2dist, G, startnode, MST, homes, dropdict):
    adjnodes = adjlist.get(node)
    popleaf = []
    dropLoc = []
    if node in homes:
        dropLoc.append(node)
    for adjnode in adjnodes:
        if not adjnode in visited:
            if adjnode in leaves:
                visited += [adjnode]
                dropLoc.append(adjnode)
                popleaf += [adjnode]
                leafdist = node2dist.pop(adjnode)
                value = dist2node.pop(leafdist)
                dist2node[leafdist] = value[1:]
                if leafdist in distances:
                    distances.remove(leafdist)
    for pop in popleaf:
        adjnodes.pop(pop)
    dropdict[node] = dropLoc
    visited += [node]
    drive += [node]
    if startnode in homes:
        if not node in visited:
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
            if fardist == 0:
                return drive, dropdict
            value = dist2node.pop(fardist)
            dist2node[fardist] = value[1:]
            farnode = value[0]
            i = 0
            while farnode in visited:
                i += 1
                farnode = value[i]
                dist2node[fardist] = value[:i - 1] + value[i + 1:]
            pathbetween = nx.dijkstra_path(G, node, farnode)
            drive += pathbetween[1:-1]
            return traverse(farnode, visited, leaves, drive, distances, adjlist, nodedict,
                            dist2node, node2dist, G, startnode, MST, homes, dropdict)
    else:
        keys = list(adjnodes.keys())
        i = 0
        nextnode = keys[i]
        while nextnode in visited:
            i += 1
            if i == MST.degree(node):
                if len(set(visited)) == nx.number_of_nodes(MST):
                    backpath = nx.dijkstra_path(MST, node, startnode)
                    return drive + backpath, dropdict
                else:
                    if not distances:
                        backpath = nx.dijkstra_path(MST, node, startnode)
                        return drive + backpath, dropdict
                    fardist = distances.pop()
                    value = dist2node.pop(fardist)
                    dist2node[fardist] = value[1:]
                    while not value:
                        if not distances:
                            backpath = nx.dijkstra_path(MST, node, startnode)
                            return drive + backpath, dropdict
                        fardist = distances.pop()
                        value = dist2node.pop(fardist)
                        dist2node[fardist] = value[1:]
                    farnode = value[0]
                    i = 0
                    while farnode in visited:
                        i += 1
                        if i > len(value) - 1:
                            if not distances:
                                backpath = nx.dijkstra_path(MST, node, startnode)
                                return drive + backpath, dropdict
                            fardist = distances.pop()
                            value = dist2node.pop(fardist)
                            dist2node[fardist] = value[1:]
                            while not value:
                                if not distances:
                                    backpath = nx.dijkstra_path(MST, node, startnode)
                                    return drive + backpath, dropdict
                                fardist = distances.pop()
                                value = dist2node.pop(fardist)
                                dist2node[fardist] = value[1:]
                            farnode = value[0]
                        else:
                            farnode = value[i]
                            dist2node[fardist] = value[:i - 1] + value[i + 1:]
                    pathbetween = nx.dijkstra_path(G, node, farnode)
                    drive += pathbetween[1:-1]
                    return traverse(farnode, visited, leaves, drive, distances, adjlist, nodedict,
                                    dist2node, node2dist, G, startnode, MST, homes, dropdict)
            nextnode = keys[i]
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
    list_home_nodes = []
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
        list_home_nodes += [homenode]
    distances.sort(reverse=False)
    mst = nx.compose_all(graphs)
    leaves = [x for x in mst.nodes() if mst.degree(x) == 1]
    visited = []
    drive = []
    adjlist = mst._adj
    startnode = nodedict.get(start)
    dropdict = {}
    tour, dropdict = traverse(startnode, visited, leaves, drive, distances,
                              adjlist, nodedict, disttonode, nodetodist, G, startnode, mst, list_home_nodes, dropdict)
    if len(tour) == 2:
        return tour[0], dropdict
    else:
        return tour, dropdict


dir = "C:/Users/Shawn/Desktop/CS 170/project/inputs"
files = get_files_with_extension(dir, 'in')
for inputfile in files:
    print(inputfile)
    tour, dropdict = findtour(inputfile)


