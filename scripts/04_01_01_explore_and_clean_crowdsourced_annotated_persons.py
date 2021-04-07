# -*- coding: utf-8 -*-
"""
Summary: This script inputs the crowdsourced annotated race, gender, and expertise

Input: race_gender_expertise_hack_on_your_own_time - Task Sheet 1.csv

Output: Cleaned Gender, Race/Ethnicity, and Expertise of the people
"""

import pandas as pd
pd.options.display.width = 0
import networkx as nx
from collections import defaultdict, Counter
import matplotlib.pyplot as plt

# %%
output_code = "04_01_01"
# %%
report_lines = []
df = pd.read_csv("../inputs/race_gender_expertise_hack_on_your_own_time - Task Sheet 1.csv", na_filter=False)
df_non_self = df.loc[df["possible_candidate"]!="SELF",["raw_name","possible_candidate"]]
df_na = df_non_self.loc[df_non_self["possible_candidate"]=="na",["raw_name","possible_candidate"]]
report_lines.append(f"We have total {df_na['possible_candidate'].count()} number of rows which we weould discard because they are detected as not available (na)")
report_lines.append(df_na.to_string(index=False))

# %%
## Then we explore the names where the possible candidate is not "SELF" and is not "na"
df_non_self_non_na = df_non_self.loc[df_non_self["possible_candidate"]!="na",["raw_name","possible_candidate"]]
report_lines.append(f"We have total {df_non_self_non_na['possible_candidate'].count()} number of rows which would potentially merge with some other candidates")
report_lines.append(df_non_self_non_na.to_string(index=False))

# %%
## Now doing a double check whether any of the raw_name and possible_cnadidate are same. 
df_non_self_non_na_same_name = df_non_self_non_na.loc[df_non_self_non_na["possible_candidate"]==df_non_self_non_na["raw_name"],["raw_name","possible_candidate"]]
if len(df_non_self_non_na_same_name) == 0:
	report_lines.append("We do not have any non SELF non na name that is same as the raw name")
else:
	report_lines.append(f"We have {len(df_non_self_non_na_same_name)} number of non SELF non na name that is same as the raw name")
	report_lines.append(df_non_self_non_na_same_name.to_string(index=False))

# %%
## Now lets double check if all the names that have are different from raw name and not na, can be found inside the actual raw names that are "SELF"
df_self = df.loc[df["possible_candidate"]=="SELF",["raw_name","possible_candidate"]]
names_that_are_self = df_self["raw_name"].values
names_that_are_self_or_na = (df.loc[df["possible_candidate"].isin(["SELF","na"]),["raw_name","possible_candidate"]])["raw_name"].values
df_disambiguate_names_not_found_in_self = df_non_self_non_na.loc[~df_non_self_non_na["possible_candidate"].isin(names_that_are_self),["raw_name","possible_candidate"]]

## First I will explore the names that are 
with open(f"../outputs/reports/{output_code}_report.txt", "w") as f:
	f.writelines("\n".join(report_lines))
