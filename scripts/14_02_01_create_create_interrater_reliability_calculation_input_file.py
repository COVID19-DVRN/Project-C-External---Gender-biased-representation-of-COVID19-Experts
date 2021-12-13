# -*- coding: utf-8 -*-
"""
Summary: 
    In this script I will perform
Input:
    ./outputs/...
Output:
    Some outputs
"""

import pandas as pd
import json
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
pd.options.display.width = 0

# %%
output_code = "14_02_01"

dict_attribute_label_to_number = {
    "pronoun_denoting_gender":{
        "He":0,
        "She":1,
        "They":2,
        "Other":3,
        "No info":4,
        "":5
    },
    "race_ethnicity":{
        "White/European":0,
        "East Asian":1,
        "South Asian":2,
        "Latinx":3,
        "Black/African":4,
        "Middle Eastern":5,
        "Aboriginal/Native American":6,
        "Other/Mixed":7,
        "Unknown":8,
        "":9
    },
    "public_health_researcher":{
        "Yes":1,
        "No":0,
        "":2
    },
    "practitioner/clinician/physician":{
        "Yes":1,
        "No":0,
        "":2
    },
    "non_public_health_researcher":{
        "Yes":1,
        "No":0,
        "":2
    },
    "politician/govt service/policymaker":{
        "Yes":1,
        "No":0,
        "":2
    },
    "industry_expert":{
        "Yes":1,
        "No":0,
        "":2
    },
    "celebrity":{
        "Yes":1,
        "No":0,
        "":2
    },
    "journalist":{
        "Yes":1,
        "No":0,
        "":2
    }
}

# %%
## Read the intercoder reliability file
df_intercoder = pd.read_csv("../inputs/14_01_01_intercoder_reliability_100_samples_double_checked.csv", dtype=str,na_filter=False)
df_intercoder = df_intercoder[[
                    "disambiguated_entity_id",
                    "pronoun_denoting_gender",
                    "race_ethnicity",
                    "public_health_researcher",
                    "practitioner/clinician/physician",
                    "non_public_health_researcher",
                    "politician/govt service/policymaker",
                    "industry_expert",
                    "celebrity",
                    "journalist"]]

# %%
## Then read the 04_02_01 where we can find the rows corresponding to the person
## and then keep only the rows
df_hackathon_worksheet = pd.read_csv("../outputs/data/04_02_01_entity_race_gender_expertise.csv", dtype=str,na_filter=False)
df_hackathon_worksheet = df_hackathon_worksheet[[
                    "disambiguated_entity_id",
                    "pronoun_denoting_gender",
                    "race_ethnicity",
                    "public_health_researcher",
                    "practitioner/clinician/physician",
                    "non_public_health_researcher",
                    "politician/govt service/policymaker",
                    "industry_expert",
                    "celebrity",
                    "journalist"]]

for attribute in dict_attribute_label_to_number:
    df_intercoder[attribute] = df_intercoder[attribute].apply(lambda x: dict_attribute_label_to_number[attribute][x])
    df_hackathon_worksheet[attribute] = df_hackathon_worksheet[attribute].apply(lambda x: dict_attribute_label_to_number[attribute][x])

df_joined = df_intercoder.set_index("disambiguated_entity_id").join(df_hackathon_worksheet.set_index("disambiguated_entity_id"),how="inner",lsuffix="_intercoder",rsuffix="_original")

attributes = ["pronoun_denoting_gender",
                    "race_ethnicity",
                    "public_health_researcher",
                    "practitioner/clinician/physician",
                    "non_public_health_researcher",
                    "politician/govt service/policymaker",
                    "industry_expert",
                    "celebrity",
                    "journalist"]

dataframe_final_columns = []
for attribute in attributes:
    dataframe_final_columns.append(attribute+"_original")
    dataframe_final_columns.append(attribute+"_intercoder")

df_joined = df_joined[dataframe_final_columns].copy()


df_joined.to_csv(f"../outputs/data/{output_code}_intercoder_reliability_calculation.csv",index=False,header=False)