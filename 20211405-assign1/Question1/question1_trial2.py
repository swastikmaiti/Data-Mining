#!/usr/bin/env python
# coding: utf-8

# In[1]:


print("Started Execution")


# In[2]:


import pandas as pd
import requests
import csv
import json
from collections import OrderedDict


# In[3]:


f = open ('neighbor-districts.json', "r")
neighbor = json.loads(f.read())


# In[4]:


neighbor


# In[5]:


punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''


# In[6]:


new_neighbor = {}


# ### Removing geolocation tag from neighbor dataset

# In[7]:


dict_items = neighbor.items()
X= list(dict_items)
for i in range(len(X)):
    x = X[i]
    key = x[0]
    value = x[1]
    split_string = key.split("/", 1)
    key = split_string[0]
    values = []
    for j in range(len(value)):
        y = value[j]
        split_string = y.split("/", 1)
        y = split_string[0]
        values.append(y)
    new_neighbor[key] = values
        


# In[8]:


neighbor = new_neighbor


# In[9]:


neighbor_dataset_districts = set()


# ### Removing geolocation tag from neighbor dataset and creating a set of neighbors with lowercase letter

# In[10]:


dict_items = neighbor.keys()
Y = list(dict_items)
for i in range(len(Y)):
    y = Y[i]
    split_string = y.split("/", 1)
    substring = split_string[0].lower()
    neighbor_dataset_districts.add(substring)


# ### Removing pounctuation from district names

# In[11]:


list1 = list(neighbor_dataset_districts)
for i in range(len(list1)):
    word = list1[i]
    old = word
    update = 0
    for letter in word:
        if letter in punc:
            word = word.replace(letter, " ")
            list1[i] = word
            update = 1
    if update==1:                                       #if district name is updated reflect the update everywhere in neighbor dataset
        neighbor[word] = neighbor.pop(old)              #update the neighbor by deleting old key(district name) with new key
        neighbor_items = list(neighbor.items())
        for j in range(len(neighbor_items)):            #update the district names in list of neighbor
            if old in neighbor_items[j][1]:
                neighbor_key = neighbor_items[j][0]
                old_list = neighbor_items[j][1]
                index = old_list.index(old)
                old_list[index] = word;
                old_list = set(old_list)
                old_list = list(old_list)
                neighbor[neighbor_key] = old_list
        
neighbor_dataset_districts = set(list1)


# In[12]:


neighbor_dataset_districts


# In[13]:


#print("Neighbor datset districts = ",len(neighbor_dataset_districts))


# In[14]:


data = pd.read_csv("cowin_vaccine_data_districtwise.csv",low_memory=False)


# In[15]:


data


# In[16]:


vaccination_dataset_districts = set(data["District"][1:])


# ### Collecting names of district in Vaccination dataset in lowercase

# In[17]:


l = list(vaccination_dataset_districts)
for i in range(len(l)):
    l[i] = l[i].lower()


# In[18]:


vaccination_dataset_districts = set(l)


# ### Removing punctuation from names of district in Vaccination dataset in lowercase

# In[19]:


list1 = list(vaccination_dataset_districts)
for i in range(len(list1)):
    word = list1[i]
    for letter in word:
        if letter in punc:
            word = word.replace(letter, " ")
            list1[i] = word
vaccination_dataset_districts = set(list1)


# In[ ]:





# In[20]:


neighbor_m_vaccination = list(neighbor_dataset_districts - vaccination_dataset_districts)
#print("neighbor_m_vaccination size = ",len(neighbor_m_vaccination))


# In[21]:


vaccination_m_neighbor = list(vaccination_dataset_districts - neighbor_dataset_districts)
#print("vaccination_m_neighbor size = ",len(vaccination_m_neighbor))


# In[22]:


vaccination_similar_neighbor_dict = {}


# ### Find District names in vaccination which are similar to neighbor(dist in vaccination whose name is part of dist in neighbor)

# In[23]:


count = 0
for i in range(len(vaccination_m_neighbor)):
    dis_vaccination = vaccination_m_neighbor[i]
    for j in range(len(neighbor_m_vaccination)):
        dis_neighbor = neighbor_m_vaccination[j]
        if dis_vaccination in dis_neighbor:                                     # if already a similar neighbor name exist append ti the list
            if dis_vaccination in vaccination_similar_neighbor_dict.keys():
                vaccination_similar_neighbor_dict[dis_vaccination].append(dis_neighbor)
            else:                                                               # if this is the first similar neighbor name update the dict value as list
                vaccination_similar_neighbor_dict[dis_vaccination] = list()
                vaccination_similar_neighbor_dict[dis_vaccination].append(dis_neighbor)
            count = count+1
#print(count)


# In[24]:


vaccination_similar_neighbor_dict


# ### Update the names in neighbor dataset according to vaccination name

# In[25]:


items = list(vaccination_similar_neighbor_dict.items())           #convert dict to list
for i in range(len(items)):                                       #go through the list of similarity
    key = items[i][0]
    values = items[i][1]
    if len(values)==1:                                            #update names if there is no other conflicting names
        values = values[0]
        neighbor[key] = neighbor.pop(values)                      #update the neighbor by deleting old key with new district names but same neighbor as the old distric names
        neighbor_items = list(neighbor.items())
        for j in range(len(neighbor_items)):                      #go through the neighbors of each district and update according to new names
            if values in neighbor_items[j][1]:
                neighbor_key = neighbor_items[j][0]
                old_list = neighbor_items[j][1]
                index = old_list.index(values)
                old_list[index] = key;
                neighbor[neighbor_key] = old_list


# In[ ]:





# In[26]:


neighbor_dataset_districts = set(neighbor)


# In[27]:


neighbor_dataset_districts


# In[28]:


neighbor_m_vaccination = list(neighbor_dataset_districts - vaccination_dataset_districts)
#print("neighbor_m_vaccination size = ",len(neighbor_m_vaccination))


# In[29]:


vaccination_m_neighbor = list(vaccination_dataset_districts - neighbor_dataset_districts)
#print("vaccination_m_neighbor size = ",len(vaccination_m_neighbor))


# In[30]:


vaccination_similar_neighbor_dict = {}


# ### Find District names in vaccination which are similar to neighbor(dist in vaccination whose name without space is part of dist in neighbor)

# In[31]:


count = 0
for i in range(len(vaccination_m_neighbor)):
    dis_vaccination = vaccination_m_neighbor[i]
    for j in range(len(neighbor_m_vaccination)):
        dis_neighbor = neighbor_m_vaccination[j]
        if dis_vaccination in dis_neighbor:
            if dis_vaccination in vaccination_similar_neighbor_dict.keys():
                vaccination_similar_neighbor_dict[dis_vaccination].append(dis_neighbor)
            else:
                vaccination_similar_neighbor_dict[dis_vaccination] = list()
                vaccination_similar_neighbor_dict[dis_vaccination].append(dis_neighbor)
            count = count+1
        else:
            dis_vaccination1 = dis_vaccination.replace(" ", "")
            if dis_vaccination1 in dis_neighbor:
                if dis_vaccination1 in vaccination_similar_neighbor_dict.keys():
                    vaccination_similar_neighbor_dict[dis_vaccination].append(dis_neighbor)
                else:
                    vaccination_similar_neighbor_dict[dis_vaccination] = list()
                    vaccination_similar_neighbor_dict[dis_vaccination].append(dis_neighbor)
                count = count+1


# In[32]:


vaccination_similar_neighbor_dict


# ### Function to Merge the districts of neighbor dataset which are part of a larger district in vaccination dataset

# In[33]:


def merge(list1):
    key = list1[0]
    values = list1[1]
    neighbor_items = list(neighbor.items())
    set1 = set()
    for i in range(len(neighbor_items)):                     #find the union of neighbor dataset of merging district 
        if neighbor_items[i][0] in values:
            set1 = set1.union(set(neighbor_items[i][1]))
            neighbor.pop(neighbor_items[i][0])               #remove the smalles district from neighbor 
    for j in range(len(values)):                             #from the set of merging districts neighbors reomove their own name
        if values[j] in set1:
            set1.remove(values[j])
            
    neighbor[key] = list(set1)                               #enter as key the new merged district
    
    neighbor_items = list(neighbor.items())
    
    for j in range(len(values)):                             #go through the neighbor of each district and change the name of old smller district with new merged district
        check_for = values[j]
        for i in range(len(neighbor_items)):
            neighbors = neighbor_items[i][1]
            if check_for in neighbors:
                neighbor_key = neighbor_items[i][0]
                old_list = neighbor_items[i][1]
                index = old_list.index(check_for)
                old_list[index] = key;
                old_list = set(old_list)
                old_list = list(old_list)
                neighbor[neighbor_key] = old_list


# In[ ]:





# In[34]:


z = list(vaccination_similar_neighbor_dict.items())
z


# In[35]:


discard = 0
for i in range(len(z)):
    if z[i][0]=="mahe":
        discard = i
for i in range(len(z)):
    if i!=discard:
        merge(z[i])
        
    


# In[36]:


neighbor_similar_vaccination_dict = {}


# ### Find District names in neighbor which are similar to vaccinatiom(dist in neighbor whose name is part of dist in vaccination)

# In[37]:


count = 0
for i in range(len(neighbor_m_vaccination)):
    dis_neighbor = neighbor_m_vaccination[i]
    for j in range(len(vaccination_m_neighbor)):
        dis_vaccination = vaccination_m_neighbor[j]
        if dis_neighbor in dis_vaccination:
            neighbor_similar_vaccination_dict[dis_neighbor] = dis_vaccination
            count = count+1
        else:
            dis_neighbor1 = dis_neighbor.replace(" ", "")
            if dis_neighbor1 in dis_vaccination:
                neighbor_similar_vaccination_dict[dis_neighbor] = dis_vaccination
                count = count+1


# In[38]:


neighbor_similar_vaccination_dict


# ### Function to Update neighbor District dataset according to its equivalent district names in vaccination dataset

# In[39]:


def update_neighbor(Dict1):
    items = list(Dict1.items())
    for i in range(len(items)):
        neighbor_name = items[i][0]
        vacination_set_name = items[i][1]
        neighbor_items = list(neighbor.items())
        for i in range(len(neighbor_items)):                                #go through the neighbor dataset
            if neighbor_name in neighbor_items[i][0]:                                    
                neighbor[vacination_set_name] = neighbor.pop(neighbor_name) #if the similar neighbor name appears in key update it with new name from vaccination dataset
            if neighbor_name in neighbor_items[i][1]:                       #if the similar neighbor name appears in neighbor of a district update it with new name from vaccination dataset
                neighbor_key = neighbor_items[i][0]
                old_list = neighbor_items[i][1]
                index = old_list.index(neighbor_name)
                old_list[index] = vacination_set_name
                old_list = set(old_list)
                old_list = list(old_list)
                neighbor[neighbor_key] = old_list


# In[40]:


update_neighbor(neighbor_similar_vaccination_dict)


# In[41]:


neighbor_dataset_districts = set(neighbor)


# In[42]:


neighbor_m_vaccination = list(neighbor_dataset_districts - vaccination_dataset_districts)
#print("neighbor_m_vaccination size = ",len(neighbor_m_vaccination))


# In[43]:


vaccination_m_neighbor = list(vaccination_dataset_districts - neighbor_dataset_districts)
#print("vaccination_m_neighbor size = ",len(vaccination_m_neighbor))


# In[44]:


vaccine_similar_neighbor_dict = dict()


# ### Find District names in vaccination which are similar to neighbor(dist in vaccination, components whose name after splitiing at space is part of dist in neighbor)

# In[45]:


count = 0
for i in range(len(vaccination_m_neighbor)):
    dis_vaccine = vaccination_m_neighbor[i]
    for j in range(len(neighbor_m_vaccination)):
        dis_neighbor = neighbor_m_vaccination[j]
        dis_vaccine_words = dis_vaccine.split()
        dis_neighbor_words = dis_neighbor.split()
        if "state" in dis_vaccine_words:
            dis_vaccine_words.remove("state")
        if "district" in dis_vaccine_words:
            dis_vaccine_words.remove("district")
        if "state" in dis_vaccine_words:
            dis_vaccine_words.remove("state")
        if "district" in dis_vaccine_words:
            dis_vaccine_words.remove("district")
        for word in dis_vaccine_words:                                       #go through each word of district names from vaccination dataset
            if word in dis_neighbor_words:                                   #if any word appears in neighbor dataset district name words then there is a similarity
                if dis_vaccine in vaccine_similar_neighbor_dict.keys():
                    values = vaccine_similar_neighbor_dict[dis_vaccine]
                    if dis_neighbor not in values:
                        vaccine_similar_neighbor_dict[dis_vaccine].append(dis_neighbor)
                else:
                    vaccine_similar_neighbor_dict[dis_vaccine] = list()
                    vaccine_similar_neighbor_dict[dis_vaccine].append(dis_neighbor)
                    count = count+1


# In[46]:


vaccine_similar_neighbor_dict


# ### Refine the above similarity to update districts in neighbor dataset

# In[47]:


vaccine_similar_neighbor_dict = {'shahid bhagat singh nagar': ['shaheed bhagat singh nagar'],
 'west singhbhum': ['pashchimi singhbhum'],
 's p s  nellore': ['sri potti sriramulu nellore'],
 's a s  nagar': ['sahibzada ajit singh nagar'],
 'saraikela kharsawan': ['seraikela kharsawan'],
 'lahaul and spiti': ['lahul and spiti'],
 'bengaluru urban': ['bangalore urban'],
 'mahe': ['mahe district'],
 'devbhumi dwarka': ['devbhumi dwaraka district'],
 'sant kabir nagar': ['sait kibir nagar'],
 'east singhbhum': ['purbi singhbhum'],
 'west champaran': ['pashchim champaran'],
 'fatehgarh sahib': ['fategarh sahib'],
 'bengaluru rural': ['bangalore rural'],
 'rae bareli': ['rae bareilly'],
 'komaram bheem': ['komram bheem'],
 'east champaran': ['purba champaran']}


# In[48]:


l1 = list(vaccine_similar_neighbor_dict.items())
for i in range(len(l1)):
    merge(l1[i])


# In[49]:


li = list(neighbor.keys())
for i in range(len(l1)):
    if "kadapa" in l1[i]:
        print(l1[i])


# In[50]:


neighbor_dataset_districts = list(neighbor.keys())
neighbor_dataset_districts = set(neighbor_dataset_districts)


# In[51]:


vaccination_m_neighbor = list(vaccination_dataset_districts - neighbor_dataset_districts)
#print("vaccination_m_neighbor size = ",len(vaccination_m_neighbor))


# In[52]:


neighbor_m_vaccination = list(neighbor_dataset_districts - vaccination_dataset_districts)
#print("neighbor_m_vaccination size = ",len(neighbor_m_vaccination))


# In[53]:


neighbor_similar_vaccine_dict = dict()


# ### Find District names in neighbor which are similar to vaccination(dist in neighbor, components whose name after splitting at space is part of dist in vaccination)

# In[54]:


count = 0
for i in range(len(neighbor_m_vaccination)):
    dis_neighbor = neighbor_m_vaccination[i]
    for j in range(len(vaccination_m_neighbor)):
        dis_vaccine = vaccination_m_neighbor[j]
        dis_vaccine_words = dis_vaccine.split()
        dis_neighbor_words = dis_neighbor.split()
        if "state" in dis_vaccine_words:
            dis_vaccine_words.remove("state")
        if "district" in dis_vaccine_words:
            dis_vaccine_words.remove("district")
        if "state" in dis_vaccine_words:
            dis_vaccine_words.remove("state")
        if "district" in dis_vaccine_words:
            dis_vaccine_words.remove("district")
        for word in dis_neighbor_words:
            if word in dis_vaccine_words:
                if dis_neighbor in neighbor_similar_vaccine_dict.keys():
                    values = neighbor_similar_vaccine_dict[dis_neighbor]
                    if dis_vaccine not in values:
                        neighbor_similar_vaccine_dict[dis_neighbor].append(dis_vaccine)
                else:
                    neighbor_similar_vaccine_dict[dis_neighbor] = list()
                    neighbor_similar_vaccine_dict[dis_neighbor].append(dis_vaccine)
                    count = count+1


# ### Repeat the above procedures with Covid datase

# In[55]:


response = requests.get("https://data.covid19india.org/v4/min/data.min.json")


# In[56]:


covid_dataset = response.json()


# In[57]:


covid_dataset_districts = set()


# ### Collect the Districts names from Covid dataset json file

# In[58]:


dict_items = covid_dataset.values()
X = list(dict_items)
for i in range(len(X)):
    x = X[i]
    if 'districts' in x.keys():
        x = x['districts']
        x = set(x.keys())
        covid_dataset_districts = covid_dataset_districts.union(x)


# In[59]:


l = list(covid_dataset_districts)
for i in range(len(l)):
    l[i] = l[i].lower()


# In[60]:


covid_dataset_districts = set(l)


# ### Remove punctuation from distric names of Covid dataset

# In[61]:


list1 = list(covid_dataset_districts)
for i in range(len(list1)):
    word = list1[i]
    for letter in word:
        if letter in punc:
            word = word.replace(letter, " ")
            list1[i] = word
covid_dataset_districts = set(list1)


# In[62]:


#print("Length of Covid datset districts = ",len(covid_dataset_districts))


# In[63]:


#print("Neighbor datset districts = ",len(neighbor_dataset_districts))


# In[64]:


neighbor_m_covid = list(neighbor_dataset_districts - covid_dataset_districts)
#print("neighbor_m_vaccination size = ",len(neighbor_m_covid))


# In[65]:


covid_m_neighbor = list(covid_dataset_districts - neighbor_dataset_districts)
#print("vaccination_m_neighbor size = ",len(covid_m_neighbor))


# In[66]:


covid_similar_neighbor_dict = {}


# ### Find District names in Covid which are similar to neighbor(dist in vaccination which are part of dist names in neighbor and dist in vaccination after removal of space which are part of dist names in neighbor)

# In[67]:


count = 0
for i in range(len(covid_m_neighbor)):
    dis_covid = covid_m_neighbor[i]
    for j in range(len(neighbor_m_covid)):
        dis_neighbor = neighbor_m_covid[j]
        if dis_covid in dis_neighbor:
            if dis_covid in covid_similar_neighbor_dict.keys():
                covid_similar_neighbor_dict[dis_covid].append(dis_neighbor)
            else:
                covid_similar_neighbor_dict[dis_covid] = list()
                covid_similar_neighbor_dict[dis_covid].append(dis_neighbor)
            count = count+1
        else:
            dis_covid1 = dis_covid.replace(" ", "")
            dis_neighbor1 = dis_neighbor
            dis_neighbor1 = dis_neighbor1.replace(" ", "")
            if dis_covid1 in dis_neighbor1:
                if dis_covid1 in covid_similar_neighbor_dict.keys():
                    covid_similar_neighbor_dict[dis_covid].append(dis_neighbor)
                else:
                    covid_similar_neighbor_dict[dis_covid] = list()
                    covid_similar_neighbor_dict[dis_covid].append(dis_neighbor)
                count = count+1


# In[68]:


covid_similar_neighbor_dict


# In[69]:


z = list(covid_similar_neighbor_dict.items())
z


# In[70]:


for i in range(len(z)):
     merge(z[i])


# In[71]:


neighbor_similar_covid_dict = {}


# ### Find District names in neighbor which are similar to covid(dist in neighbor which are part of dist names in Covid and dist in neighbor after removal of space which are part of dist names in Covid)

# In[72]:


count = 0
for i in range(len(neighbor_m_covid)):
    dis_neighbor = neighbor_m_covid[i]
    for j in range(len(covid_m_neighbor)):
        dis_covid = covid_m_neighbor[j]
        if dis_neighbor in dis_covid:
            neighbor_similar_covid_dict[dis_neighbor] = dis_covid
            count = count+1
        else:
            dis_neighbor1 = dis_neighbor.replace(" ", "")
            dis_covid1 = dis_covid.replace(" ", "")
            if dis_neighbor1 in dis_covid1:
                neighbor_similar_covid_dict[dis_neighbor] = dis_covid
                count = count+1


# In[73]:


neighbor_similar_covid_dict


# In[74]:


update_neighbor(neighbor_similar_covid_dict)


# In[75]:


neighbor_dataset_districts = set(neighbor)


# In[76]:


neighbor_m_covid = list(neighbor_dataset_districts - covid_dataset_districts)
#print("neighbor_m_vaccination size = ",len(neighbor_m_covid))


# In[77]:


covid_m_neighbor = list(covid_dataset_districts - neighbor_dataset_districts)
#print("covid_m_neighbor size = ",len(covid_m_neighbor))


# In[78]:


covid_similar_neighbor_dict = {}
neighbor_m_covid_2 = list()
covid_m_neighbor_2 = list()


# ### Find District names in neighbor and Covid which consist of more than 2 words except for the word District

# In[79]:


for i in range(len(neighbor_m_covid)):
    dist = neighbor_m_covid[i]
    if dist.count(" ")==1:
        if "district" not in dist:
            neighbor_m_covid_2.append(dist)
    elif dist.count(" ")>1:
        neighbor_m_covid_2.append(dist)


# In[80]:


for i in range(len(covid_m_neighbor)):
    dist = covid_m_neighbor[i]
    if dist.count(" ")==1:
        if "district" not in dist:
            covid_m_neighbor_2.append(dist)
    elif dist.count(" ")>1:
        covid_m_neighbor_2.append(dist)


# In[81]:


neighbor_m_covid_2


# ### Find District names in Covid which are similar to neighbor(dist in Covid, components whose name after splitiing at space is part of dist in neighbor)

# In[82]:


count = 0
for i in range(len(covid_m_neighbor_2)):
    dis_covid = covid_m_neighbor_2[i]
    for j in range(len(neighbor_m_covid_2)):
        dis_neighbor = neighbor_m_covid_2[j]
        dis_covid_words = dis_covid.split()
        dis_neighbor_words = dis_neighbor.split()
        if "state" in dis_covid_words:
            dis_covid_words.remove("state")
        if "district" in dis_covid_words:
            dis_covid_words.remove("district")
        if "state" in dis_neighbor_words:
            dis_neighbor_words.remove("state")
        if "district" in dis_neighbor_words:
            dis_neighbor_words.remove("district")
        for word in dis_covid_words:
            if word in dis_neighbor_words:
                if dis_covid in covid_similar_neighbor_dict.keys():
                    values = covid_similar_neighbor_dict[dis_covid]
                    if dis_neighbor not in values:
                        covid_similar_neighbor_dict[dis_covid].append(dis_neighbor)
                else:
                    covid_similar_neighbor_dict[dis_covid] = list()
                    covid_similar_neighbor_dict[dis_covid].append(dis_neighbor)
                    count = count+1


# In[83]:


covid_similar_neighbor_dict


# In[84]:


neighbor_dataset_districts = set(neighbor)


# In[85]:


neighbor_m_covid = list(neighbor_dataset_districts - covid_dataset_districts)
#print("neighbor_m_vaccination size = ",len(neighbor_m_covid))


# In[86]:


covid_m_neighbor = list(covid_dataset_districts - neighbor_dataset_districts)
#print("covid_m_neighbor size = ",len(covid_m_neighbor))


# In[87]:


neighbor_similar_covid_dict = {}
neighbor_m_covid_2 = list()
covid_m_neighbor_2 = list()


# ### Find District names in neighbor and Covid which consist of more than 2 words except for the word District

# In[88]:


for i in range(len(neighbor_m_covid)):
    dist = neighbor_m_covid[i]
    if dist.count(" ")==1:
        if "district" not in dist:
            neighbor_m_covid_2.append(dist)
    elif dist.count(" ")>1:
        neighbor_m_covid_2.append(dist)


# In[89]:


for i in range(len(covid_m_neighbor)):
    dist = covid_m_neighbor[i]
    if dist.count(" ")==1:
        if "district" not in dist:
            covid_m_neighbor_2.append(dist)
    elif dist.count(" ")>1:
        covid_m_neighbor_2.append(dist)


# ### Find District names in neighbor which are similar to Covid(dist in neighbor, components whose name after splitiing at space is part of dist in Covid)

# In[90]:


count = 0
for i in range(len(neighbor_m_covid_2)):
    dis_neighbor = neighbor_m_covid_2[i]
    for j in range(len(covid_m_neighbor_2)):
        dis_covid = covid_m_neighbor_2[j]
        dis_covid_words = dis_covid.split()
        dis_neighbor_words = dis_neighbor.split()
        if "state" in dis_covid_words:
            dis_covid_words.remove("state")
        if "district" in dis_covid_words:
            dis_covid_words.remove("district")
        if "state" in dis_neighbor_words:
            dis_neighbor_words.remove("state")
        if "district" in dis_neighbor_words:
            dis_neighbor_words.remove("district")
        for word in dis_neighbor_words:
            if word in dis_covid_words:
                if dis_neighbor in neighbor_similar_covid_dict.keys():
                    values = neighbor_similar_covid_dict[dis_neighbor]
                    if dis_covid not in values:
                        neighbor_similar_covid_dict[dis_neighbor].append(dis_covid)
                else:
                    neighbor_similar_covid_dict[dis_neighbor] = dis_covid
                    count = count+1        


# In[ ]:





# In[91]:


neighbor_similar_covid_dict


# In[92]:


update_neighbor(neighbor_similar_covid_dict)


# In[93]:


neighbor_m_covid = list(neighbor_dataset_districts - covid_dataset_districts)
#print("neighbor_m_vaccination size = ",len(neighbor_m_covid))


# In[94]:


neighbor_m_vaccination = list(neighbor_dataset_districts - vaccination_dataset_districts)
#print("neighbor_m_vaccination size = ",len(neighbor_m_vaccination))


# In[95]:


neighbor_dataset_districts = set(neighbor)


# ### Find District names neighbor which are not in Covid or Vaccination dataset

# In[96]:


z1 = neighbor_dataset_districts.intersection(covid_dataset_districts)


# In[97]:


z2 = neighbor_dataset_districts.intersection(vaccination_dataset_districts)


# In[98]:


z = z1.union(z2)


# In[99]:


len(z)


# In[100]:


discard = neighbor_dataset_districts - z


# In[101]:


discard = list(discard)+['niwari']


# In[102]:


for i in range(len(discard)):
    not_in = discard[i]
    neighbor_items = list(neighbor.items())
    neighbor.pop(not_in)
    for j in range(len(neighbor_items)):
        if not_in in neighbor_items[j][1]:
            neighbor_key = neighbor_items[j][0]
            old_list = neighbor_items[j][1]
            old_list.remove(not_in)
            old_list = set(old_list)
            old_list = list(old_list)
            neighbor[neighbor_key] = old_list


# ### Create dictionary of district names which are similar to district names in Vaccination dataset. The (key,value) paires are obtained from analysis below while assigning district id to districts of neighbor

# In[103]:


vaccine_similar_neighbor_dict = {'y.s.r. kadapa':['y s r  kadapa'],'s.a.s. nagar':['s a s  nagar'],'saraikela-kharsawan':['saraikela kharsawan'],'s.p.s. nellore':['s p s  nellore']}


# In[104]:


l1 = list(vaccine_similar_neighbor_dict.items())
for i in range(len(l1)):
    merge(l1[i])


# In[105]:


neighbor_dataset_districts = set(neighbor)


# In[106]:


len(neighbor_dataset_districts)


# In[107]:


neighbor_dataset_districts - vaccination_dataset_districts


# In[108]:


vaccination_data = pd.read_csv("cowin_vaccine_data_districtwise.csv",low_memory=False)


# In[109]:


vaccination_data = vaccination_data[vaccination_data.columns[0:6]]
vaccination_data['District'] = vaccination_data['District'].str.lower()
vaccination_data


# ### Create dict of district ids with district names and corrosponding district key and state key

# In[110]:


district_id = dict()


# In[111]:


check_in_vaccine = list()


# In[112]:


neighbor_dataset_districts_list = list(neighbor_dataset_districts)
for i in range(len(neighbor_dataset_districts_list)):
    dist = neighbor_dataset_districts_list[i]
    row = vaccination_data[vaccination_data['District'] == dist][['District_Key','State_Code']]
    if row.empty:
        if dist=='delhi':
            district_id[dist] = ["DL_Delhi","DL"]
        else:                       #if any district from neighbor dataset not found in vaccine dataset report
            print(dist)
            check_in_vaccine.append(dist)
            print("ERROR")
            print()
    else:
        dist_id = row['District_Key'].tolist()[0]
        state_code = row['State_Code'].tolist()[0]
        district_id[dist] = [dist_id,state_code]


# In[113]:


l1 = vaccination_data['District'].tolist()


# In[114]:


district_id


# ### Create distric id CSV for refrence in future questions

# In[115]:


a_file = open("distric_ids.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = ['district','district_id','state_id'])
writer.writeheader()
writer = csv.writer(a_file)
for key, value in district_id.items():
    writer.writerow([key] + value)

a_file.close()


# In[116]:


items = list(neighbor.items())
items


# In[117]:


modified_neighbor_data = dict()


# ### Create modified neighbor data by replacing district in neighbors with actual district id

# In[118]:


for i in range(len(items)):
    dist = items[i][0]
    neighbors = items[i][1]
    dist_id = district_id[dist][0]
    neighbors_id = list()
    for j in range(len(neighbors)):
        neighbors_id.append(district_id[neighbors[j]][0]) #append the district keys for each neighbor of a district
    modified_neighbor_data[dist_id] = neighbors_id


# In[119]:


modified_neighbor_data


# In[120]:


modified_neighbor_data = OrderedDict(sorted(modified_neighbor_data.items()))   #sort outout according to district id of key
modified_neighbor_data


# ### sort outout according to district id of neighbors

# In[121]:


list1 = list(modified_neighbor_data.items())
for i in range(len(list1)):
    item = list1[i]
    key = item[0]
    value = item[1]
    value.sort()
    modified_neighbor_data[key] = value
modified_neighbor_data


# ### Create mofidfied neighbor json file as per question requirements

# In[122]:


with open("neighbor-districts-modified.json", "w") as outfile:
    json.dump(modified_neighbor_data, outfile)


# ### Create mofidfied neighbor json file 2 as according to common distric names with out district ids for refence in future questions

# In[123]:


with open("neighbor-districts-modified2.json", "w") as outfile:
    json.dump(neighbor, outfile)


# In[124]:


print("Ended Execution")

