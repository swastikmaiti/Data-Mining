#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import collections
from collections import Counter
from collections import OrderedDict
import csv


# In[30]:


import sys
file_name = sys.argv[1]+".csv"
print("Input file name = ",file_name)
test_data = pd.read_csv(file_name,header=None)


# In[3]:


data = pd.read_csv("training-s118.csv",header=None)


# In[4]:


data


# In[5]:


number_of_class = len(pd.unique(data[0]))


# In[6]:


classes = list(pd.unique(data[0]))
classes.sort()


# In[ ]:





# In[7]:


X_train = np.array(data.iloc[: , 1:])


# In[8]:


Y_train = np.array(data.iloc[:,0])


# ### Decision Tree Structure(Monothetic Tree,Information Gain as Mesure)

# In[9]:


class Node:
    def __init__(self,depth = 0,stump=(0,0),parent = None):
        self.depth = depth;
        self.parent = parent;
        self.stump = stump;
        self.left = None;
        self.right = None;
        self.isLeaf = True;
        self.label = 0;
        self.T = None;
    
    def predict(self,data):
        if self.isLeaf:
            for item in classes:
                if self.label==item:
                    return item
        else:
            if data[self.stump[0]]>self.stump[1]:
                return self.right.predict(data)
            else:
                return self.left.predict(data)
    def getEntropy(self, frequency_list):
        entropy = 0
        total = sum(frequency_list)
        proportion_list = [number/total for number in frequency_list]
        for i in range(len(proportion_list)):
            p = proportion_list[i]
            if p>0:
                entropy = entropy - p*np.log(p)
            else:
                entropy = entropy - 0
                
        return entropy;
    
    def getStump(self, X, y):
        
        class_frequency = dict(collections.Counter(y))
        class_frequency = dict(OrderedDict(sorted(class_frequency.items())))

        n = y.size;
        bestObjective = float("-inf");
        
        for i in range(X.shape[1]):
            if self.parent is not None and i == self.parent.stump[0]:
                continue;
            candidateThresholds = np.sort(X[:,i]);
            idx = np.argsort(X[:, i]);
            for j in range(1,candidateThresholds.size-1):
                S1 = y[idx[:j]];
                S2 = y[idx[j:]];
                
                S1_class_frequency = dict(collections.Counter(S1))
                S1_class_frequency = dict(OrderedDict(sorted(S1_class_frequency.items())))
                
                S2_class_frequency = dict(collections.Counter(S2))
                S2_class_frequency = dict(OrderedDict(sorted(S2_class_frequency.items())))
                
                info = (S1.size/n)*self.getEntropy(list(S1_class_frequency.values()))+(S2.size/n)*self.getEntropy(list(S2_class_frequency.values()))
                
                candidateObjective = self.getEntropy(list(class_frequency.values()))-info;
                
                if candidateObjective>bestObjective:
                    bestObjective = candidateObjective
                    bestFeat = i
                    bestThresh = candidateThresholds[j]

        return (bestFeat, bestThresh)
    
    def train(self, X ,y ,maxLeafSize, maxDepth):
        class_frequency = dict(collections.Counter(y))
        class_frequency = dict(OrderedDict(sorted(class_frequency.items())))
        total_count = sum(class_frequency.values())
        assign_class = None
        status = 0
        for items in class_frequency.items():
            key = items[0]
            value = items[1]
            if value/total_count>0.8:  ### 80 percent Node purity is the pruning criteria
                assign_class = key
                status = 1
            
        
        if y.size<maxLeafSize or self.depth>=maxDepth or status==1:  ### Node size and Depth is also used as prining criteria
            
            if status==0:
                assign_class = max(class_frequency, key=class_frequency.get)
            
            self.isLeaf = True
            self.label = assign_class;
        else:
            self.isLeaf = False
            self.stump = self.getStump(X,y);
            self.left = Node(depth = self.depth+1,parent = self)
            self.right = Node(depth = self.depth+1,parent = self)
            discriminant = X[:, self.stump[0]] - self.stump[1]
            self.left.train( X[discriminant <= 0, :], y[discriminant <= 0], maxLeafSize, maxDepth )
            self.right.train( X[discriminant > 0, :], y[discriminant > 0], maxLeafSize, maxDepth )


# ### Define Tree

# In[10]:


class Tree:
    def __init__( self, maxLeafSize = 0, maxDepth = 0 ):
        self.root = Node()
        self.maxLeafSize = maxLeafSize
        self.maxDepth = maxDepth 
        
    def predict( self, data ):
        return self.root.predict( np.array(data) )
    
    def train( self, X, y ):
        self.root.train( X, y, self.maxLeafSize, self.maxDepth )


# In[11]:


DT = Tree(maxLeafSize = 10, maxDepth = 20)


# In[ ]:





# In[12]:


DT.train( X_train, Y_train )


# In[13]:


def predictBatch(Data):
    prediction = [];
    for i in range(Data.shape[0]):
        x  = Data[i,:]
        y_hat = DT.predict(x);
        prediction.append(y_hat);
    return prediction


# In[14]:


def accuracy(X_test,y_test):
    y_predict = predictBatch(X_test);
    y_predict = np.array(y_predict);
    y_test = np.array(y_test);
    z = y_predict==y_test
    count = np.sum(z)
    accu = count/y_test.shape[0]
    return accu


# In[15]:


print("Train accuracy = ",accuracy(X_train,Y_train))


# ### Code for Test Data

# In[25]:


X_test = np.array(test_data.iloc[: , 1:])


# In[26]:


z = predictBatch(X_test)


# In[27]:


textfile = open("classifier-s118.txt", "w")
for element in z:
    textfile.write(element + "\n")
textfile.close()


# In[29]:


a_file = open("classifier-s118.csv", "w",newline="")
writer = csv.writer(a_file)
for value in z:
    writer.writerow([value])

a_file.close()


# In[ ]:





# In[ ]:




