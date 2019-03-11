import xml.etree.cElementTree as ET

xmlDoc = r'D:\Documents\GIS_Data\ENC_Extract\ENC_Layers.xml'

root = ET.Element("root")
doc = ET.SubElement(root,"scale",name="Harbour")

lyr = ET.SubElement(doc,"category",name="AidsToNavigation")
ET.SubElement(lyr,"layer",name="buoy_point")

tree = ET.ElementTree(root)
tree.write(xmlDoc)
