from os import listdir, getcwd, system, chdir
from os.path import isfile, join
from argparse import ArgumentParser


def remove_root_files(list_of_root_files):
    for file in list_of_root_files:
        system('rm ' + file)

def combine_histograms(identifier, rmFiles=False, startsWithRegion=True, mvFiles=False, fit_dir="fit", startsWithId=False):
    
    regions = ["semiBoosted_pass","semiBoosted_fail","Boosted_pass","Boosted_fail"]
    
    for region in regions:
        list_of_root_files = []
        cwd = getcwd()
        
        for file in listdir(cwd):
            if not isfile(join(cwd, file)):
                continue
            if (file.startswith(identifier) if startsWithId else ('_'+identifier+'-') in file) and file.endswith('.root') and (file.startswith(region) if startsWithRegion else ('_'+region+'_') in file):
                list_of_root_files.append(file)

        system("hadd -f {0}_{1}_50.root {2}".format(identifier,region, " ".join(list_of_root_files)))
        if rmFiles:
            remove_root_files(list_of_root_files)
        if mvFiles:
            system("mkdir -p {0}".format(fit_dir))
            system("mv {0}_{1}_50.root {2}".format(identifier,region,fit_dir))


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
    
    parser.add_argument("--delete", dest="delete", action='store_true',
                      help="Delete Condor output root files (default: %(default)s)",
                      default=False)

    (options, args) = parser.parse_known_args()

    chdir(options.input)

    datasets = ["QCD500", "QCD700", "QCD2000", "QCD1000", "QCD1500", "TTbarHadronic", "TTbarSemileptonic",
                "JetHT2017B", "JetHT2017C", "JetHT2017D", "JetHT2017E", "JetHT2017F"]
    
    for dataset in datasets:
        combine_histograms(dataset, options.delete)

    processes = ["QCD","TTbar","JetHT2017"]

    for process in processes:
        combine_histograms(process, False, False, True, options.fit_dir, True)
