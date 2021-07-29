# Name: spp-biomass_plots  
# Description: The Python code creates species-specific plots using the data in the
## files created by the spp-biomass code.  
# Author: G. Sotnik

# Import relevant libraries.
import pandas as pd
import matplotlib.pyplot as plt

# Load data. Designate the first row and column as indices.
spp_biomass_mgmt = pd.read_csv('spp_biomass_pcm_mgmt_sim1_acersacc.csv',
                               header = 0, index_col = 0)
spp_biomass_mgmt_alb = pd.read_csv('spp_biomass_pcm_mgmt_alb_sim1_acersacc.csv',
                                   header = 0, index_col = 0)

# Plot the loaded data.
ax = plt.gca()

spp_biomass_mgmt.plot(kind='line', y = 8, ax = ax)
spp_biomass_mgmt_alb.plot(kind='line', y = 8, color = 'red', ax = ax)

plt.show()