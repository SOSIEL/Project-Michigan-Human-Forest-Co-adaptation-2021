# Name: BHE_scenarios_alb 
# Description: ???
# Author: G. Sotnik

# Import relevant library.
import matplotlib.pyplot as plt
import pandas as pd

# --------------------
# PREPARE DATA & SPACE
# --------------------

# A list of unnecessary columns to remove from csv files to save memory.
rmv_cols = ['CohortsKilledInMA1', 'CohortsKilledInMA2', 'CohortsKilledInMA3',
            'CohortsKilledInMA4', 'CohortsKilledInMA5', 'CohortsKilledInMA6',
            'CohortsKilledInMA7', 'CohortsKilledInMA8', 'CohortsKilledInMA9',
            'DamagedSitesInMA1', 'DamagedSitesInMA2', 'DamagedSitesInMA3',
            'DamagedSitesInMA4', 'DamagedSitesInMA5', 'DamagedSitesInMA6',
            'DamagedSitesInMA7', 'DamagedSitesInMA8', 'DamagedSitesInMA9']

# Load data. Designate the first row as the header. Drop unnecessary columns.
BDA_curr = pd.read_csv('output_BDA_curr_mgmt_alb_sim1.csv', header = 0)
BDA_curr = BDA_curr.drop(columns = rmv_cols)

BDA_pcm = pd.read_csv('output_BDA_pcm_mgmt_alb_sim1.csv', header = 0)
BDA_pcm = BDA_pcm.drop(columns = rmv_cols)

BDA_gfdl = pd.read_csv('output_BDA_gfdl_mgmt_alb_sim1.csv', header = 0)
BDA_gfdl = BDA_gfdl.drop(columns = rmv_cols)

dfs = ['BDA_curr', 'BDA_pcm', 'BDA_gfdl']

# Lists with scenarios and times.
scenarios = ['curr', 'pcm', 'gfdl']

# Allocating space for BDA scenarios.
BDA_scenarios = pd.DataFrame()
for row in range(71):
    BDA_scenarios.loc[row, 'year'] = row + 1


# ------------
# PROCESS DATA
# ------------

for scenario in range(3):
    for row1 in range(71):
        for row2 in range(15):
            if int(BDA_scenarios.loc[row1, 'year']) == vars()['BDA_' + scenarios[scenario]].loc[row2, 'Time']:
                BDA_scenarios.loc[row1, scenarios[scenario]] = vars()['BDA_' + scenarios[scenario]].loc[row2, 'TotalBiomassKilled']
                break
            else:
                BDA_scenarios.loc[row1, scenarios[scenario]] = 0

        
        
        
        
        BDA_scenarios.loc[row, 'pcm'] = BDA_pcm.loc[row, 'TotalBiomassKilled']
        BDA_scenarios.loc[row, 'gfdl'] = BDA_gfdl.loc[row, 'TotalBiomassKilled']

# ------------
# PLOT RESULTS
# ------------

BDA_scenarios.plot.line(y = scenarios)
plt.xlabel('Year')
plt.ylabel('Biomass Killed')
plt.savefig('BDA_scenarios_mgmt_alb_sim1.png',dpi=300)

plt.show()

# ------------
# SAVE RESULTS
# ------------

# Save the dataframe BHE_Scenarios as a csv file.
BDA_scenarios.to_csv('analysis_BDA_scenarios_mgmt_alb_sim1.csv', index=False)
