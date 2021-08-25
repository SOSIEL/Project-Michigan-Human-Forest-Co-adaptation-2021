# Name: BO_species_percent_mgmt 
# Description: Python code plotting the change in the percentage of each of the 9 
## management areas that is made up by the 13 host species. 
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
BO_pcm_species_mgmt = pd.read_csv('output_BO_pcm_mgmt_alb_sim1.csv', header = 0)
BO_gfdl_species_mgmt = pd.read_csv('output_BO_gfdl_mgmt_alb_sim1.csv', header = 0)


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

scenarios = ['curr', 'pcm', 'gfdl']
times = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]

BO_sugar = pd.DataFrame()

# ------------
# PROCESS DATA
# ------------
    
# Sum biomass harvested by scenario and year in a dataframe called BHE_scenarios.
for scenario in range(3):
    for time in range(14):
        BO_sugar.loc[times[time], scenarios[scenario]] = vars()['BO_' + scenarios[scenario] +'_species_mgmt'].loc[
            vars()['BO_' + scenarios[scenario] + '_species_mgmt']['Time'] == times[time], 'AboveGroundBiomass_acersacc'].sum()

# ------------
# PLOT RESULTS
# ------------

BO_sugar.plot.line(y = scenarios)
plt.xlabel('Year')
plt.ylabel('Above ground biomass')
#plt.yticks(np.arange(0, 1.1, 0.1))
plt.legend(loc = 2)
plt.savefig('image_BO_curr_mgmt_alb_im1_percent.png',dpi=300)

# -------------
# PRINT RESULTS
# -------------

# Save the dataframe BO_species_percent_mgmt as a csv file.
#BO_curr_species_mgmt_percent.to_csv('analysis_BO_curr_species_mgmt_percent.csv', index=False)