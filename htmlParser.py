###########################################
## Scrapes embassies and their addresses ##
## Version: 1.0                          ##
###########################################

from bs4 import BeautifulSoup as BS
import requests
import csv
import os

countryList = []
url = 'https://embassy.goabroad.com/embassies-in/'

def getCountries():
    response = requests.get(url)
    soup = BS(response.content,'html.parser')
    for li in soup.find_all('div',class_='two-cols'):
        count = li.find('ul')
        for c in count:
            a = c.find('a')
            a1 = str(a).replace("\n",'').replace("\t",'').replace('<a href="/embassies-in/','').replace('</a>','').replace('-1','').replace('">',',')
            countryList.append(a1)
    countryList2 = filter(lambda x:x != '',countryList)
    for line in countryList2:
        if line == '':
            continue
        f = line.split(',')
        print "converting: " + f[0]
        pullHtml(f[0])
        

def pullHtml(country):
    url = 'https://embassy.goabroad.com/embassies-in/'
    filePath =  os.getcwd()
    url2 = url + country

    csvFile = os.path.join(filePath,country+".csv")

    remSp = "</span>"
    remNa = "<span class="+chr(34)+"embassy-name"+chr(34)+">"
    remAd = "<span class="+chr(34)+"embassy-address"+chr(34)+">"
    remT = "\t"
    remN = "\n"

    embassies = {}
    print "Opening " + url2
    response = requests.get(url2)

    soup = BS(response.content,'html.parser')

    for emb in soup.find_all('div',class_='content'):
        place = emb.find('span',class_='embassy-name')
        place1 = str(place).replace(remNa,'').replace('</span>','').replace(remT,'').replace(remN,'')
        
        addy = emb.find('span',class_='embassy-address')
        addy1 = str(addy).replace(remAd,'').replace('</span>','').replace(remT,'').replace(remN,'')

        embassies[str(place1)] = str(addy1)

    print "Writing output to .csv file"
    with open(csvFile,'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["name","address"])
        for key, value in embassies.items():
            writer.writerow([key, value])
    print "Done"
    print str(len(embassies)) + " embassies found for " + country



###### Run it #####
getCountries()
