import re

#CW
def cw_processing(text):
   wording = text
   a = {'Replace "relevant time" with time of specification - Level 2':['John', 'consultant', 'consultant'],
    'Delete "having been supplied or placed on the market in breach of the Construction Products Regulations" - Level 4': ['having been supplied or placed on the market in breach of the Construction Products Regulations'], 
    'Delete "all" before "the reasonable skill" - Level 3':['all the reasonable skill'],
    'Insert the actual "Consultant\'s profession"':['Consultant\'s profession'],
    'Delete "successors" - Level 4':['successors'],
    'Replace "warrants" with "undertakes" - Level 1':['warrants']
    }
   for key,value in a.items():
       for item in value:
           if item in wording:
               yield (key)
               break
   b = {'gigli':['bubu'], 'buba':['warrants'], 'hoojo':['yoooha']}
   for key,value in b.items():
       for item in value:
           if item not in wording:
               yield (key)
               break           
#APP
def appoint_processing(text):
   wording = text
   a = {'adios muchachos':['John', 'consultant', 'consultant']}
   for key,value in a.items():
       for item in value:
           if item in wording:
               yield (key)
               break
   b = {'gigli':['bubu'], 'buba':['warrants'], 'hoojo':['yoooha']}
   for key,value in b.items():
       for item in value:
           if item not in wording:
               yield (key)
               break 

def regular(text):
    wording = text
    pattern = re.compile(r'[1-5]')#values beetween 1-5 
    matches = pattern.finditer(wording)#extra functionality of a match object
    for match in matches:
        yield(match)
    