# -*- coding: utf-8 -*-
import json
import pandas as pd
import unicodedata
import networkx as nx
from collections import defaultdict
from itertools import combinations
import mercator
# %%
output_code = "02_01_01"
# %%
with open("../outputs/data/00_01_01_tagged_names_from_expert_mention_articles.json", "r") as f:
    story_id_to_entities = json.load(f)

# %%
df_orig = pd.read_csv("../inputs/untracked/Coronavirus_20200101_20200409_clean_expert.csv")
df = df_orig[["stories_id","url","Text","Expert_Mention_List","Expert_Mention_Sentence_List"]]
#df = df.set_index("stories_id")


## We are creating a list of stories where we are creating the
## cliques
df_new = pd.DataFrame()
for story_id, list_of_expert_list in story_id_to_entities.items():
    for expert_list in list_of_expert_list:
        if len(expert_list) >= 2:
            print(story_id)
            df_new = df_new.append({"stories_id":int(story_id),"experts_extracted_list":expert_list}, ignore_index=True)
            for comb in combinations(expert_list,2):
                pass

#pd.merge(df,df_new,how="inner").to_csv("mishuk.csv", index=False)