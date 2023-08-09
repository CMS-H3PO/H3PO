from os import listdir, system
from os.path import join, isfile

if __name__ == '__main__':
    datasets = ["XToYHTo6B_MX-2400_MY-800"]


    for dataset in datasets:
        dataset_path = "/users/bchitrod/Data/{0}.root".format(dataset)
        print(dataset_path)
        args = "-s {0} -fp {1}".format(dataset,dataset_path)
            
        with open('job_desc' + dataset + '.txt', 'w') as job_file:
            job_file.write('executable = run_signal.sh\n')
            job_file.write('universe    =  vanilla\n')
            job_file.write('initialdir  =  /users/bchitrod/HHH/H3PO/Analysis\n')
            job_file.write('getenv = True\n')
            
            job_file.write('log = log' + dataset + '.log\n')
            job_file.write('Arguments = '+args+' \n')
            job_file.write('Output = tmp' + '-' + dataset + '.out\n')
            job_file.write('error =  tmp.err\n')
            job_file.write('queue\n\n')
        system('condor_submit job_desc' + dataset + '.txt')
            
    # print("Waiting for all jobs to finish...")
    # for dataset in datasets:
    #     system('condor_wait log' + dataset + '.log')
    #     combine_histograms(dataset)
            
    # print("All jobs finished.")

