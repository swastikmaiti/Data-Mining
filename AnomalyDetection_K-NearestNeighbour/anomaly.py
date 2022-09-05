#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt   
from numpy import asarray


# In[2]:


data = np.loadtxt('anomaly-s118.dat')


# In[3]:


print("data dimension = ",data.ndim)


# In[4]:


print("data shape = ",data.shape)


# In[5]:


data_1d = list()
for i in range(100):
    for j in range(100):
        data_1d.append(data[i,j])


# In[6]:


plt.plot(data_1d,'o')
plt.show()


# In[7]:


k_neighbor = 4
print()
print(f"Taking k={k_neighbor} for Kth nersert neighbor distance based approch")


# In[8]:


K_Nearest_Neighbor_max_distance = list()


# In[9]:


for i in range(100):
    for j in range(100):
        test_point = data[i,j]
        k_nearest_neighbor = list()
        
        k_nearest_neighbor = abs(data_1d-test_point)
            
        k_nearest_neighbor.sort()
        k_nrearest_dist = k_nearest_neighbor[1:k_neighbor+1]
        K_Nearest_Neighbor_max_distance.append(max(k_nrearest_dist))
            


# In[10]:


K_Nearest_Neighbor_max_distance


# In[11]:


print("The statistics of Kth nearest neighbor distance are as follows:-")
print()


# In[12]:


print("Median of kth nearest neighbor distances = ",np.median(K_Nearest_Neighbor_max_distance))


# In[13]:


print("Mean of kth nearest neighbor distances = ",np.mean(K_Nearest_Neighbor_max_distance))


# In[14]:


print("Maximum of kth nearest neighbor distances = ",np.max(K_Nearest_Neighbor_max_distance))


# In[15]:


print("95th percentile of kth nearest neighbor distances = ",np.percentile(K_Nearest_Neighbor_max_distance,95))


# In[16]:


print("The threshhold distance r is taken as the 95th percentile")
r = np.percentile(K_Nearest_Neighbor_max_distance,95)


# In[17]:


count = 0
for i in range(len(K_Nearest_Neighbor_max_distance)):
    if K_Nearest_Neighbor_max_distance[i]>r:
        count = count+1
print("Number of ouliers consideing r is the 95th percentile = ",count)


# In[18]:


plt.boxplot(K_Nearest_Neighbor_max_distance)


# In[19]:


mask = np.zeros((100,100))
for i in range(100):
    for j in range(100):
        test_point = data[i,j]
        k_nearest_neighbor = list()
        
        k_nearest_neighbor = abs(data_1d-test_point)
            
        k_nearest_neighbor.sort()
        k_nrearest_dist = k_nearest_neighbor[1:k_neighbor+1]
        if max(k_nrearest_dist)> r:
            mask[i,j] = 1


# In[20]:


mask


# In[21]:


np.savetxt('answer-s118.dat', asarray(mask),delimiter=' ',fmt='%d')


# In[22]:


np.savetxt('answer-s118.txt', asarray(mask),delimiter=' ',fmt='%d')


# In[ ]:





# In[ ]:




