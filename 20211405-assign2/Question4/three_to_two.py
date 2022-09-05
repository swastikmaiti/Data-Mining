#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
import csv
import json
from collections import OrderedDict
from heapq import nlargest
from heapq import nsmallest


# ### Collect and filter dataset for useful values and assign column names

# In[2]:


language_data = pd.read_csv("DDW-C18-0000.csv")


# In[3]:


language_data.head(7)


# In[4]:


language_data = language_data.loc[5:,:]


# In[5]:


['State_Code','District_Code','Area_Name','Total/Rural/Urban','Age-group','Number_speaking_second_language','Males2','Females2','Number_speaking_third_language','Males3','Females3']


# In[6]:


language_data_total = language_data.set_axis(['State_Code','District_Code','Area_Name','Total/Rural/Urban','Age-group','Number_speaking_second_language','Males2','Females2','Number_speaking_third_language','Males3','Females3'], axis=1, inplace=False)
language_data_total


# In[7]:


indexNames = language_data_total[language_data_total['Area_Name'] == 'INDIA' ].index
language_data = language_data_total.drop(indexNames , inplace=False)


# In[8]:


data = pd.read_csv("census_data.csv")
data


# In[9]:


data = data[["Level","Name","TRU","TOT_P","TOT_M","TOT_F"]]


# In[10]:


df = data[data['Level'] == "STATE"]


# In[11]:


census_dataset = df[df['TRU'] == "Total"]
census_dataset


# ### Calculating State Level Data

# In[12]:


df1 = language_data.groupby(['Area_Name'])
df1.first()


# In[13]:


group_state = list(df1.groups.keys())
group_state


# ### Calculating 3-to-2-ratio

# In[14]:


state_ratio = dict()


# In[15]:


for i in range(len(group_state)):
    key = group_state[i]
    z = df1.get_group(group_state[i])          #retrieve the dataset under that state
    z = z.iloc[0]
    Number_speaking_second_language = int(z['Number_speaking_second_language'])
    Number_speaking_third_language = int(z['Number_speaking_third_language'])
    State_Code = z['State_Code']
    State_Name = key
    population_row = census_dataset[census_dataset["Name"] == State_Name]
    population = population_row['TOT_P'].tolist()[0]
    #print("State_Name = ",State_Name)
    #print("State_Code = ",State_Code)
    #print("Number_speaking_second_language = ",Number_speaking_second_language)
    #print("Number_speaking_third_language = ",Number_speaking_third_language)
    #print("population = ",population)
    exactly_one_lang = ((population - Number_speaking_second_language)*100)/population
    exactly_two_lang = ((Number_speaking_second_language - Number_speaking_third_language)*100)/population
    three_or_more_lang = (Number_speaking_third_language*100)/population
    #print("")
    #print("exactly_two_lang = ",exactly_two_lang)
    #print("three_or_more_lang = ",three_or_more_lang)
    ratio = three_or_more_lang/exactly_two_lang
    state_ratio[State_Name] = ratio
    #print("ratio = ",ratio)
    
    #print("")
    #print("")


# In[16]:


state_ratio


# ### Find states with best ratio

# In[17]:


ratio_list = []


# In[18]:


ThreeHighest = nlargest(3, state_ratio, key = state_ratio.get)
ThreeHighest
for i in range(len(ThreeHighest)):
    State = ThreeHighest[i]
    ratio = state_ratio[State]
    #print("State = ",State)
    #print("ratio = ",ratio)
    #print("")
    ratio_list.append(State)


# ### Find states with worst ratio

# In[19]:


ThreeLowest = nsmallest(3, state_ratio, key = state_ratio.get)
ThreeLowest
for i in range(len(ThreeLowest)):
    State = ThreeLowest[i]
    ratio = state_ratio[State]
    #print("State = ",State)
    #print("ratio = ",ratio)
    #print("")
    ratio_list.append(State)


# In[20]:


ratio_list


# In[21]:



print("Displaying top-3(higher to lower ratio) states folllowed by worst-3 states (lower to higher ratio)")
print("3-to-2-ratio")
print("")
for item in ratio_list:
    print(item)


# In[22]:


a_file = open("3-to-2-ratio.csv", "w",newline="")
writer = csv.writer(a_file)
for item in ratio_list:
    writer.writerow([item])

a_file.close()

