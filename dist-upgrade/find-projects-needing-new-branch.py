#!/usr/bin/env python2

list_file1 = "repos-with-jellybean-4.3-branch.txt"
list_file2 = "ev-aosp-projects.txt"

list1=[]
list2=[]

with open(list_file1) as f:
    for l in f:
        list1.append(l.rstrip())

with open(list_file2) as f:
    for l in f:
        list2.append(l.rstrip())

list_to_remove=[]

for ii in list2:
    if ii in list1:
        list_to_remove.append(ii)

for ii in list_to_remove:
    list1.remove(ii)
    print "removing ", ii

with open("projects-need-new-branch.txt", 'w') as f:
    for ii in list1:
        f.write(ii+'\n')
