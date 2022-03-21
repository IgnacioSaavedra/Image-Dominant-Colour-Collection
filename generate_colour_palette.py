import pandas as pd
import csv



def crear_df(n):
    counter=1
    r_values=[]
    g_values=[]
    b_values=[]
    codes=[]
    
    for r in range(n):
        for g in range(n):
            for b in range(n):
                
                red = r/(n-1)
                green = g/(n-1)
                blue = b/(n-1)
                
                r_values.append(red)
                g_values.append(green)
                b_values.append(blue)
                codes.append(counter)
                
                counter=counter+1
    df = pd.DataFrame({"code": codes,
                   "r_value": r_values,
                   "g_value": g_values,
                   "b_value": b_values
                   })

    df.to_csv("colour_palette.csv", index=False,quoting=csv.QUOTE_NONNUMERIC)


crear_df(3)     