# average INP concentration over the entire eruption period plotted on North Polar Stereo maps

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcols
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
import os
import netCDF4
import glob

# files and unchanging parameters

SpringINPnumber_file = sorted(glob.glob('/scratch/lt446/netscratch/bin_sum_nc_files/springINPnc/*'))
AutumnINPnumber_file = sorted(glob.glob('/scratch/lt446/netscratch/bin_sum_nc_files/autumnINPnc/*'))

minimum_log_level = 0.0001 # minimum concentration
maximum_scale_level = 100000 # maximum concentration
INP_cmap = "PuBu" # https://matplotlib.org/stable/tutorials/colors/colormaps.html
INP_norm = mcols.SymLogNorm(linthresh= minimum_log_level,
                            vmin = 0,
                            vmax = maximum_scale_level)
# spring INP density plot
SPRINGdatafield = np.zeros((385, 1025))
counter = 0

# sum INP concentrations in each bin
for i in range(100, 101):
    nc_INP = netCDF4.Dataset(SpringINPnumber_file[i])
    INPfield = nc_INP['inp_concentration']
    
    altitude = nc_INP['altitude']
    latitude = nc_INP['latitude']
    longitude = nc_INP['longitude']
    INPdata = INPfield[:].data
    alt = altitude[:].data
    lat = latitude[:].data
    lon = longitude[:].data
    
    # various plotting options
    # datafield = np.nansum(INPdata[:, :, :], axis = 0) # INP concentration sum (divide by no. altitude bins for consistent units)
    datafield = np.nanmean(INPdata[:, :, :], axis = 0) # mean INP concentration in vertical column
    # datafield = np.nanmax(INPdata[:, :, :], axis = 0) # max INP concentration in vertical column
    # datafield = np.nansum(INPdata[10, :, :], axis = 0) # INP concentration at specific altitude
    
    # sum INP from each timestep
    for k in range(385):
        for l in range(1025):
            SPRINGdatafield[k][l] +=  datafield[k][l]
    
    counter += 1 

# average INP concentration over the duration of the eruption
for k in range(385):
        for l in range(1025):
            SPRINGdatafield[k][l] / counter
 
# plot 
y1, x1 = np.meshgrid(lon, lat)

fig = plt.figure(figsize=(10, 10))
extent = [-13000000, 13000000, -13000000, 13000000] # W, E, S, N
ax = fig.add_subplot(1, 1, 1, projection = ccrs.NorthPolarStereo()) 
ax.set_extent(extent, crs = ccrs.NorthPolarStereo())   
ax.gridlines()                                  
ax.coastlines(resolution = '50m');                  
ax.add_feature(cfeature.LAND.with_scale('50m'))
tick_levels = [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000]  # the ticks on the colorbar
levs = [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000]         # the contour levels
# the following line is the actual plotting on the map
cs = ax.contourf(y1[:,:], x1[:,:], SPRINGdatafield[:,:], levels = levs,
             transform = ccrs.PlateCarree(), cmap = INP_cmap, norm = INP_norm)
# adding the gridline labels on the map and add titles and the colorbar:
# ax.gridlines(draw_labels = True, dms = False, x_inline = False, y_inline = False)
ax.set_title('Average INP concentration Over Entire Eruption - Spring', fontsize = 14, pad = 20)
plt.colorbar(cs, orientation = 'horizontal', ticks = tick_levels, label = '# / L', pad = 0.05, shrink = 0.7);

fig.savefig('SPRINGpolar_INP.png')
plt.show()
