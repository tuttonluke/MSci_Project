# plot time and longitude averaged cross section plots of INP concentration with superimposed temperature contours
import iris
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcols
import pandas as pd
import pylab
import os
import glob

def fmt(x):
    '''format contour labels'''
    s = f"{x:.1f}"
    if s.endswith("0"):
        s = f"{x:.0f}"
    return f"{s} \u00b0C"

def limitcontour(ax, x, y, z, clevs, xlim = None, ylim  = None, **kwargs):
    '''limit contours to the same plot extent as the INP data'''
    mask = np.ones(x.shape).astype(bool)
    if xlim:
        mask = mask & (x >= xlim[0]) & (x <= xlim[1])
    if ylim:
        mask = mask & (y >= ylim[0]) & (y <= ylim[1])
    xm = np.ma.masked_where(~mask , x)
    ym = np.ma.masked_where(~mask , y)
    zm = np.ma.masked_where(~mask , z)

    cs = ax.contour(xm,ym,zm, clevs, cmap = 'Greys_r', **kwargs)
    if xlim: ax.set_xlim(xlim) #Limit the x-axisif ylim: ax.set_ylim(ylim)
    ax.clabel(cs, inline = True, fmt = fmt)
    
# files and unchanging parameters
SpringINPnumber_file = sorted(glob.glob('/scratch/lt446/netscratch/bin_sum_nc_files/springINPnc/*'))
AutumnINPnumber_file = sorted(glob.glob('/scratch/lt446/netscratch/bin_sum_nc_files/autumnINPnc/*'))

SpringTEMP_file = sorted(glob.glob('/scratch/lt446/netscratch/bin_sum_nc_files/springTEMPnc/*'))
AutumnTEMP_file = sorted(glob.glob('/scratch/lt446/netscratch/bin_sum_nc_files/autumnTEMPnc/*'))

min_log_level = 0.001
max_log_level = 10000
cmap = 'PuBu' # colour scheme, see https://matplotlib.org/stable/tutorials/colors/colormaps.html
norm = mcols.SymLogNorm(linthresh = min_log_level, vmin = 0, vmax = max_log_level) # logarithmic data normalisation
ccont_levels = [10**i for i in range(-4, 5)] # colour contour levels
cbar_ticks = [10** i for i in range(-4, 5)] # colour bar ticks
ccont_levels_temp = [-60, -50, -40, -30, -20, -10, 0, 10, 20, 30]
cbar_ticks_temp = [-60, -50, -40, -30, -20, -10, 0, 10, 20, 30]

# plots
SPRINGdatafield = np.zeros((24, 385))
TEMPdatafield = np.zeros((24, 385))
counter = 0

for i in range(len(SpringINPnumber_file)):    
    
    INPcube = iris.load_cube(SpringINPnumber_file[i])
    INPdata = INPcube.data
    INPdata[np.isinf(INPdata)] = np.nan
    INPcube_longMEAN = INPcube.collapsed('longitude', iris.analysis.MEAN)
    INPdata_longMEAN = INPcube_longMEAN.data
    
    alt = INPcube.coord('altitude').points
    lat = INPcube.coord('latitude').points

    TEMPcube = iris.load_cube(SpringTEMP_file[i])
    TEMPdata = TEMPcube.data
    TEMPcube_lonmean = TEMPcube.collapsed('longitude', iris.analysis.MEAN) # TEMPcube_lonmean is 2D [altitude, latitude]
    TEMPdata_lonmean = TEMPcube_lonmean.data
    
    SPRINGdatafield += INPdata_longMEAN
    TEMPdatafield += TEMPdata_lonmean
    counter += 1
       
SPRINGdatafield /= counter
TEMPdatafield /= counter

x1, y1 = np.meshgrid(lat, alt)
    
fig = plt.figure(figsize = (10, 10))

fig.suptitle('Mean INP Concentration over Longitude - Spring', fontsize = 14,  y = 0.92)
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('Latitude ($^\circ$ N)', fontsize = 13)
ax.set_ylabel('Altitude (m asl)', fontsize = 13)

cs = ax.contourf(x1[:, :], y1[:, :], SPRINGdatafield[:, :], levels = ccont_levels, cmap = cmap, norm = norm, alpha = 0.9)
plt.colorbar(cs, orientation = 'horizontal', ticks = cbar_ticks, label = '# / L', pad = 0.1, shrink = 0.9)
plt.grid(axis='both', alpha = 0.5)
pylab.xlim([30,90])

csTEMP = limitcontour(ax, x1[:, :], y1[:, :], TEMPdatafield[:, :], 
ccont_levels_temp, xlim = [30, 90], ylim = [0, 12000])

fig.savefig('SpringINPcross_density' + '.png')
plt.show()
