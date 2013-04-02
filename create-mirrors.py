#!/usr/bin/env python2.7
import xml.etree.ElementTree as ET


tree = ET.parse('default.xml')
root = tree.getroot()

for project in root:
    if project.tag == 'project':
        project.attrib.pop('path')
        if project.get('groups'):
          project.attrib.pop('groups')
    elif project.tag == 'remote':
        project.attrib.pop('review')
    for copyfile in project:
        if copyfile.tag == 'copyfile':
            project.remove(copyfile)

tree.write('mirror-host.xml')

tree = ET.parse('default.xml')
root = tree.getroot()

for project in root:
    if project.tag == 'project':
        if project.get('remote'):
            project.attrib.pop('remote')
    elif project.tag == 'remote':
        if project.get('name') == 'github':
            root.remove(project)
        elif project.get('name') == 'aosp':
            project.set('fetch','.')

tree.write('mirror-client.xml')

