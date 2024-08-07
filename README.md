# Installation (Lorien)

The following steps need to be done only once for the initial installation
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=el9_amd64_gcc11
cmsrel CMSSW_13_0_2
cd CMSSW_13_0_2
cmsenv
cd -

python3 -m venv H3env
source H3env/bin/activate
git clone git@github.com:CMS-H3PO/H3PO.git
cd H3PO
pip3 install -r requirements.txt
```
You now have all the required software installed and the enviroment set up.

To set up environment in a new shell, run the following
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd CMSSW_13_0_2
cmsenv
cd -
source H3env/bin/activate
cd H3PO
```
or alternatively just run
```
source H3PO/activate_env
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
