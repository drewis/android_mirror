#!/usr/bin/env python2

try:
    import requests
except ImportError:
    print "requests module not found please install it (python2-requests)"
    exit()

import json
import xml.etree.ElementTree as ET

def_remote = "github"
def_revision = "jellybean"
def_fetch_url = "https://github.com/Evervolv/"
url = "https://api.github.com/orgs/Evervolv/repos?per_page=100"
local_mirror_manifest = "evervolv.xml"
repos = []
usr = ""
pas = ""
user_pass=(usr,pas)

while True:
    retrys = 0
    while retrys < 5:
        req = requests.get(url, auth=user_pass)
        if req.status_code == requests.codes.ok:
            break
        retrys += 1
    content = json.loads(req.text)
    #repos.extend([ (c.get('name'),c.get('master_branch')) for c in content ])
    for c in content:
        req = requests.get("https://api.github.com/repos/%s/branches" % c.get("full_name"),
                auth=user_pass)
        if req.status_code == requests.codes.ok:
            branches = json.loads(req.text)
            for b in branches:
                if "jellybean-4.3" == b.get("name"):
                    repos.append(c.get("name"))
                    print c.get("name")
                    break
        else:
            print "Http err: skiping ", c.get('name')
    try:
        url = req.links['next']['url']
    except KeyError:
        break

repos.sort(key=lambda n: n[0])

with open("repos-with-current-branch.txt", 'w') as f:
    for r in repos:
        f.write(r+'\n')

exit()

root = ET.Element("manifest")
ET.SubElement(root, "remote", name="%s" % def_remote, fetch="%s" % def_fetch_url)
#ET.SubElement(root, "default", revision="%s" % def_revision, remote="%s" % def_remote)

for r in repos:
    ET.SubElement(root, "project", name="%s" % r[0], 
            remote="%s" % def_remote, revision="%s" % r[1])

tree = ET.ElementTree(root)
tree.write(local_mirror_manifest ,encoding="UTF-8", xml_declaration=True)
# ^^ Super ugly oneline xml doc, Better way ?
# Pretty print xml
import xml.dom.minidom as md
xml = md.parse(local_mirror_manifest)
with open(local_mirror_manifest, 'w') as f:
    f.write(xml.toprettyxml())

print "Done creating %s" %  local_mirror_manifest
