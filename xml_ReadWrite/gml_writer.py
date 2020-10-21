# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 12:09:34 2020

@author: Philipp
"""

import xml.etree.ElementTree as ET
import xml.dom.minidom as MD


tree_root = {}
POINT = 'gml:Point'
POS = 'gml:Pos'
POSLIST = 'gml:PosList'
LINESTR = 'gml:LineString'


def create_root():
    global tree_root
    # register Namespace gml
    namespaces = {'xmlns:gml': 'http://www.opengis.net/gml'}

    # create the tree root
    tree_root = ET.Element('Tracks', namespaces)


def update_position(track_id, lon, lat):
    global tree_root

    selected_object = None

    pos_str = str(lon) + " " + str(lat)

    for child in tree_root:
        att = child.attrib
        if att['id'] == str(track_id):
            selected_object = child
            break

    if selected_object is None:
        print("Track with ID " + str(track_id) + " not found")
        return

    print("Track to be updated:")
    print(selected_object.attrib)

    print("Length: " + str(len(selected_object)))

    # If the length is 0, it means that no position has been logged yet.
    # We now have to initialize the first position
    if len(selected_object) == 0:
        lastPos_Point = ET.SubElement(selected_object, POINT)
        lastPos_position = ET.SubElement(lastPos_Point, POS)
        # lastPos_position.set('srsDimension', "2")
        lastPos_position.text = ""

        allPos_LineString = ET.SubElement(selected_object, LINESTR)
        allPos_positions = ET.SubElement(allPos_LineString, POSLIST)
        allPos_positions.text = ""
        allPosText = pos_str

    else:
        lastPos_Point = selected_object[0]
        lastPos_position = lastPos_Point[0]
        allPos_LineString = selected_object[1]
        allPos_positions = allPos_LineString[0]
        allPosText = ", " + pos_str

    # Now, all values are initialized.
    # We can now update the position to the current one

    lastPos_position.text = pos_str
    allPos_positions.text += allPosText


def update_classiden(track_id, classification_new, identification_new):
    global tree_root

    selected_object = None

    for child in tree_root:
        att = child.attrib
        if att['id'] == str(track_id):
            selected_object = child
            break

    if selected_object is None:
        print("Track with ID " + str(track_id) + " not found")
        return

    att = selected_object.attrib

    att['track_classification'] = str(classification_new)
    att['track_identification'] = str(identification_new)

    print("Track classIden updated")


def update_full(track_id, lon, lat, class_new, iden_new):
    update_position(track_id, lon, lat)
    update_classiden(track_id, class_new, iden_new)


def add_new_track(id_number, classification, identification):
    global tree_root
    flyingObject = ET.SubElement(tree_root, "flyingObject")

    flyingObject.set("id", str(id_number))
    flyingObject.set("track_classification", str(classification))
    flyingObject.set("track_identification", str(identification))
    return flyingObject


def prettyPrint():
    print(MD.parseString(ET.tostring(tree_root).decode()).toprettyxml())


def addTracks(x):
    # x = random.randint(2, 10)
    for i in range(x):
        add_new_track(i+1, "unknown", "unknown")

    print("Added " + str(x) + " Tracks")


def read_file(filename):
    global tree_root
    tree = ET.parse(filename)
    tree_root = tree.getroot()


def write_file(filename):
    # create a new XML file with the results
    print("\n    Writing File... \n")
    mydata = ET.tostring(tree_root).decode()

    dom = MD.parseString(mydata)
    # dom = expatbuilder.parseString(mydata, False)
    mydata_pretty = dom.toprettyxml()
    print(mydata_pretty)
    with open(filename, "w+") as myfile:
        myfile.write(mydata_pretty)


if __name__ == "__main__":
    print("XML Writer")
    create_root()
    addTracks(5)
    prettyPrint()
    print("Done")
