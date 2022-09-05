#!/usr/bin/env python
# coding: utf-8

# In[1]:


print("Started Execution")


# In[2]:


import pandas as pd
from datetime import datetime
from datetime import timedelta
import math
import csv


# In[3]:


data = pd.read_csv("census_data.csv")


# In[4]:


data = data[["Level","Name","TRU","TOT_P","TOT_M","TOT_F"]]


# In[5]:


data


# ### Funtion to update census stste names according to names in vaccination data

# In[6]:


def update_census_data(Dict1):
    l1 = list(vaccine_similar_census_dict.items())
    for i in range(len(l1)):
        item = l1[i]
        vaccine_name = item[0]
        census_name = item[1]
        df.loc[(df.Name == census_name),'Name']=vaccine_name


# In[ ]:





# In[7]:


vaccine_data = pd.read_csv("cowin_vaccine_data_districtwise.csv",low_memory=False)


# In[8]:


sub_header = vaccine_data.iloc[0].tolist()
sub_header = sub_header[5:]
sub_header = sub_header[:10]
sub_header


# In[9]:


df1 = vaccine_data.groupby(['State'])
df1.first()


# In[10]:


group_state = list(df1.groups.keys())
group_state


# In[11]:


vaccine_state = group_state


# In[12]:


for i in range(len(vaccine_state)):
    vaccine_state[i] = vaccine_state[i].lower()


# In[13]:


vaccine_state_set = set(vaccine_state)


# In[14]:


data = pd.read_csv("census_data.csv")


# In[15]:


data = data[["Level","Name","TRU","TOT_P","TOT_M","TOT_F"]]
data


# In[16]:


df = data[data['Level'] == "STATE"]


# In[17]:


df = df[df['TRU'] == "Total"]


# In[18]:


df['Name'] = df['Name'].str.lower()
census_dataset = df
census_dataset


# In[19]:


census_sates = df["Name"].tolist()
census_state_set = set(census_sates)


# In[ ]:





# In[20]:


census_state_set


# In[21]:


vaccine_state_set - census_state_set


# In[22]:


census_state_set


# ### Find the states name in vaccination dataset and its equivalent name in census dataset

# In[23]:


vaccine_similar_census_dict = {'andaman and nicobar islands':'andaman & nicobar islands','jammu and kashmir':'jammu & kashmir','delhi':'nct of delhi'}


# In[24]:


update_census_data(vaccine_similar_census_dict)


# In[25]:


census_sates = df["Name"].tolist()
census_state_set = set(census_sates)


# In[26]:


vaccine_state_set - census_state_set


# In[27]:


census_state_set - vaccine_state_set


# ### Merge the following districts in census dataset according to single distric in vaccination dataset

# In[28]:


row1 = census_dataset[census_dataset["Name"] == 'dadra & nagar haveli']
row2 = census_dataset[census_dataset["Name"] == 'daman & diu']


# In[29]:


#print(row1)
#print(row2)


# In[30]:


census_dataset = census_dataset[~census_dataset["Name"].isin(['dadra & nagar haveli', 'daman & diu'])]


# In[31]:


df.loc[len(census_dataset.index)] = ['STATE','dadra and nagar haveli and daman and diu','Total', 586956,344061,242895] 


# In[32]:


df


# In[33]:


census_sates = df["Name"].tolist()
census_state_set = set(census_sates)


# In[34]:


vaccine_m_census = vaccine_state_set - census_state_set
vaccine_m_census


# In[35]:


census_dataset = df


# In[ ]:





# In[36]:


index_no = vaccine_data.columns.get_loc('15/08/2021')
index_no


# In[37]:


df1 = vaccine_data
df1 = df1[df1.columns[1:index_no-1]]


# In[38]:


df1 = vaccine_data
df1 = df1[df1.columns[1:index_no-1]]
vaccine_data = df1


# In[39]:


state_names = pd.DataFrame()      # create a new data frame to compre state names with state codes


# In[40]:


df1['District'] = df1['District'].str.lower()
state_names['State_name_original'] = df1['State'].tolist()   # preserve the original state name in new data frame without converting to lowercase
df1['State'] = df1['State'].str.lower()
state_names['State'] = df1['State'].tolist()
state_names['State_Code'] = df1['State_Code'].tolist()        # Store the corrospondind state codes in new data frame
df1


# In[41]:


df1 = df1[~df1['State'].isin(vaccine_m_census)]


# In[42]:


vaccine_state = df1["State"].tolist()
vaccine_state_set = set(vaccine_state)


# In[43]:


vaccine_state_set - census_state_set


# In[ ]:





# In[ ]:





# In[44]:


df1 = df1.groupby(['State'])
df1.first()


# In[45]:


group_state = list(df1.groups.keys())
group_state


# ###  For each state find the total number of dose1 vaccination in 1 week endind at 12/08/21. Find the population left for dose 1 vaccination and expected completion date of dose1 vaccination

# In[46]:


state_ratio = dict()


# In[47]:


for i in range(len(group_state)):
    key = group_state[i]
    z = df1.get_group(group_state[i])       #retrive vaccination information data for the entire state
    z = z[z.columns[5:]]                    #consider data only for dates
    z.dropna(inplace=True)
    z = z.astype(int)                       #covert the dataframe to numeric type
    x = z.sum(axis = 0, skipna = True)      #sum up counts for all districts in that state
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
    
    
    vaccination_rate_week = z[['14/08/2021.3','07/08/2021.3']] ##retrive dose1 count at one week ending at 14th Aug21
    li = vaccination_rate_week.values.tolist()
    li = li[0]
    dose1 = li[1]
    one_week = li[0]-li[1]   # calculate vaccination dose 1 count in tahe week
    rate = one_week/7        # calculate vaccination rate in that week interval
    row = census_dataset[census_dataset["Name"] == key]  # retrive total population of that state from census dataset
    total_population = sum(row['TOT_P'].tolist())
   
    population_left = total_population - dose1           #calculate remaining population not received dose1
    remaining_days = math.ceil(population_left/rate)     #caqlculate number of days required to vaccinate remaining population
    present_day = datetime.strptime("14-08-2021", "%d-%m-%Y")
    enddate = present_day + timedelta(days=remaining_days) # calculate the expexted date at which dose1 vaccination will be completed
    enddate = enddate.strftime('%d/%m/%Y')
    state_ratio[key] = [population_left,rate,enddate]


# In[48]:


state_ratio


# In[49]:


items = list(state_ratio.items())
for i in range(len(items)):
    old_key = items[i][0]
    state_id = state_names.loc[state_names['State'] == old_key][['State_Code','State_name_original']].values.tolist()[0]
    state_code = state_id[0]
    state = state_id[1]
    new_key = state_code+"_"+state
    state_ratio[new_key] = state_ratio.pop(old_key)   #update state name with state key


# In[50]:


state_ratio


# In[51]:


field_names = ['stateid','populationleft',', rate of vaccination','date']


# In[52]:


a_file = open("complete-vaccination.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = field_names)
writer.writeheader()
writer = csv.writer(a_file)
for key, values in state_ratio.items():
    writer.writerow([key]+values)

a_file.close()


# In[53]:


print("Ended Execution")


# In[ ]:





# In[ ]:




