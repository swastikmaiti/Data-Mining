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


data = pd.read_excel("DDW-0000C-08.xlsx")
data.head(7)


# In[3]:


data.columns.values


# In[4]:


data = data.loc[6:,:]
data.drop('Unnamed: 0',axis='columns', inplace=True)
data


# In[5]:


col = ['State_Code','District_Code','Area_Name','Total/Rural/Urban','Age-group','Total','Total_male','Total_female','Illiterate','Illiterate_male','Illiterate_female','Literate','Literate_male','Literate_female','Literate without education level','Literate without education level_male','Literate without education level_female','Literate but below primary','Literate but below primary_male','Literate but below primary_female','Primary but below middle','Primary but below middle_male','Primary but below middle_female','Middle but below matric/secondary','Middle but below matric/secondary_male','Middle but below matric/secondary_female','Matric/Secondary but below graduate','Matric/Secondary but below graduate_male','Matric/Secondary but below graduate_female','Higher secondary/Intermediate','Higher secondary/Intermediate_male','Higher secondary/Intermediate_female','Non_Technical','Non_Technical_male','Non_Technical_female','Technical','Technical_male','Technical_female','Graduate and above','Graduate and above_male','Graduate and above_female','Unclassified','Unclassified_male','Unclassified_female']
len(col)


# In[6]:


literacy_data = data.set_axis(col, axis=1, inplace=False)
literacy_data


# In[7]:


df1 = literacy_data.groupby(['Area_Name'])
df1.first()


# In[8]:


groups_name = list(df1.groups.keys())
groups_name


# In[9]:


language_data = pd.read_excel("DDW-C19-0000.xlsx", sheet_name='Sheet1')


# In[10]:


language_data.head(7)


# In[11]:


language_data = language_data.loc[5:len(language_data)-4,:]


# In[12]:


['State_Code','District_Code','Area_Name','Total/Rural/Urban','Educational level','Number_speaking_second_language','Males2','Females2','Number_speaking_third_language','Males3','Females3']


# In[13]:


language_data_total = language_data.set_axis(['State_Code','District_Code','Area_Name','Total/Rural/Urban','Educational level','Number_speaking_second_language','Males2','Females2','Number_speaking_third_language','Males3','Females3'], axis=1, inplace=False)
language_data_total


# ### Calculating State Level Data

# In[14]:


df1 = language_data_total.groupby(['Area_Name'])
df1.first()


# In[15]:


group_state = list(df1.groups.keys())
group_state


# In[16]:


df2 = literacy_data.groupby(['Area_Name'])
df2.first()


# ### Calculating State Data

# In[17]:


state_dict = dict()
country_dict = dict()


# In[18]:


temp = df1.get_group(group_state[0])
#temp
list1 = temp['Educational level'].tolist()[1:8]
list1.remove('Literate')
list1


# In[19]:


#age_range = {'5-9':['5-9'],'10-14':['10-14'],'15-19':['15-19'],'20-24':['20-24'],'25-29':['25-29'],'30-49':['30-34','35-39','40-44','45-49'],'50-69':['50-54','55-59','60-64','65-69'],'70+':['70-74','75-79','80+']}


# In[20]:


for i in range(len(group_state)):
    key = group_state[i]
    z = df1.get_group(group_state[i])          #retrieve the dataset under that state
    z = z[z['Total/Rural/Urban'] == 'Total']
    k = z.iloc[0]
    State = key
    status = 0
    if key=='INDIA':
        status = 1
    #print("State = ",key)
    z2 = df2.get_group(key)
    z2 = z2[z2['Total/Rural/Urban'] == 'Total']
    z2 = z2.iloc[0:1]
    highest_percentage = 0
    for key in list1:
        row1 = z[z['Educational level'] == key]
        Number_speaking_third_language = int(row1['Number_speaking_third_language'])
        population = 0
        if key=='Matric/Secondary but below graduate':  # Find values according to literacy group in Language dataset 
            p1 = int(z2['Matric/Secondary but below graduate'])
            p2 = int(z2['Non_Technical'])
            p3 = int(z2['Technical'])
            p4 = int(z2['Higher secondary/Intermediate'])
            population = p1+p2+p3+p4
        else:
            population = int(z2[key])
            
        percentage = (Number_speaking_third_language*100)/population
        
        if percentage>highest_percentage:
            Group = key
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


# In[21]:


state_dict


# In[22]:


a_file = open("literacy-india-b.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = ['state/ut', 'literacy-group', 'percentage'])
writer.writeheader()
writer = csv.writer(a_file)
for key, value in state_dict.items():
    writer.writerow([key] + value)

a_file.close()


# In[23]:


data = pd.read_csv("literacy-india-b.csv")
data = data.to_string(index=False)
print("Displaying states and union territories of India data")
print("")
print(data)


# In[24]:


country_dict


# In[25]:


a_file = open("literacy-india-a.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = ['Country', 'literacy-group', 'percentage'])
writer.writeheader()
writer = csv.writer(a_file)
for key, value in country_dict.items():
    writer.writerow([key] + value)

a_file.close()


# In[26]:


data = pd.read_csv("literacy-india-a.csv")
data = data.to_string(index=False)
print("Displaying over all country data")
print("")
print(data)

