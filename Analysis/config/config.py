import os
from utils.utils import *


################# Central JSONs #####################
pog_correction_path = "/cvmfs/cms-griddata.cern.ch/cat/metadata/"

pog_jsons = {
    "pileup": {
        # year      JSON                                                              CorrectionSet
        "2016APV": ["LUM/Run2-2016preVFP-UL-NanoAODv9/2021-09-10/puWeights.json.gz",  "Collisions16_UltraLegacy_goldenJSON"],
        "2016":    ["LUM/Run2-2016postVFP-UL-NanoAODv9/2021-09-10/puWeights.json.gz", "Collisions16_UltraLegacy_goldenJSON"],
        "2017":    ["LUM/Run2-2017-UL-NanoAODv9/2021-09-10/puWeights.json.gz",        "Collisions17_UltraLegacy_goldenJSON"],
        "2018":    ["LUM/Run2-2018-UL-NanoAODv9/2021-09-10/puWeights.json.gz",        "Collisions18_UltraLegacy_goldenJSON"],
        "2024":    ["LUM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/latest/puWeights_CDEFGHI.json.gz",        "Collisions24_CDEFGHI_goldenJSON"]
    },
    "btag_deepJet": {
        # year      JSON                                                             CorrectionSets
        "2016APV": ["BTV/Run2-2016preVFP-UL-NanoAODv9/2025-08-19/btagging.json.gz",  ["deepJet_comb", "deepJet_incl", "deepJet_wp_values"]],
        "2016":    ["BTV/Run2-2016postVFP-UL-NanoAODv9/2025-08-19/btagging.json.gz", ["deepJet_comb", "deepJet_incl", "deepJet_wp_values"]],
        "2017":    ["BTV/Run2-2017-UL-NanoAODv9/2025-08-19/btagging.json.gz",        ["deepJet_comb", "deepJet_incl", "deepJet_wp_values"]],
        "2018":    ["BTV/Run2-2018-UL-NanoAODv9/2025-08-19/btagging.json.gz",        ["deepJet_comb", "deepJet_incl", "deepJet_wp_values"]],
        "2024":    ["BTV/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/latest/btagging.json.gz",        ["UParTAK4_comb", "UParTAK4_light", "UParTAK4_wp_values"]]
    },
    "xbbtag_particleNetMD_XbbvsQCD": {
        # year      JSON                                                                      CorrectionSets
        "2016APV": ["BTV/Run2-2016preVFP-UL-NanoAODv9/2025-08-19/ak8_xbbcc_tagging.json.gz",  ["particleNetMD_XbbvsQCD_comb", "particleNetMD_XbbvsQCD_wp_values"]],
        "2016":    ["BTV/Run2-2016postVFP-UL-NanoAODv9/2025-08-19/ak8_xbbcc_tagging.json.gz", ["particleNetMD_XbbvsQCD_comb", "particleNetMD_XbbvsQCD_wp_values"]],
        "2017":    ["BTV/Run2-2017-UL-NanoAODv9/2025-08-19/ak8_xbbcc_tagging.json.gz",        ["particleNetMD_XbbvsQCD_comb", "particleNetMD_XbbvsQCD_wp_values"]],
        "2018":    ["BTV/Run2-2018-UL-NanoAODv9/2025-08-19/ak8_xbbcc_tagging.json.gz",        ["particleNetMD_XbbvsQCD_comb", "particleNetMD_XbbvsQCD_wp_values"]],
    },
}

# Xbb tagger per year: ParticleNetMD for Run 2, GloParT for Run 3 (2024)
xbb_tagger = {"2016APV": "particleNetMD", "2016": "particleNetMD", "2017": "particleNetMD", "2018": "particleNetMD", "2024": "GloParT"}


def get_xbb_tagger(year):
    return xbb_tagger[year]


def get_pog_json(obj, year):
    json = get_json(pog_jsons, obj, year)

    return [os.path.join(pog_correction_path, json[0]), json[1]]


################# Local JSONs #####################
local_jsons = {
    "top_pt": {
        # year      JSON                  CorrectionSet
        "Default": ["../data/toppt.json",  "top_pt_weight"]
    },
    "jmsr": {
        # year      JSON                          CorrectionSets
        "2016APV": ["../data/jmsr/jmsr_AK8_2016.json",  ["jms","jmr"]],
        "2016":    ["../data/jmsr/jmsr_AK8_2016.json",  ["jms","jmr"]],
        "2017":    ["../data/jmsr/jmsr_AK8_2017.json",  ["jms","jmr"]],
        "2018":    ["../data/jmsr/jmsr_AK8_2018.json",  ["jms","jmr"]]
    },
    # GloParT 2024 SF: no official payload on CVMFS yet, so a local JSON built from the BTV Z(bb) table is used (WP 'L' = LP)
    "xbbtag_GloParT_XbbvsQCD": {
        # year   JSON                                                        CorrectionSets
        "2024": ["../data/xbbtag/xbbtag_GloParT_XbbvsQCD_SF_2024.json", ["GloParT_XbbvsQCD_comb", "GloParT_XbbvsQCD_wp_values"]]
    },
    "xbbtag_particleNetMD_XbbvsQCD_eff_XToYHTo6B": {
        # year             JSON                                                                          CorrectionSet
        "2016APV": {"SR": ["../data/xbbtag/xbbtag_particleNetMD_XbbvsQCD_eff_2016APV_SR_XToYHTo6B.json", "xbbtag_particleNetMD_XbbvsQCD_eff_2016APV_SR_XToYHTo6B"],
                    "VR": ["../data/xbbtag/xbbtag_particleNetMD_XbbvsQCD_eff_2016APV_VR_XToYHTo6B.json", "xbbtag_particleNetMD_XbbvsQCD_eff_2016APV_VR_XToYHTo6B"]},
        "2016":    {"SR": ["../data/xbbtag/xbbtag_particleNetMD_XbbvsQCD_eff_2016_SR_XToYHTo6B.json",    "xbbtag_particleNetMD_XbbvsQCD_eff_2016_SR_XToYHTo6B"],
                    "VR": ["../data/xbbtag/xbbtag_particleNetMD_XbbvsQCD_eff_2016_VR_XToYHTo6B.json",    "xbbtag_particleNetMD_XbbvsQCD_eff_2016_VR_XToYHTo6B"]},
        "2017":    {"SR": ["../data/xbbtag/xbbtag_particleNetMD_XbbvsQCD_eff_2017_SR_XToYHTo6B.json",    "xbbtag_particleNetMD_XbbvsQCD_eff_2017_SR_XToYHTo6B"],
                    "VR": ["../data/xbbtag/xbbtag_particleNetMD_XbbvsQCD_eff_2017_VR_XToYHTo6B.json",    "xbbtag_particleNetMD_XbbvsQCD_eff_2017_VR_XToYHTo6B"]},
        "2018":    {"SR": ["../data/xbbtag/xbbtag_particleNetMD_XbbvsQCD_eff_2018_SR_XToYHTo6B.json",    "xbbtag_particleNetMD_XbbvsQCD_eff_2018_SR_XToYHTo6B"],
                    "VR": ["../data/xbbtag/xbbtag_particleNetMD_XbbvsQCD_eff_2018_VR_XToYHTo6B.json",    "xbbtag_particleNetMD_XbbvsQCD_eff_2018_VR_XToYHTo6B"]}
    }
}


def get_local_json(obj, year="Default"):
    return get_json(local_jsons, obj, year)


################# Fat jet mass definition #####################
def FatJetMass(fatjets):
    return fatjets.particleNet_mass
