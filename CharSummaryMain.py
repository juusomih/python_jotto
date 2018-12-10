from urllib3 import *
from flask import Flask, render_template, request, redirect, url_for
from urllib.request import urlopen
import re
import spacy
from collections import Counter
app = Flask(__name__)

ender = True
summarybox = []
persons = []
nlp = spacy.load('en_core_web_sm')
app = Flask(__name__)


def split_text(fulltext):  # splits the text into two = summary and actual text
    # All wikipedia texts start with bolded name of some sorts which is marked by ''' text and the summary pages end in }}
    splittext = re.split(r"}}\s*\w* *'''", fulltext, re.I)
    return splittext


def cut_out_extra(text_text):
    goodtext = re.split(r"=+.*References.*=+", text_text, re.I)
    return goodtext[0]


def addplus(search):  # replaces whitespaces with a plus
    fixed = search.replace(" ", "+")
    return fixed


def search(text):

    connection = urlopen('http://localhost:8985/solr/wiki/select?q=text:('
                         + addplus(text) + ')&wt=python&start=0&rows=1')
    response = eval(connection.read())

    for i, document in enumerate(response['response']['docs']):
        fulltext = document['text']
        title = document["title"]

    return fulltext, title


def summary(fulltext):  # returns the summary page
    summary = split_text(fulltext)
    return summary[0]


def text_text(fulltext):  # returns the actual text part
    text_text = split_text(fulltext)
    return cut_out_extra(text_text[1])  # missin cutout extra currently


def name_counter(fulltext):  # Finds all the names in the text and counts them, returns a dictionary with name and number of mentions in the text

    doc = nlp(fulltext)

    for ent in doc.ents:
        if (ent.label_ == ("PERSON")):
            persons.append(ent.text)

    counteddict = (Counter(persons))
    return counteddict


# Gets the name of the most mentioned person and returns the name
def get_important_person(personsdict):

    sorted_by_value = sorted(personsdict.items(), key=lambda kv: kv[1])
    sorted_by_value.reverse()
    person = sorted_by_value[0]
    return person[0]


def sort_info(fullsummary):  # Goes through the summary info and parses out wanted information

    try:
        description = re.findall(
            r"{{short description.*}}", fullsummary, flags=re.I)
        is_none(description[0])
    except:
        summarybox.append("Could not find a description")
    try:
        birthdate = re.search(r"{{birth date.*}}", fullsummary, flags=re.I)
        is_none(birthdate[0])
    except:
        summarybox.append("Could not find a birthdate")

    try:
        died = re.search(r"death_date.+", fullsummary, flags=re.I)
        if (died[0] == "death_date = "):
            died[0] = "Still alive"
        is_none(died[0])
    except:
        summarybox.append("death date = Still alive")

    try:
        spouse = re.search(r"{{marriage.*}}", fullsummary, flags=re.I)
        is_none(spouse[0])

    except:
        summarybox.append("Could not find a spouse")
    try:
        children = re.search(r".*(children|issue).*", fullsummary, re.I)
        is_none(children[0])
    except:
        summarybox.append("Could not find the Children")

    return summarybox


def fix_info(stringtofix):  # Strips away excess characters for ease of reading
    stringtofix = re.sub(r"{", "", stringtofix)
    stringtofix = re.sub(r"}", "", stringtofix)
    stringtofix = re.sub(r"(^\| )", "", stringtofix)
    stringtofix = re.sub(r"\|", " ", stringtofix)
    stringtofix = re.sub(r"\[", "", stringtofix)
    stringtofix = re.sub(r"\]", "", stringtofix)
    stringtofix = re.sub(r"<br>", " ", stringtofix)
    stringtofix = re.sub(r"</br>", " ", stringtofix)
    stringtofix = re.sub(r"<br/>", " ", stringtofix)
    stringtofix = re.sub(r" +", " ", stringtofix)
    stringtofix = re.sub(r"^ +", "", stringtofix)
    return stringtofix


def is_none(teststring):

    if (type(teststring) != None):
        summarybox.append(fix_info(teststring))
    else:
        return False


def charsum(text):
    del summarybox[:]  # important, empties the info box for another search
    del persons[:]
    # try:
    search1, title1 = search(text)
    summa = summary(search1)  # the summarybox part
    actualtext = text_text(search1)  # the formated text part

    # name = name_counter(actualtext)
    # imp_person = get_important_person(name)
    # search2, title2 = search(imp_person)
    # summa = summary(search2)
    # finalsummary = sort_info(summa)

    # second search is excecuted according to the name found in the text of the first search
    # gives a summary of important stuff in a table format and the title of the wikipedia article the info was taken from
    search2, title2 = (
        search(get_important_person(name_counter(actualtext))))
    finalsummary = sort_info(summary(search2))
    finalsummary.insert(0, title2)

    return finalsummary

    # except IndexError:
    # return "Couldn't find anything useful"

    # {"name": "Title:"},
    # {"name": "Description:"},
    # {"name": "Birth Date:"},
    # {"name": "Date of Death:"},
    # {"name": "Date of Death:"},
    # {"name": "Spouse:"},
    # {"name": "Children:"}


@app.route("/solr", defaults={"query": ""}, methods=["GET", "POST"])
@app.route("/solr/<query>", methods=["GET", "POST"])
def solr(query):
    if (request.method == "POST"):
        query = request.form["query"]

        return redirect(url_for("solr", query=query))

    matches = []
    if (query != ""):
        for info in charsum(query):
            matches.append({"name": info})
    return render_template("solr.html", matches=matches)


if __name__ == "__main__":
    app.run()
