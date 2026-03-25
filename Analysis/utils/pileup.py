import correctionlib
import awkward as ak
import numpy as np
from config.config import *
from utils.utils import *


def add_pileup_weight(events, weights, year):
    nPU = ak.to_numpy(events.Pileup.nTrueInt)

    cset = correctionlib.CorrectionSet.from_file(get_pog_json("pileup", year))

    pu_corr = cset[pog_jsons["pileup"][year][1]]

    # evaluate and clip up to 4 to avoid large weights
    w_nom = ak_clip(pu_corr.evaluate(nPU, "nominal"), 0, 4)
    w_up  = ak_clip(pu_corr.evaluate(nPU, "up"), 0, 4)
    w_dn  = ak_clip(pu_corr.evaluate(nPU, "down"), 0, 4)

    weights.add(
        name="pileup",
        weight=w_nom,
        weightUp=w_up,
        weightDown=w_dn
    )
