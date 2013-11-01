#!/usr/bin/env python2.7
import xml.etree.ElementTree as ET


tree = ET.parse('old.xml')
root = tree.getroot()

p = []
for project in root:
    if project.tag == 'project':
        if project.get('groups') == 'ev-aosp':
            p.append((project.get('path'),project.get('name')))

tree = ET.parse('kk.xml')
root = tree.getroot()

p2 = []
for proj in p:
    for project in root:
        if project.tag == "project":
            if project.get("path") == proj[0]:
                p2.append(project.get("name")+","+proj[1])
                break

with open('ev-aosp-projects-matched-with-aosp-project-names.txt','w') as f:
    for e in p2:
        f.write(e+'\n')
