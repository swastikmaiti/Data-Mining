#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
import csv
import json
from collections import OrderedDict


# In[2]:


language_data = pd.read_csv("DDW-C18-0000.csv")


# In[3]:


language_data.head(7)


# ### Filter the dataframe for useful data and modify column headers

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


# In[14]:


State_dict = dict()


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
    #print("exactly_one_lang = ",exactly_one_lang)
    #print("exactly_two_lang = ",exactly_two_lang)
    #print("three_or_more_lang = ",three_or_more_lang)
    State_dict[State_Code] = [round(exactly_one_lang,3),round(exactly_two_lang,3),round(three_or_more_lang,3)]


# In[16]:


State_dict = OrderedDict(sorted(State_dict.items())) # Order the ouput by first column i.e. key
State_dict


# In[17]:


a_file = open("percent-india-a.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = ['state-code', 'percent-one', 'percent-two', 'percent-three'])
writer.writeheader()
writer = csv.writer(a_file)
for key, value in State_dict.items():
    writer.writerow([key] + value)

a_file.close()


# In[18]:


data1 = pd.read_csv("percent-india-a.csv")
data1 = data1.to_string(index=False)
print("Displaying states and union territories of India data")
print("")
print(data1)


# ### Calculating Country Level Data

# In[19]:


indexNames = language_data_total[language_data_total['Area_Name'] != 'INDIA' ].index
language_data = language_data_total.drop(indexNames , inplace=False)
language_data = language_data.iloc[0]
language_data


# In[20]:


df = data[data['Level'] == "India"]


# In[21]:


census_dataset = df[df['TRU'] == "Total"]
census_dataset


# In[22]:


Number_speaking_second_language = int(language_data['Number_speaking_second_language'])
Number_speaking_third_language = int(language_data['Number_speaking_third_language'])
population = census_dataset['TOT_P'].tolist()[0]


# In[23]:


#print("Number_speaking_second_language = ",Number_speaking_second_language)
#print("Number_speaking_third_language = ",Number_speaking_third_language)
#print("population = ",population)


# In[24]:


exactly_one_lang = ((population - Number_speaking_second_language)*100)/population
exactly_two_lang = ((Number_speaking_second_language - Number_speaking_third_language)*100)/population
three_or_more_lang = (Number_speaking_third_language*100)/population
#print("exactly_one_lang = ",exactly_one_lang)
#print("exactly_two_lang = ",exactly_two_lang)
#print("three_or_more_lang = ",three_or_more_lang)


# In[25]:


Country_dict = dict()


# In[26]:


Country_dict['INDIA'] = [round(exactly_one_lang,3),round(exactly_two_lang,3),round(three_or_more_lang,3)]


# In[27]:


Country_dict


# In[28]:


print("")


# In[29]:


a_file = open("percent-india-b.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = ['Country', 'percent-one', 'percent-two', 'percent-three'])
writer.writeheader()
writer = csv.writer(a_file)
for key, value in Country_dict.items():
    writer.writerow([key] + value)

a_file.close()


# In[30]:


data = pd.read_csv("percent-india-b.csv")
data = data.to_string(index=False)
print("Displaying over all country data")
print("")
print(data)

