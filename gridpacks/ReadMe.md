The official Run 2 `XToYHTo6B` samples
```
/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM
/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM
/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM
/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM
```
do not include the following mass points
```
(mX, mY) = (2500, 2300), (3500, 3000), (3500, 3300), (4000, 3000), (4000, 3500), (4000, 3800)
```
Below are the steps to produce missing MadGraph gridpacks for these mass points:
```
git clone -b mg265UL --depth=1 https://github.com/cms-sw/genproductions.git genprod_mg265UL_slc7
python makeDatacards.py
python makeGridpacks.py
```
