import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


input_file="csv/dominant colours assigned.csv"
colour_palette='colour_palette.csv'
number_of_elements=15
colours_to_use=[]#List of colours that are to be used exclussively, and empty list means that all colours are to be used


def colour_connection(colour_code, colour_file, palette_file):
    colour_db = pd.read_csv(colour_file, encoding='utf-8')
    colour_palette=pd.read_csv(palette_file, encoding='utf-8')
    return_list=[]
    
    for n in range(colour_palette['code'].max()):#List of counters must be set to 0s
        return_list.append(0)
    for i in range(colour_db.shape[0]):
        row = colour_db.iloc[i,:]
        if row['standard colour code 1']==colour_code or row['standard colour code 2']==colour_code or row['standard colour code 3']==colour_code:
            #print(row['standard colour code 1'],row['standard colour code 2'],row['standard colour code 3'])
            try:
                return_list[int(row['standard colour code 1'])-1]=return_list[int(row['standard colour code 1'])-1]+1
            except:
                 m=''
            try:
                if(row['standard colour code 2']!=row['standard colour code 1']):
                    return_list[int(row['standard colour code 2'])-1]=return_list[int(row['standard colour code 2'])-1]+1
            except:
                 m=''            
            try:
                if((row['standard colour code 3']!=row['standard colour code 1']) and (row['standard colour code 3']!=row['standard colour code 2'])):
                    return_list[int(row['standard colour code 3'])-1]=return_list[int(row['standard colour code 3'])-1]+1
            except:
                m=''
    return_list[int(colour_code-1)]=0
    #print(colour_code)
    #print(return_list)
    return(pd.Series(data=return_list,index=colour_palette['code'].tolist(),name=colour_code))


def create_matrix(column,colour_file,image_name,palette_file,n=0,colour_list=[],log=False,colourmap="Blues"):
    colour_db = pd.read_csv(colour_file, encoding='utf-8')
    colour_palette=pd.read_csv(palette_file, encoding='utf-8')    
    
    if len(colour_list)==0:
        if n==0:
            colour_list=colour_palette['code'].tolist()
        else:
            
            colour_db['color 1 standard'] = colour_db[['color 1 red standard','color 1 green standard','color 1 blue standard']].apply(tuple, axis=1)
            colour_db['color 2 standard'] = colour_db[['color 2 red standard','color 2 green standard','color 2 blue standard']].apply(tuple, axis=1)
            colour_db['color 3 standard'] = colour_db[['color 3 red standard','color 3 green standard','color 3 blue standard']].apply(tuple, axis=1)
              
            standard_colours_1 = colour_db.loc[:, ['color 1 standard', 'standard colour code 1']]
            standard_colours_2 = colour_db.loc[:, ['color 2 standard', 'standard colour code 2']]
            standard_colours_3 = colour_db.loc[:, ['color 3 standard', 'standard colour code 3']] 
            standard_colours_1 = standard_colours_1.rename(columns={'color 1 standard': 'standard colour'})
            standard_colours_2 = standard_colours_2.rename(columns={'color 2 standard': 'standard colour'})
            standard_colours_3 = standard_colours_3.rename(columns={'color 3 standard': 'standard colour'})
            standard_colours_1 = standard_colours_1.rename(columns={'standard colour code 1': 'standard colour code'})
            standard_colours_2 = standard_colours_2.rename(columns={'standard colour code 2': 'standard colour code'})
            standard_colours_3 = standard_colours_3.rename(columns={'standard colour code 3': 'standard colour code'})
            
            standard_colours_1=standard_colours_1.dropna()
            standard_colours_2=standard_colours_2.dropna()
            standard_colours_3=standard_colours_3.dropna()
            standard_colours = pd.concat([standard_colours_1,standard_colours_2,standard_colours_3], axis=0)
            
            colour_list=standard_colours['standard colour code'].value_counts().nlargest(n).index.tolist()
    
    series_list=[]
    for colour in colour_list:

        connections=colour_connection(colour,colour_file,palette_file)

        if n==0:
            series_list.append(connections)
        else:
            series_list.append(connections[connections.index.isin(colour_list)])
    

    
    dataframe=pd.DataFrame(series_list,index=colour_list)
    dataframe=dataframe.sort_index(axis=0)
    dataframe=dataframe.sort_index(axis=1)
    
    palette = pd.read_csv(palette_file, encoding='utf-8')
    index_dictionary = palette[['code',column]]
    index_dictionary = dict(zip(index_dictionary['code'],index_dictionary[column]))
    
    dataframe=dataframe.rename(columns=index_dictionary)
    dataframe=dataframe.rename(index=index_dictionary)
    
    if log==True:
        dataframe=dataframe.fillna(1)
        dataframe=dataframe.replace(0, 1)
        dataframe=np.log(dataframe)
    else:
        dataframe=dataframe.fillna(0)
    print(sns.heatmap(dataframe, cmap=colourmap))
    plt.savefig(image_name, bbox_inches="tight")
    plt.clf()
    
    
    

create_matrix('name',input_file,'heatmap colour name.png',colour_palette,n=number_of_elements)
create_matrix('abbreviation',input_file,'heatmap colour abbreviation.png',colour_palette,n=number_of_elements)
create_matrix('name',input_file,'heatmap colour name log scaling.png',colour_palette,n=number_of_elements,log=True)
create_matrix('abbreviation',input_file,'heatmap colour abbreviation log scaling.png',colour_palette,n=number_of_elements,log=True) 