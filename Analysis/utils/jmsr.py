import correctionlib
import awkward as ak
import numpy as np
from config.config import * 


def getCalibratedJetMass(fatjets,variation,year):
    json = get_local_json("jmsr", year)

    cset = correctionlib.CorrectionSet.from_file(json[0])

    jms_corr = cset[json[1][0]]
    jmr_corr = cset[json[1][1]]

    fatjet_mass = FatJetMass(fatjets)

    # get the jet mass scale (JMS) correction
    if("jms" in variation):
        print("JMS correction: ", variation)
        scale = jms_corr.evaluate(variation[3:].lower())
    else:
        print("JMS correction: ", "nominal")
        scale = jms_corr.evaluate("nominal")

    # apply the JMS correction
    fatjet_mass = fatjet_mass * scale

    # get the jet mass resolution (JMR) correction
    if("jmr" in variation):
        print("JMR correction: ", variation)
        res = jmr_corr.evaluate(variation[3:].lower())
    else:
        print("JMR correction: ", "nominal")
        res = jmr_corr.evaluate("nominal")

    # deterministic smearing with gen match
    # (where relevant, the gen match should exist)
    matched = fatjets.genJetAK8Idx >= 0
    
    gen_mass = fatjets.matched_gen.mass
    
    # apply the JMR correction
    fatjet_mass = ak.where(
        matched,
        gen_mass + (fatjet_mass - gen_mass) * res,
        fatjet_mass
    )
    
    return fatjet_mass
