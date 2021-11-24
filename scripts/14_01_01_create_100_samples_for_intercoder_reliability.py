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
np.random.seed(42)


# %%
output_code = "14_01_01"

# %%
## First read the 08_01_01 data file that contains the final selction of the individuals
df_final_individuals = pd.read_csv("../outputs/data/08_01_01_entity_race_gender_expertise_news_count.csv")

# %%
## Create the random rows using numpy low and high
np.random.seed(42)
names=np.random.choice(df_final_individuals.entity_name,size=100,replace=False)

# %%
## Then read the 04_02_01 where we can find the rows corresponding to the person
## and then keep only the rows
df_hackathon_worksheet = pd.read_csv("../outputs/data/04_02_01_entity_race_gender_expertise.csv")

df = df_hackathon_worksheet[df_hackathon_worksheet["disambiguated_entity"].isin(names)].copy()

# %%
## Now reading the original coders name
df_original_coders = pd.read_csv("../inputs/hackathon_coder_list.csv")
dict_orig_index_to_coder_name = dict()
for _,row in df_original_coders.iterrows():
    for i in range(row["start"],row["end"]+1):
        dict_orig_index_to_coder_name[i] = row["coder"]

df["who_shouldnt_code"] = df["orig_index"].apply(lambda x: dict_orig_index_to_coder_name[x])

df = df[['orig_index', "who_shouldnt_code",'disambiguated_entity', 'disambiguated_entity_id', 'sex_at_birth', 'comment/reference',
       'pronoun_denoting_gender', 'comment/reference.1', 'race_ethnicity', 'comment/reference.2',
       'public_health_researcher', 'practitioner/clinician/physician', 'non_public_health_researcher',
       'politician/govt service/policymaker', 'industry_expert', 'celebrity', 'journalist',
       'comment/reference.3']]

df.to_csv(f"../outputs/data/{output_code}_intercoder_reliability_100_samples.csv",index=False)