import uproot
import ROOT
import json
import awkward as ak
import matplotlib.pyplot as plt
import hist
from hist import Hist
from coffea.nanoevents import NanoEventsFactory, BaseSchema
import coffea.processor as processor
from coffea.processor import accumulate
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import numpy as np
import mplhep as hep
from testSelection import *

def plotSignal(Signal_test,scale,process):

    trijet_mass_Signaltest = (Signal_test[:,0]+Signal_test[:,1]+Signal_test[:,2]).mass


    j3_sigtest_bin = hist.axis.Regular(label="Trijet Mass with pt, eta, mass>50 [GeV]", name="trijet_mass_sigtest", bins=40, start=0, stop=6000)
    j3_sigtest_hist = Hist(j3_sigtest_bin)
    j3_sigtest_hist.fill(trijet_mass_sigtest=trijet_mass_Signaltest)
    #j3_sigtest_hist *= scale


    return j3_sigtest_hist


files = open("/afs/cern.ch/work/b/bchitrod/private/HHH/H3PO/2017/CR/Sample_2017.txt", "r")
processes = ["QCD500","QCD700","QCD1000","QCD1500","QCD2000","TTbarHadronic","TTbarSemileptonic","Signal","Data"] 
filename = files.readlines()
year = "2017"
for process,fname in zip(processes,filename):
    oFile = process
    Signal_test = Signal(fname,process,eventsToRead=None)
    if (process!= "Data"):
        scale = normalizeProcess(process,year)
    if (process == "Data"):
        scale = 1
    j3_sigtest_hist = plotSignal(Signal_test,scale,process)
    with uproot.recreate("test_nonscaled_{0}.root".format(oFile)) as fout:
        fout[f"j3_sigtest_hist"] = j3_sigtest_hist


