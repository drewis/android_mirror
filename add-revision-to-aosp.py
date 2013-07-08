#!/usr/bin/env python2.7
import xml.etree.ElementTree as ET
import os
import subprocess

# Extract all projects form aosp mirror manifest
tree = ET.parse('aosp.xml')
root = tree.getroot()

aosp_repos = []
for project in root:
    if project.tag == 'project':
        aosp_repos.append(project.get('name'))

# Extract all projects from ev mirror manifest
tree = ET.parse('default.xml')
root = tree.getroot()

ev_repos = []
for project in root:
    if project.tag == 'project':
        ev_repos.append(project.get('name'))

# Sort just cause
aosp_repos.sort()
ev_repos.sort()

# Convert the ev names to equivalent aosp names
# ( eg android_frameworks_base > platform/frameworks/base
ev_repos_converted = []
for r in ev_repos:
    if r == 'android':
        ev_repos_converted.append('platform/manifest')
        continue
    r2 = r.lstrip('android').lstrip('_').replace('_','/')
    if r2.startswith('device') or r2.startswith('kernel'):
        ev_repos_converted.append(r2)
        continue
    else:
        ev_repos_converted.append('platform/'+r2)
        continue

# Map converted name to real one
ev_mapping = zip(ev_repos,ev_repos_converted)
# Map as dict (to find real name from converted one)
ev_mapping_rev_dict = dict(zip(ev_repos_converted,ev_repos))
# Match common projects
shared = set(ev_repos_converted) & set(aosp_repos)
# Locate unique ev projects
ev_unique = set(ev_repos_converted) - set(aosp_repos)
# Remap unique ev projects back to real name
ev_unique_remapped = [ r[0] for r in ev_mapping if r[1] in ev_unique ]
ev_unique_remapped.sort()
# Write unique projects to new manifest for reference
ev_manifest = "ev_unique.xml"
root = ET.Element("manifest")

for r in ev_unique_remapped:
    ET.SubElement(root, "project", name="%s" % r,remote="ev",revision="jellybean")

tree = ET.ElementTree(root)
tree.write(ev_manifest,encoding="UTF-8", xml_declaration=True)
# ^^ Super ugly oneline xml doc, Better way ?
# Pretty print xml
import xml.dom.minidom as md
xml = md.parse(ev_manifest)
with open(ev_manifest, 'w') as f:
    f.write(xml.toprettyxml())

failed = []
# Create symbolic links for ev shared projects
# to the aosp naming so mirroring will work correctly
for s in shared:
    print "linking %s.git -> %s.git" % (ev_mapping_rev_dict.get(s),s)
    try:
        os.symlink("%s.git" % s,"%s.git" % ev_mapping_rev_dict.get(s))
    except:
        failed.append(s)

cur_dir = os.getcwd()
for s in shared:
    os.chdir(s+".git")
    print "Adding ev remote %s to %s" % (ev_mapping_rev_dict.get(s),s)
    subprocess.call(['git','remote','add','ev','--no-tags',"https://github.com/Evervolv/%s"
        % ev_mapping_rev_dict.get(s)])
    print "Fixing ev remote to pull to ev/*"
    subprocess.call(['git','config','remote.ev.fetch','+refs/heads/*:refs/heads/ev/*'])
    print "Adding cm remote %s to %s (no tags)" % (ev_mapping_rev_dict.get(s),s)
    subprocess.call(['git','remote','add','cm','--no-tags',"https://github.com/CyanogenMod/%s"
        % ev_mapping_rev_dict.get(s)])
    print "Fixing cm remote to pull to cm/*"
    subprocess.call(['git','config','remote.cm.fetch','+refs/heads/*:refs/heads/cm/*'])
    print "Adding caf remote %s to %s (no tags)" % (s,s)
    subprocess.call(['git','remote','add','caf','--no-tags','git://codeaurora.org/%s'
        % s ])
    print "fixing caf remote to pull to caf/*"
    subprocess.call(['git','config','remote.caf.fetch','+refs/heads/*:refs/heads/caf/*'])

    os.chdir(cur_dir)

print failed
print "DONE"
