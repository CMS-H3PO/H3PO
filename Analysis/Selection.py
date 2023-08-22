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

    good_fatjets = fatjets[precut(fatjets)&(fatjets.msoftdrop>=mass_cut[0]) & (fatjets.msoftdrop<=mass_cut[1])]
    Signal_btag = good_fatjets[ak.num(good_fatjets, axis=1)> 2]

    Pnet = HbbvsQCD(Signal_btag)
    indices = ak.argsort(-Pnet,axis=-1)
    Signal_btag = Signal_btag[indices]

    #Pnet0 = Signal_btag[HbbvsQCD(Signal_btag[:,2])<pNet_cut]
    Pnet0 = Signal_btag
    boostedSignal_0btag = Signal_btag[ak.num(Pnet0, axis=1)> 2]

    Pnet1 = Signal_btag[HbbvsQCD(Signal_btag[:,0])>pNet_cut]
    boostedSignal_1btag = Signal_btag[ak.num(Pnet1, axis=1)> 2]

    return boostedSignal_0btag, boostedSignal_1btag


def Validation_boosted(fname,process,eventsToRead=None):
    events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema,metadata={"dataset":process},entry_stop=eventsToRead).events()

    fatjets = events.FatJet[ak.num(events.FatJet, axis=1)> 2]

    good_fatjets = fatjets[precut(fatjets) & ((fatjets[:,0].msoftdrop<mass_cut[0]) | (fatjets.msoftdrop[:,0]>mass_cut[1])) & (fatjets[:,0].msoftdrop>min_jet_mass) 
                           & (fatjets[:,1].msoftdrop>min_jet_mass) & ((fatjets[:,1].msoftdrop<mass_cut[0]) | (fatjets[:,1].msoftdrop>mass_cut[1])) 
                           & (fatjets[:,2].msoftdrop>=mass_cut[0]) & (fatjets[:,2].msoftdrop<=mass_cut[1])]

    ACR_btag = good_fatjets[ak.num(good_fatjets, axis=1)> 2]

    Pnet = HbbvsQCD(ACR_btag)
    indices = ak.argsort(-Pnet,axis=-1)
    ACR_btag = ACR_btag[indices]

    #Pnet0 = ACR_btag[HbbvsQCD(ACR_btag[:,2])<pNet_cut]
    Pnet0 = ACR_btag
    boostedCR_0btag = ACR_btag[ak.num(Pnet0, axis=1)> 2]

    Pnet1 = ACR_btag[HbbvsQCD(ACR_btag[:,0])>pNet_cut]
    boostedCR_1btag = ACR_btag[ak.num(Pnet1, axis=1)> 2]

    return boostedCR_0btag, boostedCR_1btag


def Signal_semiboosted(fname,process,eventsToRead=None):
    events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema,metadata={"dataset":process},entry_stop=eventsToRead).events()

    fatjets = events.FatJet

    good_fatjets = fatjets[precut(fatjets) & (fatjets.msoftdrop>=mass_cut[0]) & (fatjets.msoftdrop<=mass_cut[1])]
    pre_semiboosted_fatjets = good_fatjets[ak.num(good_fatjets, axis=1) == 2]
    pre_semiboosted_events = events[ak.num(good_fatjets, axis=1) == 2]

    res_jets = pre_semiboosted_events.Jet

    good_pre_jets = res_jets[(res_jets.pt > res_ptcut) & (np.absolute(res_jets.eta) < res_etacut) & (res_jets.btagDeepB>res_deepBcut)]

    good_semiboosted_jets = good_pre_jets[ak.num(good_pre_jets)>1]
    good_semiboosted_fatjets = pre_semiboosted_fatjets[ak.num(good_pre_jets)>1]
    good_semiboosted_events = pre_semiboosted_events[ak.num(good_pre_jets)>1]

    good_pairs = good_semiboosted_jets.nearest(good_semiboosted_fatjets).delta_r(good_semiboosted_jets)>delta_r_cut
    good_paired_jets = good_semiboosted_jets[good_pairs]

    min_paired_jets = good_paired_jets[ak.num(good_paired_jets, axis=1) >= 2]
    min_paired_fatjets = good_semiboosted_fatjets[ak.num(good_paired_jets, axis=1) >= 2]
    min_paired_events = good_semiboosted_events[ak.num(good_paired_jets, axis=1) >= 2]

    dijets = ak.combinations(min_paired_jets, 2, fields=['i0', 'i1'])
    dijet_masses = (dijets['i0'] + dijets['i1']).mass
    is_closest = closest(dijet_masses)
    closest_dijets = dijets[is_closest]
    mass_jets = closest_dijets[((closest_dijets['i0'] + closest_dijets['i1']).mass>=res_mass_cut[0]) & ((closest_dijets['i0'] + closest_dijets['i1']).mass<=res_mass_cut[1])]
    selected_jets = mass_jets[ak.num(mass_jets,axis=1)>0]
    selected_fatjets = min_paired_fatjets[ak.num(mass_jets,axis=1)>0]
    selected_events = min_paired_events[ak.num(mass_jets,axis=1)>0]

    Pnet = HbbvsQCD(selected_fatjets)
    indices = ak.argsort(-Pnet,axis=-1)
    selected_fatjets = selected_fatjets[indices]

    Pnet0 = selected_fatjets
    #Pnet0 = selected_fatjets[HbbvsQCD(selected_fatjets[:,1])<pNet_cut]
    semiboostedSignal_0btag_fatjets = selected_fatjets[ak.num(Pnet0, axis=1)== 2]
    semiboostedSignal_0btag_jets = selected_jets[ak.num(Pnet0, axis=1)== 2]

    Pnet1 = selected_fatjets[HbbvsQCD(selected_fatjets[:,0])>pNet_cut]
    semiboostedSignal_1btag_fatjets = selected_fatjets[ak.num(Pnet1, axis=1)== 2]
    semiboostedSignal_1btag_jets = selected_jets[ak.num(Pnet1, axis=1)== 2]

    return semiboostedSignal_0btag_fatjets,semiboostedSignal_1btag_fatjets,semiboostedSignal_0btag_jets,semiboostedSignal_1btag_jets


def Validation_semiboosted(fname,process,eventsToRead=None):
    events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema,metadata={"dataset":process},entry_stop=eventsToRead).events()

    fatjets = events.FatJet

    good_fatjets = fatjets[precut(fatjets)]
    pre_semiboosted_fatjets = good_fatjets[ak.num(good_fatjets, axis=1) == 2]
    pre_semiboosted_events = events[ak.num(good_fatjets, axis=1) == 2]

    res_jets = pre_semiboosted_events.Jet

    good_pre_jets = res_jets[(res_jets.pt > res_ptcut) & (np.absolute(res_jets.eta) < res_etacut) & (res_jets.btagDeepB>res_deepBcut)]

    good_semiboosted_jets = good_pre_jets[ak.num(good_pre_jets)>1]
    good_semiboosted_fatjets = pre_semiboosted_fatjets[ak.num(good_pre_jets)>1]
    good_semiboosted_events = pre_semiboosted_events[ak.num(good_pre_jets)>1]

    good_pairs = good_semiboosted_jets.nearest(good_semiboosted_fatjets).delta_r(good_semiboosted_jets)>delta_r_cut
    good_paired_jets = good_semiboosted_jets[good_pairs]

    min_paired_jets = good_paired_jets[ak.num(good_paired_jets, axis=1) >= 2]
    min_paired_fatjets = good_semiboosted_fatjets[ak.num(good_paired_jets, axis=1) >= 2]
    min_paired_events = good_semiboosted_events[ak.num(good_paired_jets, axis=1) >= 2]

    dijets = ak.combinations(min_paired_jets, 2, fields=['i0', 'i1'])
    dijet_masses = (dijets['i0'] + dijets['i1']).mass
    is_closest = closest(dijet_masses)
    closest_dijets = dijets[is_closest]

    resolved_pt = (closest_dijets['i0'] + closest_dijets['i1']).pt
    n=0
    resH = 0
    h=0
    for i in resolved_pt:
        if (resolved_pt[n] < min_paired_fatjets[n,1].pt):
            mass_fatjets = min_paired_fatjets[((min_paired_fatjets[:,0].msoftdrop < mass_cut[0]) | (min_paired_fatjets[:,0].msoftdrop>mass_cut[1])) & (min_paired_fatjets[:,0].msoftdrop>min_jet_mass) & (min_paired_fatjets[:,1].msoftdrop>min_jet_mass) & ((min_paired_fatjets[:,1].msoftdrop < mass_cut[0]) | (min_paired_fatjets[:,1].msoftdrop>mass_cut[1]))]
            mass_bfatjets = min_paired_fatjets[ak.num(mass_fatjets,axis=1)==2]
            mass_bjets = closest_dijets[ak.num(mass_fatjets,axis=1)==2]
            mass_events = min_paired_events[ak.num(mass_fatjets,axis=1)==2]
            mass_jets = mass_bjets[((mass_bjets['i0'] + mass_bjets['i1']).mass>=res_mass_cut[0]) & ((mass_bjets['i0'] + mass_bjets['i1']).mass<=res_mass_cut[1])]
            n=n+1
            h=h+1
        else:
            mass_fatjets = min_paired_fatjets[((min_paired_fatjets[:,0].msoftdrop < mass_cut[0] )| (min_paired_fatjets[:,0].msoftdrop>mass_cut[1])) & (min_paired_fatjets[:,0].msoftdrop>min_jet_mass) & ((min_paired_fatjets[:,1].msoftdrop>= mass_cut[0]) & (min_paired_fatjets[:,1].msoftdrop<=mass_cut[1]))]
            mass_bfatjets = min_paired_fatjets[ak.num(mass_fatjets,axis=1)==2]
            mass_bjets = closest_dijets[ak.num(mass_fatjets,axis=1)==2]
            mass_events = min_paired_events[ak.num(mass_fatjets,axis=1)==2]
            mass_jets = mass_bjets[(((mass_bjets['i0'] + mass_bjets['i1']).mass<res_mass_cut[0]) | ((mass_bjets['i0'] + mass_bjets['i1']).mass>res_mass_cut[1]))& ((mass_bjets['i0'] + mass_bjets['i1']).mass>min_jet_mass)]
            n=n+1
            resH=resH+1

    selected_jets = mass_bjets[ak.num(mass_jets,axis=1)>0]
    selected_fatjets = mass_bfatjets[ak.num(mass_jets,axis=1)>0]
    selected_events = mass_events[ak.num(mass_jets,axis=1)>0]

    print("resH = ",resH)
    print("h = ",h)

    Pnet = HbbvsQCD(selected_fatjets)
    indices = ak.argsort(-Pnet,axis=-1)
    selected_fatjets = selected_fatjets[indices]

    #Pnet0 = selected_fatjets[HbbvsQCD(selected_fatjets[:,1])<pNet_cut]
    Pnet0 = selected_fatjets
    semiboostedCR_0btag_fatjets = selected_fatjets[ak.num(Pnet0, axis=1)== 2]
    semiboostedCR_0btag_jets = selected_jets[ak.num(Pnet0, axis=1)== 2]

    Pnet1 = selected_fatjets[HbbvsQCD(selected_fatjets[:,0])>pNet_cut]
    semiboostedCR_1btag_fatjets = selected_fatjets[ak.num(Pnet1, axis=1)== 2]
    semiboostedCR_1btag_jets = selected_jets[ak.num(Pnet1, axis=1)== 2]

    return semiboostedCR_0btag_fatjets,semiboostedCR_1btag_fatjets,semiboostedCR_0btag_jets,semiboostedCR_1btag_jets


def boosted(fname,oFile,processLabel="signal",eventsToRead=None):	
    events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema,metadata={"dataset": "testSignal"},entry_stop=eventsToRead).events()

    fatjets = events.FatJet

    good_fatjets = fatjets[(fatjets.pt>ptcut) & (np.absolute(fatjets.eta)<etacut) & (fatjets.msoftdrop>=mass_cut[0]) & (fatjets.msoftdrop<=mass_cut[1])]
    pre_boosted_fatjets = good_fatjets[ak.num(good_fatjets, axis=1)> 2]
    pre_boosted_events = events[ak.num(good_fatjets, axis=1)> 2]
    #Btag cut applied at the end
    btag_boosted = pre_boosted_fatjets[HbbvsQCD(pre_boosted_fatjets)>=pNet_cut]
    btag_boosted_fatjets = btag_boosted[ak.num(btag_boosted, axis=1)> 2]
    btag_boosted_events = pre_boosted_events[ak.num(btag_boosted, axis=1)> 2]

    return btag_boosted_fatjets


def semiboosted(fname,oFile,processLabel="signal",eventsToRead=None):
    events = NanoEventsFactory.from_root(fname,schemaclass=NanoAODSchema,metadata={"dataset": "testSignal"},entry_stop=eventsToRead).events()

    fatjets = events.FatJet
    
    good_fatjets = fatjets[(fatjets.pt>ptcut) & (np.absolute(fatjets.eta)<etacut) & (fatjets.msoftdrop>=mass_cut[0]) & (fatjets.msoftdrop<=mass_cut[1])]
    pre_semiboosted_fatjets = good_fatjets[ak.num(good_fatjets, axis=1) == 2]
    pre_semiboosted_events = events[ak.num(good_fatjets, axis=1) == 2]
    #Btag cut for fatjets applied after pre selection
    btag_semiboosted = pre_semiboosted_fatjets[HbbvsQCD(pre_semiboosted_fatjets)>=pNet_cut]
    btag_semiboosted_fatjets = btag_semiboosted[ak.num(btag_semiboosted, axis=1) == 2]
    btag_semiboosted_events = pre_semiboosted_events[ak.num(btag_semiboosted, axis=1) == 2]

    #getting jets from selected fatjet events
    res_jets = btag_semiboosted_events.Jet

    good_pre_jets = res_jets[(res_jets.pt > res_ptcut) & (np.absolute(res_jets.eta) < res_etacut) & (res_jets.btagDeepB>res_deepBcut)]
    #Applying selection to all objects
    good_semiboosted_jets = good_pre_jets[ak.num(good_pre_jets)>1]
    good_semiboosted_fatjets = btag_semiboosted_fatjets[ak.num(good_pre_jets)>1]
    good_semiboosted_events = btag_semiboosted_events[ak.num(good_pre_jets)>1]
    
    #veto jets overlaping with fatjet
    good_pairs = good_semiboosted_jets.nearest(good_semiboosted_fatjets).delta_r(good_semiboosted_jets)>delta_r_cut
    good_paired_jets = good_semiboosted_jets[good_pairs]
    
    #make sure there are atleast 2 selected resolved jets in an event
    min_paired_jets = good_paired_jets[ak.num(good_paired_jets, axis=1) >= 2]
    min_paired_fatjets = good_semiboosted_fatjets[ak.num(good_paired_jets, axis=1) >= 2]
    min_paired_events = good_semiboosted_events[ak.num(good_paired_jets, axis=1) >= 2]

    #selecting jet pair whose mass is closest to Higgs mass
    dijets = ak.combinations(min_paired_jets, 2, fields=['i0', 'i1'])
    dijet_masses = (dijets['i0'] + dijets['i1']).mass
    is_closest = closest(dijet_masses)
    closest_dijets = dijets[is_closest]
    mass_jets = closest_dijets[((closest_dijets['i0'] + closest_dijets['i1']).mass>=res_mass_cut[0]) & ((closest_dijets['i0'] + closest_dijets['i1']).mass<=res_mass_cut[1])]
    selected_jets = mass_jets[ak.num(mass_jets,axis=1)>0]
    selected_fatjets = min_paired_fatjets[ak.num(mass_jets,axis=1)>0]
    selected_events = min_paired_events[ak.num(mass_jets,axis=1)>0]

    return selected_fatjets,selected_jets
