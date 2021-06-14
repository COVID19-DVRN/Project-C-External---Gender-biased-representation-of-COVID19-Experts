# -*- coding: utf-8 -*-
"""
Summary: 
	In this script I will create the number of times an entity appeared in our dataset.
Input:
	./outputs/data/04_02_01_entity_race_gender_expertise.csv
Output:
	A file that keeps the count of the times an entity appeared in our dataset
"""

import pandas as pd
import json
from collections import defaultdict
from unidecode import unidecode
import unicodedata
pd.options.display.width = 0

# %%
output_code = "07_01_01"
seed = 42

# %%
df_entity_annotated = pd.read_csv("../outputs/data/04_02_01_entity_race_gender_expertise.csv", dtype=str, na_filter=False)
df_entity_annotated.groupby(['sex_at_birth','race_ethnicity']).size().reset_index(name='counts')
df_entity_annotated.groupby(['pronoun_denoting_gender']).size().reset_index(name='counts')

# %%
with open("../outputs/data/00_01_01_tagged_names_from_expert_mention_articles.json", "r") as f:
    story_id_to_entities = json.load(f)

# %%
## Lets read the entity and their different synonyms
df_ambiguous_names_to_disambiguated_entity = pd.read_csv("../outputs/data/04_02_01_names_disambiguated.csv")
dict_ambiguous_names_to_disambiguated_entity_name = df_ambiguous_names_to_disambiguated_entity.set_index("raw_name").to_dict()["disambiguated_entity"]
dict_ambiguous_names_to_disambiguated_entity_id = df_ambiguous_names_to_disambiguated_entity.set_index("raw_name").to_dict()["disambiguated_entity_id"]

## Now we are creating a list of disambiguated entities for each of the last part of the name
disambiguated_entities = df_ambiguous_names_to_disambiguated_entity["disambiguated_entity"].values
last_names_to_disambiguated_entities = defaultdict(set)
for entity in disambiguated_entities:
	#print(entity.split()[-1])
	last_names_to_disambiguated_entities[entity.split()[-1]].add(entity)

# %%
df_ambigous_name_with_no_entity = pd.read_csv("../outputs/data/04_02_01_names_not_available.csv")
dict_ambiguous_names_with_no_candidate = df_ambigous_name_with_no_entity.set_index("raw_name").to_dict()["possible_candidate"]

# %%
## Keeping a report of what is happening here
report_lines = []

# %% 
## Preprocessing names
space_separation_list = ["-", "―", "/"]
non_space_sepration_list = ["'",".","’",'“']
dubious_space_list = ["  ", "   ","  "]
removable_keywords = ["dr ", "dr."]
def preprocess_names(s):
    s = s.lower()
    for keyword in removable_keywords:
        s = s.replace(keyword,"")
    s = "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")
    ## First replacning all . and ' with non space
    translate_table = dict((ord(char), "") for char in non_space_sepration_list)
    s = s.translate(translate_table)
    ## Then replacing - wth space
    translate_table = dict((ord(char), "") for char in space_separation_list)
    s = s.translate(translate_table)
    ## Replacing double spaces with single space
    for dubious_space in dubious_space_list:
        s = s.replace(dubious_space," ")
    return s.strip()

# %%
## For each of the story I will create a set where I will put all the 
## entities found in that story in a single set. Then I will count, in
## how many stories did the person appear
story_id_to_unique_entities = defaultdict(set)
previously_not_found_entity_to_possible_entities = dict()
entities_not_found = set()
for story_id, entities in story_id_to_entities.items():
	for entity_list in entities:
		for entity in entity_list:
			preprocessed_entity = unidecode(preprocess_names(entity))
			if preprocessed_entity not in dict_ambiguous_names_to_disambiguated_entity_name:
				if preprocessed_entity not in dict_ambiguous_names_with_no_candidate:
					## Now checking if the last name of current entity can be found in the
					## list of last names we have
					if preprocessed_entity:
					## Making sure if the preprocessed entity is non-empty	
						last_name_current_entity = preprocessed_entity.split()[-1]
						if last_name_current_entity in last_names_to_disambiguated_entities:
							previously_not_found_entity_to_possible_entities[preprocessed_entity] \
								= last_names_to_disambiguated_entities[last_name_current_entity]
						else:
							entities_not_found.add(preprocessed_entity)
			else:
				story_id_to_unique_entities[story_id].add(preprocessed_entity)
report_lines.append("Creating a new list of disambiguated names those were left behind")
for previously_not_found_entity, set_of_possible_candidates in previously_not_found_entity_to_possible_entities.items():
	if len(set_of_possible_candidates) == 1:
		disambiguated_candidate = set_of_possible_candidates.pop()
		disambiguated_candidate_name = dict_ambiguous_names_to_disambiguated_entity_name[disambiguated_candidate]
		disambiguated_candidate_id = dict_ambiguous_names_to_disambiguated_entity_id[disambiguated_candidate]
		report_lines.append(",".join(map(str,["",previously_not_found_entity,disambiguated_candidate_name,disambiguated_candidate_id])))


## First I will explore the names that are 
with open(f"../outputs/reports/{output_code}_report.txt", "w") as f:
	f.writelines("\n".join(report_lines))
