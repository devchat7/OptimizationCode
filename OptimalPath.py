import pandas as pd
import numpy as np
from gurobipy import *
import gurobipy as gp
import networkx as nx
import matplotlib.pyplot as plt

graph = pd.read_csv("hw3_graph.csv")
items = len(graph)
arr = [(graph['origin'][i],graph['destination'][i]) for i in range(items)]
G = nx.Graph()
G.add_edges_from(arr)
N = len(graph)

m = Model("ProgAss3")
x = m.addVars(G.edges, vtype=GRB.BINARY)
c = {(i,j) : graph[(graph['origin'] == i) & (graph['destination'] == j)]['length'].iloc[0] for (i,j) in arr}
m.setObjective(gp.quicksum(c[i,j] * x[i,j] for i,j in G.edges ), GRB.MINIMIZE )

for node in G.nodes:
    if node not in [1,N]:
        expr1 = gp.quicksum(x[i,node] for i in G.predecessors(node))
        expr2 = gp.quicksum(x[node, j] for j in G.successors(node))
        m.addLConstr(expr1 - expr2 == 0)

m.addConstr(gp.quicksum(x[1,j] for j in G.successors(1)) - gp.quicksum(x[i,1] for i in G.predecessors(1)) == 1)

m.addConstr(gp.quicksum(x[N,j] for j in G.successors(N)) - gp.quicksum(x[i,N] for i in G.predecessors(N)) == -1)  

m.optimize()

path_edges = [(i,j) for i,j in G.edges if x[i,j].x > 0.5 ]
path_edges = list(path_edges)
arr2 = [1]

for edge in path_edges:
    if edge[0] == arr2[-1]:
        arr2.append(edge[1])
    else:
        arr2.append(edge[0])
        arr2.append(edge[1])

print('Path:', end=' ')
for point in arr2:
    if point == N:
        print(N-1)
        break
    print(point, end=' -> ')
    
objective_value = m.getAttr(gp.GRB.Attr.ObjVal)
print("Objective Value:" , objective_value)
