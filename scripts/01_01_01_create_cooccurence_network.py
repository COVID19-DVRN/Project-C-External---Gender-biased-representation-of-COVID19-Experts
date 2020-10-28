# -*- coding: utf-8 -*-
import json
import pandas as pd
import unicodedata
import networkx as nx
from collections import defaultdict
from itertools import combinations
import mercator
# %%
output_code = "01_01_01"
# %%
with open("../outputs/data/00_01_01_tagged_names_from_expert_mention_articles.json", "r") as f:
    story_id_to_entities = json.load(f)

edgelist = defaultdict(int)

## We actually need to create it as a weighted hypergraph becuase we have
## a collection of interacting actors, not necessarily dyads

story_ids_used_in_network = []
for story_id, list_of_expert_list in story_id_to_entities.items():
    for expert_list in list_of_expert_list:
        if len(expert_list) >= 2:
            for comb in combinations(expert_list,2):
            	edgelist[tuple(sorted(comb))] += 1

G = nx.Graph()
edgelist_with_weight = [(edge[0],edge[1],{"weight":weight}) for edge,weight in edgelist.items()]
G.add_edges_from(edgelist_with_weight)

S = max(nx.connected_components(G), key=len)

Gc = G.subgraph(S).copy()

#%%
## Now we will save the undirected largest connected component as a numbered edgelist to do the mercator embedding.

## We will first create the numbered nodes to send to mercator.
Gc_integer_labeled = nx.convert_node_labels_to_integers(Gc, first_label=0, label_attribute="name")

output_dir="../outputs/mercator/input"
output_basename="comention_giant_connected_component"
output_full_fname="%s/%s_%s.edge" %(output_dir, output_code, output_basename)
nx.readwrite.edgelist.write_edgelist(Gc_integer_labeled, output_full_fname, data=False)

#%%
## Now we are taking the output edgelist as an input for the mercator embedding and create the embedding
## with metadata as a json file
custom_seed = 42
input_dir=output_dir
input_basename = output_basename
input_edgelist_full_path = "%s/%s_%s.edge" %(input_dir,output_code,input_basename)
mercator.embed(input_edgelist_full_path,"../outputs/mercator/output/%s_%s" %(output_code,input_basename), seed=custom_seed)
edge= pd.read_csv(input_edgelist_full_path,comment='#',header=None,sep='\s+',index_col= None)[[0,1]]
edge.columns = 'source target'.split()
all_edges = []
for source,target in edge.values:
	all_edges.append({"source":str(source),"target":str(target)})

coord_fname = "../outputs/mercator/output/%s_%s.inf_coord" %(output_code,input_basename)
df = pd.read_csv(coord_fname,comment='#',header=None,sep='\s+',index_col=0)
df.columns = 'k theta r'.split()
save = {}
save['nodes'] = df.T.to_dict()
save['edges'] = all_edges
#print(all_edges[0])
savedir = "../outputs/mercator/output/%s_%s" %(output_code,input_basename)
json.dump(save,open(savedir+'.json','w'))

#%%
## adding metadata to the coordinate json file we just created
input_basename = output_basename
input_fname =  "../outputs/mercator/output/%s_%s.json" %(output_code,input_basename)
with open(input_fname, "r") as f:
    whole_dict = json.load(f)
metadata=dict()
metadata["name"]=nx.get_node_attributes(Gc_integer_labeled,"name")
for metadata_type in ["name"]:
    for node in whole_dict["nodes"]:
        whole_dict["nodes"][node][metadata_type] = metadata[metadata_type][int(node)]
# %%
savedir = "../outputs/mercator/output/%s_%s" %(output_code,input_basename)
json.dump(whole_dict,open(savedir+'.json','w'))