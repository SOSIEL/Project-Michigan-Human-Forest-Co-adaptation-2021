# Name: BO_Shannon_index 
# Description: Python code plotting the Shannon index for each of the 9 
## management areas.
# Author: G. Sotnik

# Import relevant library.
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# --------------------
# PREPARE DATA & SPACE
# --------------------

# Load data. Designate the first row as the header. Drop unnecessary columns.
BO_curr_species_mgmt = pd.read_csv('output_BO_pcm_mgmt_sim1.csv', header = 0)
#BO_species_mgmt = BO_species_mgmt.drop(BO_species_mgmt[BO_species_mgmt['Time'] != 0].index)

# The list of the 33 species, minus the 7 (carycord, caryovat, castdent, pinusylv, quercocc, querfalc,
## quermacr) with zero percentages.
species = ['AboveGroundBiomass_abiebals', 'AboveGroundBiomass_acerrubr', 'AboveGroundBiomass_acersacc',
           'AboveGroundBiomass_betualle', 'AboveGroundBiomass_betupapy', 'AboveGroundBiomass_fagugran',
           'AboveGroundBiomass_fraxamer', 'AboveGroundBiomass_fraxnigr', 'AboveGroundBiomass_fraxpenn',
           'AboveGroundBiomass_piceglau', 'AboveGroundBiomass_picemari', 'AboveGroundBiomass_pinubank',
           'AboveGroundBiomass_pinuresi', 'AboveGroundBiomass_pinustro', 'AboveGroundBiomass_popubals',
           'AboveGroundBiomass_popugran', 'AboveGroundBiomass_poputrem', 'AboveGroundBiomass_prunsero',
           'AboveGroundBiomass_queralba', 'AboveGroundBiomass_querelli', 'AboveGroundBiomass_querrubr',
           'AboveGroundBiomass_quervelu', 'AboveGroundBiomass_thujocci', 'AboveGroundBiomass_tiliamer',
           'AboveGroundBiomass_tsugcana', 'AboveGroundBiomass_ulmuamer']

BO_curr_species_mgmt_percent = BO_curr_species_mgmt
BO_curr_species_mgmt_percent_Shannon = pd.DataFrame()

times = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
manage_areas = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# ------------
# PROCESS DATA
# ------------

# Create the last column that sums the total biomass for each row.
for area in range(135):
    BO_curr_species_mgmt.loc[area, 'MA_sum'] = BO_curr_species_mgmt.loc[area, species].sum()


# Calculate the percentage of each species in each management area.
for i in range(26):
    for area in range(135):
        BO_curr_species_mgmt_percent.loc[area, species[i]] = BO_curr_species_mgmt.loc[area, species[i]] /\
                                                                   BO_curr_species_mgmt.loc[area, 'MA_sum']

# Create the last column that includes the Shannon index for each row.
for area in range(135):
    components = 0
    for i in range(26):
        component = 0
        portion = BO_curr_species_mgmt_percent.loc[area, species[i]]
        component = portion * np.log(portion)
        components = components + component
    BO_curr_species_mgmt_percent.loc[area, 'Shannon'] = - components

t = 0
for time in range(15):
    for manage_area in range(9):
        BO_curr_species_mgmt_percent_Shannon.loc[times[time], manage_areas[manage_area]] = BO_curr_species_mgmt_percent.loc[ t, 'Shannon']
        t = t + 1

# ------------
# PLOT RESULTS
# ------------

BO_curr_species_mgmt_percent_Shannon.plot.line(y = manage_areas)
plt.xlabel('Year')
plt.ylabel('Shannon index')
plt.yticks(np.arange(2.8, 3.1, 0.05))
plt.legend(loc = 2)
plt.savefig('image_BO_gfdl_mgmt_pcm_sim1_Shannon.png',dpi=300)