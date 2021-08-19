#!/usr/bin/env python
# coding: utf-8

# **SPDX-License-Identifier:** LGPL-3.0-or-later  
# **Copyright** (C) 2021 SOSIEL Inc. All rights reserved.  
# 
# **Name:** ALB Phenology  
# **Description:** A Python adaptation of Talbot Trotter's MATLAB ALB (Asian Longhorned Beetle) Phenology algorithm from Trotter and Keena (2016).
# The adapted version includes the following five differences from the original code:
# 1. The ability to choose among input options is removed and in each case the default is used.
# 2. Variable names that consist of two or more words or acronyms now include hyphens that seperate them.
# 3. It is streamlined where possible.
# 4. Output has changed completely.
# 
# **Rewritten in Python by:** Garry Sotnik

# In[ ]:


import math
import numpy.matlib
import numpy as np
import pandas as pd
from ALB_Phenology_functions.ipynb import smooth_temp_data, hdd_Allen


# In[ ]:


# Load data.
ALB_HDDreq = pd.read_csv('ALB_HDDreq_recalculated.csv', header = None)

ALB_HDDreq_sd = pd.read_csv('ALB_HDDreq_sd.csv', header = None)

ALB_LCT = pd.read_csv('ALB_LCT_recalculated.csv', header = None)

ALB_UCT = pd.read_csv('ALB_UCT_recalculated.csv', header = None)


# In[ ]:


# Variables to determine timing of oviposition.
mean_time_to_oviposition = 16 # Based on Keena (2006).
sd_time_to_oviposition = 0


# In[ ]:


# The number of beetles and years to run in simulation.
annual_cycles_included = 400
number_of_beetles_used = 400


# In[ ]:


ALB_larvae_to_pupae_rate = pd.read_csv('ALB_Molt_Ratios_From_ALB_Parameters_Recalculated.csv', header=None)


# In[ ]:


# Set mean and sd of egg start date.
mean_egg_start_date = 230
sd_egg_start_date = 0
    
egg_start_dates = mean_egg_start_date + sd_egg_start_date * np.random.normal(loc=number_of_beetles_used, scale=1)


# In[ ]:


# Set the Julian Date on which the adult ALB will be removed from the system
# annualy. Note that this value is not used in the simulation, but is used to
# produce a graph of the "Flight Seasons" using the function ALBFlightSeasons.
julian_date = 345


# In[ ]:


stages = (['eggs', 'larvae_1', 'larvae_2', 'larvae_3', 'larvae_4', 'larvae_5',
           'larvae_6', 'larvae_7', 'larvae_8', 'larvae_9', 'larvae_10', 'larvae_11',
           'pupae', 'scleritizing_adults', 'emerging_adults', 'egg_laying_adults'])

scenarios = ["curr", "pcm", "gfdl"]
ecoregions = [str(i) for i in range(1,10)]


# In[ ]:


# If the pupal temperature gate is being used, set up the temperature gate
# matrix. NOTE: THIS AND THE CODE FOR THE PUPAE ASSUME THAT THE
# TEMPERATURE CURVES ARE SMOOTH, I.E. MONOTONICALLY DECREASING AFTER SUMMER MAX.
temp_gate_matrix = np.zeros((365,1))


# In[ ]:


# Pre-allocate matrices for beetles in each stage.
for stage in range(16):
    vars()[stages[stage]] = np.empty((annual_cycles_included,number_of_beetles_used))
    vars()[stages[stage]][:] = np.NaN
    
# Pre-allocate the matrices for daily HDD (Heating degree-days) values.
for stage in range(15):
    vars()[stages[stage] + '_hdd'] = np.zeros((1,365))
    base10_hdd = np.zeros((1,365))
    
# Pre-allocate the marix for output.
egg_laying_adults_diffs = np.empty((annual_cycles_included,number_of_beetles_used))


# Process temperature data

# In[ ]:


# Load local temperature data.
max_temp = pd.read_csv('NewYorkNYmaxt.csv', header = None)
min_temp = pd.read_csv('NewYorkNYmint.csv', header = None)

# If necessary, convert tempearute variables from Fahrenheit to Celsius.
min_temp = (min_temp - 32) * (5/9)
max_temp = (max_temp - 32) * (5/9)

# Call function to smooth temperature data.
smooth_temp_data(max_temp, min_temp)

for day in range(1,365):
    if min_temp.iloc[day][0] >= min_temp.iloc[day-1][0]:
        temp_gate_matrix[day][0] = 1

# If the pupal gate is being used, identify the first day of the summer
# on which temperatures begin to decrease.
last_warming_day = [];
for day in range(60,365):
    if temp_gate_matrix[day][0] == 0:
        last_warming_day = day-1
        break

# Add a set number of days onto the temperature gate, which effectively
# moves the day on which beetles are allowed to move to pupation later into
# the summer if the pupal gate is being used.
added_warming_days = 14
new_last_warming_day = last_warming_day + added_warming_days

temp_gate_matrix[(last_warming_day - 1):new_last_warming_day,0] = 1

temp_gate_matrix = np.matlib.repmat(temp_gate_matrix,1,annual_cycles_included)

min_temp_1 = min_temp
for i in range(364):
    min_temp_1.loc[i] = min_temp.loc[i+1]


# Calculate HDD for each stage

# In[ ]:


for day in range(364):
    for stage in range(15):
        vars()[stages[stage] + '_hdd'][0][day] = hdd_Allen(day,max_temp[0][day],min_temp[0][day],min_temp_1[0][day],ALB_LCT[0][stage],ALB_UCT[0][stage])
    base10_hdd[0][day] = hdd_Allen(day,max_temp[0][day],min_temp[0][day],min_temp_1[0][day],10,100)

for day in range(364,365):
    for stage in range(15):
        vars()[stages[stage] + '_hdd'][0][day] = hdd_Allen(day,max_temp[0][day],min_temp[0][day],min_temp_1[0][0],ALB_LCT[0][stage],ALB_UCT[0][stage])
    base10_hdd[0][day] = hdd_Allen(day,max_temp[0][day],min_temp[0][day],min_temp_1[0][0],10,100)

# Repeat the daily values so that the temperature record covers the
# period included in the simulation.
for stage in range(15):
    vars()[stages[stage] + '_hdd'] = np.matlib.repmat(vars()[stages[stage] + '_hdd'],1,annual_cycles_included)


# Determine the day each beetle comletes each stage.

# In[ ]:


for years in range(annual_cycles_included):
    if years == 0:
        # Stage 1 (Eggs).
        for i in range(number_of_beetles_used):
            randomized_hdd_req = ALB_HDDreq[0][0] + (ALB_HDDreq_sd[0][0] * np.random.normal(loc=0.0, scale=1.0, size=None))
            t1 = round(egg_start_dates)
            # This sets the window of days for the calculation of HDD to the
            # window bracketed by the day the egg was laid, and the "current day".
            for t2 in range(t1,(annual_cycles_included*365 + 1)):
                # If the current accumulation of HDD exceeds the required HDD
                # then the day on which the requirement was exceeded is documented.
                if sum(eggs_hdd[0][t1:t2]) >= randomized_hdd_req:
                    # % Documents the day on which the egg completed development (hatched)
                    eggs[0][i] = t2
                    break
    else:
        # Stage 1 (Eggs).
        for i in range(number_of_beetles_used):
            randomized_hdd_req = ALB_HDDreq[0][0] + (ALB_HDDreq_sd[0][0] * np.random.normal(loc=0.0, scale=1.0, size=None))
            # If the previous stage was an nan (i.e., it was not completed) then the current stage will be an nan.
            if math.isnan(egg_laying_adults[years-1][i]):
                eggs[years][i] = 'nan'
            else:
                for t in range((round(egg_laying_adults[years - 1][i]) + 1),(annual_cycles_included * 365 + 1)):
                    if sum(eggs_hdd[0][round(egg_laying_adults[years - 1][i]):t]) >= randomized_hdd_req:
                        eggs[years][i] = t
                        break
    # Stages 2-15.
    for stage in range(1,15):
        for i in range(number_of_beetles_used):
            randomized_hdd_req = ALB_HDDreq[0][stage] + (ALB_HDDreq_sd[0][stage] * np.random.normal(loc=0.0, scale=1.0, size=None))
            # If the previous stage was an NaN (i.e., it was not completed) then the current stage will be an NaN.
            if math.isnan(vars()[stages[stage-1]][years][i]):
                vars()[stages[stage]][years][i] = 'nan'
            else:
                for t in range((round(vars()[stages[stage-1]][years][i]) + 1),(annual_cycles_included * 365 + 1)):
                    if sum(vars()[stages[stage] + '_hdd'][0][round(vars()[stages[stage-1]][years][i]):t]) >= randomized_hdd_req:
                        vars()[stages[stage]][years][i] = t
                        break

    # Stage 16 (Egg laying adults).
    for i in range(number_of_beetles_used):
        if math.isnan(emerging_adults[years][i]):
            egg_laying_adults[years][i] = 'nan'
        else:
            egg_laying_adults[years][i] = emerging_adults[years][i] + (mean_time_to_oviposition +
                                         (sd_time_to_oviposition * np.random.normal(loc=0.0, scale=1.0, size=None)))
            egg_laying_adults[years][i] = round(egg_laying_adults[years][i])


# Process data for output.

# In[ ]:


egg_laying_adults = egg_laying_adults[~numpy.isnan(egg_laying_adults)]
for column in range(0,number_of_beetles_used):
    for row in range(1,21):
        egg_laying_adults_diffs[row-1][column] = egg_laying_adults[row][column] - egg_laying_adults[row-1][column]
disturbance_frequency = np.round(sum(egg_laying_adults_diffs[0:50])/50)

