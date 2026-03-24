import awkward as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from coffea.analysis_tools import PackedSelection
import numpy as np
import gzip
import cloudpickle
from condor.paths import H3_DIR
from tools.jerc import *

NanoAODSchema.warn_missing_crossrefs = False
jerc = JERC()

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

# Resolved Higgs candidate jet cuts
res_ptcut = 30.
res_etacut = 2.5
res_mass_cut = [90.,150.]
# loose cut = 0.0532, med_cut = 0.3040, tight_cut = 0.7476 (https://btv-wiki.docs.cern.ch/ScaleFactors/)
res_deepJetcut = 0.0532
#---------------------------------------------

def closest(masses):
    delta = abs(higgs_mass - masses)
    min_delta = ak.min(delta, axis=1)
    is_closest = (delta == min_delta)
    return is_closest


def FatJetMass(fatjet):
    return fatjet.particleNet_mass


def HbbvsQCD(fatjet):
    score = (fatjet.particleNetMD_Xbb/(fatjet.particleNetMD_Xbb+fatjet.particleNetMD_QCD))
    return score

# this is a jet mask
def precut(fatjets):
    return (fatjets.pt>ptcut) & (np.absolute(fatjets.eta)<etacut) & (fatjets.msoftdrop>min_jet_mass) & (fatjets.msoftdrop<max_jet_mass)


def PassCategory(fatjets):
    # sort the fat jets in the descending pNet HbbvsQCD score
    sorted_fatjets = fatjets[ak.argsort(-HbbvsQCD(fatjets),axis=-1)]

    # pass category: at least 1 fat jets passing the pNet cut
    return (HbbvsQCD(sorted_fatjets[:,0])>pNet_cut)

# this is a jet mask
def HiggsMassCut(fatjets):
    return (FatJetMass(fatjets)>=mass_cut[0]) & (FatJetMass(fatjets)<=mass_cut[1])

# this is a jet mask
def HiggsMassVeto(fatjets):
    return ((FatJetMass(fatjets)<mass_cut[0]) | (FatJetMass(fatjets)>mass_cut[1])) & (FatJetMass(fatjets)>min_jet_mass) & (FatJetMass(fatjets)<max_jet_mass)

# this is an event mask
def VR_b_JetMassCuts(fatjets):
    has_three_fatjets = (ak.num(fatjets, axis=1)>2)
    fatjets_padded = ak.pad_none(fatjets, 3)
    # jet mass window inverted for the 2 leading jets, applied to the 3rd one
    return ak.where(has_three_fatjets, ((FatJetMass(fatjets_padded[:,0])<mass_cut[0]) | (FatJetMass(fatjets_padded[:,0])>mass_cut[1])) & (FatJetMass(fatjets_padded[:,0])>min_jet_mass) & (FatJetMass(fatjets_padded[:,0])<max_jet_mass)
           & ((FatJetMass(fatjets_padded[:,1])<mass_cut[0]) | (FatJetMass(fatjets_padded[:,1])>mass_cut[1])) & (FatJetMass(fatjets_padded[:,1])>min_jet_mass) & (FatJetMass(fatjets_padded[:,1])<max_jet_mass)
           & (FatJetMass(fatjets_padded[:,2])>=mass_cut[0]) & (FatJetMass(fatjets_padded[:,2])<=mass_cut[1]), False)


def get_dijets(fatjets, jets, selection, event_counts, region):

    # require jets to be away from fat jets
    away_jets_mask = jets.nearest(fatjets).delta_r(jets)>delta_r_cut
    jets = jets[away_jets_mask]

    # require that there are at least 2 good away jets present in the event
    cut_name = "Away_jets_" + region
    selection.add(cut_name, ak.num(jets, axis=1)>1)

    event_counts[region]["Away_jets"] = ak.sum(selection.all("Trigger","Preselection_ge2fj","Mass_cut_" + region,"Preselection_jets",cut_name), axis=0)

    # calculate mass of all possible jet pairs and select the pair which has the mass closest to the Higgs boson mass
    dijets = ak.combinations(jets, 2, fields=['i0', 'i1'])
    dijet_masses = (dijets['i0'] + dijets['i1']).mass
    is_closest = closest(dijet_masses)
    closest_dijets = dijets[is_closest]
    # apply the jet mass cut to the closest dijets
    good_dijets = closest_dijets[((closest_dijets['i0'] + closest_dijets['i1']).mass>=res_mass_cut[0]) & ((closest_dijets['i0'] + closest_dijets['i1']).mass<=res_mass_cut[1])]

    return good_dijets


def Event_selection(fname,process,isMC,event_counts,variation="nominal",refTrigList=None,trigList=None,eventsToRead=None):
    events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema,metadata={"dataset":process},entry_stop=eventsToRead).events()


    selection = PackedSelection()

    # accept all events in the input file to add the skimming step in the cut flow
    selection.add("Skim", ak.Array([True] * len(events)))

    if isMC:
        for r in event_counts.keys():
            event_counts[r]["Skim"] = ak.sum(selection.all("Skim"), axis=0)

    # trigger selection
    if trigList != None and refTrigList == None:        
        trigger = ak.values_astype(ak.zeros_like(events.run), bool)
        for t in trigList:
            if t in events.HLT.fields:
                trigger = trigger | events.HLT[t]
        selection.add("Trigger", trigger)
        del trigger

        for r in event_counts.keys():
            event_counts[r]["Trigger"] = ak.sum(selection.all("Trigger"), axis=0)
    else:
        selection.add("Trigger", ak.Array([True] * len(events)))

    # if JEC re-application is turned off
    if variation == "fromFile":
        print("JEC re-application turned off")
        fatjets = events.FatJet
    else:
        jecTag = jecTagFromFileName(fname)
        print("JEC tag: ", jecTag)
        fatjets = getCalibratedJets(events.FatJet,events.fixedGridRhoFastjetAll,variation,jerc.fatjetFactory,jecTag) if len(events)>0 else events.FatJet

    # fat jet preselection
    fatjets = fatjets[precut(fatjets)]

    # select events with at least 2 preselected fat jets (relevant for the semiboosted channel)
    selection.add("Preselection_ge2fj", ak.num(fatjets, axis=1)>=2)

    # select events with at least 3 preselected fat jets
    selection.add("Preselection_ge3fj", ak.num(fatjets, axis=1)>2)

    for r in event_counts.keys():
        if 'semiboosted' in r:
            event_counts[r]["Preselection_fatjets"] = ak.sum(selection.all("Trigger","Preselection_ge2fj"), axis=0)
        else:
            event_counts[r]["Preselection"] = ak.sum(selection.all("Trigger","Preselection_ge3fj"), axis=0)

    # apply the jet mass cut to preselected fat jets
    # for SR (boosted and semiboosted)
    fatjets_SR = fatjets[HiggsMassCut(fatjets)]
    #---------------------------------------------
    # SR boosted
    # select events with at least 3 good fat jets
    SR_b_evtMask = (ak.num(fatjets_SR, axis=1)>2)
    selection.add("Mass_cut_SR_boosted", SR_b_evtMask)

    event_counts["SR_boosted"]["Mass_cut"] = ak.sum(selection.all("Trigger","Preselection_ge3fj","Mass_cut_SR_boosted"), axis=0)

    # select events in the Pass category of the SR boosted. Pass on only the 3 leading fat jets (to avoid events passing or failing due to the 4th or higher leading fat jet)
    selection.add("SR_boosted_Pass", ak.where(SR_b_evtMask, PassCategory(ak.pad_none(fatjets_SR, 3)[:,0:3]), False))

    # define Pass and Fail category event masks
    SR_b_Pass_evtMask = selection.all("Trigger","Preselection_ge3fj","Mass_cut_SR_boosted","SR_boosted_Pass")
    SR_b_Fail_evtMask = selection.require(Trigger=True,Preselection_ge3fj=True,Mass_cut_SR_boosted=True,SR_boosted_Pass=False)
    #---------------------------------------------
    # VR boosted
    # apply the VR jet mass cuts to the 3 leading (in pT) fat jets and reject overlap with the SR
    VR_b_evtMask = (VR_b_JetMassCuts(fatjets) & ~SR_b_evtMask)
    selection.add("Mass_cut_VR_boosted", VR_b_evtMask)

    event_counts["VR_boosted"]["Mass_cut"] = ak.sum(selection.all("Trigger","Preselection_ge3fj","Mass_cut_VR_boosted"), axis=0)

    # select events in the Pass category of the VR boosted. Pass on only the 3 leading fat jets (to avoid events passing or failing due to the pNet score of the 4th or higher leading fat jet)
    selection.add("VR_boosted_Pass", ak.where(VR_b_evtMask, PassCategory(ak.pad_none(fatjets, 3)[:,0:3]), False))

    # define Pass and Fail category event masks
    VR_b_Pass_evtMask = selection.all("Trigger","Preselection_ge3fj","Mass_cut_VR_boosted","VR_boosted_Pass")
    VR_b_Fail_evtMask = selection.require(Trigger=True,Preselection_ge3fj=True,Mass_cut_VR_boosted=True,VR_boosted_Pass=False)
    #---------------------------------------------
    # get standard jets
    # if JEC re-application is turned off
    if variation == "fromFile":
        jets = events.Jet
    else:
        jets = getCalibratedJets(events.Jet,events.fixedGridRhoFastjetAll,variation,jerc.jetFactory,jecTag) if len(events)>0 else events.Jet

    # apply preselection to the standard jets
    jets = jets[(jets.pt > res_ptcut) & (np.absolute(jets.eta) < res_etacut) & (jets.btagDeepFlavB>res_deepJetcut)]

    # require that there are at least 2 good jets present in the event
    selection.add("Preselection_jets", ak.num(jets, axis=1)>1)
    #---------------------------------------------
    # SR semiboosted
    # select events with exactly 2 good fat jets and reject overlap with the VR boosted (by construction orthogonal to the SR boosted)
    SR_sb_evtMask = ((ak.num(fatjets_SR, axis=1)==2) & ~VR_b_evtMask)
    selection.add("Mass_cut_SR_semiboosted", SR_sb_evtMask)

    event_counts["SR_semiboosted"]["Mass_cut_fatjets"] = ak.sum(selection.all("Trigger","Preselection_ge2fj","Mass_cut_SR_semiboosted"), axis=0)

    event_counts["SR_semiboosted"]["Preselection_jets"] = ak.sum(selection.all("Trigger","Preselection_ge2fj","Mass_cut_SR_semiboosted","Preselection_jets"), axis=0)

    # get good dijets
    good_dijets_SR_sb = get_dijets(fatjets_SR, jets, selection, event_counts, "SR_semiboosted")

    # select events with at least 1 good dijet (by construction there can be at most 1 per event)
    selection.add("Good_dijet_SR_semiboosted", ak.num(good_dijets_SR_sb, axis=1)>0)

    event_counts["SR_semiboosted"]["Good_dijet"] = ak.sum(selection.all("Trigger","Preselection_ge2fj","Mass_cut_SR_semiboosted","Preselection_jets","Away_jets_SR_semiboosted","Good_dijet_SR_semiboosted"), axis=0)

    # select events in the Pass category of the SR semiboosted
    selection.add("SR_semiboosted_Pass", ak.where(SR_sb_evtMask, PassCategory(ak.pad_none(fatjets_SR, 1)), False))

    # define Pass and Fail category event masks
    SR_sb_Pass_evtMask = selection.all("Trigger","Preselection_ge2fj","Mass_cut_SR_semiboosted","Preselection_jets","Away_jets_SR_semiboosted","Good_dijet_SR_semiboosted","SR_semiboosted_Pass")
    SR_sb_Fail_evtMask = selection.require(Trigger=True,Preselection_ge2fj=True,Mass_cut_SR_semiboosted=True,Preselection_jets=True,Away_jets_SR_semiboosted=True,Good_dijet_SR_semiboosted=True,SR_semiboosted_Pass=False)
    #---------------------------------------------
    # VR semiboosted
    # select events with 2 good leading fat jets and reject overlap with both SRs and the VR boosted
    VR_sb_evtMask = (ak.num(fatjets[HiggsMassVeto(fatjets[:,0:2])], axis=1)==2) & ~(SR_b_evtMask | SR_sb_evtMask | VR_b_evtMask)
    selection.add("Mass_cut_VR_semiboosted", VR_sb_evtMask)

    event_counts["VR_semiboosted"]["Mass_cut_fatjets"] = ak.sum(selection.all("Trigger","Preselection_ge2fj","Mass_cut_VR_semiboosted"), axis=0)

    event_counts["VR_semiboosted"]["Preselection_jets"] = ak.sum(selection.all("Trigger","Preselection_ge2fj","Mass_cut_VR_semiboosted","Preselection_jets"), axis=0)

    # get good dijets
    good_dijets_VR_sb = get_dijets(fatjets[:,0:2], jets, selection, event_counts, "VR_semiboosted")

    # select events with at least 1 good dijet (by construction there can be at most 1 per event)
    selection.add("Good_dijet_VR_semiboosted", ak.num(good_dijets_VR_sb, axis=1)>0)

    event_counts["VR_semiboosted"]["Good_dijet"] = ak.sum(selection.all("Trigger","Preselection_ge2fj","Mass_cut_VR_semiboosted","Preselection_jets","Away_jets_VR_semiboosted","Good_dijet_VR_semiboosted"), axis=0)

    # select events in the Pass category of the SR semiboosted
    selection.add("VR_semiboosted_Pass", ak.where(VR_sb_evtMask, PassCategory(ak.pad_none(fatjets[:,0:2], 1)), False))

    # define Pass and Fail category event masks
    VR_sb_Pass_evtMask = selection.all("Trigger","Preselection_ge2fj","Mass_cut_VR_semiboosted","Preselection_jets","Away_jets_VR_semiboosted","Good_dijet_VR_semiboosted","VR_semiboosted_Pass")
    VR_sb_Fail_evtMask = selection.require(Trigger=True,Preselection_ge2fj=True,Mass_cut_VR_semiboosted=True,Preselection_jets=True,Away_jets_VR_semiboosted=True,Good_dijet_VR_semiboosted=True,VR_semiboosted_Pass=False)
    #---------------------------------------------

    return events[SR_b_Fail_evtMask], events[SR_b_Pass_evtMask], fatjets_SR[SR_b_Fail_evtMask], fatjets_SR[SR_b_Pass_evtMask], events[VR_b_Fail_evtMask], events[VR_b_Pass_evtMask], fatjets[VR_b_Fail_evtMask], fatjets[VR_b_Pass_evtMask], events[SR_sb_Fail_evtMask], events[SR_sb_Pass_evtMask], fatjets_SR[SR_sb_Fail_evtMask], fatjets_SR[SR_sb_Pass_evtMask], good_dijets_SR_sb[SR_sb_Fail_evtMask], good_dijets_SR_sb[SR_sb_Pass_evtMask], events[VR_sb_Fail_evtMask], events[VR_sb_Pass_evtMask], fatjets[VR_sb_Fail_evtMask], fatjets[VR_sb_Pass_evtMask], good_dijets_VR_sb[VR_sb_Fail_evtMask], good_dijets_VR_sb[VR_sb_Pass_evtMask]
