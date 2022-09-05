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


# In[13]:


#indexNames = language_data_total[language_data_total['Area_Name'] == 'INDIA' ].index
#language_data = language_data_total.drop(indexNames , inplace=False)


# In[14]:


#data = pd.read_csv("census_data.csv")
#data


# In[15]:


#data = data[["Level","Name","TRU","TOT_P","TOT_M","TOT_F"]]


# In[16]:


#df = data[data['Level'] == "STATE"]


# In[17]:


#census_dataset = df[df['TRU'] == "Total"]
#census_dataset


# ### Calculating State Level Data

# In[18]:


df1 = language_data_total.groupby(['Area_Name'])
df1.first()


# In[19]:


group_state = list(df1.groups.keys())
group_state


# In[20]:


df2 = agegroup_data.groupby(['Area_Name'])
df2.first()


# ### Calculating State Data

# In[21]:


state_dict = dict()
country_dict = dict()
state_dict_gender = dict()
country_dict_gender = dict()


# In[22]:


age_range = {'5-9':['5-9'],'10-14':['10-14'],'15-19':['15-19'],'20-24':['20-24'],'25-29':['25-29'],'30-49':['30-34','35-39','40-44','45-49'],'50-69':['50-54','55-59','60-64','65-69'],'70+':['70-74','75-79','80+']}


# In[23]:


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
    highest_percentage_male = 0
    highest_percentage_female = 0
    for key, value in age_range.items():
        age_gp = key
        row1 = z[z['Age-group'] == age_gp]
        #Number_speaking_third_language = int(row1['Number_speaking_third_language'])
        
        Number_speaking_third_language_male = int(row1['Males3'])
        Number_speaking_third_language_female = int(row1['Females3'])
        
        population = 0
        population_male = 0
        population_female = 0
        for item in value:      # Find values according to afe group in Language dataset 
            pop_key = item
            row2 = z2[z2['Age-group'] == pop_key]
            population = population + int(row2['Total_Persons'])
            
            population_male = population_male + int(row2['Total_Males'])
            population_female = population_female + int(row2['Total_Females'])
            
        #percentage = Number_speaking_third_language/population
        
        percentage_male = Number_speaking_third_language_male/population_male
        percentage_female = Number_speaking_third_language_female/population_female
        
        #if percentage>highest_percentage:
         #   Group = age_gp
          #  highest_percentage = percentage
        
        if percentage_male>highest_percentage_male:
            Group_male = age_gp
            highest_percentage_male = percentage_male
            
        if percentage_female>highest_percentage_female:
            Group_female = age_gp
            highest_percentage_female = percentage_female
        
        
    if status==0:
        #print("Group_male = ",Group_male)
        #print("highest_percentage_male = ",highest_percentage_male)
        #print("")
        #print("Group_female = ",Group_female)
        #print("highest_percentage_female = ",highest_percentage_female)
        state_dict_gender[State]=[Group_male,round(highest_percentage_male,3),Group_female,round(highest_percentage_female,3)]
    else:
        #print("Group_male = ",Group_male)
        #print("highest_percentage_male = ",highest_percentage_male)
        #print("")
        #print("Group_female = ",Group_female)
        #print("highest_percentage_female = ",highest_percentage_female)
        state_dict_gender[State]=[Group_male,round(highest_percentage_male,3),Group_female,round(highest_percentage_female,3)]
        country_dict_gender[State]=[Group_male,round(highest_percentage_male,3),Group_female,round(highest_percentage_female,3)]
    #print("---------------------------------------------------------------------------")
    #print("")


# In[ ]:





# In[24]:


state_dict_gender


# In[25]:


a_file = open("age-gender-a.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = ['state/ut', 'age-group-males', 'ratio-males', 'age-group-females', 'ratio-females'])
writer.writeheader()
writer = csv.writer(a_file)
for key, value in state_dict_gender.items():
    writer.writerow([key] + value)

a_file.close()


# In[26]:


data = pd.read_csv("age-gender-a.csv")
data = data[data['state/ut'] != 'INDIA']
data = data.to_string(index=False)
print("Displaying states and union territories of India data (Three or more Language)")
print("")
print(data)


# In[27]:


country_dict_gender


# In[28]:


print("")


# In[29]:


data = pd.read_csv("age-gender-a.csv")
data = data[data['state/ut'] == 'INDIA']
data = data.to_string(index=False)
print("Displaying overall India data (Three or more Language)")
print("")
print(data)


# ### Exactly 2 Language

# In[ ]:





# In[30]:


state_dict = dict()
country_dict = dict()
state_dict_gender = dict()
country_dict_gender = dict()


# In[31]:


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
    #highest_percentage = 0
    highest_percentage_male = 0
    highest_percentage_female = 0
    for key, value in age_range.items():
        age_gp = key
        row1 = z[z['Age-group'] == age_gp]
        #Number_speaking_third_language = int(row1['Number_speaking_third_language'])
        
        Number_speaking_third_language_male = int(row1['Males3'])
        Number_speaking_third_language_female = int(row1['Females3'])
        
        Number_speaking_second_language_male = int(row1['Males2'])
        Number_speaking_second_language_female = int(row1['Females2'])
        
        Number_speaking_exactly_2language_male = Number_speaking_second_language_male - Number_speaking_third_language_male
        Number_speaking_exactly_2language_female = Number_speaking_second_language_female - Number_speaking_third_language_female
        
        population = 0
        population_male = 0
        population_female = 0
        for item in value:
            pop_key = item
            row2 = z2[z2['Age-group'] == pop_key]
            population = population + int(row2['Total_Persons'])
            
            population_male = population_male + int(row2['Total_Males'])
            population_female = population_female + int(row2['Total_Females'])
            
        #percentage = Number_speaking_third_language/population
        
        percentage_male = Number_speaking_exactly_2language_male/population_male
        percentage_female = Number_speaking_exactly_2language_female/population_female
        
        #if percentage>highest_percentage:
         #   Group = age_gp
          #  highest_percentage = percentage
        
        if percentage_male>highest_percentage_male:
            Group_male = age_gp
            highest_percentage_male = percentage_male
            
        if percentage_female>highest_percentage_female:
            Group_female = age_gp
            highest_percentage_female = percentage_female
        
        
    if status==0:
        #print("Group_male = ",Group_male)
        #print("highest_percentage_male = ",highest_percentage_male)
        #print("")
        #print("Group_female = ",Group_female)
        #print("highest_percentage_female = ",highest_percentage_female)
        state_dict_gender[State]=[Group_male,round(highest_percentage_male,3),Group_female,round(highest_percentage_female,3)]
    else:
        #print("Group_male = ",Group_male)
        #print("highest_percentage_male = ",highest_percentage_male)
        #print("")
        #print("Group_female = ",Group_female)
        #print("highest_percentage_female = ",highest_percentage_female)
        state_dict_gender[State]=[Group_male,round(highest_percentage_male,3),Group_female,round(highest_percentage_female,3)]
        country_dict_gender[State]=[Group_male,highest_percentage_male,Group_female,highest_percentage_female]
    #print("---------------------------------------------------------------------------")
    #print("")


# In[32]:


state_dict_gender


# In[33]:


a_file = open("age-gender-b.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = ['state/ut', 'age-group-males', 'ratio-males', 'age-group-females', 'ratio-females'])
writer.writeheader()
writer = csv.writer(a_file)
for key, value in state_dict_gender.items():
    writer.writerow([key] + value)

a_file.close()


# In[34]:


data = pd.read_csv("age-gender-b.csv")
data = data[data['state/ut'] != 'INDIA']
data = data.to_string(index=False)
print("Displaying states and union territories of India data (Exactly two Language)")
print("")
print(data)


# In[35]:


country_dict_gender


# In[36]:


print("")


# In[37]:


data = pd.read_csv("age-gender-b.csv")
data = data[data['state/ut'] == 'INDIA']
data = data.to_string(index=False)
print("Displaying overall India data (Exactly two Language)")
print("")
print(data)


# ### Exactly 1 Language

# In[ ]:





# In[38]:


state_dict = dict()
country_dict = dict()
state_dict_gender = dict()
country_dict_gender = dict()


# In[39]:


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
    #highest_percentage = 0
    highest_percentage_male = 0
    highest_percentage_female = 0
    for key, value in age_range.items():
        age_gp = key
        row1 = z[z['Age-group'] == age_gp]
        #Number_speaking_third_language = int(row1['Number_speaking_third_language'])
        
        Number_speaking_second_language_male = int(row1['Males2'])
        Number_speaking_second_language_female = int(row1['Females2'])
        
        population = 0
        population_male = 0
        population_female = 0
        for item in value:
            pop_key = item
            row2 = z2[z2['Age-group'] == pop_key]
            population = population + int(row2['Total_Persons'])
            
            population_male = population_male + int(row2['Total_Males'])
            population_female = population_female + int(row2['Total_Females'])
            
        #percentage = Number_speaking_third_language/population
        
        
        Number_speaking_exactly_1language_male = population_male - Number_speaking_second_language_male
        Number_speaking_exactly_1language_female = population_female - Number_speaking_second_language_female
        
        
        percentage_male = Number_speaking_exactly_1language_male/population_male
        percentage_female = Number_speaking_exactly_1language_female/population_female
        
        if percentage_male>highest_percentage_male:
            Group_male = age_gp
            highest_percentage_male = percentage_male
            
        if percentage_female>highest_percentage_female:
            Group_female = age_gp
            highest_percentage_female = percentage_female
        
        
    if status==0:
        #print("Group_male = ",Group_male)
        #print("highest_percentage_male = ",highest_percentage_male)
        #print("")
        #print("Group_female = ",Group_female)
        #print("highest_percentage_female = ",highest_percentage_female)
        state_dict_gender[State]=[Group_male,round(highest_percentage_male,3),Group_female,round(highest_percentage_female,3)]
    else:
        #print("Group_male = ",Group_male)
        #print("highest_percentage_male = ",highest_percentage_male)
        #print("")
        #print("Group_female = ",Group_female)
        #print("highest_percentage_female = ",highest_percentage_female)
        state_dict_gender[State]=[Group_male,round(highest_percentage_male,3),Group_female,round(highest_percentage_female,3)]
        country_dict_gender[State]=[Group_male,highest_percentage_male,Group_female,highest_percentage_female]
    #print("---------------------------------------------------------------------------")
    #print("")


# In[40]:


state_dict_gender


# In[41]:


a_file = open("age-gender-c.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = ['state/ut', 'age-group-males', 'ratio-males', 'age-group-females', 'ratio-females'])
writer.writeheader()
writer = csv.writer(a_file)
for key, value in state_dict_gender.items():
    writer.writerow([key] + value)

a_file.close()


# In[42]:


data = pd.read_csv("age-gender-c.csv")
data = data[data['state/ut'] != 'INDIA']
data = data.to_string(index=False)
print("Displaying states and union territories of India data (Exactly one Language)")
print("")
print(data)


# In[43]:


country_dict_gender


# In[44]:


print("")


# In[45]:


data = pd.read_csv("age-gender-c.csv")
data = data[data['state/ut'] == 'INDIA']
data = data.to_string(index=False)
print("Displaying overall India data (Exactly one Language)")
print("")
print(data)

