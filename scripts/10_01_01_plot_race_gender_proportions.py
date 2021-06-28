# -*- coding: utf-8 -*-
"""
Summary: 
	In this script I will perform the network analysis of the comention network
Input:
	./outputs/data/05_01_01
Output:
	Some outputs
"""

import pandas as pd
import json
from collections import defaultdict
from unidecode import unidecode
import unicodedata
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
pd.options.display.width = 0

# %%
output_code = "10_01_01"

# %%
## Adding the metadata of each entity
df = pd.read_csv(f"../outputs/data/08_01_01_entity_race_gender_expertise_news_count.csv", na_filter=False)
dict_sex_count = df["sex"].value_counts().to_dict()

title_fontsize = 15
label_fontsize = 12
legend_fontsize = 10

def func(pct, allvals):
    #absolute = int(pct/100.*np.sum(allvals))
    #return "{:.1f}% ({:d} )".format(pct, absolute)
    return "{:.1f} %".format(pct)
def my_autopct(pct):
    return ('%.2f' % pct) if pct > 6 else ''


attributes = ["sex","race","pronoun"]
for attribute in attributes:
	#attribute = "race"
	df_pie_chart = df[attribute].value_counts().reset_index().rename(columns={'index': attribute, 0: 'count', attribute: "count"})
	color_dict = {
						"sex": {'Male': '#e64550', 'Female': '#1f97ce'},
						"race":{
							"Unknown":"#000000",
							"Other/Mixed":"#E69F00",
							"Aboriginal/Native American":"#56B4E9",
							"Middle Eastern":"#009E73",
							"Black/African":"#F0E442",
							"Latinx":"#0072B2",
							"South Asian":"#D55E00",
							"East Asian":"#CC79A7",
							"White/European":"#696969"
						},
						"pronoun":{'He': '#CC79A7', 'She': '#0072B2', "No info": "#696969", "They":"#009E73", "Other":"#D55E00"},
					}	
	pie_type,count = df_pie_chart[attribute].values, df_pie_chart["count"].values
	colors = None
	if color_dict[attribute]:
		colors = [color_dict[attribute][g] for g in pie_type]
	prob = np.array(count) / sum(count)

	#Create our plot and resize it.
	#explode = [0,0.05]

	# borrowing from the following
	# https://www.machinelearningplus.com/plots/top-50-matplotlib-visualizations-the-master-plots-python/
	fig,ax = plt.subplots(1,1)
	wedges, texts, autotexts = ax.pie(count, 
	                              autopct=my_autopct, # https://stackoverflow.com/questions/34035427/conditional-removal-of-labels-in-matplotlib-pie-chart/34035864
	                              textprops=dict(color="w",size=label_fontsize), 
	                              colors=colors,
	                              startangle=40,
	                              #explode=explode,
	                              )
	ax.legend(wedges, [x.capitalize() for x in pie_type], loc="center left", bbox_to_anchor=(0.90, 0, 0.25, 1), fontsize = legend_fontsize+2)
	plt.tight_layout()
	savefig_dir = f"../figures/{output_code}_attribute_piechart_{attribute}.png"
	plt.savefig(savefig_dir)
	plt.show()
attribute="race"
df_pie_chart = df[attribute].value_counts().reset_index().rename(columns={'index': attribute, 0: 'count', attribute: "count"})