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
output_code = "13_01_01"

# %%
## Adding the metadata of each entity
df_entity_to_annotated_race_gender_expertise = pd.read_csv(f"../outputs/data/08_01_01_entity_race_gender_expertise_news_count.csv", na_filter=False)

df_entity_to_annotated_race_gender_expertise["entity_id"] = df_entity_to_annotated_race_gender_expertise["entity_id"].apply(lambda x: str(x))
metadata_index = 'entity_id'
metadata_list = [
                'entity_name',
                'sex',
                'pronoun',
                'race',
                'urm',
                "gender_urm",
                'public_health_researcher',
                'practitioner',
                'non_public_health_researcher',
                'policymaker',
                'industry_expert',
                'celebrity',
                'journalist',
                "expertise_label_by_relative_expertise",
                "expertise_label_by_relative_reach",
                'news_count',]

def merge_expertise(string):
    if string in ["journalist","industry_expert","celebrity","not_available"]:
        return "other"
    elif string in ["public_health_researcher","non_public_health_researcher"]:
        return "researcher"
    else:
        return string

df_entity_to_annotated_race_gender_expertise["merged_expertise"] = df_entity_to_annotated_race_gender_expertise["expertise_label_by_relative_expertise"].apply(merge_expertise)
 
dicts_entity_id_to_metadata = df_entity_to_annotated_race_gender_expertise.set_index(metadata_index).to_dict()

# %%
## Importing the network
input_dir="../outputs/network"
input_basename="comention_network_with_metadata"
input_full_fname=f"{input_dir}/05_01_01_{input_basename}.edgelist"
G = nx.readwrite.edgelist.read_edgelist(input_full_fname)

# %%
## Get the individuals with specific degree or mentions
count_types = ["degree count","news mention count"]
for count_type in count_types:
    dict_value_count_to_entity_ids = defaultdict(list)
    if count_type == "degree count":
        for entity_id, degree in G.degree():
            dict_value_count_to_entity_ids[degree].append(entity_id)
    elif count_type == "news mention count":
        for entity_id, news_count in dicts_entity_id_to_metadata["news_count"].items():
            dict_value_count_to_entity_ids[news_count].append(entity_id)

    # %%
    ## Get the attributes for the degree to entity_ids
    attributes = ["urm", "pronoun", "merged_expertise"]
    dict_attribute_levels = {
        "urm":["No","Yes"],
        "pronoun":["He","She","They"],
        "merged_expertise":["researcher","practitioner","policymaker","other"]
    }

    dict_attribute_levels_label = {
        "urm":["non-URM","URM"],
        "pronoun":["he","she","they"],
        "merged_expertise":["researcher","practitioner","policymaker","other"]
    }

    for attribute in attributes:
        dict_degree_to_attribute = {degree:[dicts_entity_id_to_metadata[attribute][entity_id] for entity_id in entity_ids] for degree,entity_ids in dict_value_count_to_entity_ids.items()}
        max_value_to_plot = 6
        combined_attributes_beyond_max_value = []
        for degree,attributes in dict_degree_to_attribute.items():
            if degree >= max_value_to_plot:
                combined_attributes_beyond_max_value.extend(attributes)
        dict_degree_to_attribute_values_beyond_max_combined = {k:v for k,v in dict_degree_to_attribute.items() if k < max_value_to_plot}
        dict_degree_to_attribute_values_beyond_max_combined[max_value_to_plot] = combined_attributes_beyond_max_value

        show_count_in_tick = True
        logx= False
        logy= False
        title = ""
        title = f"Distribution of {count_type} of \nindividuals by their attribute"
        savefig_dir = ""

        ## To make sure we have the same color for the whole range, we should use an array
        ## and an index
        current_attribute = attribute
        dict_values_by_attribute_level = {}
        counted_values = sorted(dict_degree_to_attribute_values_beyond_max_combined)
        for attribute in dict_attribute_levels[current_attribute]:
            attribute_count_for_sorted_values = []
            for value in counted_values:
                attribute_count_for_sorted_values.append(dict_degree_to_attribute_values_beyond_max_combined[value].count(attribute))
            dict_values_by_attribute_level[attribute] = attribute_count_for_sorted_values

        indices = range(len(counted_values))
        arr = np.zeros(shape=(len(dict_attribute_levels[current_attribute]),len(counted_values)))

        for i,attribute_level in enumerate(dict_attribute_levels[current_attribute]):
            arr[i] = dict_values_by_attribute_level[attribute_level]

        cumsum_bottom_values = np.zeros(len(counted_values))

        fig,ax = plt.subplots(figsize=(8,3.5))
        bars = []
        for i,attribute_level in enumerate(dict_attribute_levels[current_attribute]):
            print(i,attribute_level)
            values = arr[i]
            print(values)
            print(cumsum_bottom_values)
            bar=ax.bar(indices, values, bottom=cumsum_bottom_values)
            bars.append(bar)
            cumsum_bottom_values = cumsum_bottom_values+values

        val_with_count = [str(x[0])+"\n(%d)"%x[1] for x in zip(counted_values,[len(dict_degree_to_attribute_values_beyond_max_combined[degree]) for degree in counted_values])]
        xticks = range(len(counted_values))
        ax.set_xticks(xticks)
        if show_count_in_tick:
            ax.set_xticklabels(val_with_count)
        else:
            ax.set_xticklabels(counted_values)
        ax.set_ylabel("Count")
        ax.set_xlabel(current_attribute)
        ax.grid(axis="y", alpha = 0.5)
        if logx:
            ax.set_xscale('log')
        if logy:
            ax.set_yscale('log')
        if title:
            ax.set_title(title)
        ax.legend(bars, dict_attribute_levels_label[current_attribute])
        plt.tight_layout()
        count_type_name_for_fname= "_".join(count_type.split())
        savefig_dir = f"../figures/{output_code}_{count_type_name_for_fname}_by_{current_attribute}.png"
        if savefig_dir:
            plt.savefig(savefig_dir, dpi = 150)
        #plt.ylim(0,1e3)
        plt.show()




