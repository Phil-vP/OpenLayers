# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 12:09:34 2020

@author: Philipp
"""

import xml.etree.ElementTree as ET
import xml.dom.minidom as MD


global tree_root


def create_file():
    global tree_root
    # create the file structure
    # tree_root = ET.Element('data')
    # items = ET.SubElement(tree_root, 'itemsABC')
    # item1 = ET.SubElement(items, 'item')
    # item2 = ET.SubElement(items, 'item')
    # item1.set('name','item1')
    # item2.set('name','item2')
    # item1.text = 'item1abc'
    # item2.text = 'item2abc'
    tree_root = ET.Element('Tracks')
    flyingObject_1 = ET.SubElement(tree_root, "flyingObject")
    # lastPos = ET.SubElement(flyingObject_1, "gml:Point")
    # allPos = ET.SubElement(flyingObject_1, "gml:LineString")
    
    lastPos_Point = ET.SubElement(flyingObject_1, "gmlPoint")
    lastPos_position = ET.SubElement(lastPos_Point, "gmlPos")
    lastPos_position.set('srsDimension', "2")
    lastPos_position.text = "asdf"
    
    allPos_LineString = ET.SubElement(flyingObject_1, "gmlLineString")
    allPos_positions = ET.SubElement(allPos_LineString, "gmlPosList")
    
    
    
    write_file("items.xml")


def addSubEl(new_name, parent):
    global tree_root
    for child in tree_root:
        print(child.attrib)
    
    

def write_file(filename):
    global tree_root
    
    # create a new XML file with the results
    mydata = ET.tostring(tree_root).decode()
    
    dom = MD.parseString(mydata)
    mydata_pretty = dom.toprettyxml()
    print(mydata)
    print(mydata_pretty)
    with open(filename, "w+") as myfile:
        myfile.write(mydata_pretty)
    



if __name__== "__main__":
    print("XML Writer")
    create_file()
    print("Done")