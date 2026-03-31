import os
import sys
import glob
import fnmatch
import datetime
from argparse import ArgumentParser


if __name__ == '__main__':
    # usage example
    Description = "Example: %(prog)s -y 2016 2016APV 2017 2018"
    
    # input parameters
    parser = ArgumentParser(description=Description)

    parser.add_argument("-i", "--input", dest="input",
                        help="Input directories path (default: %(default)s)",
                        default="/STORE/HHH/Histograms/",
                        metavar="INPUT")
    
    parser.add_argument("-o", "--output", dest="output",
                        help="Output directory path (default: %(default)s)",
                        default="/STORE/HHH/Histograms/Run2/",
                        metavar="OUTPUT")

    parser.add_argument("-y", "--years", dest="years",
                        help="Space-separated list of years to be combined (default: %(default)s)",
                        nargs='*',
                        default=["2016","2016APV","2017","2018"],
                        metavar="YEARS")

    parser.add_argument("-p", "--processes", dest="processes",
                        help="Space-separated list of processes (default: %(default)s)",
                        nargs='*',
                        default=["TTbar","JetHT","XToYHTo6B"],
                        metavar="PROCESSES")

    parser.add_argument("-s", "--suffix", dest="suffix",
                        help="Output directory name suffix (default: %(default)s)",
                        default="",
                        metavar="SUFFIX")

    parser.add_argument("--no_timestamp", dest="no_timestamp", action="store_true",
                        help="Don't prepend the time stamp to the output directory name (default: %(default)s)",
                        default=False)

    parser.add_argument("--use_existing", dest="use_existing", action="store_true",
                        help="Use existing output directory (default: %(default)s)",
                        default=False)

    parser.add_argument("--no_symlink", dest="no_symlink", action="store_true",
                        help="Don't create/update a symlink to the output directory (default: %(default)s)",
                        default=False)

    (options, args) = parser.parse_known_args()

    sorted_years = sorted(options.years)
    process_list = options.processes
    files_dict = {}
    files_set = set()
    out_dir_name = ''
    if not options.use_existing and not options.no_timestamp:
        out_dir_name += datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # fill the file dictionary and the file set
    for year in sorted_years:
        ls_dir = os.listdir( os.path.join(options.input, year, "latest") )
        files_year_set = set()
        for process in process_list:
            files = fnmatch.filter(ls_dir, f"{process}*_Histograms.root")
            files_year_set.update(files)
            files_set.update(files)
        files_dict[year] = list(files_year_set)
        if not options.use_existing:
            out_dir_name += ("_"+year if out_dir_name else year)

    if not options.use_existing and options.suffix:
        out_dir_name += ("_"+options.suffix)

    out_dir_path = os.path.join(options.output, out_dir_name)
    if not options.use_existing:
        os.system("mkdir -pv {0}".format(out_dir_path))
        if not options.no_symlink:
            os.system("ln -sfnv {0} {1}".format(out_dir_name, os.path.join(options.output, "latest")))
    
    os.chdir(out_dir_path)

    sorted_files = sorted(files_set)

    # hadd files
    for f in sorted_files:
        # but first check that all files are in place
        file_paths = []
        for year in sorted_years:
            if f not in files_dict[year]:
                print("ERROR: File {0} is missing for year {1}. Aborting".format(f, year))
                sys.exit(1)
            else:
                file_paths.append(os.path.join(options.input, year, "latest", f))
        
        cmd = "hadd -f {0} {1}".format(f, " ".join(file_paths))
        os.system(cmd)
