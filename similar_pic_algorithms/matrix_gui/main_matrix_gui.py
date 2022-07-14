import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

FG = nx.DiGraph()
FG.add_weighted_edges_from([(1, 2, 0.125), (1, 3, 0.75), (2, 4, 1.2), (3, 4, 0.375)])

print(FG.nodes)
print(FG.nodes())

pos = {1: (0, 0), 2: (0, 10), 3: (1, 0), 4: (1, 1), }

nx.draw(FG, with_labels=True,pos=pos, arrows=True)
plt.show()