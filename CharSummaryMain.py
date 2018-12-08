from urllib.request import *
import re
import spacy
from collections import Counter
ender = True
summarybox = []
persons = []
nlp = spacy.load('en_core_web_sm')

#splits the text into two = summary and actual text
def split_text(fulltext):
    #All wikipedia texts start with bolded name of some sorts which is marked by ''' text and the summara pages end in }}
    splittext = re.split (r"}}\s*\w* *'''",fulltext, re.I)
    return splittext

def cut_out_extra(text_text):
    goodtext = re.split(r"=+.*References.*=+",text_text, re.I)
    return goodtext[0]

#replaces whitespaces with a plus
def addplus(query):
    fixed = query.replace(" ", "+")
    return fixed


def query(text):
    query = text
    ##need to fix query to work with proper terms as in "Bill Gates" not Bill,Gates
    connection = urlopen('http://localhost:8985/solr/wiki/select?q=text:(' + addplus(query) +')&wt=python&start=0&rows=1')
    response = eval(connection.read())


    for i, document in enumerate(response['response']['docs']):
        fulltext = document['text']
        title = document["title"]
    
    return fulltext,title
    
#returns the summary page
def summary(fulltext):
    summary = split_text(fulltext)
    return summary[0]
#returns the actual text part
def text_text(fulltext):
    text_text = split_text(fulltext)
    return cut_out_extra(text_text[1]) #missin cutout extra currently

def name_counter(fulltext): #Finds all the names in the text and counts them, returns a dictionary with name and number of mentions in the text
        
        doc = nlp(fulltext)  

        for ent in doc.ents:
            if (ent.label_ == ("PERSON")):
                persons.append(ent.text)
        
        counteddict = (Counter(persons))
        return counteddict

def get_important_person(personsdict): #Gets the name of the most mentioned person and returns the name
    
    sorted_by_value = sorted(personsdict.items(), key=lambda kv: kv[1])
    sorted_by_value.reverse()
    person = sorted_by_value[0]
    return person[0]

#Goes through the summary info and parses out wanted information
def sort_info(fullsummary):
    
    try:
        description = re.findall(r"{{short description.*}}", fullsummary, flags = re.I)
        is_none(description[0])
    except:
        is_none("Could not find a description")
    try:
        birthdate = re.search(r"{{birth date.*}}", fullsummary,flags =re.I)
        is_none(birthdate[0])
    except:
        is_none("Could not find a birthdate")
        
    try:
        died = re.search(r"death_date.+",fullsummary,flags =re.I)
        if (died[0] == "death_date = "):
            died[0] = "Still alive"
        is_none(died[0])
    except:
        is_none("death date = Still alive")
        
    try:
        spouse = re.search(r"{{marriage.*}}", fullsummary,flags =re.I)
        is_none(spouse[0])
        
    except:
        is_none("Could not find a spouse")
    try:
        children = re.search(r".*(children|issue).*",fullsummary,re.I)
        is_none(children[0])
    except:
        is_none("Could not find the Children")
        
    
    return summarybox

def fix_info(stringtofix): #Strips away excess characters for ease of reading
    stringtofix =re.sub(r"{","",stringtofix)
    stringtofix =re.sub(r"}","",stringtofix)
    stringtofix =re.sub(r"(^\| )","",stringtofix)
    stringtofix =re.sub(r"\|"," ",stringtofix)
    stringtofix =re.sub(r"\[","",stringtofix)
    stringtofix =re.sub(r"\]","",stringtofix)
    stringtofix =re.sub(r"<br>"," ",stringtofix)
    stringtofix =re.sub(r" +"," ",stringtofix)
    stringtofix =re.sub(r"^ +","",stringtofix)
    return stringtofix

def is_none(teststring):
    
        if (type(teststring) != None):
            summarybox.append(fix_info(teststring))
        else:
            return False
   
def main():
    try:
        while(True):
            
            text = input("Give query: ")
            
            
            
            
            
            try:
                search1, title1 = query(text)
                summa = summary(search1) #the summarybox part
                actualtext = text_text(search1) #the formated text part
                
            #second search is excecuted according to the name found in the text of the first search
                #name = name_counter(actualtext)
                #imp_person = get_important_person(name)
                #search2, title2 = query(imp_person)
                
                search2, title2 = query(get_important_person(name_counter(actualtext)))
                print("Title: "+title2)
                for i in sort_info(summary(search2)):
                    print(i)
            
                if(text == ""):
                    break
            except IndexError:
                print("Couldn't find anything useful")
                continue

            del summarybox[:] #important, empties the info box for another search
            del persons[:]
    
    except:
        print("Stopping now")
if __name__ == "__main__":
    main()

