## FAA Chat update check
## Author: Mat Frank

# Need to fix Western Aleutian Islands and editions that are 3 digits

import Tkinter, tkFileDialog
import re, urllib2, os, sys, zipfile, traceback
from os.path import isdir,join,normpath,split
from urllib2 import urlopen

root = Tkinter.Tk()
dirName = tkFileDialog.askdirectory(parent=root,initialdir="/",title="Select overall folder containing all charts")

if len(dirName) > 0:
    sectionalCharts = [
        "Albuquerque",
        "Anchorage",
        "Atlanta",
        "Bethel",
        "Billings",
        "Brownsville",
        "Cape%20Lisburne",
        "Charlotte",
        "Cheyenne",
        "Chicago",
        "Cincinnati",
        "Cold%20Bay",
        "Dallas-Ft%20Worth",
        "Dawson",
        "Denver",
        "Detroit",
        "Dutch%20Harbor",
        "El%20Paso",
        "Fairbanks",
        "Great%20Falls",
        "Green%20Bay",
        "Halifax",
        "Hawaiian%20Islands",
        "Houston",
        "Jacksonville",
        "Juneau",
        "Kansas%20City",
        "Ketchikan",
        "Klamath%20Falls",
        "Kodiak",
        "Lake%20Huron",
        "Las%20Vegas",
        "Los%20Angeles",
        "McGrath",
        "Memphis",
        "Miami",
        "Montreal",
        "New%20Orleans",
        "New%20York",
        "Nome",
        "Omaha",
        "Phoenix",
        "Point%20Barrow",
        "Salt%20Lake%20City",
        "San%20Antonio",
        "San%20Francisco",
        "Seattle",
        "Seward",
        "St%20Louis",
        "Twin%20Cities",
        "Washington",
        "Western%20Aleutian%20Islands",
        "Whitehorse",
        "Wichita"
        ]

    def unzip (path,zip):
        if not isdir(path):
            os.makedirs(path)
        for each in zip.namelist():
            print ("Extracting " + os.path.basename(each) + "...")
            if not each.endswith('/'):
                root,name = split(each)
                directory = normpath(join(path,root))
                if not isdir(directory):
                    os.makedirs(directory)
                file(join(directory,name),'wb').write(zip.read(each))


    ## Create empty dictionary for current web editions
    webEditions = {}

    print "Retrieving current chart edition numbers...\nChart Name : Edition Number"
    ## Get current editions off website
    for chart in sectionalCharts:
        urlBegin = "https://soa.smext.faa.gov/apra/vfr/sectional/info?geoname="
        urlEnd = "&edition=current"
        url = urlBegin + chart + urlEnd
        urlResponse = urlopen(url).read()
        checkEdition = re.search('<editionNumber>(.+?)</editionNumber>',urlResponse)
        checkName = re.search('<edition geoname="(.+?)" editionName',urlResponse)

        if checkEdition:
            editionNumber = checkEdition.group(1)
            editionName = checkName.group(1)
            print editionName + ": " + editionNumber
            webEditions[editionName] = editionNumber

    chartType = "Sectional_Charts"
    sectionalFolder = os.path.join(dirName,chartType)
    if not os.path.exists(sectionalFolder):
        os.makedirs(sectionalFolder)
    regex = re.compile(r'\d+')
    tempEditions = []
    for root, dirs, files in os.walk(sectionalFolder):
        fullPath = os.path.basename(root)
        tempEditions.append(fullPath)

    currentEditions = {}
    for key in tempEditions:
        row = key.replace("_"," ")
        edition = str(regex.findall(row))
        edition1 = edition.replace("[","")
        edition2 = edition1.replace("]","")
        edition3 = edition2.replace("'","")
        line = re.sub(r'\d+','',row)
        line2 = str(line[:-1])
        currentEditions[line2] = edition3

    updateArray = []
    for key in webEditions:
        if key in currentEditions:
            if webEditions[key] == currentEditions[key]:
                print key + ": Up to date"
            else:
                print key + ": Needs update"
                updateArray.append(key)

    os.chdir(sectionalFolder)
    urlChartBegin = "http://aeronav.faa.gov/content/aeronav/sectional_files/"
    urlCheckBegin = "https://soa.smext.faa.gov/apra/vfr/sectional/info?geoname="
    urlCheckEnd = "&edition=current"
    
    if len(updateArray) > 0:
        for row in updateArray:
            print "Updating " + row + "..."
            rowSpace = row.replace(" ","%20")
            url = urlCheckBegin + rowSpace + urlCheckEnd
            urlResponse = urlopen(url).read()
            checkEdition = re.search('<editionNumber>(.+?)</editionNumber>',urlResponse)
            checkName = re.search('<edition geoname="(.+?)" editionName',urlResponse)

            if checkEdition:
                editionNumber = checkEdition.group(1)
                editionName = checkName.group(1)
                extention = ".zip"
                zipFolder = editionName + "_" + editionNumber
                zipFile1 = editionName + "_" + editionNumber + extention
                zipFile = zipFile1.replace(" ","_")
                download = os.path.join(urlChartBegin,zipFile)
                f = urlopen(download)
                with open(zipFile,"wb")as code:
                    code.write(f.read())
                print '%s downloaded' % (zipFile)
                print 'Extracting %s' % (zipFile)
                if not os.path.exists(zipFolder):
                    os.makedirs(zipFolder)
                zip = zipfile.ZipFile(zipFile,'r')
                unzip(zipFolder,zip)
                zip.close()
                print 'Completed %s' % (zipFile1)
    else:
        print "All files are up to date"
    raw_input()
