import matplotlib.pyplot as plt, seaborn as sns
import pandas as pd



input_file="csv/dominant colours assigned.csv"
palette_file='colour_palette.csv'
output_file='colour bar chart'

specified_colours=[]#What colours to use, an empty list by default means use all available colours
max_number_of_colours=0#How many colours to use, 0 by default means use all available colours




for label in ["name","abbreviation"]:
    dominant_colours=pd.read_csv(input_file, encoding='utf-8')
    colour_palette=pd.read_csv(palette_file, encoding='utf-8')
    
    
    dominant_colours['standard colour 1'] = dominant_colours[['color 1 red standard','color 1 green standard','color 1 blue standard']].apply(tuple, axis=1)
    dominant_colours['standard colour 2'] = dominant_colours[['color 2 red standard','color 2 green standard','color 2 blue standard']].apply(tuple, axis=1)
    dominant_colours['standard colour 3'] = dominant_colours[['color 3 red standard','color 3 green standard','color 3 blue standard']].apply(tuple, axis=1)
                  
    standard_colours_1 = dominant_colours.loc[:, ['standard colour 1', 'standard colour code 1']]
    standard_colours_2 = dominant_colours.loc[:, ['standard colour 2', 'standard colour code 2']]
    standard_colours_3 = dominant_colours.loc[:, ['standard colour 3', 'standard colour code 3']] 
    standard_colours_1 = standard_colours_1.rename(columns={'standard colour 1': 'standard colour'})
    standard_colours_2 = standard_colours_2.rename(columns={'standard colour 2': 'standard colour'})
    standard_colours_3 = standard_colours_3.rename(columns={'standard colour 3': 'standard colour'})
    standard_colours_1 = standard_colours_1.rename(columns={'standard colour code 1': 'standard colour code'})
    standard_colours_2 = standard_colours_2.rename(columns={'standard colour code 2': 'standard colour code'})
    standard_colours_3 = standard_colours_3.rename(columns={'standard colour code 3': 'standard colour code'})
                
    standard_colours_1=standard_colours_1.dropna()
    standard_colours_2=standard_colours_2.dropna()
    standard_colours_3=standard_colours_3.dropna()
    standard_colours = pd.concat([standard_colours_1,standard_colours_2,standard_colours_3], axis=0)
    
    
    
    colour_count = standard_colours['standard colour code'].value_counts()
    index_dictionary = colour_palette[['code',label]]
    index_dictionary=dict(zip(index_dictionary['code'],index_dictionary[label]))
    colour_count=colour_count.rename(index=index_dictionary)
    colour_palette['colour'] = colour_palette[['r_value','g_value','b_value']].apply(tuple, axis=1)
    colour_dictionary = colour_palette[[label,'colour']]
    colour_dictionary=dict(zip(colour_dictionary[label], colour_dictionary['colour']))
    
    
    
    
    
    
    if len(specified_colours)==0:
        if max_number_of_colours>0:
            colour_count=standard_colours['codigo color estandar'].value_counts().nlargest(max_number_of_colours)
            colour_count=colour_count.rename(index=index_dictionary)
        grafico=sns.barplot(colour_count.index.tolist(), colour_count.values.tolist(),hue=colour_count.index.tolist(), palette=colour_dictionary,dodge = False,linewidth=1,edgecolor=".2")
        if label=="name":
            grafico.set_xticklabels(grafico.get_xticklabels(), rotation=90)
        plt.legend([],[], frameon=False)
        plt.savefig(output_file+" "+label+".png", bbox_inches="tight")
        plt.clf()
    else:
        specified_colour_count=colour_count[specified_colours]
        grafico=sns.barplot(specified_colour_count.index.tolist(), specified_colour_count.values.tolist(),hue=specified_colour_count.index.tolist(), palette=colour_dictionary,dodge = False,linewidth=1,edgecolor=".2")
        plt.legend([],[], frameon=False) 
        if label=="name":
            grafico.set_xticklabels(grafico.get_xticklabels(), rotation=90)
        plt.savefig(output_file+" "+label+".png", bbox_inches="tight")
        plt.clf()    
        