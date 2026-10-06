#!/bin/bash                                                                                                                                                             

export WORK_DIR=$PWD

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd $WORK_DIR/../../CMSSW_15_0_21/
eval `scramv1 runtime -sh`
cd ..
source H3env/bin/activate
cd $WORK_DIR

echo $WORK_DIR/Runner.py $*
python -u $WORK_DIR/Runner.py $*
