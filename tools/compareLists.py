import os
import sys


files_A = []
files_B = []

f = open(sys.argv[1], 'r')
lines = f.read().splitlines()
for line in lines:
    # skip comment lines
    if line.strip().startswith('#'):
        continue
    files_A.append(line)
f.close()

f = open(sys.argv[2], 'r')
lines = f.read().splitlines()
for line in lines:
    # skip comment lines
    if line.strip().startswith('#'):
        continue
    files_B.append(line)
f.close()

o_txt = open('1st_not_in_2nd.txt', 'w')
for f in files_A:
    if f not in files_B:
        print(f"File {f} from the 1st file not present in the 2nd")
        o_txt.write(f'{f}\n')
o_txt.close()

o_txt = open('2nd_not_in_1st.txt', 'w')
for f in files_B:
    if f not in files_A:
        print(f"File {f} from the 2nd file not present in the 1st")
        o_txt.write(f'{f}\n')
o_txt.close()
