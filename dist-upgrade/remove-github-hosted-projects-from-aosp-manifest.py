#!/usr/bin/env python2


import xml.etree.ElementTree as ET

old_xml = 'old.xml'
new_xml = 'kk.xml'

tree = ET.parse(old_xml)
root = tree.getroot()

hosted_projects = []
for project in root:
    if project.tag == 'project':
        if project.get('groups') == 'ev-aosp':
            hosted_projects.append(project.get('path'))

tree = ET.parse(new_xml)
root = tree.getroot()

projects_to_remove = []
for project in root:
    if project.tag == 'project':
        if project.get('path') in hosted_projects:
            projects_to_remove.append(project.get('path'))

for project in projects_to_remove:
    for p in root:
        if p.tag == 'project':
            if p.get('path') == project:
                root.remove(p)
                break

tree.write(new_xml)
