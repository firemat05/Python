import arcpy
import urllib
import json
import time
import os

outputFolder = r'D:\Documents\GIS_Data\Tools\clip_to_workspace' # where to save zipfiles
inputFC = r'D:\Documents\GIS_Data\Tools\clip_to_workspace\testData\aoi.shp' # polygon featureclass to get extent

aoi = []

def getExtent(fc):
    with arcpy.da.SearchCursor(fc,['SHAPE@']) as cursor:
        for row in cursor:
            shpArray = row[0].getPart()
            for vertice in range(row[0].pointCount):
                pnt = shpArray.getObject(0).getObject(vertice)
                aoi.append([pnt.X,pnt.Y])

def getENCData(url,outputZipfile):
    submitResponse = urllib.urlopen(url)
    submitJson = json.loads(submitResponse.read())

    if 'jobId' in submitJson:
        jobID = submitJson['jobId']
        status = submitJson['jobStatus']
        jobUrl = taskUrl + "/jobs/" + jobID

        while status == "esriJobSubmitted" or status == "esriJobExecuting":
            print "Checking to see if job is completed..."
            time.sleep(1)
    
            jobResponse = urllib.urlopen(jobUrl,"f=json")
            jobJson = json.loads(jobResponse.read())

            if 'jobStatus' in jobJson:
                status = jobJson['jobStatus']

                if status == "esriJobSucceeded":
                    resultsUrl = jobUrl + "/results/"
                    resultsJson = jobJson['results']
                    for paramName in resultsJson.keys():
                        resultUrl = resultsUrl + paramName
                        resultResponse = urllib.urlopen(resultUrl,"f=json")
                        resultJson = json.loads(resultResponse.read())
                        output = urllib.urlopen(resultJson['value']['url'])
                        readOutput = output.read()
                        with open (outputZipfile,'wb') as zipfile:
                            zipfile.write(readOutput)
                        print resultJson['value']['url']

                if status == 'esriJobFailed':
                    if 'messages' in jobJson:
                        print jobJson['messages']

    else:
        print "no jobId found in the response"

aidsToNavigation = ["AidsToNavigation"]

getExtent(inputFC)
if len(aoi) == 0:
    print "Feature class returned no vertices."

outzip = os.path.join(outputFolder,'harbour_soundings.zip')

clipLyrs = ["SoundingsP\\Harbour_Sounding_point"]

taskUrl = 'https://encdirect.noaa.gov/arcgis/rest/services/encdirect/enc_gp_harbour/GPServer/ENC Extract Task'
submitUrl = taskUrl + '/submitJob'

wholeUrl = 'https://encdirect.noaa.gov/arcgis/rest/services/encdirect/' \
    'enc_gp_harbour/GPServer/ENC Extract Task/submitJob?Area_of_Interest={"spatialReference":' \
    '{"wkid":102100},"features":[{"geometry":{"spatialReference":{"wkid":102100},' \
    '"rings":[' + str(aoi) + ']}}]}&env:processSR=102100&Layers_to_Clip=' + str(clipLyrs) + \
    '&f=json&Feature_Format=Shapefile - SHP - .shp&env:outSR=102100'

getENCData(wholeUrl,outzip)
