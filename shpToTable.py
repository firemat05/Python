import arcpy
import os
import random


def addFields(tempFile):
    print "Adding required fields..."
    arcpy.AddField_management(tempFile, "Date", "DATE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(tempFile, "Area", "TEXT", "", "", 25, "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(tempFile, "District", "TEXT", "", "", 25, "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(tempFile, "Type", "TEXT", "", "", 25, "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddXY_management(tempFile)

    print "Entering random dates..."
    rows = arcpy.UpdateCursor (tempFile)
    for row in rows:
        mon = random.randrange(1,12)
        day = random.randrange(1,28)
        year = "2016"
        date = "{}/{}/{}".format(day,mon,year)
        row.Date = date
        rows.updateRow(row)
    del rows

curFile = "C:\\Users\\Mat\\Documents\\GIS_Data\\GIS_Training\\GIS_Student_Folder\\Lesson_1\\Shapefiles\\misleCreation\\migPoints.shp"
addFields(curFile)
dist = "District 14"
opArea = "Pacific Area"

selection = "Migration"

if (selection == "SAR"):
    rows = arcpy.UpdateCursor(curFile)
    for row in rows:
        sarList = ['Hoax','SAR']
        sarType = random.choice(sarList)
        row.Type = sarType
        row.Area = opArea
        row.District = dist
        rows.updateRow(row)
    del rows

if (selection == "Drug"):
    arcpy.AddField_management(curFile, "Lbs", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(curFile, "Kgs", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    rows = arcpy.UpdateCursor(curFile)
    for row in rows:
        drugAmount = random.randrange(1, 1000, 1)
        drugList = ['Marijuana','Cocaine','Meth']
        drug = random.choice(drugList)
        row.Type = drug
        row.Lbs = drugAmount
        row.Kgs = row.Lbs * 0.453592
        row.Area = opArea
        row.District = dist
        rows.updateRow(row)
    del rows

if (selection == "Migration"):
    arcpy.AddField_management(curFile, "Total", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    rows = arcpy.UpdateCursor(curFile)
    for row in rows:
        nations = ['Cuba','Haiti','Dom Rep']
        nation = random.choice(nations)
        amount = random.randrange(1,30)
        row.Type = nation
        row.Total = amount
        row.Area = opArea
        row.District = dist
        rows.updateRow(row)
    del rows

