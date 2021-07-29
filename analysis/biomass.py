# Name: spp-biomass  
# Description: The Python script separates LANDIS-II's Biological Output extension's 
## output file (spp-biomass[...].csv, renamed here to [...]_biomass.csv) into
## species-specific files, in which data is aggregated among sub-ecoregions and
## saved into species-specific files.  
# Author: G. Sotnik

# Import relevant library.
import pandas as pd

# ------------
# Prepare data
# ------------

# Load data. Designate the first row as the header.
spp_biomass = pd.read_csv('spp-biomass_pcm_mgmt_alb_sim1.csv', header = 0)

# Remove all rows related to water.
spp_biomass = spp_biomass[~spp_biomass.EcoName.str.contains("water")]

# Remove unused columns.
spp_biomass.drop(labels = ['NumActiveSites', 'AboveGroundBiomass_carycord',
                           'AboveGroundBiomass_caryovat', 'AboveGroundBiomass_castdent',
                           'AboveGroundBiomass_quercocc', 'AboveGroundBiomass_querfalc',
                           'AboveGroundBiomass_quermacr'],
                 inplace = True,
                 axis = 1)

# Rename column names.
spp_biomass.columns = ['Time', 'EcoName', 'abiebals', 'acerrubr', 'acersacc',
                       'betualle', 'betupapy', 'fagugran', 'fraxamer', 'fraxnigr',
                       'fraxpenn', 'piceglau', 'picemari', 'pinubank', 'pinuresi',
                       'pinustro', 'pinusylv', 'popubals', 'popugran', 'poputrem',
                       'prunsero', 'queralba', 'querelli', 'querrubr', 'quervelu',
                       'thujocci', 'tiliamer', 'tsugcana', 'ulmuamer']

# Rename ecoregion names.
for ecoregion in range(1,10):
    spp_biomass.loc[spp_biomass['EcoName'].str.contains(
        f"Eco{ecoregion}"), 'EcoName'] = f"{ecoregion}"


# Convert all columns to numbers.
spp_biomass = spp_biomass.apply(pd.to_numeric)


# Create indices.
times = [*range(0,75,5)]
ecoregions = [*range(1,10)]

# ------------
# PROCESS DATA
# ------------

# Separate spp-biomass output file into species-specific files, in which data is aggregated
## among subecoregions and saved into species-specific files.
for species in range(2,29):
    vars()[spp_biomass.columns[species]] = pd.DataFrame(index = times, columns = ecoregions) 
    for time in range(0,75,5):
        for ecoregion in range(1,10):
            vars()[spp_biomass.columns[species]].loc[time][ecoregion] = round(spp_biomass.loc[
                (spp_biomass['Time'] == time) & (spp_biomass['EcoName'] == ecoregion),
                spp_biomass.columns[species]].sum(), 1)
    vars()[spp_biomass.columns[species]].to_csv(
        f'spp_biomass_pcm_mgmt_alb_sim1_{spp_biomass.columns[species]}.csv')