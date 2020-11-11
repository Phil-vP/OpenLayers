# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 12:09:34 2020

@author: Philipp
"""

import geojson

lastKnownPositions = {}
positionHistory = {}



def update_position(track_id, lon, lat):
    global lastKnownPositions
    global positionHistory
    
    id_str = str(track_id)
    
    # If the Track is already created, this will do nothing
    addNewTrack(track_id)
    
    updatedPoint = (lon, lat)
    
    feature = lastKnownPositions[id_str]
    feature.geometry.coordinates = updatedPoint
    
    feature_ls = positionHistory[id_str]
    feature_ls.geometry.coordinates.append(updatedPoint)
    
    
    # print("Updated Track " + id_str + " to " + str(updatedPoint))
    # print(updatedPoint)
    # print(lastKnownPositions)


def update_classiden(track_id, classification_new, identification_new):
    global lastKnownPositions
    
    id_str = str(track_id)
    
    # If the Track is already created, this will do nothing
    addNewTrack(track_id)
    
    feature = lastKnownPositions[id_str]
    fProperties = feature.properties
    
    fProperties['classification'] = str(classification_new)
    fProperties['identification'] = str(identification_new)
    
    
    feature_ls = positionHistory[id_str]
    fProperties_ls = feature_ls.properties
    
    fProperties_ls['classification'] = str(classification_new)
    fProperties_ls['identification'] = str(identification_new)


def update_full(track_id, lon, lat, class_new, iden_new):
    update_position(track_id, lon, lat)
    update_classiden(track_id, class_new, iden_new)


def update_sidc(track_id, value):
    global lastKnownPositions
    
    id_str = str(track_id)
    
    # If the Track is already created, this will do nothing
    addNewTrack(track_id)
    
    feature = lastKnownPositions[id_str]
    updatedProperties = feature['properties']
    updatedProperties['sidc'] = str(value)
    
    feature['properties'] = updatedProperties

def addNewTrack(track_id):
    global lastKnownPositions
    global positionHistory
    
    id_str = str(track_id)
    
    if id_str in list(lastKnownPositions.keys()):
        return
    
    print("Adding new track")
    
    newPoint = geojson.Point((0, 0))
    
    properties = {}
    properties['classification'] = "unknown"
    properties['identification'] = "unknown"
    f_p = geojson.Feature(id_str, newPoint, properties)
    lastKnownPositions[id_str] = f_p
    
    zerotuple = (0,0)
    coo_list = []
    
    newLineString = geojson.LineString(coo_list)
    f_ls = geojson.Feature(id_str, newLineString, properties.copy())
    positionHistory[id_str] = f_ls
    
    


def prettyPrint():
    print("Pretty printing")
    keys = list(lastKnownPositions.keys())
    for k in keys:
        print("ID: " + str(k))
        print("Feature lastKnownPositions: " + str(lastKnownPositions[k]))
        print("Feature positionHistory: " + str(positionHistory[k]))
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
    
	feature_list = []
    feature_list.extend(list(lastKnownPositions.values()))
    feature_list.extend(list(positionHistory.values()))
    feature_collection = geojson.FeatureCollection(feature_list)
    
    with open(filename, "w+") as myfile:
        myfile.write(geojson.dumps(feature_collection, indent=4, sort_keys=True))


def testRun():
    print("test run")
    update_position(1, 11.49, 48.77)
    update_position(1, 11.47, 48.80)
    update_position(1, 11.44, 48.81)
    update_position(2, 11.50, 48.81)
    update_position(2, 11.48, 48.82)
    update_classiden(1, "friendly", "AWACS")
    update_sidc(1, "SFGPUCI----F---")
	update_sidc(2, "SUAP--------")
    write_file("test1.json")
    prettyPrint()


if __name__ == "__main__":
    print("geoJSON Writer")
    testRun()
    # prettyPrint()
    print("Done")
