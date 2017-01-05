## FAA Chart Downloader
## Author: Mat Frank

import Tkinter, tkFileDialog
import sys,zipfile,traceback,urllib2,os
from os.path import isdir,join,normpath,split

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

root = Tkinter.Tk()
dirName = tkFileDialog.askdirectory(parent=root,initialdir="/",title="Select a directory")

if len(dirName) > 0:
    print 'Downloading Terminal Charts'
    terminalFolder = "Terminal_Charts"
    newTermFolder = os.path.join(dirName,terminalFolder)
    if not os.path.exists(newTermFolder):
        os.makedirs(newTermFolder)
    os.chdir(newTermFolder)

    url = "http://aeronav.faa.gov/content/aeronav/tac_files/"

    terminalIndex = [
    "Anchorage-Fairbanks_TAC_77",
    "Atlanta_TAC_94",
    "Baltimore-Washington_TAC_93",
    "Boston_TAC_88",
    "Charlotte_TAC_55",
    "Chicago_TAC_92",
    "Cincinnati_TAC_35",
    "Cleveland_TAC_86",
    "Dallas-Ft_Worth_TAC_88",
    "Denver_TAC_86",
    "Detroit_TAC_86",
    "Houston_TAC_86",
    "Kansas_City_TAC_83",
    "Las_Vegas_TAC_85",
    "Los_Angeles_TAC_73",
    "Memphis_TAC_55",
    "Miami_TAC_88",
    "Minneapolis-St_Paul_TAC_86",
    "New_Orleans_TAC_83",
    "New_York_TAC_91",
    "Philadelphia_TAC_84",
    "Phoenix_TAC_54",
    "Pittsburgh_TAC_86",
    "Puerto_Rico-VI_TAC_42",
    "St_Louis_TAC_86",
    "Salt_Lake_City_TAC_54",
    "San_Diego_TAC_72",
    "San_Francisco_TAC_89",
    "Seattle_TAC_86",
    "Tampa_TAC_53"
        ]

    # Download charts
    for chart in terminalIndex:
        zipFile = chart + ".zip"
        download = os.path.join(url,zipFile)
        f = urllib2.urlopen(download)
        with open(zipFile,"wb") as code:
            code.write(f.read())
        print '%s downloaded' % (zipFile)

    # Unzip charts
    for terminalChart in terminalIndex:
        joinedPaths = os.path.join(newTermFolder,terminalChart)
        inFile = joinedPaths + ".zip"
        if not os.path.exists(joinedPaths):
            os.makedirs(joinedPaths)
        zip = zipfile.ZipFile(inFile,'r')
        unzip(joinedPaths,zip)
        zip.close()
        print 'Completed %s' % (terminalChart)

    print 'Downloading Sectional Charts'
    sectionalFolder = "Sectional_Charts"
    newSectionalFolder = os.path.join(dirName,sectionalFolder)
    if not os.path.exists(newSectionalFolder):
        os.makedirs(newSectionalFolder)
    os.chdir(newSectionalFolder)

    url = "http://aeronav.faa.gov/content/aeronav/sectional_files/"

    sectionalIndex = [
        "Albuquerque_98",
        "Anchorage_98",
        "Atlanta_97",
        "Bethel_58",
        "Billings_92",
        "Brownsville_97",
        "Cape_Lisburne_50",
        "Charlotte_100",
        "Cheyenne_94",
        "Chicago_93",
        "Cincinnati_96",
        "Cold_Bay_49",
        "Dallas-Ft_Worth_97",
        "Dawson_49",
        "Denver_95",
        "Detroit_93",
        "Dutch_Harbor_49",
        "El_Paso_97",
        "Fairbanks_98",
        "Great_Falls_91",
        "Green_Bay_92",
        "Halifax_95",
        "Hawaiian_Islands_95",
        "Houston_98",
        "Jacksonville_98",
        "Juneau_56",
        "Kansas_City_96",
        "Klamath_Falls_95",
        "Kodiak_56",
        "Lake_Huron_92",
        "Las_Vegas_96",
        "Los_Angeles_99",
        "McGrath_58",
        "Memphis_97",
        "Miami_99",
        "Montreal_95",
        "New_Orleans_98",
        "New_York_93",
        "Nome_57",
        "Omaha_94",
        "Phoenix_96",
        "Point_Barrow_78",
        "Salt_Lake_City_96",
        "San_Antonio_97",
        "San_Francisco_97",
        "Seattle_91",
        "Seward_98",
        "St_Louis_94",
        "Twin_Cities_92",
        "Washington_100",
        "Western_Aleutian_Islands_49",
        "Whitehorse_56",
        "Wichita_97"
        ]

    for chart in sectionalIndex:
        zipFile = chart + ".zip"
        download = os.path.join(url,zipFile)
        f = urllib2.urlopen(download)
        with open(zipFile,"wb") as code:
            code.write(f.read())
        print '%s downloaded' % (zipFile)

    # Unzip charts
    for sectionalChart in sectionalIndex:
        joinedPaths = os.path.join(newSectionalFolder,sectionalChart)
        inFile = joinedPaths + ".zip"
        if not os.path.exists(joinedPaths):
            os.makedirs(joinedPaths)
        zip = zipfile.ZipFile(inFile,'r')
        unzip(joinedPaths,zip)
        zip.close()
        print 'Completed %s' % (sectionalChart)
        
