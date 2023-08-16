# Files:
skimming.py - perform a loose selection on the files and store "skimmed" files. Execution time of the selection script is significantly reduced if skims are used as input\
Selection.py - implements all the selection\
Efficiency_plot.py - creates 2D efficiency plot (Mass Y vs. Mass X)\
mass_matching_plots_boosted.py - creates MJJJ and MJJ mass distributions for boosted events\
mass_matching_plots_semiboosted.py - creates MJJJ and MJJ mass distributions for semiboosted events\
HHH_samples_2016.txt - Official sample list of 2016 NanoAOD XToYHTo6B samples (Needs to copy to Lorien once production is complete)\
HHH_samples_2017.txt - Official sample list of 2017 NanoAOD XToYHTo6B samples (Needs to copy to Lorien once production is complete)

# Make plots with signal, backgrounds and data for SR(Signal Region) and VR(Validation Region):

To run Background and Data samples:
```
python condor_selection.py
```
To run Signal Samples:
```
python condor_signal.py
```
It will submit jobs to condor for all the samples. Wait till all jobs are done. Output root files will be stored in ```condor_jobs_<timestamp>``` directory.\
To combine histograms:
```
python combine_histograms.py -i condor_jobs_<timestamp> [--delete]
```
This will combine root files and store them in ```condor_jobs_<timestamp>/fit``` directory with intermediate files left in ```condor_jobs_<timestamp>```. You can use an optional ```--delete``` parameter to delete the Condor output root files (once that is done, you can no longer re-run ```combine_histograms.py```).\
To generate boosted and semiboosted plots:
```
python Plot_Boosted.py
python Plot_semiBoosted.py
```

# Example commands:
Grid proxy needs to be initialized before running skimming to access the file on the store
```
python skimming.py -i store/mc/RunIISummer20UL17NanoAODv9/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/NANOAODSIM/106X_mc2017_realistic_v9-v1/100000/D5426269-CD07-CA4C-8E9E-E2336514139F.root -o test_output
```
