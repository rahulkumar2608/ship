# A script that plots the ship and train data
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, DateFormatter
from mpl_toolkits.basemap import Basemap
from matplotlib import cm
import read
import pandas as pd
import matplotlib.gridspec as gridspec
from scipy import stats
from matplotlib.offsetbox import AnchoredText
import average
from matplotlib.ticker import MaxNLocator
import ratios
import bias_correction

##########
#SETUP 2 #------------------------------------------------------------------------
##########
#the offste values from the bias test
#off_co21=8.34  #old sim
#off_co22=7.61  #old sim
#old offset removal method
off_co21=0
off_co22=0
off_ch41=0
off_ch42=0
off_co1=0
off_co2=0

ind1=1327 #where the ship turnes 2012
ind2=2098 #2013

#######
#FILES#------------------------------------------------------------------------
####### 
#path
path_meas = '/home/bb907/Desktop/Computer/Work/Data/Ship_Train_insitu/Ship_2012_2013/Measurements/Avg_Measurements/'
path_gc = '/home/bb907/Desktop/Computer/Work/Data/Ship_Train_insitu/Ship_2012_2013/Model/GC/'

#Read in the measurments
data1=path_meas+'avg_meas20min2012shipAll.csv'
data2=path_meas+'avg_meas20min2013shipAll.csv'

#######
#READ #------------------------------------------------------------------------
#######
#Measurements
co2_1,date1, lat1, lon1, pres1 = read.meas(data1, x_row=6)#Ship 2012
co2_2,date2, lat2, lon2, pres2 = read.meas(data2, x_row=6)#Ship 2013
#CH4
ch4_1,date1, lat1, lon1, pres1 = read.meas(data1, x_row=7)
ch4_2,date2, lat2, lon2, pres2 = read.meas(data2, x_row=7)
#CO
co_1,date1, lat1, lon1, pres1 = read.meas(data1, x_row=8)
co_2,date2, lat2, lon2, pres2 = read.meas(data2, x_row=8)

#Read in GEOS-Chem
#co2
co2_1_gc,date_gc1,lat_gc1, lon_gc1, pres_gc1 = read.read_model(path_gc+"CO2/1/*.txt", convert=1000000,offset=off_co21) 
co2_2_gc,date_gc2,lat_gc2, lon_gc2, pres_gc2 = read.read_model(path_gc+"CO2/2/*.txt", convert=1000000,offset=off_co22)
#CH4
ch4_1_gc,date_gc1,lat_gc1, lon_gc1, pres_gc1  = read.read_model(path_gc+"CH4/1/*.txt",  convert=1000000000,offset=off_ch41)
ch4_2_gc,date_gc2,lat_gc2, lon_gc2, pres_gc2  = read.read_model(path_gc+"CH4/2/*.txt",  convert=1000000000,offset=off_ch42)
#CO
co_1_gc,date_gc1,lat_gc1, lon_gc1, pres_gc1   = read.read_model(path_gc+"CO/1/*.txt",  convert=1000000000,offset=off_co1)
co_2_gc,date_gc2,lat_gc2, lon_gc2, pres_gc2   = read.read_model(path_gc+"CO/2/*.txt",  convert=1000000000,offset=off_co2)

#MERGING
#I DONT need the mergin anymore because the gc and measurements averaging is now identical so boths datasets have the same length
#the routins for the merging are at the end of this script

##################
#BIAS CORRECTION #------------------------------------------------------------------------
##################
#Only co2 and ch4

co2_1_gc=bias_correction.bias_correction(date_gc1,co2_1_gc,'CO2_13')
co2_2_gc=bias_correction.bias_correction(date_gc2,co2_2_gc,'CO2_13')

ch4_1_gc=bias_correction.bias_correction(date_gc1,ch4_1_gc,'CH4_13')
ch4_2_gc=bias_correction.bias_correction(date_gc2,ch4_2_gc,'CH4_13')

#co_1_gc=bias_correction.bias_correction(date_gc1,co_1_gc,'CO_6')
#co_2_gc=bias_correction.bias_correction(date_gc2,co_2_gc,'CO_6')

#############
#DIFFERENCE #------------------------------------------------------------------------
#############
#Calculate the difference
diff_co2_1 = co2_1_gc-co2_1
diff_ch4_1 = ch4_1_gc-ch4_1
diff_co_1 = co_1_gc-co_1

diff_co2_2 = co2_2_gc-co2_2
diff_ch4_2 = ch4_2_gc-ch4_2
diff_co_2 = co_2_gc-co_2

##############
#PLOT BASEMAP#------------------------------------------------------------------------
##############
#fig.subplots_adjust(hspace=-.2)
#fig.subplots_adjust(wspace=.1)
def plot_corr(lon,lat, gg, lab, suptitle, xlab='Longitude', ylab='Latitude'):
    x=np.array(lon)
    y=np.array(lat)
    z = np.array(gg)
    if suptitle=='Measurement 2012' or suptitle == 'Model 2012' or suptitle=='Model - Measurement 2012':
        m = Basemap(llcrnrlat=-45,  urcrnrlat=-15,
                  llcrnrlon=140, urcrnrlon=180,
                  resolution='i',projection='merc')   
        parallels = np.arange(-45,-15, 5.)
        meridians = np.arange(140,180,10.)
    else:
        m = Basemap(llcrnrlat=-45,  urcrnrlat=-5,
          llcrnrlon=95, urcrnrlon=157,
          resolution='i',projection='merc')
        parallels = np.arange(-45,-5, 10.)
        meridians = np.arange(95,155,15.)
    # labels = [left,right,top,bottom]
    m.drawparallels(parallels,labels=[True,False,True,False], fontsize=20,linewidth=0.5)
    m.drawmeridians(meridians,labels=[True,False,False,True], fontsize=20,linewidth=0.5)
    m.drawcountries()
    m.drawcoastlines()
    #m.bluemarble()
    m.drawmapboundary()  
    #create lat lon for the map
    x1,y1=m(x,y)
    if suptitle=='Model - Measurement 2012' or suptitle=='Model - Measurement 2013':
        m.scatter(x1, y1, s=95, c=z, marker="x", cmap=cm.RdGy)
    else:
        m.scatter(x1, y1, s=95, c=z, marker="x", cmap=cm.magma_r)
    c = m.colorbar()
    if suptitle=='Model - Measurement 2012' or suptitle=='Model - Measurement 2013': 
        c.set_label(lab, fontsize=25)
    c.ax.tick_params(labelsize=20)
    #limits for the colorbar and plot
    if lab=='CO2 (ppmv)' or lab=='CO2 (ppmv) ':
        plt.clim(388, 401)
        c.set_ticks(np.arange(388, 401, 2))
    elif lab=='CH4 (ppbv)' or lab=='CH4 (ppbv) ':
        plt.clim(1740, 1900)
        c.set_ticks(np.arange(1740, 1900, 30))
    elif lab=='CO (ppbv)' or lab=='CO (ppbv) ':
        plt.clim(40, 140)
        c.set_ticks(np.arange(40, 140, 15))
    elif lab=='CO2 [ppmv]':
        plt.clim(-3, 3)
        c.set_ticks(np.arange(-3,3+1,1))
    elif lab=='CO [ppbv]':
        plt.clim(-20, 20)
        c.set_ticks(np.arange(-20,20+1,5))
    else:
        plt.clim(-25, 25)
        c.set_ticks(np.arange(-25,25+1,10))
    if suptitle=='Measurement 2012' or suptitle == 'Model 2012' or suptitle=='Model - Measurement 2012' or suptitle=='Measurement 2013':
        c.remove()
    #plt.xlabel(xlab, fontsize=20)
    #plt.ylabel(ylab, fontsize=20)
    #ax1.xaxis.set_label_coords(0.5, -0.20)
    #ax1.yaxis.set_label_coords(-0.13, 0.5)
    if lab=='CO2 (ppmv)' or lab=='CO2 [ppmv]' or lab=='CO2 (ppmv) ':
        plt.title(suptitle, y=1.1,fontsize=25)
    #plt.title(title)
    #plt.subplot_tool()
    #plot the text NS and SB
    if suptitle=='Measurement 2012' and lab=='CO2 (ppmv) ':
        x1,y1 = m(142,-29)
        x2,y2 = m(165,-34)
        plt.text(x1,y1,'NB', fontsize=25, color='black')
        plt.text(x2,y2,'SB', fontsize=25, color='black')
    if suptitle=='Measurement 2013' and lab=='CO2 (ppmv) ':
        x3,y3 = m(110,-13)
        x4,y4 = m(151,-44)
        plt.text(x3,y3,'NB', fontsize=25, color='black')
        plt.text(x4,y4,'SB', fontsize=25, color='black')
    return m

fig = plt.figure()
#Measurements
#2012
#plt.subplots_adjust(wspace=-.3)

ax1=plt.subplot(361)
ax1 = plot_corr(lon1, lat1, co2_1,  lab='CO2 (ppmv) ', suptitle='Measurement 2012')
ax1=plt.subplot(367)
ax1 = plot_corr(lon1, lat1, ch4_1,lab='CH4 (ppbv) ', suptitle='Measurement 2012') 
ax1=plt.subplot(3,6,13)
ax1 = plot_corr(lon1, lat1, co_1,  lab='CO (ppbv) ', suptitle='Measurement 2012') 

#model
ax1=plt.subplot(362)
ax1 = plot_corr(lon_gc1, lat_gc1, co2_1_gc,  lab='CO2 (ppmv)', suptitle='Model 2012')
ax1=plt.subplot(368)
ax1 = plot_corr(lon_gc1, lat_gc1, ch4_1_gc,lab='CH4 (ppbv)', suptitle='Model 2012')
ax1=plt.subplot(3,6,14)
ax1 = plot_corr(lon_gc1, lat_gc1, co_1_gc,  lab='CO (ppbv)', suptitle='Model 2012')

#diff
ax1=plt.subplot(363)
ax1 = plot_corr(lon_gc1, lat_gc1, diff_co2_1,  lab='CO2 [ppmv]', suptitle='Model - Measurement 2012')
ax1=plt.subplot(369)
ax1 = plot_corr(lon_gc1, lat_gc1, diff_ch4_1,lab='CH4 [ppbv]', suptitle='Model - Measurement 2012')
ax1=plt.subplot(3,6,15)
ax1 = plot_corr(lon_gc1, lat_gc1, diff_co_1,  lab='CO [ppbv]', suptitle='Model - Measurement 2012')

#2013
ax1=plt.subplot(364)
ax1 = plot_corr(lon2, lat2, co2_2,  lab='CO2 (ppmv) ', suptitle='Measurement 2013')
ax1=plt.subplot(3,6,10)
ax1 = plot_corr(lon2, lat2, ch4_2,  lab='CH4 (ppbv) ', suptitle='Measurement 2013')
ax1=plt.subplot(3,6,16)
ax1 = plot_corr(lon2, lat2, co_2,lab='CO (ppbv) ', suptitle='Measurement 2013')

#2013
ax1=plt.subplot(365)
ax1 = plot_corr(lon_gc2, lat_gc2, co2_2_gc,  lab='CO2 (ppmv)', suptitle='Model 2013')
ax1=plt.subplot(3,6,11)
ax1 = plot_corr(lon_gc2, lat_gc2, ch4_2_gc,  lab='CH4 (ppbv)', suptitle='Model 2013')
ax1=plt.subplot(3,6,17)
ax1 = plot_corr(lon_gc2, lat_gc2, co_2_gc,lab='CO (ppbv)', suptitle='Model 2013')

#diff
ax1=plt.subplot(366)
ax1 = plot_corr(lon_gc2, lat_gc2, diff_co2_2,  lab='CO2 [ppmv]', suptitle='Model - Measurement 2013')
ax1=plt.subplot(3,6,12)
ax1 = plot_corr(lon_gc2, lat_gc2, diff_ch4_2,lab='CH4 [ppbv]', suptitle='Model - Measurement 2013')
ax1=plt.subplot(3,6,18)
ax1 = plot_corr(lon_gc2, lat_gc2, diff_co_2,  lab='CO [ppbv]', suptitle='Model - Measurement 2013')

############################
#PLOT TIME  AND DIFFERENCE #---------------------------------------------------
############################
def plot_diff(date, gg,ylab):
    plt.plot(date,gg, '.',color='black')
    ax1.yaxis.tick_right()
    ax1.yaxis.set_label_position("right")
    plt.tick_params(axis='both', which='major', labelsize=30)
    plt.axhline(y=0., color='#a90308', linestyle='--', linewidth=2)
    if ylab=='CO2 (ppm)':
        ax1.yaxis.set_ticks(np.arange(-14, 14, 4))
        plt.ylim(-14,14)
    elif ylab=='CO (ppb)':
        ax1.yaxis.set_ticks(np.arange(-100, 100, 30))
        plt.ylim(-100,100)
    elif ylab=='CH4 (ppb)':
        ax1.yaxis.set_ticks(np.arange(-200, 200, 50))
        plt.ylim(-200, 200)
    #hide the x axis
    ax1.xaxis.set_major_formatter(plt.NullFormatter())
    return plt


def plot_time_lat(date, gg, gg_gc,ylab,tl):
    plt.plot(date,gg, '.',color='#a90308', label='Measurement')
    plt.plot(date,gg_gc, '.', color='#29465b',label='Model')
    #plt.xlim(date_d[0],date_w[-1])
    plt.tick_params(axis='both', which='major', labelsize=30)
    if ylab=='CO2 (ppm)':
        ax1.yaxis.set_ticks(np.arange(385, 410, 10))
        plt.ylim(385, 410)
    elif ylab=='CO (ppb)':
        ax1.yaxis.set_ticks(np.arange(30, 180, 40))
        plt.ylim(30,180)
    elif ylab=='CH4 (ppb)':
        ax1.yaxis.set_ticks(np.arange(1700, 2050, 60))
        plt.ylim(1700,2050)
    plt.ylabel(ylab,fontsize=30)
    plt.plot(np.nan, '.',color='black', label='Model-Measurement')
    if tl=='time':
        loc = DayLocator(interval=15)  # every month
        locFmt = DateFormatter('%m/%d') #show only the months on the plot
        ax1.xaxis.set_major_locator(loc)
        ax1.xaxis.set_major_formatter(locFmt)
        plt.xlabel('Date',fontsize=30)#old sim
    else:
        plt.xlabel('Latitude',fontsize=30)
    if ylab=='CO (ppb)':
        ax1.legend(fontsize=20).draggable()
    return plt

    
gs = gridspec.GridSpec(2, 3,
                       width_ratios=[1,1,1],
                       height_ratios=[1,1]
                       )
gs.update(hspace=0)

#2012
fig = plt.figure()
ax1 = plt.subplot(gs[0])
ax1=plot_diff(date1,diff_co2_1,'CO2 (ppm)')
ax1 = plt.subplot(gs[3])
ax1=plot_time_lat(date1,co2_1,co2_1_gc,'CO2 (ppm)', 'time')
ax1 = plt.subplot(gs[1])
ax1=plot_diff(date1,diff_ch4_1,'CH4 (ppb)')
ax1 = plt.subplot(gs[4])
ax1=plot_time_lat(date1,ch4_1,ch4_1_gc,'CH4 (ppb)', 'time')
ax1 = plt.subplot(gs[2])
ax1=plot_diff(date1,diff_co_1,'CO (ppb)')
ax1 = plt.subplot(gs[5])
ax1=plot_time_lat(date1,co_1,co_1_gc,'CO (ppb)', 'time')

#2013
fig = plt.figure()
ax1 = plt.subplot(gs[0])
ax1=plot_diff(date2,diff_co2_2,'CO2 (ppm)')
ax1 = plt.subplot(gs[3])
ax1=plot_time_lat(date2,co2_2,co2_2_gc,'CO2 (ppm)','time')
ax1 = plt.subplot(gs[1])
ax1=plot_diff(date2,diff_ch4_2,'CH4 (ppb)')
ax1 = plt.subplot(gs[4])
ax1=plot_time_lat(date2,ch4_2,ch4_2_gc,'CH4 (ppb)','time')
ax1 = plt.subplot(gs[2])
ax1=plot_diff(date2,diff_co_2,'CO (ppb)')
ax1 = plt.subplot(gs[5])
ax1=plot_time_lat(date2,co_2,co_2_gc,'CO (ppb)', 'time')


#########################
#PLOT LATITUDE NB AND SB#------------------------------------------------------
#########################
#Indicies are in the setup        
gs = gridspec.GridSpec(2, 3,
                       width_ratios=[1,1,1],
                       height_ratios=[1,1]
                       )
gs.update(hspace=0)

#2012 northbount
fig = plt.figure()
ax1 = plt.subplot(gs[0])
ax1=plot_diff(lat1[:ind1],diff_co2_1[:ind1],'CO2 (ppm)')
ax1 = plt.subplot(gs[3])
ax1=plot_time_lat(lat1[:ind1],co2_1[:ind1],co2_1_gc[:ind1],'CO2 (ppm)','lat')#2013 northbound
ax1 = plt.subplot(gs[1])
ax1=plot_diff(lat1[:ind1],diff_ch4_1[:ind1],'CH4 (ppb)')
ax1 = plt.subplot(gs[4])
ax1=plot_time_lat(lat1[:ind1],ch4_1[:ind1],ch4_1_gc[:ind1],'CH4 (ppb)','lat')
ax1 = plt.subplot(gs[2])
ax1=plot_diff(lat1[:ind1],diff_co_1[:ind1],'CO (ppb)')
ax1 = plt.subplot(gs[5])
ax1=plot_time_lat(lat1[:ind1],co_1[:ind1],co_1_gc[:ind1],'CO (ppb)','lat')

#2012 southbound
fig = plt.figure()
ax1 = plt.subplot(gs[0])
ax1=plot_diff(lat1[ind1:],diff_co2_1[ind1:],'CO2 (ppm)')
ax1 = plt.subplot(gs[3])
ax1=plot_time_lat(lat1[ind1:],co2_1[ind1:],co2_1_gc[ind1:],'CO2 (ppm)','lat')
ax1 = plt.subplot(gs[1])
ax1=plot_diff(lat1[ind1:],diff_ch4_1[ind1:],'CH4 (ppb)')
ax1 = plt.subplot(gs[4])
ax1=plot_time_lat(lat1[ind1:],ch4_1[ind1:],ch4_1_gc[ind1:],'CH4 (ppb)','lat')
ax1 = plt.subplot(gs[2])
ax1=plot_diff(lat1[ind1:],diff_co_1[ind1:],'CO (ppb)')
ax1 = plt.subplot(gs[5])
ax1=plot_time_lat(lat1[ind1:],co_1[ind1:],co_1_gc[ind1:],'CO (ppb)','lat')

#2013 northbound
fig = plt.figure()
ax1 = plt.subplot(gs[0])
ax1=plot_diff(lat2[:ind2],diff_co2_2[:ind2],'CO2 (ppm)')
ax1 = plt.subplot(gs[3])
ax1=plot_time_lat(lat2[:ind2],co2_2[:ind2],co2_2_gc[:ind2],'CO2 (ppm)','lat')
ax1 = plt.subplot(gs[1])
ax1=plot_diff(lat2[:ind2],diff_ch4_2[:ind2],'CH4 (ppb)')
ax1 = plt.subplot(gs[4])
ax1=plot_time_lat(lat2[:ind2],ch4_2[:ind2],ch4_2_gc[:ind2],'CH4 (ppb)','lat')
ax1 = plt.subplot(gs[2])
ax1=plot_diff(lat2[:ind2],diff_co_2[:ind2],'CO (ppb)')
ax1 = plt.subplot(gs[5])
ax1=plot_time_lat(lat2[:ind2],co_2[:ind2],co_2_gc[:ind2],'CO (ppb)','lat')

#2013 southbound
fig = plt.figure()
ax1 = plt.subplot(gs[0])
ax1=plot_diff(lat2[ind2:],diff_co2_2[ind2:],'CO2 (ppm)')
ax1 = plt.subplot(gs[3])
ax1=plot_time_lat(lat2[ind2:],co2_2[ind2:],co2_2_gc[ind2:],'CO2 (ppm)','lat')
ax1 = plt.subplot(gs[1])
ax1=plot_diff(lat2[ind2:],diff_ch4_2[ind2:],'CH4 (ppb)')
ax1 = plt.subplot(gs[4])
ax1=plot_time_lat(lat2[ind2:],ch4_2[ind2:],ch4_2_gc[ind2:],'CH4 (ppb)','lat')
ax1 = plt.subplot(gs[2])
ax1=plot_diff(lat2[ind2:],diff_co_2[ind2:],'CO (ppb)')
ax1 = plt.subplot(gs[5])
ax1=plot_time_lat(lat2[ind2:],co_2[ind2:],co_2_gc[ind2:],'CO (ppb)','lat')

############################################################
#PLOT LATITUDE NB AND SB AGAIN BUT SEPPERATE MEAS NAD MODEL#-------------------
############################################################
#SWITCH BETWEEN MEASUREMENTS AND MODE LIN THE FUNCTION

def plot_lat(date, gg, gg_gc,ylab,tit):
    #UNCOMENT THE MEASUREMENTS OR MODEL
    plt.plot(date,gg, '.-',markersize=9,color='indigo', label='Measurement')
    #plt.plot(date,gg_gc, '.-',markersize=9, color='green',label='Model')
    #plt.xlim(date_d[0],date_w[-1])
    if ylab=='CO2 (ppm)' or ylab=='CO2 (ppm) ':
        ax1.yaxis.set_ticks(np.arange(387, 403, 5))
        plt.ylim(387, 403)
    elif ylab=='CO (ppb)' or ylab=='CO (ppb) ':
        ax1.yaxis.set_ticks(np.arange(35, 170, 40))
        plt.ylim(35,170)
    elif ylab=='CH4 (ppb)' or ylab=='CH4 (ppb) ':
        ax1.yaxis.set_ticks(np.arange(1740, 1910, 60))
        plt.ylim(1740,1910)
    plt.ylabel(ylab,fontsize=30)
    #plt.legend(loc='best')
    #ax1.legend().draggable()
    plt.xlim(-45,-8) 
    ax1.axes.get_xaxis().set_visible(False)
    if ylab=='CO (ppb)' or ylab=='CO (ppb) ':
        ax1.axes.get_xaxis().set_visible(True)
        plt.xlabel('Latitude', fontsize=30)
    if ylab=='CO2 (ppm) ' or ylab=='CH4 (ppb) ' or  ylab=='CO (ppb) ':
        ax1.axes.get_yaxis().set_visible(False)
    plt.tick_params(axis='both', which='major', labelsize=30)
    if ylab=='CO (ppb)':
        ax1.legend(fontsize=20).draggable()
    plt.title(tit,fontsize=30)
    return plt
       
       
gs = gridspec.GridSpec(3, 4,
                       width_ratios=[1,1,1,1],
                       height_ratios=[1,1,1]
                       )
gs.update(hspace=0)
gs.update(wspace=0.05)

#2012 northbount
fig = plt.figure()
ax1 = plt.subplot(gs[0])
ax1=plot_lat(lat1[:ind1],co2_1[:ind1],co2_1_gc[:ind1],ylab='CO2 (ppm)',tit='NB 2012')
ax1 = plt.subplot(gs[4])
ax1=plot_lat(lat1[:ind1],ch4_1[:ind1],ch4_1_gc[:ind1],ylab='CH4 (ppb)',tit='')
ax1 = plt.subplot(gs[8])
ax1=plot_lat(lat1[:ind1],co_1[:ind1],co_1_gc[:ind1],ylab='CO (ppb)',tit='')

#2012 southbound
ax1 = plt.subplot(gs[1])
ax1=plot_lat(lat1[ind1:],co2_1[ind1:],co2_1_gc[ind1:],ylab='CO2 (ppm) ',tit='SB 2012')
ax1 = plt.subplot(gs[5])
ax1=plot_lat(lat1[ind1:],ch4_1[ind1:],ch4_1_gc[ind1:],ylab='CH4 (ppb) ',tit='')
ax1 = plt.subplot(gs[9])
ax1=plot_lat(lat1[ind1:],co_1[ind1:],co_1_gc[ind1:],ylab='CO (ppb) ',tit='')

#2013 northbound
ax1 = plt.subplot(gs[2])
ax1=plot_lat(lat2[:ind2],co2_2[:ind2],co2_2_gc[:ind2],ylab='CO2 (ppm) ',tit='NB 2013')
ax1 = plt.subplot(gs[6])
ax1=plot_lat(lat2[:ind2],ch4_2[:ind2],ch4_2_gc[:ind2],ylab='CH4 (ppb) ',tit='')
ax1 = plt.subplot(gs[10])
ax1=plot_lat(lat2[:ind2],co_2[:ind2],co_2_gc[:ind2],ylab='CO (ppb) ',tit='')

#2013 southbound
ax1 = plt.subplot(gs[3])
ax1=plot_lat(lat2[ind2:],co2_2[ind2:],co2_2_gc[ind2:],ylab='CO2 (ppm) ',tit='SB 2013')
ax1 = plt.subplot(gs[7])
ax1=plot_lat(lat2[ind2:],ch4_2[ind2:],ch4_2_gc[ind2:],ylab='CH4 (ppb) ',tit='')
ax1 = plt.subplot(gs[11])
ax1=plot_lat(lat2[ind2:],co_2[ind2:],co_2_gc[ind2:],ylab='CO (ppb) ',tit='')


############################################################
#AVERAGE PER 0.1 LATITUDE BANDS                            #-------------------
############################################################
#CO2
lat1n,co2_1n,co2_1ng = average.average_01lat(lat1[:ind1],co2_1[:ind1],co2_1_gc[:ind1])#2012 N
lat1s,co2_1s,co2_1sg =  average.average_01lat(lat1[ind1:],co2_1[ind1:],co2_1_gc[ind1:])#2012 S
lat2n,co2_2n,co2_2ng =  average.average_01lat(lat2[:ind2],co2_2[:ind2],co2_2_gc[:ind2])#2013 N
lat2s,co2_2s,co2_2sg =  average.average_01lat(lat2[ind2:],co2_2[ind2:],co2_2_gc[ind2:])#2013 N
#CH4
lat1n,ch4_1n,ch4_1ng = average.average_01lat(lat1[:ind1],ch4_1[:ind1],ch4_1_gc[:ind1])
lat1s,ch4_1s,ch4_1sg =  average.average_01lat(lat1[ind1:],ch4_1[ind1:],ch4_1_gc[ind1:])
lat2n,ch4_2n,ch4_2ng =  average.average_01lat(lat2[:ind2],ch4_2[:ind2],ch4_2_gc[:ind2])
lat2s,ch4_2s,ch4_2sg =  average.average_01lat(lat2[ind2:],ch4_2[ind2:],ch4_2_gc[ind2:])
#CO
lat1n,co_1n,co_1ng = average.average_01lat(lat1[:ind1],co_1[:ind1],co_1_gc[:ind1])
lat1s,co_1s,co_1sg =  average.average_01lat(lat1[ind1:],co_1[ind1:],co_1_gc[ind1:])
lat2n,co_2n,co_2ng =  average.average_01lat(lat2[:ind2],co_2[:ind2],co_2_gc[:ind2])
lat2s,co_2s,co_2sg  =  average.average_01lat(lat2[ind2:],co_2[ind2:],co_2_gc[ind2:])

############################################################
#PLOT THE AVERAGED  WITH SHADED AREAS FOR CO-EMISSIONS     #-------------------
############################################################
def shade(la,lb,color):
    ax1.axvspan(la, lb,alpha=0.5, color=color)
    return ax1
    
def shade1(la,lb,color):
    ax1.axvspan(la, lb,alpha=0.5, color=color, fill=False,linewidth=3)
    return ax1    
    
def text(la,lb,ev):
    if ev in ('7','10','12','13','14'):
        plt.text(la,1890, ev,fontsize=23,fontweight='bold')
    else:
        plt.text(la,401.5, ev,fontsize=23,fontweight='bold')
    return ax1

#when i plot the model add fill=false to the shaded are so that I can get the lines    

########################
#LIMITS FOR THE SHADE  #-------------------
########################
    
#limits for the shade
#l1a=-42.2; l1b=-41.0
l2a=-39.1; l2b=-38.6
l3a=-38.4; l3b=-37.2
#l4a=-36.3; l4b=-35.3
l5a=-35.1; l5b=-34.5
l6a=-31.6; l6b=-30.9
l7a=-28.600000000000005; l7b=-27.9  #this was a stupid formating thing, since it is not -28.6
l8a=-27.6; l8b=-26.7

#limits for the shade
l9a=-41.6; l9b=-40.5
#l10a=-39.6; l10b=-38.3
l11a=-38.2; l11b=-36.6
l12a=-21.3; l12b=-19.9

#limits for the shade
l13a=-39.4; l13b=-37.7
l14a=-35.5; l14b=-34.5
#l15a=-19.8; l15b=-18.3
#l16a=-13.6; l16b=-12.4
l17a=-12.3; l17b=-10.9

#limits for the shade
l18a=-38; l18b=-36
l19a=-35.7; l19b=-35.2
#l20a=-32.8; l20b=-31.9
l21a=-29.6; l21b=-28.9
l22a=-11; l22b=-10.4

########################
#PLOT                  #-------------------
########################
gs = gridspec.GridSpec(3, 4,
                       width_ratios=[1,1,1,1],
                       height_ratios=[1,1,1]
                       )
gs.update(hspace=0)
gs.update(wspace=0.05)
#2012 northbount
fig = plt.figure()
ax1 = plt.subplot(gs[0])
ax1=plot_lat(lat1n,co2_1n,co2_1ng,ylab='CO2 (ppm)',tit='NB 2012')
shade(l2a,l2b,'red');shade1(l3a,l3b,'darkgoldenrod'); shade(l5a,l5b,'red');shade(l6a,l6b,'red');shade(l7a,l7b,'red');shade(l8a,l8b,'red')
text(l2a,l2b,'1');text(l3a,l3b,'2');text(l5a,l5b,'3');text(l6a,l6b,'4');text(l7a,l7b,'5');text(l8a,l8b,'6')

ax1 = plt.subplot(gs[4])
ax1=plot_lat(lat1n,ch4_1n,ch4_1ng,ylab='CH4 (ppb)',tit='')
shade(l2a,l2b,'red');shade(l5a,l5b,'red');shade(l6a,l6b,'red');shade(l7a,l7b,'red');shade(l8a,l8b,'red')

ax1 = plt.subplot(gs[8])
ax1=plot_lat(lat1n,co_1n,co_1ng,ylab='CO (ppb)',tit='')
shade(l2a,l2b,'red');shade1(l3a,l3b,'darkgoldenrod'); shade(l5a,l5b,'red');shade(l6a,l6b,'red');shade(l7a,l7b,'red');shade(l8a,l8b,'red')

#2012 southbound
ax1 = plt.subplot(gs[1])
ax1=plot_lat(lat1s,co2_1s,co2_1sg,ylab='CO2 (ppm) ',tit='SB 2012')
shade(l11a,l11b,'red');shade(l12a,l12b,'red')
text(l11a,l11b,'8');text(l12a,l12b,'9')

ax1 = plt.subplot(gs[5])
ax1=plot_lat(lat1s,ch4_1s,ch4_1sg,ylab='CH4 (ppb) ',tit='')
shade(l9a,l9b,'darkgray');shade(l11a,l11b,'red');shade1(l12a,l12b,'red')
text(l9a,l9b,'7')

ax1 = plt.subplot(gs[9])
ax1=plot_lat(lat1s,co_1s,co_1sg,ylab='CO (ppb) ',tit='')
shade(l9a,l9b,'darkgray');shade(l11a,l11b,'red');shade(l12a,l12b,'red')

#2013 northbound
ax1 = plt.subplot(gs[2])
ax1=plot_lat(lat2n,co2_2n,co2_2ng,ylab='CO2 (ppm) ',tit='NB 2013')
shade(l14a,l14b,'red');
text(l14a,l14b,'11')

ax1 = plt.subplot(gs[6])
ax1=plot_lat(lat2n,ch4_2n,ch4_2ng,ylab='CH4 (ppb) ',tit='')
shade(l13a,l13b,'darkgray');shade(l17a,l17b,'darkgray');shade(l14a,l14b,'red');
text(l13a,l13b,'10');text(l17a,l17b,'12')

ax1 = plt.subplot(gs[10])
ax1=plot_lat(lat2n,co_2n,co_2ng,ylab='CO (ppb) ',tit='')
shade(l13a,l13b,'darkgray');shade(l17a,l17b,'darkgray');shade(l14a,l14b,'red');

#2013 southbound
ax1 = plt.subplot(gs[3])
ax1=plot_lat(lat2s,co2_2s,co2_2sg,ylab='CO2 (ppm) ',tit='SB 2013')
shade(l21a,l21b,'aqua');shade(l22a,l22b,'red')
text(l21a,l21b,'15');text(l22a,l22b,'16')

ax1 = plt.subplot(gs[7])
ax1=plot_lat(lat2s,ch4_2s,ch4_2sg,ylab='CH4 (ppb) ',tit='')
shade1(l18a,l18b,'darkgray');shade(l19a,l19b,'darkgray'); shade(l21a,l21b,'aqua') ;shade(l22a,l22b,'red')
text(l18a,l18b,'13');text(l19a,l19b,'14')

ax1 = plt.subplot(gs[11])
ax1=plot_lat(lat2s,co_2s,co_2sg,ylab='CO (ppb) ',tit='')
shade1(l18a,l18b,'darkgray');shade(l19a,l19b,'darkgray');shade(l22a,l22b,'red')

#############################################################
#RATIOS OF THE REALTIVE ENHANCEMENTS SEPPERATE  OR COMBINED #-------------------
#############################################################
#relative change,basically the individual - the minimum of that traces, that way I wont have negative values

#SEPPARATE - ratios_sep function
#COMBINED - rations_com function

#all three
event2=ratios.ratios_com(l2a,l2b,lat1n,co2_1n,ch4_1n,co_1n,co2_1ng,ch4_1ng,co_1ng,ev='Event 1')
event5=ratios.ratios_com(l5a,l5b,lat1n,co2_1n,ch4_1n,co_1n,co2_1ng,ch4_1ng,co_1ng,ev='Event 3')
event6=ratios.ratios_com(l6a,l6b,lat1n,co2_1n,ch4_1n,co_1n,co2_1ng,ch4_1ng,co_1ng,ev='Event 4')
event7=ratios.ratios_com(l7a,l7b,lat1n,co2_1n,ch4_1n,co_1n,co2_1ng,ch4_1ng,co_1ng,ev='Event 5')
event8=ratios.ratios_com(l8a,l8b,lat1n,co2_1n,ch4_1n,co_1n,co2_1ng,ch4_1ng,co_1ng,ev='Event 6')
event11=ratios.ratios_com(l11a,l11b,lat1s,co2_1s,ch4_1s,co_1s,co2_1sg,ch4_1sg,co_1sg,ev='Event 8')
event12=ratios.ratios_com(l12a,l12b,lat1s,co2_1s,ch4_1s,co_1s,co2_1sg,ch4_1sg,co_1sg,ev='Event 9')
event14=ratios.ratios_com(l14a,l14b,lat2n,co2_2n,ch4_2n,co_2n,co2_2ng,ch4_2ng,co_2ng,ev='Event 11')
event21=ratios.ratios_com(l22a,l22b,lat2s,co2_2s,ch4_2s,co_2s,co2_2sg,ch4_2sg,co_2sg,ev='Event 16')
#ch4_co
event9=ratios.ratios_com(l9a,l9b,lat1s,co2_1s,ch4_1s,co_1s,co2_1sg,ch4_1sg,co_1sg,ev='Event 7')
event13=ratios.ratios_com(l13a,l13b,lat2n,co2_2n,ch4_2n,co_2n,co2_2ng,ch4_2ng,co_2ng,ev='Event 10')
event17=ratios.ratios_com(l17a,l17b,lat2n,co2_2n,ch4_2n,co_2n,co2_2ng,ch4_2ng,co_2ng,ev='Event 12')
event18=ratios.ratios_com(l18a,l18b,lat2s,co2_2s,ch4_2s,co_2s,co2_2sg,ch4_2sg,co_2sg,ev='Event 13')
event19=ratios.ratios_com(l19a,l19b,lat2s,co2_2s,ch4_2s,co_2s,co2_2sg,ch4_2sg,co_2sg,ev='Event 14')
#co_co2
event3=ratios.ratios_com(l3a,l3b,lat1n,co2_1n,ch4_1n,co_1n,co2_1ng,ch4_1ng,co_1ng,ev='Event 2')
#ch4_co2
event21=ratios.ratios_com(l21a,l21b,lat2s,co2_2s,ch4_2s,co_2s,co2_2sg,ch4_2sg,co_2sg,ev='Event 15')

#########################
#PLOT ALL               #------------------------------------------------------
#########################
#plot all the emission ratios on 1 plot, find a smarter way to pull ou the raitos
#2D values, events vs ratios vs standard error
ch4_co=np.array([[1,3,4,5,6,8,9,11,16,7,10,12,13,14],\
                 [1.81,1.78,1.39,1.19,3.52,4.20,1.18,0.81,0.15,1.05,0.92,0.27,2.21,1.24],\
                 [0.46,0.15,0.32,0.36,0.65,0.59,0.12,0.27,0.08,0.12,0.16,0.06,0.51,0.07]])
ch4_co2=np.array([[1,3,4,5,6,8,9,11,16,15],\
                  [13.91,8.59,3.55,2.73,3.85,15.37,4.94,2.00,5.79,1.92],\
                  [2.99,1.18,0.31,0.9,0.43,2.79,0.7,0.56,1.71,0.3]])
co_co2=np.array([[1,3,4,5,6,8,9,11,16,2],\
                 [7.18,4.73,2.15,2.08,0.86,3.30,4.12,1.43,19.02,2.3],\
                 [1.24,0.7,0.37,0.51,0.21,0.57,0.44,0.63,11.89,0.43]])

ch4_cog=np.array([[1,3,4,5,6,8,11,16,7,10,12,14],\
                 [1.82,2.45,4.96,1.45,1.87,3.61,1.73,0.14,2.52,1.52,0.07,1.86],\
                 [0.03,0.08,0.69,0.25,0.59,0.10,0.55,0.08,0.29,0.48,0.00,0.08]])
ch4_co2g=np.array([[1,3,4,5,6,8, 11,16,15],\
                  [9.15,19.14,8.95,10.64,11.52,14.40,4.02,5.50,10.12],\
                  [0.59,6.92,2.68,1.77,1.81,0.28,0.85,3.28,0.34]])
co_co2g=np.array([[1,3,4,5,6,8,9,11,16],\
                 [5.02,7.61,1.50,6.47,4.23,3.97,30.88,1.17,27.83],\
                 [0.35,3.00,0.64,1.55,1.1,0.07,11.84,0.58,13.94]])
#ratios
fig= plt.figure()
plt.errorbar(ch4_co[0],ch4_co[1],yerr=ch4_co[2],fmt='o', color='royalblue', markersize=16, label=r'$\Delta$CH4:'+r'$\Delta$CO Measurement')
plt.errorbar(ch4_co2[0],ch4_co2[1],yerr=ch4_co2[2],fmt='o', color='sandybrown', markersize=16, label=r'$\Delta$CH4:'+r'$\Delta$CO2 Measurement')
plt.errorbar(co_co2[0],co_co2[1],yerr=co_co2[2],fmt='o', color='gray', markersize=16, label=r'$\Delta$CO:'+r'$\Delta$CO2 Measurement')

plt.errorbar(ch4_cog[0],ch4_cog[1],yerr=ch4_cog[2],fmt='v', alpha=0.7, color='royalblue', markersize=16, label=r'$\Delta$CH4:'+r'$\Delta$CO Model')
plt.errorbar(ch4_co2g[0],ch4_co2g[1],yerr=ch4_co2g[2],fmt='v', alpha=0.7,color='sandybrown', markersize=16, label=r'$\Delta$CH4:'+r'$\Delta$CO2 Model')
plt.errorbar(co_co2g[0],co_co2g[1],yerr=co_co2g[2],fmt='v', alpha=0.7, color='gray', markersize=16, label=r'$\Delta$CO:'+r'$\Delta$CO2 Model')

l=plt.legend(ncol=2, fontsize=25)
l.draggable()
plt.xticks(np.arange(1,17,1))
plt.xlim(0,17)
plt.ylim(-0.4,32)
plt.xlabel('Events')
plt.ylabel('Emission ratios')

#########################
#CORRELATION            #------------------------------------------------------
#########################
#slope, intercept, r_value, p_value, std_err  
co2_1_r=stats.linregress(co2_1,co2_1_gc)
ch4_1_r=stats.linregress(ch4_1,ch4_1_gc)
co_1_r=stats.linregress(co_1,co_1_gc)

co2_2_r=stats.linregress(co2_2,co2_2_gc)
ch4_2_r=stats.linregress(ch4_2,ch4_2_gc)
co_2_r=stats.linregress(co_2,co_2_gc)

print "co2_1_r",co2_1_r[2]
print "co2_2_r",co2_2_r[2]
print "ch4_1_r",ch4_1_r[2]
print "ch4_2_r",ch4_2_r[2]
print "co_1_r",co_1_r[2]
print "co_2_r",co_2_r[2]
###---------------------------Mean Bias----------------------------------------
#model-meas
co2_1_mb=np.mean(diff_co2_1)
ch4_1_mb=np.mean(diff_ch4_1)
co_1_mb=np.mean(diff_co_1)

co2_2_mb=np.mean(diff_co2_2)
ch4_2_mb=np.mean(diff_ch4_2)
co_2_mb=np.mean(diff_co_2)

print "co2_1_mb",co2_1_mb
print "co2_2_mb",co2_2_mb
print "ch4_1_mb",ch4_1_mb
print "ch4_2_mb",ch4_2_mb
print "co_1_mb",co_1_mb
print "co_2_mb",co_2_mb

#########################
#RMSE                   #------------------------------------------------------
#########################
def rmse(predictions, targets):
    differences = predictions - targets                       #the DIFFERENCEs.
    differences_squared = differences ** 2                    #the SQUAREs of ^
    mean_of_differences_squared = differences_squared.mean()  #the MEAN of ^
    rmse_val = np.sqrt(mean_of_differences_squared)           #ROOT of ^
    return rmse_val  


co2_1_rmse=rmse(co2_1_gc,co2_1)
ch4_1_rmse=rmse(ch4_1_gc,ch4_1)
co_1_rmse=rmse(co_1_gc,co_1)

co2_2_rmse=rmse(co2_2_gc,co2_2)
ch4_2_rmse=rmse(ch4_2_gc,ch4_2)
co_2_rmse=rmse(co_2_gc,co_2)

print "co2_1_rmse",co2_1_rmse
print "co2_2_rmse",co2_2_rmse 
print "ch4_1_rmse",ch4_1_rmse 
print "ch4_2_rmse",ch4_2_rmse 
print "co_1_rmse",co_1_rmse
print "co_2_rmse",co_2_rmse

###############################################
#MEAN AND STD FOR THE ABCKGROUND REGIONS      #--------------------------------
##############################################
#Calculate the mean for all three gases between Brisbane and Fiji and in the other region with std
#2012 both SB (25 S - ) and NS part (155, 173)
print lat1n[170:]
print lat1s[70:160]

#co2
co2_1p=np.mean(co2_1n[170:])
co2_2p=np.mean(co2_1s[70:160])

co2_1ps=np.std(co2_1n[170:])
co2_2ps=np.std(co2_1s[70:160])


#CH4
ch4_1p=np.mean(ch4_1n[170:])
ch4_2p=np.mean(ch4_1s[70:160])

ch4_1ps=np.std(ch4_1n[170:])
ch4_2ps=np.std(ch4_1s[70:160])

#CO
co_1p=np.mean(co_1n[170:])
co_2p=np.mean(co_1s[70:160])

co_1ps=np.std(co_1n[170:])
co_2ps=np.std(co_1s[70:160])

print "co2_1p",co2_1p,"co2_1p std",co2_1ps,"co2_2p",co2_2p,"co2_2p std",co2_2ps
print "ch4_1p",ch4_1p,"ch4_1p std",ch4_1ps,"ch4_2p",ch4_2p,"ch4_2p std",ch4_2ps
print "co_1p",co_1p,"co_1p std",co_1ps,"co_2p",co_2p,"co_2p std",co_2ps

#2013
print lat2n[123:212]

#co2
co2_2np=np.mean(co2_2n[123:212])
co2_2nps=np.std(co2_2n[123:212])

#CH4
ch4_2np=np.mean(ch4_2n[123:212])
ch4_2nps=np.std(ch4_2n[123:212])

#CO
co_2np=np.mean(co_2n[123:212])
co_2nps=np.std(co_2n[123:212])

print "co2_2np",co2_2np,"co2_2np std",co2_2nps
print "ch4_2np",ch4_2np,"ch4_2np std",ch4_2nps
print "co_2np",co_2np,"co_2np std",co_2nps



##--------------------------------------
#
#def break_ax(x,y,r1,r2,lim1,lim2,lim3,lim4,ylab):
#    axes = []
#    gs = gridspec.GridSpec(2, 4,
#                       width_ratios=[1,1,1,1],
#                       height_ratios=[0.3,1]
#                       )
#    for i  in range(r1,r2):
#        ax = plt.subplot(gs[i])
#        axes.append(ax)
#    for i in range(r1,r2):
#        ax = plt.subplot(gs[i+4])
#        axes.append(ax)
#    
#    for i  in range(r1,r2):
#        # plot same data in both top and down axes
#        axes[i].plot(x[i],y[i], '.-',markersize=11, color='indigo')
#        axes[i].tick_params(axis='both', which='major', labelsize=30) 
#        axes[r1+4].set_ylabel(ylab,fontsize=30)
#        axes[i+4].plot(x[i],y[i], '.-',markersize=11, color='indigo')
#        axes[i+4].tick_params(axis='both', which='major', labelsize=30)        
#        axes[i+4].set_xlabel('Latitude', fontsize=30)
#        axes[i].set_xlim([-45,-8]) 
#        axes[i+4].set_xlim([-45,-8]) 
#        axes[i].axes.get_yaxis().set_visible(False)
#        axes[i+4].axes.get_yaxis().set_visible(False)
#        axes[r1].axes.get_yaxis().set_visible(True)
#        axes[r2].axes.get_yaxis().set_visible(True)
#        if ylab=='CO (ppb)':
#            axes[i].yaxis.set_ticks(np.arange(lim3, lim4, 40)) 
#        elif ylab=='CH4 (ppb)':
#            axes[i].yaxis.set_ticks(np.arange(lim3, lim4, 80))   
#    for i  in range(r1,r2):            
#        axes[i].spines['bottom'].set_visible(False)
#        axes[i+4].spines['top'].set_visible(False)
#        axes[i].xaxis.tick_top()
#        axes[i].tick_params(labeltop='off')  # don't put tick labels at the top
#        axes[i+4].xaxis.tick_bottom()
#    
#        axes[i].set_ylim([lim3,lim4])
#        axes[i+4].set_ylim([lim1,lim2])
#
#        
#
#
#lat=np.array([lat1[:ind1],lat1[ind1:],lat2[:ind2],lat2[ind2:]])
#co2=np.array([co2_1[:ind1],co2_1[ind1:],co2_2[:ind2],co2_2[ind2:]])
#ch4=np.array([ch4_1[:ind1],ch4_1[ind1:],ch4_2[:ind2],ch4_2[ind2:]])
#co=np.array([co_1[:ind1],co_1[ind1:],co_2[:ind2],co_2[ind2:]])
#
#
#fig=plt.figure()
#plt.subplots_adjust(hspace=0.1, wspace=0.05)  
#ax1=break_ax(lat,co2,0,4,387,395,395,405,'CO2 (ppm)')
#fig=plt.figure()
#plt.subplots_adjust(hspace=0.1, wspace=0.05)  
#ax1=break_ax(lat,ch4,0,4,1740,1840,1840,2010,'CH4 (ppb)')
#fig=plt.figure()
#plt.subplots_adjust(hspace=0.1, wspace=0.05)  
#ax1=break_ax(lat,co,0,4,40,80,80,201,'CO (ppb)')

#MERGING-----------------------------------------------------------------------
#def merge(date1, date2, lat1,lat2,lon1,lon2,x1,x2):
#    df = pd.DataFrame({'X':x1,'Lat':lat1,'Lon':lon1}, index=date1)   #measurements
#    df = df.loc[~df.index.duplicated(keep='first')] #there are some duplicate dates...
#    # not sure why, eliminate it or pandas wont work
#    df_gc = pd.DataFrame({'X_gc':x2,'Lat_gc':lat2,'Lon_gc':lon2}, index=date2) #geos chem output
#    df =df.reset_index()
#    df_gc =df_gc.reset_index()
#    #concate so it finds the values at same the date
#    result = pd.merge(df, df_gc, on='index')
#    #calculate the difference
#    diff=result['X'] - result['X_gc']
#    result=result.reset_index()
#    print result
#    date=result['index']
#    #convert the pandas series date to list
#    date = date.tolist()
#    #print result
#    #calculate the difference
#    #diff=result['X'] - result['X_gc']
#    lon=result['Lon']
#    lon = [float(i) for i in lon]
#    lat=result['Lat']
#    lat = [float(i) for i in lat]
#    x=result['X']
#    x = np.array([float(i) for i in x])
#    #x =x.reset_index()
#    #x=x['X']
#    lon_gc=result['Lon_gc']
#    lon_gc= [float(i) for i in lon_gc]
#    lat_gc=result['Lat_gc']
#    lat_gc= [float(i) for i in lat_gc]
#    x_gc=result['X_gc']
#    x_gc = np.array([float(i) for i in x_gc])
#    diff = x_gc-x 
#    return date, lat, lat_gc, lon, lon_gc, x,x_gc, diff

#merge the datasets
#merge it so that we can caluclate the difference
#co2
#date1m, lat1m, lat_gc1m, lon1m, lon_gc1m, co2_1m,co2_1_gcm, diff_co2_1 = merge( date1, date_gc1, lat1, lat_gc1, lon1, lon_gc1, co2_1,co2_1_gc,)
#date2m, lat2m, lat_gc2m, lon2m, lon_gc2m, co2_2m,co2_2_gcm, diff_co2_2 = merge( date2, date_gc2, lat2, lat_gc2, lon2, lon_gc2, co2_2,co2_2_gc)
#
##CH4
#date1m, lat1m, lat_gc1m, lon1m, lon_gc1m, ch4_1m,ch4_1_gcm, diff_ch4_1 = merge( date1, date_gc1, lat1, lat_gc1, lon1, lon_gc1, ch4_1,ch4_1_gc,)
#date2m, lat2m, lat_gc2m, lon2m, lon_gc2m, ch4_2m,ch4_2_gcm, diff_ch4_2 = merge( date2, date_gc2, lat2, lat_gc2, lon2, lon_gc2, ch4_2,ch4_2_gc)
#
##CO
#date1m, lat1m, lat_gc1m, lon1m, lon_gc1m, co_1m,co_1_gcm, diff_co_1 = merge( date1, date_gc1, lat1, lat_gc1, lon1, lon_gc1, co_1,co_1_gc,)
#date2m, lat2m, lat_gc2m, lon2m, lon_gc2m, co_2m,co_2_gcm, diff_co_2 = merge( date2, date_gc2, lat2, lat_gc2, lon2, lon_gc2, co_2,co_2_gc)