# -*- coding: utf-8 -*-
import json
import pandas as pd
import unicodedata
import networkx as nx
from collections import defaultdict,Counter
from itertools import combinations
import mercator
# %%
## imported from custom helper library accompanying this project
from helpers.text_processing import preprocess_names
# %%
output_code = "05_01_01"
# %%
with open("../outputs/data/00_01_01_tagged_names_from_expert_mention_articles.json", "r") as f:
    story_id_to_entities = json.load(f)

# %%
df_entity_disambiguated = pd.read_csv("../outputs/data/04_02_01_names_disambiguated.csv")
dict_expert_name_to_entity_id = df_entity_disambiguated.set_index("raw_name").to_dict()["disambiguated_entity_id"]

## Find the NA list
df_entity_not_available = pd.read_csv("../outputs/data/04_02_01_names_not_available.csv")
entities_not_available = df_entity_not_available["raw_name"].values

## Adding the metadata of each entity
df_entity_to_annotated_race_gender_expertise = pd.read_csv(f"../outputs/data/04_02_01_entity_race_gender_expertise.csv")

metadata_index = 'disambiguated_entity_id'
metadata_list = [
    'disambiguated_entity',
    'sex_at_birth',
    'pronoun_denoting_gender',
    'race_ethnicity',
    'public_health_researcher',
    'practitioner/clinician/physician',
    'non_public_health_researcher',
    'politician/govt service/policymaker',
    'industry_expert',
    'celebrity',
    'journalist',]

dicts_entity_id_to_metadata = df_entity_to_annotated_race_gender_expertise.set_index(metadata_index).to_dict()

hand_updated_entity_name_to_corresponding_disambiguated_name = {
 '':None,
 'aldrich':"matthew aldrich",
 'amesh adalja':"amesh a adalja",
 'andrés manuel lópez obrador':"andres manuel lopez obrador",
 'anthony fauci fauci':"anthony fauci",
 'anthony fauci white house':"anthony fauci",
 'anthony fauci —':"anthony fauci",
 'anthony s fauci':"anthony fauci",
 'bedford':"trevor bedford",
 'ben cowling':"benjamin cowling",
 'bezos':"jeff bezos",
 'bolsonaro':"jair bolsonaro",
 'bosch':None,
 'bowser':"muriel bowser",
 'brix':"deborah l birx",
 'burr':None,
 'burton amged el hawrani':"amged el hawrani",
 'bush':None,
 'caitlin orysko':"caitlin orpysko",
 'calderwood':"catherine calderwood",
 'camilla':"camilla pashley",
 'carey':"mariah carey",
 'carre':None,
 'cecília müller':"cecilia muller",
 'celularity':None,
 'chowdhury':"abdul mabud chowdhury",
 'colm o moráin':"colm o morain",
 'courtney subramanian trump':None,
 'cousin hisham el khider':"hisham el khider",
 'daniel lópez regalado':"daniel lopez regalado", 
 'david geffen school of medicine':None,
 'david heymann':"david l heymann",
 'deborah birx':"deborah l birx",
 'deere':"judd deere",
 'desantis':"ron desantis",
 'dewine':"mike dewine",
 'emílio ribas':None,
 'ernest n morial convention center':None,
 'falwell':"jerry falwell jr",
 'fairbanks':"abbey hardy fairbanks",
 'fauci':"anthony fauci",
 'faucis':"anthony fauci",
 'forbes':None,
 'frost':"wilfred frost",
 'fusco':"grace fusco",
 'gaetz':"matt gaetz",
 'gostin':"lawrence o gostin",
 'hanks':"tom hanks",
 'hariri':"robert hariri",
 'harley':"harley rouda",
 'healthlandscape':None,
 'helen aguirre ferré':"helen aguirre ferre",
 'hostin':"sunny hostin",
 'ingraham':"laura ingraham",
 'jeanine':"jeanine pirro",
 'jennifer m chacón':"jennifer m chacon",
 'joaquin morante cbs news':"joaquin morante",
 'joe ':None,
 'josephine':"josephine wolff",
 'joshua sharfstein':"joshua m sharfstein",
 'josé álvaro moisés':"jose alvaro moises",
 'jérôme salomon':"jerome salomon",
 'kellyanne conway bashes biden':None,
 'keurig':None,
 'kong':None,
 'laura martínez':"laura martinez",
 'lawrence gostin':"lawrence o gostin",
 'li wenliang don':"li wenliang",
 'lockhart':"joe ",
 'lucy jones center for science and seismology':None,
 'lópez obrador':"andres manuel lopez obrador",
 'lópez regalado':"daniel lopez regalado",
 'magnus gisslén':"magnus gisslen",
 'marketwatch':None,
 'martin luther king':None,
 'mcmaster':"henry mcmaster",
 'megan ranney':"megan l ranney",
 'moderna':None,
 'neil ferguson':"neil m ferguson",
 'nero':None,
 'nicolás maduro':"nicolas maduro",
 'northam':"ralph northam",
 'peacehealth':None,
 'pelosi':"nancy pelosi",
 'pepper':"pepper schwartz",
 'peter hotez':"peter jay hotez",
 'phil ':None,
 'pompeo':"mike pompeo",
 'prezcobix':None,
 'queensland heath':None,
 'redfield':"robert r redfield",
 'remdesivir':None,
 'robert redfield':"robert r redfield",
 'rogelio sáenz':"rogelio saenz",
 'ronald reagan ucla medical center':None,
 'roselle chen new york':"roselle chen",
 'schumer':"chuck schumer",
 'scott pelley fact checks mike bloomberg':"scott pelley",
 'sean asiqłuq topkok':"sean asiquq topkok",
 'sen lindsey graham':"lindsey o graham",
 'sherman':"jeff sherman",
 'sklar':"phil ",
 'soon shiong':"patrick soon shiong",
 'steven a cohen military':None,
 'steven mnuchin':"steven t mnuchin",
 'teamhealth':None,
 'tesla':None,
 'thaïs aliabadi':"thais aliabadi",
 'thomas 6 25':None,
 'tompkins stange':"megan tompkins-stange",
 'tony cárdenas':"tony cardenas",
 'tony fauci':"anthony fauci",
 'torres':"john torres",
 'tsai ing wen':"tsai ing-wen",
 'vrbo':None,
 'weibo':None,
 'winton':"andrew winton",
 'wong ka hing':"wong ka-hing",
 'yae jean kim':"yae-jean kim",
 'zacharin':"margaret zacharin",
 'zaheer shah cbs news':"zaheer shah",
 'zarif':"mohammad javad zarif",
 'zika':None,
 'zoltán kiss':"zoltan kiss",
 'zuckerberg':"mark zuckerberg",
 '—':None,
 '—vicky mckeever':"vicky mckeever"}

edgelist = defaultdict(int)

## We actually need to create it as a weighted hypergraph becuase we have
## a collection of interacting actors, they are not necessarily always dyads

disambiguation_not_found_set = set()

story_ids_used_in_network = []
for story_id, list_of_expert_list in story_id_to_entities.items():
    for expert_list in list_of_expert_list:
        if len(expert_list) >= 2:
            for comb in combinations(expert_list,2):
                expert_first = preprocess_names(comb[0])
                expert_second = preprocess_names(comb[1])

                ## We will check for the names that were hand updated later, see the dictionary above
                if expert_first in hand_updated_entity_name_to_corresponding_disambiguated_name:
                    if hand_updated_entity_name_to_corresponding_disambiguated_name[expert_first] != None:
                        expert_first = hand_updated_entity_name_to_corresponding_disambiguated_name[expert_first]
                if expert_second in hand_updated_entity_name_to_corresponding_disambiguated_name:
                    if hand_updated_entity_name_to_corresponding_disambiguated_name[expert_second] != None:
                        expert_second = hand_updated_entity_name_to_corresponding_disambiguated_name[expert_second]
                
                if expert_first not in dict_expert_name_to_entity_id:
                    #print(f"We did not find {expert_first} in the disambiguation list")
                    if expert_first not in entities_not_available:
                        if expert_first not in hand_updated_entity_name_to_corresponding_disambiguated_name:
                            disambiguation_not_found_set.add(expert_first)
                    continue
                if expert_second not in dict_expert_name_to_entity_id:
                    #print(f"We did not find {expert_second} in the disambiguation list")
                    if expert_second not in entities_not_available:
                        if expert_second not in hand_updated_entity_name_to_corresponding_disambiguated_name:
                            disambiguation_not_found_set.add(expert_second)
                    continue
                edgelist[tuple(sorted([dict_expert_name_to_entity_id[expert_first],dict_expert_name_to_entity_id[expert_second]]))] += 1

print("Here are the name those need to be taken care of", disambiguation_not_found_set)

G = nx.Graph()
edgelist_with_weight = [(edge[0],edge[1],{"weight":weight}) for edge,weight in edgelist.items()]
G.add_edges_from(edgelist_with_weight)

for metadata in metadata_list:
    dict_entity_id_to_metadata = dicts_entity_id_to_metadata[metadata]
    nx.set_node_attributes(G, dict_entity_id_to_metadata, metadata)


S = max(nx.connected_components(G), key=len)

Gc = G.subgraph(S).copy()


#%%
## Now we will save the undirected largest connected component as a numbered edgelist to do the mercator embedding.

## We will first create the numbered nodes to send to mercator.
#Gc_integer_labeled = nx.convert_node_labels_to_integers(Gc, first_label=0, label_attribute="name")

output_dir="../outputs/mercator/input"
output_basename="comention_giant_connected_component"
output_full_fname=f"{output_dir}/{output_code}_{output_basename}.edge"
nx.readwrite.edgelist.write_edgelist(Gc, output_full_fname, data=False)

#%%
## Now we are taking the output edgelist as an input for the mercator embedding and create the embedding
## with metadata as a json file
custom_seed = 42
input_dir=output_dir
input_basename = output_basename
input_edgelist_full_path = f"{input_dir}/{output_code}_{input_basename}.edge"
mercator.embed(input_edgelist_full_path,f"../outputs/mercator/output/{output_code}_{input_basename}", seed=custom_seed)
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
savedir = f"../outputs/mercator/output/{output_code}_{input_basename}"
json.dump(save,open(savedir+'.json','w'))

#%%
## adding metadata to the coordinate json file we just created
input_basename = output_basename
input_fname =  f"../outputs/mercator/output/{output_code}_{input_basename}.json"
with open(input_fname, "r") as f:
    whole_dict = json.load(f)

for metadata_type in metadata_list:
    metadata_dict = nx.get_node_attributes(Gc,metadata_type)
    for node in whole_dict["nodes"]:
        whole_dict["nodes"][node][metadata_type] = metadata_dict[int(node)]
# %%
savedir = f"../outputs/mercator/output/{output_code}_{input_basename}"
json.dump(whole_dict,open(savedir+'.json','w'))