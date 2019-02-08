import arcpy
import os

if arcpy.CheckExtension("network") == "Available":
    arcpy.CheckOutExtension("network")

folder = r'D:\Documents\GIS_Data\Tools\ship_tracks'
gdb = os.path.join(folder,'network.gdb')
network = os.path.join(gdb,'Venezuel_Network','Venezuel_Network_ND')
points = os.path.join(gdb,'Test_Points_1')

lyrName = 'BestRoute'
lyrxName = os.path.join(gdb,lyrName)

arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = True

result_object = arcpy.na.MakeRouteLayer(network,'newRoute','Length')
layer_object = result_object.getOutput(0)
sublayer_names = arcpy.na.GetNAClassNames(layer_object)
stops_layer_name = sublayer_names["Stops"]
routes_layer_name = sublayer_names["Routes"]

field_mappings = arcpy.na.NAClassFieldMappings(layer_object,stops_layer_name)
field_mappings["RouteName"].mappedFieldName = "Name"
arcpy.na.AddLocations(layer_object,stops_layer_name,points,field_mappings,"")
arcpy.na.Solve(layer_object,"SKIP")
routesSubLayer = arcpy.mapping.ListLayers(layer_object,routes_layer_name)[0]
arcpy.management.CopyFeatures(routesSubLayer,lyrxName)

print("Complete")
