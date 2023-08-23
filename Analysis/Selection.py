import awkward as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import numpy as np
import json


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


def closest(masses):
    delta = abs(higgs_mass - masses)
    closest_masses = ak.min(delta, axis=1)
    is_closest = (delta == closest_masses)
    return is_closest


def HbbvsQCD(fatjet):
    score = (fatjet.particleNetMD_Xbb/(fatjet.particleNetMD_Xbb+fatjet.particleNetMD_QCD))
    return score


def precut(fatjets):
    return (fatjets.pt>ptcut) & (np.absolute(fatjets.eta)<etacut)


def FailPassCategories(good_fatjets)
    # sort the 3 leading (in pT) fat jets in descending pNet HbbvsQCD score
    # (this is to prevent events being selected due to the 4th or higher leading jet having a high pNet score)
    sorted_fatjets_3 = good_fatjets[:,0:3]
    sorted_fatjets_3 = sorted_fatjets_3[ak.argsort(-HbbvsQCD(sorted_fatjets_3),axis=-1)]

    # fail region: 0 out of the 3 leading fat jets passing the pNet cut
    # pass region: at least 1 out of the 3 leading fat jets passing the pNet cut
    return good_fatjets[HbbvsQCD(sorted_fatjets_3[:,0])<pNet_cut], good_fatjets[HbbvsQCD(sorted_fatjets_3[:,0])>pNet_cut]


def VR_mask(fatjets):
    return (((fatjets[:,0].msoftdrop<mass_cut[0]) | (fatjets.msoftdrop[:,0]>mass_cut[1])) & (fatjets[:,0].msoftdrop>min_jet_mass) 
    & (fatjets[:,1].msoftdrop>min_jet_mass) & ((fatjets[:,1].msoftdrop<mass_cut[0]) | (fatjets[:,1].msoftdrop>mass_cut[1])) 
    & (fatjets[:,2].msoftdrop>=mass_cut[0]) & (fatjets[:,2].msoftdrop<=mass_cut[1]))


def normalizeProcess(process,year):
    json_file = open("xsecs.json")
    config = json.load(json_file)
    xsec    = config[year][process]["xsec"]
    luminosity  = config[year]["lumi"]
    sumGen     = config[year][process]["sumGen"]
    scaling     = (xsec*luminosity)/sumGen
    return scaling


def Signal_boosted(fname,process,eventsToRead=None):
    events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema,metadata={"dataset":process},entry_stop=eventsToRead).events()
    
    fatjets = events.FatJet
    
    # fat jets preselection
    good_fatjets = fatjets[precut(fatjets)]
    
    # select events with at least 3 preselected fat jets
    good_fatjets = good_fatjets[ak.num(good_fatjets, axis=1)>2]

    # require that the 3 leading (in pT) fat jets pass the jet mass cut
    good_fatjets_3 = good_fatjets[:,0:3]
    good_fatjets_3 = good_fatjets_3[(good_fatjets_3.msoftdrop>=mass_cut[0]) & (good_fatjets_3.msoftdrop<=mass_cut[1])]

    # select events with at least 3 good fat jets
    good_fatjets_SR_boosted = good_fatjets[ak.num(good_fatjets_3, axis=1)>2]

    return FailPassCategories(good_fatjets_SR_boosted)


def Validation_boosted(fname,process,eventsToRead=None):
    events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema,metadata={"dataset":process},entry_stop=eventsToRead).events()

    fatjets = events.FatJet
    
    # fat jets preselection
    good_fatjets = fatjets[precut(fatjets)]
    
    # select events with at least 3 preselected fat jets
    good_fatjets = good_fatjets[ak.num(good_fatjets, axis=1)>2]

    # require that the 2 leading (in pT) fat jets fail the jet mass cut and the 3rd one passes it
    good_fatjets_3 = good_fatjets[:,0:3]
    good_fatjets_3 = good_fatjets_3[VR_mask(good_fatjets_3)]

    # select events with at least 3 good fat jets
    good_fatjets_VR_boosted = good_fatjets[ak.num(good_fatjets_3, axis=1)>2]
    
    return FailPassCategories(good_fatjets_VR_boosted)


def Signal_semiboosted(fname,process,eventsToRead=None):
    events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema,metadata={"dataset":process},entry_stop=eventsToRead).events()

    fatjets = events.FatJet

    # Apply presection on Fatjets
    good_fatjets = fatjets[precut(fatjets) & (fatjets.msoftdrop>=mass_cut[0]) & (fatjets.msoftdrop<=mass_cut[1])]

    # Require that there are exactly 2 fatjets present in the event
    events_semiboosted_fatjets = events[ak.num(good_fatjets, axis=1) == 2]

    # Select jets array from selected events with 2 fatjets
    jets = events_semiboosted_fatjets.Jet

    # Apply preselection on resolved jets
    good_jets = jets[(jets.pt > res_ptcut) & (np.absolute(jets.eta) < res_etacut) & (jets.btagDeepB>res_deepBcut)]

    # Require that there are atleast two jets present in the event
    events_semiboosted_jets = events_semiboosted_fatjets[ak.num(good_jets)>1]

    # Require jets to be away from fatjets, delta_r = 0.8
    good_pairs = events_semiboosted_jets.Jet.nearest(events_semiboosted_jets.FatJet).delta_r(events_semiboosted_jets.Jet)>delta_r_cut
    good_paired_jets = events_semiboosted_jets.Jet[good_pairs]

    events_semiboosted_pairs = events_semiboosted_jets[ak.num(good_paired_jets, axis=1) >= 2]

    # Calculate mass of jet pairs and select the pair which has closest mass to higgs - 125
    dijets = ak.combinations(events_semiboosted_pairs.Jet, 2, fields=['i0', 'i1'])
    dijet_masses = (dijets['i0'] + dijets['i1']).mass
    is_closest = closest(dijet_masses)
    closest_dijets = dijets[is_closest]
    mass_jets = closest_dijets[((closest_dijets['i0'] + closest_dijets['i1']).mass>=res_mass_cut[0]) & ((closest_dijets['i0'] + closest_dijets['i1']).mass<=res_mass_cut[1])]
    events_semiboosted = events_semiboosted_pairs[ak.num(mass_jets,axis=1)>0]

    # sort fat jets in descending pNet HbbvsQCD score
    sorted_fatjets = events_semiboosted.FatJet[ak.argsort(-HbbvsQCD(events_semiboosted.FatJet),axis=-1)]

    # fail region: 0 fat jets passing the pNet cut
    events_semiboosted_failed = events_semiboosted[HbbvsQCD(sorted_fatjets[:,0])<pNet_cut]
    events_semiboosted_fail = events_semiboosted_failed[ak.num(events_semiboosted_failed.FatJet,axis=1)==2]
    # pass region: at least 1 fat jets passing the pNet cut
    events_semiboosted_passed = events_semiboosted[HbbvsQCD(sorted_fatjets[:,0])>pNet_cut]
    events_semiboosted_pass = events_semiboosted_passed[ak.num(events_semiboosted_passed.FatJet,axis=1)==2]


    return events_semiboosted_fail.FatJet,events_semiboosted_pass.FatJet,events_semiboosted_fail.Jet,events_semiboosted_pass.Jet


def Validation_semiboosted(fname,process,eventsToRead=None):
    events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema,metadata={"dataset":process},entry_stop=eventsToRead).events()

    fatjets = events.FatJet

    # Apply presection on Fatjets and require mass to be outside Higgs mass window for validation region
    good_fatjets = fatjets[precut(fatjets) & ((fatjets.msoftdrop<mass_cut[0]) | (fatjets.msoftdrop>mass_cut[1])) & (fatjets.msoftdrop>min_jet_mass)]


    # Require that there are exactly 2 fatjets present in the event
    events_semiboosted_fatjets = events[ak.num(good_fatjets, axis=1) == 2]

    # Select jets array from selected events with 2 fatjets
    jets = events_semiboosted_fatjets.Jet

    # Apply preselection on resolved jets
    good_jets = jets[(jets.pt > res_ptcut) & (np.absolute(jets.eta) < res_etacut) & (jets.btagDeepB>res_deepBcut)]

    # Require that there are atleast two jets present in the event
    events_semiboosted_jets = events_semiboosted_fatjets[ak.num(good_jets)>1]

    # Require jets to be away from fatjets, delta_r = 0.8
    good_pairs = events_semiboosted_jets.Jet.nearest(events_semiboosted_jets.FatJet).delta_r(events_semiboosted_jets.Jet)>delta_r_cut
    good_paired_jets = events_semiboosted_jets.Jet[good_pairs]

    events_semiboosted_pairs = events_semiboosted_jets[ak.num(good_paired_jets, axis=1) >= 2]

    # Calculate mass of jet pairs and select the pair which has closest mass to higgs - 125
    dijets = ak.combinations(events_semiboosted_pairs.Jet, 2, fields=['i0', 'i1'])
    dijet_masses = (dijets['i0'] + dijets['i1']).mass
    is_closest = closest(dijet_masses)
    closest_dijets = dijets[is_closest]
    mass_jets = closest_dijets[((closest_dijets['i0'] + closest_dijets['i1']).mass>=res_mass_cut[0]) & ((closest_dijets['i0'] + closest_dijets['i1']).mass<=res_mass_cut[1])]
    events_semiboosted = events_semiboosted_pairs[ak.num(mass_jets,axis=1)>0]

    # sort fat jets in descending pNet HbbvsQCD score
    sorted_fatjets = events_semiboosted.FatJet[ak.argsort(-HbbvsQCD(events_semiboosted.FatJet),axis=-1)]

    # fail region: 0 fat jets passing the pNet cut
    events_semiboosted_failed = events_semiboosted[HbbvsQCD(sorted_fatjets[:,0])<pNet_cut]
    events_semiboosted_fail = events_semiboosted_failed[ak.num(events_semiboosted_failed.FatJet,axis=1)==2]

    # pass region: at least 1 fat jets passing the pNet cut
    events_semiboosted_passed = events_semiboosted[HbbvsQCD(sorted_fatjets[:,0])>pNet_cut]
    events_semiboosted_pass = events_semiboosted_passed[ak.num(events_semiboosted_passed.FatJet,axis=1)==2]
    
    return events_semiboosted_fail.FatJet,events_semiboosted_pass.FatJet,events_semiboosted_fail.Jet,events_semiboosted_pass.Jet

