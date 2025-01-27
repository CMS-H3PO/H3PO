from os import listdir, getcwd, system, chdir
from os.path import isfile, join
from argparse import ArgumentParser
from condor.datasets import *
import ROOT
import json
import re 
import copy


def get_dataset_scaling_factor(dataset,year,sumGen):
    json_file = open(H3_DIR + "/xsecs.json")
    config = json.load(json_file)
    luminosity  = config[year]["lumi"]
    try:
        xsec    = config[year][dataset]["xsec"]
        scaling = (xsec*luminosity)/sumGen
    except:
        print("WARNING: Missing cross section for dataset {0}. Setting the scale factor to 1.\n".format(dataset))
        scaling = 1.
    return scaling


def get_number_of_events_in_dataset(list_of_root_files):
    nev = 0
    for root_fname in list_of_root_files:
        froot = ROOT.TFile.Open(root_fname, 'READ')
        nevHisto = froot.Get("numberOfGenEventsHisto")
        nev += nevHisto.GetBinContent(1)
        froot.Close()
    return nev


def normalize_histograms(signal_base, dataset, year, deleteFiles=False):

    datasetPresent = True

    list_of_root_files = []
    list_of_root_files = get_list_of_root_files(signal_base, dataset, startsWith=True)
    if len(list_of_root_files)>0:
        nev_in_sample = get_number_of_events_in_dataset(list_of_root_files)
        scale = get_dataset_scaling_factor(dataset, year, nev_in_sample)
        for root_fname in list_of_root_files:
            if not deleteFiles:
                cmd = "cp -p {0} unscaled_{1}".format(root_fname,root_fname)
                system(cmd)
            froot = ROOT.TFile.Open(root_fname, 'UPDATE')
            list_of_keys = copy.deepcopy(froot.GetListOfKeys()) # without deepcopy the processing time explodes, no idea why
            for myKey in list_of_keys:
                if re.match ('TH', myKey.GetClassName()):
                    hname = myKey.GetName()
                    if (hname == "numberOfGenEventsHisto"):
                        continue
                    h = froot.Get(hname)
                    h.Scale(scale)
                    h.Write("", ROOT.TObject.kOverwrite)
            froot.Close()
    else:
        datasetPresent = False

    return datasetPresent


def get_list_of_root_files(signal_base, identifier, startsWith):
    cwd = getcwd()
    list_of_root_files = []
    for file in listdir(cwd):
        if not isfile(join(cwd, file)):
            continue
        if (file.startswith(identifier+'_' if (signal_base in identifier) else identifier) if not startsWith else ('_'+identifier+'-') in file) and (file.startswith('Histograms') if startsWith else ('_Histograms') in file) and file.endswith('.root'):
            list_of_root_files.append(file)
    return list_of_root_files


def remove_root_files(list_of_root_files):
    for file in list_of_root_files:
        system('rm ' + file)


def mv_file(dir, file):
    system("mkdir -p {0}".format(dir))
    system("mv {0} {1}".format(file,dir))


def combine_histograms(signal_base, identifier, deleteFiles=False, skipNorm=False, startsWith=True, mvFiles=False, fit_dir="fit"):

    list_of_root_files = []

    list_of_root_files = get_list_of_root_files(signal_base, identifier, startsWith)
    filename = "{0}_{1}.root".format(identifier,'Histograms')

    # in case of only one source file, make sure that the source and target files do not have identical names. Otherwise, hadding is not needed
    if (len(list_of_root_files)==1 and filename==list_of_root_files[0]):
        if mvFiles:
            mv_file(fit_dir, filename)
    else:
        cmd = "hadd -f {0} {1}".format(filename," ".join(list_of_root_files))
        system(cmd)
        if deleteFiles:
            remove_root_files(list_of_root_files)
        else:
            if startsWith and not skipNorm and not "JetHT" in identifier:
                for root_fname in list_of_root_files:
                    system("mv unscaled_{0} {1}".format(root_fname,root_fname))
        if mvFiles:
            mv_file(fit_dir, filename)


def keep_dataset(signal_base, dataset, process_list):
    if signal_base not in process_list and (signal_base + "_") in dataset:
        return dataset.endswith(tuple(process_list))
    else:
        return dataset.startswith(tuple(process_list))


if __name__ == '__main__':
    # usage example
    Description = "Example: %(prog)s -i condor_jobs_<timestamp>"
    
    # input parameters
    parser = ArgumentParser(description=Description)

    parser.add_argument("-i", "--input", dest="input",
                      help="Input directory name",
                      metavar="INPUT",
                      required=True)
    
    parser.add_argument("-f", "--fit_dir", dest="fit_dir",
                      help="Fit directory name (default: %(default)s)",
                      default="fit",
                      metavar="FIT_DIR")

    parser.add_argument("-y", "--year", dest="year",
                        help="Data taking year (default: %(default)s)",
                        default="2017",
                        metavar="YEAR")
    
    parser.add_argument("-p", "--processes", dest="processes",
                        help="Space-separated list of processes (default: %(default)s)",
                        nargs='*',
                        default=["TTbar","JetHT","XToYHTo6B_MX-2500_MY-800"],
                        metavar="PROCESSES")

    parser.add_argument("--signal_base", dest="signal_base",
                        help="Signal process base name (default: %(default)s)",
                        default="XToYHTo6B",
                        metavar="SIGNAL_BASE")

    parser.add_argument("--delete_files", dest="delete_files", action='store_true',
                      help="Delete Condor output root files (default: %(default)s)",
                      default=False)
    
    parser.add_argument("--skip_norm", dest="skip_norm", action='store_true',
                        help="Specify if histograms should be normalized (default: %(default)s)",
                        default=False)


    (options, args) = parser.parse_known_args()
    
    chdir(options.input)
    
    missing_datasets = []

    signal_base = options.signal_base
    process_list = copy.deepcopy(options.processes)
    # can't have individual and merged signal samples at the same time
    if signal_base in process_list and process_list.count(signal_base + "_")>0:
        print("WARNING: Not possible to produce histograms for individual and merged signal samples at the same time. Dropping merged histograms.\n")
        process_list.remove(signal_base)

    if not options.skip_norm:
        print ("Performing normalization...")
        for dataset in datasets[options.year]:
            if not keep_dataset(signal_base, dataset, process_list):
                continue
            if ("JetHT" in dataset):
                print ("Skipping {0} during normalization".format(dataset))
                continue
            print ("Processing {0}".format(dataset))
            if not normalize_histograms(signal_base, dataset, options.year, options.delete_files):
                missing_datasets.append(dataset)
                print("WARNING: Missing files for dataset {0}. Check if this affects any of the final process files.\n".format(dataset))
        print ("Normalization done")
    else:
        # if not performing the normalization, still check for missing dataset files
        for dataset in datasets[options.year]:
            if not keep_dataset(signal_base, dataset, process_list):
                continue
            if len(get_list_of_root_files(signal_base, dataset, startsWith=True))==0:
                missing_datasets.append(dataset)
                print("WARNING: Missing files for dataset {0}. Check if this affects any of the final process files.\n".format(dataset))

    print ("Merging dataset files...")
    for dataset in datasets[options.year]:
        if dataset in missing_datasets:
            continue
        if not keep_dataset(signal_base, dataset, process_list):
            continue
        print ("Processing {0}".format(dataset))
        combine_histograms(signal_base, dataset, options.delete_files, options.skip_norm)
    print ("Merging dataset files done")

    print ("Merging process files...")
    processes = sorted(list(set(process_list))) # protection for duplicate entries
    for process in processes:
        if process in missing_datasets: # mostly relevant for signal samples where process==dataset
            continue
        print ("Processing {0}".format(process))
        combine_histograms(signal_base, process, options.delete_files, options.skip_norm, startsWith=False, mvFiles=True, fit_dir=options.fit_dir)
    print ("Merging process files done")
