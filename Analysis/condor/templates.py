from paths import CMSSW_DIR, H3_DIR, H3ENV_DIR

selection_condor = """universe              = vanilla
executable            = EXEC
output                = OUTPUT/output_JOB.out
error                 = OUTPUT/output_JOB.err
log                   = OUTPUT/output_JOB.log
RequestMemory = 15000
Arguments = "ARGS"
use_x509userproxy = true
queue
"""

skim_template='''#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd {0}
eval `scramv1 runtime -sh`
cd {1}
source H3env/bin/activate

export WORK_DIR={2}
cd JOB_DIR

echo $WORK_DIR/skimming.py $*
python $WORK_DIR/skimming.py $*
'''.format(CMSSW_DIR,H3ENV_DIR,H3_DIR)
