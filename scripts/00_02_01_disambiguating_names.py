import spacy
import pandas as pd
import editdistance
import json
import pandas as pd
import disamby.preprocessors as pre
from disamby import Disamby
import unicodedata
# %%
output_code = "00_02_01"
# %%
with open("../outputs/data/00_01_01_tagged_names_from_expert_mention_articles.json", "r") as f:
    all_article_to_names = json.load(f)
# %%
space_separation_list = ["-", "―", "/"]
non_space_sepration_list = ["'",".","’",'“']
dubious_space_list = ["  ", "   ","  "]
removable_keywords = ["dr ", "dr."]
def preprocess_names(s):
    s = s.lower()
    for keyword in removable_keywords:
        s = s.replace(keyword,"")
    s = "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")
    ## First replacning all . and ' with non space
    translate_table = dict((ord(char), "") for char in non_space_sepration_list)
    s = s.translate(translate_table)
    ## Then replacing - wth space
    translate_table = dict((ord(char), "") for char in space_separation_list)
    s = s.translate(translate_table)
    ## Replacing double spaces with single space
    for dubious_space in dubious_space_list:
        s = s.replace(dubious_space," ")
    return s.strip()
# %%
## First we are creating an unique set of names from all the expert mention sentences we have found
all_names = set([preprocess_names(name) for name_lists in all_article_to_names.values() for name_list in name_lists for name in name_list])
# %%
## Then we will work with only the names that has at least two parts
all_two_part_names = [name for name in all_names if len(name.split()) > 1]
# %%
df = pd.DataFrame(all_two_part_names)
# %%
# define the pipeline to process the strings, note that the last step must return
# a tuple of strings
pipeline = [
    pre.normalize_whitespace,
    pre.remove_punctuation,
    lambda x: pre.trigram(x) + pre.split_words(x)  # any python function is allowed
]

# instantiate the disamby object, it applies the given pre-processing pipeline and
# computes their frequency.
dis = Disamby(df, pipeline)
# %%
sets = dis.disambiguated_sets(threshold=0.80)
# %%
mergeable_sets = [s for s in sets if len(s) > 1]
# %%
for sets in mergeable_sets:
    print([df.loc[s].item() for s in sets])
"""
['gen paul frieichs', 'paul frieichs']
['debra goff', 'debra a goff']
['chris cuomo', 'anew cuomo']
['david spiegel', 'paul spiegel']
['andy pekosz', 'anew pekosz']
['sharon goldfarb', 'anna goldfarb']
['george findlay', 'james findlay']
['burton amged el hawrani', 'amged el hawrani']
['kelly goldsmith', 'stephen goldsmith']
['william hanage', 'bill hanage']
['michael morley', 'john morley']
['jay powell', 'tia powell']
['benjamin chapman', 'ron chapman', 'ben chapman']
['li wenliang don', 'li wenliang', 'li wenliang li']
['ned benton', 'david benton']
['jason m opal', 'steven m opal']
['anea anea crisanti', 'anea crisanti']
['peter hotez', 'peter jay hotez']
['edward schneider', 'daniel schneider']
['erin sorrell', 'erin m sorrell']
['frank esper', 'mark esper']
['andy sumner', 'daniel sumner']
['debra vaselech lyons', 'vaselech lyons']
['david schwartz', 'brian schwartz']
['jonathan epstein', 'richard epstein', 'jon epstein', 'john epstein']
['david staples', 'erin staples']
['arthur reingold', 'arthur l reingold']
['steven mnuchin', 'steve mnuchin']
['john stern', 'hal stern']
['steny hoyer', 'steny h hoyer']
['caitlin rivers', 'caitlin m rivers']
['robert redfield', 'robert r redfield']
['david halpern', 'scott halpern']
['mike skinner', 'michael skinner']
['ellie cannon  cannon', 'ellie cannon']
['david michaels', 'jon michaels']
['erica s shenoy', 'erica shenoy']
['david r boulware', 'david boulware']
['nick wilson', 'mark wilson']
['benjamin cowling', 'ben cowling']
['michael mcbride', 'john mcbride']
['jesse goodman', 'jesse l goodman']
['ayatollah ali khamenei', 'ayatollah khamenei']
['lawrence gostin', 'lawrence o gostin']
['tark ji il', 'ji il tark']
['martin luther king jr', 'martin luther king']
['gary leroy', 'gary l leroy']
['amesh a adalja', 'amesh adalja']
['daniel alpert', 'dan alpert']
['ann wagner', 'robert wagner', 'gary wagner']
['joe cunningham', 'joe cunningham cunningham']
['mark hyman', 'jeffrey hyman']
['jim wright', 'ron wright']
['lindsey graham', 'sen lindsey graham']
['jonathan read', 'jon read']
['mark eisner', 'michael eisner']
['steve taylor', 'john taylor', 'steven taylor']
['neil m ferguson', 'neil ferguson']
['ann carlson', 'chris carlson']
['jennifer sullivan', 'david sullivan']
['joshua m sharfstein', 'joshua sharfstein', 'josh sharfstein']
['hitoshi oshitani', 'd hitoshi oshitani']
['amir a afkhami', 'amir afkhami']
['anew coggins', 'anew coggins jr']
['lee kaplan', 'steven kaplan']
['michael waldman', 'ron waldman']
['summer johnson mcgee', 'summer mcgee']
['david reich', 'robert reich']
['jeffrey shulman', 'peter shulman']
['megan ranney', 'megan l ranney']
['john wilson', 'ian wilson']
['john brooks', 'daniel brooks']
['michael siegel', 'robert siegel']
['jeffrey klausner', 'jeffrey d klausner']
['dong yan jin', 'jin dong yan']
['peter sinclair', 'alison sinclair']
['john campbell', 'david campbell', 'james campbell', 'alan campbell']
['jennifer cassidy', 'bill cassidy']
['lisa friedman', 'tom friedman']
['john crozier', 'brett crozier']
['william schaffner', 'don schaffner', 'donald schaffner']
['alfred wu', 'alfred m wu']
['sam hayes', 'chris hayes']
['bessey e geevarghese', 'bessey geevarghese']
['geoffrey s gottlieb', 'geoffrey gottlieb']
['john williams', 'ian williams']
['courtney subramanian trump', 'courtney subramanian']
['john callahan', 'michael callahan']
['stephen griffin', 'daniel griffin']
['david freedman', 'anew freedman']
['stephen lynch', 'john lynch']
['john logan', 'james logan']
['jennifer ashton', 'john ashton', 'jen ashton']
['maria kerkhove', 'van kerkhove', 'maria van kerkhove']
['richard jackson', 'david jackson']
['michael brady', 'tom brady']
['deborah l birx', 'deborah birx']
['jim luke', 'chris luke']
['peter osborne', 'joe osborne']
['james cherry', 'robert cherry']
['stephen hahn', 'steven hahn']
['steve mclaughlin', 'michael mclaughlin']
['nancy knight', 'michael knight']
['david heymann', 'david l heymann']
['carolyn cannuscio', 'carolyn c cannuscio']
['john redd', 'stephen redd']
['steve wasserman', 'michael wasserman']
['john wiesman', 'jonathan wiesman']
['patrick soon shiong', 'soon shiong']
['william walters', 'anne walters']
['susan hopkins', 'john hopkins']
['james chalmers', 'jim chalmers']
"""
# %%
## Whenever we find a prepreprocessed anme to be a key in this file, we will
## replace them with the value
mergeable_names_by_inspecting_output_from_the_previous_cell = {
        "gen paul frieichs":"paul frieichs",
        "debra goff": "debra a goff",
        "anew cuomo": "andrew cuomo",
        "anew pekosz":"andy pekosz",
        "burton amged el hawrani":"amged el hawrani",
        "ben chapman":"benjamin chapman",
        "li wenliang li":"li wenliang",
        "li wenliang don": "li wenliang",
        "anea anea crisanti":"anea crisanti",
        "peter hotez":"peter jay hotez",
        "erin sorrell":"erin m sorrell",
        "vaselech lyon":"debra vaselech lyons",
        "steven mnuchin":"steve mnuchin",
        "steny hoyer":"steny h hoyer",
        "caitlin rivers":"caitlin m rivers",
        "robert redfield":"robert r redfield",
        'mike skinner':'michael skinner',
        'ellie cannon  cannon': 'ellie cannon',
        'erica shenoy':'erica s shenoy',
        'david boulware':'david r boulware',
        'ben cowling':"benjamin cowling",
        'jesse goodman': 'jesse l goodman',
        'ayatollah khamenei':"ayatollah ali khamenei",
        'lawrence gostin':'lawrence o gostin',
        'tark ji il': 'ji il tark',
        'martin luther king':'martin luther king jr',
        'gary l leroy':'gary leroy',
        'amesh adalja':'amesh a adalja',
        'dan alpert':'daniel alpert',
        'joe cunningham cunningham':'joe cunningham',
        'sen lindsey graham':'lindsey graham',
        'jon read':'jonathan read',
        'neil ferguson':'neil m ferguson',
        'joshua sharfstein':'joshua m sharfstein',
        'josh sharfstein':'joshua m sharfstein',
        'd hitoshi oshitani':'hitoshi oshitani',
        'amir afkhami':'amir a afkhami',
        'anew coggins jr':"andrew coggins jr",
        "anew coggins":"andrew coggins",
        'summer mcgee':'summer johnson mcgee',
        'megan ranney':'megan l ranney',
        'jeffrey klausner':'jeffrey d klausner',
        'dong yan jin':'jin dong yan',
        'don schaffner':'donald schaffner',
        'alfred wu':'alfred m wu',
        'bessey geevarghese':'bessey e geevarghese',
        'geoffrey gottlieb':'geoffrey s gottlieb',
        'courtney subramanian trump':'courtney subramanian',
        'anew freedman':'andrew freedman',
        'jen ashton':'jennifer ashton',
        'maria kerkhove':'maria van kerkhove',
        'van kerkhove': 'maria van kerkhove',
        'deborah birx':'deborah l birx',
        'david heymann': 'david l heymann',
        'carolyn cannuscio': 'carolyn c cannuscio',
        'john wiesman': 'jonathan wiesman',
        'soon shiong':'patrick soon shiong',
        'jim chalmers':'james chalmers',
        'anew winton':"andrew winton",
        "anthony fauci white house":"anthony fauci",
        "tony fauci":"anthony fauci",
        "faucis": "anthony fauci",
        "anthony fauci \u2014":"anthony fauci",
        "anthony s. fauci":"anthony fauci",
        "anthony s fauci":"anthony fauci",
        "anthony fauci fauci":"anthony fauci",
        "anthony fauci anthony fauci":"anthony fauci",
        "antony fauci":"anthony fauci"
        ""
    }
# %%
## Now lets work with the names that are only a single last name
leftover_names = all_names - set(all_two_part_names)

all_two_part_names_removing_duplicates = set(all_two_part_names) - set(mergeable_names_by_inspecting_output_from_the_previous_cell.keys())
# %%
## Now lets first get all the candidate for these names:
removal_shortlist = []
confirmed_single_name_to_ful_name = {}
for single_name in leftover_names:
    candidates = [name for name in all_two_part_names_removing_duplicates if single_name in name]
    ## We will only handcheck the candidates in the length of candidates less than 4
    if len(candidates) == 0:
        removal_shortlist.append(single_name)
    elif len(candidates) == 1:
        confirmed_single_name_to_ful_name[single_name] = candidates[0]
    elif len(candidates) < 4:
        print(single_name,candidates)
    else:
        pass
        #print(single_name, "we really can not disambiguate this name")
# %%
## After manual inspection we are removing some of the wrong candidates from the 
## confirmed list The are:
    
"""
{'mcmaster': 'henry mcmaster',
 'queen': 'queensland heath',
 'daszak': 'peter daszak',
 'pepper': 'pepper schwartz',
 'moynihan': 'don moynihan',
 'zacharin': 'margaret zacharin',
 'bedford': 'trevor bedford',
 'pearce': 'rod pearce',
 'meissner': 'h cody meissner',
 'zarif': 'mohammad javad zarif',
 'ingraham': 'laura ingraham',
 'segal': 'scott segal',
 'gostin': 'lawrence o gostin',
 'easter': 'easter swander',
 'pompeo': 'mike pompeo',
 'balmes': 'john r balmes',
 'carey': 'mariah carey',
 'chowdhury': 'abdul mabud chowdhury',
 'falwell': 'jerry falwell jr',
 'boulware': 'david r boulware',
 'burr': 'scott burris',
 'andersen': 'kristian andersen',
 'romney': 'mitt romney',
 'torres': 'john torres',
 'desantis': 'ron desantis',
 'fairbanks': 'abbey hardy fairbanks',
 'iwata': 'kentaro iwata',
 'jeanine': 'jeanine pirro',
 'vaughan': 'nilam vaughan',
 'calle': 'paul calle',
 'bush': 'george w bush',
 'sklar': 'phil sklar',
 'weisenberg': 'scott weisenberg',
 'frost': 'wilfred frost',
 'blakely': 'tony blakely',
 'hanks': 'tom hanks',
 'sherman': 'jeff sherman',
 'quigley': 'robert quigley',
 'zelenko': 'vladimir zelenko',
 'winton': 'anew winton',
 'camilla': 'camilla pashley',
 'bezos': 'jeff bezos',
 'catton': 'mike catton',
 'carome': 'michael carome',
 'mullen': 'danielle mcmullen',
 'pankhania': 'bharat pankhania',
 'aylward': 'bruce aylward',
 'pena': 'eric cioe pena',
 'gaetz': 'matt gaetz',
 'alich': 'matthew alich',
 'irani': 'irani thevarajan',
 'kinachuck': 'jason kinachuck',
 'lockhart': 'joe lockhart',
 'hostin': 'sunny hostin',
 'corrigan': 'patrick corrigan',
 'schumer': 'chuck schumer',
 'bowser': 'muriel bowser',
 'pelosi': 'nancy pelosi',
 'kuppalli': 'krutika kuppalli',
 'monto': 'arnold monto',
 'kalil': 'ane kalil',
 'hariri': 'robert hariri',
 'calderwood': 'catherine calderwood',
 'harley': 'harley rouda',
 'kong': 'zeng lingkong',
 'barney': 'barney graham',
 'peterson': 'jordan peterson',
 'barbot': 'oxiris barbot',
 'deere': 'judd deere',
 'marrazzo': 'jeanne marrazzo',
 'sens': 'larry eisenstein',
 'asgari': 'sirous asgari',
 'agus': 'david agus',
 'dewine': 'mike dewine',
 'nichole': 'nichole quick',
 'macron': 'emmanuel macron',
 'bresee': 'joe bresee',
 'nero': 'josue david cisneros',
 'redfield': 'robert r redfield',
 'oxiris': 'oxiris barbot',
 'garg': 'sandeep garg',
 'jain': 'yogesh jain',
 'brix': 'deborah brix',
 'winch': 'richard winchester',
 'hotez': 'peter jay hotez',
 'cowling': 'benjamin cowling',
 'quest': 'quest diagnostics',
 'fusco': 'grace fusco',
 'josephine': 'josephine wolff',
 'zuckerberg': 'mark zuckerberg',
 'rivkees': 'scott rivkees',
 'said': 'gabriel said reynolds',
 'manly': 'john manly',
 'qingyan': 'qingyan chen',
 'northam': 'ralph northam',
 'messonnier': 'nancy messonnier',
 'bolsonaro': 'jair bolsonaro',
 'harries': 'jenny harries',
 'iwasaki': 'akiko iwasaki'}
"""   
## We will be removing some of those keys from the confirmed list 
"""
'quest': 'quest diagnostics'
'said': 'gabriel said reynolds',
winch': 'richard winchester',
'sens': 'larry eisenstein',
'winton': 'anew winton',
'queen': 'queensland heath'
"""
confirmed_single_name_to_ful_name["fauci"] = "anthony fauci"
for removal_key in ['quest','said','winch','sens','queen']:
    del confirmed_single_name_to_ful_name[removal_key]

removal_list = ['zika','peacehealth','vox','healthlandscape','wired','tesla',
                'weibo','vrbo','forbes','prezcobix','teamhealth','ontario',
                '338','twitter','vcnx','keurig', 'celularity', 'whatsapp','bosch',
                'moderna','marketwatch','remdesivir','quest','queen','queensland heath','-']
# %%
## So now we have two dictionaries and one list
## First one maps duplicate name to an actual name
## and the second one maps the single name to a full first name
## then final there are some entities we will not keep anymore
deduplication_dictionary = {}
for raw_name in set([name for name_lists in all_article_to_names.values() for name_list in name_lists for name in name_list]):
    processed_name = preprocess_names(raw_name)
    if processed_name in removal_list:
        continue
    else:
        if processed_name in mergeable_names_by_inspecting_output_from_the_previous_cell:
        ## If the name is in the deduplication dict we will take the value of the deduplication list
            deduplication_dictionary[raw_name] = mergeable_names_by_inspecting_output_from_the_previous_cell[processed_name]
        elif processed_name in confirmed_single_name_to_ful_name:
        ## if the name is a single laste name then we will redirect it to the longer name
            deduplication_dictionary[raw_name] = confirmed_single_name_to_ful_name[processed_name]
        else:
        ## Else we will only keep the final 
            deduplication_dictionary[raw_name] = processed_name
# %%
with open("../outputs/data/%s_name_dedpulication_dictionary.json" %output_code, "w") as f:
    json.dump(deduplication_dictionary,f)
    
# %%
with open("../outputs/data/%s_more_disambiguation_requied.csv" %output_code, "w") as f:
    f.writelines("\n".join(sorted(set(deduplication_dictionary.values()))))
