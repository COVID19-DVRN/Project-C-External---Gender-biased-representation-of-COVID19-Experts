# -*- coding: utf-8 -*-
"""
Summary: 
	In this script I will perform the network analysis of the comention network
Input:
	./outputs/data/05_01_01
Output:
	Some outputs
"""

import pandas as pd
import json
from collections import defaultdict
from unidecode import unidecode
import unicodedata
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
pd.options.display.width = 0

# %%
output_code = "12_01_01"

# %%
df= pd.read_csv("../outputs/data/11_01_01_matched_data.csv")

# %%
## Getting the mean by subclass and by minority status
df.groupby(["subclass","urm"], as_index=False)['news_count'].mean()
