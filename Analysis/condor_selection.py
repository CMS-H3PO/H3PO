from condor.paths import *
from condor.datasets import *
from os import listdir, system
from os.path import join, isfile
import datetime
from argparse import ArgumentParser


if __name__ == '__main__':
    # usage example
    Description = "Example: %(prog)s -o condor_jobs"
    
    # input parameters
    parser = ArgumentParser(description=Description)

    parser.add_argument("-o", "--output", dest="output",
                      help="Output directory name (default: %(default)s)",
                      default="condor_jobs",
                      metavar="OUTPUT_DIR")

    parser.add_argument("-y", "--year", dest="year",
                        help="Data taking year (default: %(default)s)",
                        default="2017",
                        metavar="YEAR")

    parser.add_argument("-d", "--datasets", dest="datasets",
                        help="Space-separated list of datasets (default: %(default)s)",
                        nargs='*',
                        default=["QCD","TTbar","JetHT","XToYHTo6B_MX-2400_MY-800"],
                        metavar="DATASETS")

    parser.add_argument("--dry_run", dest="dry_run", action="store_true",
                        help="Dry run without submitting Condor jobs (default: %(default)s)",
                        default=False)

    parser.add_argument("--no_timestamp", dest="no_timestamp", action="store_true",
                        help="Don't append the time stamp to the output directory name (default: %(default)s)",
                        default=False)

    parser.add_argument("-j", "--jecVariations", dest="jecVariations",
                        help="Space-separated list of JEC variations (default: %(default)s)",
                        nargs='*',
                        default=None,
                        metavar="JECVARS")

    parser.add_argument("-t", "--triggerList", help="Space-separated list of triggers (default: %(default)s)",
                        nargs="*",
                        dest="triggerList",
                        default = None
                        )
    
    parser.add_argument("-r", "--refTriggerList", help="Space-separated list of reference triggers (default: %(default)s)",
                        nargs="*",
                        dest="refTriggerList",
                        default = None
                        )

    parser.add_argument("--extra_histos", dest="extra_histos", action='store_true',
                        help="Switch for producing additional histograms (default: %(default)s)",
                        default=False)

    (options, args) = parser.parse_known_args()

    initial_dir = H3_DIR
    timestamp = ''
    if not options.no_timestamp:
        timestamp = '_' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    condor_dir = options.output.rstrip('/') + timestamp
    if not options.output.startswith('/'):
        condor_dir = join(initial_dir, condor_dir)
        
    condor_dir_jobs = join(condor_dir, "jobs")
    condor_dir_logs = join(condor_dir, "logs")
    os.system('mkdir -p ' + condor_dir_jobs)
    os.system('mkdir -p ' + condor_dir_logs)

    num_of_jobs = {}
    for dataset in datasets[options.year]:
        if not dataset.startswith(tuple(options.datasets)):
            continue
        dataset_path = join(datasets[options.year][dataset], options.year, dataset)
        num_of_jobs[dataset] = 0
        for i, file in enumerate(listdir(dataset_path)):
            file_path = join(dataset_path, file)
            if not isfile(file_path):
                continue
            args = '-s={0} -i={1} -o={2}'.format(dataset, file_path, condor_dir)
            if options.jecVariations != None:
                args += ' -j ' + (' ').join(options.jecVariations)
            if options.triggerList != None:
                args += ' -t ' + (' ').join(options.triggerList)
            if options.refTriggerList != None:
                args += ' -r ' + (' ').join(options.refTriggerList)
            if options.extra_histos:
                args += ' --extra_histos'

            dataset_job = '{0}_{1}'.format(dataset, i)
            job_desc = join(condor_dir_jobs, 'job_desc-' + dataset_job + '.txt')
            
            with open(job_desc, 'w') as job_file:
                job_file.write('executable  = run.sh\n')
                job_file.write('universe    = vanilla\n')
                job_file.write('initialdir  = ' + initial_dir + '\n')
                job_file.write('getenv = False\n')
                job_file.write('RequestMemory = 2000\n')
                job_file.write('requirements = (machine == "lorientree05.hep.zef.irb.hr" )\n')
                
                job_file.write('log    = ' + join(condor_dir_logs, 'log-' + dataset_job + '.log') + '\n')
                job_file.write('output = ' + join(condor_dir_logs, 'tmp-' + dataset_job + '.out') + '\n')
                job_file.write('error  = ' + join(condor_dir_logs, 'tmp-' + dataset_job + '.err') + '\n')
                job_file.write('arguments = "' + args + '"\n')
                job_file.write('queue\n')
            if not options.dry_run:
                system('condor_submit ' + job_desc)
            num_of_jobs[dataset] += 1

    number_of_jobs_total = 0
    for dataset in num_of_jobs:
        number_of_jobs_total += num_of_jobs[dataset]
    if number_of_jobs_total == 0:
        print('No matching dataset(s) found. No jobs to submit.')
