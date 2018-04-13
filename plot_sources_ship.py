#Plot the sources for the ship data
#plot individual and then average it as southband and northbound
import numpy as np
import matplotlib.pyplot as plt
import read
import average
import stack
import mean
import scale
import split
from scipy import signal
import matplotlib as mpl
from label_color import label_color
import bias_correction

#########
#SETUP 1#------------------------------------------------------------------------
#########
#specify the trip you want to plot 1 or 2
trip=1
avg=2    #1 or 2 degree

##########
#SETUP 2 #------------------------------------------------------------------------
##########
if trip==1:
    ind=1327 #model and measurement have the same lenght now and same averaging
    year=2012
    offsetco2=0
    offsetch4=0
    offsetco=0
else:
    ind=2098     #at Darwin lon[ind]=130.917
    year=2013
    offsetco2=0
    offsetch4=0
    offsetco=0
    
if avg==1:
    avg_meas=average.average_meas_1lat
    avg_mod=average.average_mod_1lat
else:
    avg_meas=average.average_meas_2lat
    avg_mod=average.average_mod_2lat

#######
#FILES#------------------------------------------------------------------------
#######    
#path and file
path_meas = '/home/bb907/Desktop/Computer/Work/Data/Ship_Train_insitu/Ship_2012_2013/Measurements/Avg_Measurements/avg_meas20min'+str(year)+'shipAll.csv'
path_gc = '/home/bb907/Desktop/Computer/Work/Data/Ship_Train_insitu/Ship_2012_2013/Model/GC/'

#######
#READ #------------------------------------------------------------------------
#######
#Read in the measurements   
co2_m,datem, latm, lonm, presm = read.meas(path_meas, x_row=6)
ch4_m,datem, latm, lonm, presm = read.meas(path_meas, x_row=7)
co_m,datem, latm, lonm, presm = read.meas(path_meas, x_row=8)

#Read in GEOS-Chem for the specified trip
#date,lat,lon,pres,co2_tot,co2_ff,co2_oc,co2_bal,co2_bb,co2_bf,co2_nte,co2_se,co2_av,co2_ch,co2_corr,'co2_backg' 
all_co2 = read.read_model_tracers(path_gc+"CO2/"+str(trip)+"/*.txt",offsetco2, convert=1000000, sp='CO2')
#date,lat,lon,pres,ch4_tot,ch4_og,ch4_cm,ch4_ls,ch4_wa,ch4_bf,ch4_ri,ch4_an,ch4_bb,ch4_we,ch4_sa,ch4_nat 
all_ch4= read.read_model_tracers(path_gc+"CH4/"+str(trip)+"/*.txt",  offsetch4,convert=1000000000, sp='CH4')
#date,lat,lon,pres,co_tot,co_aus,co_afr,co_sam,co_oth,co_bbsam,co_bbaf,co_bbnhas,co_bbaus,co_bbindo,co_bboth,co_ch4,co_nmvoc 
all_co= read.read_model_tracers(path_gc+"CO/"+str(trip)+"/*.txt",  offsetco,convert=1000000000, sp='CO')

##################
#BIAS CORRECTION #------------------------------------------------------------------------
##################
#Only model total co2 and ch4
all_co2=list(all_co2)
all_co2[4]=bias_correction.bias_correction(all_co2[0],all_co2[4],'CO2_13')

all_ch4=list(all_ch4)
all_ch4[4]=bias_correction.bias_correction(all_ch4[0],all_ch4[4],'CH4_13')

#plt.plot(all_ch4[0],all_ch4[4])
#tracers=sum(all_ch4[5:])
#plt.plot(all_ch4[0],tracers)
#######
#SPLIT#------------------------------------------------------------------------
#######
#Now split the trip to norhtbound and southbound parts a and b
#based on date, the 1st trip 20120/4/11 - 2012/6/17 switched in June date1[1327]
#2nd trip started 2013/6/17 - 2013/10/2 switched august date2[2192]

#CO2        
co2_am,dateam, latam, lonam, presam = split.split_meas(co2_m,datem, latm, lonm, presm ,ind=ind,first='Y')
co2_bm,datebm, latbm, lonbm, presbm = split.split_meas(co2_m,datem, latm, lonm, presm ,ind=ind,first='N')
#CH4
ch4_am,dateam, latam, lonam, presam = split.split_meas(ch4_m,datem, latm, lonm, presm,ind=ind,first='Y')
ch4_bm,datebm, latbm, lonbm, presbm = split.split_meas(ch4_m,datem, latm, lonm, presm,ind=ind,first='N')
#CO
co_am,dateam, latam, lonam, presam = split.split_meas(co_m,datem, latm, lonm, presm,ind=ind,first='Y')
co_bm,datebm, latbm, lonbm, presbm = split.split_meas(co_m,datem, latm, lonm, presm,ind=ind,first='N')
       
#CO2         
all_co2a=split.split_mod(all_co2, ind=ind,first='Y')        
all_co2b=split.split_mod(all_co2,ind=ind,first='N')               
#CH4
all_ch4a=split.split_mod(all_ch4, ind=ind,first='Y')        
all_ch4b=split.split_mod(all_ch4,ind=ind,first='N')       
#CO
all_coa=split.split_mod(all_co, ind=ind,first='Y')        
all_cob=split.split_mod(all_co,ind=ind,first='N')  

#fig = plt.figure()
#plt.plot(latam,all_co2a[-1])

#####################
#CONVERT TO POSITIVE#this is now done in mean----------------------------------------------------------
#####################
#IN order to correctly calculate the realative change I cant have negative values or it will reverse the variability
#all_co2a[6]=all_co2a[6]*(-1) #ocean
#all_co2a[10]=all_co2a[10]*(-1)  #net terr
#all_co2a[-2]=all_co2a[-2]*(-1)  #ch sr corr
#
#all_co2b[6]=all_co2b[6]*(-1)
#all_co2b[10]=all_co2b[10]*(-1)
#all_co2b[-2]=all_co2b[-2]*(-1)

#####################
#DETREND BIOPSHERE  #----------------------------------------------------------
#####################
##Also detrend the balanced bisosphere
#all_co2a[7]=signal.detrend(all_co2a[7])
#all_co2b[7]=signal.detrend(all_co2b[7])
#This was before we fixed the CO2 bug where it double counted the emissions

########################
#AVERAGE PER 1 or 2 LAT#-------------------------------------------------------
########################
#measurements
#CO2      
lataam,co2_aam = avg_meas(latam,co2_am)
latabm,co2_abm =  avg_meas(latbm,co2_bm)
#CH4
lataam,ch4_aam=  avg_meas(latam,ch4_am)
latabm,ch4_abm =  avg_meas(latbm,ch4_bm)
#CO
lataam,co_aam=  avg_meas(latam,co_am)
latabm,co_abm=  avg_meas(latbm,co_bm)
    
#model, this values have 2 dimension now, the second has an additionall nested tracers
#co2
all_co2a_avg=avg_mod(all_co2a[1],all_co2a[4:]) #lat, totla model and tracers
all_co2b_avg=avg_mod(all_co2b[1],all_co2b[4:])
#ch4
all_ch4a_avg=avg_mod(all_ch4a[1],all_ch4a[4:])
all_ch4b_avg=avg_mod(all_ch4b[1],all_ch4b[4:])
#co
all_coa_avg=avg_mod(all_coa[1],all_coa[4:])
all_cob_avg=avg_mod(all_cob[1],all_cob[4:])

########
##SCALE#------------------------------------------------------------------------
########
##SCALING FOR CO2 AND CH4, because the sum of the tracers aren't = to the total gas
##co2    
#co2a_avg_s=scale.scale(all_co2a_avg[1],'CO2')
#co2b_avg_s=scale.scale(all_co2b_avg[1],'CO2')
#
##ch4
#ch4a_avg_s=scale.scale(all_ch4a_avg[1],'CH4') 
#ch4b_avg_s=scale.scale(all_ch4b_avg[1],'CH4') 

#################
#RELATIVE CHANGE#--------------------------------------------------------------
#################
#relative change,basically the individual - the minimum of that traces
#measurement and model (total and tracers)

#co2 !!!!!!NOT SCALED!!!!!!! There is still a problem with the CO2 tracers!!!!
co2a_rel=mean.mean_var(co2_aam,all_co2a_avg[1][0],all_co2a_avg[1][1:],mean='N',sp='CO2')
co2b_rel=mean.mean_var(co2_abm,all_co2b_avg[1][0],all_co2b_avg[1][1:],mean='N',sp='CO2')
##ch4 !!!!!!NOT SCALED!!!!!!!
ch4a_rel=mean.mean_var(ch4_aam,all_ch4a_avg[1][0],all_ch4a_avg[1][1:],mean='N',sp='CH4')
ch4b_rel=mean.mean_var(ch4_abm,all_ch4b_avg[1][0],all_ch4b_avg[1][1:],mean='N',sp='CH4')
#co !!!!!!NOT SCALED!!!!!!!
coa_rel=mean.mean_var(co_aam,all_coa_avg[1][0],all_coa_avg[1][1:],mean='N',sp='CO')
cob_rel=mean.mean_var(co_abm,all_cob_avg[1][0],all_cob_avg[1][1:],mean='N',sp='CO')  

#############################################
#SETUP COLORS AND LABELS FOR ALL THE SOURCES#----------------------------------
#############################################
#consistent colors and labels for the bar plot and pie plot

lc=label_color()
lab_col_co2=lc.co2
lab_col_ch4=lc.ch4
lab_col_co=lc.co

########################
##PLOT EVERYTHING TOTAL#--------------------------------------------------------
########################
##co2
#fig = plt.figure()
#ax1=plt.subplot(121)
#ax1=stack.stack_co2(lataam,co2_aam,all_co2a_avg[1][0],all_co2a_avg[1][1],all_co2a_avg[1][2],all_co2a_avg[1][3],all_co2a_avg[1][4],all_co2a_avg[1][5],all_co2a_avg[1][6],all_co2a_avg[1][7],all_co2a_avg[1][8],all_co2a_avg[1][9],all_co2a_avg[1][10],all_co2a_avg[1][11],lab_col_co2,t='am',h='')
#ax1=plt.subplot(122)
#ax1=stack.stack_co2(latabm,co2_abm,all_co2b_avg[1][0],all_co2b_avg[1][1],all_co2b_avg[1][2],all_co2b_avg[1][3],all_co2b_avg[1][4],all_co2b_avg[1][5],all_co2b_avg[1][6],all_co2b_avg[1][7],all_co2b_avg[1][8],all_co2b_avg[1][9],all_co2b_avg[1][10],all_co2b_avg[1][11],lab_col_co2,t='bm',h='')
#ax1.legend().draggable()  
#
##ch4
#fig = plt.figure()
#ax1=plt.subplot(121)
#ax1=stack.stack_ch4(lataam,ch4_aam,all_ch4a_avg[1][0],all_ch4a_avg[1][1],all_ch4a_avg[1][2],all_ch4a_avg[1][3],all_ch4a_avg[1][4],all_ch4a_avg[1][5],all_ch4a_avg[1][6],all_ch4a_avg[1][7],all_ch4a_avg[1][8],all_ch4a_avg[1][9],all_ch4a_avg[1][10],all_ch4a_avg[1][11],lab_col_ch4,t='am',h='')
#ax1=plt.subplot(122)
#ax1=stack.stack_ch4(latabm,ch4_abm,all_ch4b_avg[1][0],all_ch4b_avg[1][1],all_ch4b_avg[1][2],all_ch4b_avg[1][3],all_ch4b_avg[1][4],all_ch4b_avg[1][5],all_ch4b_avg[1][6],all_ch4b_avg[1][7],all_ch4b_avg[1][8],all_ch4b_avg[1][9],all_ch4b_avg[1][10],all_ch4b_avg[1][11],lab_col_ch4,t='bm',h='')
#ax1.legend().draggable()  
#    
##co
#fig = plt.figure()
#ax1=plt.subplot(121)
#ax1=stack.stack_co(lataam,co_aam,all_coa_avg[1][0],all_coa_avg[1][1],all_coa_avg[1][2],all_coa_avg[1][3],all_coa_avg[1][4],all_coa_avg[1][5],all_coa_avg[1][6],all_coa_avg[1][7],all_coa_avg[1][8],all_coa_avg[1][9],all_coa_avg[1][10],all_coa_avg[1][11],all_coa_avg[1][12],lab_col_co,t='am',h='')
#ax1=plt.subplot(122)
#ax1=stack.stack_co(latabm,co_abm,all_cob_avg[1][0],all_cob_avg[1][1],all_cob_avg[1][2],all_cob_avg[1][3],all_cob_avg[1][4],all_cob_avg[1][5],all_cob_avg[1][6],all_cob_avg[1][7],all_cob_avg[1][8],all_cob_avg[1][9],all_cob_avg[1][10],all_cob_avg[1][11],all_cob_avg[1][12],lab_col_co,t='bm',h='')
#ax1.legend().draggable()  

#########################
##PLOT EVERYTHING SCALED#-------------------------------------------------------
#########################
###EVERYTHING SCALED, WELL NOT CO, after the offset is fixed!!!!! CO don't need scaling
##co2
#fig = plt.figure()
#ax1=plt.subplot(121)
#ax1=stack.stack_co2(lataam,co2_aam,all_co2a_avg[1][0],co2a_avg_s[0],co2a_avg_s[1],co2a_avg_s[2],co2a_avg_s[3],co2a_avg_s[4],co2a_avg_s[5],co2a_avg_s[6],co2a_avg_s[7],co2a_avg_s[8],co2a_avg_s[9],co2a_avg_s[10],lab_col_co2,t='am',h='')
#ax1=plt.subplot(122)
#ax1=stack.stack_co2(latabm,co2_abm,all_co2b_avg[1][0],co2b_avg_s[0],co2b_avg_s[1],co2b_avg_s[2],co2b_avg_s[3],co2b_avg_s[4],co2b_avg_s[5],co2b_avg_s[6],co2b_avg_s[7],co2b_avg_s[8],co2b_avg_s[9],co2b_avg_s[10],lab_col_co2,t='bm',h='')
#ax1.legend().draggable()  
#
##ch4
#fig = plt.figure()
#ax1=plt.subplot(121)
#ax1=stack.stack_ch4(lataam,ch4_aam,all_ch4a_avg[1][0],ch4a_avg_s[0],ch4a_avg_s[1],ch4a_avg_s[2],ch4a_avg_s[3],ch4a_avg_s[4],ch4a_avg_s[5],ch4a_avg_s[6],ch4a_avg_s[7],ch4a_avg_s[8],ch4a_avg_s[9],ch4a_avg_s[10],lab_col_ch4,t='am',h='')
#ax1=plt.subplot(122)
#ax1=stack.stack_ch4(latabm,ch4_abm,all_ch4b_avg[1][0],ch4b_avg_s[0],ch4b_avg_s[1],ch4b_avg_s[2],ch4b_avg_s[3],ch4b_avg_s[4],ch4b_avg_s[5],ch4b_avg_s[6],ch4b_avg_s[7],ch4b_avg_s[8],ch4b_avg_s[9],ch4b_avg_s[10],lab_col_ch4,t='bm',h='')
#ax1.legend().draggable()  

##########################
#PLOT EVERYTHING RELATIVE#-----------------------------------------------------
##########################
##Relative change of the scaled values
#fig = plt.figure(figsize=(30,15))

fig = plt.figure()
plt.subplots_adjust(wspace=0.14,bottom=0.2,left=0.05,right=0.69)
#ch4
ax1=plt.subplot(121)
ax1=stack.stack_co2(lataam,co2a_rel[0],co2a_rel[1],co2a_rel[2][0],co2a_rel[2][1],co2a_rel[2][2],co2a_rel[2][3],co2a_rel[2][4],co2a_rel[2][5],co2a_rel[2][6],co2a_rel[2][7],co2a_rel[2][8],co2a_rel[2][9],co2a_rel[2][10],lab_col_co2,t='am',h='rel')
ax1.text(-43, 5.2, 'NB', fontsize=50) #7.8
ax1=plt.subplot(122)
ax1=stack.stack_co2(latabm,co2b_rel[0],co2b_rel[1],co2b_rel[2][0],co2b_rel[2][1],co2b_rel[2][2],co2b_rel[2][3],co2b_rel[2][4],co2b_rel[2][5],co2b_rel[2][6],co2b_rel[2][7],co2b_rel[2][8],co2b_rel[2][9],co2b_rel[2][10],lab_col_co2,t='bm',h='rel')
ax1.legend(fontsize=35).draggable()  
ax1.text(-43, 5.2, 'SB', fontsize=50)
      
#ch4
fig = plt.figure()
plt.subplots_adjust(wspace=0.14,bottom=0.2,left=0.05,right=0.69)
ax1=plt.subplot(121)
ax1=stack.stack_ch4(lataam,ch4a_rel[0],ch4a_rel[1],ch4a_rel[2][0],ch4a_rel[2][1],ch4a_rel[2][2],ch4a_rel[2][3],ch4a_rel[2][4],ch4a_rel[2][5],ch4a_rel[2][6],ch4a_rel[2][7],ch4a_rel[2][8],ch4a_rel[2][9],ch4a_rel[2][10],lab_col_ch4,t='am',h='rel')
ax1.text(-43, 40, 'NB', fontsize=50)
ax1=plt.subplot(122)
ax1=stack.stack_ch4(latabm,ch4b_rel[0],ch4b_rel[1],ch4b_rel[2][0],ch4b_rel[2][1],ch4b_rel[2][2],ch4b_rel[2][3],ch4b_rel[2][4],ch4b_rel[2][5],ch4b_rel[2][6],ch4b_rel[2][7],ch4b_rel[2][8],ch4b_rel[2][9],ch4b_rel[2][10],lab_col_ch4,t='bm',h='rel')
ax1.legend(fontsize=35).draggable()  
ax1.text(-43, 40, 'SB', fontsize=50)

#co
fig = plt.figure()
plt.subplots_adjust(wspace=0.14,bottom=0.2,left=0.05,right=0.69)
ax1=plt.subplot(121)
ax1=stack.stack_co(lataam,coa_rel[0],coa_rel[1],coa_rel[2][0],coa_rel[2][1],coa_rel[2][2],coa_rel[2][3],coa_rel[2][4],coa_rel[2][5],coa_rel[2][6],coa_rel[2][7],coa_rel[2][8],coa_rel[2][9],coa_rel[2][10],coa_rel[2][11],lab_col_co,t='am',h='rel')
ax1.text(-43, 54, 'NB', fontsize=50)
ax1=plt.subplot(122)
ax1=stack.stack_co(latabm,cob_rel[0],cob_rel[1],cob_rel[2][0],cob_rel[2][1],cob_rel[2][2],cob_rel[2][3],cob_rel[2][4],cob_rel[2][5],cob_rel[2][6],cob_rel[2][7],cob_rel[2][8],cob_rel[2][9],cob_rel[2][10],cob_rel[2][11],lab_col_co,t='bm',h='rel')
ax1.legend(fontsize=35).draggable()  
ax1.text(-43, 54, 'SB', fontsize=50)


##########
#PLOT PIE#---------------------------------------------------------------------
##########
#NOTE PIE ONLY WORKS IF ALL THE TRACERS ARE POSITIVE
#ACCTUALLY IT WORKS WITH NEGATIVE VALUES ALSO, IT WILL SHOW THE CORRECT VALUES
#BUT THE PIE WON'T LOOK NICE
#NOT SCALED TRACERS   
    
def pie(sizes,lc,sp):
    fig1, ax1 = plt.subplots()
    #get the colors because of the wierd formatting
    col=[]
    for i in range(len(lc)):
        col.append(lc[i][1])
    ax1.pie(sizes,colors=col[2:], autopct='%1.3f%%',pctdistance=0.8, textprops=dict(fontsize=20,color='white'))
    ax1.axis('equal')
    centre_circle = plt.Circle((0,0),0.2,color='black', fc='white',linewidth=1.25)
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    mpl.rcParams['font.size'] = 30

    ax1.text(1.1,1,  lc[2][0],color=lc[2][1],weight="bold")
    ax1.text(1.1,0.9,lc[3][0],color=lc[3][1],weight="bold")
    ax1.text(1.1,0.8,lc[4][0],color=lc[4][1],weight="bold")
    ax1.text(1.1,0.7,lc[5][0],color=lc[5][1],weight="bold")
    ax1.text(1.1,0.6,lc[6][0],color=lc[6][1],weight="bold")
    ax1.text(1.1,0.5,lc[7][0],color=lc[7][1],weight="bold")
    ax1.text(1.1,0.4,lc[8][0],color=lc[8][1],weight="bold")
    ax1.text(1.1,0.3,lc[9][0],color=lc[9][1],weight="bold")
    ax1.text(1.1,0.2,lc[10][0],color=lc[10][1],weight="bold")
    ax1.text(1.1,0.1,lc[11][0],color=lc[11][1],weight="bold")
    ax1.text(1.1,0,lc[12][0],color=lc[12][1],weight="bold")
    if sp=='CO':
        ax1.text(1.1,-0.1,lc[13][0],color=lc[13][1],weight="bold")
    #this is for the legend
    return plt

#mean of all the tracers during specific trip/leg
def pie_mean(all_x):
    size=[]
    for i in range(1,len(all_x[1][1:])+1):
        size.append(np.mean(all_x[1][i]))
    return size

    
##CO2 
sizes1a=pie_mean(all_co2a_avg)                     
sizes1b=pie_mean(all_co2b_avg)  

ax=pie(sizes1a,lab_col_co2,sp='CO2')    
ax=pie(sizes1b,lab_col_co2,sp='CO2')       

#CH4
sizes2a=pie_mean(all_ch4a_avg)                     
sizes2b=pie_mean(all_ch4b_avg)  

ax=pie(sizes2a,lab_col_ch4,sp='CH4')    
ax=pie(sizes2b,lab_col_ch4,sp='CH4')    

#CO
sizes3a=pie_mean(all_coa_avg)                     
sizes3b=pie_mean(all_cob_avg)  

ax=pie(sizes3a,lab_col_co,sp='CO')    
ax=pie(sizes3b,lab_col_co,sp='CO')    


#for CO2 the ocean, net terrestrial exchange and ch are NEGATIVE, 
#for ch4 the soil absorption is here POSITIVE

#2 dimensional
#lat[0], co_tot[1][0], co_aus,co_afr,co_sam,co_oth,co_bbsam,co_bbaf,co_bbnhas,co_bbaus,co_bbindo,co_bboth,co_ch4,co_nmvoc 
#lat,co2_tot,co2_ff,co2_oc,co2_bal,co2_bb,co2_bf,co2_nte,co2_se,co2_av,co2_ch,co2_corr,'co2_backg' 
#lat,ch4_tot,ch4_og,ch4_cm,ch4_ls,ch4_wa,ch4_bf,ch4_ri,ch4_an,ch4_bb,ch4_we,ch4_sa,ch4_nat 

#The idea is calculate the sum of the tracers, where I have both + and -
#Than make all of them + and calculate the precentage based on that!

xp_co2a=scale.precentage(all_co2a_avg,'CO2')
xp_co2b=scale.precentage(all_co2b_avg,'CO2')
print 'ff:  ',xp_co2a[0],'\n','oc: ',xp_co2a[1],'\n','bal:',xp_co2a[2],'\n','bb:  ',xp_co2a[3],'\n','bf:  ',xp_co2a[4],'\n',\
      'nte:',xp_co2a[5],'\n','se:  ',xp_co2a[6],'\n','av:  ',xp_co2a[7],'\n','ch:  ',xp_co2a[8],'\n',\
      'cor:',xp_co2a[9],'\n','bg:  ',xp_co2a[10]
print 'ff:  ',xp_co2b[0],'\n','oc: ',xp_co2b[1],'\n','bal:',xp_co2b[2],'\n','bb:  ',xp_co2b[3],'\n','bf:  ',xp_co2b[4],'\n',\
      'nte:',xp_co2b[5],'\n','se:  ',xp_co2b[6],'\n','av:  ',xp_co2b[7],'\n','ch:  ',xp_co2b[8],'\n',\
      'cor:',xp_co2b[9],'\n','bg:  ',xp_co2b[10]

xp_ch4a=scale.precentage(all_ch4a_avg,'CH4')
xp_ch4b=scale.precentage(all_ch4b_avg,'CH4')
print 'og:  ',xp_ch4a[0],'\n','cm:  ',xp_ch4a[1],'\n','ls:  ',xp_ch4a[2],'\n','wa:  ',xp_ch4a[3],'\n','bf:  ',xp_ch4a[4],'\n',\
      'ri:  ',xp_ch4a[5],'\n','an:  ',xp_ch4a[6],'\n','bb:  ',xp_ch4a[7],'\n','we:  ',xp_ch4a[8],'\n',\
      'sa: ',xp_ch4a[9],'\n','nat: ',xp_ch4a[10]
print 'og:  ',xp_ch4b[0],'\n','cm:  ',xp_ch4b[1],'\n','ls:  ',xp_ch4b[2],'\n','wa:  ',xp_ch4b[3],'\n','bf:  ',xp_ch4b[4],'\n',\
      'ri:  ',xp_ch4b[5],'\n','an:  ',xp_ch4b[6],'\n','bb:  ',xp_ch4b[7],'\n','we:  ',xp_ch4b[8],'\n',\
      'sa: ',xp_ch4b[9],'\n','nat: ',xp_ch4b[10]

xp_coa=scale.precentage(all_coa_avg,'CO')
xp_cob=scale.precentage(all_cob_avg,'CO')
print 'aus:  ',xp_coa[0],'\n','afr:  ',xp_coa[1],'\n','sam:  ',xp_coa[2],'\n','oth:  ',xp_coa[3],'\n','bbsam:',xp_coa[4],'\n',\
      'bbaf: ',xp_coa[5],'\n','bbnha:',xp_coa[6],'\n','bbaus:',xp_coa[7],'\n','bbind:',xp_coa[8],'\n',\
      'bboth:',xp_coa[9],'\n','ch4:  ',xp_coa[10],'\n','nmvoc:',xp_coa[11]
print 'aus:  ',xp_cob[0],'\n','afr:  ',xp_cob[1],'\n','sam:  ',xp_cob[2],'\n','oth:  ',xp_cob[3],'\n','bbsam:',xp_cob[4],'\n',\
      'bbaf: ',xp_cob[5],'\n','bbnha:',xp_cob[6],'\n','bbaus:',xp_cob[7],'\n','bbind:',xp_cob[8],'\n',\
      'bboth:',xp_cob[9],'\n','ch4:  ',xp_cob[10],'\n','nmvoc:',xp_cob[11]

 
    
## no BACKGROUDN AND CHEMICAL SURFACE CORRECITON TRACER
#def pie_nobackg(sizes,lc,sp):
#    fig1, ax1 = plt.subplots()
#    #get the colors because of the wierd formatting
#    col=[]
#    for i in range(len(lc)):
#        col.append(lc[i][1])
#    ax1.pie(sizes[:-1],colors=col[2:-1], autopct='%1.5f%%',pctdistance=0.8, textprops=dict(fontsize=20,color='white'))
#    ax1.axis('equal')
#    centre_circle = plt.Circle((0,0),0.2,color='black', fc='white',linewidth=1.25)
#    fig = plt.gcf()
#    fig.gca().add_artist(centre_circle)
#    mpl.rcParams['font.size'] = 30
#
#    ax1.text(1.1,1,  lc[2][0],color=lc[2][1],weight="bold")
#    ax1.text(1.1,0.9,lc[3][0],color=lc[3][1],weight="bold")
#    ax1.text(1.1,0.8,lc[4][0],color=lc[4][1],weight="bold")
#    ax1.text(1.1,0.7,lc[5][0],color=lc[5][1],weight="bold")
#    ax1.text(1.1,0.6,lc[6][0],color=lc[6][1],weight="bold")
#    ax1.text(1.1,0.5,lc[7][0],color=lc[7][1],weight="bold")
#    ax1.text(1.1,0.4,lc[8][0],color=lc[8][1],weight="bold")
#    ax1.text(1.1,0.3,lc[9][0],color=lc[9][1],weight="bold")
#    ax1.text(1.1,0.2,lc[10][0],color=lc[10][1],weight="bold")
#    ax1.text(1.1,0.1,lc[11][0],color=lc[11][1],weight="bold")
#    #this is for the legend
#    return plt  
      