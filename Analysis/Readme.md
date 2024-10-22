# Files:

skimming.py - perform a loose selection on the files and store "skimmed" files. Execution time of the selection script is significantly reduced if skims are used as input\
Selection.py - implements all the selection

HHH_samples_2016.txt - Official sample list of 2016 NanoAOD XToYHTo6B signal samples\
HHH_samples_2016APV.txt - Official sample list of 2016APV NanoAOD XToYHTo6B signal samples\
HHH_samples_2017.txt - Official sample list of 2017 NanoAOD XToYHTo6B samples\
HHH_samples_2018.txt - Official sample list of 2018 NanoAOD XToYHTo6B samples

The above sample lists were obtained using the following commands (requires initialized GRID proxy [*])
```
echo '# dasgoclient -query "dataset dataset=/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM" | sort -V' > HHH_samples_2016.txt
dasgoclient -query "dataset dataset=/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM" | sort -V >> HHH_samples_2016.txt
echo '# dasgoclient -query "dataset dataset=/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM" | sort -V' > HHH_samples_2016APV.txt
dasgoclient -query "dataset dataset=/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM" | sort -V >> HHH_samples_2016APV.txt
echo '# dasgoclient -query "dataset dataset=/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM" | sort -V' > HHH_samples_2017.txt
dasgoclient -query "dataset dataset=/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM" | sort -V >> HHH_samples_2017.txt
echo '# dasgoclient -query "dataset dataset=/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM" | sort -V' > HHH_samples_2018.txt
dasgoclient -query "dataset dataset=/NMSSM_XToYHTo6B_MX-*_MY-*_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM" | sort -V >> HHH_samples_2018.txt
```

The sample lists were then used to generate lists of all signal files (requires initialized GRID proxy [*])
```
python ../tools/makeFileList.py HHH_samples_2016.txt HHH_files_2016.txt
python ../tools/makeFileList.py HHH_samples_2016APV.txt HHH_files_2016APV.txt
python ../tools/makeFileList.py HHH_samples_2017.txt HHH_files_2017.txt
python ../tools/makeFileList.py HHH_samples_2018.txt HHH_files_2018.txt
```

The above file lists were used to transfer signal files to the local cluster (requires initialized GRID proxy [*])
```
python ../tools/transfer_XRootD2RBI_HHH.py HHH_files_2016.txt 2016
python ../tools/transfer_XRootD2RBI_HHH.py HHH_files_2016APV.txt 2016APV
python ../tools/transfer_XRootD2RBI_HHH.py HHH_files_2017.txt 2017
python ../tools/transfer_XRootD2RBI_HHH.py HHH_files_2018.txt 2018
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

Submit Condor jobs
```
python condor_selection.py -y 2016 -o ~/HHH/condor_jobs_2016_SDmass_DeepJet -m 4000 -j nominal -t PFHT900 PFJet450 -d JetHT TTbar XToYHTo6B_MX-1000_MY-300 XToYHTo6B_MX-1000_MY-600 XToYHTo6B_MX-1000_MY-800 XToYHTo6B_MX-1200_MY-300 XToYHTo6B_MX-1200_MY-600 XToYHTo6B_MX-1200_MY-800 XToYHTo6B_MX-1200_MY-1000 XToYHTo6B_MX-1600_MY-300 XToYHTo6B_MX-1600_MY-600 XToYHTo6B_MX-1600_MY-800 XToYHTo6B_MX-1600_MY-1000 XToYHTo6B_MX-1600_MY-1200 XToYHTo6B_MX-1600_MY-1400 XToYHTo6B_MX-2000_MY-300 XToYHTo6B_MX-2000_MY-600 XToYHTo6B_MX-2000_MY-800 XToYHTo6B_MX-2000_MY-1000 XToYHTo6B_MX-2000_MY-1200 XToYHTo6B_MX-2000_MY-1600 XToYHTo6B_MX-2000_MY-1800 XToYHTo6B_MX-2500_MY-300 XToYHTo6B_MX-2500_MY-600 XToYHTo6B_MX-2500_MY-800 XToYHTo6B_MX-2500_MY-1000 XToYHTo6B_MX-2500_MY-1200 XToYHTo6B_MX-2500_MY-1600 XToYHTo6B_MX-2500_MY-2000 XToYHTo6B_MX-2500_MY-2200 XToYHTo6B_MX-3000_MY-300 XToYHTo6B_MX-3000_MY-600 XToYHTo6B_MX-3000_MY-800 XToYHTo6B_MX-3000_MY-1000 XToYHTo6B_MX-3000_MY-1200 XToYHTo6B_MX-3000_MY-1600 XToYHTo6B_MX-3000_MY-2000 XToYHTo6B_MX-3000_MY-2500 XToYHTo6B_MX-3000_MY-2800 XToYHTo6B_MX-3500_MY-300 XToYHTo6B_MX-3500_MY-600 XToYHTo6B_MX-3500_MY-800 XToYHTo6B_MX-3500_MY-1000 XToYHTo6B_MX-3500_MY-1200 XToYHTo6B_MX-3500_MY-1600 XToYHTo6B_MX-3500_MY-2000 XToYHTo6B_MX-3500_MY-2500 XToYHTo6B_MX-3500_MY-2800 XToYHTo6B_MX-4000_MY-300 XToYHTo6B_MX-4000_MY-600 XToYHTo6B_MX-4000_MY-800 XToYHTo6B_MX-4000_MY-1000 XToYHTo6B_MX-4000_MY-1200 XToYHTo6B_MX-4000_MY-1600 XToYHTo6B_MX-4000_MY-2000 XToYHTo6B_MX-4000_MY-2500 XToYHTo6B_MX-4000_MY-2800
```
```
python condor_selection.py -y 2016APV -o ~/HHH/condor_jobs_2016APV_SDmass_DeepJet -m 4000 -j nominal -t PFHT900 PFJet450 -d JetHT TTbar XToYHTo6B_MX-1000_MY-300 XToYHTo6B_MX-1000_MY-600 XToYHTo6B_MX-1000_MY-800 XToYHTo6B_MX-1200_MY-300 XToYHTo6B_MX-1200_MY-600 XToYHTo6B_MX-1200_MY-800 XToYHTo6B_MX-1200_MY-1000 XToYHTo6B_MX-1600_MY-300 XToYHTo6B_MX-1600_MY-600 XToYHTo6B_MX-1600_MY-800 XToYHTo6B_MX-1600_MY-1000 XToYHTo6B_MX-1600_MY-1200 XToYHTo6B_MX-1600_MY-1400 XToYHTo6B_MX-2000_MY-300 XToYHTo6B_MX-2000_MY-600 XToYHTo6B_MX-2000_MY-800 XToYHTo6B_MX-2000_MY-1000 XToYHTo6B_MX-2000_MY-1200 XToYHTo6B_MX-2000_MY-1600 XToYHTo6B_MX-2000_MY-1800 XToYHTo6B_MX-2500_MY-300 XToYHTo6B_MX-2500_MY-600 XToYHTo6B_MX-2500_MY-800 XToYHTo6B_MX-2500_MY-1000 XToYHTo6B_MX-2500_MY-1200 XToYHTo6B_MX-2500_MY-1600 XToYHTo6B_MX-2500_MY-2000 XToYHTo6B_MX-2500_MY-2200 XToYHTo6B_MX-3000_MY-300 XToYHTo6B_MX-3000_MY-600 XToYHTo6B_MX-3000_MY-800 XToYHTo6B_MX-3000_MY-1000 XToYHTo6B_MX-3000_MY-1200 XToYHTo6B_MX-3000_MY-1600 XToYHTo6B_MX-3000_MY-2000 XToYHTo6B_MX-3000_MY-2500 XToYHTo6B_MX-3000_MY-2800 XToYHTo6B_MX-3500_MY-300 XToYHTo6B_MX-3500_MY-600 XToYHTo6B_MX-3500_MY-800 XToYHTo6B_MX-3500_MY-1000 XToYHTo6B_MX-3500_MY-1200 XToYHTo6B_MX-3500_MY-1600 XToYHTo6B_MX-3500_MY-2000 XToYHTo6B_MX-3500_MY-2500 XToYHTo6B_MX-3500_MY-2800 XToYHTo6B_MX-4000_MY-300 XToYHTo6B_MX-4000_MY-600 XToYHTo6B_MX-4000_MY-800 XToYHTo6B_MX-4000_MY-1000 XToYHTo6B_MX-4000_MY-1200 XToYHTo6B_MX-4000_MY-1600 XToYHTo6B_MX-4000_MY-2000 XToYHTo6B_MX-4000_MY-2500 XToYHTo6B_MX-4000_MY-2800
```
```
python condor_selection.py -y 2017 -o ~/HHH/condor_jobs_2017_SDmass_DeepJet -m 4000 -j nominal -t PFHT1050 AK8PFJet500 PFJet500 -d JetHT TTbar XToYHTo6B_MX-1000_MY-300 XToYHTo6B_MX-1000_MY-600 XToYHTo6B_MX-1000_MY-800 XToYHTo6B_MX-1200_MY-300 XToYHTo6B_MX-1200_MY-600 XToYHTo6B_MX-1200_MY-800 XToYHTo6B_MX-1200_MY-1000 XToYHTo6B_MX-1600_MY-300 XToYHTo6B_MX-1600_MY-600 XToYHTo6B_MX-1600_MY-800 XToYHTo6B_MX-1600_MY-1000 XToYHTo6B_MX-1600_MY-1200 XToYHTo6B_MX-1600_MY-1400 XToYHTo6B_MX-2000_MY-300 XToYHTo6B_MX-2000_MY-600 XToYHTo6B_MX-2000_MY-800 XToYHTo6B_MX-2000_MY-1000 XToYHTo6B_MX-2000_MY-1200 XToYHTo6B_MX-2000_MY-1600 XToYHTo6B_MX-2000_MY-1800 XToYHTo6B_MX-2500_MY-300 XToYHTo6B_MX-2500_MY-600 XToYHTo6B_MX-2500_MY-800 XToYHTo6B_MX-2500_MY-1000 XToYHTo6B_MX-2500_MY-1200 XToYHTo6B_MX-2500_MY-1600 XToYHTo6B_MX-2500_MY-2000 XToYHTo6B_MX-2500_MY-2200 XToYHTo6B_MX-3000_MY-300 XToYHTo6B_MX-3000_MY-600 XToYHTo6B_MX-3000_MY-800 XToYHTo6B_MX-3000_MY-1000 XToYHTo6B_MX-3000_MY-1200 XToYHTo6B_MX-3000_MY-1600 XToYHTo6B_MX-3000_MY-2000 XToYHTo6B_MX-3000_MY-2500 XToYHTo6B_MX-3000_MY-2800 XToYHTo6B_MX-3500_MY-300 XToYHTo6B_MX-3500_MY-600 XToYHTo6B_MX-3500_MY-800 XToYHTo6B_MX-3500_MY-1000 XToYHTo6B_MX-3500_MY-1200 XToYHTo6B_MX-3500_MY-1600 XToYHTo6B_MX-3500_MY-2000 XToYHTo6B_MX-3500_MY-2500 XToYHTo6B_MX-3500_MY-2800 XToYHTo6B_MX-4000_MY-300 XToYHTo6B_MX-4000_MY-600 XToYHTo6B_MX-4000_MY-800 XToYHTo6B_MX-4000_MY-1000 XToYHTo6B_MX-4000_MY-1200 XToYHTo6B_MX-4000_MY-1600 XToYHTo6B_MX-4000_MY-2000 XToYHTo6B_MX-4000_MY-2500 XToYHTo6B_MX-4000_MY-2800
```
```
python condor_selection.py -y 2018 -o ~/HHH/condor_jobs_2018_SDmass_DeepJet -m 4000 -j nominal -t PFHT1050 AK8PFJet500 PFJet500 -d JetHT TTbar XToYHTo6B_MX-1000_MY-300 XToYHTo6B_MX-1000_MY-600 XToYHTo6B_MX-1000_MY-800 XToYHTo6B_MX-1200_MY-300 XToYHTo6B_MX-1200_MY-600 XToYHTo6B_MX-1200_MY-800 XToYHTo6B_MX-1200_MY-1000 XToYHTo6B_MX-1600_MY-300 XToYHTo6B_MX-1600_MY-600 XToYHTo6B_MX-1600_MY-800 XToYHTo6B_MX-1600_MY-1000 XToYHTo6B_MX-1600_MY-1200 XToYHTo6B_MX-1600_MY-1400 XToYHTo6B_MX-2000_MY-300 XToYHTo6B_MX-2000_MY-600 XToYHTo6B_MX-2000_MY-800 XToYHTo6B_MX-2000_MY-1000 XToYHTo6B_MX-2000_MY-1200 XToYHTo6B_MX-2000_MY-1600 XToYHTo6B_MX-2000_MY-1800 XToYHTo6B_MX-2500_MY-300 XToYHTo6B_MX-2500_MY-600 XToYHTo6B_MX-2500_MY-800 XToYHTo6B_MX-2500_MY-1000 XToYHTo6B_MX-2500_MY-1200 XToYHTo6B_MX-2500_MY-1600 XToYHTo6B_MX-2500_MY-2000 XToYHTo6B_MX-2500_MY-2200 XToYHTo6B_MX-3000_MY-300 XToYHTo6B_MX-3000_MY-600 XToYHTo6B_MX-3000_MY-800 XToYHTo6B_MX-3000_MY-1000 XToYHTo6B_MX-3000_MY-1200 XToYHTo6B_MX-3000_MY-1600 XToYHTo6B_MX-3000_MY-2000 XToYHTo6B_MX-3000_MY-2500 XToYHTo6B_MX-3000_MY-2800 XToYHTo6B_MX-3500_MY-300 XToYHTo6B_MX-3500_MY-600 XToYHTo6B_MX-3500_MY-800 XToYHTo6B_MX-3500_MY-1000 XToYHTo6B_MX-3500_MY-1200 XToYHTo6B_MX-3500_MY-1600 XToYHTo6B_MX-3500_MY-2000 XToYHTo6B_MX-3500_MY-2500 XToYHTo6B_MX-3500_MY-2800 XToYHTo6B_MX-4000_MY-300 XToYHTo6B_MX-4000_MY-600 XToYHTo6B_MX-4000_MY-800 XToYHTo6B_MX-4000_MY-1000 XToYHTo6B_MX-4000_MY-1200 XToYHTo6B_MX-4000_MY-1600 XToYHTo6B_MX-4000_MY-2000 XToYHTo6B_MX-4000_MY-2500 XToYHTo6B_MX-4000_MY-2800
```
Once all jobs complete successfully, the following 4 steps need to be done for each year:
```
export YEAR=2016
export TIMESTAMP=20240826_152342
```
1) Create a symbolic link to the output directory to make the commands that follow more generic
```
ln -sfnv condor_jobs_${YEAR}_PNmass_DeepJet_${TIMESTAMP} ~/HHH/condor_jobs_${YEAR}_latest
```
2) Combine output files
```
python combine_histograms.py -y ${YEAR} -i ~/HHH/condor_jobs_${YEAR}_latest -p JetHT TTbar XToYHTo6B_MX-1000_MY-300 XToYHTo6B_MX-1000_MY-600 XToYHTo6B_MX-1000_MY-800 XToYHTo6B_MX-1200_MY-300 XToYHTo6B_MX-1200_MY-600 XToYHTo6B_MX-1200_MY-800 XToYHTo6B_MX-1200_MY-1000 XToYHTo6B_MX-1600_MY-300 XToYHTo6B_MX-1600_MY-600 XToYHTo6B_MX-1600_MY-800 XToYHTo6B_MX-1600_MY-1000 XToYHTo6B_MX-1600_MY-1200 XToYHTo6B_MX-1600_MY-1400 XToYHTo6B_MX-2000_MY-300 XToYHTo6B_MX-2000_MY-600 XToYHTo6B_MX-2000_MY-800 XToYHTo6B_MX-2000_MY-1000 XToYHTo6B_MX-2000_MY-1200 XToYHTo6B_MX-2000_MY-1600 XToYHTo6B_MX-2000_MY-1800 XToYHTo6B_MX-2500_MY-300 XToYHTo6B_MX-2500_MY-600 XToYHTo6B_MX-2500_MY-800 XToYHTo6B_MX-2500_MY-1000 XToYHTo6B_MX-2500_MY-1200 XToYHTo6B_MX-2500_MY-1600 XToYHTo6B_MX-2500_MY-2000 XToYHTo6B_MX-2500_MY-2200 XToYHTo6B_MX-3000_MY-300 XToYHTo6B_MX-3000_MY-600 XToYHTo6B_MX-3000_MY-800 XToYHTo6B_MX-3000_MY-1000 XToYHTo6B_MX-3000_MY-1200 XToYHTo6B_MX-3000_MY-1600 XToYHTo6B_MX-3000_MY-2000 XToYHTo6B_MX-3000_MY-2500 XToYHTo6B_MX-3000_MY-2800 XToYHTo6B_MX-3500_MY-300 XToYHTo6B_MX-3500_MY-600 XToYHTo6B_MX-3500_MY-800 XToYHTo6B_MX-3500_MY-1000 XToYHTo6B_MX-3500_MY-1200 XToYHTo6B_MX-3500_MY-1600 XToYHTo6B_MX-3500_MY-2000 XToYHTo6B_MX-3500_MY-2500 XToYHTo6B_MX-3500_MY-2800 XToYHTo6B_MX-4000_MY-300 XToYHTo6B_MX-4000_MY-600 XToYHTo6B_MX-4000_MY-800 XToYHTo6B_MX-4000_MY-1000 XToYHTo6B_MX-4000_MY-1200 XToYHTo6B_MX-4000_MY-1600 XToYHTo6B_MX-4000_MY-2000 XToYHTo6B_MX-4000_MY-2500 XToYHTo6B_MX-4000_MY-2800
```
3) Produce unnormalized histograms for one signal sample for plotting the cut flow
```
source produceUnnormalized
```
4) Copy output files to a central location
```
source copyOutput
```
Repeat the above 4 steps for the remaining years
```
export YEAR=2016APV
export TIMESTAMP=20240826_152401
```
```
export YEAR=2017
export TIMESTAMP=20240826_152426
```
```
export YEAR=2018
export TIMESTAMP=20240826_152514
```
Finally, combine files from all the years
```
python combine_years.py -y 2016 2016APV 2017 2018 -s SDmass
```
By default, the combined filed will be stored in `/STORE/HHH/Histograms/Run2/latest/`. To see all available command-line options, run
```
python combine_years.py -h
```

[*] `voms-proxy-init -rfc -voms cms -valid 168:00`
