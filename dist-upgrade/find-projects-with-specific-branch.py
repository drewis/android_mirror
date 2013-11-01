#!/usr/bin/env python2

try:
    import requests
except ImportError:
    print "requests module not found please install it (python2-requests)"
    exit()

import json
import xml.etree.ElementTree as ET

url = "https://api.github.com/orgs/Evervolv/repos?per_page=100"
int_branch = "jellybean-4.3"
output_file = "repos-with-%s-branch.txt" % int_branch
repos = []
usr = "" # XXX fill in
pas = "" # XXX fill in
user_pass=(usr,pas)

while True:
    print url
    req = requests.get(url, auth=user_pass)
    if req.status_code == requests.codes.ok:
        projects = json.loads(req.text)
        for p in projects:
            req2 = requests.get("https://api.github.com/repos/%s/branches" % p.get("full_name"),
                    auth=user_pass)
            if req2.status_code == requests.codes.ok:
                branches = json.loads(req2.text)
                for b in branches:
                    if int_branch == b.get("name"):
                        repos.append(p.get("name"))
                        print "Added ", p.get("name")
                        break
            else:
                print "Http err: skipping ", p.get('name')
    else:
        print "Http err: skipping ", url
    try:
        url = req.links['next']['url']
    except KeyError:
        break

repos.sort()

with open(output_file, 'w') as f:
    for r in repos:
        f.write(r+'\n')
