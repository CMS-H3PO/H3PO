#!/bin/bash                                                                                                                                                             

export WORK_DIR=$PWD

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd $WORK_DIR/../../CMSSW_12_3_0/
eval `scramv1 runtime -sh`
cd ..
source H3env/bin/activate
cd $WORK_DIR

echo $WORK_DIR/Mjj_Mjjj_Signal.py $*
python $WORK_DIR/Mjj_Mjjj_Signal.py $*
