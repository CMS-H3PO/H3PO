from os import listdir, getcwd, system, chdir
from os.path import isfile, join
from argparse import ArgumentParser
from condor.datasets import *
import ROOT
import json
import re 

def get_dataset_scaling_factor(process,year,sumGen):
    json_file = open(H3_DIR + "/xsecs.json")
    config = json.load(json_file)
    xsec    = config[year][process]["xsec"]
    luminosity  = config[year]["lumi"]
    scaling     = (xsec*luminosity)/sumGen
    return scaling

def get_number_of_events_in_dataset(list_of_root_files):
    nev = 0
    for root_fname in list_of_root_files:
        froot = ROOT.TFile.Open(root_fname)
        nevHisto = ROOT.gDirectory.Get("numberOfGenEventsHisto")
        nev += nevHisto.GetBinContent(1)
    return nev

def normalize_histograms(identifier, year, startsWithRegion=True, startsWithId=False):
    regions = ["Histograms"]
    
    for region in regions:
        list_of_root_files = []
        cwd = getcwd()
        list_of_root_files = get_listof_root_files(cwd, identifier, region, startsWithRegion, startsWithId)
        nev_in_sample = get_number_of_events_in_dataset(list_of_root_files)
        scale = get_dataset_scaling_factor(identifier, year, nev_in_sample)
        for root_fname in list_of_root_files:
            froot = ROOT.TFile.Open(root_fname, 'UPDATE')
            scaled_histos = []
            for myKey in ROOT.gDirectory.GetListOfKeys():
                if re.match ('TH', myKey.GetClassName()):
                    hname = myKey.GetName()
                    if (hname == "numberOfGenEventsHisto"):
                        continue                    
                    h = ROOT.gDirectory.Get(hname)
                    h.SetDirectory(0)
                    h.Scale(scale)
                    scaled_histos.append(h)
                    
            for h in scaled_histos:
                h.Write("", ROOT.TObject.kOverwrite);
        
def get_listof_root_files(cwd, identifier, region, startsWithRegion, startsWithId):
    list_of_root_files = []
    for file in listdir(cwd):
        if not isfile(join(cwd, file)):
            continue
        if (file.startswith(identifier) if startsWithId else ('_'+identifier+'-') in file) and file.endswith('.root') and (file.startswith(region) if startsWithRegion else ('_'+region) in file):
            list_of_root_files.append(file)
    return list_of_root_files
            
def remove_root_files(list_of_root_files):
    for file in list_of_root_files:
        system('rm ' + file)



def combine_histograms(identifier, rmFiles=False, startsWithRegion=True, mvFiles=False, fit_dir="fit", startsWithId=False):
    
    regions = ["Histograms"]
    
    for region in regions:
        list_of_root_files = []
        cwd = getcwd()

        list_of_root_files = get_listof_root_files(cwd, identifier, region, startsWithRegion, startsWithId)
        filename = "{0}_{1}.root".format(identifier,region)

        # in case of only one source file, make sure that the source and target files do not have identical names. Otherwise, hadding is not needed

        if not (len(list_of_root_files)==1 and filename==list_of_root_files[0]):
            system("hadd -f {0} {1}".format(filename," ".join(list_of_root_files)))
        if rmFiles:
            remove_root_files(list_of_root_files)
        if mvFiles:
            system("mkdir -p {0}".format(fit_dir))
            system("mv {0} {1}".format(filename,fit_dir))


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
                        default=["QCD","TTbar","JetHT2017","XToYHTo6B_MX-2400_MY-800"],
                        metavar="PROCESSES")
    
    parser.add_argument("--delete", dest="delete", action='store_true',
                      help="Delete Condor output root files (default: %(default)s)",
                      default=False)
    parser.add_argument("--skip_norm", dest="normalize", action='store_false',
                        help="Specify if histograms should be normalized (default: %(default)s)",
                        default=True)


    (options, args) = parser.parse_known_args()

    chdir(options.input)
    
    if (options.normalize):
        for dataset in datasets[options.year]:
            if ("JetHT" in dataset):
                print ("Skipping JetHT")
                continue
            normalize_histograms(dataset, options.year)

    for dataset in datasets[options.year]:
        combine_histograms(dataset, options.delete)

    for process in options.processes:
        combine_histograms(process, False, False, True, options.fit_dir, True)

