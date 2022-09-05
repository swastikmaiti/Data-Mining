#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests
import csv
import json
from collections import OrderedDict
import scipy.stats


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


# In[14]:


State_dict = dict()


# In[15]:


for i in range(len(group_state)):
    key = group_state[i]
    z = df1.get_group(group_state[i])          #retrieve the dataset under that state
    z = z.iloc[0]
    
    female_three_lang = int(z['Females3'])
    male_three_lang = int(z['Males3'])
    
    State_Code = z['State_Code']
    State_Name = key
    population_row = census_dataset[census_dataset["Name"] == State_Name]
    population = population_row['TOT_P'].tolist()[0]
    female_population = population_row['TOT_F'].tolist()[0]
    male_population = population_row['TOT_M'].tolist()[0]
    
    #print("State_Name = ",State_Name)
    #print("State_Code = ",State_Code)
    #print("population = ",population)
    #print("female_population = ",female_population)
    #print("male_population = ",male_population)
    
    male_prop = male_three_lang/male_population
    female_prop = female_three_lang/female_population
    pool_prop = (male_three_lang+female_three_lang)/population # Calculate Pool Proportion
    #print("male_prop = ",male_prop)
    #print("female_prop = ",female_prop)
    #print("pool_prop = ",pool_prop)
    
    male_percent = (male_three_lang*100)/male_population
    female_percent = (female_three_lang*100)/female_population
    SE = np.sqrt( ((pool_prop*(1-pool_prop))/male_population) + ((pool_prop*(1-pool_prop))/female_population) ) # Calculate Standard Error
    point_estimate = male_prop-female_prop # Calculate Point Estimate
    #print("point_estimate = ",point_estimate)
    null_value = 0                         # Null value for the Null Hypothesis
    z = (point_estimate - null_value)/SE   # Calculate z statistic
    p_value = scipy.stats.norm.sf(abs(z))*2  # Calculate p value for two tailed statistic
    #print("SE = ",SE)
    #print("z = ",z)
    
    
    #print("")
    #print("male_percent = ",male_percent)
    #print("female_percent = ",female_percent)
    #print("P value = ",p_value)
    
    State_dict[State_Code] = [round(male_percent,3),round(female_percent,4),p_value]
    
    #print("")
    #print("")


# In[16]:


State_dict = OrderedDict(sorted(State_dict.items()))
State_dict


# In[17]:


a_file = open("gender-india-c.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = ['state-code', 'male-percentage', 'female-percentage', 'p-value'])
writer.writeheader()
writer = csv.writer(a_file)
for key, value in State_dict.items():
    writer.writerow([key] + value)

a_file.close()


# In[18]:


data1 = pd.read_csv("gender-india-c.csv")
data1 = data1.to_string(index=False)
print("Displaying states and union territories of India data (Three or More Langage)")
print("")
print(data1)


# ### Exactly 2 Langage

# In[ ]:





# In[19]:


State_dict = dict()


# In[20]:


for i in range(len(group_state)):
    key = group_state[i]
    z = df1.get_group(group_state[i])          #retrieve the dataset under that state
    z = z.iloc[0]
    
    female_three_lang = int(z['Females3'])
    male_three_lang = int(z['Males3'])
    
    female_two_lang = int(z['Females2'])
    male_two_lang = int(z['Males2'])
    
    female_exactly_two = female_two_lang - female_three_lang
    male_exactly_two = male_two_lang - male_three_lang
    
    
    State_Code = z['State_Code']
    State_Name = key
    population_row = census_dataset[census_dataset["Name"] == State_Name]
    population = population_row['TOT_P'].tolist()[0]
    female_population = population_row['TOT_F'].tolist()[0]
    male_population = population_row['TOT_M'].tolist()[0]
    
    #print("State_Name = ",State_Name)
    #print("State_Code = ",State_Code)
    #print("population = ",population)
    #print("female_population = ",female_population)
    #print("male_population = ",male_population)
    
    male_prop = male_exactly_two/male_population
    female_prop = female_exactly_two/female_population
    pool_prop = (male_exactly_two+female_exactly_two)/population
    #print("male_prop = ",male_prop)
    #print("female_prop = ",female_prop)
    #print("pool_prop = ",pool_prop)
    
    male_percent = (male_exactly_two*100)/male_population
    female_percent = (female_exactly_two*100)/female_population
    SE = np.sqrt( ((pool_prop*(1-pool_prop))/male_population) + ((pool_prop*(1-pool_prop))/female_population) )
    point_estimate = male_prop-female_prop
    #print("point_estimate = ",point_estimate)
    null_value = 0
    z = (point_estimate - null_value)/SE
    p_value = scipy.stats.norm.sf(abs(z))*2
    #print("SE = ",SE)
    #print("z = ",z)
    
    
    #print("")
    #print("male_percent = ",male_percent)
    #print("female_percent = ",female_percent)
    #print("P value = ",p_value)
    
    State_dict[State_Code] = [round(male_percent,3),round(female_percent,4),p_value]
    
    #print("")
    #print("")


# In[21]:


State_dict = OrderedDict(sorted(State_dict.items()))
State_dict


# In[22]:


a_file = open("gender-india-b.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = ['state-code', 'male-percentage', 'female-percentage', 'p-value'])
writer.writeheader()
writer = csv.writer(a_file)
for key, value in State_dict.items():
    writer.writerow([key] + value)

a_file.close()


# In[23]:


print("")


# In[24]:


data1 = pd.read_csv("gender-india-b.csv")
data1 = data1.to_string(index=False)
print("Displaying states and union territories of India data (Exactly two Langage)")
print("")
print(data1)


# In[ ]:





# ### Exactly 1 Langage

# In[ ]:





# In[25]:


State_dict = dict()


# In[26]:


for i in range(len(group_state)):
    key = group_state[i]
    z = df1.get_group(group_state[i])          #retrieve the dataset under that state
    z = z.iloc[0]
    
    
    female_two_lang = int(z['Females2'])
    male_two_lang = int(z['Males2'])
       
    State_Code = z['State_Code']
    State_Name = key
    population_row = census_dataset[census_dataset["Name"] == State_Name]
    population = population_row['TOT_P'].tolist()[0]
    female_population = population_row['TOT_F'].tolist()[0]
    male_population = population_row['TOT_M'].tolist()[0]
    
    female_exactly_one = female_population - female_two_lang
    male_exactly_one = male_population - male_two_lang
    
    #print("State_Name = ",State_Name)
    #print("State_Code = ",State_Code)
    #print("population = ",population)
    #print("female_population = ",female_population)
    #print("male_population = ",male_population)
    
    male_prop = male_exactly_one/male_population
    female_prop = female_exactly_one/female_population
    pool_prop = (male_exactly_one+female_exactly_one)/population
    #print("male_prop = ",male_prop)
    #print("female_prop = ",female_prop)
    #print("pool_prop = ",pool_prop)
    
    male_percent = (male_exactly_one*100)/male_population
    female_percent = (female_exactly_one*100)/female_population
    SE = np.sqrt( ((pool_prop*(1-pool_prop))/male_population) + ((pool_prop*(1-pool_prop))/female_population) )
    point_estimate = male_prop-female_prop
    #print("point_estimate = ",point_estimate)
    null_value = 0
    z = (point_estimate - null_value)/SE
    p_value = scipy.stats.norm.sf(abs(z))*2
    #print("SE = ",SE)
    #print("z = ",z)
    
    
    #print("")
    #print("male_percent = ",male_percent)
    #print("female_percent = ",female_percent)
    #print("P value = ",p_value)
    
    State_dict[State_Code] = [round(male_percent,3),round(female_percent,4),p_value]
    
    #print("")
    #print("")


# In[27]:


State_dict = OrderedDict(sorted(State_dict.items()))
State_dict


# In[28]:


a_file = open("gender-india-a.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = ['state-code', 'male-percentage', 'female-percentage', 'p-value'])
writer.writeheader()
writer = csv.writer(a_file)
for key, value in State_dict.items():
    writer.writerow([key] + value)

a_file.close()


# In[29]:


print("")


# In[30]:


data1 = pd.read_csv("gender-india-a.csv")
data1 = data1.to_string(index=False)
print("Displaying states and union territories of India data (Exactly one Langage)")
print("")
print(data1)


# In[ ]:




