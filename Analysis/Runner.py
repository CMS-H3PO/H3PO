import os
import copy
import uproot
import awkward as ak
import hist
from hist import Hist
from Selection import *
from utils.utils import *
from config.cutflow import *


# histogram bins
j3_bins=120
j3_start=0
j3_stop=6000
j2_bins=120
j2_start=0
j2_stop=6000
ht_bins=120
ht_start=0
ht_stop=6000
eta_bins=100
eta_start=-5
eta_stop=5


def fillHistos(channel, suffix, trigSuffix, events, selection, weights, event_yield, extraHistos, refTrigList=None, trigList=None):

    isBoosted = ("semiboosted" not in channel.lower())

    _cuts_Pass = cuts_Pass
    _cuts_Fail = cuts_Fail

    if refTrigList != None:
        selection.add("RefTrigger", getTriggerDecision(events, refTrigList))
        _cuts_Pass = cuts_Pass_refTrig
        _cuts_Fail = cuts_Fail_refTrig
        if trigList != None:
            selection.add("AnTrigger", getTriggerDecision(events, trigList))
            _cuts_Pass = cuts_Pass_refAndAnTrig
            _cuts_Fail = cuts_Fail_refAndAnTrig

    # define Pass and Fail category event masks
    if isBoosted:
        SR_pass_evtMask = selection.require(**_cuts_Pass["SR_boosted"])
        SR_fail_evtMask = selection.require(**_cuts_Fail["SR_boosted"])
        VR_pass_evtMask = selection.require(**_cuts_Pass["VR_boosted"])
        VR_fail_evtMask = selection.require(**_cuts_Fail["VR_boosted"])

        event_yield[f"SR_boosted{suffix}"][f"Fail{trigSuffix}"] = ak.sum(weights.weight()[SR_fail_evtMask])
        event_yield[f"SR_boosted{suffix}"][f"Pass{trigSuffix}"] = ak.sum(weights.weight()[SR_pass_evtMask])
        event_yield[f"VR_boosted{suffix}"][f"Fail{trigSuffix}"] = ak.sum(weights.weight()[VR_fail_evtMask])
        event_yield[f"VR_boosted{suffix}"][f"Pass{trigSuffix}"] = ak.sum(weights.weight()[VR_pass_evtMask])
    else:
        SR_pass_evtMask = selection.require(**_cuts_Pass["SR_semiboosted"])
        SR_fail_evtMask = selection.require(**_cuts_Fail["SR_semiboosted"])
        VR_pass_evtMask = selection.require(**_cuts_Pass["VR_semiboosted"])
        VR_fail_evtMask = selection.require(**_cuts_Fail["VR_semiboosted"])

        event_yield[f"SR_semiboosted{suffix}"][f"Fail{trigSuffix}"] = ak.sum(weights.weight()[SR_fail_evtMask])
        event_yield[f"SR_semiboosted{suffix}"][f"Pass{trigSuffix}"] = ak.sum(weights.weight()[SR_pass_evtMask])
        event_yield[f"VR_semiboosted{suffix}"][f"Fail{trigSuffix}"] = ak.sum(weights.weight()[VR_fail_evtMask])
        event_yield[f"VR_semiboosted{suffix}"][f"Pass{trigSuffix}"] = ak.sum(weights.weight()[VR_pass_evtMask])

    # select events
    SR_pass_e = events[SR_pass_evtMask]
    SR_fail_e = events[SR_fail_evtMask]
    VR_pass_e = events[VR_pass_evtMask]
    VR_fail_e = events[VR_fail_evtMask]
    # get fat jets
    SR_pass_fj = SR_pass_e.fatjets_SR
    SR_fail_fj = SR_fail_e.fatjets_SR
    VR_pass_fj = VR_pass_e.fatjets_VR
    VR_fail_fj = VR_fail_e.fatjets_VR
    # get dijets for the semiboosted channel
    if not isBoosted:
        SR_pass_j = SR_pass_e.good_dijets_SR
        SR_fail_j = SR_fail_e.good_dijets_SR
        VR_pass_j = VR_pass_e.good_dijets_VR
        VR_fail_j = VR_fail_e.good_dijets_VR

    # histograms dictionary
    hists = {}

    if isBoosted:
        trijet_mass_SR_fail = (SR_fail_fj[:,0]+SR_fail_fj[:,1]+SR_fail_fj[:,2]).mass
        trijet_mass_SR_pass = (SR_pass_fj[:,0]+SR_pass_fj[:,1]+SR_pass_fj[:,2]).mass

        trijet_mass_VR_fail = (VR_fail_fj[:,0]+VR_fail_fj[:,1]+VR_fail_fj[:,2]).mass
        trijet_mass_VR_pass = (VR_pass_fj[:,0]+VR_pass_fj[:,1]+VR_pass_fj[:,2]).mass

        if extraHistos:
            ht_SR_fail = SR_fail_fj[:,0].pt+SR_fail_fj[:,1].pt+SR_fail_fj[:,2].pt
            ht_SR_pass = SR_pass_fj[:,0].pt+SR_pass_fj[:,1].pt+SR_pass_fj[:,2].pt

            ht_VR_fail = VR_fail_fj[:,0].pt+VR_fail_fj[:,1].pt+VR_fail_fj[:,2].pt
            ht_VR_pass = VR_pass_fj[:,0].pt+VR_pass_fj[:,1].pt+VR_pass_fj[:,2].pt

            eta1_SR_fail = SR_fail_fj[:,0].eta
            eta2_SR_fail = SR_fail_fj[:,1].eta
            eta3_SR_fail = SR_fail_fj[:,2].eta
            eta1_SR_pass = SR_pass_fj[:,0].eta
            eta2_SR_pass = SR_pass_fj[:,1].eta
            eta3_SR_pass = SR_pass_fj[:,2].eta

            eta1_VR_fail = VR_fail_fj[:,0].eta
            eta2_VR_fail = VR_fail_fj[:,1].eta
            eta3_VR_fail = VR_fail_fj[:,2].eta
            eta1_VR_pass = VR_pass_fj[:,0].eta
            eta2_VR_pass = VR_pass_fj[:,1].eta
            eta3_VR_pass = VR_pass_fj[:,2].eta
    else:
        trijet_mass_SR_fail = (SR_fail_fj[:,0]+SR_fail_fj[:,1]+SR_fail_j[:,0]['i0']+SR_fail_j[:,0]['i1']).mass
        trijet_mass_SR_pass = (SR_pass_fj[:,0]+SR_pass_fj[:,1]+SR_pass_j[:,0]['i0']+SR_pass_j[:,0]['i1']).mass

        trijet_mass_VR_fail = (VR_fail_fj[:,0]+VR_fail_fj[:,1]+VR_fail_j[:,0]['i0']+VR_fail_j[:,0]['i1']).mass
        trijet_mass_VR_pass = (VR_pass_fj[:,0]+VR_pass_fj[:,1]+VR_pass_j[:,0]['i0']+VR_pass_j[:,0]['i1']).mass

        if extraHistos:
            ht_SR_fail = SR_fail_fj[:,0].pt+SR_fail_fj[:,1].pt+(SR_fail_j[:,0]['i0']+SR_fail_j[:,0]['i1']).pt
            ht_SR_pass = SR_pass_fj[:,0].pt+SR_pass_fj[:,1].pt+(SR_pass_j[:,0]['i0']+SR_pass_j[:,0]['i1']).pt

            ht_VR_fail = VR_fail_fj[:,0].pt+VR_fail_fj[:,1].pt+(VR_fail_j[:,0]['i0']+VR_fail_j[:,0]['i1']).pt
            ht_VR_pass = VR_pass_fj[:,0].pt+VR_pass_fj[:,1].pt+(VR_pass_j[:,0]['i0']+VR_pass_j[:,0]['i1']).pt

            eta1_SR_fail = SR_fail_fj[:,0].eta
            eta2_SR_fail = SR_fail_fj[:,1].eta
            eta3_SR_fail = (SR_fail_j[:,0]['i0']+SR_fail_j[:,0]['i1']).eta
            eta1_SR_pass = SR_pass_fj[:,0].eta
            eta2_SR_pass = SR_pass_fj[:,1].eta
            eta3_SR_pass = (SR_pass_j[:,0]['i0']+SR_pass_j[:,0]['i1']).eta

            eta1_VR_fail = VR_fail_fj[:,0].eta
            eta2_VR_fail = VR_fail_fj[:,1].eta
            eta3_VR_fail = (VR_fail_j[:,0]['i0']+VR_fail_j[:,0]['i1']).eta
            eta1_VR_pass = VR_pass_fj[:,0].eta
            eta2_VR_pass = VR_pass_fj[:,1].eta
            eta3_VR_pass = (VR_pass_j[:,0]['i0']+VR_pass_j[:,0]['i1']).eta

    j3_SR_fail_bin = hist.axis.Regular(label=f"{channel} Signal Fail Trijet Mass [GeV]", name="trijet_mass_SR_fail", bins=j3_bins, start=j3_start, stop=j3_stop)
    hists["j3_SR_fail"] = Hist(j3_SR_fail_bin, storage="weight")
    hists["j3_SR_fail"].fill(trijet_mass_SR_fail=trijet_mass_SR_fail, weight=weights.weight()[SR_fail_evtMask])

    j3_SR_pass_bin = hist.axis.Regular(label=f"{channel} Signal Pass Trijet Mass [GeV]", name="trijet_mass_SR_pass", bins=j3_bins, start=j3_start, stop=j3_stop)
    hists["j3_SR_pass"] = Hist(j3_SR_pass_bin, storage="weight")
    hists["j3_SR_pass"].fill(trijet_mass_SR_pass=trijet_mass_SR_pass, weight=weights.weight()[SR_pass_evtMask])

    j3_VR_fail_bin = hist.axis.Regular(label=f"{channel} Validation Fail Trijet Mass [GeV]", name="trijet_mass_VR_fail", bins=j3_bins, start=j3_start, stop=j3_stop)
    hists["j3_VR_fail"] = Hist(j3_VR_fail_bin, storage="weight")
    hists["j3_VR_fail"].fill(trijet_mass_VR_fail=trijet_mass_VR_fail, weight=weights.weight()[VR_fail_evtMask])

    j3_VR_pass_bin = hist.axis.Regular(label=f"{channel} Validation Pass Trijet Mass [GeV]", name="trijet_mass_VR_pass", bins=j3_bins, start=j3_start, stop=j3_stop)
    hists["j3_VR_pass"] = Hist(j3_VR_pass_bin, storage="weight")
    hists["j3_VR_pass"].fill(trijet_mass_VR_pass=trijet_mass_VR_pass, weight=weights.weight()[VR_pass_evtMask])

    if extraHistos:
        ht_SR_fail_bin = hist.axis.Regular(label=f"{channel} Signal Fail H_{{T}} [GeV]", name="ht_SR_fail", bins=ht_bins, start=ht_start, stop=ht_stop)
        hists["ht_vs_mjjj_SR_fail"] = Hist(j3_SR_fail_bin, ht_SR_fail_bin, storage="weight")
        hists["ht_vs_mjjj_SR_fail"].fill(ht_SR_fail=ht_SR_fail, trijet_mass_SR_fail=trijet_mass_SR_fail, weight=weights.weight()[SR_fail_evtMask])

        eta_SR_fail_bin = hist.axis.Regular(label=f"{channel} Signal Fail Fat Jet #eta", name="eta_SR_fail", bins=eta_bins, start=eta_start, stop=eta_stop)
        hists["eta_SR_fail"] = Hist(eta_SR_fail_bin, storage="weight")
        hists["eta_SR_fail"].fill(eta_SR_fail=eta1_SR_fail, weight=weights.weight()[SR_fail_evtMask])
        hists["eta_SR_fail"].fill(eta_SR_fail=eta2_SR_fail, weight=weights.weight()[SR_fail_evtMask])
        hists["eta_SR_fail"].fill(eta_SR_fail=eta3_SR_fail, weight=weights.weight()[SR_fail_evtMask])
        #-----
        ht_SR_pass_bin = hist.axis.Regular(label=f"{channel} Signal Pass H_{{T}} [GeV]", name="ht_SR_pass", bins=ht_bins, start=ht_start, stop=ht_stop)
        hists["ht_vs_mjjj_SR_pass"] = Hist(j3_SR_pass_bin, ht_SR_pass_bin, storage="weight")
        hists["ht_vs_mjjj_SR_pass"].fill(ht_SR_pass=ht_SR_pass, trijet_mass_SR_pass=trijet_mass_SR_pass, weight=weights.weight()[SR_pass_evtMask])

        eta_SR_pass_bin = hist.axis.Regular(label=f"{channel} Signal Pass Fat Jet #eta", name="eta_SR_pass", bins=eta_bins, start=eta_start, stop=eta_stop)
        hists["eta_SR_pass"] = Hist(eta_SR_pass_bin, storage="weight")
        hists["eta_SR_pass"].fill(eta_SR_pass=eta1_SR_pass, weight=weights.weight()[SR_pass_evtMask])
        hists["eta_SR_pass"].fill(eta_SR_pass=eta2_SR_pass, weight=weights.weight()[SR_pass_evtMask])
        hists["eta_SR_pass"].fill(eta_SR_pass=eta3_SR_pass, weight=weights.weight()[SR_pass_evtMask])
        #-----
        ht_VR_fail_bin = hist.axis.Regular(label=f"{channel} Validation Fail H_{{T}} [GeV]", name="ht_VR_fail", bins=ht_bins, start=ht_start, stop=ht_stop)
        hists["ht_vs_mjjj_VR_fail"] = Hist(j3_VR_fail_bin, ht_VR_fail_bin, storage="weight")
        hists["ht_vs_mjjj_VR_fail"].fill(ht_VR_fail=ht_VR_fail, trijet_mass_VR_fail=trijet_mass_VR_fail, weight=weights.weight()[VR_fail_evtMask])

        eta_VR_fail_bin = hist.axis.Regular(label=f"{channel} Validation Fail Fat Jet #eta", name="eta_VR_fail", bins=eta_bins, start=eta_start, stop=eta_stop)
        hists["eta_VR_fail"] = Hist(eta_VR_fail_bin, storage="weight")
        hists["eta_VR_fail"].fill(eta_VR_fail=eta1_VR_fail, weight=weights.weight()[VR_fail_evtMask])
        hists["eta_VR_fail"].fill(eta_VR_fail=eta2_VR_fail, weight=weights.weight()[VR_fail_evtMask])
        hists["eta_VR_fail"].fill(eta_VR_fail=eta3_VR_fail, weight=weights.weight()[VR_fail_evtMask])
        #-----
        ht_VR_pass_bin = hist.axis.Regular(label=f"{channel} Validation Pass H_{{T}} [GeV]", name="ht_VR_pass", bins=ht_bins, start=ht_start, stop=ht_stop)
        hists["ht_vs_mjjj_VR_pass"] = Hist(j3_VR_pass_bin, ht_VR_pass_bin, storage="weight")
        hists["ht_vs_mjjj_VR_pass"].fill(ht_VR_pass=ht_VR_pass, trijet_mass_VR_pass=trijet_mass_VR_pass, weight=weights.weight()[VR_pass_evtMask])

        eta_VR_pass_bin = hist.axis.Regular(label=f"{channel} Validation Pass Fat Jet #eta", name="eta_VR_pass", bins=eta_bins, start=eta_start, stop=eta_stop)
        hists["eta_VR_pass"] = Hist(eta_VR_pass_bin, storage="weight")
        hists["eta_VR_pass"].fill(eta_VR_pass=eta1_VR_pass, weight=weights.weight()[VR_pass_evtMask])
        hists["eta_VR_pass"].fill(eta_VR_pass=eta2_VR_pass, weight=weights.weight()[VR_pass_evtMask])
        hists["eta_VR_pass"].fill(eta_VR_pass=eta3_VR_pass, weight=weights.weight()[VR_pass_evtMask])

    if isBoosted:
        dijet1_mass_SR_fail = (SR_fail_fj[:,0]+SR_fail_fj[:,1]).mass
        dijet2_mass_SR_fail = (SR_fail_fj[:,0]+SR_fail_fj[:,2]).mass
        dijet3_mass_SR_fail = (SR_fail_fj[:,1]+SR_fail_fj[:,2]).mass
        dijet1_mass_SR_pass = (SR_pass_fj[:,0]+SR_pass_fj[:,1]).mass
        dijet2_mass_SR_pass = (SR_pass_fj[:,0]+SR_pass_fj[:,2]).mass
        dijet3_mass_SR_pass = (SR_pass_fj[:,1]+SR_pass_fj[:,2]).mass

        dijet1_mass_VR_fail = (VR_fail_fj[:,0]+VR_fail_fj[:,1]).mass
        dijet2_mass_VR_fail = (VR_fail_fj[:,0]+VR_fail_fj[:,2]).mass
        dijet3_mass_VR_fail = (VR_fail_fj[:,1]+VR_fail_fj[:,2]).mass
        dijet1_mass_VR_pass = (VR_pass_fj[:,0]+VR_pass_fj[:,1]).mass
        dijet2_mass_VR_pass = (VR_pass_fj[:,0]+VR_pass_fj[:,2]).mass
        dijet3_mass_VR_pass = (VR_pass_fj[:,1]+VR_pass_fj[:,2]).mass
    else:
        dijet1_mass_SR_fail = (SR_fail_fj[:,0]+SR_fail_fj[:,1]).mass
        dijet2_mass_SR_fail = (SR_fail_fj[:,0]+SR_fail_j[:,0]['i0']+SR_fail_j[:,0]['i1']).mass
        dijet3_mass_SR_fail = (SR_fail_fj[:,1]+SR_fail_j[:,0]['i0']+SR_fail_j[:,0]['i1']).mass
        dijet1_mass_SR_pass = (SR_pass_fj[:,0]+SR_pass_fj[:,1]).mass
        dijet2_mass_SR_pass = (SR_pass_fj[:,0]+SR_pass_j[:,0]['i0']+SR_pass_j[:,0]['i1']).mass
        dijet3_mass_SR_pass = (SR_pass_fj[:,1]+SR_pass_j[:,0]['i0']+SR_pass_j[:,0]['i1']).mass

        dijet1_mass_VR_fail = (VR_fail_fj[:,0]+VR_fail_fj[:,1]).mass
        dijet2_mass_VR_fail = (VR_fail_fj[:,0]+VR_fail_j[:,0]['i0']+VR_fail_j[:,0]['i1']).mass
        dijet3_mass_VR_fail = (VR_fail_fj[:,1]+VR_fail_j[:,0]['i0']+VR_fail_j[:,0]['i1']).mass
        dijet1_mass_VR_pass = (VR_pass_fj[:,0]+VR_pass_fj[:,1]).mass
        dijet2_mass_VR_pass = (VR_pass_fj[:,0]+VR_pass_j[:,0]['i0']+VR_pass_j[:,0]['i1']).mass
        dijet3_mass_VR_pass = (VR_pass_fj[:,1]+VR_pass_j[:,0]['i0']+VR_pass_j[:,0]['i1']).mass

    j2_SR_fail_bin = hist.axis.Regular(label=f"{channel} Signal Fail Dijet Mass [GeV]", name="dijet_mass_SR_fail", bins=j2_bins, start=j2_start, stop=j2_stop)
    hists["mjj_vs_mjjj_SR_fail"] = Hist(j3_SR_fail_bin, j2_SR_fail_bin, storage="weight")
    hists["mjj_vs_mjjj_SR_fail"].fill(dijet_mass_SR_fail=dijet1_mass_SR_fail, trijet_mass_SR_fail=trijet_mass_SR_fail, weight=weights.weight()[SR_fail_evtMask])
    hists["mjj_vs_mjjj_SR_fail"].fill(dijet_mass_SR_fail=dijet2_mass_SR_fail, trijet_mass_SR_fail=trijet_mass_SR_fail, weight=weights.weight()[SR_fail_evtMask])
    hists["mjj_vs_mjjj_SR_fail"].fill(dijet_mass_SR_fail=dijet3_mass_SR_fail, trijet_mass_SR_fail=trijet_mass_SR_fail, weight=weights.weight()[SR_fail_evtMask])

    j2_SR_pass_bin = hist.axis.Regular(label=f"{channel} Signal Pass Dijet Mass [GeV]", name="dijet_mass_SR_pass", bins=j2_bins, start=j2_start, stop=j2_stop)
    hists["mjj_vs_mjjj_SR_pass"] = Hist(j3_SR_pass_bin, j2_SR_pass_bin, storage="weight")
    hists["mjj_vs_mjjj_SR_pass"].fill(dijet_mass_SR_pass=dijet1_mass_SR_pass, trijet_mass_SR_pass=trijet_mass_SR_pass, weight=weights.weight()[SR_pass_evtMask])
    hists["mjj_vs_mjjj_SR_pass"].fill(dijet_mass_SR_pass=dijet2_mass_SR_pass, trijet_mass_SR_pass=trijet_mass_SR_pass, weight=weights.weight()[SR_pass_evtMask])
    hists["mjj_vs_mjjj_SR_pass"].fill(dijet_mass_SR_pass=dijet3_mass_SR_pass, trijet_mass_SR_pass=trijet_mass_SR_pass, weight=weights.weight()[SR_pass_evtMask])

    j2_VR_fail_bin = hist.axis.Regular(label=f"{channel} Validation Fail Dijet Mass [GeV]", name="dijet_mass_VR_fail", bins=j2_bins, start=j2_start, stop=j2_stop)
    hists["mjj_vs_mjjj_VR_fail"] = Hist(j3_VR_fail_bin, j2_VR_fail_bin, storage="weight")
    hists["mjj_vs_mjjj_VR_fail"].fill(dijet_mass_VR_fail=dijet1_mass_VR_fail, trijet_mass_VR_fail=trijet_mass_VR_fail, weight=weights.weight()[VR_fail_evtMask])
    hists["mjj_vs_mjjj_VR_fail"].fill(dijet_mass_VR_fail=dijet2_mass_VR_fail, trijet_mass_VR_fail=trijet_mass_VR_fail, weight=weights.weight()[VR_fail_evtMask])
    hists["mjj_vs_mjjj_VR_fail"].fill(dijet_mass_VR_fail=dijet3_mass_VR_fail, trijet_mass_VR_fail=trijet_mass_VR_fail, weight=weights.weight()[VR_fail_evtMask])

    j2_VR_pass_bin = hist.axis.Regular(label=f"{channel} Validation Pass Dijet Mass [GeV]", name="dijet_mass_VR_pass", bins=j2_bins, start=j2_start, stop=j2_stop)
    hists["mjj_vs_mjjj_VR_pass"] = Hist(j3_VR_pass_bin, j2_VR_pass_bin, storage="weight")
    hists["mjj_vs_mjjj_VR_pass"].fill(dijet_mass_VR_pass=dijet1_mass_VR_pass, trijet_mass_VR_pass=trijet_mass_VR_pass, weight=weights.weight()[VR_pass_evtMask])
    hists["mjj_vs_mjjj_VR_pass"].fill(dijet_mass_VR_pass=dijet2_mass_VR_pass, trijet_mass_VR_pass=trijet_mass_VR_pass, weight=weights.weight()[VR_pass_evtMask])
    hists["mjj_vs_mjjj_VR_pass"].fill(dijet_mass_VR_pass=dijet3_mass_VR_pass, trijet_mass_VR_pass=trijet_mass_VR_pass, weight=weights.weight()[VR_pass_evtMask])

    return hists


def fillAllHistos(outHists, suffix, events, selection, weights, event_yield, extraHistos, refTrigList=None, trigList=None):

    trigSuffix = ""
    if refTrigList != None:
        trigSuffix += "_ref"
        if trigList != None:
            trigSuffix += "AndAn"
        trigSuffix += "Trig"

    hists = {}
    hists["boosted"]     = fillHistos("Boosted",     suffix, trigSuffix, events, selection, weights, event_yield, extraHistos, refTrigList, trigList)
    hists["semiboosted"] = fillHistos("Semiboosted", suffix, trigSuffix, events, selection, weights, event_yield, extraHistos, refTrigList, trigList)

    channels = ["boosted", "semiboosted"]
    for ch in channels:
        for hist in hists[ch]:
            outHists[f"{hist}_{ch}{suffix}{trigSuffix}"] = hists[ch][hist]

    return


if __name__ == "__main__":
    import time
    start_time = time.time()
    from argparse import ArgumentParser
    
    parser = ArgumentParser(description="Do -h to see usage")
    parser.add_argument('-s', '--sample', help='Sample name', default="QCD2000")
    parser.add_argument('-i', '--input', help='Input file')
    parser.add_argument('-o', '--output', help='Output directory')
    parser.add_argument("-j", "--jecVariations", dest="jecVariations",
                        help="Space-separated list of JEC variations (default: %(default)s). Use 'fromFile' to turn off the JEC re-application.",
                        nargs='*',
                        default=["nominal","jesUp","jesDown","jerUp","jerDown"],
                        metavar="JECVARS")
    parser.add_argument('-t', '--triggerList', help='Space-separated list of triggers (default: %(default)s);)',
                        nargs='*',
                        dest='triggerList',
                        default = None
                        )
    parser.add_argument("-r", "--refTriggerList", help="Space-separated list of reference triggers (default: %(default)s);)",
                        nargs="*",
                        dest="refTriggerList",
                        default = None
                        )
    parser.add_argument("--disable_corr", dest="disable_corr", action='store_true',
                        help="Disable corrections (default: %(default)s)",
                        default=False)
    parser.add_argument("--extra_histos", dest="extra_histos", action='store_true',
                        help="Switch for producing additional histograms (default: %(default)s)",
                        default=False)

    args = parser.parse_args()
    
    process=args.sample
    input=args.input
    output=args.output
    ofile = os.path.basename(input)
    print(process)
    yearFromInputFile(input)

    knownVariations = copy.deepcopy(parser.get_default('jecVariations'))
    knownVariations.append("fromFile")
    acceptedVariations = []
    unknownVariations = []

    for v in args.jecVariations:
        if v not in knownVariations:
            unknownVariations.append(v)
        else:
            acceptedVariations.append(v)
    if len(unknownVariations)>0:
        if len(acceptedVariations)==0:
            print("Unknown JEC variation(s) specified: {}. Defaulting to 'nominal'.".format(' '.join(unknownVariations)))
            acceptedVariations.append("nominal")
        else:
            print("Unknown JEC variation(s) specified: {}. Will be ignored.".format(' '.join(unknownVariations)))

    # special case of real data
    variations = [v for v in acceptedVariations if v in ["nominal","fromFile"]]
    if len(acceptedVariations)>0 and len(variations)==0:
        print("No appropriate JEC variation(s) for data specified. Defaulting to 'nominal'.")
        variations.append("nominal")

    # output histograms
    outHists = {}
    cutFlowHistos = {}

    # flag defining whether the dataset being processed is MC or not
    isMC = ("JetHT" not in process)
    # total number of events
    numberOfEvents = 0.
    # if MC sample
    if isMC:
        numberOfEvents = getNumberOfGenEvents(input)
        variations     = acceptedVariations

        numberOfGenEventsAxis = hist.axis.Integer(0, 1, label="Number of generated events", underflow=False, overflow=False)
        numberOfGenEventsHisto = Hist(numberOfGenEventsAxis)
        numberOfGenEventsHisto[0] = numberOfEvents
        # save the total number of generated events for MC samples
        outHists["numberOfGenEventsHisto"] = numberOfGenEventsHisto
    else:
        numberOfEvents = getNumberOfEvents(input)

    first_bin = ("Total" if isMC else "Dataset_and_skim")

    # loop over all variations
    for variation in variations:
        suffix = ("" if variation=="fromFile" else f"_{variation}")

        # event yield dictionary
        event_yield = {}

        # apply event selection
        events, selection, weights = Event_selection(input,process,isMC,apply_corrections=(not args.disable_corr),variation=variation,refTrigList=args.refTriggerList,trigList=args.triggerList,eventsToRead=None)

        for r in regions:
            key = f"{r}{suffix}"
            event_yield[key] = {}
            event_yield[key][first_bin] = numberOfEvents
            # storing skimming step for MC only
            if isMC:
                event_yield[key]["Skim"] = ak.sum(weights.weight())
            # if trigger applied and not doing trigger efficiency studies using reference triggers
            if args.triggerList != None and args.refTriggerList == None:
                event_yield[key]["Trigger"] = ak.sum(weights.weight()[selection.all("Trigger")])
            # preselection
            if 'semiboosted' not in r:
                event_yield[key]["Preselection"] = ak.sum(weights.weight()[selection.require(**preselection_boosted)])
            else:
                event_yield[key]["Preselection_fatjets"] = ak.sum(weights.weight()[selection.require(**preselection_semiboosted)])

        #---------------------------------------------
        event_yield[f"SR_boosted{suffix}"]["Mass_cut"] = ak.sum(weights.weight()[selection.require(**mass_cut_SR_boosted)])
        #---------------------------------------------
        event_yield[f"VR_boosted{suffix}"]["Mass_cut"] = ak.sum(weights.weight()[selection.require(**mass_cut_VR_boosted)])
        #---------------------------------------------
        event_yield[f"SR_semiboosted{suffix}"]["Mass_cut_fatjets"]  = ak.sum(weights.weight()[selection.require(**mass_cut_fatjets_SR_semiboosted)])
        event_yield[f"SR_semiboosted{suffix}"]["Preselection_jets"] = ak.sum(weights.weight()[selection.require(**preselection_jets_SR_semiboosted)])
        event_yield[f"SR_semiboosted{suffix}"]["Away_jets"]         = ak.sum(weights.weight()[selection.require(**away_jets_SR_semiboosted )])
        event_yield[f"SR_semiboosted{suffix}"]["Good_dijet"]        = ak.sum(weights.weight()[selection.require(**good_dijet_SR_semiboosted)])
        #---------------------------------------------
        event_yield[f"VR_semiboosted{suffix}"]["Mass_cut_fatjets"]  = ak.sum(weights.weight()[selection.require(**mass_cut_fatjets_VR_semiboosted)])
        event_yield[f"VR_semiboosted{suffix}"]["Preselection_jets"] = ak.sum(weights.weight()[selection.require(**preselection_jets_VR_semiboosted)])
        event_yield[f"VR_semiboosted{suffix}"]["Away_jets"]         = ak.sum(weights.weight()[selection.require(**away_jets_VR_semiboosted)])
        event_yield[f"VR_semiboosted{suffix}"]["Good_dijet"]        = ak.sum(weights.weight()[selection.require(**good_dijet_VR_semiboosted)])
        #---------------------------------------------

        # fill all histograms
        fillAllHistos(outHists, suffix, events, selection, weights, event_yield, args.extra_histos)

        # if doing trigger efficiency studies
        if args.refTriggerList != None:
            fillAllHistos(outHists, suffix, events, selection, weights, event_yield, args.extra_histos, args.refTriggerList)
            # if the analysis trigger(s) are applied as well
            if args.triggerList != None:
                fillAllHistos(outHists, suffix, events, selection, weights, event_yield, args.extra_histos, args.refTriggerList, args.triggerList)

        # create and fill the cut flow histograms
        for r in regions:
            key = f"{r}{suffix}"
            cutFlowHistos[key] = ROOT.TH1D(f"cutFlowHisto_{r}{suffix}", f"{r}{suffix};Cut flow;Number of events", len(event_yield[key].keys()), 0., float(len(event_yield[key].keys())))
            for i, k in enumerate(event_yield[key].keys()):
                cutFlowHistos[key].SetBinContent(i+1, event_yield[key][k])
                cutFlowHistos[key].GetXaxis().SetBinLabel(i+1, k)

    # save histograms to a ROOT file
    with uproot.recreate(os.path.join(output, "Histograms_{0}-{1}".format(process, ofile))) as fout:
        keys = sorted(outHists.keys())
        # if present, save numberOfGenEventsHisto first
        histName = "numberOfGenEventsHisto"
        if histName in keys:
            fout[histName] = outHists[histName]
            keys.remove(histName)
        # save all other histograms
        for histName in keys:
            fout[histName] = outHists[histName]
        #for k in cutFlowHistos.keys():
            #fout[f"cutFlowHisto_{k}"] = cutFlowHistos[k] # this does not work properly (see [*])

    # re-open the ROOT file for some updates and storing additional histograms
    fout = ROOT.TFile.Open(os.path.join(output, "Histograms_{0}-{1}".format(process, ofile)), 'UPDATE')
    # [*] uproot has some issues with storing histograms with labelled bins (apparently only the first bin is stored) so resorting to plain ROOT here
    for k in cutFlowHistos.keys():
        cutFlowHistos[k].Write()
    fout.Close()
    print("--- %s seconds ---" % (time.time() - start_time))
