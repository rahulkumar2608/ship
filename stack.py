#stack plots for the source contribution
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot as gridspec, lines

def stack_ch4(lata,ch4_meas,ch4_tota, ch4_oga,ch4_cma,ch4_lsa,ch4_waa,ch4_bfa,ch4_ria,ch4_ana,ch4_bba,ch4_wea,ch4_saa,ch4_nata,lc,t,h):
    width = 1.2    # the width of the bars: can also be len(x) sequence
    #plt.bar(lat, ch4_tot, width, color='#a90308')
    #SOURCES
    plt.plot(lata, ch4_meas, linewidth=8, color=lc[0][1], alpha=0.65, label=lc[0][0])
    plt.plot(lata, ch4_tota, linewidth=8 ,color=lc[1][1], alpha=0.65, label=lc[1][0])   
    plt.tick_params(axis='both', which='major', labelsize=60)
    plt.bar(lata, ch4_oga,  width, color=lc[2][1],  align='center', label=lc[2][0])
    plt.bar(lata, ch4_cma,  width, color=lc[3][1],  align='center', label=lc[3][0],  bottom=ch4_oga)
    plt.bar(lata, ch4_waa,  width, color=lc[5][1],  align='center', label=lc[5][0],  bottom=ch4_oga+ch4_cma)
    #plt.bar(lata, ch4_bfa,  width, color=lc[6][1], align='center', label='lc[6][0], bottom=ch4_oga+ch4_cma+ch4_waa)
    plt.bar(lata, ch4_lsa,  width, color=lc[4][1],  align='center', label=lc[4][0],  bottom=ch4_oga+ch4_cma+ch4_waa)
    #plt.bar(lata, ch4_ana,  width, color=lc[8][1], align='center', label=lc[8][0],  bottom=ch4_oga+ch4_cma+ch4_waa+ch4_bfa+ch4_lsa)
    plt.bar(lata, ch4_bba,  width, color=lc[9][1],  align='center', label=lc[9][0],  bottom=ch4_oga+ch4_cma+ch4_waa+ch4_lsa)      
    plt.bar(lata, ch4_wea,  width, color=lc[10][1], align='center', label=lc[10][0], bottom=ch4_oga+ch4_cma+ch4_waa+ch4_lsa+ch4_bba)
    plt.bar(lata, ch4_ria,  width, color=lc[7][1],  align='center', label=lc[7][0],  bottom=ch4_oga+ch4_cma+ch4_waa+ch4_lsa+ch4_bba+ch4_wea)
    plt.bar(lata, ch4_nata, width, color=lc[12][1], align='center', label=lc[12][0], bottom=ch4_oga+ch4_cma+ch4_waa+ch4_lsa+ch4_bba+ch4_wea+ch4_ria)        
    #SINKS+
    plt.bar(lata, ch4_saa*(-1),  width, color=lc[11][1],  align='center',label=lc[11][0])
    if t=='bm':
        plt.legend()       
    if h=='rel':
        plt.ylim(-2,45)
    plt.xlim(-45,-8)
    plt.xlabel('Latitude', fontsize=45)
    if t=='am':
        plt.ylabel(r'$\Delta$CH4 [ppbv]', fontsize=45)
    return plt


def stack_co2(lata,co2_meas,co2_tota, co2_ffa,co2_oca,co2_bala,co2_bba,co2_bfa,co2_ntea,co2_sea,co2_ava,co2_cha,co2_corra,co2_bckg,lc,t,h):
    width = 1.2    # the width of the bars: can also be len(x) sequence
    plt.plot(lata, co2_meas, linewidth=8, color=lc[0][1], alpha=0.65, label=lc[0][0])
    plt.plot(lata, co2_tota, linewidth=8, color=lc[1][1], alpha=0.65,label=lc[1][0])
    #plt.set_ylim(0,5)
    #plt.set_xlabel('Latitude')
    #plt.set_ticks(np.arange(0, 4, 1))
    #SOURCES
    plt.tick_params(axis='both', which='major', labelsize=60)  
    plt.bar(lata, co2_bckg, width, color=lc[12][1], align='center', label=lc[12][0])            
    plt.bar(lata, co2_ffa,  width, color=lc[2][1],  align='center', label=lc[2][0],  bottom=co2_bckg)          
    #plt.bar(lata, co2_sea,  width, color=lc[8][1], align='center', label=lc[8][0],  bottom=co2_bckg+co2_ffa)
    #plt.bar(lata, co2_ava,  width, color=lc[9][1], align='center', label=lc[9][0],  bottom=co2_bckg+co2_ffa+co2_sea)
    plt.bar(lata, co2_bfa,  width, color=lc[6][1],  align='center', label=lc[6][0],  bottom=co2_bckg+co2_ffa)
    plt.bar(lata, co2_bba,  width, color=lc[5][1],  align='center', label=lc[5][0],  bottom=co2_bckg+co2_ffa+co2_bfa)
    #plt.bar(lata, co2_corra,width, color=lc[11][1],align='center', label=lc[11][0], bottom=co2_ffa+co2_sea+co2_ava+co2_bfa+co2_bba)
    #plt.bar(lata, co2_cha,  width, color=lc[10][1],align='center', label=lc[10][0], bottom=co2_bckg+co2_ffa+co2_sea+co2_ava+co2_bfa+co2_bba)   
    #SINKS
    plt.bar(lata, co2_ntea*(-1), width, color=lc[7][1],align='center',label=lc[7][0])
    plt.bar(lata, co2_oca*(-1),  width, color=lc[3][1],align='center',label=lc[3][0], bottom=co2_ntea*(-1))
    #sink and source
    plt.bar(np.nan,np.nan, width, color=lc[4][1], align='center',     label=lc[4][0])
    for i in range(len(co2_bala)):
        if co2_bala[i]>0:
            plt.bar(lata[i], co2_bala[i], width, color=lc[4][1],align='center',       bottom=co2_bckg[i]+co2_ffa[i]+co2_bfa[i]+co2_bba[i])
        else:
            plt.bar(lata[i], co2_bala[i], width, color=lc[4][1],align='center',       bottom=co2_ntea[i]*(-1)+co2_oca[i]*(-1))
    if t=='bm':
        plt.legend() 
    if h=='rel':
        plt.ylim(-2.5,9)
    plt.xlim(-45,-8)
    plt.xlabel('Latitude', fontsize=45)
    if t=='am':
        plt.ylabel(r'$\Delta$CO2 [ppmv]', fontsize=45)
    return plt
      
#no background tracer
def stack_co2_NOB(lata,co2_meas,co2_tota, co2_ffa,co2_oca,co2_bala,co2_bba,co2_bfa,co2_ntea,co2_sea,co2_ava,co2_cha,co2_corra,co2_bckg,lc,t,h):
    width = 1.2    # the width of the bars: can also be len(x) sequence
    plt.plot(lata, co2_meas, linewidth=8, color=lc[0][1], alpha=0.65, label=lc[0][0])
    plt.plot(lata, co2_tota, linewidth=8, color=lc[1][1], alpha=0.65,label=lc[1][0])
    #plt.set_ylim(0,5)
    #plt.set_xlabel('Latitude')
    #plt.set_ticks(np.arange(0, 4, 1))
    #SOURCES
    plt.tick_params(axis='both', which='major', labelsize=60)  
    #plt.bar(lata, co2_bckg, width, color=lc[12][1], align='center', label=lc[12][0])            
    plt.bar(lata, co2_ffa,  width, color=lc[2][1],  align='center', label=lc[2][0])          
    #plt.bar(lata, co2_sea,  width, color=lc[8][1], align='center', label=lc[8][0],  bottom=co2_bckg+co2_ffa)
    #plt.bar(lata, co2_ava,  width, color=lc[9][1], align='center', label=lc[9][0],  bottom=co2_bckg+co2_ffa+co2_sea)
    plt.bar(lata, co2_bfa,  width, color=lc[6][1],  align='center', label=lc[6][0],  bottom=co2_ffa)
    plt.bar(lata, co2_bba,  width, color=lc[5][1],  align='center', label=lc[5][0],  bottom=co2_ffa+co2_bfa)
    #plt.bar(lata, co2_corra,width, color=lc[11][1],align='center', label=lc[11][0], bottom=co2_ffa+co2_sea+co2_ava+co2_bfa+co2_bba)
    #plt.bar(lata, co2_cha,  width, color=lc[10][1],align='center', label=lc[10][0], bottom=co2_bckg+co2_ffa+co2_sea+co2_ava+co2_bfa+co2_bba)   
    #SINKS
    plt.bar(lata, co2_ntea*(-1), width, color=lc[7][1],align='center',label=lc[7][0])
    plt.bar(lata, co2_oca*(-1),  width, color=lc[3][1],align='center',label=lc[3][0], bottom=co2_ntea*(-1))
    #sink and source
    plt.bar(np.nan,np.nan, width, color=lc[4][1], align='center',     label=lc[4][0])
    for i in range(len(co2_bala)):
        if co2_bala[i]>0:
            plt.bar(lata[i], co2_bala[i], width, color=lc[4][1],align='center',       bottom=+co2_ffa[i]+co2_bfa[i]+co2_bba[i])
        else:
            plt.bar(lata[i], co2_bala[i], width, color=lc[4][1],align='center',       bottom=co2_ntea[i]*(-1)+co2_oca[i]*(-1))
    if t=='bm':
        plt.legend() 
    if h=='rel':
        plt.ylim(-2.5,6)
    plt.xlim(-45,-8)
    plt.xlabel('Latitude', fontsize=45)
    if t=='am':
        plt.ylabel(r'$\Delta$CO2 [ppmv]', fontsize=45)
    return plt    
    
def stack_co(lata,co_meas, co_tota,co_ausa,co_afra,co_sama,co_otha,co_bbsama,co_bbafa,co_bbnhasa,co_bbausa,\
             co_bbindoa,co_bbotha,co_ch4a,co_nmvoc,lc,t,h):
    width = 1.2    # the width of the bars: can also be len(x) sequence
    #plt.bar(lat, ch4_tot, width, color='#a90308')
    plt.plot(lata, co_meas, linewidth=8,alpha=0.65, color=lc[0][1], label=lc[0][0])
    plt.plot(lata, co_tota, linewidth=8, alpha=0.65,color=lc[1][1], label=lc[1][0])
    #ax1.set_ylabel('CO', color='black')
    #ax1.tick_params('y', colors='black')
    #ax1.tick_params('x', colors='black')
    #ax1.set_xlabel('Latitude', fontsize=25)
    #ax1.set_ylim(0,75)
    plt.tick_params(axis='both', which='major', labelsize=60)   
    plt.bar(lata, co_ausa,  width, color=lc[2][1],  align='center', label=lc[2][0])
    plt.bar(lata, co_sama,  width, color=lc[4][1],  align='center', label=lc[4][0],  bottom=co_ausa)
    plt.bar(lata, co_otha,  width, color=lc[5][1],  align='center', label=lc[5][0],  bottom=co_ausa+co_sama)
    plt.bar(lata, co_afra,  width, color=lc[3][1],  align='center', label=lc[3][0],  bottom=co_ausa+co_sama+co_otha) 
    plt.bar(lata, co_bbausa,width, color=lc[9][1],  align='center', label=lc[9][0],  bottom=co_ausa+co_sama+co_otha+co_afra)
    plt.bar(lata, co_bbafa, width, color=lc[7][1],  align='center', label=lc[7][0],  bottom=co_ausa+co_sama+co_otha+co_afra+co_bbausa)
    plt.bar(lata, co_bbsama,width, color=lc[6][1],  align='center', label=lc[6][0],  bottom=co_ausa+co_sama+co_otha+co_afra+co_bbausa+co_bbafa)   
    #plt.bar(lata, co_bbnhasa,width,color=lc[8][1], align='center', label=lc[8][0],  bottom=co_ausa+co_sama+co_otha+co_afra+co_bbausa+co_bbafa+co_bbsama)
    #plt.bar(lata, co_bbindoa,width,color=lc[10][1],align='center', label=lc[10][0], bottom=co_ausa+co_sama+co_otha+co_afra+co_bbausa+co_bbafa+co_bbsama+co_bbnhasa)
    plt.bar(lata, co_bbotha,width, color=lc[11][1], align='center', label=lc[11][0], bottom=co_ausa+co_sama+co_otha+co_afra+co_bbausa+co_bbafa+co_bbsama)
    plt.bar(lata, co_ch4a,  width, color=lc[12][1], align='center', label=lc[12][0], bottom=co_ausa+co_sama+co_otha+co_afra+co_bbausa+co_bbafa+co_bbsama+co_bbotha)
    plt.bar(lata, co_nmvoc,  width,color=lc[13][1], align='center', label=lc[13][0], bottom=co_ausa+co_sama+co_otha+co_afra+co_bbausa+co_bbafa+co_bbsama+co_bbotha+co_ch4a)
    #ax.set_xticks(lata)
    #ax1.set_ylabel('Arbitary units', color='#a90308', fontsize=30)  
    #ax1.set_ylim(0,55)
    #ax1.yaxis.set_major_formatter(plt.NullFormatter())
    if t=='bm':
        plt.legend()
    if h=='rel':
        plt.ylim(0,60)
    plt.xlim(-45,-8)
    plt.xlabel('Latitude', fontsize=45)
    if t=='am':
        plt.ylabel(r'$\Delta$CO [ppbv]', fontsize=45)
    #plt.suptitle(str(trip))
    #plt.title(t)
    #ax1.set_zorder(ax1.get_zorder()+1) # put ax in front of ax2
    #ax1.patch.set_visible(False) # hide the 'canvas'    
    return plt

##ALL values
def stack_ch4_all(lata,ch4_meas,ch4_tota, ch4_oga,ch4_cma,ch4_lsa,ch4_waa,ch4_bfa,ch4_ria,ch4_ana,ch4_bba,ch4_wea,ch4_saa,ch4_nata,lc,t,h):
    width = 0.8    # the width of the bars: can also be len(x) sequence
    #plt.bar(lat, ch4_tot, width, color='#a90308')
    #SOURCES
    plt.plot(lata, ch4_meas, linewidth=8, color=lc[0][1], alpha=0.65, label=lc[0][0])
    plt.plot(lata, ch4_tota, linewidth=8 ,color=lc[1][1], alpha=0.65, label=lc[1][0])   
    plt.tick_params(axis='both', which='major', labelsize=60)
    plt.bar(lata, ch4_oga,  width, color=lc[2][1],  align='center', label=lc[2][0])
    plt.bar(lata, ch4_cma,  width, color=lc[3][1],  align='center', label=lc[3][0],  bottom=ch4_oga)
    plt.bar(lata, ch4_waa,  width, color=lc[5][1],  align='center', label=lc[5][0],  bottom=ch4_oga+ch4_cma)
    plt.bar(lata, ch4_bfa,  width, color=lc[6][1], align='center',  label=lc[6][0], bottom=ch4_oga+ch4_cma+ch4_waa)
    plt.bar(lata, ch4_lsa,  width, color=lc[4][1],  align='center', label=lc[4][0],  bottom=ch4_oga+ch4_cma+ch4_waa+ch4_bfa)
    plt.bar(lata, ch4_ana,  width, color=lc[8][1], align='center',  label=lc[8][0],  bottom=ch4_oga+ch4_cma+ch4_waa+ch4_bfa+ch4_lsa)
    plt.bar(lata, ch4_bba,  width, color=lc[9][1],  align='center', label=lc[9][0],  bottom=ch4_oga+ch4_cma+ch4_waa+ch4_bfa+ch4_lsa+ch4_ana)      
    plt.bar(lata, ch4_wea,  width, color=lc[10][1], align='center', label=lc[10][0], bottom=ch4_oga+ch4_cma+ch4_waa+ch4_bfa+ch4_lsa+ch4_ana+ch4_bba)
    plt.bar(lata, ch4_ria,  width, color=lc[7][1],  align='center', label=lc[7][0],  bottom=ch4_oga+ch4_cma+ch4_waa+ch4_bfa+ch4_lsa+ch4_ana+ch4_bba+ch4_wea)
    plt.bar(lata, ch4_nata, width, color=lc[12][1], align='center', label=lc[12][0], bottom=ch4_oga+ch4_cma+ch4_waa+ch4_bfa+ch4_lsa+ch4_ana+ch4_bba+ch4_wea+ch4_ria)        
    #SINKS+
    plt.bar(lata, ch4_saa*(-1),  width, color=lc[11][1],  align='center',label=lc[11][0])
    if t=='bm':
        plt.legend()       
    #if h=='rel':
        #plt.ylim(-2,45)
    plt.xlim(-45,-8)
    plt.xlabel('Latitude', fontsize=45)
    if t=='am':
        plt.ylabel(r'$\Delta$CH4 [ppbv]', fontsize=45)
    return plt


def stack_co2_all(lata,co2_meas,co2_tota, co2_ffa,co2_oca,co2_bala,co2_bba,co2_bfa,co2_ntea,co2_sea,co2_ava,co2_cha,co2_corra,co2_bckg,lc,t,h):
    width = 0.8    # the width of the bars: can also be len(x) sequence
    plt.plot(lata, co2_meas, linewidth=8, color=lc[0][1], alpha=0.65, label=lc[0][0])
    plt.plot(lata, co2_tota, linewidth=8, color=lc[1][1], alpha=0.65,label=lc[1][0])
    #plt.set_ylim(0,5)
    #plt.set_xlabel('Latitude')
    #plt.set_ticks(np.arange(0, 4, 1))
    #SOURCES
    plt.tick_params(axis='both', which='major', labelsize=60)  
    #plt.bar(lata, co2_bckg, width, color=lc[12][1], align='center', label=lc[12][0])            
    plt.bar(lata, co2_ffa,  width, color=lc[2][1],  align='center', label=lc[2][0])          
    plt.bar(lata, co2_sea,  width, color=lc[8][1],  align='center', label=lc[8][0],  bottom=co2_ffa)
    plt.bar(lata, co2_ava,  width, color=lc[9][1],  align='center', label=lc[9][0],  bottom=co2_ffa+co2_sea)
    plt.bar(lata, co2_bfa,  width, color=lc[6][1],  align='center', label=lc[6][0],  bottom=co2_ffa+co2_sea+co2_ava)
    plt.bar(lata, co2_bba,  width, color=lc[5][1],  align='center', label=lc[5][0],  bottom=co2_ffa+co2_sea+co2_ava+co2_bfa)
    plt.bar(lata, co2_corra,width, color=lc[11][1], align='center', label=lc[11][0], bottom=co2_ffa+co2_sea+co2_ava+co2_bfa+co2_bba)
    plt.bar(lata, co2_cha,  width, color=lc[10][1], align='center', label=lc[10][0], bottom=co2_ffa+co2_sea+co2_ava+co2_bfa+co2_bba+co2_corra)   
    #SINKS
    plt.bar(lata, co2_ntea*(-1), width, color=lc[7][1],align='center',label=lc[7][0])
    plt.bar(lata, co2_oca*(-1),  width, color=lc[3][1],align='center',label=lc[3][0], bottom=co2_ntea*(-1))
    #sink and source
    plt.bar(np.nan,np.nan, width, color=lc[4][1], align='center',     label=lc[4][0])
    for i in range(len(co2_bala)):
        if co2_bala[i]>0:
            plt.bar(lata[i], co2_bala[i], width, color=lc[4][1],align='center',       bottom=+co2_ffa[i]+co2_sea[i]++co2_ava[i]+co2_bfa[i]+co2_bba[i]+co2_corra[i])
        else:
            plt.bar(lata[i], co2_bala[i], width, color=lc[4][1],align='center',       bottom=co2_ntea[i]*(-1)+co2_oca[i]*(-1))
    if t=='bm':
        plt.legend() 
    #if h=='rel':
        #plt.ylim(-2.5,9)
    plt.xlim(-45,-8)
    plt.xlabel('Latitude', fontsize=45)
    if t=='am':
        plt.ylabel(r'$\Delta$CO2 [ppmv]', fontsize=45)
    return plt
      

def stack_co_all(lata,co_meas, co_tota,co_ausa,co_afra,co_sama,co_otha,co_bbsama,co_bbafa,co_bbnhasa,co_bbausa,\
             co_bbindoa,co_bbotha,co_ch4a,co_nmvoc,lc,t,h):
    width = 0.8    # the width of the bars: can also be len(x) sequence
    #plt.bar(lat, ch4_tot, width, color='#a90308')
    plt.plot(lata, co_meas, linewidth=8,alpha=0.65, color=lc[0][1], label=lc[0][0])
    plt.plot(lata, co_tota, linewidth=8, alpha=0.65,color=lc[1][1], label=lc[1][0])
    #ax1.set_ylabel('CO', color='black')
    #ax1.tick_params('y', colors='black')
    #ax1.tick_params('x', colors='black')
    #ax1.set_xlabel('Latitude', fontsize=25)
    #ax1.set_ylim(0,75)
    plt.tick_params(axis='both', which='major', labelsize=60)   
    plt.bar(lata, co_ausa,  width, color=lc[2][1],  align='center', label=lc[2][0])
    plt.bar(lata, co_sama,  width, color=lc[4][1],  align='center', label=lc[4][0],  bottom=co_ausa)
    plt.bar(lata, co_otha,  width, color=lc[5][1],  align='center', label=lc[5][0],  bottom=co_ausa+co_sama)
    plt.bar(lata, co_afra,  width, color=lc[3][1],  align='center', label=lc[3][0],  bottom=co_ausa+co_sama+co_otha) 
    plt.bar(lata, co_bbausa,width, color=lc[9][1],  align='center', label=lc[9][0],  bottom=co_ausa+co_sama+co_otha+co_afra)
    plt.bar(lata, co_bbafa, width, color=lc[7][1],  align='center', label=lc[7][0],  bottom=co_ausa+co_sama+co_otha+co_afra+co_bbausa)
    plt.bar(lata, co_bbsama,width, color=lc[6][1],  align='center', label=lc[6][0],  bottom=co_ausa+co_sama+co_otha+co_afra+co_bbausa+co_bbafa)   
    plt.bar(lata, co_bbnhasa,width,color=lc[8][1],  align='center', label=lc[8][0],  bottom=co_ausa+co_sama+co_otha+co_afra+co_bbausa+co_bbafa+co_bbsama)
    plt.bar(lata, co_bbindoa,width,color=lc[10][1], align='center', label=lc[10][0], bottom=co_ausa+co_sama+co_otha+co_afra+co_bbausa+co_bbafa+co_bbsama+co_bbnhasa)
    plt.bar(lata, co_bbotha,width, color=lc[11][1], align='center', label=lc[11][0], bottom=co_ausa+co_sama+co_otha+co_afra+co_bbausa+co_bbafa+co_bbsama+co_bbnhasa+co_bbindoa)
    plt.bar(lata, co_ch4a,  width, color=lc[12][1], align='center', label=lc[12][0], bottom=co_ausa+co_sama+co_otha+co_afra+co_bbausa+co_bbafa+co_bbsama+co_bbnhasa+co_bbindoa+co_bbotha)
    plt.bar(lata, co_nmvoc,  width,color=lc[13][1], align='center', label=lc[13][0], bottom=co_ausa+co_sama+co_otha+co_afra+co_bbausa+co_bbafa+co_bbsama+co_bbnhasa+co_bbindoa+co_bbotha+co_ch4a)
    #ax.set_xticks(lata)
    #ax1.set_ylabel('Arbitary units', color='#a90308', fontsize=30)  
    #ax1.set_ylim(0,55)
    #ax1.yaxis.set_major_formatter(plt.NullFormatter())
    if t=='bm':
        plt.legend()
    #if h=='rel':
        #plt.ylim(0,60)
    plt.xlim(-45,-8)
    plt.xlabel('Latitude', fontsize=45)
    if t=='am':
        plt.ylabel(r'$\Delta$CO [ppbv]', fontsize=45)
    #plt.suptitle(str(trip))
    #plt.title(t)
    #ax1.set_zorder(ax1.get_zorder()+1) # put ax in front of ax2
    #ax1.patch.set_visible(False) # hide the 'canvas'    
    return plt



    
#the averaged
   
#def stack_ch4_avg(lata, ch4_wea,ch4_lsa,ch4_oga,ch4_waa,ch4_cma,ch4_ria,ch4_bba,ch4_saa,ch4_nata,ch4_bfa,ch4_ana, ch4_weas,ch4_lsas,ch4_ogas,ch4_waas,ch4_cmas,ch4_rias,ch4_bbas,ch4_saas,ch4_natas,ch4_bfas,ch4_anas):
#    width = 0.8      # the width of the bars: can also be len(x) sequence
#    fig = plt.figure()
#    plt.bar(lata, ch4_wea,  width, color='#a90308', label='ch4_wea',yerr=ch4_weas,ecolor='black')
#    plt.bar(lata, ch4_lsa,  width, color='grey',    label='ch4_lsa',bottom=ch4_wea,yerr=ch4_lsas,ecolor='black')
#    plt.bar(lata, ch4_oga,  width, color='#ffb07c', label='ch4_oga',bottom=ch4_lsa+ch4_wea,yerr=ch4_ogas,ecolor='black')
#    plt.bar(lata, ch4_waa,  width, color='#29465b', label='ch4_waa',bottom=ch4_oga+ch4_lsa+ch4_wea,yerr=ch4_waas,ecolor='black')
#    plt.bar(lata, ch4_cma,  width, color='#acc2d9', label='ch4_cma',bottom=ch4_waa+ch4_oga+ch4_lsa+ch4_wea,yerr=ch4_cmas,ecolor='black')
#    plt.bar(lata, ch4_ria,  width, color='black', label='ch4_ria',bottom=ch4_cma+ch4_waa+ch4_oga+ch4_lsa+ch4_wea,yerr=ch4_rias,ecolor='black')
#    plt.bar(lata, ch4_bba,  width, color='#a484ac', label='ch4_bba',bottom=ch4_ria+ch4_cma+ch4_waa+ch4_oga+ch4_lsa+ch4_wea,yerr=ch4_bbas,ecolor='black')
#    plt.bar(lata, ch4_saa,  width, color='#fce166', label='ch4_saa',bottom=ch4_bba+ch4_ria+ch4_cma+ch4_waa+ch4_oga+ch4_lsa+ch4_wea,yerr=ch4_saas,ecolor='black')
#    plt.bar(lata, ch4_nata,  width, color='#86a175', label='ch4_nata',bottom=ch4_saa+ch4_bba+ch4_ria+ch4_cma+ch4_waa+ch4_oga+ch4_lsa+ch4_wea,yerr=ch4_natas,ecolor='black')
#    plt.bar(lata, ch4_bfa,  width, color='#d5869d', label='ch4_bfa',bottom=ch4_nata+ch4_saa+ch4_bba+ch4_ria+ch4_cma+ch4_waa+ch4_oga+ch4_lsa+ch4_wea,yerr=ch4_bfas,ecolor='black')
#    plt.bar(lata, ch4_ana,  width, color='#2b5d34', label='ch4_ana',bottom=ch4_ana+ch4_nata+ch4_saa+ch4_bba+ch4_ria+ch4_cma+ch4_waa+ch4_oga+ch4_lsa+ch4_wea,yerr=ch4_anas,ecolor='black')   
#    plt.ylabel('CH4')
#    plt.xlabel('Latitude')
#    plt.legend()
#    plt.suptitle('averaged')
#    plt.ylim(0,1500)
#    return plt
#    
#    
#def stack_co2_avg(lata, co2_bala,co2_ffa,co2_bba,co2_bfa,co2_sea,co2_ava,co2_oca,co2_corra,co2_ntea,co2_cha,co2_bals,co2_ffs,co2_bbs,co2_bfs,co2_ses,co2_avs,co2_ocs,co2_corrs,co2_ntes,co2_chs):
#    width = 0.8      # the width of the bars: can also be len(x) sequence
#    fig ,ax= plt.subplots()
#    #plt.bar(lat, ch4_tot, width, color='#a90308')
#    #make sure to start with the highest values or it will overplot it 
#    plt.bar(lata, co2_bala, width, color='#a90308', label='co2_bala',yerr=co2_bals,ecolor='black')
#    plt.bar(lata, co2_ffa,  width, color='grey',    label='co2_ffa', bottom=co2_bala,yerr=co2_ffs,ecolor='black')
#    plt.bar(lata, co2_bba,  width, color='#ffb07c', label='co2_bba', bottom=co2_bala+co2_ffa,yerr=co2_bbs,ecolor='black')
#    plt.bar(lata, co2_bfa,  width, color='#29465b', label='co2_bfa', bottom=co2_bala+co2_ffa+co2_bba,yerr=co2_bfs,ecolor='black')
#    plt.bar(lata, co2_sea,  width, color='#acc2d9', label='co2_sea', bottom=co2_bala+co2_ffa+co2_bba+co2_bfa,yerr=co2_ses,ecolor='black')
#    plt.bar(lata, co2_ava,  width, color='black',   label='co2_ava', bottom=co2_bala+co2_ffa+co2_bba+co2_bfa+co2_sea,yerr=co2_avs,ecolor='black')
#    plt.bar(lata, co2_oca,  width, color='#a484ac', label='co2_oca', bottom=co2_bala+co2_ffa+co2_bba+co2_bfa+co2_sea+co2_ava,yerr=co2_ocs,ecolor='black')
#    plt.bar(lata, co2_corra,width, color='#fce166', label='co2_corra', bottom=co2_bala+co2_ffa+co2_bba+co2_bfa+co2_sea+co2_ava+co2_oca,yerr=co2_corrs,ecolor='black')
#    plt.bar(lata, co2_ntea, width, color='#86a175', label='co2_ntea', bottom=co2_bala+co2_ffa+co2_bba+co2_bfa+co2_sea+co2_ava+co2_oca+co2_corra,yerr=co2_ntes,ecolor='black')
#    plt.bar(lata, co2_cha,  width, color='#d5869d', label='co2_cha', bottom=co2_bala+co2_ffa+co2_bba+co2_bfa+co2_sea+co2_ava+co2_oca+co2_corra+co2_ntea,yerr=co2_chs,ecolor='black')
#    #ax.set_xticks(lata)
#    plt.ylabel('CO2')
#    plt.xlabel('Latitude')
#    plt.legend()
#    plt.suptitle('averaged')
#    plt.ylim(0,600)
#    return plt
#    

