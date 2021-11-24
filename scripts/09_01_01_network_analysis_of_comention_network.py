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
from collections import defaultdict, Counter
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
                "expertise_label_by_relative_reach",
                'news_count',]
dicts_entity_id_to_metadata = df_entity_to_annotated_race_gender_expertise.set_index(metadata_index).to_dict()

# %%
## Importing the network
input_dir="../outputs/network"
input_basename="comention_network_with_metadata"
input_full_fname=f"{input_dir}/05_01_01_{input_basename}.edgelist"
G = nx.readwrite.edgelist.read_edgelist(input_full_fname)

# %%
## Exporting the individuals inside the network
df_individuals_inside_network = pd.DataFrame(zip(list(G.nodes()),[dicts_entity_id_to_metadata["entity_name"][entity_id] for entity_id in G.nodes()]),columns=["entity_id","entity_name"], index=None)
df_individuals_inside_network.to_csv(f"../outputs/data/{output_code}_individuals_in_comention_network.csv", index=False)


## Adding metadata
for metadata in metadata_list:
    dict_entity_id_to_metadata = dicts_entity_id_to_metadata[metadata]
    nx.set_node_attributes(G, dict_entity_id_to_metadata, metadata)

## Degree distribution
## First plot the degree distribution
def get_binned_distribution(values, number_of_bins = 20, log_binning = False, base = 10):
	lower_bound = min(values)
	upper_bound = max(values)
	
	if log_binning:
		lower_bound = np.log10(lower_bound)/ np.log10(base) if lower_bound > 0 else -1
		upper_bound = np.log10(upper_bound)/ np.log10(base)
		bins = np.logspace(lower_bound, upper_bound, number_of_bins, base=base)
	else:
		bins = np.linspace(lower_bound, upper_bound, number_of_bins)
	
	## Calculating histogram
	y, _ = np.histogram(values, bins = bins, density = True)
	
	## Now for each y we need to compute the value of x
	x = bins[1:] - np.diff(bins) / 2.
	
	# sanity check for probability density
	#print(sum(map(lambda a,b : a*b, [bins[i] - bins[i-1] for i in range(1,len(bins))],y)))
	
	return x,y

def plot(x,y, log = True, xsize = 8, ysize = 3, xlabel="", ylabel=""):
	plotted_figure = plt.figure(figsize = (xsize,ysize))
	if log:
		plt.loglog(x,y, '.')
	else:
		plt.plot(x,y, '.')
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.show()
	return plotted_figure

x,y = get_binned_distribution(list(dict(G.degree()).values()), log_binning=True)
_ = plot(x,y, xlabel=r"$k$", ylabel=r"$p_{k}$", log=False)


## creating a function that takes arbitrary list of values and then creates
## a histogram of those values
def plot_histogram_of_values(values, value_label = "", savefig_dir="", title = "", logx = False, logy= False, figsize = (12,5), show_count_in_tick=True):
	## Plotting the 
	fig,ax = plt.subplots(figsize=figsize)
	val, count = zip(*sorted(Counter(values).items()))
	val_with_count = [str(x[0])+"\n(%d)"%x[1] for x in zip(val,count)]
	ax.bar(range(len(val)),count,color='#0504aa', alpha=0.7)
	xticks = range(len(val))
	ax.set_xticks(xticks)
	if show_count_in_tick:
		ax.set_xticklabels(val_with_count)
	else:
		ax.set_xticklabels(val)
	ax.set_ylabel("Count")
	ax.set_xlabel(value_label)
	ax.grid(axis="y", alpha = 0.5)
	if logx:
		ax.set_xscale('log')
	if logy:
		ax.set_yscale('log')
	if title:
		ax.set_title(title)
	plt.tight_layout()
	if savefig_dir:
		plt.savefig(savefig_dir, dpi = 150)
	plt.show()
	#return ax

## Plotting overall degree distribution
value_label = "degree"
savefig_dir = f"../figures/{output_code}_histogram_{value_label}.png"
values = [val for (node, val) in G.degree()]
title = "Degree distribution of the experts co-mention network (undirected and unweigted)"
plot_histogram_of_values(values,value_label=value_label,savefig_dir=savefig_dir,title=title, logy = True)

## Print the top 4 nodes by degree count
dict_names=nx.get_node_attributes(G,"entity_name")
print({dict_names[k]:v for k,v in G.degree() if v > 45})


## Now lets try to find the assortativity between expertise
## Do we see more interaction between public health expert
## and policymakers? Do we see any other intersting interactions

attributes = ["expertise_label_by_relative_expertise",
			"gender_urm",
			"expertise_label_by_relative_reach"]

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
		"expertise_label_by_relative_reach":
			{
				"policymaker":0,
				"public_health_researcher":1,
				"practitioner":2,
				"industry_expert":3,
				"non_public_health_researcher":4,
				"celebrity":5,
				"journalist":6,
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
					"expertise_label_by_relative_reach":
						[
							"Policymaker",
							"Public\nHealth Researcher",
							"Practitioner",
							"Industry\nExpert",
							"Non Public\nHealth Researcher",
							"Celebrity",
							"Journalist",
						],
					"gender_urm":
						[
							"non URM, Man",
							"URM, Man",
							"non URM, Woman",
							"URM, Woman"
						]
					}

	NA_by_attribute = {
		"expertise_label_by_relative_expertise":"not_available",
		"expertise_label_by_relative_reach":"not_available",
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
			## This network is undirected, so we need to count the edge on the other way round too
			attribute_assortativity_numbers_matrix[mapping[attribute][dict_node_to_attribute[edge[1]]]][mapping[attribute][dict_node_to_attribute[edge[0]]]] += 1

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
	plt.savefig(savefig_dir, dpi=150)
	#plt.show()
#attribute = "race"