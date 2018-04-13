# A script that plots the ship and train data
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.offsetbox import AnchoredText
import mean

############################################################
#RATIOS OF THE REALTIVE ENHANCEMENTS SEPPERATE             #-------------------
############################################################
def ratios_sep(lim1,lim2,lat,co2,ch4,co,co2g,ch4g,cog,ev):
    #calculate the realtive change
    co2r,co2gr,x=mean.mean_var(co2,co2g,np.zeros((3,2)),mean='N',sp='CO2')
    ch4r,ch4gr,x=mean.mean_var(ch4,ch4g,np.zeros((3,2)),mean='N',sp='CH4')
    cor,cogr,x=mean.mean_var(co,cog,np.zeros((3,2)),mean='N',sp='CO')
       
    #The indicise that correspond to the limits values
    l1ai=np.where(lat==lim1)[0]; l1bi=np.where(lat==lim2)[0]

    #select the values that correspond to the indicies
    co2_i=co2r[l1ai[0]:l1bi[0]]
    ch4_i=ch4r[l1ai[0]:l1bi[0]]
    co_i=cor[l1ai[0]:l1bi[0]]
    
    co2g_i=co2gr[l1ai[0]:l1bi[0]]
    ch4g_i=ch4gr[l1ai[0]:l1bi[0]]
    cog_i=cogr[l1ai[0]:l1bi[0]]
    
    def plot_corr(x,y, xlab, ylab,col,tit):
        #calculate everything I need for the linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        plt.plot(x,y,'o', color=col,alpha=0.7,markersize=17)
        plt.plot(x,slope*np.array(x)+intercept, 'r-',linewidth=2)
        equation='$Y='+str('%4.2f'%(slope)+r"$$\pm$$"+'%4.2f'%(std_err))+'*X'+str('%+4.2f'%(intercept))+'$'
        #equation='$Y='+str('%4.2f'%(slope))+'*X'+str('%+4.2f'%(intercept))+'$'
        r_squared='$R^2='+str('%4.2f'%(r_value)**2)+'$'
        anchored_text = AnchoredText(equation+'\n'+r_squared+'\n'+'$r= '+str('%4.2f'%(r_value))+'$''\n'+'$p= '+str('%4.4f'%(p_value))+'$', loc=2,prop=dict(size=19))
        ax1.add_artist(anchored_text)
        #for integer numbers on the axis
        #ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
        #or    
        #plt.plot(x,polyval(bla,x), 'r-') 
        plt.tick_params(axis='both', which='major', labelsize=27)
        plt.xlabel(xlab,fontsize=30)
        plt.ylabel(ylab,fontsize=30)
        plt.suptitle(tit, fontsize=30)
        plt.locator_params(nbins=6)
        #plt.legend(loc='upper left')
        return plt

    fig = plt.figure()
    #fig.subplots_adjust(hspace=.2)
    fig.subplots_adjust(wspace=.25,left=0.07,right=0.94)
    ax1=plt.subplot(231)
    ax1 = plot_corr(co_i,ch4_i, xlab=r'$\Delta$CO (ppb)', ylab=r'$\Delta$CH4 (ppb)',col='black', tit=ev)
    ax1=plt.subplot(232)
    ax1 = plot_corr(co2_i,ch4_i,  xlab=r'$\Delta$CO2 (ppm)', ylab=r'$\Delta$CH4(ppb)',col='black',tit=ev)
    ax1=plt.subplot(233)
    ax1 = plot_corr(co2_i,co_i, xlab=r'$\Delta$CO2 (ppm)', ylab=r'$\Delta$CO (ppb)',col='black', tit=ev)
    
    ax1=plt.subplot(234)
    ax1 = plot_corr(cog_i,ch4g_i, xlab=r'$\Delta$CO (ppb)', ylab=r'$\Delta$CH4 (ppb)',col='maroon', tit=ev)
    ax1=plt.subplot(235)
    ax1 = plot_corr(co2g_i,ch4g_i,  xlab=r'$\Delta$CO2 (ppm)', ylab=r'$\Delta$CH4 (ppb)',col='maroon',tit=ev)
    ax1=plt.subplot(236)
    ax1 = plot_corr(co2g_i,cog_i, xlab=r'$\Delta$CO2 (ppm)', ylab=r'$\Delta$CO (ppb)',col='maroon', tit=ev)
    return ax1


############################################################
#RATIOS OF THE REALTIVE ENHANCEMENTS COMBINED              #-------------------
############################################################
def ratios_com(lim1,lim2,lat,co2,ch4,co,co2g,ch4g,cog,ev):
    #calculate the realtive change
    co2r,co2gr,x=mean.mean_var(co2,co2g,np.zeros((3,2)),mean='N',sp='CO2')
    ch4r,ch4gr,x=mean.mean_var(ch4,ch4g,np.zeros((3,2)),mean='N',sp='CH4')
    cor,cogr,x=mean.mean_var(co,cog,np.zeros((3,2)),mean='N',sp='CO')
       
    #The indicise that correspond to the limits values
    l1ai=np.where(lat==lim1)[0]; l1bi=np.where(lat==lim2)[0]

    #select the values that correspond to the indicies
    co2_i=co2r[l1ai[0]:l1bi[0]]
    ch4_i=ch4r[l1ai[0]:l1bi[0]]
    co_i=cor[l1ai[0]:l1bi[0]]
    
    co2g_i=co2gr[l1ai[0]:l1bi[0]]
    ch4g_i=ch4gr[l1ai[0]:l1bi[0]]
    cog_i=cogr[l1ai[0]:l1bi[0]]
    
    def plot_corr(x,y, x1,y1, xlab, ylab,col,tit):
        #calculate everything I need for the linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        slope1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(x1,y1)
        plt.plot(x,y,'o', color='black',alpha=0.7,markersize=17)
        plt.plot(x1,y1,'o', color='maroon',alpha=0.7,markersize=17)
        plt.plot(x,slope*np.array(x)+intercept, 'black',linewidth=3)
        plt.plot(x1,slope1*np.array(x1)+intercept1, 'maroon',linewidth=3)
        #add 1:1 line
        lims = [
        np.min([ax1.get_xlim(), ax1.get_ylim()]),  # min of both axes
        np.max([ax1.get_xlim(), ax1.get_ylim()]),  # max of both axes
        ]
        plt.plot(lims,lims,'--r',linewidth=3)
        equation='$Y='+str('%4.2f'%(slope)+r"$$\pm$$"+'%4.2f'%(std_err))+'*X'+str('%+4.2f'%(intercept))+'$'
        #equation='$Y='+str('%4.2f'%(slope))+'*X'+str('%+4.2f'%(intercept))+'$'
        r_squared='$R^2='+str('%4.2f'%(r_value)**2)+'$'
        anchored_text = AnchoredText(equation+'\n'+r_squared+'\n'+'$r= '+str('%4.2f'%(r_value))+'$''\n'+'$p= '+str('%4.4f'%(p_value))+'$', loc=4,prop=dict(size=20,fontweight="bold",color='black'),frameon=False,bbox_to_anchor=(0.55, -0.6), bbox_transform=ax1.transAxes)
        ax1.add_artist(anchored_text)
        equation1='$Y='+str('%4.2f'%(slope1)+r"$$\pm$$"+'%4.2f'%(std_err1))+'*X'+str('%+4.2f'%(intercept1))+'$'
        #equation='$Y='+str('%4.2f'%(slope))+'*X'+str('%+4.2f'%(intercept))+'$'
        r_squared1='$R^2='+str('%4.2f'%(r_value1)**2)+'$'
        anchored_text1 = AnchoredText(equation1+'\n'+r_squared1+'\n'+'$r= '+str('%4.2f'%(r_value1))+'$''\n'+'$p= '+str('%4.4f'%(p_value1))+'$', loc=3,prop=dict(size=20,fontweight="bold",color='maroon'),frameon=False,bbox_to_anchor=(0.5, -0.6), bbox_transform=ax1.transAxes)
        ax1.add_artist(anchored_text1)
        #for integer numbers on the axis
        #ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
        #or    
        #plt.plot(x,polyval(bla,x), 'r-') 
        plt.tick_params(axis='both', which='major', labelsize=27)
        plt.xlabel(xlab,fontsize=30)
        plt.ylabel(ylab,fontsize=30)
        plt.suptitle(tit, fontsize=30)
        plt.locator_params(nbins=6)
        #the 1:1 changes the limits
        plt.xlim(lims)
        plt.ylim(lims)
        #plt.legend(loc='upper left')
        return plt, slope, slope1
    if ev=='Event 1' or ev=='Event 3' or ev=='Event 4' or ev=='Event 5' or ev=='Event 6' or ev=='Event 8' or ev=='Event 9' or ev=='Event 11' or ev=='Event 16':
        fig = plt.figure(figsize=(25,8))
        #fig.subplots_adjust(hspace=.2)
        fig.subplots_adjust(wspace=.25,bottom=0.34)
        ax1=plt.subplot(131)
        ax1, sl_co_ch4, slg_co_ch4 = plot_corr(co_i,ch4_i, cog_i,ch4g_i,xlab=r'$\Delta$CO (ppb)', ylab=r'$\Delta$CH4 (ppb)',col='indigo', tit=ev)
        ax1=plt.subplot(132)
        ax1, sl_co2_ch4, slg_co2_ch4 = plot_corr(co2_i,ch4_i,co2g_i,ch4g_i,  xlab=r'$\Delta$CO2 (ppm)', ylab=r'$\Delta$CH4(ppb)',col='indigo',tit=ev)
        ax1=plt.subplot(133)
        ax1 , sl_co2_co, slg_co2_co= plot_corr(co2_i,co_i, co2g_i,cog_i,xlab=r'$\Delta$CO2 (ppm)', ylab=r'$\Delta$CO (ppb)',col='indigo', tit=ev)
    elif ev=='Event 7' or ev=='Event 10' or ev=='Event 12' or ev=='Event 13' or ev=='Event 14':
        fig = plt.figure(figsize=(9,8))
        #fig.subplots_adjust(hspace=.2)
        fig.subplots_adjust(wspace=.25,bottom=0.34,left=0.20,right=0.83)
        ax1=plt.subplot(111)
        ax1, sl_co_ch4, slg_co_ch4 = plot_corr(co_i,ch4_i, cog_i,ch4g_i,xlab=r'$\Delta$CO (ppb)', ylab=r'$\Delta$CH4 (ppb)',col='indigo', tit=ev)
    elif ev=='Event 2':
        fig = plt.figure(figsize=(9,8))
        #fig.subplots_adjust(hspace=.2)
        fig.subplots_adjust(wspace=.25,bottom=0.34,left=0.20,right=0.83)
        ax1=plt.subplot(111)
        ax1, sl_co2_co, slg_co2_co = plot_corr(co2_i,co_i, co2g_i,cog_i,xlab=r'$\Delta$CO2 (ppm)', ylab=r'$\Delta$CO (ppb)',col='indigo', tit=ev)
    else:
        fig = plt.figure(figsize=(9,8))
        #fig.subplots_adjust(hspace=.2)
        fig.subplots_adjust(wspace=.25,bottom=0.34,left=0.20,right=0.83)
        ax1=plt.subplot(111)
        ax1, sl_co2_ch4, slg_co2_ch4= plot_corr(co2_i,ch4_i,co2g_i,ch4g_i, xlab=r'$\Delta$CO2 (ppm)', ylab=r'$\Delta$CH4(ppb)',col='indigo',tit=ev)
    plt.savefig('/home/bb907/Desktop/Computer/Work/Data/Ship_Train_insitu/Ship_2012_2013/scripts/plots/correlation/with_1_1/'+ev)
    #return the plot and the ratios
    if ev=='Event 1' or ev=='Event 3' or ev=='Event 4' or ev=='Event 5' or ev=='Event 6' or ev=='Event 8' or ev=='Event 9' or ev=='Event 11' or ev=='Event 16':
        return ax1,sl_co_ch4,sl_co2_ch4,sl_co2_co
    elif ev=='Event 7' or ev=='Event 10' or ev=='Event 12' or ev=='Event 13' or ev=='Event 14':    
        return ax1,sl_co_ch4
    elif ev=='Event 2':
        return ax1,sl_co2_co
    else:
        return ax1,sl_co2_ch4
        
####################################################################
#RATIOS OF THE REALTIVE ENHANCEMENTS COMBINED WITH THE AVERAGE LINE#-------------------
####################################################################
def ratios_com_avg(lim1,lim2,lat,co2,ch4,co,co2g,ch4g,cog,ch4co_avg,coco2_avg,co2ch4_avg,ev):
    #calculate the realtive change
    co2r,co2gr,x=mean.mean_var(co2,co2g,np.zeros((3,2)),mean='N',sp='CO2')
    ch4r,ch4gr,x=mean.mean_var(ch4,ch4g,np.zeros((3,2)),mean='N',sp='CH4')
    cor,cogr,x=mean.mean_var(co,cog,np.zeros((3,2)),mean='N',sp='CO')
       
    #The indicise that correspond to the limits values
    l1ai=np.where(lat==lim1)[0]; l1bi=np.where(lat==lim2)[0]

    #select the values that correspond to the indicies
    co2_i=co2r[l1ai[0]:l1bi[0]]
    ch4_i=ch4r[l1ai[0]:l1bi[0]]
    co_i=cor[l1ai[0]:l1bi[0]]
    
    co2g_i=co2gr[l1ai[0]:l1bi[0]]
    ch4g_i=ch4gr[l1ai[0]:l1bi[0]]
    cog_i=cogr[l1ai[0]:l1bi[0]]
    
    def plot_corr(x,y, x1,y1, x_avg, xlab, ylab,col,tit):
        #calculate everything I need for the linear regression
        #slope, intercept, r, p, std_err
        stat_meas= stats.linregress(x,y)
        stat_mod = stats.linregress(x1,y1)
        plt.plot(x,y,'o', color='black',alpha=0.7,markersize=17)
        plt.plot(x1,y1,'o', color='maroon',alpha=0.7,markersize=17)
        plt.plot(x,stat_meas[0]*np.array(x)+stat_meas[1], 'black',linewidth=3)
        plt.plot(x1,stat_mod[0]*np.array(x1)+stat_mod[1], 'maroon',linewidth=3)
        #add the average emission ratio line
        #create a new array that has the x values from 0 to the maximum value
        lims_x = [
        np.min([ax1.get_xlim()]),  # min of x axes
        np.max([ax1.get_xlim()]),  # max of x axes
        ]
        lims_y = [
        np.min([ax1.get_ylim()]),  # min of y axes
        np.max([ax1.get_ylim()]),  # max of y axes
        ]
        x_lim=np.arange(0,lims_x[-1]+5)
        plt.plot(x_lim,x_avg*x_lim,color='goldenrod',linestyle='dashed',linewidth=3) #linear regression line
        equation='$Y='+str('%4.2f'%(stat_meas[0])+r"$$\pm$$"+'%4.2f'%(stat_meas[-1]))+'*X'+str('%+4.2f'%(stat_meas[1]))+'$'
        #equation='$Y='+str('%4.2f'%(slope))+'*X'+str('%+4.2f'%(intercept))+'$'
        r_squared='$R^2='+str('%4.2f'%(stat_meas[2])**2)+'$'
        anchored_text = AnchoredText(equation+'\n'+r_squared+'\n'+'$r= '+str('%4.2f'%(stat_meas[2]))+'$''\n'+'$p= '+str('%4.4f'%(stat_meas[3]))+'$', loc=4,prop=dict(size=20,fontweight="bold",color='black'),frameon=False,bbox_to_anchor=(0.55, -0.6), bbox_transform=ax1.transAxes)
        ax1.add_artist(anchored_text)
        equation1='$Y='+str('%4.2f'%(stat_mod[0])+r"$$\pm$$"+'%4.2f'%(stat_mod[-1]))+'*X'+str('%+4.2f'%(stat_mod[1]))+'$'
        #equation='$Y='+str('%4.2f'%(slope))+'*X'+str('%+4.2f'%(intercept))+'$'
        r_squared1='$R^2='+str('%4.2f'%(stat_mod[2])**2)+'$'
        anchored_text1 = AnchoredText(equation1+'\n'+r_squared1+'\n'+'$r= '+str('%4.2f'%(stat_mod[2]))+'$''\n'+'$p= '+str('%4.4f'%(stat_mod[3]))+'$', loc=3,prop=dict(size=20,fontweight="bold",color='maroon'),frameon=False,bbox_to_anchor=(0.5, -0.6), bbox_transform=ax1.transAxes)
        ax1.add_artist(anchored_text1)
        #for integer numbers on the axis
        #ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
        #or    
        #plt.plot(x,polyval(bla,x), 'r-') 
        plt.tick_params(axis='both', which='major', labelsize=27)
        plt.xlabel(xlab,fontsize=30)
        plt.ylabel(ylab,fontsize=30)
        plt.suptitle(tit, fontsize=30)
        plt.locator_params(nbins=6)
        #limits on the plot, set everything to start with 0 and end with the max value (measured and modelled)
        plt.xlim(0,lims_x[-1])
        plt.ylim(0,lims_y[-1])
        #plt.legend(loc='upper left')
        return plt,stat_meas,stat_mod
    if ev=='Event 1' or ev=='Event 3' or ev=='Event 4' or ev=='Event 5' or ev=='Event 6' or ev=='Event 8' or ev=='Event 9' or ev=='Event 11' or ev=='Event 16':
        fig = plt.figure(figsize=(25,8))
        #fig.subplots_adjust(hspace=.2)
        fig.subplots_adjust(wspace=.25,bottom=0.34)
        ax1=plt.subplot(131)
        ax1,stat_meas1,stat_mod1 = plot_corr(co_i,ch4_i, cog_i,ch4g_i,ch4co_avg,xlab=r'$\Delta$CO (ppb)', ylab=r'$\Delta$CH4 (ppb)',col='indigo', tit=ev)
        ax1=plt.subplot(132)
        ax1,stat_meas2,stat_mod2 = plot_corr(co2_i,ch4_i,co2g_i,ch4g_i, co2ch4_avg, xlab=r'$\Delta$CO2 (ppm)', ylab=r'$\Delta$CH4(ppb)',col='indigo',tit=ev)
        ax1=plt.subplot(133)
        ax1,stat_meas3,stat_mod3= plot_corr(co2_i,co_i, co2g_i,cog_i,coco2_avg,xlab=r'$\Delta$CO2 (ppm)', ylab=r'$\Delta$CO (ppb)',col='indigo', tit=ev)
    elif ev=='Event 7' or ev=='Event 10' or ev=='Event 12' or ev=='Event 13' or ev=='Event 14':
        fig = plt.figure(figsize=(9,8))
        #fig.subplots_adjust(hspace=.2)
        fig.subplots_adjust(wspace=.25,bottom=0.34,left=0.20,right=0.83)
        ax1=plt.subplot(111)
        ax1,stat_meas,stat_mod= plot_corr(co_i,ch4_i, cog_i,ch4g_i,ch4co_avg,xlab=r'$\Delta$CO (ppb)', ylab=r'$\Delta$CH4 (ppb)',col='indigo', tit=ev)
    elif ev=='Event 2':
        fig = plt.figure(figsize=(9,8))
        #fig.subplots_adjust(hspace=.2)
        fig.subplots_adjust(wspace=.25,bottom=0.34,left=0.20,right=0.83)
        ax1=plt.subplot(111)
        ax1,stat_meas,stat_mod= plot_corr(co2_i,co_i, co2g_i,cog_i,coco2_avg,xlab=r'$\Delta$CO2 (ppm)', ylab=r'$\Delta$CO (ppb)',col='indigo', tit=ev)
    else:
        fig = plt.figure(figsize=(9,8))
        #fig.subplots_adjust(hspace=.2)
        fig.subplots_adjust(wspace=.25,bottom=0.34,left=0.20,right=0.83)
        ax1=plt.subplot(111)
        ax1,stat_meas,stat_mod= plot_corr(co2_i,ch4_i,co2g_i,ch4g_i, co2ch4_avg,xlab=r'$\Delta$CO2 (ppm)', ylab=r'$\Delta$CH4(ppb)',col='indigo',tit=ev)
    plt.savefig('/home/bb907/Desktop/Computer/Work/Data/Ship_Train_insitu/Ship_2012_2013/scripts/plots/correlation/'+ev)
    #return the plot and all the STATS
    if ev=='Event 1' or ev=='Event 3' or ev=='Event 4' or ev=='Event 5' or ev=='Event 6' or ev=='Event 8' or ev=='Event 9' or ev=='Event 11' or ev=='Event 16':
        return ax1,stat_meas1,stat_mod1,stat_meas2,stat_mod2,stat_meas3,stat_mod3
    else:
        return ax1,stat_meas,stat_mod
