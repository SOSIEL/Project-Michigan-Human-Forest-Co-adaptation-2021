#!/usr/bin/env python
# coding: utf-8

# **SPDX-License-Identifier:** LGPL-3.0-or-later  
# **Copyright** (C) 2021 SOSIEL Inc. All rights reserved.  
# 
# **Name:** Normalize ecoregion-specific results  
# **Description:** The Python code normalizes the ecoregion-specific ALB phenology results to use as ecoregion modifiers in BDA.  
# **Author:** Garry Sotnik

# Important libraries.

# In[1]:


import pandas as pd
import numpy as np


# Input data from csv files as dataframes. Identify the first row (index=0) as header.

# In[2]:


infest_freq_curr = pd.read_csv('infestation_frequency_curr.csv', header = 0)
ecoregions = pd.read_csv('ecoregions.csv', header = 0)


# Calculate the mean of the "years" column.

# In[3]:


infest_freq_curr_mean = np.round(infest_freq_curr['years'].mean(), 1)


# Create an empty list, called "normalized", to hold normalized data.

# In[4]:


normalized = []


# Generate normalized data.

# In[5]:


for eco in range(9):
    f = np.round(((infest_freq_curr.iloc[eco][2]/infest_freq_curr_mean)-1),2)
    normalized.append(f)


# Add the normalized data to the infest_freq_curr dataframe as a new column, called "normal".

# In[6]:


infest_freq_curr['normal'] = normalized


# Write the expanded infest_freq_curr dataframe to a new .csv file, called "infestation_frequency_curr_normal". Do not create an index column in the new file.

# In[7]:


infest_freq_curr.to_csv('infestation_frequency_curr_normal.csv', index=False)


# Drop duplicate ecoregions.

# In[8]:


ecoregions = ecoregions.drop_duplicates()


# Reset index.

# In[9]:


ecoregions = ecoregions.reset_index(drop=True)


# Create an empty list, called "modifier", to hold modified data.

# In[10]:


modifier = []


# Generate modified data.

# In[11]:


for row in range(90):
    for eco in range(9):
        if f'Eco{eco+1}' in ecoregions.loc[row][0]:
            modifier.append(infest_freq_curr.loc[eco]['normal'])


# Add the modified data to the ecoregions dataframe as a new column, called "modifier".

# In[12]:


ecoregions['modifier'] = modifier


# Write the expanded ecoregions dataframe to a new .csv file, called "ecoregions_modifiers". Do not create an index column in the new file.

# In[14]:


ecoregions.to_csv('ecoregions_modifiers.csv', index=False)


# In[ ]:




