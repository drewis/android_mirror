#!/usr/bin/env python2

import os
import subprocess

projects = []
with open('ev-aosp-projects-matched-with-aosp-project-names.txt') as f:
    for l in f:
        projects.append((l.rstrip().split(',')))

gerrit_user = 'drewis'
aosp_tag = 'kitkat-release'
new_branch = 'kitkat'

topdir = os.getcwd()
for p in projects:
    print p[0]
    os.chdir(p[0]+'.git')
    subprocess.call(['git','push','ssh://%s@review.evervolv.com:8082/%s.git'
        % (gerrit_user,p[1]), '%s:refs/heads/%s' % (aosp_tag,new_branch)])
    os.chdir(topdir)
