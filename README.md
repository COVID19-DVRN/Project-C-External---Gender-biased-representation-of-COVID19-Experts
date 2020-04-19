# Project-C-External---Gender-biased-representation-of-COVID19-Experts

Copy the raw data from media cloud named `Coronavirus_20200101_20200409_clean_expert` to `input/untracked`

```
python3 -m venv venv/
source venv/bin/activate
pip3 install -r requirements.txt
python3 -m spacy download en_core_web_sm
python -m nltk.downloader punkt
```

Copy the latest model of Stanford Core NLP from here: https://nlp.stanford.edu/software/CRF-NER.html . you will find a lonk titled `Download Stanford Named Entity Recognizer version 3.9.2` in that page. Then after extracting the zip copy `stanford-ner.jar` and `classifiers/english.all.3class.distsim.crf.ser` `classifiers/english.all.4class.distsim.crf.ser` and `classifiers/english.all.7class.distsim.crf.ser` to `untracked/stanford-ner`.

To install java in macosx you can use brew cask
```
brew cask install java
```