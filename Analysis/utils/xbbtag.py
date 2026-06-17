import correctionlib
import awkward as ak
import numpy as np
from config.config import *
from config.cutflow import *


class XbbTagSFAK8:
    """
    ParticleNetMD_XbbvsQCD AK8 WP scale factors using correctionlib.
    """

    def __init__(self, year):

        json = get_pog_json("xbbtag_particleNetMD_XbbvsQCD", year)

        cset = correctionlib.CorrectionSet.from_file(json[0])

        self.sf  = cset[json[1][0]]
        self.wps = cset[json[1][1]]


    def wp_value(
        self,
        wp="L"
    ):
        return self.wps.evaluate(wp)


    def evaluate_wp(
        self,
        jets,
        systematic="central",
        wp="L",
    ):
        """
        Returns per-jet SFs
        """

        counts = ak.num(jets, axis=1)

        pt = ak.flatten(jets.pt)

        sf = self.sf.evaluate(
            systematic,
            wp,
            pt,
        )

        return ak.unflatten(sf, counts) 


def get_ak8_xbbtag_weights_boosted(pass_mask, fail_mask, sf):
    """
    Using Method 1a) from https://btv-wiki.docs.cern.ch/PerformanceCalibration/fixedWPSFRecommendations/
    applied to the boosted channel
    """
    # tagging efficiencies for the leading 3 fat jets (eventually to come from efficiency maps, currently hardcoded to some placeholder values)
    eff1 = 0.8
    eff2 = 0.8
    eff3 = 0.8
    
    # SFs for the leading 3 fat jets
    SF1 = sf[:,0]
    SF2 = sf[:,1]
    SF3 = sf[:,2]
    
    # MC probability for the fail category
    prob_fail_MC = (1 - eff1) * (1 - eff2) * (1 - eff3)
    # DATA probability for the fail category (per-jet probabilitites restricted between 0. and 1.)
    prob_fail_DATA = ak_clip((1 - SF1*eff1), 0., 1.) * ak_clip((1 - SF2*eff2), 0., 1.) * ak_clip((1 - SF3*eff3), 0., 1.)

    # weights for the fail category
    w_fail = ak.where(fail_mask, prob_fail_DATA / prob_fail_MC, 1.)

    # weights for the pass category
    w_pass = ak.where(pass_mask, (1 - prob_fail_DATA) / (1 - prob_fail_MC), 1.)

    return w_pass * w_fail


def get_ak8_xbbtag_weights_semiboosted(pass_mask, fail_mask, sf):
    """
    Using Method 1a) from https://btv-wiki.docs.cern.ch/PerformanceCalibration/fixedWPSFRecommendations/
    applied to the semiboosted channel
    """
    # tagging efficiencies for the leading 3 fat jets (eventually to come from efficiency maps, currently hardcoded to some placeholder values)
    eff1 = 0.8
    eff2 = 0.8

    # SFs for the leading 3 fat jets
    SF1 = sf[:,0]
    SF2 = sf[:,1]

    # MC probability for the fail category
    prob_fail_MC = (1 - eff1) * (1 - eff2)
    # DATA probability for the fail category (per-jet probabilitites restricted between 0. and 1.)
    prob_fail_DATA = ak_clip((1 - SF1*eff1), 0., 1.) * ak_clip((1 - SF2*eff2), 0., 1.)

    # weights for the fail category
    w_fail = ak.where(fail_mask, prob_fail_DATA / prob_fail_MC, 1.)

    # weights for the pass category
    w_pass = ak.where(pass_mask, (1 - prob_fail_DATA) / (1 - prob_fail_MC), 1.)

    return w_pass * w_fail


def get_ak8_xbbtag_weights(selection, xbbtag_sf, fatjets_SR, fatjets, systematic):

    # SFs for fat jets
    sf_SR = ak.fill_none(ak.pad_none(xbbtag_sf.evaluate_wp(fatjets_SR, systematic), 3), 1.)
    sf_VR = ak.fill_none(ak.pad_none(xbbtag_sf.evaluate_wp(fatjets, systematic), 3), 1.)

    # boosted channel event masks
    SR_b_pass_mask = selection.require(**cuts_Pass["SR_boosted"])
    SR_b_fail_mask = selection.require(**cuts_Fail["SR_boosted"])
    VR_b_pass_mask = selection.require(**cuts_Pass["VR_boosted"])
    VR_b_fail_mask = selection.require(**cuts_Fail["VR_boosted"])

    # get weights for the SR boosted
    w_SR_b = get_ak8_xbbtag_weights_boosted(SR_b_pass_mask, SR_b_fail_mask, sf_SR)
    
    # get weights for the VR boosted
    w_VR_b = get_ak8_xbbtag_weights_boosted(VR_b_pass_mask, VR_b_fail_mask, sf_VR)

    # semiboosted channel event masks
    SR_sb_pass_mask = selection.require(**cuts_Pass["SR_semiboosted"])
    SR_sb_fail_mask = selection.require(**cuts_Fail["SR_semiboosted"])
    VR_sb_pass_mask = selection.require(**cuts_Pass["VR_semiboosted"])
    VR_sb_fail_mask = selection.require(**cuts_Fail["VR_semiboosted"])

    # get weights for the SR semiboosted
    w_SR_sb = get_ak8_xbbtag_weights_semiboosted(SR_sb_pass_mask, SR_sb_fail_mask, sf_SR)

    # get weights for the VR semiboosted
    w_VR_sb = get_ak8_xbbtag_weights_semiboosted(VR_sb_pass_mask, VR_sb_fail_mask, sf_VR)

    # ok to multiply since all categories mutually orthogonal
    return w_SR_b * w_VR_b * w_SR_sb * w_VR_sb


def add_ak8_xbbtag_weights(weights, selection, xbbtag_sf, fatjets_SR, fatjets):
    # nominal weights    
    nominal = get_ak8_xbbtag_weights(selection, xbbtag_sf, fatjets_SR, fatjets, systematic="central")
    # up variation
    up      = get_ak8_xbbtag_weights(selection, xbbtag_sf, fatjets_SR, fatjets, systematic="up")
    # down variation 
    down    = get_ak8_xbbtag_weights(selection, xbbtag_sf, fatjets_SR, fatjets, systematic="down")

    # add Xbb-tag weights including systematic variations
    weights.add(
        name="Xbbtag_comb_total",
        weight=nominal,
        weightUp=up,
        weightDown=down
    )
