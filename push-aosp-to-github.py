#!/usr/bin/env python2

import json
import os
import subprocess

with open('shared.json') as f:
    mapping = json.load(f)

shared = []
with open('shared.txt') as f:
    for l in f:
        shared.append(l.rstrip('\n'))

tree = '/opt/android2/aosp'
gerrit_user = 'drewis'
aosp_tag = 'android-4.3_r2.1'
new_branch = 'jellybean-4.3'
os.chdir(tree)
for s in shared:
    cur_dir = os.getcwd()
    os.chdir(s)
    subprocess.call(['echo','git','push','ssh://%s@review.evervolv.com:8082/%s.git'
            % (gerrit_user,mapping.get(s)), '%s:refs/heads/%s' % (aosp_tag,new_branch)])
    os.chdir(cur_dir)

