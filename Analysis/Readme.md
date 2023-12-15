# Files:
skimming.py - perform a loose selection on the files and store "skimmed" files. Execution time of the selection script is significantly reduced if skims are used as input\
Selection.py - implements all the selection

HHH_samples_2016.txt - Official sample list of 2016 NanoAOD XToYHTo6B samples\
HHH_samples_2017.txt - Official sample list of 2017 NanoAOD XToYHTo6B samples

<!-- Efficiency_plot.py - creates 2D efficiency plot (Mass Y vs. Mass X)\ -->
<!-- mass_matching_plots_boosted.py - creates MJJJ and MJJ mass distributions for boosted events\ -->
<!-- mass_matching_plots_semiboosted.py - creates MJJJ and MJJ mass distributions for semiboosted events\ -->

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

<!-- To generate boosted and semiboosted plots: -->
<!-- ``` -->
<!-- python Plot_Boosted.py -->
<!-- python Plot_semiBoosted.py -->
<!-- ``` -->

# Example commands:

Grid proxy needs to be initialized before running skimming to access the file on the store
```
python skimming.py -i store/mc/RunIISummer20UL17NanoAODv9/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/NANOAODSIM/106X_mc2017_realistic_v9-v1/100000/D5426269-CD07-CA4C-8E9E-E2336514139F.root -o test_output
```

Commands from the last round of histogram production:
```
python condor_selection.py -o /users/ferencek/HHH/condor_jobs_data_background_signal -j nominal -t PFHT1050 AK8PFJet500 PFJet500 -d JetHT QCD TTbar XToYHTo6B_MX-1000_MY-300 XToYHTo6B_MX-1000_MY-600 XToYHTo6B_MX-1000_MY-800 XToYHTo6B_MX-1200_MY-300 XToYHTo6B_MX-1200_MY-600 XToYHTo6B_MX-1200_MY-800 XToYHTo6B_MX-1200_MY-1000 XToYHTo6B_MX-1600_MY-300 XToYHTo6B_MX-1600_MY-600 XToYHTo6B_MX-1600_MY-800 XToYHTo6B_MX-1600_MY-1000 XToYHTo6B_MX-1600_MY-1200 XToYHTo6B_MX-1600_MY-1400 XToYHTo6B_MX-2000_MY-300 XToYHTo6B_MX-2000_MY-600 XToYHTo6B_MX-2000_MY-800 XToYHTo6B_MX-2000_MY-1000 XToYHTo6B_MX-2000_MY-1200 XToYHTo6B_MX-2000_MY-1600 XToYHTo6B_MX-2000_MY-1800 XToYHTo6B_MX-2500_MY-300 XToYHTo6B_MX-2500_MY-600 XToYHTo6B_MX-2500_MY-800 XToYHTo6B_MX-2500_MY-1000 XToYHTo6B_MX-2500_MY-1200 XToYHTo6B_MX-2500_MY-1600 XToYHTo6B_MX-2500_MY-2000 XToYHTo6B_MX-2500_MY-2200 XToYHTo6B_MX-3000_MY-300 XToYHTo6B_MX-3000_MY-600 XToYHTo6B_MX-3000_MY-800 XToYHTo6B_MX-3000_MY-1000 XToYHTo6B_MX-3000_MY-1200 XToYHTo6B_MX-3000_MY-1600 XToYHTo6B_MX-3000_MY-2000 XToYHTo6B_MX-3000_MY-2500 XToYHTo6B_MX-3000_MY-2800 XToYHTo6B_MX-3500_MY-300 XToYHTo6B_MX-3500_MY-600 XToYHTo6B_MX-3500_MY-800 XToYHTo6B_MX-3500_MY-1000 XToYHTo6B_MX-3500_MY-1200 XToYHTo6B_MX-3500_MY-1600 XToYHTo6B_MX-3500_MY-2000 XToYHTo6B_MX-3500_MY-2500 XToYHTo6B_MX-3500_MY-2800 XToYHTo6B_MX-4000_MY-300 XToYHTo6B_MX-4000_MY-600 XToYHTo6B_MX-4000_MY-800 XToYHTo6B_MX-4000_MY-1000 XToYHTo6B_MX-4000_MY-1200 XToYHTo6B_MX-4000_MY-1600 XToYHTo6B_MX-4000_MY-2000 XToYHTo6B_MX-4000_MY-2500 XToYHTo6B_MX-4000_MY-2800
```
```
python combine_histograms.py -i /users/ferencek/HHH/condor_jobs_data_background_signal_20231215_184046 -p JetHT QCD TTbar XToYHTo6B_MX-1000_MY-300 XToYHTo6B_MX-1000_MY-600 XToYHTo6B_MX-1000_MY-800 XToYHTo6B_MX-1200_MY-300 XToYHTo6B_MX-1200_MY-600 XToYHTo6B_MX-1200_MY-800 XToYHTo6B_MX-1200_MY-1000 XToYHTo6B_MX-1600_MY-300 XToYHTo6B_MX-1600_MY-600 XToYHTo6B_MX-1600_MY-800 XToYHTo6B_MX-1600_MY-1000 XToYHTo6B_MX-1600_MY-1200 XToYHTo6B_MX-1600_MY-1400 XToYHTo6B_MX-2000_MY-300 XToYHTo6B_MX-2000_MY-600 XToYHTo6B_MX-2000_MY-800 XToYHTo6B_MX-2000_MY-1000 XToYHTo6B_MX-2000_MY-1200 XToYHTo6B_MX-2000_MY-1600 XToYHTo6B_MX-2000_MY-1800 XToYHTo6B_MX-2500_MY-300 XToYHTo6B_MX-2500_MY-600 XToYHTo6B_MX-2500_MY-800 XToYHTo6B_MX-2500_MY-1000 XToYHTo6B_MX-2500_MY-1200 XToYHTo6B_MX-2500_MY-1600 XToYHTo6B_MX-2500_MY-2000 XToYHTo6B_MX-2500_MY-2200 XToYHTo6B_MX-3000_MY-300 XToYHTo6B_MX-3000_MY-600 XToYHTo6B_MX-3000_MY-800 XToYHTo6B_MX-3000_MY-1000 XToYHTo6B_MX-3000_MY-1200 XToYHTo6B_MX-3000_MY-1600 XToYHTo6B_MX-3000_MY-2000 XToYHTo6B_MX-3000_MY-2500 XToYHTo6B_MX-3000_MY-2800 XToYHTo6B_MX-3500_MY-300 XToYHTo6B_MX-3500_MY-600 XToYHTo6B_MX-3500_MY-800 XToYHTo6B_MX-3500_MY-1000 XToYHTo6B_MX-3500_MY-1200 XToYHTo6B_MX-3500_MY-1600 XToYHTo6B_MX-3500_MY-2000 XToYHTo6B_MX-3500_MY-2500 XToYHTo6B_MX-3500_MY-2800 XToYHTo6B_MX-4000_MY-300 XToYHTo6B_MX-4000_MY-600 XToYHTo6B_MX-4000_MY-800 XToYHTo6B_MX-4000_MY-1000 XToYHTo6B_MX-4000_MY-1200 XToYHTo6B_MX-4000_MY-1600 XToYHTo6B_MX-4000_MY-2000 XToYHTo6B_MX-4000_MY-2500 XToYHTo6B_MX-4000_MY-2800 XToYHTo6B_MX-4000_MY-2800
```
