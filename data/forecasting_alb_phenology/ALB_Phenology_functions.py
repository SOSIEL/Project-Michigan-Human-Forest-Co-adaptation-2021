#!/usr/bin/env python
# coding: utf-8

# **SPDX-License-Identifier:** LGPL-3.0-or-later  
# **Copyright** (C) 2021 SOSIEL Inc. All rights reserved.  
# 
# **Name:** ALB_Phenology_functions  
# **Description:** A Python adaptation of Talbot Trotter's MATLAB ALB (Asian Longhorned Beetle) Phenology algorithm from Trotter and Keena (2016). This file includes the two functions that are used in the main socurce code file, called ALB Phenology.  
# **Rewritten in Python by:** Garry Sotnik

# Use the smooth_temp_data function to smooth the temperature data. The function does this by averaging 5 day temperature windows centered on the target date, and repeating this process 10 times.

# In[ ]:


def smooth_temp_data(max_temp, min_temp):
    for i in range(10):
        min_temp.iloc[0] = (
            min_temp.iloc[363] + min_temp.iloc[364] + min_temp.iloc[0] + min_temp.iloc[1] + min_temp.iloc[2])/5
        min_temp.iloc[1] = (
            min_temp.iloc[364] + min_temp.iloc[0] + min_temp.iloc[1] + min_temp.iloc[2] + min_temp.iloc[3])/5
        min_temp.iloc[363] = (
            min_temp.iloc[361] + min_temp.iloc[362] + min_temp.iloc[363] + min_temp.iloc[364] + min_temp.iloc[0])/5
        min_temp.iloc[364] = (
            min_temp.iloc[362] + min_temp.iloc[363] + min_temp.iloc[364] + min_temp.iloc[0] + min_temp.iloc[1])/5
        for day in range(2,363):
            min_temp.iloc[day] = (
                min_temp.iloc[day-2] + min_temp.iloc[day-1] + min_temp.iloc[day] + min_temp.iloc[
                    day+1] + min_temp.iloc[day+2])/5
        max_temp.iloc[0] = (
            max_temp.iloc[363] + max_temp.iloc[364] + max_temp.iloc[0] + max_temp.iloc[1] + max_temp.iloc[2])/5
        max_temp.iloc[1] = (
            max_temp.iloc[364] + max_temp.iloc[0] + max_temp.iloc[1] + max_temp.iloc[2] + max_temp.iloc[3])/5
        max_temp.iloc[363] = (
            max_temp.iloc[361] + max_temp.iloc[362] + max_temp.iloc[363] + max_temp.iloc[364] + max_temp.iloc[0])/5
        max_temp.iloc[364] = (
            max_temp.iloc[362] + max_temp.iloc[363] + max_temp.iloc[364] + max_temp.iloc[0] + max_temp.iloc[1])/5
        for day in range(2,363):
            max_temp.iloc[day] = (
                max_temp.iloc[day-2] + max_temp.iloc[day-1] + max_temp.iloc[day] + max_temp.iloc[
                    day+1] + max_temp.iloc[day+2])/5


# Use the hdd_Allen function to calculate heating and cooling degree days.

# In[ ]:


def hdd_Allen(day,max_temp,min_temp,min_temp_1,ALB_LCT,ALB_UCT):
    
    import cmath
    
    temp_ave_am = (max_temp + min_temp) / 2
    temp_ave_pm = (max_temp + min_temp_1) / 2

# Case 1 and 2, both minimum and maximum temperatures above or below
# upper or lower critical temperature thresholds, respectively.
    if min_temp_1 >= ALB_UCT: # If the lower temperature exceeds the upper critical temperature then there is no development
        return 0
    if max_temp <= ALB_LCT: # If the upper temperature exceeds the lower critical temperature then there is no development
        return 0
 
# Case 3, minimum and maximum temperatures both between upper and lower
# critical threshold temperatures.
    if(min_temp >= ALB_LCT and min_temp <= ALB_UCT and max_temp >= ALB_LCT and max_temp <= ALB_UCT):
        hdd_am = 0.5 * (temp_ave_am - ALB_LCT)
        hdd_pm = 0.5 * (temp_ave_pm - ALB_LCT)
        hdd = hdd_am + hdd_pm
        return hdd
 
# If the above conditions have not been met, then calculations may require the following variables.
    alpha_am = (max_temp - min_temp) / 2
    theta_am = cmath.asin((ALB_LCT - temp_ave_am) / alpha_am)
    alpha_pm = (max_temp - min_temp_1) / 2
    theta_pm = cmath.asin((ALB_LCT - temp_ave_pm) / alpha_pm)
 
# Case 4, minimum temperature is below minimum critical threshold
# temperature, but maximum temperature is above minimum critical threshold
# temperature, and below maximum critical threshold temperature.
    if(min_temp <= ALB_LCT and max_temp >= ALB_LCT and max_temp <= ALB_UCT):
        hdd_am = (1 / (2 * cmath.pi)) * ((temp_ave_am - ALB_LCT) *
                ((cmath.pi / 2) - theta_am) + (alpha_am * cmath.cos(theta_am)))
        hdd_pm = (1 / (2 * cmath.pi)) * ((temp_ave_pm - ALB_LCT) *
                ((cmath.pi / 2) - theta_pm) + (alpha_pm * cmath.cos(theta_pm)))
        hdd = hdd_am + hdd_pm
        return hdd

# If the above conditions have not been met, then calculations may require the following variables.
    theta_2_am = cmath.asin((ALB_UCT - temp_ave_am) / alpha_am)
    theta_2_pm = cmath.asin((ALB_UCT - temp_ave_pm) / alpha_pm)
 
# Case 5, minimum temperature is between the minimum and maximum critical
# temperature thresholds, but the maximum temperature is above the maximum
# critical temperature threshold.
    if(min_temp >= ALB_LCT and min_temp <= ALB_UCT and max_temp >= ALB_LCT):
        hdd_am = (1 / (2 * cmath.pi)) * ((temp_ave_am - ALB_LCT) *
                (theta_2_am + (cmath.pi / 2)) +
                (ALB_UCT - ALB_LCT) * 
                ((cmath.pi / 2) - theta_2_am) -
                (alpha_am * cmath.cos(theta_2_am)))
        hdd_pm = (1 / (2 * cmath.pi)) * ((temp_ave_pm - ALB_LCT) *
                (theta_2_pm + (cmath.pi / 2)) +
                (ALB_LCT - ALB_UCT) *
                ((cmath.pi / 2) - theta_2_pm) -
                (alpha_pm * cmath.cos(theta_2_pm)))
        hdd = hdd_am + hdd_pm
        return hdd
 
# Case 6, minimum temperature is below the minimum critical threshold
# temperature, and maximum temperature is above the maximum critical
# threshold temperature.
    if(min_temp <= ALB_LCT and max_temp >= ALB_UCT):
        hdd_am = (1 / (2 * cmath.pi)) * ((temp_ave_am - ALB_LCT) *
                (theta_2_am - theta_am) + alpha_am *
                (cmath.cos(theta_am) - cmath.cos(theta_2_am)) +
                (ALB_UCT - ALB_LCT) * ((cmath.pi / 2) - theta_2_am))
        hdd_pm = (1 / (2 * cmath.pi)) * ((temp_ave_pm - ALB_LCT) *
                (theta_2_pm - theta_pm) + alpha_pm *
                (cmath.cos(theta_pm) - cmath.cos(theta_2_pm)) +
                (ALB_UCT - ALB_LCT) * ((cmath.pi / 2) - theta_2_pm))
        hdd = hdd_am + hdd_pm
        return hdd

