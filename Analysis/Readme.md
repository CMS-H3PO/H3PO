# Files:

`skimming.py` - perform a loose selection on the files and store "skimmed" files. Execution time of the selection script is significantly reduced if skims are used as input\
`Selection.py` - implements all the selection

`../data/HHH_samples_2016.txt` - Official sample list of 2016 NanoAOD XToYHTo6B signal samples\
`../data/HHH_samples_2016APV.txt` - Official sample list of 2016APV NanoAOD XToYHTo6B signal samples\
`../data/HHH_samples_2017.txt` - Official sample list of 2017 NanoAOD XToYHTo6B samples\
`../data/HHH_samples_2018.txt` - Official sample list of 2018 NanoAOD XToYHTo6B samples

The above sample lists were obtained using the following commands (requires initialized GRID proxy [*])
```
echo '# dasgoclient -query "dataset dataset=/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v*/NANOAODSIM" | sort -V' > ../data/HHH_samples_2016.txt
dasgoclient -query "dataset dataset=/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v*/NANOAODSIM" | sort -V >> ../data/HHH_samples_2016.txt
echo '# dasgoclient -query "dataset dataset=/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v*/NANOAODSIM" | sort -V' > ../data/HHH_samples_2016APV.txt
dasgoclient -query "dataset dataset=/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v*/NANOAODSIM" | sort -V >> ../data/HHH_samples_2016APV.txt
echo '# dasgoclient -query "dataset dataset=/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v*/NANOAODSIM" | sort -V' > ../data/HHH_samples_2017.txt
dasgoclient -query "dataset dataset=/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v*/NANOAODSIM" | sort -V >> ../data/HHH_samples_2017.txt
echo '# dasgoclient -query "dataset dataset=/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v*/NANOAODSIM" | sort -V' > ../data/HHH_samples_2018.txt
dasgoclient -query "dataset dataset=/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV_madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v*/NANOAODSIM" | sort -V >> ../data/HHH_samples_2018.txt
```

The sample lists were then used to generate lists of all signal files (requires initialized GRID proxy [*])
```
python ../tools/makeFileList.py ../data/HHH_samples_2016.txt ../data/HHH_files_2016.txt
python ../tools/makeFileList.py ../data/HHH_samples_2016APV.txt ../data/HHH_files_2016APV.txt
python ../tools/makeFileList.py ../data/HHH_samples_2017.txt ../data/HHH_files_2017.txt
python ../tools/makeFileList.py ../data/HHH_samples_2018.txt ../data/HHH_files_2018.txt
```

The above file lists were used to transfer signal files to the local cluster (requires initialized GRID proxy [*])
```
python ../tools/transfer_XRootD2RBI_HHH.py ../data/HHH_files_2016.txt 2016
python ../tools/transfer_XRootD2RBI_HHH.py ../data/HHH_files_2016APV.txt 2016APV
python ../tools/transfer_XRootD2RBI_HHH.py ../data/HHH_files_2017.txt 2017
python ../tools/transfer_XRootD2RBI_HHH.py ../data/HHH_files_2018.txt 2018
```

A single file can be skimmed as in the following example (requires initialized GRID proxy [*])
```
python skimming.py -i /store/mc/RunIISummer20UL16NanoAODAPVv9/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/2DD52229-3161-1C4D-9D73-B638B33B259C.root -o test_output
```

Large scale skimming of JetHT and TTbar datasets was done using the following commands:
```
cd condor/
python run_skim.py -c skim_configs/2016APV/mc.json -y 2016APV
python run_skim.py -c skim_configs/2016APV/data.json -y 2016APV
python run_skim.py -c skim_configs/2016/mc.json -y 2016
python run_skim.py -c skim_configs/2016/data.json -y 2016
python run_skim.py -c skim_configs/2017/mc.json -y 2017
python run_skim.py -c skim_configs/2017/data.json -y 2017
python run_skim.py -c skim_configs/2018/mc.json -y 2018
python run_skim.py -c skim_configs/2018/data.json -y 2018
```
Each of the above commands prints out `source` commands to be executed in order to submit skimming Condor jobs.


Additional skimming of QCD samples and SingleMuon primary datasets was done using the following commands:
```
python run_skim.py -c skim_configs/2016APV/qcd.json -y 2016APV
python run_skim.py -c skim_configs/2016APV/muon.json -y 2016APV
python run_skim.py -c skim_configs/2016/qcd.json -y 2016
python run_skim.py -c skim_configs/2016/muon.json -y 2016
python run_skim.py -c skim_configs/2017/qcd.json -y 2017
python run_skim.py -c skim_configs/2017/muon.json -y 2017
python run_skim.py -c skim_configs/2018/qcd.json -y 2018
python run_skim.py -c skim_configs/2018/muon.json -y 2018
```

# Make histograms with signal, backgrounds and data for SR (Signal Region) and VR (Validation Region):

To run over all 2017 samples:
```
python condor_selection.py -y 2017
```
This will submit jobs to Condor for all 2017 samples. Wait until all jobs are done. Output root files will be stored in `condor_jobs_<timestamp>` directory. To see all available command-line options, run
```
python condor_selection.py -h
```

To combine histograms:
```
python combine_histograms.py -i condor_jobs_<timestamp>
```
This will combine root files and store them in the `condor_jobs_<timestamp>/fit` subdirectory with intermediate files left in `condor_jobs_<timestamp>`. To see all available command-line options, run
```
python combine_histograms.py -h
```

# Example commands:

Commands from the last round of histogram production:

```
export SUFFIX="$(git rev-parse --short HEAD)"
export CONDOR_OUTPUT=~/HHH/Condor_jobs
```
Submit Condor jobs
```
python condor_selection.py -y 2016APV -o ${CONDOR_OUTPUT}/2016APV_${SUFFIX} -m 4000 -c all -s all -t PFHT900 PFJet450 -d JetHT TTbar XToYHTo6B_MX-1000_MY-300 XToYHTo6B_MX-1000_MY-600 XToYHTo6B_MX-1000_MY-800 XToYHTo6B_MX-1200_MY-300 XToYHTo6B_MX-1200_MY-600 XToYHTo6B_MX-1200_MY-800 XToYHTo6B_MX-1200_MY-1000 XToYHTo6B_MX-1600_MY-300 XToYHTo6B_MX-1600_MY-600 XToYHTo6B_MX-1600_MY-800 XToYHTo6B_MX-1600_MY-1000 XToYHTo6B_MX-1600_MY-1200 XToYHTo6B_MX-1600_MY-1400 XToYHTo6B_MX-2000_MY-300 XToYHTo6B_MX-2000_MY-600 XToYHTo6B_MX-2000_MY-800 XToYHTo6B_MX-2000_MY-1000 XToYHTo6B_MX-2000_MY-1200 XToYHTo6B_MX-2000_MY-1600 XToYHTo6B_MX-2000_MY-1800 XToYHTo6B_MX-2500_MY-300 XToYHTo6B_MX-2500_MY-600 XToYHTo6B_MX-2500_MY-800 XToYHTo6B_MX-2500_MY-1000 XToYHTo6B_MX-2500_MY-1200 XToYHTo6B_MX-2500_MY-1600 XToYHTo6B_MX-2500_MY-2000 XToYHTo6B_MX-2500_MY-2200 XToYHTo6B_MX-2500_MY-2300 XToYHTo6B_MX-3000_MY-300 XToYHTo6B_MX-3000_MY-600 XToYHTo6B_MX-3000_MY-800 XToYHTo6B_MX-3000_MY-1000 XToYHTo6B_MX-3000_MY-1200 XToYHTo6B_MX-3000_MY-1600 XToYHTo6B_MX-3000_MY-2000 XToYHTo6B_MX-3000_MY-2500 XToYHTo6B_MX-3000_MY-2800 XToYHTo6B_MX-3500_MY-300 XToYHTo6B_MX-3500_MY-600 XToYHTo6B_MX-3500_MY-800 XToYHTo6B_MX-3500_MY-1000 XToYHTo6B_MX-3500_MY-1200 XToYHTo6B_MX-3500_MY-1600 XToYHTo6B_MX-3500_MY-2000 XToYHTo6B_MX-3500_MY-2500 XToYHTo6B_MX-3500_MY-2800 XToYHTo6B_MX-3500_MY-3000 XToYHTo6B_MX-3500_MY-3300 XToYHTo6B_MX-4000_MY-300 XToYHTo6B_MX-4000_MY-600 XToYHTo6B_MX-4000_MY-800 XToYHTo6B_MX-4000_MY-1000 XToYHTo6B_MX-4000_MY-1200 XToYHTo6B_MX-4000_MY-1600 XToYHTo6B_MX-4000_MY-2000 XToYHTo6B_MX-4000_MY-2500 XToYHTo6B_MX-4000_MY-2800 XToYHTo6B_MX-4000_MY-3000 XToYHTo6B_MX-4000_MY-3500 XToYHTo6B_MX-4000_MY-3800 --date_only
```
```
python condor_selection.py -y 2016 -o ${CONDOR_OUTPUT}/2016_${SUFFIX} -m 4000 -c all -s all -t PFHT900 PFJet450 -d JetHT TTbar XToYHTo6B_MX-1000_MY-300 XToYHTo6B_MX-1000_MY-600 XToYHTo6B_MX-1000_MY-800 XToYHTo6B_MX-1200_MY-300 XToYHTo6B_MX-1200_MY-600 XToYHTo6B_MX-1200_MY-800 XToYHTo6B_MX-1200_MY-1000 XToYHTo6B_MX-1600_MY-300 XToYHTo6B_MX-1600_MY-600 XToYHTo6B_MX-1600_MY-800 XToYHTo6B_MX-1600_MY-1000 XToYHTo6B_MX-1600_MY-1200 XToYHTo6B_MX-1600_MY-1400 XToYHTo6B_MX-2000_MY-300 XToYHTo6B_MX-2000_MY-600 XToYHTo6B_MX-2000_MY-800 XToYHTo6B_MX-2000_MY-1000 XToYHTo6B_MX-2000_MY-1200 XToYHTo6B_MX-2000_MY-1600 XToYHTo6B_MX-2000_MY-1800 XToYHTo6B_MX-2500_MY-300 XToYHTo6B_MX-2500_MY-600 XToYHTo6B_MX-2500_MY-800 XToYHTo6B_MX-2500_MY-1000 XToYHTo6B_MX-2500_MY-1200 XToYHTo6B_MX-2500_MY-1600 XToYHTo6B_MX-2500_MY-2000 XToYHTo6B_MX-2500_MY-2200 XToYHTo6B_MX-2500_MY-2300 XToYHTo6B_MX-3000_MY-300 XToYHTo6B_MX-3000_MY-600 XToYHTo6B_MX-3000_MY-800 XToYHTo6B_MX-3000_MY-1000 XToYHTo6B_MX-3000_MY-1200 XToYHTo6B_MX-3000_MY-1600 XToYHTo6B_MX-3000_MY-2000 XToYHTo6B_MX-3000_MY-2500 XToYHTo6B_MX-3000_MY-2800 XToYHTo6B_MX-3500_MY-300 XToYHTo6B_MX-3500_MY-600 XToYHTo6B_MX-3500_MY-800 XToYHTo6B_MX-3500_MY-1000 XToYHTo6B_MX-3500_MY-1200 XToYHTo6B_MX-3500_MY-1600 XToYHTo6B_MX-3500_MY-2000 XToYHTo6B_MX-3500_MY-2500 XToYHTo6B_MX-3500_MY-2800 XToYHTo6B_MX-3500_MY-3000 XToYHTo6B_MX-3500_MY-3300 XToYHTo6B_MX-4000_MY-300 XToYHTo6B_MX-4000_MY-600 XToYHTo6B_MX-4000_MY-800 XToYHTo6B_MX-4000_MY-1000 XToYHTo6B_MX-4000_MY-1200 XToYHTo6B_MX-4000_MY-1600 XToYHTo6B_MX-4000_MY-2000 XToYHTo6B_MX-4000_MY-2500 XToYHTo6B_MX-4000_MY-2800 XToYHTo6B_MX-4000_MY-3000 XToYHTo6B_MX-4000_MY-3500 XToYHTo6B_MX-4000_MY-3800 --date_only
```
```
python condor_selection.py -y 2017 -o ${CONDOR_OUTPUT}/2017_${SUFFIX} -m 4000 -c all -s all -t PFHT1050 AK8PFJet500 PFJet500 -d JetHT TTbar XToYHTo6B_MX-1000_MY-300 XToYHTo6B_MX-1000_MY-600 XToYHTo6B_MX-1000_MY-800 XToYHTo6B_MX-1200_MY-300 XToYHTo6B_MX-1200_MY-600 XToYHTo6B_MX-1200_MY-800 XToYHTo6B_MX-1200_MY-1000 XToYHTo6B_MX-1600_MY-300 XToYHTo6B_MX-1600_MY-600 XToYHTo6B_MX-1600_MY-800 XToYHTo6B_MX-1600_MY-1000 XToYHTo6B_MX-1600_MY-1200 XToYHTo6B_MX-1600_MY-1400 XToYHTo6B_MX-2000_MY-300 XToYHTo6B_MX-2000_MY-600 XToYHTo6B_MX-2000_MY-800 XToYHTo6B_MX-2000_MY-1000 XToYHTo6B_MX-2000_MY-1200 XToYHTo6B_MX-2000_MY-1600 XToYHTo6B_MX-2000_MY-1800 XToYHTo6B_MX-2500_MY-300 XToYHTo6B_MX-2500_MY-600 XToYHTo6B_MX-2500_MY-800 XToYHTo6B_MX-2500_MY-1000 XToYHTo6B_MX-2500_MY-1200 XToYHTo6B_MX-2500_MY-1600 XToYHTo6B_MX-2500_MY-2000 XToYHTo6B_MX-2500_MY-2200 XToYHTo6B_MX-2500_MY-2300 XToYHTo6B_MX-3000_MY-300 XToYHTo6B_MX-3000_MY-600 XToYHTo6B_MX-3000_MY-800 XToYHTo6B_MX-3000_MY-1000 XToYHTo6B_MX-3000_MY-1200 XToYHTo6B_MX-3000_MY-1600 XToYHTo6B_MX-3000_MY-2000 XToYHTo6B_MX-3000_MY-2500 XToYHTo6B_MX-3000_MY-2800 XToYHTo6B_MX-3500_MY-300 XToYHTo6B_MX-3500_MY-600 XToYHTo6B_MX-3500_MY-800 XToYHTo6B_MX-3500_MY-1000 XToYHTo6B_MX-3500_MY-1200 XToYHTo6B_MX-3500_MY-1600 XToYHTo6B_MX-3500_MY-2000 XToYHTo6B_MX-3500_MY-2500 XToYHTo6B_MX-3500_MY-2800 XToYHTo6B_MX-3500_MY-3000 XToYHTo6B_MX-3500_MY-3300 XToYHTo6B_MX-4000_MY-300 XToYHTo6B_MX-4000_MY-600 XToYHTo6B_MX-4000_MY-800 XToYHTo6B_MX-4000_MY-1000 XToYHTo6B_MX-4000_MY-1200 XToYHTo6B_MX-4000_MY-1600 XToYHTo6B_MX-4000_MY-2000 XToYHTo6B_MX-4000_MY-2500 XToYHTo6B_MX-4000_MY-2800 XToYHTo6B_MX-4000_MY-3000 XToYHTo6B_MX-4000_MY-3500 XToYHTo6B_MX-4000_MY-3800 --date_only
```
```
python condor_selection.py -y 2018 -o ${CONDOR_OUTPUT}/2018_${SUFFIX} -m 4000 -c all -s all -t PFHT1050 AK8PFJet500 PFJet500 -d JetHT TTbar XToYHTo6B_MX-1000_MY-300 XToYHTo6B_MX-1000_MY-600 XToYHTo6B_MX-1000_MY-800 XToYHTo6B_MX-1200_MY-300 XToYHTo6B_MX-1200_MY-600 XToYHTo6B_MX-1200_MY-800 XToYHTo6B_MX-1200_MY-1000 XToYHTo6B_MX-1600_MY-300 XToYHTo6B_MX-1600_MY-600 XToYHTo6B_MX-1600_MY-800 XToYHTo6B_MX-1600_MY-1000 XToYHTo6B_MX-1600_MY-1200 XToYHTo6B_MX-1600_MY-1400 XToYHTo6B_MX-2000_MY-300 XToYHTo6B_MX-2000_MY-600 XToYHTo6B_MX-2000_MY-800 XToYHTo6B_MX-2000_MY-1000 XToYHTo6B_MX-2000_MY-1200 XToYHTo6B_MX-2000_MY-1600 XToYHTo6B_MX-2000_MY-1800 XToYHTo6B_MX-2500_MY-300 XToYHTo6B_MX-2500_MY-600 XToYHTo6B_MX-2500_MY-800 XToYHTo6B_MX-2500_MY-1000 XToYHTo6B_MX-2500_MY-1200 XToYHTo6B_MX-2500_MY-1600 XToYHTo6B_MX-2500_MY-2000 XToYHTo6B_MX-2500_MY-2200 XToYHTo6B_MX-2500_MY-2300 XToYHTo6B_MX-3000_MY-300 XToYHTo6B_MX-3000_MY-600 XToYHTo6B_MX-3000_MY-800 XToYHTo6B_MX-3000_MY-1000 XToYHTo6B_MX-3000_MY-1200 XToYHTo6B_MX-3000_MY-1600 XToYHTo6B_MX-3000_MY-2000 XToYHTo6B_MX-3000_MY-2500 XToYHTo6B_MX-3000_MY-2800 XToYHTo6B_MX-3500_MY-300 XToYHTo6B_MX-3500_MY-600 XToYHTo6B_MX-3500_MY-800 XToYHTo6B_MX-3500_MY-1000 XToYHTo6B_MX-3500_MY-1200 XToYHTo6B_MX-3500_MY-1600 XToYHTo6B_MX-3500_MY-2000 XToYHTo6B_MX-3500_MY-2500 XToYHTo6B_MX-3500_MY-2800 XToYHTo6B_MX-3500_MY-3000 XToYHTo6B_MX-3500_MY-3300 XToYHTo6B_MX-4000_MY-300 XToYHTo6B_MX-4000_MY-600 XToYHTo6B_MX-4000_MY-800 XToYHTo6B_MX-4000_MY-1000 XToYHTo6B_MX-4000_MY-1200 XToYHTo6B_MX-4000_MY-1600 XToYHTo6B_MX-4000_MY-2000 XToYHTo6B_MX-4000_MY-2500 XToYHTo6B_MX-4000_MY-2800 XToYHTo6B_MX-4000_MY-3000 XToYHTo6B_MX-4000_MY-3500 XToYHTo6B_MX-4000_MY-3800 --date_only
```
Once all jobs complete successfully, the following 4 steps need to be done for each year:
```
export TIMESTAMP=20260827
export YEAR=2016APV
```
1) Create a symbolic link to the output directory to make the commands that follow more generic
```
ln -sfnv ${YEAR}_${SUFFIX}_${TIMESTAMP} ${CONDOR_OUTPUT}/${YEAR}_latest
```
2) Combine output files
```
python combine_histograms.py -y ${YEAR} -i ${CONDOR_OUTPUT}/${YEAR}_latest -p JetHT TTbar XToYHTo6B_MX-1000_MY-300 XToYHTo6B_MX-1000_MY-600 XToYHTo6B_MX-1000_MY-800 XToYHTo6B_MX-1200_MY-300 XToYHTo6B_MX-1200_MY-600 XToYHTo6B_MX-1200_MY-800 XToYHTo6B_MX-1200_MY-1000 XToYHTo6B_MX-1600_MY-300 XToYHTo6B_MX-1600_MY-600 XToYHTo6B_MX-1600_MY-800 XToYHTo6B_MX-1600_MY-1000 XToYHTo6B_MX-1600_MY-1200 XToYHTo6B_MX-1600_MY-1400 XToYHTo6B_MX-2000_MY-300 XToYHTo6B_MX-2000_MY-600 XToYHTo6B_MX-2000_MY-800 XToYHTo6B_MX-2000_MY-1000 XToYHTo6B_MX-2000_MY-1200 XToYHTo6B_MX-2000_MY-1600 XToYHTo6B_MX-2000_MY-1800 XToYHTo6B_MX-2500_MY-300 XToYHTo6B_MX-2500_MY-600 XToYHTo6B_MX-2500_MY-800 XToYHTo6B_MX-2500_MY-1000 XToYHTo6B_MX-2500_MY-1200 XToYHTo6B_MX-2500_MY-1600 XToYHTo6B_MX-2500_MY-2000 XToYHTo6B_MX-2500_MY-2200 XToYHTo6B_MX-2500_MY-2300 XToYHTo6B_MX-3000_MY-300 XToYHTo6B_MX-3000_MY-600 XToYHTo6B_MX-3000_MY-800 XToYHTo6B_MX-3000_MY-1000 XToYHTo6B_MX-3000_MY-1200 XToYHTo6B_MX-3000_MY-1600 XToYHTo6B_MX-3000_MY-2000 XToYHTo6B_MX-3000_MY-2500 XToYHTo6B_MX-3000_MY-2800 XToYHTo6B_MX-3500_MY-300 XToYHTo6B_MX-3500_MY-600 XToYHTo6B_MX-3500_MY-800 XToYHTo6B_MX-3500_MY-1000 XToYHTo6B_MX-3500_MY-1200 XToYHTo6B_MX-3500_MY-1600 XToYHTo6B_MX-3500_MY-2000 XToYHTo6B_MX-3500_MY-2500 XToYHTo6B_MX-3500_MY-2800 XToYHTo6B_MX-3500_MY-3000 XToYHTo6B_MX-3500_MY-3300 XToYHTo6B_MX-4000_MY-300 XToYHTo6B_MX-4000_MY-600 XToYHTo6B_MX-4000_MY-800 XToYHTo6B_MX-4000_MY-1000 XToYHTo6B_MX-4000_MY-1200 XToYHTo6B_MX-4000_MY-1600 XToYHTo6B_MX-4000_MY-2000 XToYHTo6B_MX-4000_MY-2500 XToYHTo6B_MX-4000_MY-2800 XToYHTo6B_MX-4000_MY-3000 XToYHTo6B_MX-4000_MY-3500 XToYHTo6B_MX-4000_MY-3800
```
3) Copy output files to a central location
```
source copyOutput
```
Repeat the above steps for the remaining years
```
export YEAR=2016
```
```
export YEAR=2017
```
```
export YEAR=2018
```
Finally, combine files from all the years
```
python combine_years.py -y 2016APV 2016 2017 2018 -s ${SUFFIX} --date_only
```
By default, the combined files will be stored in `/STORE/HHH/Histograms/Run2/latest/`. To see all available command-line options, run
```
python combine_years.py -h
```

# Processing tips and tricks

If some jobs were held, check which ones by running
```
grep -ri held --include="*.log" ${CONDOR_OUTPUT}/*${TIMESTAMP}/ | sort -V
```
If you want to produce a list of job description files for the held jobs (for later use with sed or condor_submit commanda), run
```
grep -ri held --include="*.log" ${CONDOR_OUTPUT}/*${TIMESTAMP}/ | sort -V | cut -d: -f1 | sed 's|logs/tmp-|jobs/job_desc-|g' | sed 's|\.log|\.txt|g'
```
If some jobs were held again, check which ones by running
```
grep -ri held --include="*.log" ${CONDOR_OUTPUT}/*${TIMESTAMP}/ | sort -V | cut -d: -f1 | uniq -d
```
(grep for lines containing 'held'; keep only the file names; print only the duplicates)

If some jobs were held more than once, check which ones by running
```
grep -ri held --include="*.log" ${CONDOR_OUTPUT}/*${TIMESTAMP}/ | sort -V | cut -d: -f1 | uniq -d -c
```
(grep for lines containing 'held'; keep only the file names; print only the duplicates and prefix lines by the number of occurrences)

Remove jobs before resubmitting
```
condor_rm $USER
```
Example `sed` and `condor_submit` commands:
```
sed -i 's/RequestMemory = 4000/RequestMemory = 20000/g' ${CONDOR_OUTPUT}/${YEAR}_${SUFFIX}_${TIMESTAMP}/jobs/job_desc-XToYHTo6B_MX-1000_MY-600_0.txt
```
```
condor_submit ${CONDOR_OUTPUT}/${YEAR}_${SUFFIX}_${TIMESTAMP}/jobs/job_desc-XToYHTo6B_MX-1000_MY-600_0.txt
```

[*] `voms-proxy-init -rfc -voms cms -valid 168:00`
