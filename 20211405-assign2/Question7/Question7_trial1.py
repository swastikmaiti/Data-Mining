#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
import csv
import json
from collections import OrderedDict
import os
import glob
from heapq import nlargest


# ### Collect dtaset for all the states

# In[2]:


path = os.getcwd()
xlsx_files = glob.glob(os.path.join(path, "DDW-C17-*.XLSX"))


# In[3]:


state_dict = dict()


# ### Calculate Count of different Language in Each states

# In[4]:


for f in xlsx_files:
      
    # read the csv file
    df = pd.read_excel(f)
      
    file_name = f.split("\\")[-1]
    file_name = file_name.split(".")[0]
    file_name = file_name+".csv"

    df.to_csv (file_name,index = None,header=True)
    
    df = pd.DataFrame(pd.read_csv(file_name))
    
    language_data = df.loc[5:,:]
    col = ['C-17 POPULATION BY BILINGUALISM AND TRILINGUALISM','Unnamed: 1','Unnamed: 3','Unnamed: 4','Unnamed: 8','Unnamed: 9','Unnamed: 13','Unnamed: 14']
    language_data = language_data[col]
    
    language_data= language_data.set_axis(['State_Code','State_name','Mother_Tongue','Mother_Tongue_Person','Second_Lang','Second_Lang_Person','Third_Lang','Third_Lang_Person'], axis=1, inplace=False)
    language_data = language_data.fillna(0)
    language_data["Mother_Tongue_Person"] = pd.to_numeric(language_data["Mother_Tongue_Person"])
    language_data["Second_Lang_Person"] = pd.to_numeric(language_data["Second_Lang_Person"])
    language_data["Third_Lang_Person"] = pd.to_numeric(language_data["Third_Lang_Person"])

    df1 = language_data.groupby(['State_Code','State_name','Mother_Tongue','Second_Lang','Third_Lang']).sum()
    
    language_count_dict = dict()
    
    
    for i in range(len(language_data)):
        row = language_data.iloc[i]
        State_name = row[1]
        Mother_Tongue_Person = row[3]
        Second_Lang_Person = row[5]
        Third_Lang_Person = row[7]
        lang = None
        count = 0
        if Mother_Tongue_Person!=0:
            lang = row[2]
            count = Mother_Tongue_Person
        elif Second_Lang_Person!=0:
            lang = row[4]
            count = Second_Lang_Person
        elif Third_Lang_Person!=0:
            lang = row[6]
            count = Third_Lang_Person
        val = language_count_dict.get(lang,0)
        new_val = val+count
        language_count_dict[lang] = new_val
    
    state_dict[State_name] = language_count_dict
    
    #print("State = ",State_name)
    #print("language_count_dict = ",language_count_dict)
    #print("-------------------------------------------------------------------------------------------------------")
    #print("")
    #print("")

    


# In[5]:


North = ['JAMMU & KASHMIR','HIMACHAL PRADESH','PUNJAB','CHANDIGARH','UTTARAKHAND','HARYANA','NCT OF DELHI']


# In[6]:


West = ['RAJASTHAN','GUJARAT','DAMAN & DIU','DADRA & NAGAR HAVELI','MAHARASHTRA','GOA']


# In[7]:


Central = ['UTTAR PRADESH','CHHATTISGARH','MADHYA PRADESH']


# In[8]:


East = ['BIHAR','WEST BENGAL','JHARKHAND','ODISHA']


# In[9]:


South = ['ANDHRA PRADESH','KARNATAKA','LAKSHADWEEP','KERALA','TAMIL NADU','PUDUCHERRY']


# In[10]:


North_East = ['SIKKIM','ARUNACHAL PRADESH','NAGALAND','MANIPUR','MIZORAM','TRIPURA','MEGHALAYA','ASSAM','ANDAMAN & NICOBAR ISLANDS']


# In[11]:


Division_dict = {'North':['JAMMU & KASHMIR','HIMACHAL PRADESH','PUNJAB','CHANDIGARH','UTTARAKHAND','HARYANA','NCT OF DELHI'],'West':['RAJASTHAN','GUJARAT','DAMAN & DIU','DADRA & NAGAR HAVELI','MAHARASHTRA','GOA'],'Central':['UTTAR PRADESH','CHHATTISGARH','MADHYA PRADESH'],'East':['BIHAR','WEST BENGAL','JHARKHAND','ODISHA'],'South':['ANDHRA PRADESH','KARNATAKA','LAKSHADWEEP','KERALA','TAMIL NADU','PUDUCHERRY'],'North_East':['SIKKIM','ARUNACHAL PRADESH','NAGALAND','MANIPUR','MIZORAM','TRIPURA','MEGHALAYA','ASSAM','ANDAMAN & NICOBAR ISLANDS']}


# In[12]:


Region_dict = dict()


# ### Group the states into region and sum uo their language counts

# In[13]:


for items in Division_dict.items():
    Div = items[0]
    States = items[1]
    ini_dict = []
    for state in States:
        ini_dict.append(state_dict[state])
    result = {}
    for d in ini_dict:
        for k in d.keys():
            result[k] = result.get(k, 0) + d[k]
    
    ThreeHighest = nlargest(3, result, key = result.get)
    #print("ThreeHighest = ",ThreeHighest)
    Region_dict[Div] = ThreeHighest
    


# ### Sort the data

# In[14]:


Region_dict = OrderedDict(sorted(Region_dict.items()))
Region_dict


# In[15]:


a_file = open("region-india-b.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = ['region', 'language-1', 'language-2', 'language-3'])
writer.writeheader()
writer = csv.writer(a_file)
for key, value in Region_dict.items():
    writer.writerow([key] + value)

a_file.close()


# In[16]:


data1 = pd.read_csv("region-india-b.csv")
data1 = data1.to_string(index=False)
print("Displaying data considering mother tongue + 2nd language + 3rd language")
print("")
print(data1)


# ### Considering Only Mothertongue

# In[ ]:





# In[17]:


for f in xlsx_files:
      
    # read the csv file
    df = pd.read_excel(f)
      
    file_name = f.split("\\")[-1]
    file_name = file_name.split(".")[0]
    file_name = file_name+".csv"

    df.to_csv (file_name,index = None,header=True)
    
    df = pd.DataFrame(pd.read_csv(file_name))
    
    language_data = df.loc[5:,:]
    col = ['C-17 POPULATION BY BILINGUALISM AND TRILINGUALISM','Unnamed: 1','Unnamed: 3','Unnamed: 4']
    language_data = language_data[col]
    
    language_data= language_data.set_axis(['State_Code','State_name','Mother_Tongue','Mother_Tongue_Person'], axis=1, inplace=False)
    language_data = language_data.fillna(0)
    language_data["Mother_Tongue_Person"] = pd.to_numeric(language_data["Mother_Tongue_Person"])

    df1 = language_data.groupby(['State_Code','State_name','Mother_Tongue']).sum()
    
    language_count_dict = dict()
    
    
    for i in range(len(language_data)):
        row = language_data.iloc[i]
        State_name = row[1]
        Mother_Tongue_Person = row[3]
        lang = None
        count = 0
        if Mother_Tongue_Person!=0:
            lang = row[2]
            count = Mother_Tongue_Person
            val = language_count_dict.get(lang,0)
            new_val = val+count
            language_count_dict[lang] = new_val
    
    state_dict[State_name] = language_count_dict
    
    #print("State = ",State_name)
    #print("language_count_dict = ",language_count_dict)
    #print("-------------------------------------------------------------------------------------------------------")
    #print("")
    #print("")


# In[18]:


Region_dict_mothertongue = dict()


# In[19]:


for items in Division_dict.items():
    Div = items[0]
    States = items[1]
    ini_dict = []
    for state in States:
        ini_dict.append(state_dict[state])
    result = {}
    for d in ini_dict:
        for k in d.keys():
            result[k] = result.get(k, 0) + d[k]
    
    ThreeHighest = nlargest(3, result, key = result.get)
    #print("ThreeHighest = ",ThreeHighest)
    Region_dict_mothertongue[Div] = ThreeHighest


# In[20]:


Region_dict_mothertongue = OrderedDict(sorted(Region_dict_mothertongue.items()))
Region_dict_mothertongue


# In[21]:


a_file = open("region-india-a.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = ['region', 'language-1', 'language-2', 'language-3'])
writer.writeheader()
writer = csv.writer(a_file)
for key, value in Region_dict.items():
    writer.writerow([key] + value)

a_file.close()


# In[22]:


print("")


# In[23]:


data1 = pd.read_csv("region-india-a.csv")
data1 = data1.to_string(index=False)
print("Displaying data considering only mother tongue")
print("")
print(data1)

