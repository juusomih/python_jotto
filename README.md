# Character Summary Tool


The main program searches through any given English Wikipedia article and returns a 
short summary of the person with most mentions. Alternatively, the user can directly search for
a person included in English Wikipedia, which would return a summary of the person in question.
This is a handy tool for anyone who is looking for basic information about a key person in a
given English Wikipedia article.

# How to run the program:

 To run the program, you can start by installing, configuring and running Solr. 
 Download a suitable English Wikipedia dump, and make sure to index it. Solr is expected to be
 running in port 5004. The program imports spaCy, which also needs to be installed.

 The search functionalities can be accessed through a web application running on Flask. 
 To install and configure Flask, you can follow the instructions provided by Mikko Aulamo 
 (https://github.com/miau1/flask-example). Make sure to run Flask in the correct port and access
 the program via localhost:5004/.

# Input & output:

The expected input is any search term that can be matched to an English Wikipedia article.
The output includes a name and some key information about a person, such as 
date of birth, date of death, name of spouse, and known children. If a date of death, 
for example, is not available, the output will state that such information could not be found.



THE PLAN :

The most important character summary tool




 

M simple main function with solr query functionality 

    Search field 

    Until break 

 

L search function ---> searches text 

    Take query and search through top result text 

    XL spacy function --> highlights character names 

        S take highlighted character function 

          S count char mentions function 

            S if even randomly select name 

    L search through chosen char’s wiki page get info function  

      XXL take most important info function  

        Born 

        Died 

        Spouse 

      S create summary of important info function 

      S post summary function 
