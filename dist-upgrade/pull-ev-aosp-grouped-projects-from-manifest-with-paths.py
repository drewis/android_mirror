#!/usr/bin/env python2.7
import xml.etree.ElementTree as ET


tree = ET.parse('old.xml')
root = tree.getroot()

p = []
for project in root:
    if project.tag == 'project':
        if project.get('groups') == 'ev-aosp':
            p.append(project.get('path')+","+project.get('name'))

with open('ev-aosp-projects-with-paths.txt','w') as f:
    for e in p:
        f.write(e+'\n')
