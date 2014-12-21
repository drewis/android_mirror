#!/usr/bin/env python2
'''Scraps github and creates repo manifest of all projects'''

try:
    import requests
except ImportError:
    print "requests module not found please install it (python2-requests)"
    exit()

import json
import xml.etree.ElementTree as ET

def_remote = "github"
def_fetch_url = "https://github.com/Evervolv/"
url = "https://api.github.com/orgs/Evervolv/repos?per_page=100"
local_mirror_manifest = "evervolv.xml"
repos = []

while True:
    retrys = 0
    while retrys < 5:
        req = requests.get(url)
        if req.status_code == requests.codes.ok:
            break
        retrys += 1
    content = json.loads(req.text)
    repos.extend([ (c.get('name'),c.get('default_branch')) for c in content ])
    try:
        url = req.links['next']['url']
    except KeyError:
        break

repos.sort(key=lambda n: n[0])

root = ET.Element("manifest")
ET.SubElement(root, "remote", name="%s" % def_remote, fetch="%s" % def_fetch_url)

for r in repos:
    ET.SubElement(root, "project", name="%s" % r[0], 
            remote="%s" % def_remote, revision="%s" % r[1])

tree = ET.ElementTree(root)
tree.write(local_mirror_manifest ,encoding="UTF-8", xml_declaration=True)
# ^^ Super ugly oneline xml doc
# Pretty print xml
import xml.dom.minidom as md
xml = md.parse(local_mirror_manifest)
with open(local_mirror_manifest, 'w') as f:
    f.write(xml.toprettyxml())

print "Done creating %s" %  local_mirror_manifest
