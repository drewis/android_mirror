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
'''
        if project.get('remote') == 'github':
            project.attrib.pop('remote')
        else:
            project.attrib['remote'] = 'aosp'
        if project.get('revision') == 'jellybean-4.3':
            project.attrib.pop('revision')
        else:
            project.attrib['revision'] = 'android-4.3_r2.1'

tree.write('default.xml')
'''
'''
with open('ev_unique_projects.txt','w') as f:
    for t in p:
        f.write(t + '\n')
'''
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
