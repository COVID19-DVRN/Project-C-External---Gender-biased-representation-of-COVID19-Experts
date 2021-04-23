# -*- coding: utf-8 -*-
"""
Summary: 
	This script inputs the crowdsourced disambiguated names
	For each name that is one single entity and represented by a "possible_candidate"
	to be SELF, we will create a hash, a unique id corresponding to the name.
	For each of multiple form of an entity each of them will correspond to a unique
	entity id and the unique SELF raw_name

Input:
	race_gender_expertise_hack_on_your_own_time - Task Sheet 1.csv

Output:
	Two files
	The disambiguation file maps all the available names to a unique
	entity id.
	The race gender ethnicity file maps all the unique entity (the
	entity those are SELF) and their race gender etc.
"""

import pandas as pd
pd.options.display.width = 0
import xxhash

# %%
output_code = "04_02_01"
seed = 42
# %%
df_orig = pd.read_csv("../inputs/race_gender_expertise_hack_on_your_own_time - Task Sheet 1.csv", dtype=str, na_filter=False)

# %%
header_disambiguation = [
	'orig_index',
	'raw_name',
	"disambiguated_entity",
	"disambiguated_entity_id",
]
df_disambiguation_file = pd.DataFrame(columns =(header_disambiguation))


header_race_gender_ethnicity = [
	'orig_index',
	"disambiguated_entity",
	"disambiguated_entity_id",
]
keys_coming_from_orig_df = ['sex_at_birth',
	'comment/reference',
	'pronoun_denoting_gender', 'comment/reference.1', 'race_ethnicity', 'comment/reference.2', 'public_health_researcher',
	'practitioner/clinician/physician', 'non_public_health_researcher', 'politician/govt service/policymaker', 'industry_expert',
	'celebrity', 'journalist', 'comment/reference.3']
df_race_gender_expertise_file = pd.DataFrame(columns =(header_race_gender_ethnicity+keys_coming_from_orig_df))

for _, row in df_orig[df_orig["possible_candidate"]!="na"].iterrows():
	disambiguation_doc = {}
	race_gender_expertise_doc = {}

	if row["possible_candidate"] == "SELF":
		disambiguation_doc["orig_index"] = row["orig_index"]
		disambiguation_doc["raw_name"] = row["raw_name"]
		disambiguation_doc["disambiguated_entity"] = row["raw_name"]
		disambiguation_id = xxhash.xxh32(row["raw_name"],seed=seed).intdigest()
		disambiguation_doc["disambiguated_entity_id"] = disambiguation_id

		race_gender_expertise_doc = row[keys_coming_from_orig_df]
		for key in header_race_gender_ethnicity:
			race_gender_expertise_doc[key] = disambiguation_doc[key]

		df_race_gender_expertise_file = df_race_gender_expertise_file.append(race_gender_expertise_doc, ignore_index=True)

	else:
		#print(row["orig_index"])
		disambiguation_doc["orig_index"] = row["orig_index"]
		disambiguation_doc["raw_name"] = row["raw_name"]
		target_entity = row["possible_candidate"]
		disambiguation_doc["disambiguated_entity"] = target_entity
		disambiguation_id = xxhash.xxh32(target_entity,seed=seed).intdigest()
		disambiguation_doc["disambiguated_entity_id"] = disambiguation_id
		#print(disambiguation_doc)

	df_disambiguation_file = df_disambiguation_file.append(disambiguation_doc, ignore_index=True)

df_na = df_orig[df_orig["possible_candidate"].str.lower()=="na"]
df_na.to_csv(f"../outputs/data/{output_code}_names_not_available.csv",index=False)
df_disambiguation_file.to_csv(f"../outputs/data/{output_code}_names_disambiguated.csv",index=False)
df_race_gender_expertise_file.to_csv(f"../outputs/data/{output_code}_entity_race_gender_expertise.csv",index=False)
