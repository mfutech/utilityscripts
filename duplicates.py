#!/usr/bin/env python3
"""
duplicate.py

scan current folder for all files, make a sha1sum of each file
print out all file with the same sha1

2020 mfutech@gmail.com 
"""

import os
import sys
import hashlib
import re

DUPDIR="Duplicates"

def hash_file ( filename ):
    """ hash file 'filename', return a sha1 object
    """
    sha1 = hashlib.sha1()
    with open( filename, 'rb' ) as f:
        while True:
            buf = f.read(65536) # read by 64kb buffers size
            if not buf:
                break
            sha1.update(buf)
    return sha1

duplicateFiles = {}
reTrashDir = re.compile (f'.*/{DUPDIR}')

for dirName, subDir, files in os.walk('.'):

    # walk through all dir, but skip "Trash folders"
    if reTrashDir.match(dirName):
        print ( f"Skipping {dirName}")
        continue

    print ( f"Processing '{dirName}' ... ", end="")
    # for each file, push hash to list of files, by hash
    for f in files:
        fname = os.path.join(dirName, f)
        h = hash_file(fname)
        hx = h.hexdigest()
        if hx in duplicateFiles:
            duplicateFiles[hx].append(fname)
        else:
            duplicateFiles[hx] = [ fname ]
    print ("done\n")

with open('rmscript.sh', 'w') as rmscript:
    # create 'rmscript.sh' that will move all file to the Trash folder
    rmscript.write(f"mkdir -p {DUPDIR}\n")
    for hx in duplicateFiles:
        files = duplicateFiles[hx]
        if len(files) > 1:
            # if more that one file for that hash, select first to keep 
            # propose all other to move to Trash folder
            files.sort()
            keep = files.pop()
            print (f"{hx}:")
            print (f"\tkeep: {keep}")
            for f in files:
                print (f"\tremove {f}")
                rmscript.write(f'mv "{f}" {DUPDIR}\n')




