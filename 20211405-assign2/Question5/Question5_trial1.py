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


data = pd.read_excel("DDW-0000C-14.xlsx", sheet_name='Sheet1')
data.head(7)


# In[3]:


data = data.loc[6:,:]
data.drop('Unnamed: 0',axis='columns', inplace=True)
data


# In[4]:


['State_Code','District_Code','Area_Name','Age-group','Total_Persons','Total_Males','Total_Females','Rural_Persons','Rural_Males','Rural_Females','Urban_Persons','Urban_Males','Urban_Females']


# In[5]:


agegroup_data = data.set_axis(['State_Code','District_Code','Area_Name','Age-group','Total_Persons','Total_Males','Total_Females','Rural_Persons','Rural_Males','Rural_Females','Urban_Persons','Urban_Males','Urban_Females'], axis=1, inplace=False)
agegroup_data


# In[6]:


df1 = agegroup_data.groupby(['Area_Name'])
df1.first()


# In[7]:


groups_name = list(df1.groups.keys())
groups_name


# In[8]:


language_data = pd.read_excel("DDW-C18-0000.xlsx", sheet_name='Sheet1')


# In[9]:


language_data.head(7)


# In[10]:


language_data = language_data.loc[5:,:]


# In[11]:


['State_Code','District_Code','Area_Name','Total/Rural/Urban','Age-group','Number_speaking_second_language','Males2','Females2','Number_speaking_third_language','Males3','Females3']


# In[12]:


language_data_total = language_data.set_axis(['State_Code','District_Code','Area_Name','Total/Rural/Urban','Age-group','Number_speaking_second_language','Males2','Females2','Number_speaking_third_language','Males3','Females3'], axis=1, inplace=False)
language_data_total


# ### Calculating State Level Data

# In[13]:


df1 = language_data_total.groupby(['Area_Name'])
df1.first()


# In[14]:


group_state = list(df1.groups.keys())
group_state


# In[15]:


df2 = agegroup_data.groupby(['Area_Name'])
df2.first()


# ### Calculating State Data

# In[16]:


state_dict = dict()
country_dict = dict()


# In[17]:


age_range = {'5-9':['5-9'],'10-14':['10-14'],'15-19':['15-19'],'20-24':['20-24'],'25-29':['25-29'],'30-49':['30-34','35-39','40-44','45-49'],'50-69':['50-54','55-59','60-64','65-69'],'70+':['70-74','75-79','80+']}


# In[18]:


for i in range(len(group_state)):
    key = group_state[i]
    z = df1.get_group(group_state[i])          #retrieve the dataset under that state
    z = z[z['Total/Rural/Urban'] == 'Total']
    k = z.iloc[0]
    State = key
    status=0
    if key=='INDIA':
        status = 1
        key = 'India'
    #print("State = ",key)
    z2 = df2.get_group(key)
    highest_percentage = 0
    for key, value in age_range.items():
        age_gp = key
        row1 = z[z['Age-group'] == age_gp]
        Number_speaking_third_language = int(row1['Number_speaking_third_language'])
        population = 0
        for item in value: # Find valued according to age group in Language dataset 
            pop_key = item
            row2 = z2[z2['Age-group'] == pop_key]
            population = population + int(row2['Total_Persons'])
        percentage = (Number_speaking_third_language/population)*100
        if percentage>highest_percentage:
            Group = age_gp
            highest_percentage = percentage
    if status==0:
        #print("Group = ",Group)
        #print("highest_percentage = ",highest_percentage)
        state_dict[State] = [Group,round(highest_percentage,3)]
    else:
        #print("Group = ",Group)
        #print("highest_percentage = ",highest_percentage)
        country_dict[State] = [Group,round(highest_percentage,3)]
    #print("")


# In[19]:


state_dict


# In[20]:


a_file = open("age-india-b.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = ['state/ut', 'age-group', 'percentage'])
writer.writeheader()
writer = csv.writer(a_file)
for key, value in state_dict.items():
    writer.writerow([key] + value)

a_file.close()


# In[21]:


data = pd.read_csv("age-india-b.csv")
data = data.to_string(index=False)
print("Displaying states and union territories of India data")
print("")
print(data)


# In[22]:


print("")


# In[ ]:





# In[23]:


country_dict


# In[24]:


a_file = open("age-india-a.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = ['Country', 'age-group', 'percentage'])
writer.writeheader()
writer = csv.writer(a_file)
for key, value in country_dict.items():
    writer.writerow([key] + value)

a_file.close()


# In[25]:


data = pd.read_csv("age-india-a.csv")
data = data.to_string(index=False)
print("Displaying over all country data")
print("")
print(data)

