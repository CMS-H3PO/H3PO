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
