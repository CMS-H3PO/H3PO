import os
import sys

# this script works with Python 3
# execute 'voms-proxy-init -rfc -voms cms -valid 168:00' before running the script

# open a file containing a list of datasets
s_txt = open(sys.argv[1], 'r')
samples = s_txt.read().splitlines()
s_txt.close()

o = sys.argv[2]

for s in samples:
    # skip comment lines
    if s.strip().startswith('#'):
        continue

    print(f'Processing {s}')

    cmd = f'dasgoclient -query "file dataset={s}" >> {o}'
    #print(cmd)
    os.system(cmd)
