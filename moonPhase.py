## Classification: UNCLASSIFIED
## Name: Moon Phaser
## Author: Mat Frank
## Description: Determines moon phase

import os
import xlrd
import arcpy
import csv

# Define parameters

excelIn = arcpy.GetParameterAsText(0)
excelPath = os.path.dirname (excel)

databaseOut = arcpy.GetParameterAsText(1)
tableIn = arcpy.GetParameterAsText(2)
fieldName = arcpy.GetParameterAsText (3) # Derived from tableIn

tableOutput = os.path.join(excelPath,"Moon_Output.csv")


# Excel to table function
def importAllSheets(in_excel,out_gdb):
    workbook = xlrd.open_workbook(in_excel)
    sheets = [sheet.name for sheet in workbook.sheets()]
    print('{} sheets found: {}'.format(len(sheets), ','.join(sheets)))
    for sheet in sheets:
        out_table = os.path.join(
            out_gdb,
            arcpy.ValidateTableName(
                "{0}_{1}".format(os.path.basename(in_excel),sheet),out_gdb))
        print('Converting {} to {}'.format(sheet,out_gdb))
        arcpy.ExcelToTable_conversion(in_excel,out_table,sheet)

# Determine moon phase function
def moonPhase(month,day,year):
    ages = [15, 0, 11, 22, 3, 14, 25, 6, 17, 28, 9, 20, 1, 12, 23, 4, 15, 26, 7]
    offsets = [-1, 1, 0, 1, 2, 3, 4, 5, 7, 7, 9, 9]
    description = ["new (totally dark)",
                   "waxing crescent (increasing to full)",
                   "in its first quarter (increasing to full)",
                   "waxing gibbous (increasing to full)",
                   "full (full light)",
                   "waning gibbous (decreasing from full)",
                   "in its last quarter (decreasing from full)",
                   "waning crescent (decreasing from full)"]
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    if day == 31:
        day = 1
    days_into_phase = ((ages[(year+1) % 19] +
                        ((day + offsets[month-1]) % 30) +
                        (year < 1900)) % 30)
    index = int((days_into_phase + 2) * 16/59.0)
    #print(index) #test
    if index > 7:
        index = 7
    status = description[index]

    # Light should be 100% 15 days into phase
    light = int(2 * days_into_phase * 100/29)
    if light > 100:
        light=abs(light-200);
    date = "%d%s%d" % (day,months[month-1],year)
    return date, status, light

# Start the fireworks below here:

# See if the output file already exists and delete if it does
try:
    os.remove(tableOutput)
except OSError:
    pass
print("Moon_Output.csv deleted")
outText = tableOutput

# Convert the excel sheet to a table:
if __name__ == '__main__':
    importAllSheets(excelIn,databaseOut)


# Determine moonphase
cursor = arcpy.SearchCursor(tableIn)
for row in cursor:
    fullDate = str(row.getValue(fieldName))
    year = int(fullDate[:4])
    month = int(fullDate[5:7])
    day = int(fullDate[8:10])
    date,status,light = moonPhase(month,day,year)
    ("Date: %s, Status: %s, light: %d%s" % (date,status,light,'%'))
    openFile.write("Date: %s, Status: %s, light: %d%s" % (date,status,light,'%, '))
openFile.close()

with open(outtext,'w') as csvfile:
    fieldnames = ['Date', 'Status', 'Light']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({})#############

print "done"



dates = [09/28/2016,09/28/2016,09/30/2016,09/30/2016,09/30/2016,09/29/2016,09/29/2016,09/29/2016,09/28/2016,09/24/2016,09/21/2016,09/8/2016,09/3/2016,09/3/2016,08/29/2016,08/23/2016,08/10/2016,07/29/2016,07/14/2016,07/4/2016,07/1/2016,06/19/2016,06/11/2016,05/29/2016,05/11/2016,02/10/2016,02/8/2016,02/3/2016,01/23/2016,10/31/2015,01/11/2016,12/16/2015,12/4/2015,11/21/2015,10/25/2015,10/18/2015,10/10/2015]
for date in dates:
    year = int(date[-4:])
    month = int(date[0:2])
    day = int(date[3:5])
