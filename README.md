# Project-C-External---Gender-biased-representation-of-COVID19-Experts

## Key data files:

[News data extracted from media cloud](https://drive.google.com/file/d/13eB3LRXU-6yhsvbozqIcGqiSmoBdTqqr/view?usp=sharing)

[Individual data Raw](https://github.com/COVID19-DVRN/Project-C-External---Gender-biased-representation-of-COVID19-Experts/blob/master/inputs/race_gender_expertise_hack_on_your_own_time%20-%20Task%20Sheet%201.csv)

[Individual data cleaned](https://github.com/COVID19-DVRN/Project-C-External---Gender-biased-representation-of-COVID19-Experts/blob/master/outputs/data/08_01_01_entity_race_gender_expertise_news_count.csv)


[Network Edgelist](https://github.com/COVID19-DVRN/Project-C-External---Gender-biased-representation-of-COVID19-Experts/blob/master/outputs/network/05_01_01_comention_network_with_metadata.edgelist): The id corresponds to the unique id found in the individual data cleaned file.

## Key scripts:
[Named entity recognition](https://github.com/COVID19-DVRN/Project-C-External---Gender-biased-representation-of-COVID19-Experts/blob/master/scripts/00_01_01_create_names_from_sentences.py)

[Disambiguation of individuals and create unique id of individuals](https://github.com/COVID19-DVRN/Project-C-External---Gender-biased-representation-of-COVID19-Experts/blob/master/scripts/04_02_01_create_raw_name_to_disambiguated_name.py)

[Add metadata for all the individuals](https://github.com/COVID19-DVRN/Project-C-External---Gender-biased-representation-of-COVID19-Experts/blob/master/scripts/08_01_01_combine_race_gender_expertise_newscount_count.py)

[Network Analysis, degree distribution, power inequality in the network, assortativity analysis](https://github.com/COVID19-DVRN/Project-C-External---Gender-biased-representation-of-COVID19-Experts/blob/master/scripts/09_01_01_network_analysis_of_comention_network.py)

[Degree distribution stacked by attribute levels](https://github.com/COVID19-DVRN/Project-C-External---Gender-biased-representation-of-COVID19-Experts/blob/master/scripts/13_01_01_stacked_barplots_newscountdist_and_degree_dist.py)


### Useful instructions
Copy the raw data from media cloud named `Coronavirus_20200101_20200409_clean_expert` to `inputs/untracked`

```
python3 -m venv venv/
source venv/bin/activate
pip3 install -r requirements.txt
python3 -m spacy download en_core_web_sm
python3 -m nltk.downloader punkt
```

Copy the latest model of Stanford Core NLP from here: https://nlp.stanford.edu/software/CRF-NER.html . you will find a link titled `Download Stanford Named Entity Recognizer version 3.9.2` in that page. Then after extracting the zip copy `stanford-ner.jar`, `classifiers/english.all.3class.distsim.crf.ser.gz`, `classifiers/english.all.4class.distsim.crf.ser.gz`, and `classifiers/english.all.7class.distsim.crf.ser.gz` to `untracked/stanford-ner`.

To install java in macosx you can use brew cask
```
brew cask install java
```
