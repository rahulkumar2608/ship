#THis is to scale the tracers to the total amount of the model output

import numpy as np

def scale(x,sp):
    #this is the total
    print 'Total ', x[0][0]
    #This is the sum of the tracers
    if sp=='CH4':
        #For ch4 it is the sum of all - soil absorption (twice because it is also included in the sum)
        x_g_trac_sum=np.sum(x[1:],axis=0)-2*x[-2]
    if sp=='CO2':
        #For co2 it is the sum of all - net terresttrial - ocean + detrended balanced bioshpere 
        #detrendet bisophere can be both positive and negative, but for now it is OK
        #but since the ocean and net terr are negative already it is just the sum
        # + the background
        x_g_trac_sum=np.sum(x[1:],axis=0)-2*x[6]-2*x[10]
    print 'Tracres Sum ', x_g_trac_sum[0]
    def sc(x1):
        #now calculate the ratio of the tracer and the sum
        ratio=np.array(x1)/x_g_trac_sum
        #now scale that amount to the total amount
        x_scaled=ratio*np.array(x[0])
        return x_scaled
    return sc(x[1]),sc(x[2]),sc(x[3]),sc(x[4]),sc(x[5]),sc(x[6]),sc(x[7]),sc(x[8]),sc(x[9]),sc(x[10]),sc(x[11])


def precentage(x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,sp):
    #This is the sum of the tracers
    if sp=='CH4':
        #For ch4 it is the sum of all - soil absorbtion
        x_g_trac_sum=np.array(x1)+np.array(x2)+np.array(x3)+np.array(x4)+np.array(x5)+np.array(x6)+np.array(x7)+\
        np.array(x8)+np.array(x9)+np.array(x11)-np.array(x10)
    elif sp=='CO2':
        #For ch4 it is the sum of all - soil absorbtion
        x_g_trac_sum=np.array(x1)+np.array(x2)+np.array(x3)+np.array(x4)+np.array(x5)+np.array(x6)+np.array(x7)+\
        np.array(x8)+np.array(x9)+np.array(x10)
    else:
        #For ch4 it is the sum of all - soil absorbtion
        x_g_trac_sum=np.array(x1)+np.array(x2)+np.array(x3)+np.array(x4)+np.array(x5)+np.array(x6)+np.array(x7)+\
        np.array(x8)+np.array(x9)+np.array(x10)+np.array(x11)+np.array(x12)
    def prec(x):
        #now calculate the precentage of the tracer
        x_p=x/x_g_trac_sum*100
        return np.mean(abs(x_p)) #abs because for CO2 there are negative values, and also this sould be the mean to the whole time period
    return prec(x1),prec(x2),prec(x3),prec(x4),prec(x5),prec(x6),prec(x7),prec(x8),prec(x9),prec(x10),prec(x11),prec(x12)
    
    
    
    
#def scale(x_tot,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,sp):
#    #this is the total
#    print 'Total ', x_tot[0]
#    #This is the sum of the tracers
#    if sp=='CH4':
#        #For ch4 it is the sum of all - soil absorbtion
#        x_g_trac_sum=np.array(x1)+np.array(x2)+np.array(x3)+np.array(x4)+np.array(x5)+np.array(x6)+np.array(x7)+\
#        np.array(x8)+np.array(x9)+np.array(x11)-np.array(x10)
#    if sp=='CO2':
#        #For co2it is the sum of all - net terresttrial - ocean
#        x_g_trac_sum=np.array(x1)-np.array(x2)+np.array(x3)+np.array(x4)+np.array(x5)-np.array(x6)+np.array(x7)+\
#        np.array(x8)+np.array(x9)+np.array(x10)
#    print 'Tracres Sum ', x_g_trac_sum[0]
#    def sc(x):
#        #now calculate the ratio of the tracer and the sum
#        ratio=np.array(x)/x_g_trac_sum
#        #now scale that amount to the total amount
#        x_scaled=ratio*np.array(x_tot)
#        return x_scaled
#    return sc(x1),sc(x2),sc(x3),sc(x4),sc(x5),sc(x6),sc(x7),sc(x8),sc(x9),sc(x10),sc(x11),sc(x12)

        