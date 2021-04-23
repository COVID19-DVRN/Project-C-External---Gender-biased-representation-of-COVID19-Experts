import unicodedata
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