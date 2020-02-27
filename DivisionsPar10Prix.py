#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[18]:


data = pd.read_csv("data.csv")
price_step = 10 # 44 output values


# In[19]:


data["price"] = data["price"].apply(lambda x: x//price_step)


# In[22]:


data.to_csv("data.csv")

# In[ ]:




