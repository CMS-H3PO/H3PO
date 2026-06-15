import correctionlib
import awkward as ak
import numpy as np
from config.config import *
from config.cutflow import *


class BTagSFAK4:
    """
    DeepJet AK4 WP scale factors using correctionlib.

    Uses:
        deepJet_comb : b- and c-jets
        deepJet_incl : light-flavor jets
    """

    def __init__(self, year):

        json = get_pog_json("btag_deepJet", year)

        cset = correctionlib.CorrectionSet.from_file(json[0])

        self.sf_bc    = cset[json[1][0]]
        self.sf_light = cset[json[1][1]]
        self.wps      = cset[json[1][2]]


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
        Returns per-jet SFs with the appropriate correction
        chosen according to hadron flavor.
        """

        counts = ak.num(jets, axis=1)

        # heavy- and light-flavor systematics treated as uncorrelated
        if "_" in systematic:
            if "bc" in systematic:
                systematic_bc    = systematic.split("_")[1]
                systematic_light = "central"
            else:
                systematic_bc    = "central"
                systematic_light = systematic.split("_")[1]
        else:
            systematic_bc    = systematic
            systematic_light = systematic

        flav = ak.flatten(jets.hadronFlavour)
        pt = ak.flatten(jets.pt)
        eta = ak.flatten(ak_clip(abs(jets.eta), 0, 2.499)) # jet abs(eta) can go only up to 2.5

        sf = np.ones(len(flav), dtype=np.float64)

        # --------------------------------------
        # b and c jets -> deepJet_comb
        # --------------------------------------

        bc_mask = (flav == 4) | (flav == 5)

        if np.any(bc_mask):

            sf[bc_mask] = self.sf_bc.evaluate(
                systematic_bc,
                wp,
                flav[bc_mask],
                eta[bc_mask],
                pt[bc_mask],
            )

        # --------------------------------------
        # light jets -> deepJet_incl
        # --------------------------------------

        light_mask = flav == 0

        if np.any(light_mask):

            sf[light_mask] = self.sf_light.evaluate(
                systematic_light,
                wp,
                flav[light_mask],
                eta[light_mask],
                pt[light_mask],
            )

        return ak.unflatten(sf, counts) 


def get_ak4_btag_weights(selection, btag_sf, dijets_SR, dijets_VR, systematic):
    # event masks
    SR_mask = selection.require(**good_dijet_SR_semiboosted)
    VR_mask = selection.require(**good_dijet_VR_semiboosted)

    # where possible, get the SFs for jets forming the SR dijets. Otherwise, set it to 1. Replace any remaining None's with 1.
    # Finally, get the first (and only) SF in each event
    SF1 = ak.fill_none(ak.where(SR_mask, btag_sf.evaluate_wp(dijets_SR[:,0:1]['i0'], systematic), [[1.]]), [1.], axis=0)[:,0]
    SF2 = ak.fill_none(ak.where(SR_mask, btag_sf.evaluate_wp(dijets_SR[:,0:1]['i1'], systematic), [[1.]]), [1.], axis=0)[:,0]

    w = SF1*SF2

    # where possible, get the SFs for jets forming the VR dijets. Otherwise, set it to 1. Replace any remaining None's with 1.
    # Finally, get the first (and only) SF in each event
    SF1 = ak.fill_none(ak.where(VR_mask, btag_sf.evaluate_wp(dijets_VR[:,0:1]['i0'], systematic), [[1.]]), [1.], axis=0)[:,0]
    SF2 = ak.fill_none(ak.where(VR_mask, btag_sf.evaluate_wp(dijets_VR[:,0:1]['i1'], systematic), [[1.]]), [1.], axis=0)[:,0]
    
    return w*(SF1*SF2)


def add_ak4_btag_weights(events, weights, selection, btag_sf, dijets_SR, dijets_VR):
    # nominal weights    
    nominal    = get_ak4_btag_weights(selection, btag_sf, dijets_SR, dijets_VR, systematic="central")
    # bc up    
    bc_up      = get_ak4_btag_weights(selection, btag_sf, dijets_SR, dijets_VR, systematic="bc_up")
    # bc down    
    bc_down    = get_ak4_btag_weights(selection, btag_sf, dijets_SR, dijets_VR, systematic="bc_down")
    # light up    
    light_up   = get_ak4_btag_weights(selection, btag_sf, dijets_SR, dijets_VR, systematic="light_up")
    # light down    
    light_down = get_ak4_btag_weights(selection, btag_sf, dijets_SR, dijets_VR, systematic="light_down")
    
    # add nominal weights
    weights.add("btag_deepJet", nominal)

    # add systematic variations (poor man's replacement for add_multivariation() available in more recent versions of Coffea)
    weights.add(
        name="btag_fixedWP_bc_simple",
        weight=np.ones_like(nominal),
        weightUp=(bc_up / nominal),
        weightDown=(bc_down / nominal)
    )

    weights.add(
        name="btag_fixedWP_light_simple",
        weight=np.ones_like(nominal),
        weightUp=(light_up / nominal),
        weightDown=(light_down / nominal)
    )
