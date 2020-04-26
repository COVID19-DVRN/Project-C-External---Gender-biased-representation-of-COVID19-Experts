import spacy
import json
import pandas as pd
## for standford ner tagger
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import editdistance
# %%
## the setting up of the stanfrod ner tagger code is borrowed from 
## https://pythonprogramming.net/named-entity-recognition-stanford-ner-tagger/
st = StanfordNERTagger('../untracked/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
					   '../untracked/stanford-ner/stanford-ner.jar',
					   encoding='utf-8')
r=st.tag('Rami Eid is studying at Stony Brook University in NY'.split())
print(r) 

## Using answer from this link we get the multi term ner tagger from stanford ner
## https://stackoverflow.com/questions/30664677/extract-list-of-persons-and-organizations-using-stanford-ner-tagger-in-nltk

# %%
# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")

# %%
def remove_special_characters(s):
    punct_list = ['!', '"', '#', '$', '%', "'", '(', ')', '*', '+', ',', '/', ':', ';', 
                     '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '\n','■','•','”', '”',"’","-"]
    translate_table = dict((ord(char), " ") for char in punct_list)
    s = s.translate(translate_table)
    return s

def get_continuous_chunks(tagged_sent):
    continuous_chunk = []
    current_chunk = []

    for token, tag in tagged_sent:
        if tag != "O":
            current_chunk.append((token, tag))
        else:
            if current_chunk: # if the current chunk is not empty
                continuous_chunk.append(current_chunk)
                current_chunk = []
    # Flush the final current_chunk into the continuous_chunk, if any.
    if current_chunk:
        continuous_chunk.append(current_chunk)
    return continuous_chunk

def get_all_entities_from_stanfor_ner(sentence,stanfor_ner_tagger = st):
    ne_tagged_sent = st.tag(word_tokenize(sentence))
    named_entities = get_continuous_chunks(ne_tagged_sent)
    named_entities_str_tag = [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities]
    return named_entities_str_tag

def get_persons(text,model):
    if model=="stanford":
        person_names = [ent[0] for ent in get_all_entities_from_stanfor_ner(text) if ent[1]=="PERSON"]
    elif model=="spacy":
        doc = nlp(text)
        person_names = [entity.text for entity in doc.ents if entity.label_=="PERSON"]
    return person_names

        
# %%
df_orig = pd.read_csv("../inputs/untracked/Coronavirus_20200101_20200409_clean_expert.csv")
df = df_orig[["stories_id","url","Text","Expert_Mention_Sentence_List"]]
df = df.set_index("stories_id")


# %%
def get_all_persons_from_whole_article(story_id, df = df, model="stanford"):
    """

    Parameters
    ----------
    story_id : TYPE
        DESCRIPTION.
    df : TYPE, optional
        DESCRIPTION. The default is df.
    model : TYPE, optional
        DESCRIPTION. The default is "stanford".
        Options are "stanford" and "spacy". "spacy" is less accurate

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    text = df.loc[story_id,"Text"]
    return get_persons(text,model=model)

def check_single_name_matches_fuzzily_with_any_part_of_full_name(single_name, full_name):
    single_name = remove_special_characters(single_name.strip().lower()).strip()
    full_name = remove_special_characters(full_name.strip().lower()).strip()
    full_name_parts = full_name.split()
    for part in full_name_parts:
        part = remove_special_characters(part.strip().lower()).strip()
        if editdistance.eval(single_name,part) <= 2:
            return True
    return False
            

def get_target_full_name_using_single_name_from_article(single_name,story_id,df=df,model="stanford"):
    """

    Parameters
    ----------
    single_name : TYPE
        the name we want to find in the whole article who might be in two pieces
        e.g. cramer in one article is somehow mentioned as "jim cramer", we want
        to capture that
    story_id : TYPE
        story_id in the dataframe provide by Marie
    df : TYPE, optional
        DESCRIPTION. The default is df.
    model : TYPE, optional
        DESCRIPTION. The default is "stanford".
        Options are "stanford" and "spacy". "spacy" is less accurate
    Returns
    -------
    TYPE
        DESCRIPTION.
    
    One example on why we should use editdistance for two length list
    1508781606 [['New state government requirements demand residents to self-isolate for 14 days from when they left Wuhan, says chief health officer Dr Jeannette Young.'], ['Dr Young said the football team posed no risk to the Queensland community.'], ["'That restaurant is OK to go to now, people don't need to avoid the area or indeed anywhere else,' Victoria's Chief Health Officer Dr Brett Sutton said."], ['Dr Sutton said health authorities had followed up with the restaurant, as well as patrons who were there on that evening.']]
	jeannette young
	young
    we have these ambiguous cnadidate names so returning none ['jeannette young', 'jeanette young']
    
    
   One example why we needed strip afer special character removal
1521492048 [['“If the public had believed these ‘rumors’ at the time, and carried out measures like wearing masks, strictly disinfecting and avoiding wildlife markets … it might have been a good thing,” wrote Judge Tang Xinghua in the Supreme Court statement, closely echoing what Dr. Zeng said in his Global Times interview.']]
	tang xinghua
	zeng
[['tang xinghua', None]]
    """
    single_name = remove_special_characters(single_name.strip().lower()).strip()
    all_names = [remove_special_characters(name.strip().lower()).strip() for name in get_all_persons_from_whole_article(story_id,df=df,model=model)]
    #print(all_names)
    candidate_names = set([name for name in all_names if single_name in name])
    ## if a spacy single name get searched by stanford all names
    if single_name in candidate_names:
        candidate_names.remove(single_name)
    candidate_names = list(candidate_names)
    #print(candidate_names)
    if len(candidate_names) < 1:
        ## One more check for speelng mistake in the single name e.g. 
        ## messonnier was spelled messonier somewhere and it missed the actual name
        #print("checking messonier")
        for full_name in all_names:
            if check_single_name_matches_fuzzily_with_any_part_of_full_name(single_name,full_name):
                candidate_names.append(full_name)
        ## example of new candidate names ['nancy messonnier', 'messonnier']
        ## now we will return larger of the two because that is most possible full name
        if candidate_names:
            return(sorted(candidate_names,key=len)[-1])
        else:
            return single_name
    else:        
        candidates_without_exact_self_match = set(candidate_names)
        ## if a spacy single name get searched by stanford all names
        if single_name in candidates_without_exact_self_match:
            candidates_without_exact_self_match.remove(single_name)
        candidates_without_exact_self_match = list(candidates_without_exact_self_match)
        if len(candidates_without_exact_self_match) == 1:
            return(candidates_without_exact_self_match[0])
        elif len(candidates_without_exact_self_match) == 2:
            ## if there are are two candidates we will check if the edit distance is
            ## less than 2, in that case we will take the longer one
            ## e.g. ['jeannette young', 'jeanette young']
            #print(candidates_without_exact_self_match)
            if editdistance.eval(*candidates_without_exact_self_match) <= 1:
                return((sorted(candidates_without_exact_self_match)[-1]))
                ## Taking the longer one is an arbitrary decision, but for now I am taking this decsion based
                ## on the single example I have
            else:
                return(single_name)
        elif len(candidates_without_exact_self_match)==0:
            ## We could not find a better name so returning single name
            return single_name
        else:
            ## We could not find a better name so returning single name
            print("we have these ambiguous candidate names so returning none",candidates_without_exact_self_match)
            return single_name

# %%
# =============================================================================
# models = ["stanford","spacy"]
# for story_id,sentence_lists in df.to_dict()["Expert_Mention_Sentence_List"].items():
#     print(story_id, sentence_lists)
#     for sentence in eval(sentence_lists):
#         for model in models:
#             print(model)
#             for person_name in get_persons(sentence[0],model=model):
#                 print("\t"+person_name)
#     input("Press Enter to continue...")
# =============================================================================
# %%
# #Couldn't detect the name
## 1511515765 [['"There are lots of very smart people in this business, but very few of them are infectious disease experts," Cramer said, arguing that Thursday\'s run shouldn\'t have happened']]
## The same
"""
1511515765 [['"There are lots of very smart people in this business, but very few of them are infectious disease experts," Cramer said, arguing that Thursday\'s run shouldn\'t have happened.']]
stanford
	Cramer
spacy
"""

## Once agian stanford is better at detecting the three word names
"""
Press Enter to continue...
1515330175 [['“It’s a ridiculous assertion,” said Dr. Michael Mina, assistant professor of epidemiology and immunology at Harvard University.'], ['“Misinformation around these outbreaks is definitely a problem,” said Dr. Tara Kirk Sell, senior scholar at Baltimore’s Johns Hopkins Center for Health Security.']]
stanford
	Michael Mina
spacy
	Michael Mina
stanford
	Tara Kirk Sell
spacy
	Tara Kirk
"""

## Repeated news
## 157,1545400665,1/31/2020 16:40,"11 questions about the Covid-19 coronavirus outbreak, answered",https://www.vox.com/2020/1/31/21113178/what-is-coronavirus-symptoms-travel-china-map?utm_source=facebook&utm_campaign=vox.social&utm_content=voxdotcom&utm_medium=social,en,False,"medicine and health, diseases and conditions, travel and vacations, viruses",104828,Vox,
## 164,1511004242,1/31/2020 16:35,"8 questions about the coronavirus outbreak, answered",https://www.vox.com/2020/1/31/21113178/what-is-coronavirus-symptoms-travel-china-map

## In some sentences we miss the name because it ended with something like "said dr."
## 1510939280 [[', this is what is killing us,” said UC Riverside epidemiologist Brandon Brown'], ['Advertisement “Get your flu shot — take measures to prevent getting sick with the many things in this country we have to get sick from,” said Tufts Medical Center infectious disease specialist Dr'], ['To protect against the flu — or coronavirus, if that’s your concern — people should wash their hands frequently, sneeze or cough into the crook of their elbow and avoid contact with ill people, said Dartmouth College professor Dr']]    

## For some reason spacy is only detecting the names with Two parts Firstname Surname, but the ones with a single surname or even some of them with three part, it is missing
## 1510576258 [['Stacie San Miguel, the director of medical services at the University of California, San Diego’s student health center, said students and others had been flocking to physicians for checkups']]
## In this case stanford is working
"""
1510576258 [['Stacie San Miguel, the director of medical services at the University of California, San Diego’s student health center, said students and others had been flocking to physicians for checkups']]
stanford
	Stacie San Miguel
spacy
"""

## Sometimes there are names which have dash separated last name, they are well recognized by spacy
## 1510550623 [['People who are well should refrain from hoarding masks \'just in case\' they need it, as this may lead to a lack of masks in settings that really need it," said Annelies Wilder-Smith, a professor of emerging infectious diseases at the London School of Hygiene and Tropical Medicine'], ['"While we should take the outbreak seriously, we mustn\'t panic and behave in a manner that is disproportionate to the threat we are confronted with," said Wilder-Smith, who was a front-line clinician at Singapore\'s Tan Tock Seng Hospital during the severe acute respiratory syndrome outbreak in 2003'], ['As countries around the world guard against the viral outbreak, the scramble for face masks as a form of psychological aid is "completely understandable," said William Schaffner, an infectious diseases expert at the Vanderbilt University\'s Medical Center in Nashville, Tennessee']]
## Annelies Wilder-Smith
## Wilder-Smith
## William Schaffner

## False Positive of person recognition
## 1510472231 [['Queensland Health chief officer Dr Jeannette Young on Thursday said she was concerned about everyone on the plane']]
## Queensland Health
## Jeannette Young
## Stanford doesn't recognize Queensland health

## WE are missing any name, but there is a "he says" term in the sentence
## 1545436144 [['But the Centers for Disease Control has been proactive from the beginning, setting up protocols to screen travelers who are returning from China, and pushing out information to clinicians about how to be alert for the virus, he says']]

## We are missing Dr Tedros Adhanom Ghebreyesus
## 1510421385 [["Speaking to reporters, WHO Director-General Dr Tedros Adhanom Ghebreyesus said: 'The main reason for this declaration is not because of what is happening in China, but because of what is happening in other countries"], ['They all took Tiger Air flight TT566, landing on the Gold Coast about 8pm on Monday on a plane that carries up to 189 passengersQueensland Health chief officer Dr Jeannette Young on Thursday said she was concerned about everyone on the plane']]
## Tiger Air
## Jeannette Young
"""
stanford
	Jeannette Young
spacy
	Tiger Air
	Jeannette Young
"""


## After adding Stanford most of the time stanford works better than spacy but this is one example where spacy is better:
## 1512650660 [['Matthew Kennedy analyst at Renaissance Capital Gary Dushnitsky, associate professor of strategy and entrepreneurship at the London Business School, who has studied the role of corporations in venture investing, said some corporates invest in start-ups with an explicit goal of generating financial returns — with the belief that they are better at evaluating and nurturing start-ups and therefore should make superior returns'], ['Reena Aggarwal, a Georgetown University business professor and IPO expert said many of these investors are not flippers and do look at holdings on a longer-term basis']]
##stanford
##	Matthew Kennedy
##spacy
##	Matthew Kennedy
##	Gary Dushnitsky


"""
1510456517 [['Additional resources from non-governmental organizations including Doctors Without Borders and charitable groups such as the Bill and Melinda Gates Foundation could be extremely useful for governments struggling to bring in medical teams and identify infected persons, Gostin said']]
stanford
	Bill
	Gostin
spacy
	Bill
	Gostin

Press Enter to continue...
1511797507 [['“Alex has pushed to see if we can send some of our people there to not only help the Chinese but also get some information that would inform our strategies and response," said Fauci, the infectious disease doctor']]
stanford
	Alex
	Fauci
spacy
	Fauci
"""

##Sometimes surprisingly spacy detects soemthing that Stanfrod couldn't
"""
1510405065 [["Virologist and professor of microbiology and immunology at Columbia University Vincent Racaniello, PhD, spoke about the virus on Monday and said it differs from SARS in that it's spreading outside of the medical community"]]
stanford
spacy
	Vincent Racaniello
"""

## Spacy  doesn't detect the single name persons
"""
Press Enter to continue...
1532063047 [['“This is the time for science, not rumors,” Dr Tedros said']]
stanford
	Tedros
spacy
"""

## Again stanford does better on single name stuffs
"""
1510291862 [['"The fact that such warm water was just now recorded by our team along a section of Thwaites grounding zone where we have known the glacier is melting suggests that it may be undergoing an unstoppable retreat that has huge implications for global sea-level rise," explains Holland, a professor at NYU\'s Courant Institute of Mathematical Sciences']]
stanford
	Holland
spacy
"""

"""
297,1510881493,1/31/2020 13:33,U.S. Imposes Coronavirus Quarantine on Group in California Evacuated From Wuhan,https://www.nytimes.com/2020/01/31/health/quarantine-coronavirus.html,en,False,,1,New York Times,http://nytimes.com,
"Dr. Messonnier called the federal order on Friday “science-based,” saying it was warranted because of the worsening epidemic in China. She cited the widening, rapid spread of the disease there, the increase in person-to-person transmission and the rising death toll. In addition, evidence has been emerging that people can transmit the disease even before they show symptoms of the illness, which can cause pneumonia in severe cases. Another concern was that the passengers evacuated had been in Wuhan, the epicenter of the outbreak. At a news conference later on Friday, Alex M. Azar II, the secretary of health and human services, announced that other citizens of the United States who were returning from Hubei Province, which includes Wuhan, would also be quarantined for up to two weeks. Mr. Azar declared a public health emergency for the United States, and said foreign nationals who had been to China during the last 14 days would not be allowed into the United States. “This is a very serious public health situation, and the C.D.C. and federal government have and will continue to take aggressive action to protect the public,” Dr. Messonnier said. “If we take strong measures now, we may be able to blunt” the impact of the virus in the United States. Dr. Messonnier said that the people who were quarantined did not pose a threat to the surrounding community. Since the 195 evacuees arrived in Riverside, they have had their noses and throats swabbed to test for the virus, and their temperatures taken several times a day. They were initially told that they would be detained for at least 72 hours, and possibly 14 days. Two weeks is thought to be the upper limit of the incubation period; if symptoms don’t start by then, a person can be cleared as not infected.",0.0,271,13.0,342.0,26.307692307692307,0.30116959064327486,0.21929824561403508,0.06984615384615385,0.8554615384615384,0.07476923076923077,0.05350000000000002,1,"[['Dr.', 'said'], ['Dr.', 'said']]","[['and federal government have and will continue to take aggressive action to protect the public,” Dr. Messonnier said.'], ['Dr. Messonnier said that the people who were quarantined did not pose a threat to the surrounding community.']]",1,3,5,6,1,3,5,6,pneumonia in severe case,pneumonia in severe cases,['NA'],['NA'],['NA'],['NA'],and the rising death,['NA'],['NA'],['NA'],['NA'],['NA'],NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,2020-01-31,1/31/2020,660
"""

## One example of enahancing the name from the whole article instead of the 
## target sentence
"""
1510291862 [['"The fact that such warm water was just now recorded by our team along a section of Thwaites grounding zone where we have known the glacier is melting suggests that it may be undergoing an unstoppable retreat that has huge implications for global sea-level rise," explains Holland, a professor at NYU\'s Courant Institute of Mathematical Sciences.']]
	holland
[['david holland']]
"""

"""
1511300080 [['"I think China is doing a great job," said Madad, a professor and expert in public health and special pathogen preparedness and response.']]
	madad
[['syra madad']]
"""

## Another example that multiple names get merged in one sentence
"""
1508562446 [['In addition, says Richard Sugrue, an associate professor in the school of biological sciences at Nanyang Technological University in Singapore, “at the moment it seems like the fever is being used as a major indicator of infection, but then again, this is in the middle of a flu season, so you have to confirm if the person with the fever has the coronavirus, or do they have something else?” Sugrue says the only real way to confirm an 2019-nCoV infection is diagnostic testing like polymerase chain reaction (PCR) tests or electron microscopy, which may take several hours to complete and would be infeasible in a scenario like an international airport, where tens of thousands of people pass through every day.'], ['“Infected people who are asymptomatic or minimally symptomatic would likely not seek medical care or stay home from work or school, which could facilitate spread of the virus and make it much harder to contain,” says Charles Chiu, a professor of laboratory medicine at the University of California, San Francisco.'], ['Dr. Anthony Fauci, director of the National Institute of Allergy and Infectious Diseases at the U.S. National Institutes of Health said on Sunday that agency officials had not yet seen details on how Chinese authorities had collected data, according to CNN.']]
	richard sugrue
	sugrue
	charles chiu
	anthony fauci
[['richard sugrue'], ['charles chiu'], ['anthony fauci']]9
"""

# Another example that an enitity that was shortened in another sentence get merged together
"""
1506350209 [['It says it is consulting with physicians who are treating patients.'], ['But it degrades quickly, said Vincent Munster, a virologist with the National Institute of Allergy and Infectious Diseases who led the research.'], ['These droplets are small enough to remain suspended in the air for half an hour to an hour, depending on air flow, Dr. Munster said.']]
	vincent munster
	munster
[[], ['vincent munster'], ['vincent munster']]
"""
## Check this news we only have last name
"""
1510881493 [['and federal government have and will continue to take aggressive action to protect the public,” Dr. Messonnier said.'], ['Dr. Messonnier said that the people who were quarantined did not pose a threat to the surrounding community.']]
	messonnier
	messonnier
[['messonnier'], ['messonnier']]
"""


# %%
## Based on the examples so far I have decided to use Stanford NER to get the persons
mediacloud_story_id_to_names = {}

for story_id,sentence_lists in df.to_dict()["Expert_Mention_Sentence_List"].items():
    print(story_id, sentence_lists)
    persons_in_all_sents = []
    for sentence in eval(sentence_lists):
        persons_in_current_sent = []
        ## makign use of tow different models
        ## We trust stanford NER more, but if stanford returns empty
        ## we will try with spacy
        ## The example where stanford do not work but spacy works is:
        ## Virologist and professor of microbiology and immunology at Columbia University Vincent Racaniello, PhD, spoke about the virus on Monday and said it differs from SARS in that it's spreading outside of the medical community
        persons_detected = get_persons(sentence[0],model="stanford")
        if len(persons_detected) < 1:
            persons_detected = get_persons(sentence[0],model="spacy")
        for person_name in persons_detected:
            person_name = remove_special_characters(person_name.strip().lower()).strip()
            print("\t"+person_name)
            if len(person_name.split()) < 2:
                person_name = get_target_full_name_using_single_name_from_article(person_name,story_id,model="stanford")
                ## For the single name replace lets trust stanford
            persons_in_current_sent.append(person_name)
        persons_in_all_sents.append(list(set(persons_in_current_sent)))
    print(persons_in_all_sents)
    mediacloud_story_id_to_names[story_id] = persons_in_all_sents
    
    
# %%
## TO CHECK LATER
"""
1508637093 [["In a media call on Wednesday, Dr Nancy Messonnier of the Centers for Disease Control and Prevention (CDC) said the passengers have been 'screened, monitored and evaluated' for signs of coronavirus since landing."], ["Encouragingly, Dr Anthony Fauci of the National Institutes of Health said the agency is studying a 'candidate vaccine,' modeled after an experimental one developed amid the 2003 outbreak of SARS, a coronavirus cousin of the current infection."], ['Pictured: Paramilitary officers wearing face masks at Tiananmen Gate in Beijing on Monday HHS Secretary Alex Azar said the US has offered to send medical experts to China three times, but the government has declined.'], ["'Part of the delay is the sample getting to CDC, and entirely one of the reasons we are focusing on the possibility of getting those tests out closer to the patients so the results can become available more quickly,' Dr Messonnier, said in a call to reporters last week."], ['On Tuesday, Dr Messonier said the CDC hope to have the tests more locally available in a week or two.'], ["'We're really working to understand the full spectrum of the illness with this coronavirus,' Dr Messonnier said at a briefing."], ["'This patient did travel to the area of concern in China within the last 14 days and thankfully had mild upper respiratory symptoms, and he was improving,' said Dr Eric Wilke with the Brazos County Health Department."], ["'I believe the time the patient presented at the emergency department, it was more out of concern,' said Dr Eric Wilke with the Brazos County Health Department."]]
	nancy messonnier
	anthony fauci
	alex azar
	messonnier
	messonier
	messonnier
	eric wilke
	eric wilke
[['nancy messonnier'], ['anthony fauci'], ['alex azar'], ['nancy messonnier'], ['nancy messonnier'], ['nancy messonnier'], ['eric wilke'], ['eric wilke']]
"""
"""
1505962154 [['“We don’t know the source of this virus, we don’t understand how easily it spreads & we don’t fully understand its clinical features or severity,” Tedros said, noting that the organization was working to “fill the gaps in our knowledge as quickly as possible.” Investigations to identify an animal source of the disease are underway in China and Wuhan, said Dr. Maria Van Kerkhove, head of emerging diseases and zoonosis at WHO, said Tuesday’s press conference.'], ['“This was a very astute gentleman,” said Scott Lindquist, Washington state’s epidemiologist, who noted that the man had researched and shared information about the virus with his provider.'], ['The CDC said the agency had already been preparing for the introduction of the virus into the U.S. “for weeks” and had told clinicians to be vigilant about patients reporting “respiratory symptoms and a history of travel to Wuhan” as early as Jan. 8.'], ['“I think the public health authorities in China realized that that really was not the way to handle things, that things come out eventually, that response is best when it is handled promptly,” Monto, the University of Michigan public health professor, says.'], ['Still, professor Gabriel Leung, the dean of the University of Hong Kong’s Faculty of Medicine, said at a press conference Tuesday: “[There is] a very strong sense of deja vu [with SARS], except the time scale has been compressed.” He added: “Whereas you saw an unrecognized epidemic brewing for months since the end of 2002 up until the peak of it in March and April in Hong Kong, here you are talking about the same number, but the unit is weeks.” Statistics modelling led by Leung suggests that there could be over 1,300 cases in Wuhan, in line with research by the London-based team that states the number of patients infected with the virus is significantly more than is being reported.'], ['Leo Poon, a virologist and SARS expert at the University of Hong Kong, says it is best to avoid densely populated areas and maintain good personal hygiene, especially frequent hand washing.']]
	maria van kerkhove
	scott lindquist
	gabriel leung
	leung
	leo poon
[['maria van kerkhove'], ['scott lindquist'], [], [], ['leung', 'gabriel leung'], ['leo poon']]
"""
## My general question how this news was slected to be one with experts?
"""

1507273407 [["Scaling The Peaks (Biotech Stocks Hitting 52-week highs on Jan. 27) 10X Genomics Inc (NASDAQ: TXG) (NASDAQ: TXG) Achillion Pharmaceuticals, Inc. (NASDAQ: ACHN)(announced early termination of waiting period for its proposed acquisition by Alexion Pharmaceuticals, Inc. (NASDAQ: ALXN)) (NASDAQ: ACHN)(announced early termination of waiting period for its proposed acquisition by (NASDAQ: ALXN)) Cidara Therapeutics Inc (NASDAQ: CDTX) (NASDAQ: CDTX) Cleveland BioLabs, Inc. (NASDAQ: CBLI)(saw a coronavirus-induced rally ) (NASDAQ: CBLI)(saw a coronavirus-induced rally ) Denali Therapeutics Inc (NASDAQ: DNLI) (NASDAQ: DNLI) Dr.Reddy's Laboratories Ltd (NYSE: RDY)(reacted to its Q3 results) (NYSE: RDY)(reacted to its Q3 results) Inovio Pharmaceuticals Inc (NASDAQ: INO)(announced (NASDAQ: INO)(announced Nevro Corp (NYSE: NVRO) (NYSE: NVRO) Oyster Point Pharma Inc (NASDAQ: OYST) (NASDAQ: OYST) Quest Diagnostics Inc (NYSE: DGX) (NYSE: DGX) Rapt Therapeutics Inc (NASDAQ: RAPT) (NASDAQ: RAPT) SI-Bone Inc (NASDAQ: SIBN) (NASDAQ: SIBN) Vaccinex Inc (NASDAQ: VCNX) (NASDAQ: VCNX) Vir Biotechnology Inc (NASDAQ: VIR) Down In The Dumps (Biotech Stocks Hitting 52-week lows on Jan. 27) Alkermes Plc (NASDAQ: ALKS) (NASDAQ: ALKS) Allogene Therapeutics Inc (NASDAQ: ALLO) (NASDAQ: ALLO) Autolus Therapeutics Ltd – ADR (NASDAQ: AUTL) (NASDAQ: AUTL) Axovant Gene Therapies Ltd (NASDAQ: AXGT) (NASDAQ: AXGT) Avanos Medical Inc (NYSE: AVNS) (NYSE: AVNS) Blueprint Medicines Corp (NASDAQ: BPMC) (NASDAQ: BPMC) Correvio Pharma Corp (NASDAQ: CORV) (NASDAQ: CORV) Enanta Pharmaceuticals Inc (NASDAQ: ENTA) (NASDAQ: ENTA) Heat Biologics Inc (NASDAQ: HTBX) (NASDAQ: HTBX) HTG Molecular Diagnostics Inc (NASDAQ: HTGM) (NASDAQ: HTGM) Kura Oncology Inc (NASDAQ: KURA) (NASDAQ: KURA) Madrigal Pharmaceuticals Inc (NASDAQ: MDGL) (NASDAQ: MDGL) MediciNova, Inc. (NASDAQ: MNOV) (NASDAQ: MNOV) Nemaura Medical Inc (NASDAQ: NMRD) (NASDAQ: NMRD) Neuronetics Inc (NASDAQ: STIM) (NASDAQ: STIM) Portola Pharmaceuticals Inc (NASDAQ: PTLA) (NASDAQ: PTLA) Rhythm Pharmaceuticals Inc (NASDAQ: RYTM) (NASDAQ: RYTM) Sellas Life Sciences Group Inc (NASDAQ: SLS) (NASDAQ: SLS) Stealth BioTherapeutics Corp (NASDAQ: MITO) (NASDAQ: MITO) Spectrum Pharmaceuticals, Inc. (NASDAQ: SPPI) (NASDAQ: SPPI) Therapix Biosciences Ltd – ADR (NASDAQ: TRPX) (NASDAQ: TRPX) X4 Pharmaceuticals Inc (NASDAQ: XFOR) (NASDAQ: XFOR) VIVUS, Inc. (NASDAQ: VVUS) See Also: The Week Ahead In Biotech: Amgen, Eli Lilly, Pfizer In Earnings Mix, IPO Flow Resumes Stocks In Focus Acceleron's Pulmonary Arterial Hypertension Drug Aces Mid-Stage Study Acceleron Pharma Inc (NASDAQ: XLRN) said a Phase 2 study dubbed PULSAR that evaluated its sotatercept in patients with pulmonary arterial hypertension met its primary and key secondary endpoints."]]
	vcnx
"""

# also this one, how are the expert sentences select
"""
1509283295 [['Google says it puts even more emphasis on authoritative sources when it comes to sensitive topics such as health information.']]
"""

## None of the model detected a person from here:
"""
"'We want to get the message out there that even people with low-level symptoms should come forward,' Dr Chant said."
"""
# and this one too
"""
1509619169 [['Tedros Adhanom Ghebreyesus, director-general of the World Health Organization, said he will reconvene on Thursday with global infectious disease experts to determine whether the outbreak constitutes a public health emergency of international concern.']]
"""