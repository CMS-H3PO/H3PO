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

def HbbvsQCD(fatjet):
    score = (fatjet.particleNetMD_Xbb/(fatjet.particleNetMD_Xbb+fatjet.particleNetMD_QCD))
    return score

def Signal(fname,process,eventsToRead=None):
    events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema,metadata={"dataset":process},entry_stop=eventsToRead).events()

    fatjets = events.FatJet
    jets = events.Jet
    ptcut  = 250
    etacut = 2.5
    mass_cut = [100,150]
    pNet_cut = 0.9105
    good_fatjets = fatjets[(fatjets.pt>ptcut) & (np.absolute(fatjets.eta)<etacut) & (fatjets.msoftdrop>=50)]
    Signal_test = good_fatjets[ak.num(good_fatjets, axis=1)> 2]
    return Signal_test


def normalizeProcess(process,year):
    json_file = open("xsecs.json")
    config = json.load(json_file)
    xsec    = config[year][process]["xsec"]
    luminosity  = config[year]["lumi"]
    sumGen     = config[year][process]["sumGen"]
    scaling     = (xsec*luminosity)/sumGen
    return scaling

