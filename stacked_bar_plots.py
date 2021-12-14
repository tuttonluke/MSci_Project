# stacked bar plots of ash mass, number, surface area and INP number concentration burdens

import pandas as pd
import matplotlib.pyplot as plt
import glob
import iris
import numpy as np
import netCDF4
import sqlite3
import math

# create DataFrame from file names list for ease of sorting and naming
def date_df(lst):
    
    time_list = []
    name_list = []
    for i in range(len(lst)):
        time_list.append(lst[i][-15:-3])
    for i in lst:
        name_list.append(i[-15:-3])
    df = pd.DataFrame({'date' : time_list, 'name' : name_list})
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by = 'date')
    df['sorted_index'] = [i for i in range(len(time_list))]
    return df
  
# file lists and unchanging parameters
SpringBin1_ASHmass_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin1/Bin1ASHmass*.nc'))
SpringBin2_ASHmass_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin2/Bin2ASHmass*.nc'))
SpringBin3_ASHmass_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin3/Bin3ASHmass*.nc'))
SpringBin4_ASHmass_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin4/Bin4ASHmass*.nc'))
SpringBin5_ASHmass_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin5/Bin5ASHmass*.nc'))
SpringBin6_ASHmass_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin6/Bin6ASHmass*.nc'))
SpringBin7_ASHmass_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin7/Bin7ASHmass*.nc'))

AutumnBin1_ASHmass_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin1/Bin1OctASHmass*.nc'))
AutumnBin2_ASHmass_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin2/Bin2OctASHmass*.nc'))
AutumnBin3_ASHmass_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin3/Bin3OctASHmass*.nc'))
AutumnBin4_ASHmass_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin4/Bin4OctASHmass*.nc'))
AutumnBin5_ASHmass_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin5/Bin5OctASHmass*.nc'))
AutumnBin6_ASHmass_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin6/Bin6OctASHmass*.nc'))
AutumnBin7_ASHmass_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin7/Bin7OctASHmass*.nc'))

SpringBin1_ASH_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin1/Bin1ASHnumber*.nc'))
SpringBin2_ASH_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin2/Bin2ASHnumber*.nc'))
SpringBin3_ASH_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin3/Bin3ASHnumber*.nc'))
SpringBin4_ASH_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin4/Bin4ASHnumber*.nc'))
SpringBin5_ASH_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin5/Bin5ASHnumber*.nc'))
SpringBin6_ASH_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin6/Bin6ASHnumber*.nc'))
SpringBin7_ASH_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin7/Bin7ASHnumber*.nc'))

AutumnBin1_ASH_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin1/Bin1OctASHnumber*.nc'))
AutumnBin2_ASH_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin2/Bin2OctASHnumber*.nc'))
AutumnBin3_ASH_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin3/Bin3OctASHnumber*.nc'))
AutumnBin4_ASH_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin4/Bin4OctASHnumber*.nc'))
AutumnBin5_ASH_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin5/Bin5OctASHnumber*.nc'))
AutumnBin6_ASH_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin6/Bin6OctASHnumber*.nc'))
AutumnBin7_ASH_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin7/Bin7OctASHnumber*.nc'))

SpringBin1_INP_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin1/Bin1INP*.nc'))
SpringBin2_INP_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin2/Bin2INP*.nc'))
SpringBin3_INP_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin3/Bin3INP*.nc'))
SpringBin4_INP_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin4/Bin4INP*.nc'))
SpringBin5_INP_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin5/Bin5INP*.nc'))
SpringBin6_INP_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin6/Bin6INP*.nc'))
SpringBin7_INP_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/springBin7/Bin7INP*.nc'))

AutumnBin1_INP_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin1/Bin1OctINP*.nc'))
AutumnBin2_INP_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin2/Bin2OctINP*.nc'))
AutumnBin3_INP_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin3/Bin3OctINP*.nc'))
AutumnBin4_INP_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin4/Bin4OctINP*.nc'))
AutumnBin5_INP_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin5/Bin5OctINP*.nc'))
AutumnBin6_INP_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin6/Bin6OctINP*.nc'))
AutumnBin7_INP_list = sorted(glob.glob('/scratch/lt446/netscratch/bin_nc_files/autumnBin7/Bin7OctINP*.nc'))

SPRINGdf = date_df(SpringBin1_ASHmass_list)
AUTUMNdf = date_df(AutumnBin1_ASHmass_list)

# create lists of dates for spring and autumn eruption
SPRINGdates = list(SPRINGdf['date'])
for i in range(len(SPRINGdates)):
    SPRINGdates[i] = str(SPRINGdates[i])
SPRINGdays = []
for i in range(len(SpringBin1_ASHmass_list)):
    SPRINGdays.append(SPRINGdates[i][0:10])
SPRINGdf['days'] = SPRINGdays

AUTUMNdates = list(AUTUMNdf['date'])
for i in range(len(AUTUMNdates)):
    AUTUMNdates[i] = str(AUTUMNdates[i])
AUTUMNdays = []
for i in range(len(AutumnBin1_ASHmass_list)):
    AUTUMNdays.append(AUTUMNdates[i][0:10])
AUTUMNdf['days'] = AUTUMNdays

# account for volume differences at different locations (the Earth is spherical)
tempASHcube = iris.load_cube(SpringBin1_ASHmass_list[0])
lat = tempASHcube.coord('latitude').points

delta_alt = 500 # altitude bin size
delta_lat = 0.234375 # latitude bin size
R = 6378100.0 # radius of the Earth / m
delta_lat_metre = delta_lat * 2 * np.pi * R/360 # latitude bin size in metres

delta_lon = 0.3515625 # longitude bin size
delta_lon_metre = np.zeros(385) # empty array with the same dimension as latitude
delta_lon_metre[:] = delta_lon * 2 * np.pi * R * np.cos(lat[:] * np.pi / 180) / 360 # longitude bin sizes in metres

volume_array = np.zeros([24, 385, 1025]) # create an empty array with the same dimensions as INPcube
for i in range(len(volume_array[:, 0, 0])): # loop over altitude
    for j in range(len(volume_array[0,:,0])): # loop over latitude
        for k in range(len(volume_array[0, 0, :])): # loop over longitude
            volume_array[i, j, k]= delta_alt * delta_lat_metre * delta_lon_metre[j] # fill the array with gridbox volumes in m^3

VAdiams = ((6.34 * 10**-7), (2.85 * 10**-6), (5.63 * 10**-6), (1.13 * 10**-5), (2.25 * 10**-5), (4.51 * 10**-5), (9.02 * 10**-5)) # average diameters of ash particles for each bin
col_lst = ['dodgerblue', 'gold', 'firebrick', 'forestgreen', 'darkorchid', 'darkorange', 'teal'] # bar colours

# example plot (Ash mass burden)
SpringBin1ASHmass_burden_time = np.zeros(len(SpringBin1_ASHmass_list))
SpringBin2ASHmass_burden_time = np.zeros(len(SpringBin2_ASHmass_list))
SpringBin3ASHmass_burden_time = np.zeros(len(SpringBin3_ASHmass_list))
SpringBin4ASHmass_burden_time = np.zeros(len(SpringBin4_ASHmass_list))
SpringBin5ASHmass_burden_time = np.zeros(len(SpringBin5_ASHmass_list))
SpringBin6ASHmass_burden_time = np.zeros(len(SpringBin6_ASHmass_list))
SpringBin7ASHmass_burden_time = np.zeros(len(SpringBin7_ASHmass_list))

# calculate ash mass burden for each timestep for each bin size
# Bin 1
for i in range(len(SpringBin1_ASHmass_list)):
    ASHcube = iris.load_cube(SpringBin1_ASHmass_list[i])
    ASHdata = ASHcube.data # in # / m^3 
    ASHdata[np.isinf(ASHdata)] = np.nan
    # calculate the ash mass burden
    mass = (volume_array * ASHdata / 10**3) # convert to kg
    mass_burden = np.nansum(mass)
    SpringBin1ASHmass_burden_time[i] = mass_burden
    
# Bin 2
for i in range(len(SpringBin2_ASHmass_list)):
    ASHcube = iris.load_cube(SpringBin2_ASHmass_list[i])
    ASHdata = ASHcube.data
    ASHdata[np.isinf(ASHdata)] = np.nan
   # calculate the ash mass burden
    mass = (volume_array * ASHdata / 10**3) # convert to kg
    mass_burden = np.nansum(mass)
    SpringBin2ASHmass_burden_time[i] = mass_burden

# Bin 3
for i in range(len(SpringBin3_ASHmass_list)):
    ASHcube = iris.load_cube(SpringBin3_ASHmass_list[i])
    ASHdata = ASHcube.data 
    ASHdata[np.isinf(ASHdata)] = np.nan
    # calculate the ash mass burden
    mass = (volume_array * ASHdata / 10**3) # convert to kg
    mass_burden = np.nansum(mass)
    SpringBin3ASHmass_burden_time[i] = mass_burden 
    
# Bin 4
for i in range(len(SpringBin4_ASHmass_list)):
    ASHcube = iris.load_cube(SpringBin4_ASHmass_list[i])
    ASHdata = ASHcube.data
    ASHdata[np.isinf(ASHdata)] = np.nan
   # calculate the ash mass burden
    mass = (volume_array * ASHdata / 10**3) # convert to kg
    mass_burden = np.nansum(mass)
    SpringBin4ASHmass_burden_time[i] = mass_burden
    
# Bin 5
for i in range(len(SpringBin5_ASHmass_list)):
    ASHcube = iris.load_cube(SpringBin5_ASHmass_list[i])
    ASHdata = ASHcube.data 
    ASHdata[np.isinf(ASHdata)] = np.nan
   # calculate the ash mass burden
    mass = (volume_array * ASHdata / 10**3) # convert to kg
    mass_burden = np.nansum(mass)
    SpringBin5ASHmass_burden_time[i] = mass_burden
    
# Bin 6
for i in range(len(SpringBin6_ASHmass_list)):
    ASHcube = iris.load_cube(SpringBin6_ASHmass_list[i])
    ASHdata = ASHcube.data
    ASHdata[np.isinf(ASHdata)] = np.nan
    # calculate the ash mass burden
    mass = (volume_array * ASHdata / 10**3) # convert to kg
    mass_burden = np.nansum(mass)
    SpringBin6ASHmass_burden_time[i] = mass_burden
    
# Bin 7
for i in range(len(SpringBin7_ASHmass_list)):
    ASHcube = iris.load_cube(SpringBin7_ASHmass_list[i])
    ASHdata = ASHcube.data
    ASHdata[np.isinf(ASHdata)] = np.nan
   # calculate the ash mass burden
    mass = (volume_array * ASHdata / 10**3) # convert to kg
    mass_burden = np.nansum(mass)
    SpringBin7ASHmass_burden_time[i] = mass_burden

 # obtain daily averages using SQL
SPRINGmassBin1 = pd.DataFrame({'date' : SPRINGdays, 'mass' : SpringBin1ASHmass_burden_time})
SPRINGmassBin2 = pd.DataFrame({'date' : SPRINGdays, 'mass' : SpringBin2ASHmass_burden_time})
SPRINGmassBin3 = pd.DataFrame({'date' : SPRINGdays, 'mass' : SpringBin3ASHmass_burden_time})
SPRINGmassBin4 = pd.DataFrame({'date' : SPRINGdays, 'mass' : SpringBin4ASHmass_burden_time})
SPRINGmassBin5 = pd.DataFrame({'date' : SPRINGdays, 'mass' : SpringBin5ASHmass_burden_time})
SPRINGmassBin6 = pd.DataFrame({'date' : SPRINGdays, 'mass' : SpringBin6ASHmass_burden_time})
SPRINGmassBin7 = pd.DataFrame({'date' : SPRINGdays, 'mass' : SpringBin7ASHmass_burden_time})

SpringMASSdatabase = 'SpringASHmass.db'
SpringMASSconn = sqlite3.connect(SpringMASSdatabase)

SPRINGmassBin1.to_sql(name = 'spring_mass_bin1', con = SpringMASSconn)
SPRINGmassBin2.to_sql(name = 'spring_mass_bin2', con = SpringMASSconn)
SPRINGmassBin3.to_sql(name = 'spring_mass_bin3', con = SpringMASSconn)
SPRINGmassBin4.to_sql(name = 'spring_mass_bin4', con = SpringMASSconn)
SPRINGmassBin5.to_sql(name = 'spring_mass_bin5', con = SpringMASSconn)
SPRINGmassBin6.to_sql(name = 'spring_mass_bin6', con = SpringMASSconn)
SPRINGmassBin7.to_sql(name = 'spring_mass_bin7', con = SpringMASSconn)

SpringMASScur = SpringMASSconn.cursor()

sqlstr = ''' 
SELECT AVG(mass)
FROM spring_mass_bin1
GROUP BY date
'''

sqlstr2 = ''' 
SELECT AVG(mass)
FROM spring_mass_bin2
GROUP BY date
'''

sqlstr3 = ''' 
SELECT AVG(mass)
FROM spring_mass_bin3
GROUP BY date
'''
sqlstr4 = ''' 
SELECT AVG(mass)
FROM spring_mass_bin4
GROUP BY date
'''

sqlstr5 = ''' 
SELECT AVG(mass)
FROM spring_mass_bin5
GROUP BY date
'''

sqlstr6 = ''' 
SELECT AVG(mass)
FROM spring_mass_bin6
GROUP BY date
'''

sqlstr7 = ''' 
SELECT AVG(mass)
FROM spring_mass_bin7
GROUP BY date
'''

Bin1spring_mass_lst = []
Bin2spring_mass_lst = []
Bin3spring_mass_lst = []
Bin4spring_mass_lst = []
Bin5spring_mass_lst = []
Bin6spring_mass_lst = []
Bin7spring_mass_lst = []

for row in SpringMASScur.execute(sqlstr):
    Bin1spring_mass_lst.append(row[0])
for row in SpringMASScur.execute(sqlstr2):
    Bin2spring_mass_lst.append(row[0])
for row in SpringMASScur.execute(sqlstr3):
    Bin3spring_mass_lst.append(row[0])
for row in SpringMASScur.execute(sqlstr4):
    Bin4spring_mass_lst.append(row[0])
for row in SpringMASScur.execute(sqlstr5):
    Bin5spring_mass_lst.append(row[0])
for row in SpringMASScur.execute(sqlstr6):
    Bin6spring_mass_lst.append(row[0])
for row in SpringMASScur.execute(sqlstr7):
    Bin7spring_mass_lst.append(row[0])


# convert from kg to Tg
for i in range(len(Bin1spring_mass_lst)):
    Bin1spring_mass_lst[i] = Bin1spring_mass_lst[i] / 10**9
for i in range(len(Bin2spring_mass_lst)):
    Bin2spring_mass_lst[i] = Bin2spring_mass_lst[i] / 10**9
for i in range(len(Bin3spring_mass_lst)):
    Bin3spring_mass_lst[i] = Bin3spring_mass_lst[i] / 10**9
for i in range(len(Bin4spring_mass_lst)):
    Bin4spring_mass_lst[i] = Bin4spring_mass_lst[i] / 10**9
for i in range(len(Bin5spring_mass_lst)):
    Bin5spring_mass_lst[i] = Bin5spring_mass_lst[i] / 10**9
for i in range(len(Bin6spring_mass_lst)):
    Bin6spring_mass_lst[i] = Bin6spring_mass_lst[i] / 10**9
for i in range(len(Bin7spring_mass_lst)):
    Bin7spring_mass_lst[i] = Bin7spring_mass_lst[i] / 10**9

SpringMASSdf = pd.DataFrame({'0.1 - 2.0' : Bin1spring_mass_lst, '2.0 - 3.9' : Bin2spring_mass_lst, '3.9 - 7.8' : Bin3spring_mass_lst,
                       '7.8 - 15.6' : Bin4spring_mass_lst, '15.6 - 31.2' : Bin5spring_mass_lst, '31.2 - 62.5' : Bin6spring_mass_lst,
                       '62.5 - 125.0' : Bin7spring_mass_lst})

# plot the stacked bar plot
fig, ax = plt.subplots(figsize = (8, 5))

bottom = np.zeros(len(Bin1spring_mass_lst))

for i, col in enumerate(SpringMASSdf.columns):
    ax.bar(SpringMASSdf.index, SpringMASSdf[col], bottom = bottom, label = col, color = col_lst[i])
    bottom += np.array(SpringMASSdf[col])
    
ax.set_title('Ash Mass Burden by Particle Size - Spring', fontsize = 13, pad = 10)
ax.grid()
ax.set_axisbelow(True)
ax.set_ylabel('Ash mass burden (Tg)', fontsize = 12, labelpad = 10)
ax.set_ylim(0, 3.5)
ax.set_xlabel('Days From Start of Eruption', fontsize = 12, labelpad = 10)    
ax.legend(title = 'Bin sizes (μm)')

fig.savefig('ASHmassSPRING.png')
plt.show()
