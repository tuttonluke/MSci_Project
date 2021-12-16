# convert .txt files to more efficient .nc files
# calculate Ice Nucleating Particle (INP) concentrations from Volcanic Ash Concentrations
# sum all particle size bins for total concentration

import iris
import math
import numpy as np
import glob

# function to calculate INP concentration
def INP_calc(VAdiam, VAmass, Temp):
    ''' calculate INP concentration ash particle parameters and temperature'''
    VApvol = (4/3) * math.pi * (VAdiam / 2)**3 # ash particle volume assuming sphere
    VApsa = (4) * math.pi * (VAdiam / 2)**2 * 2 # ash particle SA - multiplied by 2 assuming ash sphericity is actually 0.5
    VAvol = VAmass / 2300000 # ash volume (mass/density)
    VApnum = VAvol / VApvol # ash particle number
    ns = np.where((Temp >= -35) & (Temp <= -12.5), np.power(10, (0.2663 - 0.183 * Temp)) * np.power(10, 4), 0) # parameterisation of ice-nucleating activity of Icelandic ash/dust
    INP = (1 - np.exp(-ns * VApsa)) * VApnum
    return INP # INP concentration in units # / m^3
  
# spring eruption files
field_file_list = sorted(glob.glob('/shared/netscratch/jd876/Fields_grid82*'))
met_file_list = sorted(glob.glob('/shared/netscratch/jd876/Met_Data1*'))

# autumn eruption files
field_file_list = sorted(glob.glob('/shared/netscratch/jd876/OctNov_simulation/Fields_grid82*'))
met_file_list = sorted(glob.glob('/shared/netscratch/jd876/OctNov_simulation/Met_Data1*'))

# process and save .nc files for ash mass concentration, temperature, and INP concentration
for i in range(len(field_file_list)):

    file_names = [field_file_list[i], met_file_list[i]]
    cubes = iris.load(file_names) 

    cubeVA0 = cubes[0] * 0.05 # we assume only 5% of ash mass remains airborne distally
    cubeVA1 = cubes[1] * 0.05
    cubeVA2 = cubes[2] * 0.05
    cubeVA3 = cubes[3] * 0.05
    cubeVA4 = cubes[4] * 0.05
    cubeVA5 = cubes[5] * 0.05
    cubeVA6 = cubes[6] * 0.05

    ashtotcube = (cubeVA0 + cubeVA1 + cubeVA2 + cubeVA3 + cubeVA4 + cubeVA5 + cubeVA6) * 1000000 # sum particle size bins and convert to ug / m^3
    ashtotcube.rename('ASH CONCENTRATION')
    ashtotcube.units = 'ug / m^3'

    iris.fileformats.netcdf.save(ashtotcube, 'OctASH' + field_file_list[i][-16:-4] + '.nc', netcdf_format='NETCDF4')

    cubeT = cubes[7] - 273.15 # convert Kelvin to Celsius
    cubeT.rename('TEMPERTAURE')
    cubeT.units = 'Celsius'
    Temp =  cubeT.data

    iris.fileformats.netcdf.save(cubeT,'OctTEMP' + met_file_list[i][-16:-4] + '.nc', netcdf_format='NETCDF4')

    VAdiams = ((6.34 * 10**-7), (2.85 * 10**-6), (5.63 * 10**-6), (1.13 * 10**-5), (2.25 * 10**-5), (4.51 * 10**-5), (9.02 * 10**-5))
    VAmasses = (cubeVA0.data, cubeVA1.data, cubeVA2.data, cubeVA3.data, cubeVA4.data, cubeVA5.data, cubeVA6.data)
    
    INP0 = INP_calc(VAdiams[0],VAmasses[0], Temp) 
    INP1 = INP_calc(VAdiams[1],VAmasses[1], Temp)
    INP2 = INP_calc(VAdiams[2],VAmasses[2], Temp)
    INP3 = INP_calc(VAdiams[3],VAmasses[3], Temp)
    INP4 = INP_calc(VAdiams[4],VAmasses[4], Temp)
    INP5 = INP_calc(VAdiams[5],VAmasses[5], Temp)
    INP6 = INP_calc(VAdiams[6],VAmasses[6], Temp)

    INPtot = (INP0 + INP1 + INP2 + INP3 + INP4 + INP5 + INP6) / 1000 # sum particle size bins and convert from #/m^3 to #/L
    INPtotcube = cubeT.copy() 
    INPtotcube.rename('INP CONCENTRATION')
    INPtotcube.units = '# / L'
    INPtotcube.data = INPtot

    iris.fileformats.netcdf.save(INPtotcube,'OctINP' + field_file_list[i][-16:-4] + '.nc', netcdf_format='NETCDF4')

# repeat for ash number concentration
for i in range(155, len(field_file_list)):

    file_names = [field_file_list[i], met_file_list[i]]
    cubes = iris.load(file_names) 

    VAmasses = (3.07 * 10**-13, 2.77 * 10**-11, 2.15 * 10**-10, 1.72 * 10**-9, 1.37 * 10**-8, 1.1 * 10**-7, 8.83 * 10**-7) # volcanic ash average masses for particle size bins

    # we assume only 5% of ash mass remains airborne distally
    # convert to # / m^3 by dividing my average mass of particle
    # convert to # / L by dividing by 1000
    cubeVA0 = ((cubes[0] * 0.05) / VAmasses[0]) / 1000
    cubeVA1 = ((cubes[1] * 0.05) / VAmasses[1]) / 1000
    cubeVA2 = ((cubes[2] * 0.05) / VAmasses[2]) / 1000
    cubeVA3 = ((cubes[3] * 0.05) / VAmasses[3]) / 1000
    cubeVA4 = ((cubes[4] * 0.05) / VAmasses[4]) / 1000
    cubeVA5 = ((cubes[5] * 0.05) / VAmasses[5]) / 1000
    cubeVA6 = ((cubes[6] * 0.05) / VAmasses[6]) / 1000
   
    ashtotcube = (cubeVA0 + cubeVA1 + cubeVA2 + cubeVA3 + cubeVA4 + cubeVA5 + cubeVA6) # sum bins
    ashtotcube.rename('ASH CONCENTRATION')
    ashtotcube.units = '# / L'

    iris.fileformats.netcdf.save(ashtotcube,'OctASHnumber' + field_file_list[i][-16:-4] + '.nc', netcdf_format='NETCDF4')
