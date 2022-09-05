#!/usr/bin/env python
# coding: utf-8

# In[1]:


print("Started Execution")


# In[2]:


import pandas as pd
import csv


# In[3]:


vaccine_data = pd.read_csv("cowin_vaccine_data_districtwise.csv",low_memory=False)


# In[4]:


index_no = vaccine_data.columns.get_loc('02/09/2021') #from this date onward no vaccination data is available
index_no


# In[5]:


df1 = vaccine_data
df =df1


# In[6]:


df1 = df1[df1.columns[1:index_no]]


# ### Find the sub headers under the dates

# In[7]:


sub_header = df1.iloc[0].tolist()


# In[8]:


sub_header = sub_header[5:15]
sub_header


# In[9]:


df1.dropna(inplace=True)
vaccine_data = df1


# In[10]:


df1 = df1.groupby(['State','District'])
df1.first()


# In[11]:


group_dist = list(df1.groups.keys())
group_dist


# In[12]:


district_ratio = dict()


# ### For each districts find total number of covidhield and covaxin doses and their ratios

# In[13]:


for i in range(len(group_dist)):
    key = group_dist[i][1]
    z = df1.get_group(group_dist[i])   #Retrieve the vaccination data for that district
    district_id = z['District_Key']
    column_length = len(z.columns)
    z1 = z.iloc[: , -9:]               #retrieve vaccination data for the last date
    date_id = z1.columns[0]
    doses = z1.iloc[:,[7,8]]           #retrieve covaxin and covidhield dose count
    doses = doses.values.tolist()[0]
    doses = [0 if x != x else x for x in doses]
    covaxin = int(doses[0])
    covishield = int(doses[1])
    
    if covaxin>0:
        vaccination_ratio = covishield/covaxin        #calculate the dose ratio
    else:
        vaccination_ratio = float("NAN")
    district_ratio[key] = [vaccination_ratio]   


# In[ ]:





# In[14]:


district_ratio


# In[15]:


items = list(district_ratio.items())
for i in range(len(items)):
    old_key = items[i][0]
    dist_id = df.loc[df['District'] == old_key]['District_Key'].tolist() #convert district names to district ids
    district_ratio[dist_id[0]] = district_ratio.pop(old_key)


# In[16]:


district_ratio


# In[ ]:





# In[17]:


field_names = ['districtid','vaccineratio']


# In[18]:


a_file = open("district_vaccine-type-ratio.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = field_names)
writer.writeheader()
writer = csv.writer(a_file)
for key, values in district_ratio.items():
    writer.writerow([key]+values)

a_file.close()


# In[ ]:





# In[19]:


df1 = vaccine_data.groupby(['State'])
df1.first()


# In[20]:


group_state = list(df1.groups.keys())
group_state


# ### For each states find total number of covidhield and covaxin doses and their ratios

# In[21]:


state_ratio = dict()


# In[22]:


for i in range(len(group_state)):
    key = group_state[i]
    z = df1.get_group(group_state[i])                 #retrive vaccination information data for the entire state
    z = z[z.columns[5:]]                              #consider data only for dates
    z.dropna(inplace=True)
    z = z.astype(int)                                 #covert the dataframe to numeric type
    x = z.sum(axis = 0, skipna = True)                #sum up counts for all districts in that state
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
    
    z1  = z.iloc[: , -10:]
    doses = z1.iloc[:,[8,9]]
    doses = doses.values.tolist()[0]
    doses = [0 if x != x else x for x in doses]
    covaxin = covaxin+int(doses[0])
    covishield = covishield+int(doses[1])
    if covaxin>0:
        vaccination_ratio = covishield/covaxin
    else:
        vaccination_ratio = float("NAN")
    state_ratio[key] = [vaccination_ratio]    


# In[23]:


state_ratio


# In[24]:


items = list(state_ratio.items())
for i in range(len(items)):
    old_key = items[i][0]
    state_id = df1.get_group(old_key).iloc[0]['State_Code'] 
    new_key = state_id+"_"+old_key
    state_ratio[new_key] = state_ratio.pop(old_key)   #replace state name with state codes


# In[25]:


state_ratio


# In[ ]:





# In[ ]:





# In[26]:


field_names = ['stateid','vaccineratio']


# In[27]:


a_file = open("state_vaccine-type-ratio.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = field_names)
writer.writeheader()
writer = csv.writer(a_file)
for key, values in state_ratio.items():
    writer.writerow([key]+values)

a_file.close()


# In[ ]:





# ### For the country find total number of covidhield and covaxin doses and their ratios

# In[28]:


new_data = vaccine_data.iloc[1:,5:]


# In[29]:


new_data


# In[30]:


new_data = new_data.astype(int,errors='ignore')


# In[31]:


new_data = new_data.iloc[: , -10:] #consider the dataset for last date
new_data


# In[32]:


new_data. dropna(inplace=True) 


# ### Calculate the sum of covaxin and covishield doses for entire country

# In[33]:


covaxin = new_data.iloc[:, 8].tolist()
covaxin = sum([int(i) for i in covaxin])
covaxin


# In[34]:


covishield = new_data.iloc[:, 9].tolist()
covishield = sum([int(i) for i in covishield])
covishield


# In[35]:


vaccineratio = covishield/covaxin
vaccineratio 


# In[36]:


country_ratio = dict()


# In[37]:


country_ratio['INDIA'] = vaccineratio


# In[38]:


field_names = ['country','vaccineratio']


# In[39]:


a_file = open("overall_vaccine-type-ratio.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = field_names)
writer.writeheader()
writer = csv.writer(a_file)
for key, values in country_ratio.items():
    writer.writerow([key]+[values])

a_file.close()


# In[40]:


print("Ended Execution")

