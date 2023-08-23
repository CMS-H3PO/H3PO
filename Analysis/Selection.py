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
    min_delta = ak.min(delta, axis=1)
    is_closest = (delta == min_delta)
    return is_closest


def HbbvsQCD(fatjet):
    score = (fatjet.particleNetMD_Xbb/(fatjet.particleNetMD_Xbb+fatjet.particleNetMD_QCD))
    return score


def precut(fatjets):
    return (fatjets.pt>ptcut) & (np.absolute(fatjets.eta)<etacut)


def FailPassCategories(good_fatjets):
    # sort the 3 leading (in pT) fat jets in descending pNet HbbvsQCD score
    # (this is to prevent events being selected due to the 4th or higher leading jet having a high pNet score)
    sorted_fatjets_3 = good_fatjets[:,0:3]
    sorted_fatjets_3 = sorted_fatjets_3[ak.argsort(-HbbvsQCD(sorted_fatjets_3),axis=-1)]

    # fail region: 0 out of the 3 leading fat jets passing the pNet cut
    # pass region: at least 1 out of the 3 leading fat jets passing the pNet cut
    return good_fatjets[HbbvsQCD(sorted_fatjets_3[:,0])<pNet_cut], good_fatjets[HbbvsQCD(sorted_fatjets_3[:,0])>pNet_cut]


def FailPassCategoriesSemiboosted(good_fatjets, good_jets):
    # sort the good fat jets in descending pNet HbbvsQCD score
    sorted_fatjets = good_fatjets[ak.argsort(-HbbvsQCD(good_fatjets),axis=-1)]

    # fail region: 0 fat jets passing the pNet cut
    # pass region: at least 1 fat jets passing the pNet cut
    fail_mask = (HbbvsQCD(sorted_fatjets[:,0])<pNet_cut)
    pass_mask = (HbbvsQCD(sorted_fatjets[:,0])>pNet_cut)
    return good_fatjets[fail_mask], good_fatjets[pass_mask], good_jets[fail_mask], good_jets[pass_mask]


def SR_mask(fatjets):
    return (fatjets.msoftdrop>=mass_cut[0]) & (fatjets.msoftdrop<=mass_cut[1])


def VR_boosted_mask(fatjets):
    return (((fatjets[:,0].msoftdrop<mass_cut[0]) | (fatjets.msoftdrop[:,0]>mass_cut[1])) & (fatjets[:,0].msoftdrop>min_jet_mass) 
    & (fatjets[:,1].msoftdrop>min_jet_mass) & ((fatjets[:,1].msoftdrop<mass_cut[0]) | (fatjets[:,1].msoftdrop>mass_cut[1])) 
    & (fatjets[:,2].msoftdrop>=mass_cut[0]) & (fatjets[:,2].msoftdrop<=mass_cut[1]))


def VR_semiboosted_mask(fatjets):
    return ((fatjets.msoftdrop<mass_cut[0]) | (fatjets.msoftdrop>mass_cut[1])) & (fatjets.msoftdrop>min_jet_mass)


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
    good_fatjets_3 = good_fatjets_3[VR_boosted_mask(good_fatjets_3)]

    # select events with at least 3 good fat jets
    good_fatjets_VR_boosted = good_fatjets[ak.num(good_fatjets_3, axis=1)>2]
    
    return FailPassCategories(good_fatjets_VR_boosted)


def Region_semiboosted(mask,N_req,N_sel,fname,process,eventsToRead=None):
    events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema,metadata={"dataset":process},entry_stop=eventsToRead).events()

    fatjets = events.FatJet

    # fat jets preselection
    good_fatjets = fatjets[precut(fatjets)]
    
    # select events with at least 3 preselected fat jets
    events_preselection =       events[ak.num(good_fatjets, axis=1)>2]
    good_fatjets        = good_fatjets[ak.num(good_fatjets, axis=1)>2]

    # apply the jet mass cut to the 3 leading (in pT) fat jets
    good_fatjets = good_fatjets[:,0:3]
    good_fatjets = good_fatjets[mask(good_fatjets)]

    # select events with exactly N_req good fat jets and select N_sel leading good fat jets
    events_semiboosted_fatjets = events_preselection[ak.num(good_fatjets, axis=1)==N_req]
    good_fatjets               =       (good_fatjets[ak.num(good_fatjets, axis=1)==N_req])[:,0:N_sel]

    # select jets from selected events with exactly N_req good fat jets
    jets = events_semiboosted_fatjets.Jet

    # apply preselection on the resolved jets
    good_jets = jets[(jets.pt > res_ptcut) & (np.absolute(jets.eta) < res_etacut) & (jets.btagDeepB>res_deepBcut)]

    # require that there are at least 2 good jets present in the event
    good_fatjets = good_fatjets[ak.num(good_jets, axis=1)>1]
    good_jets    =    good_jets[ak.num(good_jets, axis=1)>1]

    # require jets to be away from fat jets
    away_jets_mask = good_jets.nearest(good_fatjets).delta_r(good_jets)>delta_r_cut
    good_jets = good_jets[away_jets_mask]

    # require that there are at least 2 good away jets present in the event
    good_fatjets = good_fatjets[ak.num(good_jets, axis=1)>1]
    good_jets    =    good_jets[ak.num(good_jets, axis=1)>1]

    # calculate mass of all possible jet pairs and select the pair which has the mass closest to the Higgs boson mass
    dijets = ak.combinations(good_jets, 2, fields=['i0', 'i1'])
    dijet_masses = (dijets['i0'] + dijets['i1']).mass
    is_closest = closest(dijet_masses)
    closest_dijets = dijets[is_closest]
    # apply the jet mass cut to the closest dijets
    good_dijets = closest_dijets[((closest_dijets['i0'] + closest_dijets['i1']).mass>=res_mass_cut[0]) & ((closest_dijets['i0'] + closest_dijets['i1']).mass<=res_mass_cut[1])]
    
    # select events with at least 1 good dijet (by construction there can be at most 1 per event)
    good_fatjets = good_fatjets[ak.num(good_dijets, axis=1)>0]
    good_jets    =    good_jets[ak.num(good_dijets, axis=1)>0]

    return FailPassCategoriesSemiboosted(good_fatjets, good_jets)


def Signal_semiboosted(fname,process,eventsToRead=None):
    return Region_semiboosted(SR_mask,2,2,fname,process,eventsToRead=None)


def Validation_semiboosted(fname,process,eventsToRead=None):
    return Region_semiboosted(VR_semiboosted_mask,3,2,fname,process,eventsToRead=None)
