from urllib.request import *
import re
ender = True

#splits the text into two = summary and actual text
def split_text(fulltext):
    #All wikipedia texts start with bolded name of some sorts which is marked by ''' text and the summara pages end in }}
    splittext = re.split (r"}}\s*\w*'''",fulltext)
    return splittext


def query():
    query = input("Give query ")
    ##need to fix query to work with proper terms as in "Bill Gates" not Bill,Gates
    connection = urlopen('http://localhost:8985/solr/wiki/select?q=text:' + query + '&wt=python&start=0&rows=1')
    response = eval(connection.read())

    for i, document in enumerate(response['response']['docs']):
        text = document['text']
    return text

#returns the summary page
def summary(fulltext):
    summary = split_text(fulltext)
    return summary[0]
#returns the actual text part
def text_text(fulltext):
    text_text = split_text(fulltext)
    return text_text[1]

def main():
    ##Crashes as a end since the connection is open try to figure out how to close properly
    ##Might not be necessary in flask/html version
    while(ender):
        text = query()
        summa = summary(text)

        #the summary is in 0 location
        print(summa)
        
    


    

if __name__ == "__main__":
    main()

    
    
    


