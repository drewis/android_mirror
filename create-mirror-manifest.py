#!/usr/bin/env python2

try:
    import requests
except ImportError:
    print "requests module not found please install it (python2-requests)"
    exit()

import json
import xml.etree.ElementTree as ET

def_remote = "ev"
def_revision = "jellybean"
url = "https://api.github.com/orgs/Evervolv/repos?per_page=100"
repos = []

while True:
    retrys = 0
    while retrys < 5:
        req = requests.get(url)
        if req.status_code == requests.codes.ok:
            break
        retrys += 1
    content = json.loads(req.text)
    repos.extend([ c.get('name') for c in content ])
    try:
        url = req.links['next']['url']
    except KeyError:
        break

repos.sort()

root = ET.Element("manifest")
ET.SubElement(root, "remote", name="%s" % def_remote, fetch="..")
ET.SubElement(root, "default", revision="%s" % def_revision, remote="%s" % def_remote)

for r in repos:
    ET.SubElement(root, "project", name="%s" % r)

tree = ET.ElementTree(root)
tree.write("manifest.xml" ,encoding="UTF-8", xml_declaration=True)
# ^^ Super ugly oneline xml doc, Better way ?
# Pretty print xml
import xml.dom.minidom as md
xml = md.parse("manifest.xml")
with open("manifest.xml", 'w') as f:
    f.write(xml.toprettyxml())

print "Done creating %s" %  "mainfest.xml"
