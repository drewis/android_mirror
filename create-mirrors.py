#!/usr/bin/env python2.7
import xml.etree.ElementTree as ET


tree = ET.parse('ev_unique.xml')
root = tree.getroot()

p = []
for project in root:
    if project.tag == 'project':
        if project.get('path'):
            project.attrib.pop('path')
        if project.get('groups'):
            project.attrib.pop('groups')
        if project.get('revision'):
            project.attrib.pop('revision')
        p.append(project.get('name') + '.git')
    elif project.tag == 'remote':
        project.attrib.pop('review')
    for copyfile in project:
        if copyfile.tag == 'copyfile':
            project.remove(copyfile)

tree.write('mirror-host.xml')
with open('ev_unique_projects.txt','w') as f:
    for t in p:
        f.write(t + '\n')
'''
tree = ET.parse('default.xml')
root = tree.getroot()

for project in root:
    if project.tag == 'project':
        if project.get('remote'):
            project.attrib.pop('remote')
        if project.get('groups'):
            project.attrib.pop('groups')
    elif project.tag == 'remote':
        if project.get('name') == 'github':
            root.remove(project)
        elif project.get('name') == 'aosp':
            project.attrib.pop('review')
            project.set('fetch','.')

tree.write('mirror-client.xml')
'''
