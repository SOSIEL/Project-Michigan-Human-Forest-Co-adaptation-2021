# SPDX-License-Identifier: LGPL-3.0-or-later  
# Copyright (C) 2021 SOSIEL Inc. All rights reserved.  

import pandas as pd
import numpy as np

infest_freq_curr = pd.read_csv('infestation_frequency_curr.csv', header = 0)
ecoregions = pd.read_csv('ecoregions.csv', header = 0)

infest_freq_curr_mean = np.round(infest_freq_curr['years'].mean(), 1)

normalized = []

for eco in range(9):
    f = np.round(((infest_freq_curr.iloc[eco][2]/infest_freq_curr_mean)-1),2)
    normalized.append(f)
    
infest_freq_curr['normal'] = normalized

infest_freq_curr.to_csv('infestation_frequency_curr_normal.csv', index=False)

# Drop duplicate ecoregions.
ecoregions = ecoregions.drop_duplicates()

# Reset index.
ecoregions = ecoregions.reset_index(drop=True)

modifier = []

for row in range(90):
    for eco in range(9):
        if f'Eco{eco+1}' in ecoregions.loc[row][0]:
            modifier.append(infest_freq_curr.loc[eco]['normal'])

ecoregions['modifier'] = modifier

ecoregions.to_csv('ecoregions_modifiers.csv', index=False)