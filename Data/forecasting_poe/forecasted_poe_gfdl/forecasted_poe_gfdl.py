# The algorithm generates 70 annual probability of establishment projections for 33 species
# in nine ecoregion locations each with 10 climate areas using projected annual temperature and the historic
# relationship between temperature and each species' probability of establishment. Note: The data and code are
# seperated into parts becuase otherwise the algorithm becomes too memory-intensive. 
# Data is from Duveneck 2014 and Ibanez 2020.
# Code is by Sotnik and was last updated on April 11th, 2020.

### INPUT ###########################################################################################

import pandas as pd
import csv
import random
from random import gauss
random.seed(12345)

# A list of lists, with each list representing a year (00_05) and each list element the projected July temperature
# in one of the nine ecoregions.
ProjJulyTemp_00_05 = [[ 20, 20, 20, 20, 20, 20, 20, 20, 20 ], [ 20, 20, 21, 20, 20, 20, 20, 20, 20 ],   # 2000-2001.
                      [ 19, 19, 20, 20, 20, 19, 19, 19, 19 ], [ 22, 22, 23, 21, 23, 21, 22, 21, 21 ],   # 2002-2003.
                      [ 19, 19, 20, 19, 19, 19, 19, 19, 19 ], [ 23, 22, 23, 22, 23, 22, 22, 23, 22 ]]   # 2004-2005.

# A list of lists, with each list representing a year (06_11) and each list element the projected July temperature
# in one of the nine ecoregions.
ProjJulyTemp_06_11 = [[ 21, 21, 22, 21, 21, 21, 21, 21, 20 ], [ 21, 21, 21, 21, 21, 21, 21, 21, 21 ],   # 2006-2007.
                      [ 18, 18, 19, 18, 19, 18, 18, 18, 19 ], [ 23, 23, 23, 23, 23, 23, 23, 23, 22 ],   # 2008-2009.
                      [ 19, 19, 19, 18, 19, 18, 18, 19, 19 ], [ 20, 20, 21, 20, 21, 20, 20, 20, 20 ]]   # 2010-2011.

# A list of lists, with each list representing a year (12_17) and each list element the projected July temperature
# in one of the nine ecoregions.
ProjJulyTemp_12_17 = [[ 21, 21, 22, 21, 22, 21, 21, 21, 21 ], [ 19, 18, 19, 18, 19, 18, 18, 18, 18 ],   # 2012-2013.
                      [ 20, 20, 20, 20, 20, 20, 19, 20, 20 ], [ 26, 26, 26, 26, 26, 26, 26, 26, 26 ],   # 2014-2015.
                      [ 23, 22, 23, 22, 23, 22, 22, 22, 21 ], [ 21, 21, 21, 20, 21, 20, 21, 21, 20 ]]   # 2016-2017.

# A list of lists, with each list representing a year (18_23) and each list element the projected July temperature
# in one of the nine ecoregions.
ProjJulyTemp_18_23 = [[ 20, 20, 20, 20, 20, 20, 19, 20, 19 ], [ 20, 20, 21, 19, 20, 20, 20, 20, 20 ],   # 2018-2019.
                      [ 21, 20, 21, 20, 20, 20, 20, 20, 20 ], [ 27, 27, 27, 27, 27, 27, 27, 27, 26 ],   # 2020-2021.
                      [ 23, 23, 23, 23, 23, 23, 23, 22, 23 ], [ 22, 22, 22, 22, 21, 22, 21, 22, 21 ]]   # 2022-2023.

# A list of lists, with each list representing a year (24_29) and each list element the projected July temperature
# in one of the nine ecoregions.
ProjJulyTemp_24_29 = [[ 24, 24, 25, 24, 24, 24, 24, 24, 23 ], [ 22, 22, 23, 22, 23, 22, 22, 22, 21 ],   # 2024-2025.
                      [ 22, 22, 23, 22, 23, 22, 22, 22, 21 ], [ 21, 20, 21, 20, 21, 20, 20, 20, 20 ],   # 2026-2027.
                      [ 25, 25, 26, 25, 26, 25, 26, 25, 25 ], [ 23, 23, 25, 23, 25, 23, 24, 23, 22 ]]   # 2028-2029.

# A list of lists, with each list representing a year (30_35) and each list element the projected July temperature
# in one of the nine ecoregions.
ProjJulyTemp_30_35 = [[ 25, 25, 26, 25, 26, 25, 26, 25, 24 ], [ 19, 19, 19, 19, 19, 18, 18, 19, 19 ],   # 2030-2031.
                      [ 24, 24, 24, 24, 24, 24, 24, 24, 23 ], [ 23, 23, 24, 23, 24, 23, 23, 23, 23 ],   # 2032-2033.
                      [ 23, 23, 23, 23, 23, 23, 23, 23, 22 ], [ 21, 21, 22, 21, 22, 21, 21, 21, 21 ]]   # 2034-2035.

# A list of lists, with each list representing a year (36_41) and each list element the projected July temperature
# in one of the nine ecoregions.                      
ProjJulyTemp_36_41 = [[ 26, 26, 26, 26, 26, 26, 26, 26, 26 ], [ 23, 23, 24, 22, 23, 22, 23, 22, 22 ],   # 2036-2037.
                      [ 21, 21, 22, 21, 21, 21, 21, 21, 21 ], [ 23, 22, 23, 22, 23, 22, 23, 22, 23 ],   # 2038-2039.
                      [ 21, 21, 21, 21, 21, 21, 21, 21, 21 ], [ 24, 24, 25, 24, 25, 24, 24, 24, 24 ]]   # 2040-2041.

# A list of lists, with each list representing a year (42_47) and each list element the projected July temperature
# in one of the nine ecoregions.
ProjJulyTemp_42_47 = [[ 20, 20, 20, 20, 20, 20, 20, 19, 19 ], [ 25, 25, 26, 24, 26, 25, 25, 25, 24 ],   # 2042-2043.
                      [ 21, 21, 22, 21, 22, 21, 21, 21, 21 ], [ 23, 23, 24, 23, 24, 23, 23, 23, 22 ],   # 2044-2045.
                      [ 27, 26, 26, 26, 26, 26, 26, 26, 26 ], [ 22, 22, 23, 22, 22, 22, 22, 22, 21 ]]   # 2046-2047.

# A list of lists, with each list representing a year (48_53) and each list element the projected July temperature
# in one of the nine ecoregions.                      
ProjJulyTemp_48_53 = [[ 29, 29, 29, 28, 29, 29, 29, 28, 28 ], [ 22, 22, 23, 22, 22, 22, 22, 22, 22 ],   # 2048-2049.
                      [ 26, 26, 27, 26, 27, 26, 26, 25, 25 ], [ 24, 24, 24, 24, 24, 24, 24, 24, 23 ],   # 2050-2051.
                      [ 22, 22, 24, 22, 23, 22, 22, 22, 21 ], [ 27, 27, 28, 26, 27, 27, 27, 27, 25 ]]   # 2052-2053.

# A list of lists, with each list representing a year (54_59) and each list element the projected July temperature
# in one of the nine ecoregions.
ProjJulyTemp_54_59 = [[ 25, 25, 25, 25, 25, 25, 25, 25, 24 ], [ 27, 27, 28, 27, 28, 27, 27, 26, 26 ],   # 2054-2055.
                      [ 27, 27, 28, 27, 28, 27, 28, 27, 26 ], [ 26, 26, 26, 26, 26, 26, 26, 26, 26 ],   # 2056-2057.
                      [ 28, 28, 28, 27, 28, 28, 28, 28, 28 ], [ 26, 26, 26, 26, 26, 26, 26, 26, 25 ]]   # 2058-2059.

# A list of lists, with each list representing a year (60_65) and each list element the projected July temperature
# in one of the nine ecoregions.                      
ProjJulyTemp_60_65 = [[ 25, 25, 25, 24, 25, 24, 25, 24, 24 ], [ 27, 27, 27, 26, 27, 27, 26, 26, 26 ],   # 2060-2061.
                      [ 29, 29, 29, 28, 29, 28, 29, 28, 28 ], [ 24, 25, 27, 25, 26, 25, 25, 24, 24 ],   # 2062-2063.
                      [ 29, 29, 29, 28, 28, 28, 29, 28, 28 ], [ 22, 21, 23, 21, 22, 21, 22, 21, 21 ]]   # 2064-2065.

# A list of lists, with each list representing a year (66_70) and each list element the projected July temperature
# in one of the nine ecoregions.
ProjJulyTemp_66_70 = [[ 25, 26, 26, 25, 26, 25, 26, 25, 25 ], [ 29, 28, 29, 28, 29, 28, 29, 28, 27 ],   # 2066-2067.
                      [ 27, 27, 28, 27, 27, 27, 27, 26, 26 ], [ 29, 29, 29, 28, 29, 28, 29, 28, 28 ],   # 2068-2069.
                      [ 29, 28, 29, 28, 29, 28, 29, 28, 27 ]]                                           # 2070.

# Converting the above lists of lists into data phrames.
ProjJulyTemp_00_05 = pd.DataFrame(ProjJulyTemp_00_05)
ProjJulyTemp_06_11 = pd.DataFrame(ProjJulyTemp_06_11)
ProjJulyTemp_12_17 = pd.DataFrame(ProjJulyTemp_12_17)
ProjJulyTemp_18_23 = pd.DataFrame(ProjJulyTemp_18_23)
ProjJulyTemp_24_29 = pd.DataFrame(ProjJulyTemp_24_29)
ProjJulyTemp_30_35 = pd.DataFrame(ProjJulyTemp_30_35)
ProjJulyTemp_36_41 = pd.DataFrame(ProjJulyTemp_36_41)
ProjJulyTemp_42_47 = pd.DataFrame(ProjJulyTemp_42_47)
ProjJulyTemp_48_53 = pd.DataFrame(ProjJulyTemp_48_53)
ProjJulyTemp_54_59 = pd.DataFrame(ProjJulyTemp_54_59)
ProjJulyTemp_60_65 = pd.DataFrame(ProjJulyTemp_60_65)
ProjJulyTemp_66_70 = pd.DataFrame(ProjJulyTemp_66_70)

# Arrays to store years dutring calculation. 
Years1 = pd.Series(range(0,6))
Years2 = pd.Series(range(0,5))

# A list of 33 species. Order of species aligns with order in original input file (In order
# to align with values of other parameters). Note: Not entirely in an alphabetical order to follow
# the order in Duveneck's file.
Species = [ 'abiebals', 'acerrubr', 'acersacc', 'betualle', 'betupapy', 'carycord', 'caryovat',
            'castdent', 'fagugran', 'fraxamer', 'fraxnigr', 'fraxpenn', 'piceglau', 'picemari',
            'pinubank', 'pinuresi', 'pinustro', 'pinusylv', 'popubals', 'popugran', 'poputrem',
            'prunsero', 'queralba', 'quercocc', 'querelli','querfalc', 'quermacr', 'querrubr',
            'quervelu', 'thujocci', 'tiliamer', 'tsugcana', 'ulmuamer' ]

# A list of 13 possible July temperature values (16-29).
JulyTemp = [ 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29 ]

# A list of lists of probability of establishment values, with the order of species (rows) corresponding
# to the order in the list of Speices, while the columns corresponding to the columns in the list of
# possible July temperatures.

ProbEstGauss = [ [ gauss( 0.01371,   0.1012), gauss( 0.01095,  0.08264), gauss(0.007376,  0.06373), # 1. abiebals (tsugcana).
                   gauss( 0.00645,   0.0618), gauss( 0.00609,   0.0659), gauss(0.005025,  0.05885),
                   gauss(0.004687,  0.05671), gauss(0.004682,  0.05248), gauss(0.005329,  0.05516),
                   gauss(0.006574,  0.06729), gauss(0.006949,  0.07304), gauss(0.006716,  0.07203),
                   gauss(0.005637,  0.06427), gauss(0.005442,  0.06253) ],        
                 [ gauss(  0.4841,   0.1045), gauss(  0.4414,   0.1067), gauss(  0.4005,   0.1076), # 2. acerrubr.
                   gauss(  0.3616,   0.1073), gauss(  0.3251,   0.1058), gauss(  0.2909,   0.1033),
                   gauss(  0.2591,  0.09982), gauss(  0.2299,  0.09561), gauss(  0.2031,  0.09079),
                   gauss(  0.1787,  0.08551), gauss(  0.1566,  0.07992), gauss(  0.1368,  0.07414),
                   gauss(   0.119,  0.06829), gauss(  0.1031,  0.06247) ],
                 [ gauss(  0.4167,  0.05293), gauss(  0.3726,  0.05331), gauss(  0.3311,  0.05298), # 3. acersacc.
                   gauss(  0.2923,  0.05202), gauss(  0.2564,   0.0505), gauss(  0.2235,   0.0485),
                   gauss(  0.1935,  0.04612), gauss(  0.1666,  0.04345), gauss(  0.1425,  0.04058),
                   gauss(  0.1212,  0.03759), gauss(  0.1024,  0.03454), gauss( 0.08606,  0.03152),
                   gauss( 0.07188,  0.02856), gauss( 0.05969,  0.02571) ],
                 [ gauss(  0.1558,   0.0635), gauss(  0.1183,  0.04851), gauss( 0.08849,  0.03826), # 4. betualle.
                   gauss(  0.0654,  0.03092), gauss( 0.04783,   0.0251), gauss( 0.03465,  0.02017),
                   gauss( 0.02488,  0.01595), gauss(  0.0177,   0.0124), gauss( 0.01248, 0.009466),
                   gauss(0.008718, 0.007111), gauss(0.006032, 0.005261), gauss(0.004133, 0.003836),
                   gauss(0.002804, 0.002759), gauss(0.001883, 0.001958) ],
                 [ gauss(  0.1241,   0.1217), gauss(  0.1022,   0.1039), gauss( 0.08342,  0.08815), # 5. betupapy.
                   gauss( 0.06754,   0.0742), gauss( 0.05424,  0.06201), gauss( 0.04321,  0.05145),
                   gauss( 0.03417,  0.04238), gauss( 0.02681,  0.03465), gauss( 0.02089,  0.02814),
                   gauss( 0.01615,  0.02268), gauss(  0.0124,  0.01815), gauss(0.009459,  0.01443),
                   gauss(0.007165,  0.01138), gauss(0.005391, 0.008916) ],
                 [ gauss(   0.974,  0.05154), gauss(  0.9708,  0.05723), gauss(  0.9676,  0.06305), # 6. carycord (CARYasp).
                   gauss(  0.9643,  0.06898), gauss(  0.9608,  0.07499), gauss(  0.9572,  0.08106),
                   gauss(  0.9535,  0.08716), gauss(  0.9498,  0.09328), gauss(  0.9459,  0.09939),
                   gauss(   0.942,   0.1055), gauss(   0.938,   0.1115), gauss(   0.934,   0.1175),
                   gauss(  0.9299,   0.1234), gauss(  0.9257,   0.1292) ],
                 [ gauss(   0.974,  0.05154), gauss(  0.9708,  0.05723), gauss(  0.9676,  0.06305), # 7. caryovat (CARYAsp).
                   gauss(  0.9643,  0.06898), gauss(  0.9608,  0.07499), gauss(  0.9572,  0.08106),
                   gauss(  0.9535,  0.08716), gauss(  0.9498,  0.09328), gauss(  0.9459,  0.09939),
                   gauss(   0.942,   0.1055), gauss(   0.938,   0.1115), gauss(   0.934,   0.1175),
                   gauss(  0.9299,   0.1234), gauss(  0.9257,   0.1292) ],
                 [ gauss(  0.5188,   0.1025), gauss(  0.4777,   0.1063), gauss(  0.4381,    0.109), # 8. castdent (querrubr).
                   gauss(     0.4,   0.1107), gauss(  0.3637,   0.1113), gauss(  0.3294,   0.1109),
                   gauss(  0.2972,   0.1097), gauss(  0.2672,   0.1076), gauss(  0.2393,   0.1048),
                   gauss(  0.2136,   0.1014), gauss(    0.19,  0.09751), gauss(  0.1685,  0.09321),
                   gauss(   0.149,  0.08862), gauss(  0.1313,  0.08383) ],                 
                 [ gauss(  0.6533,   0.1699), gauss(  0.6209,   0.1822), gauss(  0.5889,   0.1937), # 9. fagugran.
                   gauss(  0.5577,   0.2041), gauss(  0.5273,   0.2135), gauss(   0.498,   0.2219),
                   gauss(  0.4697,   0.2291), gauss(  0.4427,   0.2353), gauss(   0.417,   0.2405),
                   gauss(  0.3925,   0.2446), gauss(  0.3694,   0.2478), gauss(  0.3477,   0.2501),
                   gauss(  0.3272,   0.2516), gauss(   0.308,   0.2524) ],
                 [ gauss(  0.9764,  0.03404), gauss(  0.9734,  0.03808), gauss(  0.9704,  0.04229), # 10. fraxamer.
                   gauss(  0.9672,  0.04665), gauss(  0.9638,  0.05115), gauss(  0.9603,  0.05578),
                   gauss(  0.9567,  0.06052), gauss(   0.953,  0.06536), gauss(  0.9492,   0.0703),
                   gauss(  0.9452,  0.07531), gauss(  0.9412,  0.08039), gauss(   0.937,  0.08552),
                   gauss(  0.9327,  0.09069), gauss(  0.9284,  0.09589) ],
                 [ gauss(  0.4991,   0.3822), gauss(  0.4802,	0.3781), gauss(  0.4613,   0.3743), # 11. fraxnigr (FRAXINUSsp).
                   gauss(  0.4445,   0.3707), gauss(  0.4294,   0.3671), gauss(  0.4162,   0.3641),
                   gauss(   0.404,   0.3625), gauss(  0.3914,   0.3608), gauss(  0.3781,   0.3586),
                   gauss(  0.3647,   0.3554), gauss(  0.3511,   0.3515), gauss(  0.3373,   0.3464),
                   gauss(  0.3237,   0.3407), gauss(  0.3105,	0.3351) ],
                 [ gauss(  0.4991,   0.3822), gauss(  0.4802,	0.3781), gauss(  0.4613,   0.3743), # 12. fraxpenn (FRAXINUSsp).
                   gauss(  0.4445,   0.3707), gauss(  0.4294,   0.3671), gauss(  0.4162,   0.3641),
                   gauss(   0.404,   0.3625), gauss(  0.3914,   0.3608), gauss(  0.3781,   0.3586),
                   gauss(  0.3647,   0.3554), gauss(  0.3511,   0.3515), gauss(  0.3373,   0.3464),
                   gauss(  0.3237,   0.3407), gauss(  0.3105,	0.3351) ],
                 [ gauss(  0.3218,  0.07202), gauss(  0.2791,  0.06999), gauss(  0.2401,  0.06706), # 13. piceglau (PICEAsp).
                   gauss(   0.205,  0.06339), gauss(  0.1737,  0.05916), gauss(  0.1461,  0.05453),
                   gauss(   0.122,  0.04968), gauss(  0.1011,  0.04476), gauss( 0.08326,   0.0399),
                   gauss( 0.06808,  0.03521), gauss(  0.0553,  0.03077), gauss( 0.04463,  0.02663),
                   gauss( 0.03579,  0.02285), gauss( 0.02851,  0.01943) ],
                 [ gauss(  0.3218,  0.07202), gauss(  0.2791,  0.06999), gauss(  0.2401,  0.06706), # 14. picemari (PICEAsp).
                   gauss(   0.205,  0.06339), gauss(  0.1737,  0.05916), gauss(  0.1461,  0.05453),
                   gauss(   0.122,  0.04968), gauss(  0.1011,  0.04476), gauss( 0.08326,   0.0399),
                   gauss( 0.06808,  0.03521), gauss(  0.0553,  0.03077), gauss( 0.04463,  0.02663),
                   gauss( 0.03579,  0.02285), gauss( 0.02851,  0.01943) ],
                 [ gauss(  0.5642,  0.06676), gauss(  0.5244,  0.07091), gauss(  0.4852,  0.07467), # 15. pinubank (PINUSsp).
                   gauss(  0.4472,  0.07799), gauss(  0.4104,  0.08088), gauss(  0.3751,  0.08333),
                   gauss(  0.3415,  0.08537), gauss(  0.3097,    0.087), gauss(  0.2798,  0.08824),
                   gauss(  0.2519,  0.08914), gauss(  0.2259,  0.08971), gauss(  0.2019,  0.08998),
                   gauss(  0.1798,     0.09), gauss(  0.1597,  0.08978) ],
                 [ gauss(  0.5642,  0.06676), gauss(  0.5244,  0.07091), gauss(  0.4852,  0.07467), # 16. pinuresi (PINUSsp).
                   gauss(  0.4472,  0.07799), gauss(  0.4104,  0.08088), gauss(  0.3751,  0.08333),
                   gauss(  0.3415,  0.08537), gauss(  0.3097,    0.087), gauss(  0.2798,  0.08824),
                   gauss(  0.2519,  0.08914), gauss(  0.2259,  0.08971), gauss(  0.2019,  0.08998),
                   gauss(  0.1798,     0.09), gauss(  0.1597,  0.08978) ],
                 [ gauss(  0.5642,  0.06676), gauss(  0.5244,  0.07091), gauss(  0.4852,  0.07467), # 17. pinustro (PINUSsp).
                   gauss(  0.4472,  0.07799), gauss(  0.4104,  0.08088), gauss(  0.3751,  0.08333),
                   gauss(  0.3415,  0.08537), gauss(  0.3097,    0.087), gauss(  0.2798,  0.08824),
                   gauss(  0.2519,  0.08914), gauss(  0.2259,  0.08971), gauss(  0.2019,  0.08998),
                   gauss(  0.1798,     0.09), gauss(  0.1597,  0.08978) ],
                 [ gauss(  0.5642,  0.06676), gauss(  0.5244,  0.07091), gauss(  0.4852,  0.07467), # 18. pinusylv (PINUSsp).
                   gauss(  0.4472,  0.07799), gauss(  0.4104,  0.08088), gauss(  0.3751,  0.08333),
                   gauss(  0.3415,  0.08537), gauss(  0.3097,    0.087), gauss(  0.2798,  0.08824),
                   gauss(  0.2519,  0.08914), gauss(  0.2259,  0.08971), gauss(  0.2019,  0.08998),
                   gauss(  0.1798,     0.09), gauss(  0.1597,  0.08978) ],
                 [ gauss( 0.08235,  0.07297), gauss( 0.06367,  0.05804), gauss( 0.04862,   0.0456), # 19. popubals (POPULUSsp).
                   gauss( 0.03665,   0.0354), gauss( 0.02727,  0.02717), gauss( 0.02003,  0.02063),
                   gauss( 0.01451,  0.01552), gauss( 0.01038,  0.01157), gauss(0.007329, 0.008563),
                   gauss(0.005106, 0.006297), gauss(0.003511, 0.004607), gauss(0.002382, 0.003356),
                   gauss(0.001596, 0.002435), gauss(0.001056,  0.00176) ],
                 [ gauss( 0.08235,  0.07297), gauss( 0.06367,  0.05804), gauss( 0.04862,   0.0456), # 20. popugran (POPULUSsp).
                   gauss( 0.03665,   0.0354), gauss( 0.02727,  0.02717), gauss( 0.02003,  0.02063),
                   gauss( 0.01451,  0.01552), gauss( 0.01038,  0.01157), gauss(0.007329, 0.008563),
                   gauss(0.005106, 0.006297), gauss(0.003511, 0.004607), gauss(0.002382, 0.003356),
                   gauss(0.001596, 0.002435), gauss(0.001056,  0.00176) ],
                 [ gauss(  0.5642,  0.06676), gauss(  0.5244,  0.07091), gauss(  0.4852,  0.07467), # 21. poputrem (POPULUSsp).
                   gauss(  0.4472,  0.07799), gauss(  0.4104,  0.08088), gauss(  0.3751,  0.08333),
                   gauss(  0.3415,  0.08537), gauss(  0.3097,    0.087), gauss(  0.2798,  0.08824),
                   gauss(  0.2519,  0.08914), gauss(  0.2259,  0.08971), gauss(  0.2019,  0.08998),
                   gauss(  0.1798,     0.09), gauss(  0.1597,  0.08978) ],
                 [ gauss(  0.3844,   0.1422), gauss(  0.3438,   0.1363), gauss(  0.3058,     0.13), # 22. prunsero.
                   gauss(  0.2706,   0.1231), gauss(  0.2382,   0.1159), gauss(  0.2086,   0.1084),
                   gauss(  0.1819,   0.1008), gauss(  0.1578,  0.09309), gauss(  0.1364,  0.08544),
                   gauss(  0.1173,  0.07794), gauss(  0.1005,  0.07067), gauss( 0.08571,   0.0637),
                   gauss( 0.07282,  0.05709), gauss( 0.06164,  0.05088) ],
                 [ gauss(  0.6696,   0.1427), gauss(  0.6378,   0.1535), gauss(  0.6063,   0.1638), # 23. queralba.
                   gauss(  0.5752,   0.1734), gauss(  0.5446,   0.1823), gauss(  0.5148,   0.1905),
                   gauss(  0.4859,    0.198), gauss(   0.458,   0.2048), gauss(  0.4311,   0.2109),
                   gauss(  0.4054,   0.2164), gauss(  0.3809,   0.2214), gauss(  0.3576,   0.2257),
                   gauss(  0.3356,   0.2296), gauss(  0.3148,   0.2329) ],
                 [ gauss(  0.9847,  0.05004), gauss(  0.9828,  0.05593), gauss(  0.9809,  0.06198), # 24. quercocc (quervelu).
                   gauss(  0.9789,  0.06815), gauss(  0.9768,  0.07442), gauss(  0.9747,  0.08076),
                   gauss(  0.9726,  0.08715), gauss(  0.9704,  0.09356), gauss(  0.9683,  0.09996),
                   gauss(  0.9661,   0.1063), gauss(  0.9639,   0.1127), gauss(  0.9616,   0.1189),
                   gauss(  0.9594,   0.1251), gauss(  0.9573,   0.1312) ],
                 [ gauss(  0.6696,   0.1427), gauss(  0.6378,   0.1535), gauss(  0.6063,   0.1638), # 25. querelli (queralba).
                   gauss(  0.5752,   0.1734), gauss(  0.5446,   0.1823), gauss(  0.5148,   0.1905),
                   gauss(  0.4859,    0.198), gauss(   0.458,   0.2048), gauss(  0.4311,   0.2109),
                   gauss(  0.4054,   0.2164), gauss(  0.3809,   0.2214), gauss(  0.3576,   0.2257),
                   gauss(  0.3356,   0.2296), gauss(  0.3148,   0.2329) ],
                 [ gauss(  0.9847,  0.05004), gauss(  0.9828,  0.05593), gauss(  0.9809,  0.06198), # 26. querfalc (quervelu).
                   gauss(  0.9789,  0.06815), gauss(  0.9768,  0.07442), gauss(  0.9747,  0.08076),
                   gauss(  0.9726,  0.08715), gauss(  0.9704,  0.09356), gauss(  0.9683,  0.09996),
                   gauss(  0.9661,   0.1063), gauss(  0.9639,   0.1127), gauss(  0.9616,   0.1189),
                   gauss(  0.9594,   0.1251), gauss(  0.9573,   0.1312) ],
                 [ gauss(  0.9847,  0.05004), gauss(  0.9828,  0.05593), gauss(  0.9809,  0.06198), # 27. quermacr (quervelu).
                   gauss(  0.9789,  0.06815), gauss(  0.9768,  0.07442), gauss(  0.9747,  0.08076),
                   gauss(  0.9726,  0.08715), gauss(  0.9704,  0.09356), gauss(  0.9683,  0.09996),
                   gauss(  0.9661,   0.1063), gauss(  0.9639,   0.1127), gauss(  0.9616,   0.1189),
                   gauss(  0.9594,   0.1251), gauss(  0.9573,   0.1312) ],
                 [ gauss(  0.5188,   0.1025), gauss(  0.4777,   0.1063), gauss(  0.4381,    0.109), # 28. querrubr.
                   gauss(     0.4,   0.1107), gauss(  0.3637,   0.1113), gauss(  0.3294,   0.1109),
                   gauss(  0.2972,   0.1097), gauss(  0.2672,   0.1076), gauss(  0.2393,   0.1048),
                   gauss(  0.2136,   0.1014), gauss(    0.19,  0.09751), gauss(  0.1685,  0.09321),
                   gauss(   0.149,  0.08862), gauss(  0.1313,  0.08383) ],
                 [ gauss(  0.9847,  0.05004), gauss(  0.9828,  0.05593), gauss(  0.9809,  0.06198), # 29. quervelu.
                   gauss(  0.9789,  0.06815), gauss(  0.9768,  0.07442), gauss(  0.9747,  0.08076),
                   gauss(  0.9726,  0.08715), gauss(  0.9704,  0.09356), gauss(  0.9683,  0.09996),
                   gauss(  0.9661,   0.1063), gauss(  0.9639,   0.1127), gauss(  0.9616,   0.1189),
                   gauss(  0.9594,   0.1251), gauss(  0.9573,   0.1312) ],
                 [ gauss(  0.1526,   0.2397), gauss(   0.119,   0.1863), gauss( 0.09313,   0.1504), # 30. thujocci.
                   gauss(  0.0709,   0.1191), gauss( 0.05505,   0.0963), gauss( 0.04397,  0.08181),
                   gauss( 0.03974,  0.09356), gauss( 0.03242,  0.08802), gauss( 0.02787,  0.08965),
                   gauss( 0.02467,  0.09238), gauss( 0.02198,  0.09424), gauss( 0.01886,  0.08685),
                   gauss( 0.01465,  0.07164), gauss( 0.01081,  0.05094) ],
                 [  gauss(  0.4167,  0.05293), gauss(  0.3726,  0.05331), gauss(  0.3311,  0.05298), # 31. tiliamer (acersacc).
                   gauss(  0.2923,  0.05202), gauss(  0.2564,   0.0505), gauss(  0.2235,   0.0485),
                   gauss(  0.1935,  0.04612), gauss(  0.1666,  0.04345), gauss(  0.1425,  0.04058),
                   gauss(  0.1212,  0.03759), gauss(  0.1024,  0.03454), gauss( 0.08606,  0.03152),
                   gauss( 0.07188,  0.02856), gauss( 0.05969,  0.02571) ],
                 [ gauss( 0.01371,   0.1012), gauss( 0.01095,  0.08264), gauss(0.007376,  0.06373), # 32. tsugcana.
                   gauss( 0.00645,   0.0618), gauss( 0.00609,   0.0659), gauss(0.005025,  0.05885),
                   gauss(0.004687,  0.05671), gauss(0.004682,  0.05248), gauss(0.005329,  0.05516),
                   gauss(0.006574,  0.06729), gauss(0.006949,  0.07304), gauss(0.006716,  0.07203),
                   gauss(0.005637,  0.06427), gauss(0.005442,  0.06253) ],
                 [ gauss(  0.1469,  0.05086), gauss(  0.1131,  0.04045), gauss( 0.08576,   0.0322), # 33. ulmuamer.
                   gauss(  0.0641,  0.02574), gauss( 0.04727,  0.02066), gauss( 0.03441,  0.01657),
                   gauss( 0.02474,  0.01319), gauss( 0.01757,  0.01037), gauss( 0.01233, 0.008049),
                   gauss(0.008556,  0.00616), gauss(0.005868, 0.004653), gauss( 0.00398,  0.00347),
                   gauss( 0.00267, 0.002558), gauss(0.001772, 0.001864) ] ]

# A list of lists, with each of the 9 rows representing an ecoregion and each of
# the columns one of its 10 climate areas.
Ecoregions = [[ 1036, 1064, 1072, 1078, 1083, 1090, 1102, 1133, 1226, 1441 ],   # Ecoregion 1
              [ 2036, 2064, 2072, 2078, 2083, 2090, 2102, 2133, 2226, 2441 ],   # Ecoregion 2
              [ 3036, 3064, 3072, 3078, 3083, 3090, 3102, 3133, 3226, 3441 ],   # Ecoregion 3
              [ 4036, 4064, 4072, 4078, 4083, 4090, 4102, 4133, 4226, 4441 ],   # Ecoregion 4
              [ 5036, 5064, 5072, 5078, 5083, 5090, 5102, 5133, 5226, 5441 ],   # Ecoregion 5
              [ 6036, 6064, 6072, 6078, 6083, 6090, 6102, 6133, 6226, 6441 ],   # Ecoregion 6
              [ 7036, 7064, 7072, 7078, 7083, 7090, 7102, 7133, 7226, 7441 ],   # Ecoregion 7
              [ 8036, 8064, 8072, 8078, 8083, 8090, 8102, 8133, 8226, 8441 ],   # Ecoregion 8
              [ 9036, 9064, 9072, 9078, 9083, 9090, 9102, 9133, 9226, 9441 ]]   # Ecoregion 9

# Nine lists of undefined lenght for storing year-range-specific results.
ProjProbEst_00_05 = []
ProjProbEst_06_11 = []
ProjProbEst_12_17 = []
ProjProbEst_18_23 = []
ProjProbEst_24_29 = []
ProjProbEst_30_35 = []
ProjProbEst_36_41 = []
ProjProbEst_42_47 = []
ProjProbEst_48_53 = []
ProjProbEst_54_59 = []
ProjProbEst_60_65 = []
ProjProbEst_66_70 = []

### FORMATTING ProbEstGauss ####################################################################################################

format_function = lambda x: round( min(1, max(0, x)), 5 )
ProbEst = [ list( map( format_function, i ) ) for i in ProbEstGauss ]

# Write randomized and formatted probability of establishment values into a csv file, called ProbEst.
with open('output_ProbEst_higher_em.csv', 'w') as f:
    wr = csv.writer(f, lineterminator = '\n')
    for projprobest in ProbEst:
        wr.writerow([projprobest])

### CALCULATION 00-05 ##########################################################################################################

# The code generates annual probability of establishment projections for a set of species, for a set of
# climate regions, and for 6 years, using projected temperature and the historic relationship between
# temperature and each species' probability of establishment.
for year in Years1:
    a = year
    for areas in Ecoregions:
        b = Ecoregions.index(areas)
        for area in areas:
            for species in Species:
                c = Species.index(species)
                for temp in JulyTemp:
                    d = JulyTemp.index(temp)
                    e = int(round(ProjJulyTemp_00_05.at[a,b]))
                    if (e == JulyTemp[d]):
                        ProjProbEst_00_05.append(ProbEst[c][d])

### OUTPUT 00_05 #####################################################################################################################

# Write the annual probability of establishment projections into a csv file, called ProjProbEst.
                    with open('output_ProjProbEst_higher_em_00_05.csv', 'w') as f:
                        wr = csv.writer(f, lineterminator = '\n')
                        for projprobest in ProjProbEst_00_05:
                            wr.writerow([projprobest])

### CALCULATION 06_11 ################################################################################################################

# The code generates annual probability of establishment projections for a set of species, for a set of
# climate regions, and for 6 years, using projected temperature and the historic relationship between
# temperature and each species' probability of establishment.
for year in Years1:
    a = year
    for areas in Ecoregions:
        b = Ecoregions.index(areas)
        for area in areas:
            for species in Species:
                c = Species.index(species)
                for temp in JulyTemp:
                    d = JulyTemp.index(temp)
                    e = int(round(ProjJulyTemp_06_11.at[a,b]))
                    if (e == JulyTemp[d]):
                        ProjProbEst_06_11.append(ProbEst[c][d])

### OUTPUT 06_11 #####################################################################################################################

# The code writes the annual probability of establishment projections into a csv file, called ProjProbEst.
                    with open('output_ProjProbEst_higher_em_06_11.csv', 'w') as f:
                        wr = csv.writer(f, lineterminator = '\n')
                        for projprobest in ProjProbEst_06_11:
                            wr.writerow([projprobest])

### CALCULATION 12_17 ################################################################################################################

# The code generates annual probability of establishment projections for a set of species, for a set of
# climate regions, and for 6 years, using projected temperature and the historic relationship between
# temperature and each species' probability of establishment.
for year in Years1:
    a = year
    for areas in Ecoregions:
        b = Ecoregions.index(areas)
        for area in areas:
            for species in Species:
                c = Species.index(species)
                for temp in JulyTemp:
                    d = JulyTemp.index(temp)
                    e = int(round(ProjJulyTemp_12_17.at[a,b]))
                    if (e == JulyTemp[d]):
                        ProjProbEst_12_17.append(ProbEst[c][d])

### OUTPUT 12_17 #####################################################################################################################

# The code writes the annual probability of establishment projections into a csv file, called ProjProbEst.
                    with open('output_ProjProbEst_higher_em_12_17.csv', 'w') as f:
                        wr = csv.writer(f, lineterminator = '\n')
                        for projprobest in ProjProbEst_12_17:
                            wr.writerow([projprobest])

### CALCULATION 18_23 ################################################################################################################

# The code generates annual probability of establishment projections for a set of species, for a set of
# climate regions, and for 6 years, using projected temperature and the historic relationship between
# temperature and each species' probability of establishment.
for year in Years1:
    a = year
    for areas in Ecoregions:
        b = Ecoregions.index(areas)
        for area in areas:
            for species in Species:
                c = Species.index(species)
                for temp in JulyTemp:
                    d = JulyTemp.index(temp)
                    e = int(round(ProjJulyTemp_18_23.at[a,b]))
                    if (e == JulyTemp[d]):
                        ProjProbEst_18_23.append(ProbEst[c][d])

### OUTPUT 18_23 #####################################################################################################################

# The code writes the annual probability of establishment projections into a csv file, called ProjProbEst.
                    with open('output_ProjProbEst_higher_em_18_23.csv', 'w') as f:
                        wr = csv.writer(f, lineterminator = '\n')
                        for projprobest in ProjProbEst_18_23:
                            wr.writerow([projprobest])

### CALCULATION 24_29 ################################################################################################################

# The code generates annual probability of establishment projections for a set of species, for a set of
# climate regions, and for 6 years, using projected temperature and the historic relationship between
# temperature and each species' probability of establishment.
for year in Years1:
    a = year
    for areas in Ecoregions:
        b = Ecoregions.index(areas)
        for area in areas:
            for species in Species:
                c = Species.index(species)
                for temp in JulyTemp:
                    d = JulyTemp.index(temp)
                    e = int(round(ProjJulyTemp_24_29.at[a,b]))
                    if (e == JulyTemp[d]):
                        ProjProbEst_24_29.append(ProbEst[c][d])

### OUTPUT 24_29 #####################################################################################################################

# The code writes the annual probability of establishment projections into a csv file, called ProjProbEst.
                    with open('output_ProjProbEst_higher_em_24_29.csv', 'w') as f:
                        wr = csv.writer(f, lineterminator = '\n')
                        for projprobest in ProjProbEst_24_29:
                            wr.writerow([projprobest])
                            
### CALCULATION 30_35 ################################################################################################################

# The code generates annual probability of establishment projections for a set of species, for a set of
# climate regions, and for 6 years, using projected temperature and the historic relationship between
# temperature and each species' probability of establishment.
for year in Years1:
    a = year
    for areas in Ecoregions:
        b = Ecoregions.index(areas)
        for area in areas:
            for species in Species:
                c = Species.index(species)
                for temp in JulyTemp:
                    d = JulyTemp.index(temp)
                    e = int(round(ProjJulyTemp_30_35.at[a,b]))
                    if (e == JulyTemp[d]):
                        ProjProbEst_30_35.append(ProbEst[c][d])

### OUTPUT 30_35 #####################################################################################################################

# The code writes the annual probability of establishment projections into a csv file, called ProjProbEst.
                    with open('output_ProjProbEst_higher_em_30_35.csv', 'w') as f:
                        wr = csv.writer(f, lineterminator = '\n')
                        for projprobest in ProjProbEst_30_35:
                            wr.writerow([projprobest])

### CALCULATION 36_41 ################################################################################################################

# The code generates annual probability of establishment projections for a set of species, for a set of
# climate regions, and for 6 years, using projected temperature and the historic relationship between
# temperature and each species' probability of establishment.
for year in Years1:
    a = year
    for areas in Ecoregions:
        b = Ecoregions.index(areas)
        for area in areas:
            for species in Species:
                c = Species.index(species)
                for temp in JulyTemp:
                    d = JulyTemp.index(temp)
                    e = int(round(ProjJulyTemp_36_41.at[a,b]))
                    if (e == JulyTemp[d]):
                        ProjProbEst_36_41.append(ProbEst[c][d])

### OUTPUT 36_41 #####################################################################################################################

# The code writes the annual probability of establishment projections into a csv file, called ProjProbEst.
                    with open('output_ProjProbEst_higher_em_36_41.csv', 'w') as f:
                        wr = csv.writer(f, lineterminator = '\n')
                        for projprobest in ProjProbEst_36_41:
                            wr.writerow([projprobest])

### CALCULATION 42_47 ################################################################################################################

# The code generates annual probability of establishment projections for a set of species, for a set of
# climate regions, and for 6 years, using projected temperature and the historic relationship between
# temperature and each species' probability of establishment.
for year in Years1:
    a = year
    for areas in Ecoregions:
        b = Ecoregions.index(areas)
        for area in areas:
            for species in Species:
                c = Species.index(species)
                for temp in JulyTemp:
                    d = JulyTemp.index(temp)
                    e = int(round(ProjJulyTemp_42_47.at[a,b]))
                    if (e == JulyTemp[d]):
                        ProjProbEst_42_47.append(ProbEst[c][d])

### OUTPUT 42_47 #####################################################################################################################

# The code writes the annual probability of establishment projections into a csv file, called ProjProbEst.
                    with open('output_ProjProbEst_higher_em_42_47.csv', 'w') as f:
                        wr = csv.writer(f, lineterminator = '\n')
                        for projprobest in ProjProbEst_42_47:
                            wr.writerow([projprobest])

### CALCULATION 48_53 ################################################################################################################

# The code generates annual probability of establishment projections for a set of species, for a set of
# climate regions, and for 6 years, using projected temperature and the historic relationship between
# temperature and each species' probability of establishment.
for year in Years1:
    a = year
    for areas in Ecoregions:
        b = Ecoregions.index(areas)
        for area in areas:
            for species in Species:
                c = Species.index(species)
                for temp in JulyTemp:
                    d = JulyTemp.index(temp)
                    e = int(round(ProjJulyTemp_48_53.at[a,b]))
                    if (e == JulyTemp[d]):
                        ProjProbEst_48_53.append(ProbEst[c][d])

### OUTPUT 48_53 #####################################################################################################################

# The code writes the annual probability of establishment projections into a csv file, called ProjProbEst.
                    with open('output_ProjProbEst_higher_em_48_53.csv', 'w') as f:
                        wr = csv.writer(f, lineterminator = '\n')
                        for projprobest in ProjProbEst_48_53:
                            wr.writerow([projprobest])

### CALCULATION 54_59 ################################################################################################################

# The code generates annual probability of establishment projections for a set of species, for a set of
# climate regions, and for 6 years, using projected temperature and the historic relationship between
# temperature and each species' probability of establishment.
for year in Years1:
    a = year
    for areas in Ecoregions:
        b = Ecoregions.index(areas)
        for area in areas:
            for species in Species:
                c = Species.index(species)
                for temp in JulyTemp:
                    d = JulyTemp.index(temp)
                    e = int(round(ProjJulyTemp_54_59.at[a,b]))
                    if (e == JulyTemp[d]):
                        ProjProbEst_54_59.append(ProbEst[c][d])

### OUTPUT 54_59 #####################################################################################################################

# The code writes the annual probability of establishment projections into a csv file, called ProjProbEst.
                    with open('output_ProjProbEst_higher_em_54_59.csv', 'w') as f:
                        wr = csv.writer(f, lineterminator = '\n')
                        for projprobest in ProjProbEst_54_59:
                            wr.writerow([projprobest])

### CALCULATION 60_65 ################################################################################################################

# The code generates annual probability of establishment projections for a set of species, for a set of
# climate regions, and for 6 years, using projected temperature and the historic relationship between
# temperature and each species' probability of establishment.
for year in Years1:
    a = year
    for areas in Ecoregions:
        b = Ecoregions.index(areas)
        for area in areas:
            for species in Species:
                c = Species.index(species)
                for temp in JulyTemp:
                    d = JulyTemp.index(temp)
                    e = int(round(ProjJulyTemp_60_65.at[a,b]))
                    if (e == JulyTemp[d]):
                        ProjProbEst_60_65.append(ProbEst[c][d])

### OUTPUT 60_65 #####################################################################################################################

# The code writes the annual probability of establishment projections into a csv file, called ProjProbEst.
                    with open('output_ProjProbEst_higher_em_60_65.csv', 'w') as f:
                        wr = csv.writer(f, lineterminator = '\n')
                        for projprobest in ProjProbEst_60_65:
                            wr.writerow([projprobest])

### CALCULATION 66_70 ################################################################################################################

# The code generates annual probability of establishment projections for a set of species, for a set of
# climate regions, and for 5 years, using projected temperature and the historic relationship between
# temperature and each species' probability of establishment.
for year in Years2:
    a = year
    for areas in Ecoregions:
        b = Ecoregions.index(areas)
        for area in areas:
            for species in Species:
                c = Species.index(species)
                for temp in JulyTemp:
                    d = JulyTemp.index(temp)
                    e = int(round(ProjJulyTemp_66_70.at[a,b]))
                    if (e == JulyTemp[d]):
                        ProjProbEst_66_70.append(ProbEst[c][d])

### OUTPUT 66_70 #####################################################################################################################

# The code writes the annual probability of establishment projections into a csv file, called ProjProbEst.
                    with open('output_ProjProbEst_higher_em_66_70.csv', 'w') as f:
                        wr = csv.writer(f, lineterminator = '\n')
                        for projprobest in ProjProbEst_66_70:
                            wr.writerow([projprobest])
