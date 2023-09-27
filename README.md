# Installation (Lorien)
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc10
cmsrel CMSSW_12_3_0
cd CMSSW_12_3_0
cmsenv
cd ..
python3 -m venv H3env
source H3env/bin/activate
git clone git@github.com:CMS-H3PO/H3PO.git
pip install -r H3PO/requirements.txt
```
Setup environment
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd CMSSW_12_3_0
cmsenv
cd ..
source H3env/bin/activate
cd H3PO
```

# Running the notebooks from a server

On a server
```
cd H3PO
jupyter notebook --no-browser --port=8889 #Output shows the token which may be necessary to provide in browser on first connection
```
On a local machine
```
ssh -N -f -L localhost:8888:localhost:8889 USER@SERVER
http://localhost:8888 #type this in a browser
```
