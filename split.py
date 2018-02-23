import numpy as np

#measurements
def split_meas(x1,x2,x3,x4,x5,ind,first):
    if first=='Y':
        return x1[:ind],x2[:ind],x3[:ind],x4[:ind],x5[:ind]
    else:
        return x1[ind:],x2[ind:],x3[ind:],x4[ind:],x5[ind:]
        
        
#model
def split_mod(x,ind,first):
    x_new=[]
    for i in range(len(x)):
        if first=='Y':
            x_new.append(x[i][:ind])
            #print x_new
        else:
            x_new.append(x[i][ind:])    
    return x_new