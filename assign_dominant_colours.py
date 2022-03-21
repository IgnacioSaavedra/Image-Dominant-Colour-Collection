import pandas as pd
import numpy as np
import math


input_file="csv/dominant colours.csv"

output_file="csv/dominant colours assigned.csv"
                
colour_palette='colour_palette.csv'




def create_dictionary(df_colour):#Assumed column names: r,g,b,name
    dic={(np.nan,np.nan,np.nan):np.nan}
    for i in range(df_colour.shape[0]):
        fila_actual=df_colour.iloc[i,:]
        r=fila_actual["r_value"]
        g=fila_actual["g_value"]
        b=fila_actual["b_value"]
        dic[(r,g,b)]=fila_actual["code"]
    
    return dic


def closest_colour(x,y,z,colour_df):
    dfc=colour_df
    if math.isnan(x) or math.isnan(y) or math.isnan(z):
        return [np.nan,np.nan,np.nan]
    #Calculate distances
    dfc['difx2']=(dfc['r_value']-x).abs()
    dfc['dify2']=(dfc['g_value']-y).abs()
    dfc['difz2']=(dfc['b_value']-z).abs()
    dfc['dist2']=dfc['difx2']+dfc['dify2']+dfc['difz2']
    dfc=dfc.sort_values(by=['dist2'])
    #Return the closes r,g,b values to the x,y,z arguments
    return [dfc.iloc[0,:]['r_value'],dfc.iloc[0,:]['g_value'],dfc.iloc[0,:]['b_value']]

            
colour_palette = pd.read_csv(colour_palette, encoding='utf-8') 





colour_dictionary = create_dictionary(colour_palette)




dominant_colours = pd.read_csv(input_file, encoding='utf-8')

#Replace all rgb values greater than 1 by one

r1s=[]
g1s=[]
b1s=[]
r2s=[]
g2s=[]
b2s=[]
r3s=[]
g3s=[]
b3s=[]

codes_1=[]
codes_2=[]
codes_3=[]
for i in range(dominant_colours.shape[0]):
    row  = dominant_colours.iloc[i,:]
    #print(fila)
    close_colour=closest_colour(row['colour 1 red'],row['colour 1 green'],row['colour 1 blue'],colour_palette)
    r1=close_colour[0]
    g1=close_colour[1]
    b1=close_colour[2]
    if r1>1:
        r1=1
    if g1>1:
        g1=1
    if b1>1:
        b1=1
    r1s.append(r1)
    g1s.append(g1)
    b1s.append(b1)
    codes_1.append(colour_dictionary[(r1,g1,b1)])
    
    try:
        close_colour=closest_colour(row['colour 2 red'],row['colour 2 green'],row['colour 2 blue'],colour_palette)
        r2=close_colour[0]
        g2=close_colour[1]
        b2=close_colour[2]
        if r2>1:
            r2=1
        if g2>1:
            g2=1
        if b2>1:
            b2=1
    except:
        r2=np.nan
        g2=np.nan
        b2=np.nan
    r2s.append(r2)
    g2s.append(g2)
    b2s.append(b2)    
    codes_2.append(colour_dictionary[(r2,g2,b2)])
               
    try:
        close_colour=closest_colour(row['colour 3 red'],row['colour 3 green'],row['colour 3 blue'],colour_palette)
        r3=close_colour[0]
        g3=close_colour[1]
        b3=close_colour[2]
        if r3>1:
            r3=1
        if g3>1:
            g3=1
        if b3>1:
            b3=1
    except:
        r3=np.nan
        g3=np.nan
        b3=np.nan       
    r3s.append(r3)
    g3s.append(g3)
    b3s.append(b3)   
    codes_3.append(colour_dictionary[(r3,g3,b3)])
               
    



    
dominant_colours['color 1 red standard']=r1s
dominant_colours['color 1 green standard']=g1s
dominant_colours['color 1 blue standard']=b1s
dominant_colours['standard colour code 1']=codes_1
dominant_colours['color 2 red standard']=r2s
dominant_colours['color 2 green standard']=g2s
dominant_colours['color 2 blue standard']=b2s
dominant_colours['standard colour code 2']=codes_2
dominant_colours['color 3 red standard']=r3s
dominant_colours['color 3 green standard']=g3s
dominant_colours['color 3 blue standard']=b3s
dominant_colours['standard colour code 3']=codes_3


dominant_colours.to_csv(output_file, index=False)