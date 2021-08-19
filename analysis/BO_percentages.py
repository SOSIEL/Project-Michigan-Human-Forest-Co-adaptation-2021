# Name: BO_species_percent_mgmt 
# Description: Python code calculating the percentage of each of the 9 management areas that is composed
## of each of the 27 specieas. 
# Author: G. Sotnik

# Import relevant library.
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# --------------------
# PREPARE DATA & SPACE
# --------------------

# Load data. Designate the first row as the header. Drop unnecessary columns.
BO_curr_species_mgmt = pd.read_csv('output_BO_curr_mgmt_alb_sim1.csv', header = 0)
#BO_species_mgmt = BO_species_mgmt.drop(BO_species_mgmt[BO_species_mgmt['Time'] != 0].index)

species = ['AboveGroundBiomass_abiebals', 'AboveGroundBiomass_acerrubr', 'AboveGroundBiomass_acersacc',
           'AboveGroundBiomass_betualle', 'AboveGroundBiomass_betupapy', 'AboveGroundBiomass_carycord',
           'AboveGroundBiomass_caryovat', 'AboveGroundBiomass_castdent', 'AboveGroundBiomass_fagugran',
           'AboveGroundBiomass_fraxamer', 'AboveGroundBiomass_fraxnigr', 'AboveGroundBiomass_fraxpenn',
           'AboveGroundBiomass_piceglau', 'AboveGroundBiomass_picemari', 'AboveGroundBiomass_pinubank',
           'AboveGroundBiomass_pinuresi', 'AboveGroundBiomass_pinustro', 'AboveGroundBiomass_pinusylv',
           'AboveGroundBiomass_popubals', 'AboveGroundBiomass_popugran', 'AboveGroundBiomass_poputrem',
           'AboveGroundBiomass_prunsero', 'AboveGroundBiomass_queralba', 'AboveGroundBiomass_quercocc',
           'AboveGroundBiomass_querelli', 'AboveGroundBiomass_querfalc', 'AboveGroundBiomass_quermacr',
           'AboveGroundBiomass_querrubr', 'AboveGroundBiomass_quervelu', 'AboveGroundBiomass_thujocci',
           'AboveGroundBiomass_tiliamer', 'AboveGroundBiomass_tsugcana', 'AboveGroundBiomass_ulmuamer']

hosts = ['AboveGroundBiomass_acerrubr', 'AboveGroundBiomass_acersacc', 'AboveGroundBiomass_betualle',
         'AboveGroundBiomass_betupapy', 'AboveGroundBiomass_fagugran', 'AboveGroundBiomass_fraxamer',
         'AboveGroundBiomass_fraxnigr', 'AboveGroundBiomass_fraxpenn', 'AboveGroundBiomass_popubals',
         'AboveGroundBiomass_popugran', 'AboveGroundBiomass_poputrem', 'AboveGroundBiomass_prunsero',
         'AboveGroundBiomass_ulmuamer']

non_hosts = ['AboveGroundBiomass_abiebals', 'AboveGroundBiomass_carycord', 'AboveGroundBiomass_caryovat',
             'AboveGroundBiomass_castdent', 'AboveGroundBiomass_piceglau', 'AboveGroundBiomass_picemari',
             'AboveGroundBiomass_pinubank', 'AboveGroundBiomass_pinuresi', 'AboveGroundBiomass_pinustro',
             'AboveGroundBiomass_pinusylv', 'AboveGroundBiomass_queralba', 'AboveGroundBiomass_quercocc',
             'AboveGroundBiomass_querelli', 'AboveGroundBiomass_querfalc', 'AboveGroundBiomass_quermacr',
             'AboveGroundBiomass_querrubr', 'AboveGroundBiomass_quervelu', 'AboveGroundBiomass_thujocci',
             'AboveGroundBiomass_tiliamer', 'AboveGroundBiomass_tsugcana']

BO_curr_species_mgmt_percent = BO_curr_species_mgmt
BO_curr_species_mgmt_percent_hosts = pd.DataFrame()
BO_curr_species_mgmt_percent_non_hosts = pd.DataFrame()

times = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
manage_areas = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# ------------
# PROCESS DATA
# ------------

# Create the last column that sums the total biomass for each row.
for area in range(135):
    BO_curr_species_mgmt.loc[area, 'MA_sum'] = BO_curr_species_mgmt.loc[area, species].sum()


# Calculate the percentage of each species in each management area.
for i in range(33):
    for area in range(135):
        BO_curr_species_mgmt_percent.loc[area, species[i]] = round(BO_curr_species_mgmt.loc[area, species[i]] /\
                                                                   BO_curr_species_mgmt.loc[area, 'MA_sum'], 2)

# Create the last column that sums the total percentage for each row.
for area in range(135):
    BO_curr_species_mgmt_percent.loc[area, 'MA_sum'] = BO_curr_species_mgmt_percent.loc[area, species].sum()
    
# Create the last column that sums the total percentage for the hosts in each row.
for area in range(135):
    BO_curr_species_mgmt_percent.loc[area, 'MA_sum_hosts'] = BO_curr_species_mgmt_percent.loc[area, hosts].sum()
    
# Create the last column that sums the total percentage for the non-hosts in each row.
for area in range(135):
    BO_curr_species_mgmt_percent.loc[area, 'MA_sum_non_hosts'] = BO_curr_species_mgmt_percent.loc[area, non_hosts].sum()

t = 0
for time in range(15):
    for manage_area in range(9):
        BO_curr_species_mgmt_percent_hosts.loc[times[time], manage_areas[manage_area]] = BO_curr_species_mgmt_percent.loc[ t, 'MA_sum_hosts']
        t = t + 1
        
t = 0
for time in range(15):
    for manage_area in range(9):
        BO_curr_species_mgmt_percent_non_hosts.loc[times[time], manage_areas[manage_area]] = BO_curr_species_mgmt_percent.loc[ t, 'MA_sum_non_hosts']
        t = t + 1

# ------------
# PLOT RESULTS
# ------------

BO_curr_species_mgmt_percent_hosts.plot.line(y = manage_areas)
plt.xlabel('Year')
plt.ylabel('Percent of management area')
plt.yticks(np.arange(0, 1.1, 0.1))
plt.legend(loc = 2)
plt.savefig('image_BO_curr_mgmt_alb_sim1_percent.png',dpi=300)

# -------------
# PRINT RESULTS
# -------------

# Save the dataframe BO_species_percent_mgmt as a csv file.
#BO_curr_species_mgmt_percent.to_csv('analysis_BO_curr_species_mgmt_percent.csv', index=False)