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
import networkx as nx
from collections import defaultdict, Counter
import matplotlib.pyplot as plt

# %%
output_code = "04_02_01"
# %%
