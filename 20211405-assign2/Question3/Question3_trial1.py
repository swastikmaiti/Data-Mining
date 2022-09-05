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


# ### Collect and filter dataset for useful values and assogn column names

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


# ### Calculating Rural Data

# In[11]:


#census_dataset = df[(df['TRU'] == "Rural") | (df['TRU'] == "Urban")]
census_dataset = df
census_dataset


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
    z1 = z[z['Total/Rural/Urban'] == 'Rural']
    z1 = z1.iloc[0]
    
    z2 = z[z['Total/Rural/Urban'] == 'Urban']
    z2 = z2.iloc[0]

    rural_three_lang = int(z1['Number_speaking_third_language'])
    urban_three_lang = int(z2['Number_speaking_third_language'])
    
    State_Code = z1['State_Code']
    State_Name = key
    population_row = census_dataset[census_dataset["Name"] == State_Name]
    
    Total_row = population_row[population_row["TRU"] == "Total"]
    Rural_row = population_row[population_row["TRU"] == "Rural"]
    Urban_row = population_row[population_row["TRU"] == "Urban"]
    
    population = Total_row['TOT_P'].tolist()[0]

    rural_population = Rural_row['TOT_P'].tolist()[0]
    urban_population = Urban_row['TOT_P'].tolist()[0]
    
    #print("State_Name = ",State_Name)
    #print("State_Code = ",State_Code)
    #print("population = ",population)
    #print("rural_three_lang = ",rural_three_lang)
    #print("rural_population = ",rural_population)
    #print("urban_three_lang = ",urban_three_lang)
    #print("urban_population = ",urban_population)
    
    rural_prop = rural_three_lang/rural_population
    urban_prop = urban_three_lang/urban_population
    pool_prop = (rural_three_lang+urban_three_lang)/population           # Calculate Pool Proportion
    #print("rural_prop = ",rural_prop)
    #print("urban_prop = ",urban_prop)
    #print("pool_prop = ",pool_prop)
    
    rural_percent = (rural_three_lang*100)/rural_population
    urban_percent = (urban_three_lang*100)/urban_population
    SE = np.sqrt( ((pool_prop*(1-pool_prop))/rural_population) + ((pool_prop*(1-pool_prop))/urban_population) )   # Calculate Standard Error
    point_estimate = rural_prop-urban_prop           # Calculate Point Estimate
    #print("point_estimate = ",point_estimate)
    null_value = 0                                 # Null value for the Null Hypothesis
    z = (point_estimate - null_value)/SE           # Calculate z statistic
    p_value = scipy.stats.norm.sf(abs(z))*2        # Calculate p value for two tailed statistic
    #print("SE = ",SE)
    #print("z = ",z)
    
    
    #print("")
    #print("rural_percent = ",rural_percent)
    #print("urban_percent = ",urban_percent)
    #print("P value = ",p_value)
    State_dict[State_Code] = [round(urban_percent,3),round(rural_percent,3),p_value]
    
    #print("")
    #print("")


# In[16]:


State_dict = OrderedDict(sorted(State_dict.items()))
State_dict


# In[17]:


a_file = open("geography-india-c.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = ['state-code', 'urban-percentage', 'rural-percentage', 'p-value'])
writer.writeheader()
writer = csv.writer(a_file)
for key, value in State_dict.items():
    writer.writerow([key] + value)

a_file.close()


# In[18]:


data1 = pd.read_csv("geography-india-c.csv")
data1 = data1.to_string(index=False)
print("Displaying states and union territories of India data (Three or More Langage)")
print("")
print(data1)


# ### Exacly 2 Language

# In[ ]:





# In[19]:


State_dict = dict()


# In[20]:


for i in range(len(group_state)):
    key = group_state[i]
    z = df1.get_group(group_state[i])          #retrieve the dataset under that state
    z1 = z[z['Total/Rural/Urban'] == 'Rural']
    z1 = z1.iloc[0]
    
    z2 = z[z['Total/Rural/Urban'] == 'Urban']
    z2 = z2.iloc[0]

    rural_three_lang = int(z1['Number_speaking_third_language'])
    urban_three_lang = int(z2['Number_speaking_third_language'])
    
    rural_two_lang = int(z1['Number_speaking_second_language'])
    urban_two_lang = int(z2['Number_speaking_second_language'])
    
    rural_exactly_two = rural_two_lang - rural_three_lang
    urban_exactly_two = urban_two_lang - urban_three_lang
    
    State_Code = z1['State_Code']
    State_Name = key
    population_row = census_dataset[census_dataset["Name"] == State_Name]
    
    Total_row = population_row[population_row["TRU"] == "Total"]
    Rural_row = population_row[population_row["TRU"] == "Rural"]
    Urban_row = population_row[population_row["TRU"] == "Urban"]
    
    population = Total_row['TOT_P'].tolist()[0]

    rural_population = Rural_row['TOT_P'].tolist()[0]
    urban_population = Urban_row['TOT_P'].tolist()[0]
    
    #print("State_Name = ",State_Name)
    #print("State_Code = ",State_Code)
    #print("population = ",population)
    #print("rural_three_lang = ",rural_three_lang)
    #print("rural_population = ",rural_population)
    #print("urban_three_lang = ",urban_three_lang)
    #print("urban_population = ",urban_population)
    
    rural_prop = rural_exactly_two/rural_population
    urban_prop = urban_exactly_two/urban_population
    pool_prop = (rural_exactly_two+urban_exactly_two)/population
    #print("rural_prop = ",rural_prop)
    #print("urban_prop = ",urban_prop)
    #print("pool_prop = ",pool_prop)
    
    rural_percent = (rural_exactly_two*100)/rural_population
    urban_percent = (urban_exactly_two*100)/urban_population
    SE = np.sqrt( ((pool_prop*(1-pool_prop))/rural_population) + ((pool_prop*(1-pool_prop))/urban_population) )
    point_estimate = rural_prop-urban_prop
    #print("point_estimate = ",point_estimate)
    null_value = 0
    z = (point_estimate - null_value)/SE
    p_value = scipy.stats.norm.sf(abs(z))*2
    #print("SE = ",SE)
    #print("z = ",z)
    
    
    #print("")
    #print("rural_percent = ",rural_percent)
    #print("urban_percent = ",urban_percent)
    #print("P value = ",p_value)
    State_dict[State_Code] = [round(urban_percent,3),round(rural_percent,3),p_value]
    
    #print("")
    #print("")


# In[21]:


State_dict = OrderedDict(sorted(State_dict.items()))
State_dict


# In[22]:


a_file = open("geography-india-b.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = ['state-code', 'urban-percentage', 'rural-percentage', 'p-value'])
writer.writeheader()
writer = csv.writer(a_file)
for key, value in State_dict.items():
    writer.writerow([key] + value)

a_file.close()


# In[23]:


print("")


# In[24]:


data1 = pd.read_csv("geography-india-b.csv")
data1 = data1.to_string(index=False)
print("Displaying states and union territories of India data (Exactly two Langage)")
print("")
print(data1)


# In[ ]:





# ### Exactly 1 Language

# In[ ]:





# In[25]:


State_dict = dict()


# In[26]:


for i in range(len(group_state)):
    key = group_state[i]
    z = df1.get_group(group_state[i])          #retrieve the dataset under that state
    z1 = z[z['Total/Rural/Urban'] == 'Rural']
    z1 = z1.iloc[0]
    
    z2 = z[z['Total/Rural/Urban'] == 'Urban']
    z2 = z2.iloc[0]
    
    rural_two_lang = int(z1['Number_speaking_second_language'])
    urban_two_lang = int(z2['Number_speaking_second_language'])
    
    State_Code = z1['State_Code']
    State_Name = key
    population_row = census_dataset[census_dataset["Name"] == State_Name]
    
    Total_row = population_row[population_row["TRU"] == "Total"]
    Rural_row = population_row[population_row["TRU"] == "Rural"]
    Urban_row = population_row[population_row["TRU"] == "Urban"]
    
    population = Total_row['TOT_P'].tolist()[0]

    rural_population = Rural_row['TOT_P'].tolist()[0]
    urban_population = Urban_row['TOT_P'].tolist()[0]
    
    rural_exactly_one = rural_population - rural_two_lang
    urban_exactly_one = urban_population - urban_two_lang
    
    #print("State_Name = ",State_Name)
    #print("State_Code = ",State_Code)
    #print("population = ",population)
    #print("rural_three_lang = ",rural_three_lang)
    #print("rural_population = ",rural_population)
    #print("urban_three_lang = ",urban_three_lang)
    #print("urban_population = ",urban_population)
    
    rural_prop = rural_exactly_one/rural_population
    urban_prop = urban_exactly_one/urban_population
    pool_prop = (rural_exactly_one+urban_exactly_one)/population
    #print("rural_prop = ",rural_prop)
    #print("urban_prop = ",urban_prop)
    #print("pool_prop = ",pool_prop)
    
    rural_percent = (rural_exactly_one*100)/rural_population
    urban_percent = (urban_exactly_one*100)/urban_population
    SE = np.sqrt( ((pool_prop*(1-pool_prop))/rural_population) + ((pool_prop*(1-pool_prop))/urban_population) )
    point_estimate = rural_prop-urban_prop
    #print("point_estimate = ",point_estimate)
    null_value = 0
    z = (point_estimate - null_value)/SE
    p_value = scipy.stats.norm.sf(abs(z))*2
    #print("SE = ",SE)
    #print("z = ",z)
    
    
    #print("")
    #print("rural_percent = ",rural_percent)
    #print("urban_percent = ",urban_percent)
    #print("P value = ",p_value)
    State_dict[State_Code] = [round(urban_percent,3),round(rural_percent,3),p_value]
    
    #print("")
    #print("")


# In[27]:


State_dict = OrderedDict(sorted(State_dict.items()))
State_dict


# In[28]:


a_file = open("geography-india-a.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = ['state-code', 'urban-percentage', 'rural-percentage', 'p-value'])
writer.writeheader()
writer = csv.writer(a_file)
for key, value in State_dict.items():
    writer.writerow([key] + value)

a_file.close()


# In[29]:


print("")


# In[30]:


data1 = pd.read_csv("geography-india-a.csv")
data1 = data1.to_string(index=False)
print("Displaying states and union territories of India data (Exactly one Langage)")
print("")
print(data1)

