import networkx as nx 
from utils import get_files_with_extension, read_file
from student_utils import data_parser, adjacency_matrix_to_graph


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
    return paths

dir = "C:/Users/Shawn/Desktop/CS 170/project/inputs"
files = get_files_with_extension(dir, 'in')
for inputfile in files:
    paths = findtour(inputfile)


    
