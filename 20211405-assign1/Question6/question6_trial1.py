#!/usr/bin/env python
# coding: utf-8

# In[1]:


print("Started Execution")


# In[2]:


import pandas as pd
import csv


# In[3]:


data = pd.read_csv("census_data.csv")


# In[4]:


data = data[["Level","Name","TRU","TOT_P","TOT_M","TOT_F"]]


# In[5]:


data


# In[6]:


df = data[data['Level'] == "DISTRICT"]


# In[7]:


df = df[df['TRU'] == "Total"]


# In[8]:


df['Name'] = df['Name'].str.lower()
census_dataset = df
census_dataset


# ### Find the names of districts available in census data

# In[9]:


census_districts = df["Name"].tolist()


# In[10]:


for i in range(len(census_districts)):
    census_districts[i] = census_districts[i].lower()


# In[11]:


punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''


# ### Remove punctuations from district names in census data

# In[12]:


census_districts_set = set(census_districts)


# In[13]:


list1 = list(census_districts_set)
for i in range(len(list1)):
    word = list1[i]
    for letter in word:
        if letter in punc:
            word = word.replace(letter,"")
            list1[i] = word
census_districts_set = set(list1)


# In[14]:


census_districts_set


# In[15]:


vaccine_data = pd.read_csv("cowin_vaccine_data_districtwise.csv",low_memory=False)


# In[16]:


index_no = vaccine_data.columns.get_loc('02/09/2021')  #from this date onward no vaccination data is available
index_no


# In[17]:


df1 = vaccine_data


# ### Consised the vaccination data for which vaccination value is available

# In[18]:


df1 = df1[df1.columns[1:index_no-1]]


# In[19]:


df1 =  df1.dropna(axis = 0, how ='any')
df1


# In[20]:


vaccine_districts = df1["District"].tolist()


# In[21]:


for i in range(len(vaccine_districts)):
    vaccine_districts[i] = vaccine_districts[i].lower()


# In[22]:


vaccine_districts_set = set(vaccine_districts)
vaccine_districts_set


# In[23]:


vaccine_m_census = list(vaccine_districts_set-census_districts_set)
census_m_vaccine = list(census_districts_set-vaccine_districts_set)


# In[24]:


len(vaccine_m_census)


# In[25]:


len(census_m_vaccine)


# ### Find District names in vaccination which are similar to census(dist in vaccination whose name is part of dist in census)

# In[26]:


vaccine_similar_census_dict = {}


# In[27]:


count = 0
for i in range(len(vaccine_m_census)):
    dis_vaccination = vaccine_m_census[i]
    for j in range(len(census_m_vaccine)):
        dis_census = census_m_vaccine[j]
        if dis_vaccination in dis_census:
            vaccine_similar_census_dict[dis_vaccination] = dis_census
            count = count+1


# In[28]:


len(vaccine_similar_census_dict)


# ### Function to update census dataset distric names accoding to names in vaccination dataset

# In[29]:


def update_census_data(Dict1):
    l1 = list(vaccine_similar_census_dict.items())
    for i in range(len(l1)):
        item = l1[i]
        vaccine_name = item[0]
        census_name = item[1]
        df.loc[(df.Name == census_name),'Name']=vaccine_name #replace district names in census data according to vaccination data


# ### Update the census dataset district names

# In[30]:


update_census_data(vaccine_similar_census_dict)


# In[31]:


census_districts = df["Name"].tolist()
census_districts_set = set(census_districts)


# In[32]:


vaccine_m_census = list(vaccine_districts_set-census_districts_set)
census_m_vaccine = list(census_districts_set-vaccine_districts_set)


# In[33]:


len(vaccine_m_census)


# ### Find District names in census which are similar to vaccination(dist in census whose name is part of dist in vaccination)

# In[34]:


census_similar_vaccine_dict  = dict()


# In[35]:


count = 0
for i in range(len(census_m_vaccine)):
    dis_census = census_m_vaccine[i]
    for j in range(len(vaccine_m_census)):
        dis_vaccine = vaccine_m_census[j]
        if dis_census in dis_vaccine:
            census_similar_vaccine_dict[dis_census] = dis_vaccine
            count = count+1


# In[36]:


census_similar_vaccine_dict


# In[37]:


l1 = list(census_similar_vaccine_dict.items())


# In[38]:


l1


# ### Refine the above list for district names to update in census dataset

# In[39]:


l1 = [('jalor', 'jalore'),('dibang valley', 'upper dibang valley'),('kheri', 'lakhimpur kheri'),('warangal', 'warangal rural'),('y.s.r.', 'y.s.r. kadapa'),('chamarajanagar', 'chamarajanagara'),('garhwal', 'pauri garhwal'),('muktsar', 'sri muktsar sahib')]


# In[40]:


vaccine_similar_census_dict = dict()


# In[41]:


for i in range(len(l1)):
    item = l1[i]
    vaccine_similar_census_dict[item[1]] = item[0]
    


# In[42]:


vaccine_similar_census_dict


# ### Update the census dataset district names according to vaccination dataset

# In[43]:


update_census_data(vaccine_similar_census_dict)


# In[44]:


census_districts = df["Name"].tolist()
census_districts_set = set(census_districts)


# In[45]:


vaccine_m_census = list(vaccine_districts_set-census_districts_set)
census_m_vaccine = list(census_districts_set-vaccine_districts_set)


# In[46]:


len(vaccine_m_census)


# In[47]:


vaccine_m_census


# ### Find District names in vaccination which are similar to census(dist in vaccination, components whose name after splitiing at space is part of dist in census)

# In[48]:


vaccine_similar_census_dict = dict()


# In[49]:


count = 0
for i in range(len(vaccine_m_census)):
    dis_vaccine = vaccine_m_census[i]
    for j in range(len(census_m_vaccine)):
        dis_census = census_m_vaccine[j]
        dis_vaccine_words = dis_vaccine.split()
        dis_census_words = dis_census.split()
        if "state" in dis_vaccine_words:
            dis_vaccine_word.remove("state")
        if "district" in dis_vaccine_words:
            dis_vaccine_word.remove("district")
        if "state" in dis_census_words:
            dis_census_words.remove("state")
        if "district" in dis_census_words:
            dis_census_words.remove("district")
        for word in dis_vaccine_words:              #go through each word of district names from vaccination dataset
            if word in dis_census_words:             #if any word appears in census dataset district name words then there is a similarity
                if dis_vaccine in vaccine_similar_census_dict.keys():
                    values = vaccine_similar_census_dict[dis_vaccine]
                    if dis_census not in values:
                        vaccine_similar_census_dict[dis_vaccine].append(dis_census)
                else:
                    vaccine_similar_census_dict[dis_vaccine] = list()
                    vaccine_similar_census_dict[dis_vaccine].append(dis_census)
                    count = count+1


# In[50]:


vaccine_similar_census_dict


# ### Refine the above dictionary for district names in census to update

# In[51]:


l1 = {'janjgir champa': ['janjgir - champa'],
 's.p.s. nellore': ['sri potti sriramulu nellore'],
 'west singhbhum': ['pashchimi singhbhum',],
 'khandwa': ['khandwa (east nimar)'],
 'north and middle andaman': ['north  & middle andaman'],
 'bengaluru rural': ['bangalore rural'],
 'east champaran': ['purba champaran'],
 'dadra and nagar haveli': ['dadra & nagar haveli'],
 'purba bardhaman': ['purba champaran'],
 'kaimur': ['kaimur (bhabua)'],
 'lahaul and spiti': ['lahul & spiti'],
 'north 24 parganas': ['north twenty four parganas'],
 'east singhbhum': ['purbi singhbhum'],
 'khargone': ['khargone (west nimar)'],
 'west champaran': ['pashchim champaran'],
 's.a.s. nagar': ['sahibzada ajit singh nagar'],
 'south 24 parganas': ['south twenty four parganas']}


# In[52]:


l1 = list(l1.items()) #convert the similarity dict to list


# In[53]:


vaccine_similar_census_dict = dict()


# In[54]:


for i in range(len(l1)):  # go though the similarity list and create new similarity dict with vaccination distric name as key
    vaccine_name = l1[i][0] #....and census distric name as value for update duntion to work
    census_name = l1[i][1][0]
    vaccine_similar_census_dict[vaccine_name] = census_name


# In[55]:


vaccine_similar_census_dict


# ### Update the census dataset district names according to vaccination dataset

# In[56]:


update_census_data(vaccine_similar_census_dict)


# In[57]:


census_districts = df["Name"].tolist()
census_districts_set = set(census_districts)


# In[58]:


vaccine_m_census = list(vaccine_districts_set-census_districts_set)
census_m_vaccine = list(census_districts_set-vaccine_districts_set)


# In[59]:


len(vaccine_m_census)


# ### Find District names in census which are similar to vaccination(dist in census, components whose name after splitting at space is part of dist in vaccination)

# In[60]:


census_similar_vaccine_dict = dict()


# In[61]:


count = 0
for i in range(len(census_m_vaccine)):
    dis_census = census_m_vaccine[i]
    for j in range(len(vaccine_m_census)):
        dis_vaccine = vaccine_m_census[j]
        dis_vaccine_words = dis_vaccine.split()
        dis_census_words = dis_census.split()
        if "state" in dis_vaccine_words:
            dis_vaccine_word.remove("state")
        if "district" in dis_vaccine_words:
            dis_vaccine_word.remove("district")
        if "state" in dis_census_words:
            dis_census_words.remove("state")
        if "district" in dis_census_words:
            dis_census_words.remove("district")
        for word in dis_census_words:
            if word in dis_vaccine_words:
                if dis_census in census_similar_vaccine_dict.keys():
                    values = census_similar_vaccine_dict[dis_census]
                    if dis_vaccine not in values:
                        census_similar_vaccine_dict[dis_census].append(dis_vaccine)
                else:
                    census_similar_vaccine_dict[dis_census] = list()
                    census_similar_vaccine_dict[dis_census].append(dis_vaccine)
                    count = count+1


# In[62]:


census_similar_vaccine_dict


# In[63]:


vaccine_m_census = list(vaccine_districts_set-census_districts_set)


# In[64]:


len(vaccine_m_census)


# In[65]:


vaccine_data = pd.read_csv("cowin_vaccine_data_districtwise.csv",low_memory=False)


# In[66]:


index_no = vaccine_data.columns.get_loc('02/09/2021')
index_no


# In[67]:


df1 = vaccine_data
df1 = df1[df1.columns[1:index_no-1]]


# In[68]:


df1 =  df1.dropna(axis = 0, how ='any')
df1


# In[69]:


df1['District'] = df1['District'].str.lower()
df1['State'] = df1['State'].str.lower()
df1


# ### Remove district names from vaccination dataset which are not present in Census dataset

# In[70]:


df1 = df1[~df1['District'].isin(vaccine_m_census)]


# In[71]:


df1


# In[72]:


vaccine_districts = df1["District"].tolist()
vaccine_districts_set = set(vaccine_districts)


# In[73]:


vaccine_m_census = list(vaccine_districts_set-census_districts_set)
vaccine_m_census


# ### Remove from census dataset districts whose name not in vaccine dataset

# In[74]:


census_dataset = census_dataset[census_dataset['Name'].isin(vaccine_districts_set)]


# In[75]:


census_dataset


# In[76]:


df = df1


# ### Find the sub headers under the dates

# In[77]:


sub_header = df.iloc[0].tolist()


# In[78]:


sub_header = sub_header[5:]
sub_header


# In[79]:


sub_header = sub_header[:10]
sub_header


# In[80]:


df.dropna(inplace=True) #district 'shi yomi' does not have any record 


# In[81]:


df1 = df.groupby(['State','District'])
df1.first()


# In[82]:


group_dist = list(df1.groups.keys())
group_dist


# ### For each districts find total number of male and female vaccinated, their corrousponding distric population and the required ratios

# In[83]:


district_ratio = dict()


# In[84]:


for i in range(len(group_dist)):
    key = group_dist[i][1]
    if key=='shi yomi':
        print("HELLO")
        break
    z = df1.get_group(group_dist[i])           #retrieve the dataset under that district
    district_id = z['District_Key']
    column_length = len(z.columns)
    z1 = z.iloc[: , -9:]                       #retrive the vaccination information of last date
    date_id = z1.columns[0]
    doses = z1.iloc[:,[5,6]]                   #retrieve total number of male and female vaccinated
    doses = doses.values.tolist()[0]
    doses = [0 if x != x else x for x in doses]
    male = int(doses[0])                       #conver value to numeric type
    female = int(doses[1])
    vaccination_ratio = female/male            #calculate ratio of female to male vaccination count
    row = census_dataset[census_dataset["Name"] == key]     #retrive population information for that district from census dataset
    total_female = sum(row['TOT_F'].tolist())               #retrive total female population information for that district
    total_male = sum(row['TOT_M'].tolist())                 #retrive total male population information for that district
    if total_female>0 and total_male>0:
        census_ratio = total_female/total_male              #calculate census ratio
        ratio_fraction = vaccination_ratio/census_ratio     #calculate ratio fraction
        district_ratio[key] = [vaccination_ratio,census_ratio,ratio_fraction]


# In[85]:


district_ratio


# In[86]:


items = list(district_ratio.items())
for i in range(len(items)):
    old_key = items[i][0]
    dist_id = df.loc[df['District'] == old_key]['District_Key'].tolist()
    district_ratio[dist_id[0]] = district_ratio.pop(old_key)  #update distrci names with district id


# In[87]:


district_ratio


# In[88]:


field_names = ['districtid','vaccinationratio','populationratio','ratioofratios']


# In[89]:


a_file = open("district_vaccination-population-ratio.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = field_names)
writer.writeheader()
writer = csv.writer(a_file)
for key, values in district_ratio.items():
    writer.writerow([key]+values)

a_file.close()


# In[ ]:





# ### Repeat the above procedure for each state

# In[ ]:





# In[90]:


df1 = df.groupby(['State'])
df1.first()


# In[91]:


group_state = list(df1.groups.keys())
group_state


# In[92]:


vaccine_state = group_state


# In[93]:


for i in range(len(vaccine_state)):
    vaccine_state[i] = vaccine_state[i].lower()


# In[94]:


vaccine_state_set = set(vaccine_state)


# In[95]:


data = pd.read_csv("census_data.csv")


# In[96]:


data = data[["Level","Name","TRU","TOT_P","TOT_M","TOT_F"]]
data


# In[97]:


df = data[data['Level'] == "STATE"]


# In[98]:


df = df[df['TRU'] == "Total"]


# In[99]:


df['Name'] = df['Name'].str.lower()
census_dataset = df
census_dataset


# In[100]:


census_sates = df["Name"].tolist()
census_state_set = set(census_sates)


# In[101]:


census_state_set


# In[102]:


vaccine_state_set - census_state_set


# In[103]:


census_state_set


# ### Find the states name in vaccination dataset and its equivalent name in census dataset

# In[104]:


vaccine_similar_census_dict = {'andaman and nicobar islands':'andaman & nicobar islands','jammu and kashmir':'jammu & kashmir','delhi':'nct of delhi'}


# In[105]:


update_census_data(vaccine_similar_census_dict)


# In[106]:


census_sates = df["Name"].tolist()
census_state_set = set(census_sates)


# In[107]:


vaccine_state_set - census_state_set


# In[108]:


census_state_set - vaccine_state_set


# ### Merge the following districts in census dataset according to single distric in vaccination dataset

# In[109]:


row1 = census_dataset[census_dataset["Name"] == 'dadra & nagar haveli']
row2 = census_dataset[census_dataset["Name"] == 'daman & diu']


# In[110]:


#print(row1)
#print(row2)


# In[111]:


census_dataset = census_dataset[~census_dataset["Name"].isin(['dadra & nagar haveli', 'daman & diu'])]


# In[112]:


df.loc[len(census_dataset.index)] = ['STATE','dadra and nagar haveli and daman and diu','Total', 586956,344061,242895] 


# In[113]:


df


# In[114]:


census_sates = df["Name"].tolist()
census_state_set = set(census_sates)


# In[115]:


vaccine_m_census = vaccine_state_set - census_state_set


# In[116]:


census_dataset = df


# In[117]:


index_no = vaccine_data.columns.get_loc('02/09/2021')
index_no


# In[118]:


df1 = vaccine_data
df1 = df1[df1.columns[1:index_no-1]]


# In[119]:


df1 = vaccine_data
df1 = df1[df1.columns[1:index_no-1]]
vaccine_data = df1


# In[120]:


state_names = pd.DataFrame() # create a new data frame to compre state names with state codes


# In[121]:


df1['District'] = df1['District'].str.lower()
state_names['State_name_original'] = df1['State'].tolist()   # preserve the original state name in new data frame without converting to lowercase
df1['State'] = df1['State'].str.lower()
state_names['State'] = df1['State'].tolist()
state_names['State_Code'] = df1['State_Code'].tolist()    # Store the corrospondind state codes in new data frame


# In[122]:


df1 = df1[~df1['State'].isin(vaccine_m_census)]


# In[123]:


vaccine_state = df1["State"].tolist()
vaccine_state_set = set(vaccine_districts)


# In[124]:


vaccine_state_set - census_state_set


# In[125]:


df1 = df1.groupby(['State'])
df1.first()


# In[126]:


group_state = list(df1.groups.keys())
group_state


# ### For each states find total number of male and female vaccinated, their corrousponding distric population and the required ratios

# In[127]:


state_ratio = dict()


# In[128]:


for i in range(len(group_state)):
    key = group_state[i]
    z = df1.get_group(group_state[i])                #retrive vaccination information data for the entire state
    z = z[z.columns[5:]]                             #consider data only for dates
    z.dropna(inplace=True)                           
    z = z.astype(int)                                #covert the dataframe to numeric type
    x = z.sum(axis = 0, skipna = True)               #sum up counts for all districts in that state
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
    
    z1  = z.iloc[: , -9:]
    doses = z1.iloc[:,[5,6]]
    doses = doses.values.tolist()[0]
    doses = [0 if x != x else x for x in doses]
    male = int(doses[0])
    female = int(doses[1])

    vaccination_ratio = female/male
    row = census_dataset[census_dataset["Name"] == key]
    total_female = sum(row['TOT_F'].tolist())
    total_male = sum(row['TOT_M'].tolist())
    if total_female>0 and total_male>0:
        census_ratio = total_female/total_male
        ratio_fraction = vaccination_ratio/census_ratio
        state_ratio[key] = [vaccination_ratio,census_ratio,ratio_fraction]


# In[129]:


state_ratio


# In[130]:


items = list(state_ratio.items())
for i in range(len(items)):
    old_key = items[i][0]
    state_id = state_names.loc[state_names['State'] == old_key][['State_Code','State_name_original']].values.tolist()[0]
    state_code = state_id[0]
    state = state_id[1]
    new_key = state_code+"_"+state
    state_ratio[new_key] = state_ratio.pop(old_key)  #update state name with state key


# In[131]:


state_ratio


# In[132]:


field_names = ['stateid','vaccinationratio','populationratio','ratioofratios']


# In[133]:


a_file = open("state_vaccination-population-ratio.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = field_names)
writer.writeheader()
writer = csv.writer(a_file)
for key, values in state_ratio.items():
    writer.writerow([key]+values)

a_file.close()


# In[ ]:





# ### For entire country find total number of male and female vaccinated, their corrousponding distric population and the required ratios

# In[134]:


vaccine_data


# In[135]:


new_data = vaccine_data.iloc[1:,5:]


# In[136]:


new_data


# In[137]:


new_data = new_data.astype(int,errors='ignore')


# In[138]:


new_data = new_data.iloc[: , -9:]
new_data


# In[139]:


new_data. dropna(inplace=True) 


# In[140]:


len(new_data)


# ### Find the female and male vaccination count in last date for entire country

# In[141]:


male = new_data.iloc[:, 5].tolist()
male = sum([int(i) for i in male])
male


# In[142]:


female = new_data.iloc[:, 6].tolist()
female = sum([int(i) for i in female])
female


# In[143]:


vaccination_ratio = female/male
vaccination_ratio


# In[144]:


country_tally = data.iloc[0]
country_tally


# In[145]:


Total_female = country_tally[5]
Total_female


# In[146]:


Total_male = country_tally[4]
Total_male


# In[147]:


census_ratio = Total_female/Total_male
census_ratio


# In[148]:


fraction_ratio = vaccination_ratio/census_ratio
fraction_ratio


# In[149]:


country_ratio = {"INDIA":[vaccination_ratio,census_ratio,fraction_ratio]}


# In[150]:


country_ratio


# In[151]:


field_names = ['country','vaccinationratio','populationratio','ratioofratios']


# In[152]:


a_file = open("overall_vaccination-population-ratio.csv", "w",newline="")
writer = csv.DictWriter(a_file, fieldnames = field_names)
writer.writeheader()
writer = csv.writer(a_file)
for key, values in country_ratio.items():
    writer.writerow([key]+values)

a_file.close()


# In[153]:


print("Ended Execution")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




