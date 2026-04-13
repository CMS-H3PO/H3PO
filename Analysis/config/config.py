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
        "2018":    ["LUM/Run2-2018-UL-NanoAODv9/2021-09-10/puWeights.json.gz",        "Collisions18_UltraLegacy_goldenJSON"]
    }
}


def get_pog_json(obj, year):
    json = get_json(pog_jsons, obj, year)

    return [os.path.join(pog_correction_path, json[0]), json[1]]


################# Local JSONs #####################
local_jsons = {
    "top_pt": {
        # year      JSON                  CorrectionSet
        "Default": ["config/toppt.json",  "top_pt_weight"]
    }
}


def get_local_json(obj, year="Default"):

    return get_json(local_jsons, obj, year)
