# -*- coding: utf-8 -*-
import pandas as pd
import unicodedata
import networkx as nx
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
# %%
output_code = "03_01_01"
# %%
df = pd.read_csv("../inputs/untracked/Coronavirus_20200101_20200409_clean_expert_bigger.csv")
outlets = df["media_name"].values
count_outlets = Counter(outlets)

## Exploring what are the links that is associated with drudgereport
df_drudge = df[df["media_name"]=="drudgereport"]
urls = df_drudge["url"].values
print(Counter([x.strip().split("//")[1].split("/")[0] for x in  urls]))
## Counter({'www.dailymail.co.uk': 1633})
## So all 1633 drudge report urls are coming from dailymail

## Replacing drudgerreport with dailymail, bacuase we know that in this dataset
## all the news that is coming from drudgereport are actually from dailymail
count_outlets["Daily Mail"] = count_outlets["drudgereport"]
del count_outlets["drudgereport"]

keys, values = zip(*sorted(count_outlets.items(), key = lambda x:x[1]))
fig,ax = plt.subplots(figsize = (10,7))
ax.barh(keys,values,color='#0504aa', alpha=0.6)
for i, v in enumerate(values):
    ax.text(v + 3.5, i - 0, str(v), color='blue', fontsize = 8)
#ax.set_yticklabels(ticklabels)
#ax.set_xlim(0,140)
plt.tight_layout()
plt.savefig("../figures/%s_distribution_of_news_outlets.png" %(output_code))
plt.show()

# %%
## Creating the story id to outlet
df_story_id_to_outlet = df[["stories_id","media_name"]].copy()
## Becuase all of the drudger report news are coming from daily mail
## we will change it to daily mail
df_story_id_to_outlet["outlet"] = df_story_id_to_outlet["media_name"].apply(lambda x: x if x!="drudgereport" else "Daily Mail")
df_story_id_to_outlet.to_csv(f"../outputs/data/{output_code}_story_id_to_outlet_name.csv",index=False)