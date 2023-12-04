import sys


samples = set()
with open(sys.argv[1], 'r') as files:
    for f in files.read().splitlines():
        # skip comment lines
        if f.strip().startswith('#'):
            continue
        #print(f)
        spl = f.split('_')
        samples.add( (int(spl[2].split('-')[1]), int(spl[3].split('-')[1])) )

samples = sorted(samples)
print(samples)
