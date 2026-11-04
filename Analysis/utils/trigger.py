import correctionlib
import awkward as ak
from config.config import *
from config.cutflow import *


class TriggerSF:
    """
    Trigger efficiency scale factors using correctionlib.
    """

    def __init__(self, year):

        json = get_local_json("trigger", year)

        cset = correctionlib.CorrectionSet.from_file(json[0])

        self.boosted     = cset[json[1][0]]
        self.semiboosted = cset[json[1][1]]


def get_trigger_weights(selection, events, sf, systematic):
    # boosted channel event masks
    SR_b_mask = selection.require(**mass_cut_SR_boosted)
    VR_b_mask = selection.require(**mass_cut_VR_boosted)

    # get weights for the boosted channel
    w_b = ak.where((SR_b_mask | VR_b_mask), sf.boosted.evaluate(events["Mjjj"], systematic), 1.)

    # semiboosted channel event masks
    SR_sb_mask = selection.require(**mass_cut_fatjets_SR_semiboosted)
    VR_sb_mask = selection.require(**mass_cut_fatjets_VR_semiboosted)

    # get weights for the semiboosted channel
    w_sb = ak.where((SR_sb_mask | VR_sb_mask), sf.semiboosted.evaluate(events["Mjjj"], systematic), 1.)

    # ok to multiply since channels mutually orthogonal
    return w_b * w_sb


def add_trigger_weights(weights, selection, events, sf):
    # nominal weights    
    nominal = get_trigger_weights(selection, events, sf, systematic="nominal")
    # up variation
    up      = get_trigger_weights(selection, events, sf, systematic="up")
    # down variation 
    down    = get_trigger_weights(selection, events, sf, systematic="down")

    # add Xbb-tag weights including systematic variations
    weights.add(
        name="trigger",
        weight=nominal,
        weightUp=up,
        weightDown=down
    )
