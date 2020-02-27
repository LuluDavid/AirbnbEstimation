#!/usr/bin/env python
# coding: utf-8

# In[110]:


import pandas as pd
import json
from sklearn.model_selection import train_test_split


# In[111]:


data = pd.read_csv("data.csv",header=0, index_col=0, squeeze=True)


# In[112]:


data["property_type"] = data["property_type"].astype("category")
data["room_type"] = data["room_type"].astype("category")


# In[113]:


# record associations values <-> category
d1 = dict(enumerate(data["property_type"].copy().cat.categories))
d2 = dict(enumerate(data["room_type"].copy().cat.categories))


# In[114]:


# outputing the associations
with open('associations.txt', 'w') as file:
     file.write("Property_type associatons : \n")
     file.write(json.dumps(d1))
     file.write("\n \n Room_type associatons : \n")
     file.write(json.dumps(d2))


# In[115]:


data["property_type_value"] = data["property_type"].cat.codes
data["room_type_value"] = data["property_type"].cat.codes


# In[116]:


data = data.loc[:,data.columns != 'property_type']
data = data.loc[:,data.columns != 'room_type']


# In[117]:


training_data, test_data = train_test_split(data, test_size=0.2)


# In[118]:


#outputing training and test data
training_data.to_csv("training_data.csv")
test_data.to_csv("test_data.csv")


# In[ ]:




