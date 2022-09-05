#!/usr/bin/env python
# coding: utf-8

# In[1]:


print("Stareted Execution")


# In[2]:


import pandas as pd
import requests
import json
import csv
from collections import OrderedDict


# In[3]:


data = pd.read_csv("cowin_vaccine_data_districtwise.csv",low_memory=False)


# In[4]:


index_no = data.columns.get_loc('02/09/2021') #from this date onward no data is available
index_no


# In[5]:


df = data


# ### Consider the data upto which vaccination data is available

# In[6]:


df = df[df.columns[1:index_no-1]]


# In[7]:


df


# ### Find the sub headers under the dates

# In[8]:


sub_header = df.iloc[0].tolist()


# In[9]:


sub_header = sub_header[5:]
sub_header


# In[10]:


sub_header = sub_header[:10]
sub_header


# In[ ]:





# In[ ]:





# In[11]:


df.dropna(inplace=True)


# In[12]:


df1 = df.groupby(['State','District'])
df1.first()


# In[13]:


group_dist = list(df1.groups.keys())
group_dist


# In[14]:


len(group_dist)


# In[ ]:





# In[15]:


district_weekly = dict()


# ### Find the weekly counts of vaccine doses for each districts

# In[16]:


for i in range(len(group_dist)):
    key = group_dist[i][1]
    z = df1.get_group(group_dist[i])        #retrieve the dataset under that district
    district_id = z['District_Key']
    column_length = len(z.columns)
    start = 5                               #date wise information starts from column index location 5                         
    stop = start+len(sub_header)            #sub information of a date ends at from column index after interval of sub_header length
    week_no=1
    date_id = 0
    dose1 = 0
    dose2 = 0
    dose1_prev = 0;
    dose2_prev = 0
    dose_list = dict()
    

    for week in range(60,column_length+1,70): #go through each week. Each date has 10 sub_header. First week information starts at colum index 60
        if week+stop<=column_length:
            z1 = z[z.columns[week+start:week+stop]]
            date_id = z1.columns[0]
            doses = z1.iloc[:,[3,4]]                  #get counts of dose 1 and dose 2
            doses = doses.values.tolist()[0]
            doses = [0 if x != x else x for x in doses]
            temp1 =dose1_prev
            temp2 = dose2_prev
            dose1 = int(doses[0])                    # convert dose counts to int data type
            dose2 = int(doses[1])
            dose1_prev = dose1
            dose2_prev = dose2
            dose1 = dose1 - temp1                    # subtruct previous dose count from current count to obtain doses at 1 week interval as its cumulative data
            dose2 = dose2 - temp2
            dose_list[date_id]=[dose1,dose2]
            district_weekly[key] = dose_list
    


# In[17]:


district_weekly


# In[18]:


items = list(district_weekly.items())
for i in range(len(items)):
    old_key = items[i][0]
    dist_id = df.loc[df['District'] == old_key]['District_Key'].tolist()
    district_weekly[dist_id[0]] = district_weekly.pop(old_key) #update district name with district key


# In[19]:


district_weekly


# In[20]:


district_weekly = OrderedDict(sorted(district_weekly.items()))   #sort outout according to district id
district_weekly


# In[ ]:





# In[21]:


z = district_weekly['AN_Nicobars']


# In[22]:


keys = list(z.keys())


# In[23]:


field_names = ['Districtid']
for i in range(len(keys)):
    a1 = keys[i]+"dose1"
    a2 = keys[i]+"dose2"
    field_names.append(a1)
    field_names.append(a2)


# In[24]:


a_file = open("weekly_district_vaccinated-count-time.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = field_names)
writer.writeheader()
writer = csv.writer(a_file)
for key, values in district_weekly.items():
    l1 = [key]
    for value in values:
        l1 = l1+district_weekly[key][value]
    writer.writerow(l1)

a_file.close()


# In[25]:


district_monthly = dict()


# ### Find the monthly counts of vaccine doses for each districts

# In[26]:


for i in range(len(group_dist)):
    key = group_dist[i][1]
    z = df1.get_group(group_dist[i])
    district_id = z['District_Key']
    column_length = len(z.columns)
    start = 0
    stop = start+len(sub_header)
    week_no=1
    date_id = 0
    dose1 = 0
    dose2 = 0
    dose1_prev = 0
    dose2_prev = 0
    dose_list = dict()
    
    dates = ['14/02/2021','14/03/2021','14/04/2021','14/05/2021','14/06/2021','14/07/2021','14/08/2021']  #dates at monthly interval of 30 days
    for i in range(len(dates)):
        date_id = dates[i]
        index_no = z.columns.get_loc(date_id)              #get index of column where information of that date is available
        z1 = z[z.columns[index_no+start:index_no+stop]]    #retrieve all the information for all sub headers of that date
        date_id = z1.columns[0]
        doses = z1.iloc[:,[3,4]]
        doses = doses.values.tolist()[0]
        doses = [0 if x != x else x for x in doses]
        temp1 =dose1_prev
        temp2 = dose2_prev
        dose1 = int(doses[0])
        dose2 = int(doses[1])
        dose1_prev = dose1
        dose2_prev = dose2
        dose1 = dose1 - temp1
        dose2 = dose2 - temp2
        dose_list[date_id]=[dose1,dose2]
        district_monthly[key] = dose_list
    


# In[27]:


district_monthly


# In[28]:


items = list(district_monthly.items())
for i in range(len(items)):
    old_key = items[i][0]
    dist_id = df.loc[df['District'] == old_key]['District_Key'].tolist()
    district_monthly[dist_id[0]] = district_monthly.pop(old_key)


# In[29]:


district_monthly


# In[30]:


district_monthly = OrderedDict(sorted(district_monthly.items()))
district_monthly


# In[31]:


z = district_weekly['AN_Nicobars']


# In[32]:


keys = list(z.keys())


# In[33]:


field_names = ['Districtid']
for i in range(len(keys)):
    a1 = keys[i]+"dose1"
    a2 = keys[i]+"dose2"
    field_names.append(a1)
    field_names.append(a2)


# In[34]:


a_file = open("monthly_district_vaccinated-count-time.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = field_names)
writer.writeheader()
writer = csv.writer(a_file)
for key, values in district_weekly.items():
    l1 = [key]
    for value in values:
        l1 = l1+district_weekly[key][value]
    writer.writerow(l1)

a_file.close()


# In[ ]:





# In[35]:


district_overall = dict()
dose_list = list()


# ### Find the overall counts of vaccine doses for each districts

# In[36]:


for i in range(len(group_dist)):
    key = group_dist[i][1]
    z = df1.get_group(group_dist[i])
    district_id = z['District_Key']
    column_length = len(z.columns)
    z1 = z.iloc[: , -9:]             #consider only the dose counts of last date
    date_id = z1.columns[0]
    doses = z1.iloc[:,[3,4]]
    doses = doses.values.tolist()[0]
    doses = [0 if x != x else x for x in doses]
    dose1 = int(doses[0])
    dose2 = int(doses[1])
    dose_list=[dose1,dose2]
    district_overall[key] = dose_list


# In[37]:


district_overall


# In[38]:


items = list(district_overall.items())
for i in range(len(items)):
    old_key = items[i][0]
    dist_id = df.loc[df['District'] == old_key]['District_Key'].tolist()
    district_overall[dist_id[0]] = district_overall.pop(old_key)


# In[39]:


district_overall


# In[40]:


district_overall = OrderedDict(sorted(district_overall.items()))
district_overall


# In[41]:


field_names = ['Districtid','dose1','dose']


# In[42]:


a_file = open("overall_district_vaccinated-count-time.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = field_names)
writer.writeheader()
writer = csv.writer(a_file)
for key, values in district_overall.items():
    writer.writerow([key]+values)

a_file.close()


# In[ ]:





# ### Repeat the obove procedures to find weekly, monthly and overall vaccine doses for each states

# In[43]:


df1 = df.groupby(['State'])
df1.first()


# In[44]:


group_state = list(df1.groups.keys())
group_state


# In[45]:


state_weekly = dict()


# In[46]:


for i in range(len(group_state)):
    key = group_state[i]
    z = df1.get_group(group_state[i])            #retrive vaccination information data for the entire state
    z = z[z.columns[5:]]                        #consider data only for dates
    z = z.astype(int)                           #covert the dataframe to numeric type
    x = z.sum(axis = 0, skipna = True)          #sum up counts for all districts in that state
    #covert into dataframe of counts date wise for entire state
    x = x.to_frame()
    x.reset_index(level=0, inplace=True)
    x = x.T
    x.reset_index(level=0, inplace=True)
    index = x.index
    x = x[x.columns[1:]]
    header_row = 0
    x.columns = x.iloc[header_row]
    x = x.drop(header_row)
    z = x.reset_index(drop=True)
    
    
    column_length = len(z.columns)
    start = 0
    stop = start+len(sub_header)
    week_no=1
    date_id = 0
    dose1 = 0
    dose2 = 0
    dose1_prev = 0;
    dose2_prev = 0
    dose_list = dict()
    

    for week in range(60,column_length+1,70):
        if week+stop<=column_length:
            z1 = z[z.columns[week+start:week+stop]]
            date_id = z1.columns[0]
            doses = z1.iloc[:,[3,4]]
            doses = doses.values.tolist()[0]
            doses = [0 if x != x else x for x in doses]
            temp1 =dose1_prev
            temp2 = dose2_prev
            dose1 = int(doses[0])
            dose2 = int(doses[1])
            dose1_prev = dose1
            dose2_prev = dose2
            dose1 = dose1 - temp1
            dose2 = dose2 - temp2
            dose_list[date_id]=[dose1,dose2]
            state_weekly[key] = dose_list
    


# In[47]:


items = list(state_weekly.items())
for i in range(len(items)):
    old_key = items[i][0]
    state_id = df1.get_group(old_key).iloc[0]['State_Code']
    new_key = state_id+"_"+old_key
    state_weekly[new_key] = state_weekly.pop(old_key) #update state name with state key


# In[48]:


state_weekly


# In[49]:


state_weekly = OrderedDict(sorted(state_weekly.items()))    #sort output according to state id
state_weekly


# In[ ]:





# In[50]:


z = state_weekly['AN_Andaman and Nicobar Islands']


# In[51]:


keys = list(z.keys())


# In[52]:


field_names = ['stateid']
for i in range(len(keys)):
    a1 = keys[i]+"dose1"
    a2 = keys[i]+"dose2"
    field_names.append(a1)
    field_names.append(a2)


# In[53]:


a_file = open("weekly_state_vaccinated-count-time.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = field_names)
writer.writeheader()
writer = csv.writer(a_file)
for key, values in state_weekly.items():
    l1 = [key]
    for value in values:
        l1 = l1+state_weekly[key][value]
    writer.writerow(l1)

a_file.close()


# In[54]:


state_monthly = dict()


# In[55]:


for i in range(len(group_state)):
    key = group_state[i]
    z = df1.get_group(group_state[i])
    z = z[z.columns[5:]]
    z = z.astype(int)
    x = z.sum(axis = 0, skipna = True)
    x = x.to_frame()
    x.reset_index(level=0, inplace=True)
    x = x.T
    x.reset_index(level=0, inplace=True)
    index = x.index
    x = x[x.columns[1:]]
    header_row = 0
    x.columns = x.iloc[header_row]
    x = x.drop(header_row)
    z = x.reset_index(drop=True)
    
    
    column_length = len(z.columns)
    start = 0
    stop = start+len(sub_header)
    week_no=1
    date_id = 0
    dose1 = 0
    dose2 = 0
    dose1_prev = 0
    dose2_prev = 0
    dose_list = dict()
    
    dates = ['14/02/2021','14/03/2021','14/04/2021','14/05/2021','14/06/2021','14/07/2021','14/08/2021']
    for i in range(len(dates)):
        date_id = dates[i]
        index_no = z.columns.get_loc(date_id)
        z1 = z[z.columns[index_no+start:index_no+stop]]
        date_id = z1.columns[0]
        doses = z1.iloc[:,[3,4]]
        doses = doses.values.tolist()[0]
        doses = [0 if x != x else x for x in doses]
        temp1 =dose1_prev
        temp2 = dose2_prev
        dose1 = int(doses[0])
        dose2 = int(doses[1])
        dose1_prev = dose1
        dose2_prev = dose2
        dose1 = dose1 - temp1
        dose2 = dose2 - temp2
        dose_list[date_id]=[dose1,dose2]
        state_monthly[key] = dose_list
    


# In[56]:


state_monthly


# In[57]:


items = list(state_monthly.items())
for i in range(len(items)):
    old_key = items[i][0]
    state_id = df1.get_group(old_key).iloc[0]['State_Code']
    new_key = state_id+"_"+old_key
    state_monthly[new_key] = state_monthly.pop(old_key) #update state names with state key


# In[58]:


z = state_monthly['AN_Andaman and Nicobar Islands']


# In[59]:


state_monthly = OrderedDict(sorted(state_monthly.items()))
state_monthly


# In[60]:


keys = list(z.keys())


# In[61]:


field_names = ['stateid']
for i in range(len(keys)):
    a1 = keys[i]+"dose1"
    a2 = keys[i]+"dose2"
    field_names.append(a1)
    field_names.append(a2)


# In[62]:


a_file = open("monthly_state_vaccinated-count-time.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = field_names)
writer.writeheader()
writer = csv.writer(a_file)
for key, values in state_weekly.items():
    l1 = [key]
    for value in values:
        l1 = l1+state_weekly[key][value]
    writer.writerow(l1)

a_file.close()


# In[63]:


state_overall = dict()
dose_list = list()


# In[64]:


for i in range(len(group_state)):
    key = group_state[i]
    z = df1.get_group(group_state[i])
    z = z[z.columns[5:]]
    z.dropna(inplace=True)
    z = z.astype(int)
    x = z.sum(axis = 0, skipna = True)
    x = x.to_frame()
    x.reset_index(level=0, inplace=True)
    x = x.T
    x.reset_index(level=0, inplace=True)
    index = x.index
    x = x[x.columns[1:]]
    header_row = 0
    x.columns = x.iloc[header_row]
    x = x.drop(header_row)
    z = x.reset_index(drop=True)
    
    z1  = z.iloc[: , -9:]
    doses = z1.iloc[:,[3,4]]
    doses = doses.values.tolist()[0]
    doses = [0 if x != x else x for x in doses]
    dose1 = int(doses[0])
    dose2 = int(doses[1])
    dose_list = [dose1,dose2]
    state_overall[key] = dose_list
    


# In[ ]:





# In[65]:


items = list(state_overall.items())
for i in range(len(items)):
    old_key = items[i][0]
    state_id = df1.get_group(old_key).iloc[0]['State_Code']
    new_key = state_id+"_"+old_key
    state_overall[new_key] = state_overall.pop(old_key) #update state name with state key


# In[66]:


state_overall


# In[67]:


state_overall = OrderedDict(sorted(state_overall.items()))
state_overall


# In[68]:


field_names = ['Stateid','dose1','dose']


# In[69]:


a_file = open("overall_state_vaccinated-count-time.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = field_names)
writer.writeheader()
writer = csv.writer(a_file)
for key, values in state_overall.items():
    writer.writerow([key]+values)

a_file.close()


# In[70]:


print("Ended Execution")

