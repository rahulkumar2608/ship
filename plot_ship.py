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
from label_color import label_color
from taylorDiagram import TaylorDiagram
import mean
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

##Read in GEOS-Chem
##co2
#co2_1_gc,date_gc1,lat_gc1, lon_gc1, pres_gc1 = read.read_model(path_gc+"CO2/1/*.txt", convert=1000000,offset=off_co21) 
#co2_2_gc,date_gc2,lat_gc2, lon_gc2, pres_gc2 = read.read_model(path_gc+"CO2/2/*.txt", convert=1000000,offset=off_co22)
##CH4
#ch4_1_gc,date_gc1,lat_gc1, lon_gc1, pres_gc1  = read.read_model(path_gc+"CH4/1/*.txt",  convert=1000000000,offset=off_ch41)
#ch4_2_gc,date_gc2,lat_gc2, lon_gc2, pres_gc2  = read.read_model(path_gc+"CH4/2/*.txt",  convert=1000000000,offset=off_ch42)
##CO
#co_1_gc,date_gc1,lat_gc1, lon_gc1, pres_gc1   = read.read_model(path_gc+"CO/1/*.txt",  convert=1000000000,offset=off_co1)
#co_2_gc,date_gc2,lat_gc2, lon_gc2, pres_gc2   = read.read_model(path_gc+"CO/2/*.txt",  convert=1000000000,offset=off_co2)

#Read in GEOS-Chem for the specified trip
#date,lat,lon,pres,co2_tot,co2_ff,co2_oc,co2_bal,co2_bb,co2_bf,co2_nte,co2_se,co2_av,co2_ch,co2_corr,'co2_backg' 
date_gc1,lat_gc1, lon_gc1, pres_gc1,co2_1_gc,co2t_11,co2t_21,co2t_31,co2t_41,co2t_51,co2t_61,co2t_71,co2t_81,co2t_91,co2t_101,co2t_111 = read.read_model_tracers(path_gc+"CO2/1/*.txt",off_co21, convert=1000000, sp='CO2')
date_gc2,lat_gc2, lon_gc2, pres_gc2,co2_2_gc,co2t_12,co2t_22,co2t_32,co2t_42,co2t_52,co2t_62,co2t_72,co2t_82,co2t_92,co2t_102,co2t_112= read.read_model_tracers(path_gc+"CO2/2/*.txt",off_co22, convert=1000000, sp='CO2')
#date,lat,lon,pres,ch4_tot,ch4_og,ch4_cm,ch4_ls,ch4_wa,ch4_bf,ch4_ri,ch4_an,ch4_bb,ch4_we,ch4_sa,ch4_nat 
date_gc1,lat_gc1, lon_gc1, pres_gc1,ch4_1_gc, ch4t_11,ch4t_21,ch4t_31,ch4t_41,ch4t_51,ch4t_61,ch4t_71,ch4t_81,ch4t_91,ch4t_101,ch4t_111= read.read_model_tracers(path_gc+"CH4/1/*.txt",  off_ch41,convert=1000000000, sp='CH4')
date_gc2,lat_gc2, lon_gc2, pres_gc2,ch4_2_gc, ch4t_12,ch4t_22,ch4t_32,ch4t_42,ch4t_52,ch4t_62,ch4t_72,ch4t_82,ch4t_92,ch4t_102,ch4t_112= read.read_model_tracers(path_gc+"CH4/2/*.txt",  off_ch42,convert=1000000000, sp='CH4')
#date,lat,lon,pres,co_tot,co_aus,co_afr,co_sam,co_oth,co_bbsam,co_bbaf,co_bbnhas,co_bbaus,co_bbindo,co_bboth,co_ch4,co_nmvoc 
date_gc1,lat_gc1, lon_gc1, pres_gc1,co_1_gc, cot_11,cot_21,cot_31,cot_41,cot_51,cot_61,cot_71,cot_81,cot_91,cot_101,cot_111,cot_121= read.read_model_tracers(path_gc+"CO/1/*.txt",  off_co1,convert=1000000000, sp='CO')
date_gc2,lat_gc2, lon_gc2, pres_gc2,co_2_gc, cot_12,cot_22,cot_32,cot_42,cot_52,cot_62,cot_72,cot_82,cot_92,cot_102,cot_112,cot_121= read.read_model_tracers(path_gc+"CO/2/*.txt",  off_co2,convert=1000000000, sp='CO')

#group the tracers into 1 variable
co2_trac_1=np.array([co2t_11,co2t_21,co2t_31,co2t_41,co2t_51,co2t_61,co2t_71,co2t_81,co2t_91,co2t_101,co2t_111])
co2_trac_2=np.array([co2t_12,co2t_22,co2t_32,co2t_42,co2t_52,co2t_62,co2t_72,co2t_82,co2t_92,co2t_102,co2t_112])

ch4_trac_1=np.array([ch4t_11,ch4t_21,ch4t_31,ch4t_41,ch4t_51,ch4t_61,ch4t_71,ch4t_81,ch4t_91,ch4t_101,ch4t_111])
ch4_trac_2=np.array([ch4t_12,ch4t_22,ch4t_32,ch4t_42,ch4t_52,ch4t_62,ch4t_72,ch4t_82,ch4t_92,ch4t_102,ch4t_112])

co_trac_1=np.array([cot_11,cot_21,cot_31,cot_41,cot_51,cot_61,cot_71,cot_81,cot_91,cot_101,cot_111,cot_121])
co_trac_2=np.array([cot_12,cot_22,cot_32,cot_42,cot_52,cot_62,cot_72,cot_82,cot_92,cot_102,cot_112,cot_121])

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
        meridians = np.arange(150,190,10.)
    else:
        m = Basemap(llcrnrlat=-45,  urcrnrlat=-5,
          llcrnrlon=95, urcrnrlon=157,
          resolution='i',projection='merc')
        parallels = np.arange(-45,-5, 10.)
        meridians = np.arange(105,165,15.)
    # labels = [left,right,top,bottom]
    if suptitle=='Measurement 2012' or suptitle=='Measurement 2013':
        m.drawparallels(parallels,labels=[False,True,True,False], fontsize=20,linewidth=0.5)
        m.drawmeridians(meridians,labels=[False,True,False,True], fontsize=20,linewidth=0.5)
    else:
        m.drawparallels(parallels,labels=[False,False,False,False], fontsize=20,linewidth=0.5)
        m.drawmeridians(meridians,labels=[False,False,False,False], fontsize=20,linewidth=0.5)
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
    if suptitle=='Model - Measurement 2013': 
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
    if suptitle=='Measurement 2012' or suptitle=='Measurement 2013':
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
        x4,y4 = m(150,-44)
        plt.text(x3,y3,'NB', fontsize=25, color='black')
        plt.text(x4,y4,'SB', fontsize=25, color='black')
    if suptitle=='Measurement 2012' and lab=='CO2 (ppmv) ':
        x1,y1 = m(123,-15)
        plt.text(x1,y1,'a) CO2', fontsize=25, color='black')
    elif suptitle=='Measurement 2012' and lab=='CH4 (ppbv) ':
        x1,y1 = m(123,-15)
        plt.text(x1,y1,'b) CH4', fontsize=25, color='black')
    elif suptitle=='Measurement 2012' and lab=='CO (ppbv) ':
        x1,y1 = m(123,-15)
        plt.text(x1,y1,'c) CO', fontsize=25, color='black')
    return m

#r"${CH_4} (ppbv)$"
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

#############################
##PLOT TIME  AND DIFFERENCE #---------------------------------------------------
#############################
#def plot_diff(date, gg,ylab):
#    plt.plot(date,gg, '.',color='black')
#    ax1.yaxis.tick_right()
#    ax1.yaxis.set_label_position("right")
#    plt.tick_params(axis='both', which='major', labelsize=30)
#    plt.axhline(y=0., color='#a90308', linestyle='--', linewidth=2)
#    if ylab=='CO2 (ppm)':
#        ax1.yaxis.set_ticks(np.arange(-14, 14, 4))
#        plt.ylim(-14,14)
#    elif ylab=='CO (ppb)':
#        ax1.yaxis.set_ticks(np.arange(-100, 100, 30))
#        plt.ylim(-100,100)
#    elif ylab=='CH4 (ppb)':
#        ax1.yaxis.set_ticks(np.arange(-200, 200, 50))
#        plt.ylim(-200, 200)
#    #hide the x axis
#    ax1.xaxis.set_major_formatter(plt.NullFormatter())
#    return plt
#
#
#def plot_time_lat(date, gg, gg_gc,ylab,tl):
#    plt.plot(date,gg, '.',color='#a90308', label='Measurement')
#    plt.plot(date,gg_gc, '.', color='#29465b',label='Model')
#    #plt.xlim(date_d,date_w[-1])
#    plt.tick_params(axis='both', which='major', labelsize=30)
#    if ylab=='CO2 (ppm)':
#        ax1.yaxis.set_ticks(np.arange(385, 410, 10))
#        plt.ylim(385, 410)
#    elif ylab=='CO (ppb)':
#        ax1.yaxis.set_ticks(np.arange(30, 180, 40))
#        plt.ylim(30,180)
#    elif ylab=='CH4 (ppb)':
#        ax1.yaxis.set_ticks(np.arange(1700, 2050, 60))
#        plt.ylim(1700,2050)
#    plt.ylabel(ylab,fontsize=30)
#    plt.plot(np.nan, '.',color='black', label='Model-Measurement')
#    if tl=='time':
#        loc = DayLocator(interval=15)  # every month
#        locFmt = DateFormatter('%m/%d') #show only the months on the plot
#        ax1.xaxis.set_major_locator(loc)
#        ax1.xaxis.set_major_formatter(locFmt)
#        plt.xlabel('Date',fontsize=30)#old sim
#    else:
#        plt.xlabel('Latitude',fontsize=30)
#    if ylab=='CO (ppb)':
#        ax1.legend(fontsize=20).draggable()
#    return plt
#
#    
#gs = gridspec.GridSpec(2, 3,
#                       width_ratios=[1,1,1],
#                       height_ratios=[1,1]
#                       )
#gs.update(hspace=0)
#
##2012
#fig = plt.figure()
#ax1 = plt.subplot(gs[0])
#ax1=plot_diff(date1,diff_co2_1,'CO2 (ppm)')
#ax1 = plt.subplot(gs[3])
#ax1=plot_time_lat(date1,co2_1,co2_1_gc,'CO2 (ppm)', 'time')
#ax1 = plt.subplot(gs[1])
#ax1=plot_diff(date1,diff_ch4_1,'CH4 (ppb)')
#ax1 = plt.subplot(gs[4])
#ax1=plot_time_lat(date1,ch4_1,ch4_1_gc,'CH4 (ppb)', 'time')
#ax1 = plt.subplot(gs[2])
#ax1=plot_diff(date1,diff_co_1,'CO (ppb)')
#ax1 = plt.subplot(gs[5])
#ax1=plot_time_lat(date1,co_1,co_1_gc,'CO (ppb)', 'time')
#
##2013
#fig = plt.figure()
#ax1 = plt.subplot(gs[0])
#ax1=plot_diff(date2,diff_co2_2,'CO2 (ppm)')
#ax1 = plt.subplot(gs[3])
#ax1=plot_time_lat(date2,co2_2,co2_2_gc,'CO2 (ppm)','time')
#ax1 = plt.subplot(gs[1])
#ax1=plot_diff(date2,diff_ch4_2,'CH4 (ppb)')
#ax1 = plt.subplot(gs[4])
#ax1=plot_time_lat(date2,ch4_2,ch4_2_gc,'CH4 (ppb)','time')
#ax1 = plt.subplot(gs[2])
#ax1=plot_diff(date2,diff_co_2,'CO (ppb)')
#ax1 = plt.subplot(gs[5])
#ax1=plot_time_lat(date2,co_2,co_2_gc,'CO (ppb)', 'time')
#
#
##########################
##PLOT LATITUDE NB AND SB#------------------------------------------------------
##########################
##Indicies are in the setup        
#gs = gridspec.GridSpec(2, 3,
#                       width_ratios=[1,1,1],
#                       height_ratios=[1,1]
#                       )
#gs.update(hspace=0)
#
##2012 northbount
#fig = plt.figure()
#ax1 = plt.subplot(gs[0])
#ax1=plot_diff(lat1[:ind1],diff_co2_1[:ind1],'CO2 (ppm)')
#ax1 = plt.subplot(gs[3])
#ax1=plot_time_lat(lat1[:ind1],co2_1[:ind1],co2_1_gc[:ind1],'CO2 (ppm)','lat')#2013 northbound
#ax1 = plt.subplot(gs[1])
#ax1=plot_diff(lat1[:ind1],diff_ch4_1[:ind1],'CH4 (ppb)')
#ax1 = plt.subplot(gs[4])
#ax1=plot_time_lat(lat1[:ind1],ch4_1[:ind1],ch4_1_gc[:ind1],'CH4 (ppb)','lat')
#ax1 = plt.subplot(gs[2])
#ax1=plot_diff(lat1[:ind1],diff_co_1[:ind1],'CO (ppb)')
#ax1 = plt.subplot(gs[5])
#ax1=plot_time_lat(lat1[:ind1],co_1[:ind1],co_1_gc[:ind1],'CO (ppb)','lat')
#
##2012 southbound
#fig = plt.figure()
#ax1 = plt.subplot(gs[0])
#ax1=plot_diff(lat1[ind1:],diff_co2_1[ind1:],'CO2 (ppm)')
#ax1 = plt.subplot(gs[3])
#ax1=plot_time_lat(lat1[ind1:],co2_1[ind1:],co2_1_gc[ind1:],'CO2 (ppm)','lat')
#ax1 = plt.subplot(gs[1])
#ax1=plot_diff(lat1[ind1:],diff_ch4_1[ind1:],'CH4 (ppb)')
#ax1 = plt.subplot(gs[4])
#ax1=plot_time_lat(lat1[ind1:],ch4_1[ind1:],ch4_1_gc[ind1:],'CH4 (ppb)','lat')
#ax1 = plt.subplot(gs[2])
#ax1=plot_diff(lat1[ind1:],diff_co_1[ind1:],'CO (ppb)')
#ax1 = plt.subplot(gs[5])
#ax1=plot_time_lat(lat1[ind1:],co_1[ind1:],co_1_gc[ind1:],'CO (ppb)','lat')
#
##2013 northbound
#fig = plt.figure()
#ax1 = plt.subplot(gs[0])
#ax1=plot_diff(lat2[:ind2],diff_co2_2[:ind2],'CO2 (ppm)')
#ax1 = plt.subplot(gs[3])
#ax1=plot_time_lat(lat2[:ind2],co2_2[:ind2],co2_2_gc[:ind2],'CO2 (ppm)','lat')
#ax1 = plt.subplot(gs[1])
#ax1=plot_diff(lat2[:ind2],diff_ch4_2[:ind2],'CH4 (ppb)')
#ax1 = plt.subplot(gs[4])
#ax1=plot_time_lat(lat2[:ind2],ch4_2[:ind2],ch4_2_gc[:ind2],'CH4 (ppb)','lat')
#ax1 = plt.subplot(gs[2])
#ax1=plot_diff(lat2[:ind2],diff_co_2[:ind2],'CO (ppb)')
#ax1 = plt.subplot(gs[5])
#ax1=plot_time_lat(lat2[:ind2],co_2[:ind2],co_2_gc[:ind2],'CO (ppb)','lat')
#
##2013 southbound
#fig = plt.figure()
#ax1 = plt.subplot(gs[0])
#ax1=plot_diff(lat2[ind2:],diff_co2_2[ind2:],'CO2 (ppm)')
#ax1 = plt.subplot(gs[3])
#ax1=plot_time_lat(lat2[ind2:],co2_2[ind2:],co2_2_gc[ind2:],'CO2 (ppm)','lat')
#ax1 = plt.subplot(gs[1])
#ax1=plot_diff(lat2[ind2:],diff_ch4_2[ind2:],'CH4 (ppb)')
#ax1 = plt.subplot(gs[4])
#ax1=plot_time_lat(lat2[ind2:],ch4_2[ind2:],ch4_2_gc[ind2:],'CH4 (ppb)','lat')
#ax1 = plt.subplot(gs[2])
#ax1=plot_diff(lat2[ind2:],diff_co_2[ind2:],'CO (ppb)')
#ax1 = plt.subplot(gs[5])
#ax1=plot_time_lat(lat2[ind2:],co_2[ind2:],co_2_gc[ind2:],'CO (ppb)','lat')

############################################################
#PLOT LATITUDE NB AND SB AGAIN BUT SEPPERATE MEAS AND MODEL#-------------------
############################################################
#SWITCH BETWEEN MEASUREMENTS AND MODE LIN THE FUNCTION

def plot_lat(date, gg, gg_gc,ylab,tit):
    #UNCOMENT THE MEASUREMENTS OR MODEL
    #plt.plot(date,gg, '.-',markersize=9,color='black',alpha=0.7, label='Measurement')
    plt.plot(date,gg_gc, '.-',markersize=9, color='maroon',alpha=0.7,label='Model')
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
       
       
#gs = gridspec.GridSpec(3, 4,
#                       width_ratios=[1,1,1,1],
#                       height_ratios=[1,1,1]
#                       )
#gs.update(hspace=0)
#gs.update(wspace=0.05)
#
##2012 northbount
#fig = plt.figure()
#ax1 = plt.subplot(gs[0])
#ax1=plot_lat(lat1[:ind1],co2_1[:ind1],co2_1_gc[:ind1],ylab='CO2 (ppm)',tit='NB 2012')
#ax1 = plt.subplot(gs[4])
#ax1=plot_lat(lat1[:ind1],ch4_1[:ind1],ch4_1_gc[:ind1],ylab='CH4 (ppb)',tit='')
#ax1 = plt.subplot(gs[8])
#ax1=plot_lat(lat1[:ind1],co_1[:ind1],co_1_gc[:ind1],ylab='CO (ppb)',tit='')
#
##2012 southbound
#ax1 = plt.subplot(gs[1])
#ax1=plot_lat(lat1[ind1:],co2_1[ind1:],co2_1_gc[ind1:],ylab='CO2 (ppm) ',tit='SB 2012')
#ax1 = plt.subplot(gs[5])
#ax1=plot_lat(lat1[ind1:],ch4_1[ind1:],ch4_1_gc[ind1:],ylab='CH4 (ppb) ',tit='')
#ax1 = plt.subplot(gs[9])
#ax1=plot_lat(lat1[ind1:],co_1[ind1:],co_1_gc[ind1:],ylab='CO (ppb) ',tit='')
#
##2013 northbound
#ax1 = plt.subplot(gs[2])
#ax1=plot_lat(lat2[:ind2],co2_2[:ind2],co2_2_gc[:ind2],ylab='CO2 (ppm) ',tit='NB 2013')
#ax1 = plt.subplot(gs[6])
#ax1=plot_lat(lat2[:ind2],ch4_2[:ind2],ch4_2_gc[:ind2],ylab='CH4 (ppb) ',tit='')
#ax1 = plt.subplot(gs[10])
#ax1=plot_lat(lat2[:ind2],co_2[:ind2],co_2_gc[:ind2],ylab='CO (ppb) ',tit='')
#
##2013 southbound
#ax1 = plt.subplot(gs[3])
#ax1=plot_lat(lat2[ind2:],co2_2[ind2:],co2_2_gc[ind2:],ylab='CO2 (ppm) ',tit='SB 2013')
#ax1 = plt.subplot(gs[7])
#ax1=plot_lat(lat2[ind2:],ch4_2[ind2:],ch4_2_gc[ind2:],ylab='CH4 (ppb) ',tit='')
#ax1 = plt.subplot(gs[11])
#ax1=plot_lat(lat2[ind2:],co_2[ind2:],co_2_gc[ind2:],ylab='CO (ppb) ',tit='')


############################################################
#AVERAGE PER 0.1 LATITUDE BANDS                            #-------------------
############################################################
#CO2 measurement and model total
lat1n,co2_1n,co2_1ng = average.average_01lat(lat1[:ind1],co2_1[:ind1],co2_1_gc[:ind1])#2012 N
lat1s,co2_1s,co2_1sg =  average.average_01lat(lat1[ind1:],co2_1[ind1:],co2_1_gc[ind1:])#2012 S
lat2n,co2_2n,co2_2ng =  average.average_01lat(lat2[:ind2],co2_2[:ind2],co2_2_gc[:ind2])#2013 N
lat2s,co2_2s,co2_2sg =  average.average_01lat(lat2[ind2:],co2_2[ind2:],co2_2_gc[ind2:])#2013 N
co2_t_1ng=[] #it will be 3d, lat, tracers, tracers
co2_t_1sg=[] #it will be 3d, lat, tracers, tracers
co2_t_2ng=[] #it will be 3d, lat, tracers, tracers
co2_t_2sg=[] #it will be 3d, lat, tracers, tracers
for i in range(len(co2_trac_1)):
    co2_t_1ng.append(average.average_01lat(lat1[:ind1],co2_trac_1[i][:ind1],co2_trac_1[i][:ind1]))#2012 N
    co2_t_1sg.append(average.average_01lat(lat1[ind1:],co2_trac_1[i][ind1:],co2_trac_1[i][ind1:]))#2012 S
    co2_t_2ng.append(average.average_01lat(lat2[:ind2],co2_trac_2[i][:ind2],co2_trac_2[i][:ind2]))#2013 N
    co2_t_2sg.append(average.average_01lat(lat2[ind2:],co2_trac_2[i][ind2:],co2_trac_2[i][ind2:]))#2013 S

#CH4
lat1n,ch4_1n,ch4_1ng = average.average_01lat(lat1[:ind1],ch4_1[:ind1],ch4_1_gc[:ind1])
lat1s,ch4_1s,ch4_1sg =  average.average_01lat(lat1[ind1:],ch4_1[ind1:],ch4_1_gc[ind1:])
lat2n,ch4_2n,ch4_2ng =  average.average_01lat(lat2[:ind2],ch4_2[:ind2],ch4_2_gc[:ind2])
lat2s,ch4_2s,ch4_2sg =  average.average_01lat(lat2[ind2:],ch4_2[ind2:],ch4_2_gc[ind2:])
ch4_t_1ng=[] #it will be 3d, lat, tracers, tracers
ch4_t_1sg=[] #it will be 3d, lat, tracers, tracers
ch4_t_2ng=[] #it will be 3d, lat, tracers, tracers
ch4_t_2sg=[] #it will be 3d, lat, tracers, tracers
for i in range(len(ch4_trac_1)):
    ch4_t_1ng.append(average.average_01lat(lat1[:ind1],ch4_trac_1[i][:ind1],ch4_trac_1[i][:ind1]))#2012 N
    ch4_t_1sg.append(average.average_01lat(lat1[ind1:],ch4_trac_1[i][ind1:],ch4_trac_1[i][ind1:]))#2012 S
    ch4_t_2ng.append(average.average_01lat(lat2[:ind2],ch4_trac_2[i][:ind2],ch4_trac_2[i][:ind2]))#2013 N
    ch4_t_2sg.append(average.average_01lat(lat2[ind2:],ch4_trac_2[i][ind2:],ch4_trac_2[i][ind2:]))#2013 S
    
#CO
lat1n,co_1n,co_1ng = average.average_01lat(lat1[:ind1],co_1[:ind1],co_1_gc[:ind1])
lat1s,co_1s,co_1sg =  average.average_01lat(lat1[ind1:],co_1[ind1:],co_1_gc[ind1:])
lat2n,co_2n,co_2ng =  average.average_01lat(lat2[:ind2],co_2[:ind2],co_2_gc[:ind2])
lat2s,co_2s,co_2sg  =  average.average_01lat(lat2[ind2:],co_2[ind2:],co_2_gc[ind2:])
co_t_1ng=[] #it will be 3d, lat, tracers, tracers
co_t_1sg=[] #it will be 3d, lat, tracers, tracers
co_t_2ng=[] #it will be 3d, lat, tracers, tracers
co_t_2sg=[] #it will be 3d, lat, tracers, tracers
for i in range(len(co_trac_1)):
    co_t_1ng.append(average.average_01lat(lat1[:ind1],co_trac_1[i][:ind1],co_trac_1[i][:ind1]))#2012 N
    co_t_1sg.append(average.average_01lat(lat1[ind1:],co_trac_1[i][ind1:],co_trac_1[i][ind1:]))#2012 S
    co_t_2ng.append(average.average_01lat(lat2[:ind2],co_trac_2[i][:ind2],co_trac_2[i][:ind2]))#2013 N
    co_t_2sg.append(average.average_01lat(lat2[ind2:],co_trac_2[i][ind2:],co_trac_2[i][ind2:]))#2013 S

############################################################
#PLOT THE TRACERS                                          #-------------------
############################################################
#consistent colors and labels for the bar plot and pie plot

lc=label_color()
lab_col_co2=lc.co2
lab_col_ch4=lc.ch4
lab_col_co=lc.co

def plot_lat_tr(lat, x_tot, x_trac,lc,tot,n,n1):   
    p_n=np.arange(1,tot+1)
    p_n=p_n[::4] 
    ax1=plt.subplot(tot/4,4,n)
    plt.plot(lat,x_tot, 'o-',markersize=3, color=lc[0][1],alpha=0.7,label=lc[0][0])  
    for i in range(len(x_trac)):
        #ax1 = plt.subplot(gs[i])
        ax1=plt.subplot(tot/4,4,p_n[i+1]+n1)
        plt.plot(lat,x_trac[i][1], 'o-',markersize=3, color=lc[i+1][1],alpha=0.7,label=lc[i+1][0])
        plt.tick_params(axis='both', which='major', labelsize=10)
        if n==4:
            ax1.legend(loc='best',fontsize=10).draggable()
    return plt
    
fig = plt.figure()
fig.subplots_adjust(hspace=0)
ax1=plot_lat_tr(lat1n,co2_1ng,co2_t_1ng,lab_col_co2[1:],48,1,0)
ax1=plot_lat_tr(lat1s,co2_1sg,co2_t_1sg,lab_col_co2[1:],48,2,1)
ax1=plot_lat_tr(lat2n,co2_2ng,co2_t_2ng,lab_col_co2[1:],48,3,2) 
ax1=plot_lat_tr(lat2s,co2_2sg,co2_t_2sg,lab_col_co2[1:],48,4,3)

fig = plt.figure()
ax1=plot_lat_tr(lat1n,ch4_1ng,ch4_t_1ng,lab_col_ch4[1:],48,1,0)
ax1=plot_lat_tr(lat1s,ch4_1sg,ch4_t_1sg,lab_col_ch4[1:],48,2,1)
ax1=plot_lat_tr(lat2n,ch4_2ng,ch4_t_2ng,lab_col_ch4[1:],48,3,2) 
ax1=plot_lat_tr(lat2s,ch4_2sg,ch4_t_2sg,lab_col_ch4[1:],48,4,3)
    
fig = plt.figure()
ax1=plot_lat_tr(lat1n,co_1ng,co_t_1ng,lab_col_co[1:],52,1,0)
ax1=plot_lat_tr(lat1s,co_1sg,co_t_1sg,lab_col_co[1:],52,2,1)
ax1=plot_lat_tr(lat2n,co_2ng,co_t_2ng,lab_col_co[1:],52,3,2) 
ax1=plot_lat_tr(lat2s,co_2sg,co_t_2sg,lab_col_co[1:],52,4,3) 

############################################################
#PLOT THE AVERAGED  WITH SHADED AREAS FOR CO-EMISSIONS     #-------------------
############################################################
def shade(la,lb,color):
    ax1.axvspan(la, lb,alpha=0.6, color=color)
    return ax1
    
def shade1(la,lb,color):
    ax1.axvspan(la, lb,alpha=0.6, color=color, fill=False,linewidth=3)
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
l1a=-39.1; l1b=-38.6
l2a=-38.4; l2b=-37.2
l3a=-35.1; l3b=-34.5
l4a=-31.6; l4b=-30.9
l5a=-28.600000000000005; l5b=-27.9  #this was a stupid formating thing, since it is not -28.6
l6a=-27.6; l6b=-26.7
l7a=-41.6; l7b=-40.5
l8a=-38.2; l8b=-36.6
l9a=-21.3; l9b=-19.9
l10a=-39.4; l10b=-37.7
l11a=-35.5; l11b=-34.5
l12a=-12.3; l12b=-10.9
l13a=-38;   l13b=-36
l14a=-35.7; l14b=-35.2
l15a=-29.6; l15b=-28.9
l16a=-11;   l16b=-10.4

#other old events
#l1a=-42.2; l1b=-41.0
#l4a=-36.3; l4b=-35.3
#l10a=-39.6; l10b=-38.3
#l15a=-19.8; l15b=-18.3
#l16a=-13.6; l16b=-12.4
#l20a=-32.8; l20b=-31.9
########################
#PLOT                  #-------------------
########################
gs = gridspec.GridSpec(3, 4,
                       width_ratios=[1,1,1,1],
                       height_ratios=[1,1,1]
                       )
gs.update(hspace=0)
gs.update(wspace=0.05)

#colors
a='red'
b='indigo'
c='darkorange'
d='darkgrey'

#2012 northbount
fig = plt.figure()
ax1 = plt.subplot(gs[0])
ax1=plot_lat(lat1n,co2_1n,co2_1ng,ylab='CO2 (ppm)',tit='NB 2012')
shade(l1a,l1b,a);shade1(l2a,l2b,b); shade(l3a,l3b,a);shade(l4a,l4b,a);shade(l5a,l5b,a);shade(l6a,l6b,a)
text(l1a,l1b,'1');text(l2a,l2b,'2');text(l3a,l3b,'3');text(l4a,l4b,'4');text(l5a,l5b,'5');text(l6a,l6b,'6')

ax1 = plt.subplot(gs[4])
ax1=plot_lat(lat1n,ch4_1n,ch4_1ng,ylab='CH4 (ppb)',tit='')
shade(l1a,l1b,a);shade(l3a,l3b,a);shade(l4a,l4b,a);shade(l5a,l5b,a);shade(l6a,l6b,a)

ax1 = plt.subplot(gs[8])
ax1=plot_lat(lat1n,co_1n,co_1ng,ylab='CO (ppb)',tit='')
shade(l1a,l1b,a);shade1(l2a,l2b,b); shade(l3a,l3b,a);shade(l4a,l4b,a);shade(l5a,l5b,a);shade(l6a,l6b,a)

#2012 southbound
ax1 = plt.subplot(gs[1])
ax1=plot_lat(lat1s,co2_1s,co2_1sg,ylab='CO2 (ppm) ',tit='SB 2012')
shade(l8a,l8b,a);shade(l9a,l9b,a)
text(l8a,l8b,'8');text(l9a,l9b,'9')

ax1 = plt.subplot(gs[5])
ax1=plot_lat(lat1s,ch4_1s,ch4_1sg,ylab='CH4 (ppb) ',tit='')
shade(l7a,l7b,c);shade(l8a,l8b,a);shade1(l9a,l9b,a)
text(l7a,l7b,'7')

ax1 = plt.subplot(gs[9])
ax1=plot_lat(lat1s,co_1s,co_1sg,ylab='CO (ppb) ',tit='')
shade(l7a,l7b,c);shade(l8a,l8b,a);shade(l9a,l9b,a)

#2013 northbound
ax1 = plt.subplot(gs[2])
ax1=plot_lat(lat2n,co2_2n,co2_2ng,ylab='CO2 (ppm) ',tit='NB 2013')
shade(l11a,l11b,a);
text(l11a,l11b,'11')

ax1 = plt.subplot(gs[6])
ax1=plot_lat(lat2n,ch4_2n,ch4_2ng,ylab='CH4 (ppb) ',tit='')
shade(l10a,l10b,c);shade(l12a,l12b,c);shade(l11a,l11b,a);
text(l10a,l10b,'10');text(l12a,l12b,'12')

ax1 = plt.subplot(gs[10])
ax1=plot_lat(lat2n,co_2n,co_2ng,ylab='CO (ppb) ',tit='')
shade(l10a,l10b,c);shade(l12a,l12b,c);shade(l11a,l11b,a);

#2013 southbound
ax1 = plt.subplot(gs[3])
ax1=plot_lat(lat2s,co2_2s,co2_2sg,ylab='CO2 (ppm) ',tit='SB 2013')
shade(l15a,l15b,d);shade(l16a,l16b,a)
text(l15a,l15b,'15');text(l16a,l16b,'16')

ax1 = plt.subplot(gs[7])
ax1=plot_lat(lat2s,ch4_2s,ch4_2sg,ylab='CH4 (ppb) ',tit='')
shade1(l13a,l13b,c);shade(l14a,l14b,c); shade(l15a,l15b,d) ;shade(l16a,l16b,a)
text(l13a,l13b,'13');text(l14a,l14b,'14')

ax1 = plt.subplot(gs[11])
ax1=plot_lat(lat2s,co_2s,co_2sg,ylab='CO (ppb) ',tit='')
shade1(l13a,l13b,c);shade(l14a,l14b,c);shade(l16a,l16b,a)

#############################################################
#RATIOS OF THE REALTIVE ENHANCEMENTS SEPPERATE  OR COMBINED #-------------------
#############################################################
#relative change,basically the individual - the minimum of that traces, that way I wont have negative values

#SEPPARATE - ratios_sep function
#COMBINED - ratioss_com function with 1:1 line

############################################################
#RATIOS OF THE REALTIVE ENHANCEMENTS COMBINED              #-------------------
############################################################

#all three
event1,sl_coch41,sl_co2ch41,sl_co2co1=ratios.ratios_com(l1a,l1b,lat1n,co2_1n,ch4_1n,co_1n,co2_1ng,ch4_1ng,co_1ng,ev='Event 1')
event3,sl_coch43,sl_co2ch43,sl_co2co3=ratios.ratios_com(l3a,l3b,lat1n,co2_1n,ch4_1n,co_1n,co2_1ng,ch4_1ng,co_1ng,ev='Event 3')
event4,sl_coch44,sl_co2ch44,sl_co2co4=ratios.ratios_com(l4a,l4b,lat1n,co2_1n,ch4_1n,co_1n,co2_1ng,ch4_1ng,co_1ng,ev='Event 4')
event5,sl_coch45,sl_co2ch45,sl_co2co5=ratios.ratios_com(l5a,l5b,lat1n,co2_1n,ch4_1n,co_1n,co2_1ng,ch4_1ng,co_1ng,ev='Event 5')
event6,sl_coch46,sl_co2ch46,sl_co2co6=ratios.ratios_com(l6a,l6b,lat1n,co2_1n,ch4_1n,co_1n,co2_1ng,ch4_1ng,co_1ng,ev='Event 6')
event8,sl_coch48,sl_co2ch48,sl_co2co8=ratios.ratios_com(l8a,l8b,lat1s,co2_1s,ch4_1s,co_1s,co2_1sg,ch4_1sg,co_1sg,ev='Event 8')
event9,sl_coch49,sl_co2ch49,sl_co2co9=ratios.ratios_com(l9a,l9b,lat1s,co2_1s,ch4_1s,co_1s,co2_1sg,ch4_1sg,co_1sg,ev='Event 9')
event11,sl_coch411,sl_co2ch411,sl_co2co11=ratios.ratios_com(l12a,l12b,lat2n,co2_2n,ch4_2n,co_2n,co2_2ng,ch4_2ng,co_2ng,ev='Event 11')
event16,sl_coch416,sl_co2ch416,sl_co2co16=ratios.ratios_com(l16a,l16b,lat2s,co2_2s,ch4_2s,co_2s,co2_2sg,ch4_2sg,co_2sg,ev='Event 16')
#ch4_co
event7,sl_coch47=ratios.ratios_com(l7a,l7b,lat1s,co2_1s,ch4_1s,co_1s,co2_1sg,ch4_1sg,co_1sg,ev='Event 7')
event10,sl_coch410=ratios.ratios_com(l10a,l10b,lat2n,co2_2n,ch4_2n,co_2n,co2_2ng,ch4_2ng,co_2ng,ev='Event 10')
event12,sl_coch412=ratios.ratios_com(l12a,l12b,lat2n,co2_2n,ch4_2n,co_2n,co2_2ng,ch4_2ng,co_2ng,ev='Event 12')
event13,sl_coch413=ratios.ratios_com(l13a,l13b,lat2s,co2_2s,ch4_2s,co_2s,co2_2sg,ch4_2sg,co_2sg,ev='Event 13')
event14,sl_coch414=ratios.ratios_com(l14a,l14b,lat2s,co2_2s,ch4_2s,co_2s,co2_2sg,ch4_2sg,co_2sg,ev='Event 14')
#co_co2
event2,sl_co2co2=ratios.ratios_com(l2a,l2b,lat1n,co2_1n,ch4_1n,co_1n,co2_1ng,ch4_1ng,co_1ng,ev='Event 2')
#ch4_co2
event15,sl_co2ch415=ratios.ratios_com(l15a,l15b,lat2s,co2_2s,ch4_2s,co_2s,co2_2sg,ch4_2sg,co_2sg,ev='Event 15')

#Calculate the median emission ratio
#ch4_co
ch4_co=np.array([sl_coch41,sl_coch43,sl_coch44,sl_coch45,sl_coch46,sl_coch48,sl_coch49,sl_coch411,sl_coch416,\
                 sl_coch47,sl_coch410,sl_coch412,sl_coch413,sl_coch414])
ch4_co_avg=np.median(ch4_co)

#co_co2
co_co2=np.array([sl_co2co1,sl_co2co3,sl_co2co4,sl_co2co5,sl_co2co6,sl_co2co8,sl_co2co9,sl_co2co11,sl_co2co16,\
                 sl_co2co2])
co_co2_avg=np.median(co_co2)

#ch4_co2        plt.plot(x_lim,x_avg*x_lim,color='goldenrod',linestyle='dashed',linewidth=3) #linear regression line
co2_ch4=np.array([sl_co2ch41,sl_co2ch43,sl_co2ch44,sl_co2ch45,sl_co2ch46,sl_co2ch48,sl_co2ch49,sl_co2ch411,sl_co2ch416,\
                 sl_co2ch415])
co2_ch4_avg=np.median(co2_ch4)

#now do it again but this time add the avergae emission ratio (slope) to the plot instead the 1:1 line
#all three
#return co_ch4,co2_ch4,co2_co
ev1=ratios.ratios_com_avg(l1a,l1b,lat1n,co2_1n,ch4_1n,co_1n,co2_1ng,ch4_1ng,co_1ng,ch4_co_avg,co_co2_avg,co2_ch4_avg,ev='Event 1')
ev3=ratios.ratios_com_avg(l3a,l3b,lat1n,co2_1n,ch4_1n,co_1n,co2_1ng,ch4_1ng,co_1ng,ch4_co_avg,co_co2_avg,co2_ch4_avg,ev='Event 3')
ev4=ratios.ratios_com_avg(l4a,l4b,lat1n,co2_1n,ch4_1n,co_1n,co2_1ng,ch4_1ng,co_1ng,ch4_co_avg,co_co2_avg,co2_ch4_avg,ev='Event 4')
ev5=ratios.ratios_com_avg(l5a,l5b,lat1n,co2_1n,ch4_1n,co_1n,co2_1ng,ch4_1ng,co_1ng,ch4_co_avg,co_co2_avg,co2_ch4_avg,ev='Event 5')
ev6=ratios.ratios_com_avg(l6a,l6b,lat1n,co2_1n,ch4_1n,co_1n,co2_1ng,ch4_1ng,co_1ng,ch4_co_avg,co_co2_avg,co2_ch4_avg,ev='Event 6')
ev8=ratios.ratios_com_avg(l8a,l8b,lat1s,co2_1s,ch4_1s,co_1s,co2_1sg,ch4_1sg,co_1sg,ch4_co_avg,co_co2_avg,co2_ch4_avg,ev='Event 8')
ev9=ratios.ratios_com_avg(l9a,l9b,lat1s,co2_1s,ch4_1s,co_1s,co2_1sg,ch4_1sg,co_1sg,ch4_co_avg,co_co2_avg,co2_ch4_avg,ev='Event 9')
ev11=ratios.ratios_com_avg(l11a,l11b,lat2n,co2_2n,ch4_2n,co_2n,co2_2ng,ch4_2ng,co_2ng,ch4_co_avg,co_co2_avg,co2_ch4_avg,ev='Event 11')
ev16=ratios.ratios_com_avg(l16a,l16b,lat2s,co2_2s,ch4_2s,co_2s,co2_2sg,ch4_2sg,co_2sg,ch4_co_avg,co_co2_avg,co2_ch4_avg,ev='Event 16')
#ch4_co
ev7=ratios.ratios_com_avg(l7a,l7b,lat1s,co2_1s,ch4_1s,co_1s,co2_1sg,ch4_1sg,co_1sg,ch4_co_avg,co_co2_avg,co2_ch4_avg,ev='Event 7')
ev10=ratios.ratios_com_avg(l10a,l10b,lat2n,co2_2n,ch4_2n,co_2n,co2_2ng,ch4_2ng,co_2ng,ch4_co_avg,co_co2_avg,co2_ch4_avg,ev='Event 10')
ev12=ratios.ratios_com_avg(l12a,l12b,lat2n,co2_2n,ch4_2n,co_2n,co2_2ng,ch4_2ng,co_2ng,ch4_co_avg,co_co2_avg,co2_ch4_avg,ev='Event 12')
ev13=ratios.ratios_com_avg(l13a,l13b,lat2s,co2_2s,ch4_2s,co_2s,co2_2sg,ch4_2sg,co_2sg,ch4_co_avg,co_co2_avg,co2_ch4_avg,ev='Event 13')
ev14=ratios.ratios_com_avg(l14a,l14b,lat2s,co2_2s,ch4_2s,co_2s,co2_2sg,ch4_2sg,co_2sg,ch4_co_avg,co_co2_avg,co2_ch4_avg,ev='Event 14')
#co_co2
ev2=ratios.ratios_com_avg(l2a,l2b,lat1n,co2_1n,ch4_1n,co_1n,co2_1ng,ch4_1ng,co_1ng,ch4_co_avg,co_co2_avg,co2_ch4_avg,ev='Event 2')
#ch4_co2
ev15=ratios.ratios_com_avg(l15a,l15b,lat2s,co2_2s,ch4_2s,co_2s,co2_2sg,ch4_2sg,co_2sg,ch4_co_avg,co_co2_avg,co2_ch4_avg,ev='Event 15')

#########################
#CORREALTION W TRACERS  #------------------------------------------------------
#########################

#with TOTAL MODEL
def rel_lim(lim1,lim2,lat,x_meas, x_mod,x_trac,ev,sp):
    #tracers varaible is in a weird shape after averaging so extract the tracers only
    x_t=[]
    for i in range(len(x_trac)):
        x_t.append(x_trac[i][1])    
    #calculate the realtive change
    #measurement, model total and tracers 
    xr,xgr,xtr=mean.mean_var(x_meas,x_mod,x_t,mean='N',sp=sp)
    #The indicise that correspond to the limits values
    l1ai=np.where(lat==lim1)[0]; l1bi=np.where(lat==lim2)[0]
    #select the values that correspond to the indicies
    x_i=xr[l1ai[0]:l1bi[0]]
    x_gi=xgr[l1ai[0]:l1bi[0]]
    x_ti=[]
    for i in range(len(xtr)):
        x_ti.append(xtr[i][l1ai[0]:l1bi[0]])
    #After I calculated the rel value and selected the values I need
    #I need 3 thigs for the plots
    #1. r, p-value and std
    #slope, intercept, r, p, std_err
    stat_t=[]
    for i in range(len(x_ti)):
        stat_t.append(stats.linregress(x_gi,x_ti[i])) #meaurements all the tracers
    #std
    enh_meas=max(x_i) - min(x_i)
    enh_mod=max(x_gi) - min(x_gi)
    enh_t=[]
    for i in range(len(x_ti)):
        enh_t.append(max(x_ti[i]) - min(x_ti[i])) #meaurements all the tracers
    return stat_t,enh_meas,enh_mod,enh_t,ev


#co2
stat1_co2=rel_lim(l1a,l1b,lat1n,co2_1n,co2_1ng,co2_t_1ng,'Event 1','CO2')
stat2_co2=rel_lim(l2a,l2b,lat1n,co2_1n,co2_1ng,co2_t_1ng,'Event 2','CO2')
stat3_co2=rel_lim(l3a,l3b,lat1n,co2_1n,co2_1ng,co2_t_1ng,'Event 3','CO2')
stat4_co2=rel_lim(l4a,l4b,lat1n,co2_1n,co2_1ng,co2_t_1ng,'Event 4','CO2')
stat5_co2=rel_lim(l5a,l5b,lat1n,co2_1n,co2_1ng,co2_t_1ng,'Event 5','CO2')
stat6_co2=rel_lim(l6a,l6b,lat1n,co2_1n,co2_1ng,co2_t_1ng,'Event 6','CO2')
stat8_co2=rel_lim(l8a,l8b,lat1s,co2_1s,co2_1sg,co2_t_1sg,'Event 8','CO2')
stat9_co2=rel_lim(l9a,l9b,lat1s,co2_1s,co2_1sg,co2_t_1sg,'Event 9','CO2')
stat11_co2=rel_lim(l11a,l11b,lat2n,co2_2n,co2_2ng,co2_t_2ng,'Event 11','CO2')
stat15_co2=rel_lim(l15a,l15b,lat2s,co2_2s,co2_2sg,co2_t_2sg,'Event 15','CO2')
stat16_co2=rel_lim(l16a,l16b,lat2s,co2_2s,co2_2sg,co2_t_2sg,'Event 16','CO2')

stat_co2=np.array([stat1_co2,stat2_co2,stat3_co2,stat4_co2,stat5_co2,stat6_co2,stat8_co2,stat9_co2,stat11_co2,stat15_co2,stat16_co2])

#co
stat1_co= rel_lim(l1a,l1b,lat1n,co_1n,  co_1ng,co_t_1ng,'Event 1','CO')
stat2_co= rel_lim(l2a,l2b,lat1n,co_1n,  co_1ng,co_t_1ng,'Event 2','CO')
stat3_co= rel_lim(l3a,l3b,lat1n,co_1n,  co_1ng,co_t_1ng,'Event 3','CO')
stat4_co= rel_lim(l4a,l4b,lat1n,co_1n,  co_1ng,co_t_1ng,'Event 4','CO')
stat5_co= rel_lim(l5a,l5b,lat1n,co_1n,  co_1ng,co_t_1ng,'Event 5','CO')
stat6_co= rel_lim(l6a,l6b,lat1n,co_1n,  co_1ng,co_t_1ng,'Event 6','CO')
stat7_co= rel_lim(l7a,l7b,lat1s,co_1n,  co_1sg, co_t_1sg,'Event 7','CO')
stat8_co= rel_lim(l8a,l8b,lat1s,co_1s,  co_1sg, co_t_1sg,'Event 8','CO')
stat9_co= rel_lim(l9a,l9b,lat1s,co_1s,   co_1sg, co_t_1sg,'Event 9','CO')
stat10_co= rel_lim(l10a,l10b,lat2n,co_2n, co_2ng, co_t_2ng,'Event 10','CO')
stat11_co= rel_lim(l11a,l11b,lat2n,co_2n, co_2ng, co_t_2ng,'Event 11','CO')
stat12_co= rel_lim(l12a,l12b,lat2n,co_2n, co_2ng, co_t_2ng,'Event 12','CO')
stat13_co= rel_lim(l13a,l13b,lat2s,co_2s, co_2sg, co_t_2sg,'Event 13','CO')
stat14_co= rel_lim(l14a,l14b,lat2s,co_2s, co_2sg, co_t_2sg,'Event 14','CO')
stat16_co= rel_lim(l16a,l16b,lat2s,co_2s, co_2sg, co_t_2sg,'Event 16','CO')

stat_co=np.array([stat1_co,stat2_co,stat3_co,stat4_co,stat5_co,stat6_co,stat7_co,stat8_co,stat9_co,stat10_co,stat11_co,stat12_co,stat13_co,stat14_co,stat16_co])

#ch4
stat1_ch4=rel_lim(l1a,l1b,lat1n,ch4_1n,ch4_1ng,ch4_t_1ng,'Event 1','CH4')
stat3_ch4=rel_lim(l3a,l3b,lat1n,ch4_1n,ch4_1ng,ch4_t_1ng,'Event 3','CH4')
stat4_ch4=rel_lim(l4a,l4b,lat1n,ch4_1n,ch4_1ng,ch4_t_1ng,'Event 4','CH4')
stat5_ch4=rel_lim(l5a,l5b,lat1n,ch4_1n,ch4_1ng,ch4_t_1ng,'Event 5','CH4')
stat6_ch4=rel_lim(l6a,l6b,lat1n,ch4_1n,ch4_1ng,ch4_t_1ng,'Event 6','CH4')
stat7_ch4=rel_lim(l7a,l7b,lat1s,ch4_1s,ch4_1sg, ch4_t_1sg,'Event 7','CH4')
stat8_ch4=rel_lim(l8a,l8b,lat1s,ch4_1s,ch4_1sg, ch4_t_1sg,'Event 8','CH4')
stat9_ch4=rel_lim(l9a,l9b,lat1s,ch4_1s,ch4_1sg, ch4_t_1sg,'Event 9','CH4')
stat10_ch4=rel_lim(l10a,l10b,lat2n,ch4_2n, ch4_2ng, ch4_t_2ng,'Event 10','CH4')
stat11_ch4=rel_lim(l11a,l11b,lat2n,ch4_2n, ch4_2ng, ch4_t_2ng,'Event 11','CH4')
stat12_ch4=rel_lim(l12a,l12b,lat2n,ch4_2n, ch4_2ng, ch4_t_2ng,'Event 12','CH4')
stat13_ch4=rel_lim(l13a,l13b,lat2s,ch4_2s, ch4_2sg, ch4_t_2sg,'Event 13','CH4')
stat14_ch4=rel_lim(l14a,l14b,lat2s,ch4_2s, ch4_2sg, ch4_t_2sg,'Event 14','CH4')
stat15_ch4=rel_lim(l15a,l15b,lat2s,ch4_2s, ch4_2sg,ch4_t_2sg, 'Event 15','CH4')
stat16_ch4=rel_lim(l16a,l16b,lat2s,ch4_2s, ch4_2sg, ch4_t_2sg,'Event 16','CH4')

stat_ch4=np.array([stat1_ch4,stat3_ch4,stat4_ch4,stat5_ch4,stat6_ch4,stat7_ch4,stat8_ch4,stat9_ch4,stat10_ch4,stat11_ch4,stat12_ch4,stat13_ch4,stat14_ch4,stat15_ch4,stat16_ch4])

def taylor_plot(stat,lc,n1,n2,n3,tit,sp):
    # Reference std of the measurements
    stdrefs = dict(event=stat[2])
    # Sample std,r,p,lable&color: Be sure to check order and that correct numbers are placed!    
    if sp=='CO':
        samples = dict(event=[ [stat[-2][0], stat[0][0][2],stat[0][0][3], lc[2][0]],
                               [stat[-2][1], stat[0][1][2],stat[0][1][3], lc[3][0]],
                               [stat[-2][2], stat[0][2][2],stat[0][2][3], lc[4][0]],
                               [stat[-2][3], stat[0][3][2],stat[0][3][3], lc[5][0]],
                               [stat[-2][4], stat[0][4][2],stat[0][4][3], lc[6][0]],
                               [stat[-2][5], stat[0][5][2],stat[0][5][3], lc[7][0]],
                               [stat[-2][6], stat[0][6][2],stat[0][6][3], lc[8][0]],
                               [stat[-2][7], stat[0][7][2],stat[0][7][3], lc[9][0]],
                               [stat[-2][8], stat[0][8][2],stat[0][8][3], lc[10][0]],
                               [stat[-2][9], stat[0][9][2],stat[0][9][3], lc[11][0]],
                               [stat[-2][10], stat[0][10][2],stat[0][10][3], lc[12][0]],
                               [stat[-2][11], stat[0][11][2],stat[0][11][3], lc[13][0]]])
    else:
        samples = dict(event=[ [stat[-2][0], stat[0][0][2],stat[0][0][3], lc[2][0]],
                               [stat[-2][1], stat[0][1][2],stat[0][1][3], lc[3][0]],
                               [stat[-2][2], stat[0][2][2],stat[0][2][3], lc[4][0]],
                               [stat[-2][3], stat[0][3][2],stat[0][3][3], lc[5][0]],
                               [stat[-2][4], stat[0][4][2],stat[0][4][3], lc[6][0]],
                               [stat[-2][5], stat[0][5][2],stat[0][5][3], lc[7][0]],
                               [stat[-2][6], stat[0][6][2],stat[0][6][3], lc[8][0]],
                               [stat[-2][7], stat[0][7][2],stat[0][7][3], lc[9][0]],
                               [stat[-2][8], stat[0][8][2],stat[0][8][3], lc[10][0]],
                               [stat[-2][9], stat[0][9][2],stat[0][9][3], lc[11][0]],
                               [stat[-2][10], stat[0][10][2],stat[0][10][3], lc[12][0]]])
    fig.suptitle(sp, size='x-large')    
    dia = TaylorDiagram(stdrefs['event'], fig=fig, r1=n1,r2=n2,r3=n3,
                        label=lc[0][0])
       
    #dia.ax.plot(x95,y95,color='r')
    # Add samples to Taylor diagram
    for i,(stddev,corrcoef,p_val,name) in enumerate(samples['event']):
        if p_val<=0.05:
            dia.add_sample(stddev, corrcoef,
                           marker='$%d$' % (i+2), ms=10, ls='',
                           #mfc='k', mec='k', # B&W
                           mfc='black', mec='black', # mec=lc[i+1][1], # Colors
                           label=name)
        else:
            dia.add_sample(stddev, corrcoef,
                   marker='$%d$' % (i+2), ms=10, ls='',
                   #mfc='k', mec='k', # B&W
                   mfc='red', mec='red', # Colors
                   label=name)
    
    # Add RMS contours, and label them
    #contours = dia.add_contours(levels=5, colors='0.5') # 5 levels
    #dia.ax.clabel(contours, inline=1, fontsize=10, fmt='%.1f')
    dia.add_grid(color='r')
    dia._ax.set_title(tit.capitalize())
    fig.legend(dia.samplePoints,
               [ p.get_label() for p in dia.samplePoints ],
               numpoints=1, prop=dict(size='small'), loc='center right')
    #fig.tight_layout()
    plt.show()
    return plt


#for all 16 events    
fig = plt.figure(figsize=(15,8))   
plt.subplots_adjust(left=0.02,right=0.95)
for i in range(len(stat_co2)): 
    taylor_plot(stat_co2[i],lab_col_co2,2,6,i+1,stat_co2[i][-1],'CO2')
plt.text(stat_co2[-1][1]+0.5,stat_co2[-1][1], r'$p \leq 0.05$',fontsize=20,fontweight='bold',color='black')
plt.text(stat_co2[-1][1]+0.5,stat_co2[-1][1]-0.1, r'$p > 0.05$',fontsize=20,fontweight='bold',color='red')

#for all 16 events    
fig = plt.figure(figsize=(15,8))   
plt.subplots_adjust(left=0.02,right=0.95)
for i in range(len(stat_co)): 
    taylor_plot(stat_co[i],lab_col_co,2,8,i+1,stat_co[i][-1],'CO')
plt.text(stat_co[-1][1]+0.5,stat_co[-1][1], r'$p \leq 0.05$',fontsize=20,fontweight='bold',color='black')
plt.text(stat_co[-1][1]+0.5,stat_co[-1][1]-0.1, r'$p > 0.05$',fontsize=20,fontweight='bold',color='red')

#for all 16 events    
fig = plt.figure(figsize=(15,8))   
plt.subplots_adjust(left=0.02,right=0.95)
for i in range(len(stat_ch4)): 
    taylor_plot(stat_ch4[i],lab_col_ch4,2,8,i+1,stat_ch4[i][-1],'CH4')
plt.text(stat_ch4[-1][1]+0.5,stat_ch4[-1][1], r'$p \leq 0.05$',fontsize=20,fontweight='bold',color='black')
plt.text(stat_ch4[-1][1]+0.5,stat_ch4[-1][1]-0.1, r'$p > 0.05$',fontsize=20,fontweight='bold',color='red')

#########################
#PLOT ALL               #------------------------------------------------------
#########################
#plot all the emission ratios on 1 plot, find a smarter way to pull ou the raitos
#2D values, events vs ratios vs standard error vs R2
#Measurements
ch4_co=np.array([[1,3,4,5,6,8,9,11,16,7,10,12,13,14],\
                 [ev1[1][0],ev3[1][0],ev4[1][0],ev5[1][0],ev6[1][0],ev8[1][0],ev9[1][0],ev11[1][0],ev16[1][0],ev7[1][0],ev10[1][0],ev12[1][0],ev13[1][0],ev14[1][0]],\
                 [ev1[1][-1],ev3[1][-1],ev4[1][-1],ev5[1][-1],ev6[1][-1],ev8[1][-1],ev9[1][-1],ev11[1][-1],ev16[1][-1],ev7[1][-1],ev1[1][-1],ev12[1][-1],ev13[1][-1],ev14[1][-1]],\
                 [ev1[1][2]**2,ev3[1][2]**2,ev4[1][2]**2,ev5[1][2]**2,ev6[1][2]**2,ev8[1][2]**2,ev9[1][2]**2,ev11[1][2]**2,ev16[1][2]**2,ev7[1][2]**2,ev12[1][2]**2,ev12[1][2]**2,ev13[1][2]**2,ev14[1][2]**2]])
ch4_co2=np.array([[1,3,4,5,6,8,9,11,16,15],\
                  [ev1[3][0],ev3[3][0],ev4[3][0],ev5[3][0],ev6[3][0],ev8[3][0],ev9[3][0],ev11[3][0],ev16[3][0],ev15[1][0]],\
                  [ev1[3][-1],ev3[3][-1],ev4[3][-1],ev5[3][-1],ev6[3][-1],ev8[3][-1],ev9[3][-1],ev11[3][-1],ev16[3][-1],ev15[1][-1]],\
                  [ev1[3][2]**2,ev3[3][2]**2,ev4[3][2]**2,ev5[3][2]**2,ev6[3][2]**2,ev8[3][2]**2,ev9[3][2]**2,ev11[3][2]**2,ev16[3][2]**2,ev15[1][2]**2]])
co_co2=np.array([[1,3,4,5,6,8,9,11,16,2],\
                 [ev1[5][0],ev3[5][0],ev4[5][0],ev5[5][0],ev6[5][0],ev8[5][0],ev9[5][0],ev11[5][0],ev16[5][0],ev2[1][0]],\
                 [ev1[5][-1],ev3[5][-1],ev4[5][-1],ev5[5][-1],ev6[5][-1],ev8[5][-1],ev9[5][-1],ev11[5][-1],ev16[5][-1],ev2[1][-1]],\
                 [ev1[5][2]**2,ev3[5][2]**2,ev4[5][2]**2,ev5[5][2]**2,ev6[5][2]**2,ev8[5][2]**2,ev9[5][2]**2,ev11[5][2]**2,ev16[5][2]**2,ev2[1][2]**2]])

#model total
ch4_cog=np.array([[1,3,4,5,6,8,9,11,16,7,10,12,13,14],\
                 [ev1[2][0],ev3[2][0],ev4[2][0],ev5[2][0],ev6[2][0],ev8[2][0],np.nan,ev11[2][0],ev16[2][0],ev7[2][0],ev10[2][0],ev12[2][0],np.nan,ev14[2][0]],\
                 [ev1[2][-1],ev3[2][-1],ev4[2][-1],ev5[2][-1],ev6[2][-1],ev8[2][-1],np.nan,ev11[2][-1],ev16[2][-1],ev7[2][-1],ev1[2][-1],ev12[2][-1],np.nan,ev14[2][-1]],\
                 [ev1[2][2]**2,ev3[2][2]**2,ev4[2][2]**2,ev5[2][2]**2,ev6[2][2]**2,ev8[2][2]**2,np.nan,ev11[2][2]**2,ev16[2][2]**2,ev7[2][2]**2,ev12[2][2]**2,ev12[2][2]**2,np.nan,ev14[2][2]]])
ch4_co2g=np.array([[1,3,4,5,6,8,9,11,16,15],\
                  [ev1[4][0],ev3[4][0],ev4[4][0],ev5[4][0],ev6[4][0],ev8[4][0],np.nan,ev11[4][0],ev16[4][0],ev15[2][0]],\
                  [ev1[4][-1],ev3[4][-1],ev4[4][-1],ev5[4][-1],ev6[4][-1],ev8[4][-1],np.nan,ev11[4][-1],ev16[4][-1],ev15[2][-1]],\
                  [ev1[4][2]**2,ev3[4][2]**2,ev4[4][2]**2,ev5[4][2]**2,ev6[4][2]**2,ev8[4][2]**2,np.nan,ev11[4][2]**2,ev16[4][2]**2,ev15[2][2]**2]])
co_co2g=np.array([[1,3,4,5,6,8,9,11,16,2],\
                 [ev1[6][0],ev3[6][0],ev4[6][0],ev5[6][0],ev6[6][0],ev8[6][0],ev9[6][0],ev11[6][0],ev16[6][0],np.nan],\
                 [ev1[6][-1],ev3[6][-1],ev4[6][-1],ev5[6][-1],ev6[6][-1],ev8[6][-1],ev9[6][-1],ev11[6][-1],ev16[6][-1],np.nan],\
                 [ev1[6][2]**2,ev3[6][2]**2,ev4[6][2]**2,ev5[6][2]**2,ev6[6][2]**2,ev8[6][2]**2,ev9[6][2]**2,ev11[6][2]**2,ev16[6][2]**2,np.nan]])

#total measurement enhancement ch4 and co
ch4_co_meas=np.array([[1,3,4,5,6,8,9,11,16,7,10,12,13,14],\
                 [stat1_ch4[1],stat3_ch4[1],stat4_ch4[1],stat5_ch4[1],stat6_ch4[1],stat8_ch4[1],stat9_ch4[1],stat11_ch4[1],stat16_ch4[1],stat7_ch4[1],stat10_ch4[1],stat12_ch4[1],stat13_ch4[1],stat14_ch4[1]],\
                 [stat1_co[1],stat3_co[1],stat4_co[1],stat5_co[1],stat6_co[1],stat8_co[1],stat9_co[1],stat11_co[1],stat16_co[1],stat7_co[1],stat10_co[1],stat12_co[1],stat13_co[1],stat14_co[1]]])

ch4_co2_meas=np.array([[1,3,4,5,6,8,9,11,16,15],\
                 [stat1_ch4[1],stat3_ch4[1],stat4_ch4[1],stat5_ch4[1],stat6_ch4[1],stat8_ch4[1],stat9_ch4[1],stat11_ch4[1],stat16_ch4[1],stat15_ch4[1]],\
                 [stat1_co2[1],stat3_co2[1],stat4_co2[1],stat5_co2[1],stat6_co2[1],stat8_co2[1],stat9_co2[1],stat11_co2[1],stat16_co2[1],stat15_co2[1]]])

co_co2_meas=np.array([[1,3,4,5,6,8,9,11,16,2],\
                 [stat1_co[1],stat3_co[1],stat4_co[1],stat5_co[1],stat6_co[1],stat8_co[1],stat9_co[1],stat11_co[1],stat16_co[1],stat2_co[1]],\
                 [stat1_co2[1],stat3_co2[1],stat4_co2[1],stat5_co2[1],stat6_co2[1],stat8_co2[1],stat9_co2[1],stat11_co2[1],stat16_co2[1],stat2_co2[1]]])

#total model enhancement ch4 and co
ch4_co_mod=np.array([[1,3,4,5,6,8,9,11,16,7,10,12,13,14],\
                 [stat1_ch4[2],stat3_ch4[2],stat4_ch4[2],stat5_ch4[2],stat6_ch4[2],stat8_ch4[2],np.nan,stat11_ch4[2],stat16_ch4[2],stat7_ch4[2],stat10_ch4[2],stat12_ch4[2],np.nan,stat14_ch4[2]],\
                 [stat1_co[2],stat3_co[2],stat4_co[2],stat5_co[2],stat6_co[2],stat8_co[2],stat9_co[2],stat11_co[2],stat16_co[2],stat7_co[2],stat10_co[2],stat12_co[2],np.nan,stat14_co[2]]])

ch4_co2_mod=np.array([[1,3,4,5,6,8,9,11,16,15],\
                 [stat1_ch4[2],stat3_ch4[2],stat4_ch4[2],stat5_ch4[2],stat6_ch4[2],stat8_ch4[2],np.nan,stat11_ch4[2],stat16_ch4[2],stat15_ch4[2]],\
                 [stat1_co2[2],stat3_co2[2],stat4_co2[2],stat5_co2[2],stat6_co2[2],stat8_co2[2],stat9_co2[2],stat11_co2[2],stat16_co2[2],stat15_co2[2]]])

co_co2_mod=np.array([[1,3,4,5,6,8,9,11,16,2],\
                 [stat1_co[2],stat3_co[2],stat4_co[2],stat5_co[2],stat6_co[2],stat8_co[2],stat9_co[2],stat11_co[2],stat16_co[2],np.nan],\
                 [stat1_co2[2],stat3_co2[2],stat4_co2[2],stat5_co2[2],stat6_co2[2],stat8_co2[2],stat9_co2[2],stat11_co2[2],stat16_co2[2],np.nan]])

#This is done by eye based on the Taylor diagrams!
#ALL THE EVENTS WHEN I HAVE EMISSIONS, AND TRACERS THAT CORRESPODENT TO THE EVENT
#Event, Tracer, color, enhancement, r

#ch4_og,ch4_cm,ch4_ls,ch4_wa,ch4_bf,ch4_ri,ch4_an,ch4_bb,ch4_we,ch4_sa,ch4_nat, name number -2
ch4_trac= dict(ev1=[[1,"10 Wet",lab_col_ch4[10][1],stat1_ch4[3][8], stat1_ch4[0][8][2]],  [1,"5 Wa",lab_col_ch4[5][1],   stat1_ch4[3][3], stat1_ch4[0][3][2]]],
               ev3=[[3,"3 Cm",lab_col_ch4[3][1],   stat3_ch4[3][1], stat3_ch4[0][1][2]],  [3,"4 Ls",lab_col_ch4[4][1],   stat3_ch4[3][2], stat3_ch4[0][2][2]], [3,"5 Wa",lab_col_ch4[5][1], stat3_ch4[3][3], stat3_ch4[0][3][2]]],
               ev4=[[4,"10 Wet",lab_col_ch4[10][1],stat4_ch4[3][8], stat4_ch4[0][8][2]],  [4,"3 Cm",lab_col_ch4[3][1],   stat4_ch4[3][1], stat4_ch4[0][1][2]], [4,"4 Ls",lab_col_ch4[4][1],stat4_ch4[3][2], stat4_ch4[0][2][2]]],
               ev5=[[5,"4 Ls",lab_col_ch4[4][1],  stat5_ch4[3][2], stat5_ch4[0][2][2]]],
               ev6=[[6,"4 Ls",lab_col_ch4[4][1],  stat6_ch4[3][2], stat6_ch4[0][2][2]],   [6,"3 Cm",lab_col_ch4[3][1],   stat6_ch4[3][1], stat6_ch4[0][1][2]],[6,"5 Wa",lab_col_ch4[5][1], stat6_ch4[3][3],stat6_ch4[0][3][2]]],
               ev7=[[7,"4 Ls",lab_col_ch4[4][1],  stat7_ch4[3][2], stat7_ch4[0][2][2]],   [7,"10 Wet",lab_col_ch4[10][1], stat7_ch4[3][8], stat7_ch4[0][8][2]],[7,"5 Wa",lab_col_ch4[5][1], stat7_ch4[3][3], stat7_ch4[0][3][2]]],
               ev8=[[8,"3 Cm",lab_col_ch4[3][1],  stat8_ch4[3][1], stat8_ch4[0][1][2]],   [8,"4 Ls",lab_col_ch4[4][1],   stat8_ch4[3][2], stat8_ch4[0][2][2]]],
               ev9=[[9,"4 Ls",lab_col_ch4[4][1], np.nan, np.nan],   [9,"3 Cm",lab_col_ch4[3][1],   np.nan, np.nan]],
               ev10=[[10,"4 Ls",lab_col_ch4[4][1],stat10_ch4[3][2],stat10_ch4[0][2][2]],  [10,"5 Wa",lab_col_ch4[5][1],  stat10_ch4[3][3],stat10_ch4[0][3][2]]],
               ev11=[[11,"10 Wet",lab_col_ch4[10][1],stat11_ch4[3][8],stat11_ch4[0][8][2]],[11,"2 Og",lab_col_ch4[2][1], stat11_ch4[3][0],stat11_ch4[0][0][2]]],
               ev12=[[12,"9 Bb",lab_col_ch4[9][1], stat12_ch4[3][7], stat12_ch4[0][7][2]]],
               ev13=[[13,"3 Cm",lab_col_ch4[3][1], stat13_ch4[3][1], stat13_ch4[0][1][2]],[13,"4 Ls",lab_col_ch4[4][1], stat13_ch4[3][2], stat13_ch4[0][2][2]],[13,"5 Wa",lab_col_ch4[5][1], stat13_ch4[3][3], stat13_ch4[0][3][2]]],
               ev14=[[14,"4 Ls",lab_col_ch4[4][1],stat14_ch4[3][2], stat14_ch4[0][2][2]], [14,"5 Wa",lab_col_ch4[5][1], stat14_ch4[3][3], stat14_ch4[0][3][2]],[14,"2 Og",lab_col_ch4[2][1], stat14_ch4[3][0], stat14_ch4[0][0][2]]],
               ev15=[[15,"4 Ls",lab_col_ch4[4][1],stat15_ch4[3][2], stat15_ch4[0][2][2]], [15,"3 Cm",lab_col_ch4[3][1], stat15_ch4[3][1], stat15_ch4[0][1][2]],[15,"5 Wa",lab_col_ch4[5][1], stat15_ch4[3][3], stat15_ch4[0][3][2]]],
               ev16=[[16,"4 Ls",lab_col_ch4[4][1],stat16_ch4[3][2], stat16_ch4[0][2][2]]])

#co_aus,co_afr,co_sam,co_oth,co_bbsam,co_bbaf,co_bbnhas,co_bbaus,co_bbindo,co_bboth,co_ch4,co_nmvoc 
co_trac = dict(ev1=[[1,"2 AAua",lab_col_co[2][1],  stat1_co[3][0], stat1_co[0][0][2]],  [1,"9 BAua", lab_col_co[9][1], stat1_co[3][7], stat1_co[0][7][2]]],
               ev2=[[2,"2 AAua",lab_col_co[2][1],  stat2_co[3][0], stat2_co[0][0][2]]], 
               ev3=[[3,"2 AAua",lab_col_co[2][1],  stat3_co[3][0], stat3_co[0][0][2]],  [3,"9 BAua", lab_col_co[9][1], stat3_co[3][7], stat3_co[0][7][2]]],
               ev4=[[4,"2 AAua",lab_col_co[2][1],  stat4_co[3][0], stat4_co[0][0][2]]],
               ev5=[[5,"12 CH4",lab_col_co[12][1], np.nan,np.nan]],
               ev6=[[6,"9 BAua",lab_col_co[9][1],  stat6_co[3][7], stat6_co[0][7][2]]],
               ev7=[[7,"2 AAua",lab_col_co[2][1],  stat7_co[3][0], stat7_co[0][0][2]],  [7,"9 BAua", lab_col_co[9][1], stat7_co[3][7], stat7_co[0][7][2]]],
               ev8=[[8,"2 AAua",lab_col_co[2][1],  stat8_co[3][0], stat8_co[0][0][2]],  [8,"9 BAua", lab_col_co[9][1], stat8_co[3][7], stat8_co[0][7][2]]],
               ev9=[[9,"11 Both",lab_col_co[11][1], stat9_co[3][9], stat9_co[0][9][2]]],
               ev10=[[10,"9 BAua",lab_col_co[9][1],stat10_co[3][7],stat10_co[0][7][2]]],
               ev11=[[11,"7 BAfr",lab_col_co[7][1],stat11_co[3][5],stat11_co[0][5][2]], [11,"3 AAfr",lab_col_co[3][1], stat11_co[3][1],stat11_co[0][1][2]]],
               ev12=[[12,"9 BAua",lab_col_co[9][1],stat12_co[3][7],stat12_co[0][7][2]]],
               ev13=[[13,"2 AAua",lab_col_co[2][1],stat13_co[3][0],stat13_co[0][0][2]], [13,"9 BAua",lab_col_co[9][1],stat13_co[3][7],stat13_co[0][7][2]]],
               ev14=[[14,"2 AAua",lab_col_co[2][1],stat14_co[3][0],stat14_co[0][0][2]], [14,"7 BAfr",lab_col_co[7][1],stat14_co[3][5],stat14_co[0][5][2]]],
               ev16=[[16,"9 BAua",lab_col_co[9][1],stat16_co[3][7],stat16_co[0][7][2]]])

#NOT USING THE BACKGROUND!
#co2_ff,co2_oc,co2_bal,co2_bb,co2_bf,co2_nte,co2_se,co2_av,co2_ch,co2_corr,'co2_backg' 
co2_trac= dict(ev1=[[1,"2 Ff", lab_col_co2[2][1],  stat1_co2[3][0], stat1_co2[0][0][2]],  [1,"4 Bal",lab_col_co2[4][1],stat1_co2[3][2], stat1_co2[0][2][2]]],
               ev2=[[2,"4 Bal",lab_col_co2[4][1],  stat2_co2[3][2], stat2_co2[0][2][2]],  [2,"2 Ff",lab_col_co2[2][1], stat2_co2[3][0], stat2_co2[0][0][2]]], 
               ev3=[[3,"4 Bal",lab_col_co2[4][1],  stat3_co2[3][2], stat3_co2[0][2][2]],  [3,"2 Ff",lab_col_co2[2][1], stat3_co2[3][0], stat3_co2[0][0][2]]],
               ev4=[[4,"4 Bal",lab_col_co2[4][1],  stat4_co2[3][2], stat4_co2[0][2][2]],  [4,"2 Ff",lab_col_co2[2][1], stat4_co2[3][0], stat4_co2[0][0][2]]],
               ev5=[[5,"5 Bb", lab_col_co2[5][1],  stat5_co2[3][3], stat5_co2[0][3][2]],  [5,"2 Ff",lab_col_co2[2][1], stat5_co2[3][0], stat5_co2[0][0][2]]],
               ev6=[[6,"4 Bal",lab_col_co2[4][1],  stat6_co2[3][2], stat6_co2[0][2][2]],  [6,"2 Ff",lab_col_co2[2][1], stat6_co2[3][0], stat6_co2[0][0][2]]],
               ev8=[[8,"4 Bal",lab_col_co2[4][1],  stat8_co2[3][2], stat8_co2[0][2][2]],  [8,"2 Ff",lab_col_co2[2][1], stat8_co2[3][0], stat8_co2[0][0][2]]],
               ev9=[[9,"5 Bb",  lab_col_co2[5][1], stat9_co2[3][3], stat9_co2[0][3][2]]],
               ev11=[[11,"4 Bal",lab_col_co2[4][1],stat11_co2[3][2],stat11_co2[0][2][2]], [11,"2 Ff",lab_col_co2[2][1],stat11_co2[3][0],stat11_co2[0][0][2]]],
               ev15=[[15,"4 Bal",lab_col_co2[4][1],stat15_co2[3][2], stat15_co2[0][2][2]],[15,"2 Ff",lab_col_co2[2][1],stat15_co2[3][0],stat15_co2[0][0][2]]],
               ev16=[[16,"4 Bal",lab_col_co2[4][1],stat16_co2[3][2], stat16_co2[0][2][2]],[16,"5 Bb",lab_col_co2[5][1],stat16_co2[3][3],stat16_co2[0][3][2]]])


#labels
l_ch4=np.array([lab_col_ch4[2],lab_col_ch4[3],lab_col_ch4[4],lab_col_ch4[5],lab_col_ch4[9],lab_col_ch4[10]])
l_co=np.array([lab_col_co[2],lab_col_co[3],lab_col_co[9],lab_col_co[7],lab_col_co[11]])
l_co2=np.array([lab_col_co2[2],lab_col_co2[5],lab_col_co2[4]])
   

def stack_all(x_meas,x_mod,xg1,xg2,all_ev,l1,l2,sp1,sp2,col1,col2,ylim1a,ylim1b,ylim2a,ylim2b):
    #fig= plt.figure()   
    for i in range(len(x_mod[0])):
        ax1.plot(x_meas[0][i]-0.2,x_meas[1][i],marker="o",alpha=0.7, color=col1, ms=16)
        ax1.plot(x_mod[0][i]-0.2,x_mod[1][i],marker="v", alpha=0.7,color=col1, ms=16)
    for event in all_ev:
        bottom_counter=0
        for i,(ev,trac,col,enh,corrcoef) in enumerate(xg1[event]):
            ax1.bar(ev-0.3,enh,width=0.3, color=col,bottom=bottom_counter)
            bottom_counter+=enh
    plt.ylim(ylim1a,ylim1b)
    plt.ylabel(r'$\Delta$'+sp1, color=col1,fontsize=25)
    plt.yticks(color=col1,fontsize=25)
    plt.xticks(np.arange(1,17,1),fontsize=25)
    plt.grid(axis='x')
    ax1.spines['top'].set_visible(False) 
    ax2 = ax1.twinx()
    for i in range(len(x_mod[0])):
        ax2.plot(x_meas[0][i]+0.2,x_meas[2][i],'o',alpha=0.7, color=col2, ms=16)
        ax2.plot(x_mod[0][i]+0.2,x_mod[2][i],'v', alpha=0.7,color=col2, ms=16)
    for event in all_ev:
        bottom_counter=0
        for i,(ev,trac,col,enh,corrcoef) in enumerate(xg2[event]):
            ax2.bar(ev,enh,width=0.3, color=col,bottom=bottom_counter)
            bottom_counter+=enh
    #LABELS (LEGENDS)
    #plt.plot(np.nan,np.nan,marker="o",  color=col1, ms=20,ls='None',label='Total '+sp1+' Meas')
    #plt.plot(np.nan,np.nan,marker="v",  color=col1, ms=20,ls='None',label='Total '+sp1+' Model')
    #for i in range(len(l1)):
            #plt.plot(np.nan,np.nan,marker="_",  color=l1[i][1], ms=40,mew=15,ls='None',label=l1[i][0]) 
    #plt.plot(np.nan,np.nan,marker="o",  color=col2, ms=20,ls='None',label='Total '+sp2+' Meas')
    #plt.plot(np.nan,np.nan,marker="v",  color=col2, ms=20,ls='None',label='Total '+sp2+' Model')
    #for i in range(len(l2)):
            #plt.plot(np.nan,np.nan,marker="_",  color=l2[i][1], ms=40,mew=15,ls='None',label=l2[i][0]) 
    #l=plt.legend(numpoints=1,ncol=1, fontsize=20)
    #l.draggable()
    ax2.spines['top'].set_visible(False) 
    plt.ylabel(r'$\Delta$'+sp2,color=col2,fontsize=25)
    plt.yticks(color=col2,fontsize=25)
    plt.xlim(0,17)
    plt.ylim(ylim2a,ylim2b)
    ax2.axhline(y=ylim2b, color='black', alpha=0.2, linestyle='--')
    d = .01 # how big to make the diagonal lines in axes coordinates
    # arguments to pass plot, just so we don't keep repeating them
    kwargs = dict(transform=ax1.transAxes, color='black', clip_on=False)
   
    kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
    ax2.plot((-d,+d),(1-d,1+d), **kwargs)   # bottom-left diagonal
    ax2.plot((1-d,1+d),(1-d,1+d), **kwargs) # bottom-right diagonal
    #ax1.axes.get_xaxis().set_visible(False)
    return plt
               
def stack_all_break(x_meas,x_mod,xg1,xg2,all_ev,col1,col2,ylim1a,ylim1b,ylim2a,ylim2b):
    #fig= plt.figure()   
    for i in range(len(x_mod[0])):
        ax1.plot(x_meas[0][i]-0.2,x_meas[1][i],marker="o",alpha=0.7, color=col1, ms=16)
        ax1.plot(x_mod[0][i]-0.2,x_mod[1][i],marker="v", alpha=0.7,color=col1, ms=16)
    for event in all_ev:
        bottom_counter=0
        for i,(ev,trac,col,enh,corrcoef) in enumerate(xg1[event]):
            ax1.bar(ev-0.3,enh,width=0.3, color=col,bottom=bottom_counter)
            bottom_counter+=enh
    plt.ylim(ylim1a,ylim1b)
    ax1.yaxis.set_ticks(np.arange(ylim1a, ylim1b, ylim1b-ylim1a-1))
    plt.yticks(color=col1,fontsize=25)
    plt.xticks(np.arange(1,17,1),fontsize=0)
    plt.grid(axis='x')
    ax1.spines['bottom'].set_visible(False) 
    ax2 = ax1.twinx()
    for i in range(len(x_mod[0])):
        ax2.plot(x_meas[0][i]+0.2,x_meas[2][i],'o',alpha=0.7, color=col2, ms=16)
        ax2.plot(x_mod[0][i]+0.2,x_mod[2][i],'v', alpha=0.7,color=col2, ms=16)
    for event in all_ev:
        bottom_counter=0
        for i,(ev,trac,col,enh,corrcoef) in enumerate(xg2[event]):
            ax2.bar(ev,enh,width=0.3, color=col,bottom=bottom_counter)
            bottom_counter+=enh
    # Hide the right and top spines
    plt.yticks(color=col2,fontsize=25)
    plt.xlim(0,17)
    ax2.yaxis.set_ticks(np.arange(ylim2a, ylim2b, ylim2b-ylim2a-1))
    ax2.spines['bottom'].set_visible(False)  
    plt.ylim(ylim2a,ylim2b)
    ax2.axhline(y=ylim2a, color='black', linestyle='--')
    #ax1.axes.get_xaxis().set_visible(False)
    return plt


def legend(l1,l2,l3,sp1,sp2,sp3,col1,col2,col3):
    #LABELS (LEGENDS)
    plt.plot(np.nan,np.nan,marker="o",  color=col1, ms=20,ls='None',label='Total '+sp1+' Meas')
    plt.plot(np.nan,np.nan,marker="v",  color=col1, ms=20,ls='None',label='Total '+sp1+' Model')
    for i in range(len(l1)):
            plt.plot(np.nan,np.nan,marker="_",  color=l1[i][1], ms=40,mew=15,ls='None',label=l1[i][0]) 
    plt.plot(np.nan,np.nan,marker="o",  color=col2, ms=20,ls='None',label='Total '+sp2+' Meas')
    plt.plot(np.nan,np.nan,marker="v",  color=col2, ms=20,ls='None',label='Total '+sp2+' Model')
    for i in range(len(l2)):
            plt.plot(np.nan,np.nan,marker="_",  color=l2[i][1], ms=40,mew=15,ls='None',label=l2[i][0]) 
    plt.plot(np.nan,np.nan,marker="o",  color=col3, ms=20,ls='None',label='Total '+sp3+' Meas')
    plt.plot(np.nan,np.nan,marker="v",  color=col3, ms=20,ls='None',label='Total '+sp3+' Model')
    for i in range(len(l3)):
            plt.plot(np.nan,np.nan,marker="_",  color=l3[i][1], ms=40,mew=15,ls='None',label=l3[i][0]) 
    l=plt.legend(numpoints=1,ncol=1, fontsize=20)
    l.draggable()
    return plt
    
def plt_emis(x,xg,sp1,sp2,ylima,ylimb): 
    #fig= plt.figure()   
    for i in range(len(x[0])):
        plt.errorbar(x[0][i],x[1][i],yerr=x[2][i],fmt='o', alpha=0.7, color='black', ms=x[-1][i]*30)
        plt.errorbar(xg[0][i],xg[1][i],yerr=xg[2][i],fmt='v', alpha=0.7, color='firebrick', ms=xg[-1][i]*30)
    plt.errorbar(np.nan,np.nan,yerr=np.nan,fmt='o', alpha=0.7, color='black', ms=16, label=r'$\Delta$'+sp1+':'+r'$\Delta$'+sp2+' Measurement')
    plt.errorbar(np.nan,np.nan,yerr=np.nan,fmt='v', alpha=0.7, color='firebrick', ms=16, label=r'$\Delta$'+sp1+':'+r'$\Delta$'+sp2+' Model')
    l=plt.legend(ncol=2, fontsize=25)
    l.draggable()
    plt.xticks(np.arange(1,17,1),fontsize=25)
    plt.yticks(fontsize=25)
    plt.xlim(0,17)
    #plt.ylim(-0.4,10)
    plt.xlabel('Events',fontsize=25)
    plt.ylabel('Emission ratios',fontsize=25)
    plt.grid(axis='x')
    plt.ylim(ylima,ylimb)
    return plt
   
gs = gridspec.GridSpec(3, 1,
                       width_ratios=[1],
                       height_ratios=[0.1,0.6,0.9]
                       )
gs.update(hspace=0.13)
#gs.update(wspace=0.05)

#CH4_CO
all_ev1=['ev1','ev3','ev4','ev5','ev6','ev8','ev9','ev11','ev16','ev7','ev10','ev12','ev14']

fig = plt.figure()
plt.subplots_adjust(right=0.75, left=0.1,bottom=0.18)  
ax1 = plt.subplot(gs[0])    
plt.text(-2.5,210,'a)'+ r'$\Delta$CH4:'+r'$\Delta$CO', fontsize=30, color='black')
ch4_co_plt=stack_all_break(ch4_co_meas,ch4_co_mod,ch4_trac,co_trac,all_ev1,'steelblue','darkorange',60,141,60,161)
ax1 = plt.subplot(gs[1])  
ch4_co_plt=stack_all(ch4_co_meas,ch4_co_mod,ch4_trac,co_trac,all_ev1,l_ch4,l_co,'CH4','CO','steelblue','darkorange',0,40,0,35)
ax1 = plt.subplot(gs[2])    
ch4_co_plt=plt_emis(ch4_co,ch4_cog,'CH4','CO',0,6)             
        
#CH4_CO2
all_ev2=['ev1','ev3','ev4','ev5','ev6','ev8','ev9','ev11','ev16','ev15']
fig = plt.figure()
plt.subplots_adjust(right=0.75, left=0.1,bottom=0.18)  
ax1 = plt.subplot(gs[0])    
plt.text(-2.5,50,'b)'+ r'$\Delta$CH4:'+r'$\Delta$CO2', fontsize=30, color='black')
ch4_co2_plt=stack_all_break(ch4_co2_meas,ch4_co2_mod,ch4_trac,co2_trac,all_ev2,'steelblue','m',30,41,4.5,16)
ax1 = plt.subplot(gs[1])    
ch4_co2_plt=stack_all(ch4_co2_meas,ch4_co2_mod,ch4_trac,co2_trac,all_ev2,l_ch4,l_co2,'CH4','CO2','steelblue','m',0,30,0,2.5)
legend(l_ch4,l_co,l_co2,'CH4','CO','CO2','steelblue','darkorange','m')
ax1 = plt.subplot(gs[2])    
ch4_co2_plt=plt_emis(ch4_co2,ch4_co2g,'CH4','CO2',0,22)

#CO_CO2
all_ev3=['ev1','ev3','ev4','ev5','ev6','ev8','ev9','ev11','ev16']
fig = plt.figure()
plt.subplots_adjust(right=0.75, left=0.1,bottom=0.18)  
ax1 = plt.subplot(gs[0])    
plt.text(-2.5,44,'c)'+ r'$\Delta$CO:'+r'$\Delta$CO2', fontsize=30, color='black')
co_co2_plt=stack_all_break(co_co2_meas,co_co2_mod,co_trac,co2_trac,all_ev3,'darkorange','m',16,31,4,15)
ax1 = plt.subplot(gs[1])    
co_co2_plt=stack_all(co_co2_meas,co_co2_mod,co_trac,co2_trac,all_ev3,l_co,l_co2,'CO','CO2','darkorange','m',0,14,0,2.5)
ax1 = plt.subplot(gs[2])    
co_co2_plt=plt_emis(co_co2,co_co2g,'CO','CO2',0,32)

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
#OLD TRACER EVENT PLOT
#def plt_tracers(x,xg1,xg2,all_ev,l1,l2,sp1,sp2,col1,col2,x1,x2): 
#    #fig= plt.figure()   
#    for i in range(len(x[0])):
#        ax1.plot(x[0][i],x[1][i],marker="_", color=col1, ms=20,mew=2)
#    for event in all_ev:
#        #when I have more then 1 tracer
#        for i,(ev,trac,mark,enh,corrcoef) in enumerate(xg1[event]):
#            ax1.plot(ev,enh,marker=mark,ms=corrcoef*15,mfc=col1,mec=col1)
#    plt.ylabel(r'$\Delta$'+sp1, color=col1,fontsize=20)
#    plt.yticks(color=col1,fontsize=20)
#    plt.xticks(np.arange(1,17,1),fontsize=20)
#    plt.grid(axis='x')
#    ax2 = ax1.twinx()
#    for i in range(len(x[0])):
#        ax2.plot(x[0][i],x[2][i],'_', color=col2, ms=20,mew=2)
#    for event in all_ev:
#        #when I have more then 1 tracer
#        for i,(ev,trac,mark,enh,corrcoef) in enumerate(xg2[event]):
#            ax2.plot(ev,enh,marker=mark,ms=corrcoef*15,mfc=col2,mec=col2)
#    #LABELS (LEGENDS)
#    plt.plot(np.nan,np.nan,marker="_",  color=col1, ms=20,mew=2,ls='None',label='Total '+sp1)
#    for i in range(x1):
#        plt.plot(np.nan,np.nan,marker="$"+str(i+1)+"$",  mfc=col1,mec=col1, ms=15,ls='None',label=l1[i])  
#    plt.plot(np.nan,np.nan,marker="_",  color=col2, ms=20,mew=2,ls='None',label='Total '+sp2)
#    for i in range(x2):
#        plt.plot(np.nan,np.nan,marker="$"+str(i+1)+"$",  mfc=col2,mec=col2, ms=15,ls='None',label=l2[i])  
#    l=plt.legend(numpoints=1,ncol=1, fontsize=20)
#    l.draggable()
#    plt.ylabel(r'$\Delta$'+sp2,color=col2,fontsize=20)
#    plt.yticks(color=col2,fontsize=20)
#    plt.xlim(0,17)
#    #ax1.axes.get_xaxis().set_visible(False)
#    return plt    


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