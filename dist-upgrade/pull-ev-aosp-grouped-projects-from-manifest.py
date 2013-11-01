#!/usr/bin/env python2.7
import xml.etree.ElementTree as ET


tree = ET.parse('default.xml')
root = tree.getroot()

p = []
for project in root:
    if project.tag == 'project':
        if project.get('groups') == 'ev-aosp':
            p.append(project.get('name'))

with open('ev-aosp-projects.txt','w') as f:
    for e in p:
        f.write(e+'\n')
