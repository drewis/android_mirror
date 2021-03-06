#!/usr/bin/env python2
import xml.etree.ElementTree as ET
import os
import subprocess
import xml.dom.minidom as md

# Extract all projects form aosp mirror manifest
tree = ET.parse('aosp.xml')
root = tree.getroot()

aosp_repos = []
for project in root:
    if project.tag == 'project':
        aosp_repos.append(project.get('name'))

# Extract all projects from ev mirror manifest
local_mirror_manifest = "evervolv.xml"
tree = ET.parse(local_mirror_manifest)
root = tree.getroot()

ev_repos = []
ev_repos_branches = {}
for project in root:
    if project.tag == 'project':
        ev_repos.append(project.get('name'))
        ev_repos_branches[project.get('name')] = project.get('revision')

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
    elif r == 'android_external_fsck_msdos':
        ev_repos_converted.append('platform/external/fsck_msdos')
        continue
    elif r == 'android_external_wpa_supplicant':
        ev_repos_converted.append('platform/external/wpa_supplicant')
        continue
    elif r == 'android_external_wpa_supplicant_6':
        ev_repos_converted.append('platform/external/wpa_supplicant_6')
        continue
    elif r == 'android_external_wpa_supplicant_8':
        ev_repos_converted.append('platform/external/wpa_supplicant_8')
        continue
    elif r == 'android_hardware_libhardware_legacy':
        ev_repos_converted.append('platform/hardware/libhardware_legacy')
        continue
    elif r == 'android_kernel_grouper':
        ev_repos_converted.append('kernel/tegra')
        continue
    elif r == 'android_kernel_lge_mako':
        ev_repos_converted.append('kernel/msm')
        continue
    elif r == 'android_kernel_samsung_manta':
        ev_repos_converted.append('kernel/exynos')
        continue
    elif r == 'android_kernel_samsung_tuna':
        ev_repos_converted.append('kernel/omap')
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
shared = sorted(set(ev_repos_converted) & set(aosp_repos))
# Locate unique ev projects
ev_unique = sorted(set(ev_repos_converted) - set(aosp_repos))
# Remap unique ev projects back to real name
ev_unique_remapped = sorted([ r[0] for r in ev_mapping if r[1] in ev_unique ])

# Write unique projects to new manifest for reference
ev_manifest = "ev_unique.xml"
def_remote = "ev"
def_revision = "jellybean"
def_fetch_url = "https://github.com/Evervolv/"
root = ET.Element("manifest")
ET.SubElement(root, "remote", name=def_remote, fetch=def_fetch_url)

for r in ev_unique_remapped:
    ET.SubElement(root, "project", name=r, remote="ev", revision=ev_repos_branches.get(r))

tree = ET.ElementTree(root)
tree.write(ev_manifest,encoding="UTF-8", xml_declaration=True)
# Pretty print xml
xml = md.parse(ev_manifest)
with open(ev_manifest, 'w') as f:
    f.write(xml.toprettyxml())
# write unique projects
with open('ev_unique.txt','w') as f:
    for r in sorted(ev_unique_remapped):
        f.write(r+"\n")



# create manifest for shared projects
ev_manifest = "shared.xml"
root = ET.Element("manifest")
#ET.SubElement(root, "remote", name="%s" % r, remote="%s" % def_remote, fetch="%s" % def_fetch_url)
for r in shared:
    ET.SubElement(root,"remove-project", name=r)
    ET.SubElement(root,"project", name=ev_mapping_rev_dict.get(r),
            remote=def_remote, revision=ev_repos_branches.get(ev_mapping_rev_dict.get(r)))

tree = ET.ElementTree(root)
tree.write(ev_manifest, encoding="UTF-8", xml_declaration=True)
# Pretty print xml
xml = md.parse(ev_manifest)
with open(ev_manifest, 'w') as f:
    f.write(xml.toprettyxml())

# write shared projects
import json
shared_json = {}
for s in shared:
    shared_json[s] = ev_mapping_rev_dict.get(s)
with open('shared.json','w') as f:
    json.dump(shared_json,f,indent=2)
with open('shared.txt','w') as f:
    for s in sorted(shared):
        f.write(s+"\n")
shared_remapped = []
for s in shared:
    shared_remapped.append(ev_mapping_rev_dict.get(s))
with open('shared-remapped.txt','w') as f:
    for s in sorted(shared_remapped):
        f.write(s+"\n")

# For setting up combined mirror
# Dont use keeping as reference
symlinks = False
if symlinks:
    failed = []
    # Create symbolic links for ev shared projects
    # to the aosp naming so --reference will work correctly
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

# could possibly be "." if mirrored in same directory
local_mirror_base_path = "/opt/storage/git/android/mirrors"
# aosp clone
aosp_mirror_path = os.path.join(local_mirror_base_path,"aosp")
# evervolv clone
evervolv_mirror_path = os.path.join(local_mirror_base_path,"evervolv")
# here we are adding the local aosp clone as remotes for the evervolv clone
# this way when aosp updates we only have to download it once
# when we update evervolv we only need to update the aosp remoet first
# then repo sync wont need to pull it from network
os.chdir(evervolv_mirror_path)
remotes = False
if remotes:
    cur_dir = os.getcwd()
    for s in shared:
        evproject = ev_mapping_rev_dict.get(s)
        os.chdir(evproject+".git")
        print "adding local aosp remote to" , evproject
        subprocess.call(['git','remote','add','aosp',"%s/%s.git" %(aosp_mirror_path,s)])
        print "fixing remote to pull to aosp/*"
        subprocess.call(['git','config','remote.aosp.fetch','+refs/heads/*:refs/heads/aosp/*'])
        os.chdir(cur_dir)
print "DONE"
