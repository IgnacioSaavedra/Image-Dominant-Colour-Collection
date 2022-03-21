import multiprocessing
import os
import pandas as pd
import matplotlib.image as img
from scipy.cluster.vq import whiten
from scipy.cluster.vq import kmeans
import csv
import numpy as np


def name(fullname):#Name of the file whitout extension
    return os.path.basename(fullname).split('.')[0]




#Recordatorio, cambiar la variable ciudad de ser necesario
def dominant_colours(n,image_list):
    print("Starting Process")
    
    

    #Create lists that will serve as columns
    filenames = []
    colours = []
    colours.append([])
    colours.append([])
    colours.append([])
    colours[0].append([])
    colours[0].append([])
    colours[0].append([])
    colours[1].append([])
    colours[1].append([])
    colours[1].append([])
    colours[2].append([])
    colours[2].append([])
    colours[2].append([])
    color_number = []#How many dominant colours the image has, max 3, min 1
    
    
    maximun_images = 0#Number of images to analyse, 0 means analyse all images in the images folder
    image_counter = 0#How many images have been analysed so far

    for image in image_list:
        filenames.append(image)
        path = 'images'
        image_to_analyse=(r''+path+'/'+image)
        image_to_analyse = img.imread(image_to_analyse)
        r = []
        g = []
        b = []
        for row in image_to_analyse:
            #for temp_r, temp_g, temp_b, temp in row:
            for temp_r, temp_g, temp_b in row:
                r.append(temp_r)
                g.append(temp_g)
                b.append(temp_b)
          
        image_df = pd.DataFrame({'red' : r,
                                  'green' : g,
                                  'blue' : b})
         
        try:
            image_df['scaled_color_red'] = whiten(image_df['red'])
        except:
           image_df['scaled_color_red'] = image_df['red'].astype(float)
        try:   
            image_df['scaled_color_blue'] = whiten(image_df['blue'])
        except:
            image_df['scaled_color_blue'] = image_df['blue'].astype(float)
        try:    
            image_df['scaled_color_green'] = whiten(image_df['green'])
        except: 
            image_df['scaled_color_green'] = image_df['green'].astype(float)
         
        cluster_centers, _ = kmeans(image_df[['scaled_color_red',
                                            'scaled_color_blue',
                                            'scaled_color_green']], 3)
         
        dominant_colors = []
         
        red_std, green_std, blue_std = image_df[['red',
                                                  'green',
                                                  'blue']].std()
         
        for cluster_center in cluster_centers:
            red_scaled, green_scaled, blue_scaled = cluster_center
            dominant_colors.append((
                red_scaled * red_std / 255,
                green_scaled * green_std / 255,
                blue_scaled * blue_std / 255
            ))
            
        
        color_number.append(len(dominant_colors))
        for i in range(len(dominant_colors)):
            colours[i][0].append(dominant_colors[i][0])
            colours[i][1].append(dominant_colors[i][1])
            colours[i][2].append(dominant_colors[i][2])
    
        
        for n in range(3-len(dominant_colors)):#If there are less than 3 colours, add nan
            colours[2-n][0].append(np.nan)
            colours[2-n][1].append(np.nan)
            colours[2-n][2].append(np.nan)
        image_counter=image_counter+1
        if(maximun_images==image_counter):
            break
            
        
    # crear un data frame
    df = pd.DataFrame({"filename": filenames,
                       "colores dominantes": color_number,
                       "colour 1 red":colours[0][0],
                       "colour 1 green":colours[0][1],
                       "colour 1 blue":colours[0][2],
                       "colour 2 red":colours[1][0],
                       "colour 2 green":colours[1][1],
                       "colour 2 blue":colours[1][2],
                       "colour 3 red":colours[2][0],
                       "colour 3 green":colours[2][1],
                       "colour 3 blue":colours[2][2]
                       })
    
    # guardar data frame
    df.to_csv("csv/dominant colours part "+str(n)+".csv", index=False,quoting=csv.QUOTE_NONNUMERIC)



if __name__ == "__main__":    
    number_of_jobs=multiprocessing.cpu_count()
    image_list=[]
    path = 'images'
    for filename in os.listdir(path):
        image_list.append(filename)
    image_number=len(image_list)
    partition_size=int(image_number/number_of_jobs)
    jobs = []
    for i in range(number_of_jobs):
        if i!=number_of_jobs-1:
            images_to_be_used=image_list[i*partition_size:(i+1)*partition_size]
        else:
            images_to_be_used=image_list[i*partition_size:image_number]
    
    
        process = multiprocessing.Process(target=dominant_colours, 
                                          args=(i+1,images_to_be_used))
        jobs.append(process)
    
    for j in jobs:
        (print(j))
        j.start()
    
    # Ensure all of the processes have finished
    for j in jobs:
        (print(j))
        j.join()
    
    df_list = []
    for p in range(number_of_jobs):
        df_list.append(pd.read_csv("csv/dominant colours part "+str(p+1)+".csv", encoding='utf-8'))    
    df = pd.concat(df_list, axis=0)
    df.to_csv("csv/dominant colours.csv", index=False,quoting=csv.QUOTE_NONNUMERIC)
    
    
