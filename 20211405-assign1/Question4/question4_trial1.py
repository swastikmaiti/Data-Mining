#!/usr/bin/env python
# coding: utf-8

# In[1]:


print("Started Execution")


# In[2]:


import pandas as pd
import csv
import json
import datetime


# In[3]:


data = pd.read_csv("districts.csv")
data


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
districts_considered #district considered is the set of districts whose names are present in modified neighbor data


# In[11]:


delete_index = list()


# In[12]:


df = data


# ### Find the index form districts dtaset whose district are not to be considered

# In[13]:


for i in range(len(df)):
    if df.loc[i,"District"].lower() not in districts_considered:
        delete_index.append(i)
    


# In[14]:


district_removal_set = set()
redundant_index = list()


# In[15]:


for i in range(len(delete_index)):                                 #go through the index list for which districts are to be deleted
    index = delete_index[i]
    if df.loc[index,"District"].lower() in district_removal_set:   #if that district is already considered the add the indect to list of redundant indexes
        redundant_index.append(index)
    else:
        district_removal_set.add(df.loc[index,"District"].lower()) # else add the district to district removal set


# In[16]:


delete_index = list(set(delete_index) - set(redundant_index))


# In[17]:


l1 = list(districts_considered)
keep_index = list()


# ### Find distric names from district dataset whose subwords are similar to district in neighbor dataset

# In[18]:


for i in range(len(delete_index)):             #go through the list of districts which are not present in modified neighbor dataset
    w_district = df.loc[delete_index[i],"District"].lower()
    for j in range(len(l1)):                           #go through the districts in modified neighbor dataset
        w_districts_considered = l1[j]
        district_words = w_district.split()
        districts_considered_words = w_districts_considered.split()
        ignore = ["west","east","north","south","district","state"]   #remove these word befor comparating for similarity
        for k in range(len(ignore)):
            ignore_word = ignore[k]
            if ignore_word in district_words:
                district_words.remove(ignore_word)
            if ignore_word in districts_considered_words:
                districts_considered_words.remove(ignore_word)    
        for word in district_words:                           #if any word in naames of mismatch district 
            if word in districts_considered_words:            #  ....is present in words in district names from neighbor there exist a similarity
                keep_index.append(delete_index[i])


# In[19]:


delete_index = list(set(delete_index) - set(keep_index))


# In[20]:


delete_districts = set()


# ### Find the rows indexes from district dataset for which the district is not to be considered

# In[21]:


for i in range(len(delete_index)):
    index = delete_index[i]
    delete_dis = df.loc[index,"District"]
    delete_districts.add(delete_dis)


# In[22]:


delete_districts = list(delete_districts)


# In[23]:


df = pd.read_csv("districts.csv", index_col ="District" )


# ### Remove the rows indexes from district dataset for which the district is not to be considered

# In[24]:


df.drop(delete_districts, inplace = True)
df.reset_index(inplace = True)


# In[ ]:





# In[25]:


df = df[["Date","State","District","Confirmed"]]
df


# In[26]:


df[df['District']=='Dibrugarh']


# In[27]:


df1 = df.groupby(['State','District'])
df1.first()


# ### the date at overlapping weekly intervals of starting from 15th march

# In[28]:


weekly_dates = list()
x1 = datetime.date(2020, 3, 21)
x2 = datetime.date(2020, 3, 25)
y = datetime.date(2021, 8, 14)
status=0
while x1<=y:
    timestampStr = x1.strftime("%Y-%m-%d")
    weekly_dates.append(timestampStr)
    x1 = (x1 + datetime.timedelta(days=7))    #dates at 1 week interval
while x2<=y:
    timestampStr = x2.strftime("%Y-%m-%d")
    weekly_dates.append(timestampStr)
    x2 = (x2 + datetime.timedelta(days=7))    #overlapping dates ate 1 week interval


# In[29]:


weekly_dates.sort()


# In[ ]:





# In[30]:


group_dist = list(df1.groups.keys())
group_dist


# In[31]:


district_weekly_case = dict()
district_weekly_case1 = dict()
district_weekly_case2 = dict()


# ### Find the weekly case counts for each districts for the dates found above for overlapping weeks

# In[32]:


for i in range(len(group_dist)):
    key = group_dist[i][1]
    z = df1.get_group(group_dist[i])              #retrive the dataset under that particular district
    date = list(z['Date'])
    for j in range(0,len(weekly_dates),2):        #go through the list of weekly datses at 1 week interval
        d1 = weekly_dates[j]
        if d1 in date:
            row = z[z['Date'] == d1]              #retrive the row corrosponding to that particular date
            conf = int(row['Confirmed'])
            if key in district_weekly_case1.keys():
                total = sum(district_weekly_case1[key])
                district_weekly_case1[key].append(conf - total)   #update the weekly case count by subtructing previous counts from present count as its cumulative dataset
            else:
                district_weekly_case1[key] = list()
                district_weekly_case1[key].append(conf)
        else:
            if key in district_weekly_case1.keys():
                district_weekly_case1[key].append(0)
            else:
                district_weekly_case1[key] = list()
                district_weekly_case1[key].append(0)
    for j in range(1,len(weekly_dates),2):     #go through the list of weekly datses at 1 week interval intermeditate weeks
        d1 = weekly_dates[j]
        if d1 in date:
            row = z[z['Date'] == d1]            #retrive the row corrosponding to that particular date
            conf = int(row['Confirmed'])
            if key in district_weekly_case2.keys():
                total = sum(district_weekly_case2[key])
                district_weekly_case2[key].append(conf - total) #update the weekly case count by subtructing previous counts from present count as its cumulative dataset
            else:
                district_weekly_case2[key] = list()
                district_weekly_case2[key].append(conf)
        else:
            if key in district_weekly_case2.keys():
                district_weekly_case2[key].append(0)
            else:
                district_weekly_case2[key] = list()
                district_weekly_case2[key].append(0)
    p =  [sub[item] for item in range(len(district_weekly_case2[key]))         #merge the weekly counts from district_weekly_case1 and district_weekly_case2 to obtain etire ovelapping counts
                      for sub in [district_weekly_case1[key], district_weekly_case2[key]]]
    if key not in district_weekly_case.keys():
        district_weekly_case[key] = p


# In[33]:


weekly_dates


# In[34]:


len(weekly_dates)


# In[35]:


district_level_wave = dict()
date_dict = dict()


# ### Find the dates of 2 maximum peaks for each districts

# In[36]:


keys = list(district_weekly_case.keys())
for j in range(len(keys)):
    key = keys[j]
    a = district_weekly_case[key]
    start_index = 0
    for i in range(len(a)):
        if a[i]!=0:
            start_index = i         # strat index is the index where covid case count is non zero for first time
            break
    if start_index==0:
        continue
    window = 4            #dine window size to condiser to total case counts in that interval of window
    week_ids = dict()
    for i in range(start_index,len(a)-window*2,window):
        x1 = a[i:i+window]                   #case counts in first window interval
        x2 = a[i+window:i+(2*window)]        #case counts in next(2nd) window interval
        x3 = a[i+(2*window):i+(3*window)]    #case counts in next(3rd) window interval
        sum1 = sum(x1)                  #total case count in first window interval
        sum2 = sum(x2)                  #total case count in next(2nd) window interval
        sum3 = sum(x3)                  #total case count in next(3rd) window interval
        if sum1<sum2 and sum2>sum3:         #if middle window case count is more that case counts in first and last window means
            l1 = x1+x2+x3                   #....in this interival case increased from last interval and decreasing in next interval
            maxpos = l1.index(max(l1))      #....hence peak is detected
            max_case = max(l1)
            max_index = i+maxpos
            week = weekly_dates[max_index]
            week_ids[week] = max_index+1     #store the week index as vale of peak date
            date_dict[week] = max_case       #store number of cases in that peak
    
    max_key1 = max(date_dict, key=date_dict.get)     # find the peak with maximum case counts
    date_dict.pop(max_key1)
    max_key2 = max(date_dict, key=date_dict.get)     # find the peak with second maximum case counts
    l1 = [max_key1,max_key2]
    l1.sort()                                        #sort the two maximum peak dates to get peak timing of covid wave
    week_id1 = week_ids[l1[0]]
    week_id2 = week_ids[l1[1]]
    month_id1 = l1[0].split("-")
    month_id2 = l1[1].split("-")
    month_id1 = month_id1[1]
    month_id2 = month_id2[1]
    l2 = list()
    l2.append(week_id1)
    l2.append(week_id2)
    l1 = [int(month_id1),int(month_id2)]
    date_dict = dict()
    district_level_wave[key] = l2+l1


# In[37]:


district_level_wave


# In[ ]:





# In[38]:


district_ids = pd.read_csv("distric_ids.csv")


# In[39]:


items = list(district_level_wave.items())
for i in range(len(items)):
    old_key = items[i][0]
    dist = items[i][0].lower()
    dist_id = district_ids.loc[district_ids['district'] == dist].values.tolist()[0]
    district_level_wave[dist_id[1]] = district_level_wave.pop(old_key)


# In[40]:


district_level_wave


# ### Write the wave peaks dates ate distric level to csv file

# In[41]:


field_names = ['Districtid','wave1 - weekid','wave2_weekid','wave1_monthid','wave2_monthid']
field_names
a_file = open("district_peaks.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = field_names)
writer.writeheader()
writer = csv.writer(a_file)
for key, value in district_level_wave.items():
    writer.writerow([key] + value)

a_file.close()


# ### Repeat the above procedures to find pekas for each states

# In[42]:


df1 = df.groupby(['State'])
df1.first()


# In[43]:


weekly_dates = list()
x1 = datetime.date(2020, 3, 21)
x2 = datetime.date(2020, 3, 25)
y = datetime.date(2021, 8, 14)
status=0
while x1<=y:
    timestampStr = x1.strftime("%Y-%m-%d")
    weekly_dates.append(timestampStr)
    x1 = (x1 + datetime.timedelta(days=7))
while x2<=y:
    timestampStr = x2.strftime("%Y-%m-%d")
    weekly_dates.append(timestampStr)
    x2 = (x2 + datetime.timedelta(days=7))


# In[44]:


weekly_dates.sort()


# In[45]:


group_state = list(df1.groups.keys())


# In[46]:


state_weekly_case = dict()
state_weekly_case1 = dict()
state_weekly_case2 = dict()


# In[47]:


import numpy as np
for i in range(len(group_state)):
    key = group_state[i]
    z = df1.get_group(group_state[i])
    df2 = z.groupby(['Date'])
    z = df2['Confirmed'].agg(np.sum)
    z = z.to_frame()
    z.reset_index(level=0, inplace=True)
    date = list(z['Date'])
    for j in range(0,len(weekly_dates),2):
        d1 = weekly_dates[j]
        if d1 in date:
            row = z[z['Date'] == d1]
            conf = int(row['Confirmed'])
            if key in state_weekly_case1.keys():
                total = sum(state_weekly_case1[key])
                state_weekly_case1[key].append(conf - total)
            else:
                state_weekly_case1[key] = list()
                state_weekly_case1[key].append(conf)
        else:
            if key in state_weekly_case1.keys():
                state_weekly_case1[key].append(0)
            else:
                state_weekly_case1[key] = list()
                state_weekly_case1[key].append(0)
    for j in range(1,len(weekly_dates),2):
        d1 = weekly_dates[j]
        if d1 in date:
            row = z[z['Date'] == d1]
            conf = int(row['Confirmed'])
            if key in state_weekly_case2.keys():
                total = sum(state_weekly_case2[key])
                state_weekly_case2[key].append(conf - total)
            else:
                state_weekly_case2[key] = list()
                state_weekly_case2[key].append(conf)
        else:
            if key in state_weekly_case2.keys():
                state_weekly_case2[key].append(0)
            else:
                state_weekly_case2[key] = list()
                state_weekly_case2[key].append(0)
    p =  [sub[item] for item in range(len(state_weekly_case2[key]))
                      for sub in [state_weekly_case1[key], state_weekly_case2[key]]]
    if key not in district_weekly_case.keys():
        state_weekly_case[key] = p
    


# In[48]:


state_level_wave = dict()
date_dict = dict()


# In[49]:


keys = list(state_weekly_case.keys())
for j in range(len(keys)):
    key = keys[j]
    a = state_weekly_case[key]
    start_index = 0
    for i in range(len(a)):
        if a[i]!=0:
            start_index = i
            break
    if start_index==0:
        continue
    window = 4
    week_ids = dict()
    for i in range(start_index,len(a)-window*2,window):
        x1 = a[i:i+window]
        x2 = a[i+window:i+(2*window)]
        x3 = a[i+(2*window):i+(3*window)]
        sum1 = sum(x1)
        sum2 = sum(x2)
        sum3 = sum(x3)
        if sum1<sum2 and sum2>sum3:
            l1 = x1+x2+x3
            maxpos = l1.index(max(l1))
            max_case = max(l1)
            max_index = i+maxpos
            week = weekly_dates[max_index]
            date_dict[week] = max_case
            week_ids[week] = max_index+1
            
    max_key1 = max(date_dict, key=date_dict.get)
    date_dict.pop(max_key1)
    max_key2 = max(date_dict, key=date_dict.get)
    l1 = [max_key1,max_key2]
    l1.sort()
    week_id1 = week_ids[l1[0]]
    week_id2 = week_ids[l1[1]]
    l2 = list()
    l2.append(week_id1)
    l2.append(week_id2)
    month_id1 = l1[0].split("-")
    month_id2 = l1[1].split("-")
    month_id1 = month_id1[1]
    month_id2 = month_id2[1]
    l2 = list()
    l2.append(week_id1)
    l2.append(week_id2)
    l1 = [int(month_id1),int(month_id2)]
    date_dict = dict()
    state_level_wave[key] = l2+l1


# In[50]:


state_level_wave


# In[51]:


state_id = {'Andhra Pradesh': 'AP_Andhra Pradesh',
 'Arunachal Pradesh': 'AR_Arunachal Pradesh',
 'Bihar': 'BR_Bihar',
 'Chhattisgarh': 'CT_Chhattisgarh',
 'Dadra and Nagar Haveli and Daman and Diu': 'DN_Dadra and Nagar Haveli and Daman and Diu',
 'Gujarat': 'GJ_Gujarat',
 'Haryana': 'HR_Haryana',
 'Himachal Pradesh': 'HP_Himachal Pradesh',
 'Jammu and Kashmir': 'JK_Jammu and Kashmir',
 'Jharkhand': 'JH_Jharkhand',
 'Karnataka': 'KA_Karnataka',
 'Kerala': 'KL_Kerala',
 'Ladakh': 'LA_Ladakh',
 'Madhya Pradesh': 'MP_Madhya Pradesh',
 'Maharashtra': 'MH_Maharashtra',
 'Meghalaya': 'ML_Meghalaya',
 'Mizoram': 'MZ_Mizoram',
 'Nagaland': 'NL_Nagaland',
 'Odisha': 'OR_Odisha',
 'Punjab': 'PB_Punjab',
 'Rajasthan': 'RJ_Rajasthan',
 'Tamil Nadu': 'TN_Tamil Nadu',
 'Tripura': 'TR_Tripura',
 'Uttar Pradesh': 'UP_Uttar Pradesh',
 'Uttarakhand': 'UT_Uttarakhand',
 'West Bengal': 'WB_West Bengal'}


# In[52]:


list1 = list(state_level_wave.items())
for i in range(len(list1)):
    item = list1[i]
    old_key = item[0]
    new_key = state_id[old_key]
    state_level_wave[new_key] = state_level_wave.pop(old_key)
state_level_wave


# In[53]:


field_names = ['Stateid','wave1 - weekid','wave2_weekid','wave1_monthid','wave2_monthid']
field_names
a_file = open("state_peaks.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = field_names)
writer.writeheader()
writer = csv.writer(a_file)
for key, value in state_level_wave.items():
    writer.writerow([key] + value)

a_file.close()


# In[ ]:





# In[ ]:





# ### Repeat the above procedures to find pekas for the country

# In[54]:


df1 = df.groupby(['Date'])
df1.first()


# In[55]:


weekly_dates = list()
x1 = datetime.date(2020, 3, 21)
x2 = datetime.date(2020, 3, 25)
y = datetime.date(2021, 8, 14)
status=0
while x1<=y:
    timestampStr = x1.strftime("%Y-%m-%d")
    weekly_dates.append(timestampStr)
    x1 = (x1 + datetime.timedelta(days=7))
while x2<=y:
    timestampStr = x2.strftime("%Y-%m-%d")
    weekly_dates.append(timestampStr)
    x2 = (x2 + datetime.timedelta(days=7))


# In[56]:


weekly_dates.sort()
len(weekly_dates)


# In[57]:


group_date = list(df1.groups.keys())


# In[ ]:





# In[58]:


Total_weekly_case = dict()
Total_weekly_case1 = dict()
total_weekly_case2 = dict()
Total_tally = dict()


# In[59]:


for i in range(len(group_date)):
    key = group_date[i]
    #print(key)
    z = df1.get_group(group_date[i])
    z1 = z['Confirmed'].agg(np.sum)            #find the total case counts for each dates
    Total_tally[key] = z1
    


# In[60]:


date = list(Total_tally.keys())
for j in range(0,len(weekly_dates),2):
    d1 = weekly_dates[j]
    if d1 in date:
        conf = int(Total_tally[d1])
        if key in Total_weekly_case1.keys():
            total = sum(Total_weekly_case1[key])
            Total_weekly_case1[key].append(conf - total)
        else:
            Total_weekly_case1[key] = list()
            Total_weekly_case1[key].append(conf)
    else:
        if key in Total_weekly_case1.keys():
            Total_weekly_case1[key].append(0)
        else:
            Total_weekly_case1[key] = list()
            Total_weekly_case1[key].append(0)
for j in range(1,len(weekly_dates),2):
    d1 = weekly_dates[j]
    if d1 in date:
        conf = int(Total_tally[d1])
        if key in total_weekly_case2.keys():
            total = sum(total_weekly_case2[key])
            total_weekly_case2[key].append(conf - total)
        else:
            total_weekly_case2[key] = list()
            total_weekly_case2[key].append(conf)
    else:
        if key in total_weekly_case2.keys():
            total_weekly_case2[key].append(0)
        else:
            total_weekly_case2[key] = list()
            total_weekly_case2[key].append(0)
p =  [sub[item] for item in range(len(total_weekly_case2[key]))
                      for sub in [Total_weekly_case1[key], total_weekly_case2[key]]]
if key not in Total_weekly_case.keys():
    Total_weekly_case['INDIA'] = p
    


# In[61]:


country_level_wave = dict()


# In[62]:


keys = list(Total_weekly_case.keys())
for j in range(len(keys)):
    key = keys[j]
    a = Total_weekly_case[key]
    start_index = 0
    for i in range(len(a)):
        if a[i]!=0:
            start_index = i
            break
    window = 4
    week_ids = dict()
    for i in range(start_index,len(a)-window*2,window):
        x1 = a[i:i+window]
        x2 = a[i+window:i+(2*window)]
        x3 = a[i+(2*window):i+(3*window)]
        sum1 = sum(x1)
        sum2 = sum(x2)
        sum3 = sum(x3)
        if sum1<sum2 and sum2>sum3:
            l1 = x1+x2+x3
            maxpos = l1.index(max(l1))
            max_case = max(l1)
            max_index = i+maxpos
            week = weekly_dates[max_index]
            date_dict[week] = max_case
            week_ids[week] = max_index+1
            
    max_key1 = max(date_dict, key=date_dict.get)
    date_dict.pop(max_key1)
    max_key2 = max(date_dict, key=date_dict.get)
    l1 = [max_key1,max_key2]
    l1.sort()
    week_id1 = week_ids[l1[0]]
    week_id2 = week_ids[l1[1]]
    l2 = list()
    l2.append(week_id1)
    l2.append(week_id2)
    month_id1 = l1[0].split("-")
    month_id2 = l1[1].split("-")
    month_id1 = month_id1[1]
    month_id2 = month_id2[1]
    l2 = list()
    l2.append(week_id1)
    l2.append(week_id2)
    l1 = [int(month_id1),int(month_id2)]
    date_dict = dict()
    country_level_wave[key] = l2+l1


# In[63]:


country_level_wave


# In[64]:


field_names = ['Country','wave1 - weekid','wave2_weekid','wave1_monthid','wave2_monthid']
field_names
a_file = open("overall_peaks.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = field_names)
writer.writeheader()
writer = csv.writer(a_file)
for key, value in country_level_wave.items():
    writer.writerow([key] + value)

a_file.close()


# In[65]:


print("Ended Execution")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




