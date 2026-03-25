import awkward as ak
import numpy as np
import gzip
import cloudpickle
from condor.paths import H3_DIR
from utils.utils import *


class JERC:
    def __init__(self):
        jmeDB              = cloudpickle.load(gzip.open(H3_DIR+"/../data/jec/jme_UL_pickled.pkl"))
        self.fatjetFactory = jmeDB["fatjet_factory"]
        self.jetFactory    = jmeDB["jet_factory"]


def jecTagFromFileName(fname):
    year = yearFromInputFile(fname)
    #MC
    if not "JetHT" in fname:
        jecTag  = year+"mc"
        return jecTag
    
    #Data
    era = fname.split("JetHT"+year)[1][0]#E.g.targetting "B" in JetHT2018B: first character in a string AFTER the JetHT$year
    if year=="2016APV":
        if era in "BCD":
            return "2016APVRunBCD"
        else:
            return "2016APVRunEF"

    elif year=="2016":
        return "2016RunFGH"

    elif year=="2017":
        jecTag = year+"Run"+era
        return jecTag

    elif year=="2018":
        jecTag = year+"Run"+era
        return jecTag


def addJECVariables(jets,event_rho,isData):
    jets["pt_raw"] = (1 - jets.rawFactor)*jets.pt
    jets["mass_raw"] = (1 - jets.rawFactor)*jets.mass
    jets["event_rho"] = ak.broadcast_arrays(event_rho, jets.pt)[0]
    if not isData:
        jets["pt_gen"] = ak.values_astype(ak.fill_none(jets.matched_gen.pt, 0), np.float32)
    return jets 
  
  
def getCalibratedJets(jets,event_rho,variation,jetFactory,jecTag):
    jecCache = {}
    if("mc" in jecTag):
        isData = False
    else:
        isData = True
    jetsCalib = jetFactory[jecTag].build(addJECVariables(jets,event_rho,isData), jecCache)
        
    if(variation=="nominal"):
        jets         = jetsCalib
    elif(variation=="jesUp"):
        jets         = jetsCalib.JES_jes.up
    elif(variation=="jesDown"):
        jets         = jetsCalib.JES_jes.down
    elif(variation=="jerUp"):
        jets         = jetsCalib.JER.up
    elif(variation=="jerDown"):
        jets         = jetsCalib.JER.down
    else:       
        raise ValueError('Invalid variation: ', variation)

    return jets
