# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 13:15:49 2020

@author: Philipp
"""

import xml.etree.ElementTree as ET


def read_file():
    tree = ET.parse('countries.xml')
    root = tree.getroot()
    print(root.tag)
    print(root.attrib)
    
    
    for child in root:
        print(child.attrib)
        for uc in child:
            print(uc.tag, uc.attrib, uc.text)






if __name__== "__main__":
    print("XML Reader")
    read_file()
    print("Done")