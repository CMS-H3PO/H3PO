import awkward as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import numpy as np
import json
import gzip
import cloudpickle
from condor.paths import H3_DIR

#---------------------------------------------
# Selection cuts
#---------------------------------------------
higgs_mass = 125.
delta_r_cut = 0.8
min_jet_mass = 60.
max_jet_mass = 250.

# FatJet cuts
ptcut = 250.
etacut = 2.5
mass_cut = [100.,150.]
pNet_cut = 0.9105


def addJECVariables(jets, event_rho,isData):
    jets["pt_raw"] = (1 - jets.rawFactor)*jets.pt
    jets["mass_raw"] = (1 - jets.rawFactor)*jets.mass
    jets["event_rho"] = ak.broadcast_arrays(event_rho, jets.pt)[0]
    if not isData:
        jets["pt_gen"] = ak.values_astype(ak.fill_none(jets.matched_gen.pt, 0), np.float32)
    return jets


def yearFromInputFile(inputFile):
    if("2016APV" in inputFile):
        return "2016APV"
    #Because 2016 repeats, ordering is important
    elif("2016" in inputFile):
        return "2016"
    elif("2017" in inputFile):
        return "2017"
    elif("2018" in inputFile):
        return "2018" 
    else:       
        raise ValueError('Could not determine year from input file: {0}'.format(inputFile))


def jecTagFromFileName(fname):
    year    = yearFromInputFile(fname)
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


def FailPassCategories(events, fatjets, jets=None):
    # sort the fat jets in the descending pNet HbbvsQCD score
    sorted_fatjets = fatjets[ak.argsort(-HbbvsQCD(fatjets),axis=-1)]

    # fail region: 0 fat jets passing the pNet cut
    # pass region: at least 1 fat jets passing the pNet cut
    fail_mask = (HbbvsQCD(sorted_fatjets[:,0])<=pNet_cut)
    pass_mask = (HbbvsQCD(sorted_fatjets[:,0])>pNet_cut)
    if jets is not None:
        return events[fail_mask], events[pass_mask], fatjets[fail_mask], fatjets[pass_mask], jets[fail_mask], jets[pass_mask]
    else:
        return events[fail_mask], events[pass_mask], fatjets[fail_mask], fatjets[pass_mask]


def getCalibratedAK8(events,variation,fatjetFactory,jecTag):
    AK8jecCache         = {}
    if("mc" in jecTag):
        isData = False
    else:
        isData = True
    fatjetsCalib        = fatjetFactory[jecTag].build(addJECVariables(events.FatJet, events.fixedGridRhoFastjetAll,isData), AK8jecCache)

    if(variation=="nominal"):
        fatjets         = fatjetsCalib
    elif(variation=="jesUp"):
        fatjets         = fatjetsCalib.JES_jes.up
    elif(variation=="jesDown"):
        fatjets         = fatjetsCalib.JES_jes.down
    elif(variation=="jerUp"):
        fatjets         = fatjetsCalib.JER.up
    elif(variation=="jerDown"):
        fatjets         = fatjetsCalib.JER.down
    else:       
        raise ValueError('Invalid variation: ', variation)

    return fatjets







def HbbvsQCD(fatjet):
    score = (fatjet.particleNetMD_Xbb/(fatjet.particleNetMD_Xbb+fatjet.particleNetMD_QCD))
    return score


def FatJetMass_sd(fatjet):
	return fatjet.msoftdrop

def FatJetMass_pn(fatjet):
	return fatjet.particleNet_mass

# this is a jet mask
def precut(fatjets):
    return (fatjets.pt>ptcut) & (np.absolute(fatjets.eta)<etacut)

# this is an event mask
def SR_b_JetMass_evtMask(fatjets):
    # one jet mass is in mass window [ mass_cut[0], mass_cut[1] ], one grater than mass_cut[1]
    return ( ( ( FatJetMass_sd(fatjets[:,0]) >= mass_cut[0] ) & ( FatJetMass_sd(fatjets[:,0]) <= mass_cut[1] ) & ( FatJetMass_sd(fatjets[:,1]) > max_jet_mass ) )
				| ( ( FatJetMass_sd(fatjets[:,1]) >= mass_cut[0] ) & ( FatJetMass_sd(fatjets[:,1]) <= mass_cut[1] ) & ( FatJetMass_sd(fatjets[:,0]) > max_jet_mass ) ) )
	


# this is an event mask
def VR_b_JetMass_evtMask(fatjets):
    # jet mass window inverted for the Higgs candidate, Y candidate is same as in SR
    return ( ( ( ( FatJetMass_sd(fatjets[:,0]) < mass_cut[0] ) | ( FatJetMass_sd(fatjets[:,0]) > mass_cut[1] ) ) & ( FatJetMass_sd(fatjets[:,0]) > min_jet_mass ) & ( FatJetMass_sd(fatjets[:,0]) < max_jet_mass )
        & ( FatJetMass_sd(fatjets[:,1]) > max_jet_mass ) )
		| ( ( ( FatJetMass_sd(fatjets[:,1]) < mass_cut[0] ) | ( FatJetMass_sd(fatjets[:,1]) > mass_cut[1] ) ) & ( FatJetMass_sd(fatjets[:,1]) > min_jet_mass ) & ( FatJetMass_sd(fatjets[:,1]) < max_jet_mass ) 
		&  ( FatJetMass_sd(fatjets[:,0]) > max_jet_mass ) ) )

#this is an event cut
#phicut = 2
#def phi_evtMask(fatjets):
#	return (abs(fatjets[:,0].delta_phi(fatjets[:,1])) > phicut)



#this is a jet mask
def higgsCandidateMask(fatjets):
	return (FatJetMass_sd(fatjets) >= mass_cut[0]) & (FatJetMass_sd(fatjets) <= mass_cut[1])

#this is a jet mask
def yCandidateMask(fatjets):
	return FatJetMass_sd(fatjets) >= max_jet_mass



def Event_selection(fname,process,event_counts,variation="nominal",refTrigList=None,trigList=None,eventsToRead=None):
    events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema,metadata={"dataset":process},entry_stop=eventsToRead).events()

    if "JetHT" not in process:
        for r in event_counts.keys():
            event_counts[r]["Skim"] = len(events)

    if trigList != None and refTrigList == None:
        triggerBits = np.array([events.HLT[t] for t in trigList if t in events.HLT.fields])
        triggerMask = np.logical_or.reduce(triggerBits, axis=0)
        events = events[triggerMask]

        for r in event_counts.keys():
            event_counts[r]["Trigger"] = len(events)

    # if JEC re-application is turned off
    if variation == "fromFile":
        print("JEC re-application turned off")
        fatjets = events.FatJet
    else:
        with gzip.open(H3_DIR+"/../data/jec/jme_UL_pickled.pkl") as fin:
            jmeDB           = cloudpickle.load(fin)
            fatjetFactory   = jmeDB["fatjet_factory"]
            jetFactory      = jmeDB["jet_factory"]

        jecTag              = jecTagFromFileName(fname)
        print("JEC tag: ", jecTag)
        fatjets             = getCalibratedAK8(events,variation,fatjetFactory,jecTag) if len(events)>0 else events.FatJet

    # fat jet preselection
    fatjets = fatjets[precut(fatjets)]


    # select events with at least 2 preselected fat jets
    events  =  events[ak.num(fatjets, axis=1)>1]
    fatjets = fatjets[ak.num(fatjets, axis=1)>1]


    for r in event_counts.keys():
        event_counts[r]["Preselection"] = len(fatjets)


    # SR boosted
    # apply the SR jet mass cut to the 2 leading (in pT) fat jets.
	# Pass on only the 2 leading fat jets (to avoid events passing or failing due to the 3rd or higher leading fat jet)
    fatjets_SR_b_evtMask = SR_b_JetMass_evtMask(fatjets)# & phi_evtMask(fatjets)
    events_SR_b  =     events[fatjets_SR_b_evtMask]
    fatjets_SR_b =    fatjets[fatjets_SR_b_evtMask][:,0:2]

    # VR boosted
    # apply the VR jet mass cuts to the 2 leading (in pT) fat jets and reject overlap with the SR.
    # Pass on only the 2 leading fat jets (to avoid events passing or failing due to the pNet score of the 3th or higher leading fat jet)
    fatjets_VR_b_evtMask = VR_b_JetMass_evtMask(fatjets)
    events_VR_b  =  events[fatjets_VR_b_evtMask & ~fatjets_SR_b_evtMask]
    fatjets_VR_b = fatjets[fatjets_VR_b_evtMask & ~fatjets_SR_b_evtMask][:,0:2]

    event_counts["SR_boosted"]["Mass_cut"] = len(fatjets_SR_b)
    event_counts["VR_boosted"]["Mass_cut"] = len(fatjets_VR_b)

    return *FailPassCategories(events_SR_b, fatjets_SR_b), *FailPassCategories(events_VR_b, fatjets_VR_b)
