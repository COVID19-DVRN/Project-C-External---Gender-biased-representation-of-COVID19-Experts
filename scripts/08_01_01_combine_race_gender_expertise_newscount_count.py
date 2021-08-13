# -*- coding: utf-8 -*-
"""
Summary: 
	In this script I will combine multiple variables related to each entity
Input:
	./outputs/data/07_01_01
Output:
	A file that keeps a combined variables of 
"""

import pandas as pd
import json
from collections import defaultdict
from unidecode import unidecode
import unicodedata
pd.options.display.width = 0

# %%
output_code = "08_01_01"
seed = 42

# %%
df_entity_race_gender_expertise = pd.read_csv("../outputs/data/04_02_01_entity_race_gender_expertise.csv", dtype=str, na_filter=False)
df_entity_race_gender_expertise.set_index("disambiguated_entity_id")
df_entity_news_count = pd.read_csv("../outputs/data/07_01_01_entity_news_count.csv", dtype=str, na_filter=False)
df_entity_news_count.set_index("disambiguated_entity_id")

df_merged = df_entity_race_gender_expertise.merge(df_entity_news_count, how = "inner")
## The number of rows in the new file should be the length of 
## dataframe of news count. As it has less number of entity than the entity race gender
## dataframe, and also all of the entity in news count should be present in the entity
## race gender dataframe.
assert(len(df_entity_news_count)==len(df_merged))

df_merged = df_merged[["disambiguated_entity_id",
			"disambiguated_entity",
			"sex_at_birth",
			"pronoun_denoting_gender",
			"race_ethnicity",
			"public_health_researcher",
			"practitioner/clinician/physician",
			"non_public_health_researcher",
			"politician/govt service/policymaker",
			"industry_expert",
			"celebrity",
			"journalist",
			"number_of_unique_news_appeared_in"]]

df_merged = df_merged.rename(columns={"disambiguated_entity_id":"entity_id",
			"disambiguated_entity":"entity_name",
			"sex_at_birth":"sex",
			"pronoun_denoting_gender":"pronoun",
			"race_ethnicity":"race",
			#"public_health_researcher":"public_health_researcher",
			"practitioner/clinician/physician":"practitioner",
			#"non_public_health_researcher":"non_public_health_researcher",
			"politician/govt service/policymaker":"policymaker",
			#"industry_expert":"industry_expert",
			#"celebrity":"celebrity",
			#"journalist":"journalist",
			"number_of_unique_news_appeared_in":"news_count"})

report_lines = []
report_lines.append(f"We initially had {len(df_merged)} rows.")

## Now lets remove all the rows where the sex at birth is unknown or
## the race is unknown and the pronoun is No info
df_merged = df_merged[~((df_merged["sex"]=="Unidentified")|(df_merged["race"]=="Unknown")|(df_merged["pronoun"]=="No info"))]
report_lines.append(f"But after removing all the rows where sex is unidentified or the race is unknown or the pronoun is No info, we are left with {len(df_merged)} rows.")

## Now let me create a new variable called URM (Yes/No)
## Underrepresentated minority vs non-minority
## white + East Asian are not URM
## Rest are URM
URM_races = ["Black/African", "Latinx", "South Asian", "Middle Eastern", "Aboriginal/Native American", "Other/Mixed"]
non_URM_races = ["White/European", "East Asian"]
df_merged["urm"] = df_merged["race"].apply(lambda x: "Yes" if x in URM_races else "No")

## Now creating an intersection between gender and urm
def gender_urm_intersection(sex,urm):
	if urm == "Yes":
		if sex == "Female":
			return "urm_female"
		elif sex == "Male":
			return "urm_male"
	elif urm == "No":
		if sex == "Female":
			return "non_urm_female"
		elif sex == "Male":
			return "non_urm_male"
	else:
		return "unknown"
df_merged["gender_urm"] = df_merged.apply(lambda row: gender_urm_intersection(row.sex,row.urm), axis=1)

## Now creating an intersection between gender and urm
def pronoun_urm_intersection(pronoun,urm):
	if urm == "Yes":
		if pronoun == "She":
			return "urm_she"
		elif pronoun == "He":
			return "urm_he"
		elif pronoun == "They":
			return "urm_they"
	elif urm == "No":
		if pronoun == "She":
			return "non_urm_she"
		elif pronoun == "He":
			return "non_urm_he"
		elif pronoun == "They":
			return "non_urm_they"
	else:
		return "unknown"
df_merged["pronoun_urm"] = df_merged.apply(lambda row: pronoun_urm_intersection(row.pronoun,row.urm), axis=1)

## Now create a single expertise for each of the entity
## First the one for relative expertise in terms of public health:
def singlemost_important_expert_label_from_relative_expertise(row):
	if row["public_health_researcher"] == "Yes":
		return "public_health_researcher"
	elif row["practitioner"] == "Yes":
		return "practitioner"
	elif row["non_public_health_researcher"] == "Yes":
		return "non_public_health_researcher"
	elif row["policymaker"] == "Yes":
		return "policymaker"
	elif row["industry_expert"] == "Yes":
		return "industry_expert"
	elif row["journalist"] == "Yes":
		return "journalist"
	elif row["celebrity"] == "Yes":
		return "celebrity"
	else: return "not_available"

df_merged["expertise_label_by_relative_expertise"] = df_merged.apply(lambda row: singlemost_important_expert_label_from_relative_expertise(row), axis=1)

## Then the one for relative reach of expertise in terms of public health messages:
def singlemost_important_expert_label_from_relative_reach(row):
	if row["policymaker"] == "Yes":
		return "policymaker"
	elif row["public_health_researcher"] == "Yes":
		return "public_health_researcher"
	elif row["practitioner"] == "Yes":
		return "practitioner"
	elif row["industry_expert"] == "Yes":
		return "industry_expert"
	elif row["non_public_health_researcher"] == "Yes":
		return "non_public_health_researcher"
	elif row["celebrity"] == "Yes":
		return "celebrity"
	elif row["journalist"] == "Yes":
		return "journalist"
	else: return "not_available"

df_merged["expertise_label_by_relative_reach"] = df_merged.apply(lambda row: singlemost_important_expert_label_from_relative_reach(row), axis=1)


df_merged = df_merged[['entity_id',
						'entity_name',
						'sex',
						'pronoun',
						'race',
						'urm',
						"gender_urm",
						"pronoun_urm",
						'public_health_researcher',
						'practitioner',
						'non_public_health_researcher',
						'policymaker',
						'industry_expert',
						'celebrity',
						'journalist',
						"expertise_label_by_relative_expertise",
						"expertise_label_by_relative_reach",
						'news_count',]]

df_merged.to_csv(f"../outputs/data/{output_code}_entity_race_gender_expertise_news_count.csv", index=False)

with open(f"../outputs/reports/{output_code}_report.txt","w") as f:
	f.writelines("\n".join(report_lines))

# data = read.csv("/Users/haque.s/development/Project-C-External---Gender-biased-representation-of-COVID19-Experts/outputs/data/08_01_01_entity_race_gender_expertise_news_count.csv")
# library(MASS)
# model2 <- lm(news_count ~ sex + race + public_health_researcher + practitioner + policymaker + industry_expert + celebrity + journalist, data = data)
# model2 <- lm(news_count ~ pronoun + race + public_health_researcher + practitioner + policymaker + industry_expert + celebrity + journalist, data = data)
# model_nb <- glm.nb(news_count ~ sex + race + public_health_researcher + practitioner + policymaker + industry_expert + celebrity + journalist, data = data)
# data <- data[!(data$entity_name == "anthony fauci"),]
# as.factor kore categorical, I already tried that do not have any difference
# incidence rate ratio
# ekta reference froup er tulonay arekta group e nao, se ekta news e participate
## Log of expected count, jodi positive male theke female ke subtract kortesi

## Self loop, other nodes
## Create a hierarchy and highest in the hierarchy
## in terms the number of people they would be impacting
## Policymaker -- impacts most number of people
## Publich health researcher
## Practitionaer
## Industry expert
## Non Public health researcher
## Celebrity
## Journalist

## Also then the relative expertise
## Publich health researchers
## Pratitioner
## non publich health 
## policymaker
## industry expert
## Journalist
## Celebrity

## Even though we wanted to see mutiple

## Change opacity of the urm_gender plot

## Health science researcher
## Coefficent plot

## Caveat that we are missing religious leaders

## tomasz wojtasik queer

## All lawyer put into industry expert

## For viz the commit "Add gender_urm intersection variable" is working

## Call URM Underrepresentated races