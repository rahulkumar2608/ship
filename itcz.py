#Linear correction method for the GC measurements bias for CO2 nad CH4
#The correction is based on the monthly averaged files

import matplotlib.pyplot as plt 
import numpy as np
from datetime import datetime, timedelta
from netCDF4 import MFDataset, Dataset
import matplotlib.dates as mdates
from matplotlib.offsetbox import AnchoredText
import matplotlib.ticker as ticker
import pandas as pd
from mpl_toolkits.basemap import Basemap,interp

##############
# FILES      #----------------------------------------------------------------- 
##############
#GEOS-Chem
gc='/home/bb907/Desktop/Computer/Work/Data/Ship_Train_insitu/GEOS_CHEM/merra2_CO2/monthly_all_old/monthly2013.nc'
dataset= MFDataset(gc)  
##############
# READ       #----------------------------------------------------------------- 
##############

tau=dataset.variables['tau0'][:]
x=dataset.variables['DAO-FLDS_PRECON'][:]
lat=dataset.variables['latitude_bounds'][:]
lon=dataset.variables['longitude_bounds'][:]
#Change from Tau to normal real time
d0=datetime(1985,1,1,0)
date = []
for time in tau:
    hrs=timedelta(hours=int(time))
    date.append(d0+hrs)

lats=lat[:,0]
#late=lat[-1,1]
#latn= np.append(lats,late)
lons=lon[:,0]
#lone=lon[-1,1]
#lonn= np.append(lons,lone)



def basemap(lons,lats,time,tit):
    #Set the map colour
    pl_color='magma_r'
    m=Basemap(projection='cyl',llcrnrlat=-88,urcrnrlat=88, llcrnrlon=-178,urcrnrlon=178,resolution='c')
    m.drawcountries(linewidth=0.7,color='black')
    m.drawcoastlines(linewidth=0.7,color='black')
    m.drawmapboundary(linewidth=0.7,color='black')
    m.drawparallels([0],labels=[0,0,0,0], linewidth=2,color='black') # draw equator, no label     
    lons,lats=m(lons,lats)
    #CO pcolor
    cs=m.pcolormesh(lons, lats, x[time,0,:,:], cmap=pl_color,latlon=True)#, vmin=0, vmax=500)#,
    #add title, colorbar
    cb=m.colorbar(cs,"bottom",size="5%", pad="2%")
    cb.ax.tick_params(labelsize=25)
    cb.set_label('mm/day',fontsize=25)
    plt.clim(0,11)
    cb.set_ticks(np.arange(0, 11, 2))
    if tit=='July':
        cb.remove()
    plt.title(tit,fontsize=25)
    return m

fig = plt.figure()    
ax1=plt.subplot(211)
ax1 = basemap(lons,lats,6,'July')
ax1=plt.subplot(212)
ax1 = basemap(lons,lats,7, 'August')
