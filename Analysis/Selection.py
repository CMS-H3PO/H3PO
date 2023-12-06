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
min_jet_mass = 50.

# FatJet cuts
ptcut = 250.
etacut = 2.5
mass_cut = [100.,150.]
pNet_cut = 0.9105

# Resolved jet cuts
res_ptcut = 30.
res_etacut = 2.5
res_mass_cut = [90.,150.]
# loose cut = 0.0532, med_cut = 0.3040, tight_cut = 0.7476 , https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL17   
res_deepBcut = 0.0532
#---------------------------------------------
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


def closest(masses):
    delta = abs(higgs_mass - masses)
    min_delta = ak.min(delta, axis=1)
    is_closest = (delta == min_delta)
    return is_closest


def HbbvsQCD(fatjet):
    score = (fatjet.particleNetMD_Xbb/(fatjet.particleNetMD_Xbb+fatjet.particleNetMD_QCD))
    return score

# this is a jet mask
def precut(fatjets):
    return (fatjets.pt>ptcut) & (np.absolute(fatjets.eta)<etacut)


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

# this is a jet mask
def HiggsMassCut(fatjets):
    return (fatjets.msoftdrop>=mass_cut[0]) & (fatjets.msoftdrop<=mass_cut[1])

# this is a jet mask
def HiggsMassVeto(fatjets):
    return ((fatjets.msoftdrop<mass_cut[0]) | (fatjets.msoftdrop>mass_cut[1])) & (fatjets.msoftdrop>min_jet_mass)

# this is an event mask
def VR_b_JetMass_evtMask(fatjets):
    # jet mass window inverted for the 2 leading jets, applied to the 3rd one
    return (((fatjets[:,0].msoftdrop<mass_cut[0]) | (fatjets.msoftdrop[:,0]>mass_cut[1])) & (fatjets[:,0].msoftdrop>min_jet_mass) 
          & ((fatjets[:,1].msoftdrop<mass_cut[0]) | (fatjets[:,1].msoftdrop>mass_cut[1])) & (fatjets[:,1].msoftdrop>min_jet_mass)  
          & (fatjets[:,2].msoftdrop>=mass_cut[0]) & (fatjets[:,2].msoftdrop<=mass_cut[1]))


def get_dijets(fatjets, jets, events, event_counts, addCounts=False):
    # apply preselection to the resolved jets
    jets = jets[(jets.pt > res_ptcut) & (np.absolute(jets.eta) < res_etacut) & (jets.btagDeepB>res_deepBcut)]

    # require that there are at least 2 good jets present in the event
    fatjets = fatjets[ak.num(jets, axis=1)>1]
    events  =  events[ak.num(jets, axis=1)>1]
    jets    =    jets[ak.num(jets, axis=1)>1]

    if addCounts:
        event_counts["Preselection_jets"] += len(fatjets)
    else:
        event_counts["Preselection_jets"] = len(fatjets)

    # require jets to be away from fat jets
    away_jets_mask = jets.nearest(fatjets).delta_r(jets)>delta_r_cut
    jets = jets[away_jets_mask]

    # require that there are at least 2 good away jets present in the event
    fatjets = fatjets[ak.num(jets, axis=1)>1]
    events  =  events[ak.num(jets, axis=1)>1]
    jets    =    jets[ak.num(jets, axis=1)>1]

    if addCounts:
        event_counts["Away_jets"] += len(fatjets)
    else:
        event_counts["Away_jets"] = len(fatjets)

    # calculate mass of all possible jet pairs and select the pair which has the mass closest to the Higgs boson mass
    dijets = ak.combinations(jets, 2, fields=['i0', 'i1'])
    dijet_masses = (dijets['i0'] + dijets['i1']).mass
    is_closest = closest(dijet_masses)
    closest_dijets = dijets[is_closest]
    # apply the jet mass cut to the closest dijets
    good_dijets = closest_dijets[((closest_dijets['i0'] + closest_dijets['i1']).mass>=res_mass_cut[0]) & ((closest_dijets['i0'] + closest_dijets['i1']).mass<=res_mass_cut[1])]
    
    # select events with at least 1 good dijet (by construction there can be at most 1 per event)
    fatjets     =     fatjets[ak.num(good_dijets, axis=1)>0]
    events      =      events[ak.num(good_dijets, axis=1)>0]
    good_dijets = good_dijets[ak.num(good_dijets, axis=1)>0]
    
    if addCounts:
        event_counts["Good_dijet"] += len(fatjets)
    else:
        event_counts["Good_dijet"] = len(fatjets)
    
    return fatjets, good_dijets, events


def getCalibratedAK4(events,variation,jetFactory,jecTag):
    AK4jecCache         = {}
    if("mc" in jecTag):
        isData = False
    else:
        isData = True
    jetsCalib           = jetFactory[jecTag].build(addJECVariables(events.Jet, events.fixedGridRhoFastjetAll,isData), AK4jecCache)
        
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

def Event_selection(fname,process,event_counts,variation="nominal",refTrigList=None,trigList=None,eventsToRead=None):
    events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema,metadata={"dataset":process},entry_stop=eventsToRead).events()

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
        fatjets             = getCalibratedAK8(events,variation,fatjetFactory,jecTag)

    # fat jet preselection
    fatjets = fatjets[precut(fatjets)]

    # select events with exactly 2 preselected fat jets
    events_eq2  =  events[ak.num(fatjets, axis=1)==2]
    fatjets_eq2 = fatjets[ak.num(fatjets, axis=1)==2]

    # select events with at least 3 preselected fat jets
    events  =  events[ak.num(fatjets, axis=1)>2]
    fatjets = fatjets[ak.num(fatjets, axis=1)>2]

    for r in event_counts.keys():
        if 'semiboosted' in r:
            event_counts[r]["Preselection_fatjets"] = (len(fatjets) + len(fatjets_eq2))
        else:
            event_counts[r]["Preselection"] = len(fatjets)
    
    # apply the jet mass cut to preselected fat jets
    # for SR (boosted and semiboosted)
    fatjets_SR = fatjets[HiggsMassCut(fatjets)]

    # SR boosted
    # select events with at least 3 good fat jets. Pass on only the 3 leading fat jets (to avoid events passing or failing due to the 4th or higher leading fat jet)
    fatjets_SR_b_evtMask = (ak.num(fatjets_SR, axis=1)>2)
    events_SR_b  =     events[fatjets_SR_b_evtMask]
    fatjets_SR_b = fatjets_SR[fatjets_SR_b_evtMask][:,0:3]

    # VR boosted
    # apply the VR jet mass cuts to the 3 leading (in pT) fat jets and reject overlap with the SR.
    # Pass on only the 3 leading fat jets (to avoid events passing or failing due to the pNet score of the 4th or higher leading fat jet)
    fatjets_VR_b_evtMask = VR_b_JetMass_evtMask(fatjets)
    events_VR_b  =  events[fatjets_VR_b_evtMask & ~fatjets_SR_b_evtMask]
    fatjets_VR_b = fatjets[fatjets_VR_b_evtMask & ~fatjets_SR_b_evtMask][:,0:3]

    event_counts["SR_boosted"]["Mass_cut"] = len(fatjets_SR_b)
    event_counts["VR_boosted"]["Mass_cut"] = len(fatjets_VR_b)

    # SR semiboosted
    # select events with exactly 2 good fat jets and reject overlap with the VR boosted (by construction orthogonal to the SR boosted)
    fatjets_SR_sb_evtMask = (ak.num(fatjets_SR, axis=1)==2)
    events_SR_sb  =     events[fatjets_SR_sb_evtMask & ~(fatjets_VR_b_evtMask)]
    fatjets_SR_sb = fatjets_SR[fatjets_SR_sb_evtMask & ~(fatjets_VR_b_evtMask)]
    # get resolved jets from selected events
    # if JEC re-application is turned off
    if variation == "fromFile":
        jets_SR_sb = events_SR_sb.Jet
    else:
        jets_SR_sb = getCalibratedAK4(events_SR_sb,variation,jetFactory,jecTag)

    event_counts["SR_semiboosted"]["Mass_cut_fatjets"] = len(fatjets_SR_sb)

    # get good dijets
    fatjets_SR_sb, good_dijets_SR_sb, events_SR_sb = get_dijets(fatjets_SR_sb, jets_SR_sb, events_SR_sb, event_counts["SR_semiboosted"])

    # VR semiboosted
    # select events with exactly 2 good fat jets and reject overlap with both SR and the VR boosted
    fatjets_VR_sb = fatjets[:,0:2]
    fatjets_VR_sb = fatjets_VR_sb[HiggsMassVeto(fatjets_VR_sb)]
    fatjets_VR_sb_evtMask = (ak.num(fatjets_VR_sb, axis=1)==2)
    events_VR_sb  =        events[fatjets_VR_sb_evtMask & ~(fatjets_SR_b_evtMask | fatjets_SR_sb_evtMask | fatjets_VR_b_evtMask)]
    fatjets_VR_sb = fatjets_VR_sb[fatjets_VR_sb_evtMask & ~(fatjets_SR_b_evtMask | fatjets_SR_sb_evtMask | fatjets_VR_b_evtMask)]
    # get resolved jets from selected events
    # if JEC re-application is turned off
    if variation == "fromFile":
        jets_VR_sb = events_VR_sb.Jet
    else:
        jets_VR_sb = getCalibratedAK4(events_VR_sb,variation,jetFactory,jecTag)

    event_counts["VR_semiboosted"]["Mass_cut_fatjets"] = len(fatjets_VR_sb)
    
    # get good dijets
    fatjets_VR_sb, good_dijets_VR_sb, events_VR_sb = get_dijets(fatjets_VR_sb, jets_VR_sb, events_VR_sb, event_counts["VR_semiboosted"])
    
    # SR semiboosted (==2 fatjets)
    # apply the jet mass cut to preselected fat jets
    fatjets_SR_sb_eq2 = fatjets_eq2[HiggsMassCut(fatjets_eq2)]
    # select events with exactly 2 good fat jets
    events_SR_sb_eq2  =        events_eq2[ak.num(fatjets_SR_sb_eq2, axis=1)==2]
    fatjets_SR_sb_eq2 = fatjets_SR_sb_eq2[ak.num(fatjets_SR_sb_eq2, axis=1)==2]
    # get resolved jets from selected events
    # if JEC re-application is turned off
    if variation == "fromFile":
        jets_SR_sb_eq2 = events_SR_sb_eq2.Jet    
    else:
        jets_SR_sb_eq2 = getCalibratedAK4(events_SR_sb_eq2,variation,jetFactory,jecTag)

    event_counts["SR_semiboosted"]["Mass_cut_fatjets"] += len(fatjets_SR_sb_eq2)

    # get good dijets
    fatjets_SR_sb_eq2, good_dijets_SR_sb_eq2, events_SR_sb_eq2 = get_dijets(fatjets_SR_sb_eq2, jets_SR_sb_eq2, events_SR_sb_eq2, event_counts["SR_semiboosted"], True)

    # VR semiboosted (==2 fatjets)
    # apply the jet mass cut to preselected fat jets
    fatjets_VR_sb_eq2 = fatjets_eq2[HiggsMassVeto(fatjets_eq2)]
    # select events with exactly 2 good fat jets
    events_VR_sb_eq2  =        events_eq2[ak.num(fatjets_VR_sb_eq2, axis=1)==2]
    fatjets_VR_sb_eq2 = fatjets_VR_sb_eq2[ak.num(fatjets_VR_sb_eq2, axis=1)==2]
    # get resolved jets from selected events
    # if JEC re-application is turned off
    if variation == "fromFile":
        jets_VR_sb_eq2 = events_VR_sb_eq2.Jet
    else:
        jets_VR_sb_eq2 = getCalibratedAK4(events_VR_sb_eq2,variation,jetFactory,jecTag)

    event_counts["VR_semiboosted"]["Mass_cut_fatjets"] += len(fatjets_VR_sb_eq2)

    # get good dijets
    fatjets_VR_sb_eq2, good_dijets_VR_sb_eq2, events_VR_sb_eq2 = get_dijets(fatjets_VR_sb_eq2, jets_VR_sb_eq2, events_VR_sb_eq2, event_counts["VR_semiboosted"], True)

    return *FailPassCategories(events_SR_b, fatjets_SR_b), *FailPassCategories(events_VR_b, fatjets_VR_b), *FailPassCategories(events_SR_sb, fatjets_SR_sb, good_dijets_SR_sb), *FailPassCategories(events_VR_sb, fatjets_VR_sb, good_dijets_VR_sb), *FailPassCategories(events_SR_sb_eq2, fatjets_SR_sb_eq2, good_dijets_SR_sb_eq2), *FailPassCategories(events_VR_sb_eq2, fatjets_VR_sb_eq2, good_dijets_VR_sb_eq2)
