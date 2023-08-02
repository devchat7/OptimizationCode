#!/usr/bin/env python
# coding: utf-8

# In[55]:


import pandas as pd
import numpy as np
from gurobipy import *
import gurobipy as gp


# In[274]:


cost_data = pd.read_csv("cost_data.csv")
demand_data = pd.read_csv("demand_data.csv")
product_data = pd.read_csv("product_data.csv")
volume_data = pd.read_csv("volume_data.csv")

m = Model("ProgAss2")

x = m.addVars(range(1,cost_data.shape[0] + 1), range(1,cost_data.shape[1])) #
I = m.addVars(range(1,cost_data.shape[0] + 1), range(1,cost_data.shape[1])) #

n = cost_data.shape[1]-1 # number of products
T = cost_data.shape[0] # number of months

Obj1= gp.quicksum(x[t,i]*cost_data.iloc[t-1,i] 
                  for t in range(1,T+1) 
                  for i in range(1,n+1))
Obj2= gp.quicksum(I[t,i]*product_data.iloc[i-1,2] 
                  for i in range(1,n+1)
                  for t in range(1,T) )
           

m.setObjective(Obj1 + Obj2, GRB.MINIMIZE)

for i in range(1,n + 1):
    m.addConstr(I[1,i] == x[1,i] - demand_data.iloc[0,i])
    
for i in range(1,n + 1):
    for t in range(2,T + 1):
        m.addConstr(I[t,i] == I[t - 1, i] + x[t,i] - demand_data.iloc[t-1,i])
        
for t in range(1,T + 1):
    for i in range (1,n + 1):
        m.addConstr(product_data.iloc[i-2,1]*I[t,i] <= volume_data.iloc[0,1])
        

m.optimize()

print("Opitimal Objective value: $" + str(m.objVal))


# print(cost_data.shape[0])
# for i in range(cost_data.shape[0]) :
#     for j in cost
#     print()


# In[262]:





# In[241]:





# In[ ]:




