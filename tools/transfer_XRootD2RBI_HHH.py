import os
import sys
import subprocess
from datetime import datetime

# this script works with Python 3
# execute 'voms-proxy-init -rfc -voms cms -valid 168:00' before running the script

# open a file containing a list of remote files
r_txt = open(sys.argv[1], 'r')
remote_files = r_txt.read().splitlines()
r_txt.close()

#for r in remote_files:
    #print (r)

year = sys.argv[2]

t_txt = open(f'transferred_files_{year}.txt', 'a+')
t_txt.seek(0)
transferred_files = t_txt.read().splitlines()

#for t in transferred_files:
    #print (t)

print(datetime.now())

for r in remote_files:
    # skip file if already transferred
    if r in transferred_files:
      print(f'{r} already transferred')
      continue
  
    split = r.split('_')
    #print(split[2])
    #print(split[3])
    mx = split[2]
    my = split[3]
    
    dest = f'/STORE/HHH/skims/{year}/XToYHTo6B_{mx}_{my}'
    
    if not os.path.exists(dest):
        cmd = f"mkdir -p {dest}"
        print('\n' + cmd)
        os.system(cmd)

    dest_file = os.path.join(dest, os.path.basename(r))
    if os.path.exists(dest_file):
        print(f"{dest_file} already exists, skipping")
        continue

    cmd = f'xrdcp -f root://cms-xrd-global.cern.ch//{r} {dest}'
    print(cmd + '\n')
    # use system-installed xrdcp in a clean shell environment
    result = subprocess.run(cmd.split(), env={})
    if result.returncode == 0:
        t_txt.write(f'{r}\n')
    print(datetime.now())

t_txt.close()

print("\nTransfer done!")
