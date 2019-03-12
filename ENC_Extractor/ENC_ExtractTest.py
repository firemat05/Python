import arcpy
import urllib
import json
import time
import xml.etree.ElementTree as ET
import os

arcpy.env.ouverwriteOutput = True
mainDict = {}

def getXMLLayers():
    xmlFile = r'D:\Documents\GIS_Data\ENC_Extract\ENC_scale_layers.xml'
    xmlTree = ET.parse(xmlFile)
    xmlRoot = xmlTree.getroot()
    for elem in xmlRoot:
        elemArray = []
        for subElem in elem:
            elemArray.append(subElem.attrib['name'])
        mainDict[elem.attrib['name']] = elemArray        

getXMLLayers()

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [ENC_Extract]


class ENC_Extract(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "ENC Extract Test"
        self.description = "This is a test"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        param0 = arcpy.Parameter(
            displayName="Output Folder:",
            name="outputFolder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        param1 = arcpy.Parameter(
            displayName="Input Polygon Featureclass:",
            name="inputFC",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")

        param2 = arcpy.Parameter(
            displayName="Scale",
            name="scale",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        param2.filter.type = "ValueList"
        param2.filter.list = ["Overview","General","Coastal","Approach","Harbour","Berthing"]

        param3 = arcpy.Parameter(
            displayName="Categories",
            name="categories",
            datatype="GPString",
            parameterType="Required",
            multiValue="True",
            direction="Input")

        param3.parameterDependencies = [param2.name]

        params = [param0,param1,param2,param3]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
	
        parameters[3].filter.list = mainDict[parameters[2].value]

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        outputFolder = parameters[0].valueAsText
        inputFC = parameters[1].value
        scale = parameters[2].value
        options = parameters[3].valueAsText
        optionSplit = options.split(";")

        # get the extent of featureclass polygon
        def getExtent(fc):
            spatRef = arcpy.Describe(fc).spatialReference.name
            if spatRef != 'WGS_1984_Web_Mercator_Auxiliary_Sphere':
                arcpy.AddMessage("Projecting featureclass")
                arcpy.Project_management(fc,os.path.join(outputFolder,"aoi_proj.shp"),3857)
                fc = os.path.join(outputFolder,"aoi_proj.shp")
            with arcpy.da.SearchCursor(fc,['SHAPE@']) as cursor:
                for row in cursor:
                    shpArray = row[0].getPart()
                    for vertice in range(row[0].pointCount):
                        pnt = shpArray.getObject(0).getObject(vertice)
                        aoi.append([pnt.X,pnt.Y])

        # submit job to cooresponding geoprocess and downloads zipfile when complete
        def getENCData(url,outputZipfile,jobName,scaleText):
            taskUrl = 'https://encdirect.noaa.gov/arcgis/rest/services/encdirect/enc_gp_'+scale.lower()+'/GPServer/ENC Extract Task'
            
            submitResponse = urllib.urlopen(url)
            submitJson = json.loads(submitResponse.read())

            if 'jobId' in submitJson:
                jobID = submitJson['jobId']
                status = submitJson['jobStatus']
                jobUrl = taskUrl + "/jobs/" + jobID

                while status == "esriJobSubmitted" or status == "esriJobExecuting":
                    message = ("Checking to see if {} {} is completed...").format(scaleText,jobName)
                    arcpy.AddMessage(message)
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
                                message = resultJson['value']['url']
                                arcpy.AddMessage(message)

                        if status == 'esriJobFailed':
                            if 'messages' in jobJson:
                                message = jobJson['messages']
                                arcpy.AddMessage(message)

            else:
                arcpy.AddMessage("no jobId found in the response")

        # format the text from layer to input into clip layer array
        def formatArrayText(textCategory,scaleText,textLayer):
            geometries = {"OINT":"P","LINE":"L","AREA":"A"}
            outputText = ("{}{}\\{}_{}").format(textCategory,geometries[textLayer[-4:].upper()],scaleText,textLayer)
            return outputText

        # iterate xml to get available layers from each scale
        def getLayerNames(scaleToExtract,wantedLayer):
            xmlFile = r'D:\Documents\GIS_Data\ENC_Extract\ENC_scale_layers.xml' # change later
            finalArray = []
            tree = ET.parse(xmlFile)
            root = tree.getroot()
            for elem in root:
                if elem.attrib['name'] == scaleToExtract:
                    for subelem in elem:
                        if subelem.attrib['name'] == wantedLayer:
                            finalArray.append(subelem.attrib['name'])
            for category in finalArray:
                categoryArray = []
                for elem in root:
                    if elem.attrib['name'] == scaleToExtract:
                        for subelem in elem:
                            if subelem.attrib['name'] == category:
                                for subsubelem in subelem:
                                    categoryText = formatArrayText(subelem.attrib['name'],scaleToExtract,subsubelem.attrib['name'])
                                    categoryArray.append(categoryText)
            return categoryArray

        wantedLayers = []
        for option in optionSplit:
            wantedLayers.append(option)

        aoi = []
        getExtent(inputFC)
        if len(aoi) == 0:
            arcpy.AddMessage("Featureclass returned no vertices.")
        else:
            # iterate through layers list and download zipfile from online geoprocess
            for layer in wantedLayers:
                outzip = os.path.join(outputFolder,scale+"_"+layer+'.zip')
                clipLyrs = getLayerNames(scale,layer)
    
                wholeUrl = 'https://encdirect.noaa.gov/arcgis/rest/services/encdirect/enc_gp_' + scale.lower() + \
                    '/GPServer/ENC Extract Task/submitJob?Area_of_Interest={"spatialReference":{"wkid":102100},' \
                    '"features":[{"geometry":{"spatialReference":{"wkid":102100},"rings":['+str(aoi)+']}}]}&env' \
                    ':processSR=102100&Layers_to_Clip='+str(clipLyrs)+'&f=json&Feature_Format=Shapefile - SHP - .shp&env:outSR=102100'

                message = ("Submitted: {}, {}").format(scale,layer)
                arcpy.AddMessage(message)
                getENCData(wholeUrl,outzip,layer,scale)
        #arcpy.AddMessage(outputFolder)
        #arcpy.AddMessage(inputFC)
        #arcpy.AddMessage(optionArray)

        return


