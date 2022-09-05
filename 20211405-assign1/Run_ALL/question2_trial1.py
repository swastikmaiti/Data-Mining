#!/usr/bin/env python
# coding: utf-8

# In[ ]:


print("Started Execution")


# In[1]:


import json
import csv


# ### Read modifed neghbor json data

# In[2]:


f = open('neighbor-districts-modified.json')


# In[3]:


data = json.load(f)


# In[4]:


edge_list = list()


# In[5]:


items = list(data.items())


# ### Go thorough each districts and its neighbors and insert the (district,neighbor) pairs as edge in edge list

# In[6]:


for i in range(len(items)):
    dis = items[i][0]
    neighbor = items[i][1]
    for j in range(len(neighbor)):
        edge = [dis,neighbor[j]]
        edge_list.append(edge)


# ### Print the edges

# In[7]:


print("EDGE LIST")


# In[8]:


for i in range(len(edge_list)):
    print(edge_list[i])


# In[9]:


with open('edge-graph.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(edge_list)


# In[ ]:


print("Ended Execution")

