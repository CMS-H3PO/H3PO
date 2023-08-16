from condor.paths import *
from os import listdir, system
from os.path import join, isfile
import datetime


if __name__ == '__main__':
    datasets = ["QCD500", "QCD700", "QCD2000", "QCD1000", "QCD1500", "TTbarHadronic", "TTbarSemileptonic",
                "JetHT2017B", "JetHT2017C", "JetHT2017D", "JetHT2017E", "JetHT2017F"]

    initial_dir = H3_DIR
    condor_dir = join(initial_dir, 'condor_jobs_' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    condor_dir_jobs = join(condor_dir, "jobs")
    condor_dir_logs = join(condor_dir, "logs")
    os.system('mkdir -p ' + condor_dir_jobs)
    os.system('mkdir -p ' + condor_dir_logs)

    num_of_jobs = {}
    for dataset in datasets:
        dataset_path = join(SKIM_DIR, '2017', dataset)
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
            system('condor_submit ' + job_desc)
            num_of_jobs[dataset] += 1
            


