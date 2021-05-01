# -*- coding: utf-8 -*-
"""
Summary: 
	In this script we will explore some ways to visualize the intersectionality
	of the experts we have annotated.

Input:
	./outputs/data/04_02_01_entity_race_gender_expertise.csv

Output:
	Some visualizations
"""

import pandas as pd
pd.options.display.width = 0

# %%
output_code = "06_01_01"
seed = 42

# %%
df_entity_annotated = pd.read_csv("../outputs/data/04_02_01_entity_race_gender_expertise.csv", dtype=str, na_filter=False)
df_entity_annotated.groupby(['sex_at_birth','race_ethnicity']).size().reset_index(name='counts')
df_entity_annotated.groupby(['pronoun_denoting_gender']).size().reset_index(name='counts')