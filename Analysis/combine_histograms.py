from os import listdir, getcwd, system, chdir
from os.path import isfile, join
from argparse import ArgumentParser
from condor.datasets import *


def remove_root_files(list_of_root_files):
    for file in list_of_root_files:
        system('rm ' + file)


def combine_histograms(identifier, rmFiles=False, startsWithRegion=True, mvFiles=False, fit_dir="fit", startsWithId=False):
    
    regions = ["Histograms"]
    
    for region in regions:
        list_of_root_files = []
        cwd = getcwd()
        
        for file in listdir(cwd):
            if not isfile(join(cwd, file)):
                continue
            if (file.startswith(identifier) if startsWithId else ('_'+identifier+'-') in file) and file.endswith('.root') and (file.startswith(region) if startsWithRegion else ('_'+region) in file):
                list_of_root_files.append(file)

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

    (options, args) = parser.parse_known_args()

    chdir(options.input)

    for dataset in datasets[options.year]:
        combine_histograms(dataset, options.delete)

    for process in options.processes:
        combine_histograms(process, False, False, True, options.fit_dir, True)
