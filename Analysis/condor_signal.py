from condor.paths import *
from os import listdir, system
from os.path import join, isfile
import datetime


if __name__ == '__main__':
    datasets = ["XToYHTo6B_MX-2400_MY-800"]


    initial_dir = H3_DIR
    condor_dir = join(initial_dir, 'condor_jobs_' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    condor_dir_jobs = join(condor_dir, "jobs")
    condor_dir_logs = join(condor_dir, "logs")
    os.system('mkdir -p ' + condor_dir_jobs)
    os.system('mkdir -p ' + condor_dir_logs)


    for dataset in datasets:
        file_path = "/users/bchitrod/Data/{0}.root".format(dataset)
        print(file_path)
        args = '-s={0} -i={1} -o={2}'.format(dataset, file_path, condor_dir)
        job_desc = join(condor_dir_jobs, 'job_desc-' + dataset + '.txt')
            
        with open('job_desc-' + dataset + '.txt', 'w') as job_file:
            job_file.write('executable  = run_signal.sh\n')
            job_file.write('universe    = vanilla\n')
            job_file.write('initialdir  = ' + initial_dir + '\n')
            job_file.write('getenv = False\n')
            
            job_file.write('log    = ' + join(condor_dir_logs, 'log-' + dataset + '.log') + '\n')
            job_file.write('output = ' + join(condor_dir_logs, 'tmp-' + dataset + '.out') + '\n')
            job_file.write('error  = ' + join(condor_dir_logs, 'tmp-' + dataset + '.err') + '\n')
            job_file.write('arguments = "' + args + '"\n')
            job_file.write('queue\n')
        system('condor_submit job_desc-' + dataset + '.txt')
            
    # print("Waiting for all jobs to finish...")
    # for dataset in datasets:
    #     system('condor_wait log' + dataset + '.log')
    #     combine_histograms(dataset)
            
    # print("All jobs finished.")

