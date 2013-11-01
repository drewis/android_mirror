#!/usr/bin/env python2.7
import xml.etree.ElementTree as ET


tree = ET.parse('kk.xml')
root = tree.getroot()

rem = "aosp"
rev = "refs/tags/android-4.4_r1"

for project in root:
    if project.tag == 'project':
        project.attrib['remote'] = rem
        project.attrib['revision'] = rev

tree.write('kk.xml')
