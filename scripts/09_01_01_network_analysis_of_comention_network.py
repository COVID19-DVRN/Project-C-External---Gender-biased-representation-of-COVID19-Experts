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
output_code = "09_01_01"

# %%
## Adding the metadata of each entity
df_entity_to_annotated_race_gender_expertise = pd.read_csv(f"../outputs/data/08_01_01_entity_race_gender_expertise_news_count.csv", na_filter=False)

df_entity_to_annotated_race_gender_expertise["entity_id"] = df_entity_to_annotated_race_gender_expertise["entity_id"].apply(lambda x: str(x))
metadata_index = 'entity_id'
metadata_list = [
                'entity_name',
                'sex',
                'pronoun',
                'race',
                'urm',
                "gender_urm",
                'public_health_researcher',
                'practitioner',
                'non_public_health_researcher',
                'policymaker',
                'industry_expert',
                'celebrity',
                'journalist',
                "expertise_label_by_relative_expertise",
                'news_count',]
dicts_entity_id_to_metadata = df_entity_to_annotated_race_gender_expertise.set_index(metadata_index).to_dict()

# %%
## Importing the network
input_dir="../outputs/network"
input_basename="comention_network_with_metadata"
input_full_fname=f"{input_dir}/05_01_01_{input_basename}.edgelist"
G = nx.readwrite.edgelist.read_edgelist(input_full_fname)

## Adding metadata
for metadata in metadata_list:
    dict_entity_id_to_metadata = dicts_entity_id_to_metadata[metadata]
    nx.set_node_attributes(G, dict_entity_id_to_metadata, metadata)

## Now lets try to find the assortativity between expertise
## Do we see more interaction between public health expert
## and policymakers? Do we see any other intersting interactions

attributes = ["expertise_label_by_relative_expertise","gender_urm"]

for attribute in attributes:
	#attribute = "expertise_label_by_relative_expertise"

	#%%
	## Plotting the attribute mixing matrix (whole network)
	## https://stackoverflow.com/questions/32980633/adding-text-ticklabels-to-pcolor-heatmap
	fig, ax = plt.subplots(figsize = (12,8))
	fig.subplots_adjust(bottom=0.25,left=0.25) # make room for labels

	mapping = {
		"expertise_label_by_relative_expertise":{
			"public_health_researcher":0,
			"practitioner":1,
			"non_public_health_researcher":2,
			"policymaker":3,
			"industry_expert":4,
			"journalist":5,
			"celebrity":6,
			},
		"gender_urm":
			{
				"non_urm_male":0,
				"urm_male":1,
				"non_urm_female":2,
				"urm_female":3
			}
		}

	## Here follow the order of 0,1,2,3,... etc in the list from the mapping above
	ticklabels = {"expertise_label_by_relative_expertise":	
						["Public\nHealth Researcher",
						"Practitioner",
						"Non Public\nHealth Researcher",
						"Policymaker",
						"Industry\nExpert",
						"Journalist",
						"Celebrity"],
					"gender_urm":
						[
							"non URM, Man",
							"URM, Man",
							"non URM, Woman",
							"URM, Woman"
						]
					}

	NA_by_attribute = {
		"expertise_label_by_relative_expertise":"NA",
		"gender_urm":None
	}

	dict_node_to_attribute = nx.get_node_attributes(G,attribute)
	## TODO: Double check the NA individuals
	nodeset = dict_node_to_attribute.keys()

	if NA_by_attribute[attribute]:
	## If we want to filter the nodeset by removing a single type of value for this attribute
		nodeset = [node for node,value in dict_node_to_attribute.items() if value!=NA_by_attribute[attribute]]

	e_ij = nx.attribute_mixing_matrix(G,attribute,nodes=nodeset,mapping=mapping[attribute])
	#e_ij = nx.attribute_mixing_matrix(G,attribute,mapping=mapping)

	attribute_assortativity_numbers_matrix = np.zeros((len(mapping[attribute]),len(mapping[attribute])), dtype=int, order='C')
	for edge in G.edges(data=True):
		#print(edge)
		if edge[0] in nodeset and edge[1] in nodeset:
			attribute_assortativity_numbers_matrix[mapping[attribute][dict_node_to_attribute[edge[0]]]][mapping[attribute][dict_node_to_attribute[edge[1]]]] += 1

	r = nx.attribute_assortativity_coefficient(G,attribute,nodes=nodeset)
	##visualize matrix
	ax.set_title(r"Attribute assortativity matrix of co-mention network, $r$=%.3f"%(r),fontsize=14)
	heatmap = ax.pcolormesh(e_ij, cmap='plasma')
	#plt.pcolormesh(e_ij, norm=LogNorm(vmax=e_ij.max()),cmap='plasma')
	plt.colorbar(heatmap)
	## The number shown here sums up to the number of edges considered in the assortativity calculation

	## Setting xticks and yticks
	## Set ticks in center of cells
	ax.set_xticks(np.arange(e_ij.shape[1]) + 0.5, minor=False)
	ax.set_yticks(np.arange(e_ij.shape[0]) + 0.5, minor=False)

	# Rotate the xlabels. Set both x and y labels to headers[1:]
	ax.set_xticklabels(ticklabels[attribute],rotation=90)
	ax.set_yticklabels(ticklabels[attribute])

	## Putting the numbers inside the blocks
	## https://stackoverflow.com/questions/20998083/show-the-values-in-the-grid-using-matplotlib
	for (i, j), z in np.ndenumerate(attribute_assortativity_numbers_matrix):
	    ax.text(j+0.5, i+0.5, '{:0.0f}'.format(z), ha='center', va='center',
	    	bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3'))
	savefig_dir = f"../figures/{output_code}_assortativity_attributes_{attribute}_comention_network.png"
	plt.savefig(savefig_dir)
	#plt.show()
