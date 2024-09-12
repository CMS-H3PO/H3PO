#!/usr/bin/env python

import os, sys, re
from templates import *
import subprocess
from paths import SKIM_DIR, SKIM_JOB_DIR

def createDirIfNotExist(path):
    if not os.path.exists(path):
        print("CREATING DIR: ", path)
        os.makedirs(path)

def removeProcessedFiles(inputFiles,outputDir):
    filesToProcess = []

    for iFile in inputFiles:
        fileName = iFile.split("/")[-1]
        outputPath = os.path.join(outputDir,fileName)
        if not os.path.exists(outputPath):
            filesToProcess.append(iFile)

    return filesToProcess



def create_jobs(config,year="2016",jobs_dir="",out_dir=""):
    submissionCmds     = []
    for sample, sample_cfg in config.items():
        
        sampleJobs_dir = os.path.join(jobs_dir,sample)
        sampleOut_dir  = os.path.join(out_dir, sample)
        #Create dir to store jobs and dir to store output
        createDirIfNotExist(os.path.join(sampleJobs_dir, 'input'))
        createDirIfNotExist(os.path.join(sampleJobs_dir, 'output'))
        createDirIfNotExist(sampleOut_dir)

        exeScript     = skim_template.replace("JOB_DIR",sampleJobs_dir)
        open(os.path.join(sampleJobs_dir, 'input', 'run_{}.sh'.format(sample)), 'w').write(exeScript)
        os.system("chmod +x {0}".format(os.path.join(sampleJobs_dir, 'input', 'run_{}.sh'.format(sample))))

        #Get input files
        dataset     = sample_cfg["dataset"]
        das_query   =[]
        for singleDataset in dataset.split(','):
            query   = "dasgoclient -query='file dataset={singleDataset}'".format(**locals())
            das_query.append(query)
        allFiles    = []
        for query in das_query:
            files   = subprocess.check_output(das_query, shell=True).split()
            for file in files:
                allFiles.append(file.decode("utf-8"))


        #Check if files already processed
        nDASFiles   = len(allFiles)
        allFiles    = removeProcessedFiles(allFiles,sampleOut_dir)
        print("{0}:\t{1}/{2} files processed".format(sample,nDASFiles-len(allFiles),nDASFiles))

        if(len(allFiles)==0):
            continue

        #Create file with Condor commands
        cmdFile       = open(os.path.join(sampleJobs_dir, 'input', 'cmds_{}.txt'.format(sample)), 'w')
        #Loop over files to be processed
        for i, iFile in enumerate(allFiles):
            fName      = iFile.split("/")[-1]

            condor_script = re.sub('EXEC',os.path.join(sampleJobs_dir, 'input', 'run_{}.sh'.format(sample)), selection_condor)
            condor_script = re.sub('OUTPUT',os.path.join(sampleJobs_dir, 'output'), condor_script)
            condor_script = re.sub('JOB','{}'.format(i), condor_script)
            condor_script = re.sub('ARGS',"-i {} -o {}".format(iFile,sampleOut_dir), condor_script)
            open(os.path.join(sampleJobs_dir, 'input', 'condor_{}_{}.condor'.format(sample, i)), 'w').write(condor_script)
            #Submit command
            cmdFile.write("condor_submit {0}\n".format(os.path.join(sampleJobs_dir, 'input', 'condor_{}_{}.condor'.format(sample, i))))

        #Commands to source
        submissionCmds.append("source {0}".format(os.path.join(sampleJobs_dir, 'input', 'cmds_{}.txt'.format(sample))))
    
    for cmd in submissionCmds:
        print(cmd)

def main():

    import json
    
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Do -h to see usage")

    parser.add_argument('-c', '--config', help='Job config file in JSON format')
    parser.add_argument('-y', '--year', help='Dataset year',default="2016")
 
    args = parser.parse_args()

    print(args)

    out_dir  = os.path.join(SKIM_DIR,args.year)
    jobs_dir = os.path.join(SKIM_JOB_DIR,args.year)

    with open(args.config, 'r') as config_file:
        config = json.load(config_file)
        create_jobs(config,year=args.year,out_dir=out_dir,jobs_dir=jobs_dir)
                    

            

if __name__ == "__main__":
    main()

