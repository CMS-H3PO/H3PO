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

The above file lists were used to transfer files to the local cluster (requires initialized GRID proxy [*])
```
python3 ../tools/transfer_XRootD2RBI_HHH.py HHH_files_2016.txt 2016
python3 ../tools/transfer_XRootD2RBI_HHH.py HHH_files_2016APV.txt 2016APV
python3 ../tools/transfer_XRootD2RBI_HHH.py HHH_files_2017.txt 2017
python3 ../tools/transfer_XRootD2RBI_HHH.py HHH_files_2018.txt 2018
```

# Make histograms with signal, backgrounds and data for SR (Signal Region) and VR (Validation Region):

To run over all samples:
```
python condor_selection.py
```
This will submit jobs to condor for all the samples. Wait until all jobs are done. Output root files will be stored in ```condor_jobs_<timestamp>``` directory. To see all available command-line options, run
```
python condor_selection.py -h
```

To combine histograms:
```
python combine_histograms.py -i condor_jobs_<timestamp>
```
This will combine root files and store them in the ```condor_jobs_<timestamp>/fit``` subdirectory with intermediate files left in ```condor_jobs_<timestamp>```. To see all available command-line options, run
```
python combine_histograms.py -h
```

# Example commands:

GRID proxy needs to be initialized [*] before running skimming to access the file on the store
```
python skimming.py -i store/mc/RunIISummer20UL17NanoAODv9/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/NANOAODSIM/106X_mc2017_realistic_v9-v1/100000/D5426269-CD07-CA4C-8E9E-E2336514139F.root -o test_output
```

Commands from the last round of histogram production:

Submit Condor jobs
```
python condor_selection.py -o /users/ferencek/HHH/condor_jobs_data_background_signal -j nominal -t PFHT1050 AK8PFJet500 PFJet500 -d JetHT QCD TTbar XToYHTo6B_MX-1000_MY-300 XToYHTo6B_MX-1000_MY-600 XToYHTo6B_MX-1000_MY-800 XToYHTo6B_MX-1200_MY-300 XToYHTo6B_MX-1200_MY-600 XToYHTo6B_MX-1200_MY-800 XToYHTo6B_MX-1200_MY-1000 XToYHTo6B_MX-1600_MY-300 XToYHTo6B_MX-1600_MY-600 XToYHTo6B_MX-1600_MY-800 XToYHTo6B_MX-1600_MY-1000 XToYHTo6B_MX-1600_MY-1200 XToYHTo6B_MX-1600_MY-1400 XToYHTo6B_MX-2000_MY-300 XToYHTo6B_MX-2000_MY-600 XToYHTo6B_MX-2000_MY-800 XToYHTo6B_MX-2000_MY-1000 XToYHTo6B_MX-2000_MY-1200 XToYHTo6B_MX-2000_MY-1600 XToYHTo6B_MX-2000_MY-1800 XToYHTo6B_MX-2500_MY-300 XToYHTo6B_MX-2500_MY-600 XToYHTo6B_MX-2500_MY-800 XToYHTo6B_MX-2500_MY-1000 XToYHTo6B_MX-2500_MY-1200 XToYHTo6B_MX-2500_MY-1600 XToYHTo6B_MX-2500_MY-2000 XToYHTo6B_MX-2500_MY-2200 XToYHTo6B_MX-3000_MY-300 XToYHTo6B_MX-3000_MY-600 XToYHTo6B_MX-3000_MY-800 XToYHTo6B_MX-3000_MY-1000 XToYHTo6B_MX-3000_MY-1200 XToYHTo6B_MX-3000_MY-1600 XToYHTo6B_MX-3000_MY-2000 XToYHTo6B_MX-3000_MY-2500 XToYHTo6B_MX-3000_MY-2800 XToYHTo6B_MX-3500_MY-300 XToYHTo6B_MX-3500_MY-600 XToYHTo6B_MX-3500_MY-800 XToYHTo6B_MX-3500_MY-1000 XToYHTo6B_MX-3500_MY-1200 XToYHTo6B_MX-3500_MY-1600 XToYHTo6B_MX-3500_MY-2000 XToYHTo6B_MX-3500_MY-2500 XToYHTo6B_MX-3500_MY-2800 XToYHTo6B_MX-4000_MY-300 XToYHTo6B_MX-4000_MY-600 XToYHTo6B_MX-4000_MY-800 XToYHTo6B_MX-4000_MY-1000 XToYHTo6B_MX-4000_MY-1200 XToYHTo6B_MX-4000_MY-1600 XToYHTo6B_MX-4000_MY-2000 XToYHTo6B_MX-4000_MY-2500 XToYHTo6B_MX-4000_MY-2800
```
Combine output files
```
python combine_histograms.py -i /users/ferencek/HHH/condor_jobs_data_background_signal_20231220_123208 -p JetHT QCD TTbar XToYHTo6B_MX-1000_MY-300 XToYHTo6B_MX-1000_MY-600 XToYHTo6B_MX-1000_MY-800 XToYHTo6B_MX-1200_MY-300 XToYHTo6B_MX-1200_MY-600 XToYHTo6B_MX-1200_MY-800 XToYHTo6B_MX-1200_MY-1000 XToYHTo6B_MX-1600_MY-300 XToYHTo6B_MX-1600_MY-600 XToYHTo6B_MX-1600_MY-800 XToYHTo6B_MX-1600_MY-1000 XToYHTo6B_MX-1600_MY-1200 XToYHTo6B_MX-1600_MY-1400 XToYHTo6B_MX-2000_MY-300 XToYHTo6B_MX-2000_MY-600 XToYHTo6B_MX-2000_MY-800 XToYHTo6B_MX-2000_MY-1000 XToYHTo6B_MX-2000_MY-1200 XToYHTo6B_MX-2000_MY-1600 XToYHTo6B_MX-2000_MY-1800 XToYHTo6B_MX-2500_MY-300 XToYHTo6B_MX-2500_MY-600 XToYHTo6B_MX-2500_MY-800 XToYHTo6B_MX-2500_MY-1000 XToYHTo6B_MX-2500_MY-1200 XToYHTo6B_MX-2500_MY-1600 XToYHTo6B_MX-2500_MY-2000 XToYHTo6B_MX-2500_MY-2200 XToYHTo6B_MX-3000_MY-300 XToYHTo6B_MX-3000_MY-600 XToYHTo6B_MX-3000_MY-800 XToYHTo6B_MX-3000_MY-1000 XToYHTo6B_MX-3000_MY-1200 XToYHTo6B_MX-3000_MY-1600 XToYHTo6B_MX-3000_MY-2000 XToYHTo6B_MX-3000_MY-2500 XToYHTo6B_MX-3000_MY-2800 XToYHTo6B_MX-3500_MY-300 XToYHTo6B_MX-3500_MY-600 XToYHTo6B_MX-3500_MY-800 XToYHTo6B_MX-3500_MY-1000 XToYHTo6B_MX-3500_MY-1200 XToYHTo6B_MX-3500_MY-1600 XToYHTo6B_MX-3500_MY-2000 XToYHTo6B_MX-3500_MY-2500 XToYHTo6B_MX-3500_MY-2800 XToYHTo6B_MX-4000_MY-300 XToYHTo6B_MX-4000_MY-600 XToYHTo6B_MX-4000_MY-800 XToYHTo6B_MX-4000_MY-1000 XToYHTo6B_MX-4000_MY-1200 XToYHTo6B_MX-4000_MY-1600 XToYHTo6B_MX-4000_MY-2000 XToYHTo6B_MX-4000_MY-2500 XToYHTo6B_MX-4000_MY-2800
```
Copy output files to a central location
```
mkdir -p /STORE/HHH/Histograms/2017/20231220_123208/
cp -p /users/ferencek/HHH/condor_jobs_data_background_signal_20231220_123208/fit/*.root /STORE/HHH/Histograms/2017/20231220_123208/
```
Produce unnormalized histograms for one signal sample for plotting the cut flow
```
mv /users/ferencek/HHH/condor_jobs_data_background_signal_20231220_123208/fit/XToYHTo6B_MX-2500_MY-800_Histograms.root /users/ferencek/HHH/condor_jobs_data_background_signal_20231220_123208/fit/XToYHTo6B_MX-2500_MY-800_Histograms_normalized.root
python combine_histograms.py -i /users/ferencek/HHH/condor_jobs_data_background_signal_20231220_123208 -p XToYHTo6B_MX-2500_MY-800 --skip_norm
mv /users/ferencek/HHH/condor_jobs_data_background_signal_20231220_123208/fit/XToYHTo6B_MX-2500_MY-800_Histograms.root /STORE/HHH/Histograms/2017/20231220_123208/XToYHTo6B_MX-2500_MY-800_Histograms_unnormalized.root
mv /users/ferencek/HHH/condor_jobs_data_background_signal_20231220_123208/fit/XToYHTo6B_MX-2500_MY-800_Histograms_normalized.root /users/ferencek/HHH/condor_jobs_data_background_signal_20231220_123208/fit/XToYHTo6B_MX-2500_MY-800_Histograms.root
```

[*] `voms-proxy-init -rfc -voms cms -valid 168:00`
