import correctionlib
import awkward as ak
import numpy as np
from config.config import *


def add_top_pT_reweighting(events, weights):
    """
    Apply this SF only to TTbar datasets! The lastest recommendation implemented in the JSON file loaded below.
    Documentation:
    - https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting
    - https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting#TOP_PAG_corrections_based_on_the
    """
    json = get_local_json("top_pt")
    cset = correctionlib.CorrectionSet.from_file(json[0])
    corr = cset[json[1]]
    
    # get top quarks (the last copy)
    tops = events.GenPart[
        (abs(events.GenPart.pdgId) == 6)
        & events.GenPart.hasFlags(["isLastCopy"])
    ]
    # split into top/anti-top
    top     = tops[tops.pdgId == 6]
    antitop = tops[tops.pdgId == -6]
    # safely get pt values
    top_pt     = ak.fill_none(ak.pad_none(top.pt,     1), 0.)[:, 0]
    antitop_pt = ak.fill_none(ak.pad_none(antitop.pt, 1), 0.)[:, 0]

    var_names = {
        "weight":     "nominal",
        #"weightUp":   "up",  # flat +10%
        #"weightDown": "down" # flat -10%
    }
    w_dict = {}
    
    # collect weights for all enabled variations
    for var in var_names.keys():
        w_top     = corr.evaluate(top_pt,     var_names[var])
        w_antitop = corr.evaluate(antitop_pt, var_names[var])

        w_dict[var] = np.sqrt(w_top * w_antitop)

    # add weights        
    weights.add("top_pt", **w_dict)
