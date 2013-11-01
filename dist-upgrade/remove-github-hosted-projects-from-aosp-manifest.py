#!/usr/bin/env python2


import xml.etree.ElementTree as ET

old_xml = 'default.xml'
new_xml = 'kk.xml'

tree = ET.parse(old_xml)
root = tree.getroot()

hosted_projects = []
for project in root:
    if project.tag == 'project':
        if project.get('groups') == 'ev-aosp':
            hosted_projects.append(project.get('path')) # path here

tree = ET.parse(new_xml)
root = tree.getroot()

for project in root:
    if project.tag == 'project':
        if project.get('path') in hosted_projects:
            root.remove(project)

tree.write(new_xml)
