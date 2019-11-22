import Networkx as nx
import matplotlib.pyplot as plt 
graph = nx.fast_gnp_random_graph(50, 0.1, False)
nx.draw(graph, with_labels=True) 
plt.show() 
matrix = nx.convert_matrix.to_numpy_matrix(graph)
print(matrix)