import os

#Location of the H3env environment
H3ENV_DIR           = os.path.dirname(os.path.abspath(__file__)).replace("/H3PO/Analysis/condor", "")
#Location of the main H3PO Analysis directory
H3_DIR              = os.path.join(H3ENV_DIR, "H3PO/Analysis")
#Where to store condor logs for skimming jobs
SKIM_JOB_DIR        = os.path.join(H3_DIR, "condor/skim_jobs")
#Location of the CMSSW dir
CMSSW_DIR           = os.path.join(H3ENV_DIR, "CMSSW_13_0_2")
#Where to store skimmed NanoAODs
SKIM_DIR            = "/STORE/matej/H3_skims/"
