#!/usr/bin/env python
# coding: utf-8

# In[1]:


print("Started Executing")


# In[2]:


import pandas as pd
import csv
import json
import datetime


# In[3]:


data = pd.read_csv("districts.csv")


# In[4]:


data = data[["Date","State","District","Confirmed"]]
data


# ### Retrieve the set of districts in lowecase from distric dataset

# In[5]:


districts = data["District"].tolist()


# In[6]:


for i in range(len(districts)):
    districts[i] = districts[i].lower()


# In[7]:


districts = set(districts)


# ### Read the modified neighbor districts json data to retrieve set of districs to be considered in district dataset

# In[8]:


f = open ('neighbor-districts-modified2.json', "r")


# In[9]:


districts_considered = json.loads(f.read())


# In[10]:


districts_considered = set(districts_considered)
districts_considered            #district considered is the set of districts whose names are present in modified neighbor data


# In[11]:


len(districts - districts_considered)


# In[12]:


delete_index = list()


# In[13]:


df = data


# ### Find the index form districts dataset whose district are not to be considered

# In[14]:


for i in range(len(df)):
    if df.loc[i,"District"].lower() not in districts_considered:
        delete_index.append(i)
    


# In[15]:


len(delete_index)


# In[16]:


district_removal_set = set()
redundant_index = list()


# In[17]:


for i in range(len(delete_index)):  #go through the index list for which districts are to be deleted
    index = delete_index[i]
    if df.loc[index,"District"].lower() in district_removal_set:  #if that district is already considered the add the indect to list of redundant indexes
        redundant_index.append(index)
    else:
        district_removal_set.add(df.loc[index,"District"].lower()) # else add the district to district removal set


# In[18]:


delete_index = list(set(delete_index) - set(redundant_index))


# In[19]:


len(delete_index)


# In[20]:


df


# In[21]:


l1 = list(districts_considered)
keep_index = list()


# ### Find distric names from district dataset whose subwords are similar to district in neighbor dataset

# In[22]:


for i in range(len(delete_index)):                 #go through the list of districts which are not present in modified neighbor dataset
    w_district = df.loc[delete_index[i],"District"].lower()
    for j in range(len(l1)):                       #go through the districts in modified neighbor dataset
        w_districts_considered = l1[j]
        district_words = w_district.split()
        districts_considered_words = w_districts_considered.split()
        ignore = ["west","east","north","south","district","state"] #remove these word befor comparating for similarity
        for k in range(len(ignore)):
            ignore_word = ignore[k]
            if ignore_word in district_words:
                district_words.remove(ignore_word)
            if ignore_word in districts_considered_words:
                districts_considered_words.remove(ignore_word)    
        for word in district_words:                  #if any word in naames of mismatch district 
            if word in districts_considered_words:   #  ....is present in words in district names from neighbor there exist a similarity
                keep_index.append(delete_index[i])


# In[23]:


delete_index = list(set(delete_index) - set(keep_index))


# In[24]:


len(delete_index)


# In[25]:


delete_districts = set()


# ### Find the rows indexes from district dataset for which the district is not to be considered

# In[26]:


for i in range(len(delete_index)):
    index = delete_index[i]
    delete_dis = df.loc[index,"District"]
    delete_districts.add(delete_dis)


# In[27]:


delete_districts = list(delete_districts)


# In[28]:


df = pd.read_csv("districts.csv", index_col ="District" )


# ### Remove the rows indexes from district dataset for which the district is not to be considered

# In[29]:


df.drop(delete_districts, inplace = True)
df.reset_index(inplace = True)


# In[30]:


df


# In[31]:


df = df[["Date","State","District","Confirmed"]]
df


# In[32]:


df1 = df.groupby(['State','District'])


# In[33]:


df1.first()


# In[34]:


df1.ngroups


# ### the date at weekly interval of 7 days starting from 15th march

# In[35]:


weekly_dates = list()
x = datetime.date(2020, 3, 21)
y = datetime.date(2021, 8, 14)
while x<=y:
    timestampStr = x.strftime("%Y-%m-%d")
    weekly_dates.append(timestampStr)
    x = (x + datetime.timedelta(days=7))


# In[36]:


group_dist = list(df1.groups.keys())
group_dist


# In[37]:


df1.get_group(group_dist[0])


# In[38]:


weekly_case = dict()


# ### Find the weekly case counts for each districts for the dates found above

# In[39]:


for i in range(len(group_dist)):
    key = group_dist[i][1]
    z = df1.get_group(group_dist[i])     #retrive the dataset under that particular district
    date = list(z['Date'])
    for j in range(len(weekly_dates)):   #go through the list of weekly datses to consider
        d1 = weekly_dates[j]
        if d1 in date:
            row = z[z['Date'] == d1]               #retrive the row corrosponding to that particular date
            conf = int(row['Confirmed'])
            if key in weekly_case.keys():          #update the weekly case count by subtructing previous counts from present count as its cumulative dataset
                total = sum(weekly_case[key])
                weekly_case[key].append(conf - total)
            else:
                weekly_case[key] = list()
                weekly_case[key].append(conf)
        else:                                      #if data for a week is not available insert zero
            if key in weekly_case.keys():
                weekly_case[key].append(0)
            else:
                weekly_case[key] = list()
                weekly_case[key].append(0)
            


# In[40]:


weekly_case


# In[41]:


district_ids = pd.read_csv("distric_ids.csv")


# In[42]:


district_ids


# ### Update the district weekly case by replacing district names with district key as in modified neighbor dataset

# In[43]:


items = list(weekly_case.items())
for i in range(len(items)):
    old_key = items[i][0]
    dist = items[i][0].lower()
    dist_id = district_ids.loc[district_ids['district'] == dist].values.tolist()[0]
    weekly_case[dist_id[1]] = weekly_case.pop(old_key)


# In[44]:


weekly_case


# In[45]:


field_names = ['Districtid']
field_names


# In[46]:


for i in range(len(weekly_case['AP_Anantapur'])):
    x = "week"+str((i+1))
    field_names.append(x)


# ### Write the district weekly case in the csv file

# In[47]:


a_file = open("weekly-cases-time.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = field_names)
writer.writeheader()
writer = csv.writer(a_file)
for key, value in weekly_case.items():
    writer.writerow([key] + value)

a_file.close()


# ### the date at monthly interval of 30 days starting from 15th march

# In[48]:


monthly_dates = list()
x = datetime.date(2020, 4, 14)
y = datetime.date(2021, 8, 14)
for i in range(4,13):
    x = datetime.date(2020, i, 14)
    timestampStr = x.strftime("%Y-%m-%d")
    monthly_dates.append(timestampStr)
for i in range(1,9):
    x = datetime.date(2021, i, 14)
    timestampStr = x.strftime("%Y-%m-%d")
    monthly_dates.append(timestampStr)


# In[49]:


group_dist = list(df1.groups.keys())


# In[50]:


monthly_case = dict()


# ### Find the monthly case counts for each districts for the dates found above

# In[51]:


for i in range(len(group_dist)):
    key = group_dist[i][1]
    z = df1.get_group(group_dist[i])
    date = list(z['Date'])
    for j in range(len(monthly_dates)):
        d1 = weekly_dates[j]
        if d1 in date:
            row = z[z['Date'] == d1]
            conf = int(row['Confirmed'])
            if key in monthly_case.keys():
                total = sum(monthly_case[key])
                monthly_case[key].append(conf - total)
            else:
                monthly_case[key] = list()
                monthly_case[key].append(conf)
        else:
            if key in monthly_case.keys():
                monthly_case[key].append(0)
            else:
                monthly_case[key] = list()
                monthly_case[key].append(0)
            


# In[52]:


items = list(monthly_case.items())
for i in range(len(items)):
    old_key = items[i][0]
    dist = items[i][0].lower()
    dist_id = district_ids.loc[district_ids['district'] == dist].values.tolist()[0]
    monthly_case[dist_id[1]] = monthly_case.pop(old_key)


# In[53]:


monthly_case


# In[54]:


field_names = ['Districtid']
field_names


# In[55]:


for i in range(len(monthly_case['AP_Anantapur'])):
    x = "month"+str((i+1))
    field_names.append(x)


# ### Write the district weekly case in the csv file

# In[56]:


a_file = open("monthly-cases-time.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = field_names)
writer.writeheader()
writer = csv.writer(a_file)
for key, value in monthly_case.items():
    writer.writerow([key] + value)

a_file.close()


# In[ ]:





# In[ ]:





# In[57]:


group_dist = list(df1.groups.keys())


# In[58]:


overall_case = dict()


# ### Find the last value as the final count of cases

# In[59]:


for i in range(len(group_dist)):
    key = group_dist[i][1]
    z = df1.get_group(group_dist[i])
    z = z.iloc[-1]
    overall_case[key] = z['Confirmed']


# ### Find over all case for each districts

# In[60]:


items = list(overall_case.items())
for i in range(len(items)):
    old_key = items[i][0]
    dist = items[i][0].lower()
    dist_id = district_ids.loc[district_ids['district'] == dist].values.tolist()[0]
    overall_case[dist_id[1]] = overall_case.pop(old_key)


# In[61]:


overall_case


# In[62]:


field_names = ['Districtid','overall']


# ### Write the district overall case in the csv file

# In[63]:


a_file = open("overall-cases-time.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = field_names)
writer.writeheader()
writer = csv.writer(a_file)
for key, value in overall_case.items():
    writer.writerow([key,value])

a_file.close()


# In[64]:


print("Ended Execution")

