import uproot
import awkward as ak
import matplotlib.pyplot as plt
import hist
from hist import Hist
from coffea.nanoevents import NanoEventsFactory, BaseSchema
import coffea.processor as processor
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema, schemas
import numpy as np
import mplhep as hep
from Selection import *
from os import listdir, getcwd, system, chdir
from os.path import isfile, join

def remove_root_files(list_of_root_files):
    for file in list_of_root_files:
        system('rm ' + file)

def combine_histograms(dataset):
    regions = ["semiBoosted_pass","semiBoosted_fail","Boosted_pass","Boosted_fail"]
    for region in regions:
        list_of_root_files = []
        try:
            system('rm {0}_{1}.root'.format(dataset,region))
        except:
            print('{0}_{1}.root didn\'t exist before'.format(dataset,region))
            
        for file in listdir(getcwd()):
            if not isfile(join(getcwd(), file)):
                continue
            if dataset in file and '.root' in file and '.png' not in file and region in file:
                list_of_root_files.append(file)

        system("hadd -f {0}_{1}_50.root {2}".format(dataset,region, " ".join(list_of_root_files)))
        remove_root_files(list_of_root_files)
        system("mv {0}_{1}_50.root ./rootfiles/".format(dataset,region))

if __name__ == '__main__':
    datasets = ["QCD500", "QCD700", "QCD2000", "QCD1000", "QCD1500", "TTbarHadronic", "TTbarSemileptonic",
                "JetHT2017B", "JetHT2017C", "JetHT2017D", "JetHT2017E", "JetHT2017F"]
    for dataset in datasets:
        combine_histograms(dataset)


    chdir('/users/bchitrod/HHH/H3PO/Analysis/rootfiles/')
    regions = ["semiBoosted_pass","semiBoosted_fail","Boosted_pass","Boosted_fail"]
    processes = ["QCD","TTbar","JetHT2017"]

    for process in processes:
        for region in regions:
            list_of_root_files = []
            for file in listdir(getcwd()):
                if not isfile(join(getcwd(), file)):
                    continue
                if process in file and '.root' in file and '.png' not in file and region in file and '_50' in file:
                    list_of_root_files.append(file)
            system("hadd {0}_{1}_50.root {2}".format(process,region," ".join(list_of_root_files)))
            system("mv {0}_{1}_50.root ./fit/".format(process,region))
