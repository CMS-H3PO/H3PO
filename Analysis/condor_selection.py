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

    parser.add_argument("--dry_run", dest="dry_run", action="store_true",
                        help="Dry run without submitting Condor jobs (default: %(default)s)",
                        default=False)

    (options, args) = parser.parse_known_args()

    initial_dir = H3_DIR
    if options.output.startswith('/'):
        condor_dir = options.output.rstrip('/') + '_' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    else:
        condor_dir = join(initial_dir, options.output.rstrip('/') + '_' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    condor_dir_jobs = join(condor_dir, "jobs")
    condor_dir_logs = join(condor_dir, "logs")
    os.system('mkdir -p ' + condor_dir_jobs)
    os.system('mkdir -p ' + condor_dir_logs)

    num_of_jobs = {}
    for dataset in datasets[options.year]:
        dataset_path = join(datasets[options.year][dataset], options.year, dataset)
        num_of_jobs[dataset] = 0
        for i, file in enumerate(listdir(dataset_path)):
            file_path = join(dataset_path, file)
            if not isfile(file_path):
                continue
            args = '-s={0} -i={1} -o={2}'.format(dataset, file_path, condor_dir)
            dataset_job = '{0}_{1}'.format(dataset, i)
            job_desc = join(condor_dir_jobs, 'job_desc-' + dataset_job + '.txt')
            
            with open(job_desc, 'w') as job_file:
                job_file.write('executable  = run.sh\n')
                job_file.write('universe    = vanilla\n')
                job_file.write('initialdir  = ' + initial_dir + '\n')
                job_file.write('getenv = False\n')
                
                job_file.write('log    = ' + join(condor_dir_logs, 'log-' + dataset_job + '.log') + '\n')
                job_file.write('output = ' + join(condor_dir_logs, 'tmp-' + dataset_job + '.out') + '\n')
                job_file.write('error  = ' + join(condor_dir_logs, 'tmp-' + dataset_job + '.err') + '\n')
                job_file.write('arguments = "' + args + '"\n')
                job_file.write('queue\n')
            if not options.dry_run:
                system('condor_submit ' + job_desc)
            num_of_jobs[dataset] += 1
            


