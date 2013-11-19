#!/usr/bin/env python2

try:
    import requests
except ImportError:
    print "requests module not found please install it (python2-requests)"
    exit()

import json

url = "https://api.github.com/orgs/Evervolv/repos?per_page=100"
url_branches = "https://api.github.com/repos/%(full_name)s/branches"
url_patch = "https://api.github.com/repos/Evervolv/%(repo_name)s"
int_branch = "kitkat"
usr = "" # XXX fill in
pas = "" # XXX fill in
user_pass=(usr,pas)

while True:
    print url
    req = requests.get(url, auth=user_pass)
    if req.status_code == requests.codes.ok:
        projects = json.loads(req.text)
        for p in projects:
            req2 = requests.get(url_branches % dict(full_name=p.get("full_name")),
                    auth=user_pass)
            if req2.status_code == requests.codes.ok:
                branches = json.loads(req2.text)
                for b in branches:
                    if int_branch == b.get("name"):
                        print "Found", p.get("name")
                        resp = requests.patch(url_patch % dict(repo_name=p.get("name")),
                            data=json.dumps(dict(name=p.get("name"),
                                default_branch=int_branch)),
                            auth=user_pass)
                        if resp.status_code == requests.codes.ok:
                            print "Set default_branch:", int_branch
                        else:
                            print "FAILED setting default_branch err:", resp.status_code
                        break
            else:
                print "Http err: skipping ", p.get("name")
    else:
        print "Http err: skipping ", url
    try:
        url = req.links["next"]["url"]
    except KeyError:
        break
