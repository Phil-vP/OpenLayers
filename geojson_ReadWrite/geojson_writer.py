# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 12:09:34 2020

@author: Philipp
"""

import geojson

lastKnownPositions = {}



def update_position(track_id, lon, lat):
    global lastKnownPositions
    
    id_str = str(track_id)
    
    # If the Track is already created, this will do nothing
    addNewTrack(track_id)
    
    updatedPoint = geojson.Point((lon, lat))
    
    feature = lastKnownPositions[id_str]
    feature["geometry"] = updatedPoint
    
    # print("Updated Track " + id_str + " to " + str(updatedPoint))
    # print(updatedPoint)
    # print(lastKnownPositions)


def update_classiden(track_id, classification_new, identification_new):
    global lastKnownPositions
    
    id_str = str(track_id)
    
    # If the Track is already created, this will do nothing
    addNewTrack(track_id)
    
    feature = lastKnownPositions[id_str]
    updatedProperties = feature['properties']
    
    updatedProperties['classification'] = str(classification_new)
    updatedProperties['identification'] = str(identification_new)
    
    feature['properties'] = updatedProperties


def update_full(track_id, lon, lat, class_new, iden_new):
    update_position(track_id, lon, lat)
    # update_classiden(track_id, class_new, iden_new)


def addNewTrack(track_id):
    global lastKnownPositions
    
    id_str = str(track_id)
    
    if id_str in list(lastKnownPositions.keys()):
        return
    
    print("Adding new track")
    
    newPoint = geojson.Point((0, 0))
    
    properties = {}
    properties['classification'] = "unknown"
    properties['identification'] = "unknown"
    f = geojson.Feature(id_str, newPoint, properties)
    lastKnownPositions[id_str] = f
    


def prettyPrint():
    print("Pretty printing")
    keys = list(lastKnownPositions.keys())
    for k in keys:
        print("ID: " + str(k))
        print("Feature: " + str(lastKnownPositions[k]))
        print("================")


def addTracks(x):
    # x = random.randint(2, 10)
    for i in range(x):
        addNewTrack(i+1)

    print("Added " + str(x) + " Tracks")


def read_file(filename):
    print("Reading file " + str(filename) + "...")


def write_file(filename):
    # create a new XML file with the results
    print("\n    Writing File... \n")
    
    feature_list = list(lastKnownPositions.values())
    feature_collection = geojson.FeatureCollection(feature_list)
    
    with open(filename, "w+") as myfile:
        myfile.write(geojson.dumps(feature_collection, indent=4, sort_keys=True))


def testRun():
    print("test run")
    update_position(1, 10, 15)
    update_position(2, 8, 7)
    update_classiden(1, "friendly", "AWACS")
    write_file("test1.json")


if __name__ == "__main__":
    print("geoJSON Writer")
    testRun()
    # prettyPrint()
    print("Done")
