import os


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
    try:
        pog_json = pog_jsons[obj]
    except:
        print(f"No JSON for {obj}")

    return [os.path.join(pog_correction_path, pog_json[year][0]), pog_json[year][1]]
