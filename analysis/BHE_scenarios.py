# Name: BHE_scenarios 
# Description: ???
# Author: G. Sotnik

# Import relevant library.
import matplotlib.pyplot as plt
import pandas as pd

# --------------------
# PREPARE DATA & SPACE
# --------------------

# A list of unnecessary columns to remove from csv files to save memory.
rmv_cols = ['Prescription', 'Stand', 'EventID', 'StandAge', 'StandRank', 'NumberOfSites',
            'HarvestedSites', 'MgBioRemovedPerDamagedHa',
            'TotalCohortsPartialHarvest', 'TotalCohortsCompleteHarvest', 'CohortsHarvested_abiebals',
            'CohortsHarvested_acerrubr', 'CohortsHarvested_acersacc', 'CohortsHarvested_betualle',
            'CohortsHarvested_betupapy', 'CohortsHarvested_carycord', 'CohortsHarvested_caryovat',
            'CohortsHarvested_castdent', 'CohortsHarvested_fagugran', 'CohortsHarvested_fraxamer',
            'CohortsHarvested_fraxnigr', 'CohortsHarvested_fraxpenn', 'CohortsHarvested_piceglau',
            'CohortsHarvested_picemari', 'CohortsHarvested_pinubank', 'CohortsHarvested_pinuresi',
            'CohortsHarvested_pinustro', 'CohortsHarvested_pinusylv', 'CohortsHarvested_popubals',
            'CohortsHarvested_popugran', 'CohortsHarvested_poputrem', 'CohortsHarvested_prunsero',
            'CohortsHarvested_queralba', 'CohortsHarvested_quercocc', 'CohortsHarvested_querelli',
            'CohortsHarvested_querfalc', 'CohortsHarvested_quermacr', 'CohortsHarvested_querrubr',
            'CohortsHarvested_quervelu', 'CohortsHarvested_thujocci', 'CohortsHarvested_tiliamer',
            'CohortsHarvested_tsugcana', 'CohortsHarvested_ulmuamer']

# Lists with scenarios and times.
scenarios = ['curr', 'pcm', 'gfdl']
times = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]

# Allocating space for BHE scenarios.
BHE_scenarios = pd.DataFrame()

# Load data. Designate the first row as the header. Drop unnecessary columns.
BHE_curr_mgmt_sim1 = pd.read_csv('output_BHE_curr_mgmt_sim1.csv', header = 0)
BHE_curr_mgmt_sim1 = BHE_curr_mgmt_sim1.drop(columns = rmv_cols)

BHE_pcm_mgmt_sim1 = pd.read_csv('output_BHE_pcm_mgmt_sim1.csv', header = 0)
BHE_pcm_mgmt_sim1 = BHE_pcm_mgmt_sim1.drop(columns = rmv_cols)

BHE_gfdl_mgmt_sim1 = pd.read_csv('output_BHE_gfdl_mgmt_sim1.csv', header = 0)
BHE_gfdl_mgmt_sim1 = BHE_gfdl_mgmt_sim1.drop(columns = rmv_cols)

# ------------
# PROCESS DATA
# ------------

# Sum biomass harvested by scenario and year in a dataframe called BHE_scenarios.
for scenario in range(3):
    for time in range(14):
        BHE_scenarios.loc[times[time], scenarios[scenario]] = vars()['BHE_' + scenarios[scenario] +'_mgmt_sim1'].loc[
            vars()['BHE_' + scenarios[scenario] + '_mgmt_sim1']['Time'] == times[time], 'MgBiomassRemoved'].sum()

# ------------
# PLOT RESULTS
# ------------

BHE_scenarios.plot.line(y = scenarios)
plt.xlabel('Year')
plt.ylabel('Biomass Harvested (Tg)')
plt.savefig('BHE_scenarios.png',dpi=300)

plt.show()

# ------------
# SAVE RESULTS
# ------------

# Save the dataframe BHE_Scenarios as a csv file.
BHE_scenarios.to_csv('analysis_BHE_scenarios.csv', index=False)
