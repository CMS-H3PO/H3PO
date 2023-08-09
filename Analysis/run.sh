#!/bin/bash                                                                                                                                                             
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /users/bchitrod/git_HHH/CMSSW_12_3_0/
eval `scramv1 runtime -sh`
cd /users/bchitrod/git_HHH/
source H3env/bin/activate

export WORK_DIR=/users/bchitrod/git_HHH/H3PO/Analysis/
cd /users/bchitrod/git_HHH/H3PO/Analysis/

echo $WORK_DIR/Mjj_Mjjj.py $*
python $WORK_DIR/Mjj_Mjjj.py $*
