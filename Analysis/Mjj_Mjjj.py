import os
import copy
import re
import uproot
import awkward as ak
import hist
from hist import Hist
from Selection import *
from Util import *


j3_bins=120
j3_start=0
j3_stop=6000
j2_bins=120
j2_start=0
j2_stop=6000


def plotboosted(boosted_SR_fail, boosted_SR_pass, boosted_VR_fail, boosted_VR_pass, process):

    trijet_mass_SR_fail = (boosted_SR_fail[:,0]+boosted_SR_fail[:,1]+boosted_SR_fail[:,2]).mass
    trijet_mass_SR_pass = (boosted_SR_pass[:,0]+boosted_SR_pass[:,1]+boosted_SR_pass[:,2]).mass

    trijet_mass_VR_fail = (boosted_VR_fail[:,0]+boosted_VR_fail[:,1]+boosted_VR_fail[:,2]).mass
    trijet_mass_VR_pass = (boosted_VR_pass[:,0]+boosted_VR_pass[:,1]+boosted_VR_pass[:,2]).mass

    j3_SR_fail_bin = hist.axis.Regular(label="Boosted Signal Fail Trijet Mass [GeV]", name="trijet_mass_SR_fail", bins=j3_bins, start=j3_start, stop=j3_stop)
    j3_SR_fail_hist = Hist(j3_SR_fail_bin, storage="weight")
    j3_SR_fail_hist.fill(trijet_mass_SR_fail=trijet_mass_SR_fail)

    j3_SR_pass_bin = hist.axis.Regular(label="Boosted Signal Pass Trijet Mass [GeV]", name="trijet_mass_SR_pass", bins=j3_bins, start=j3_start, stop=j3_stop)
    j3_SR_pass_hist = Hist(j3_SR_pass_bin, storage="weight")
    j3_SR_pass_hist.fill(trijet_mass_SR_pass=trijet_mass_SR_pass)

    j3_VR_fail_bin = hist.axis.Regular(label="Boosted Validation Fail Trijet Mass [GeV]", name="trijet_mass_VR_fail", bins=j3_bins, start=j3_start, stop=j3_stop)
    j3_VR_fail_hist = Hist(j3_VR_fail_bin, storage="weight")
    j3_VR_fail_hist.fill(trijet_mass_VR_fail=trijet_mass_VR_fail)

    j3_VR_pass_bin = hist.axis.Regular(label="Boosted Validation Pass Trijet Mass [GeV]", name="trijet_mass_VR_pass", bins=j3_bins, start=j3_start, stop=j3_stop)
    j3_VR_pass_hist = Hist(j3_VR_pass_bin, storage="weight")
    j3_VR_pass_hist.fill(trijet_mass_VR_pass=trijet_mass_VR_pass)

    dijet1_mass_SR_fail = (boosted_SR_fail[:,0]+boosted_SR_fail[:,1]).mass
    dijet2_mass_SR_fail = (boosted_SR_fail[:,0]+boosted_SR_fail[:,2]).mass
    dijet3_mass_SR_fail = (boosted_SR_fail[:,1]+boosted_SR_fail[:,2]).mass
    dijet1_mass_SR_pass = (boosted_SR_pass[:,0]+boosted_SR_pass[:,1]).mass
    dijet2_mass_SR_pass = (boosted_SR_pass[:,0]+boosted_SR_pass[:,2]).mass
    dijet3_mass_SR_pass = (boosted_SR_pass[:,1]+boosted_SR_pass[:,2]).mass

    dijet1_mass_VR_fail = (boosted_VR_fail[:,0]+boosted_VR_fail[:,1]).mass
    dijet2_mass_VR_fail = (boosted_VR_fail[:,0]+boosted_VR_fail[:,2]).mass
    dijet3_mass_VR_fail = (boosted_VR_fail[:,1]+boosted_VR_fail[:,2]).mass
    dijet1_mass_VR_pass = (boosted_VR_pass[:,0]+boosted_VR_pass[:,1]).mass
    dijet2_mass_VR_pass = (boosted_VR_pass[:,0]+boosted_VR_pass[:,2]).mass
    dijet3_mass_VR_pass = (boosted_VR_pass[:,1]+boosted_VR_pass[:,2]).mass

    j2_SR_fail_bin = hist.axis.Regular(label="Boosted Signal Fail Dijet Mass [GeV]", name="dijet_mass_SR_fail", bins=j2_bins, start=j2_start, stop=j2_stop)
    mjj_vs_mjjj_SR_fail = Hist(j3_SR_fail_bin, j2_SR_fail_bin, storage="weight")
    mjj_vs_mjjj_SR_fail.fill(dijet_mass_SR_fail=dijet1_mass_SR_fail,trijet_mass_SR_fail=trijet_mass_SR_fail)
    mjj_vs_mjjj_SR_fail.fill(dijet_mass_SR_fail=dijet2_mass_SR_fail,trijet_mass_SR_fail=trijet_mass_SR_fail)
    mjj_vs_mjjj_SR_fail.fill(dijet_mass_SR_fail=dijet3_mass_SR_fail,trijet_mass_SR_fail=trijet_mass_SR_fail)

    j2_SR_pass_bin = hist.axis.Regular(label="Boosted Signal Pass Dijet Mass [GeV]", name="dijet_mass_SR_pass", bins=j2_bins, start=j2_start, stop=j2_stop)
    mjj_vs_mjjj_SR_pass = Hist(j3_SR_pass_bin, j2_SR_pass_bin, storage="weight")
    mjj_vs_mjjj_SR_pass.fill(dijet_mass_SR_pass=dijet1_mass_SR_pass,trijet_mass_SR_pass=trijet_mass_SR_pass)
    mjj_vs_mjjj_SR_pass.fill(dijet_mass_SR_pass=dijet2_mass_SR_pass,trijet_mass_SR_pass=trijet_mass_SR_pass)
    mjj_vs_mjjj_SR_pass.fill(dijet_mass_SR_pass=dijet3_mass_SR_pass,trijet_mass_SR_pass=trijet_mass_SR_pass)

    j2_VR_fail_bin = hist.axis.Regular(label="Boosted Validation Fail Dijet Mass [GeV]", name="dijet_mass_VR_fail", bins=j2_bins, start=j2_start, stop=j2_stop)
    mjj_vs_mjjj_VR_fail = Hist(j3_VR_fail_bin, j2_VR_fail_bin, storage="weight")
    mjj_vs_mjjj_VR_fail.fill(dijet_mass_VR_fail=dijet1_mass_VR_fail,trijet_mass_VR_fail=trijet_mass_VR_fail)
    mjj_vs_mjjj_VR_fail.fill(dijet_mass_VR_fail=dijet2_mass_VR_fail,trijet_mass_VR_fail=trijet_mass_VR_fail)
    mjj_vs_mjjj_VR_fail.fill(dijet_mass_VR_fail=dijet3_mass_VR_fail,trijet_mass_VR_fail=trijet_mass_VR_fail)

    j2_VR_pass_bin = hist.axis.Regular(label="Boosted Validation Pass Dijet Mass [GeV]", name="dijet_mass_VR_pass", bins=j2_bins, start=j2_start, stop=j2_stop)
    mjj_vs_mjjj_VR_pass = Hist(j3_VR_pass_bin, j2_VR_pass_bin, storage="weight")
    mjj_vs_mjjj_VR_pass.fill(dijet_mass_VR_pass=dijet1_mass_VR_pass,trijet_mass_VR_pass=trijet_mass_VR_pass)
    mjj_vs_mjjj_VR_pass.fill(dijet_mass_VR_pass=dijet2_mass_VR_pass,trijet_mass_VR_pass=trijet_mass_VR_pass)
    mjj_vs_mjjj_VR_pass.fill(dijet_mass_VR_pass=dijet3_mass_VR_pass,trijet_mass_VR_pass=trijet_mass_VR_pass)

    return j3_SR_fail_hist,j3_SR_pass_hist,j3_VR_fail_hist,j3_VR_pass_hist,mjj_vs_mjjj_SR_fail,mjj_vs_mjjj_SR_pass,mjj_vs_mjjj_VR_fail,mjj_vs_mjjj_VR_pass


def plotsemiboosted(label, semiboosted_SR_fail_fatjet, semiboosted_SR_pass_fatjet, semiboosted_SR_fail_jet, semiboosted_SR_pass_jet, semiboosted_VR_fail_fatjet, semiboosted_VR_pass_fatjet, semiboosted_VR_fail_jet, semiboosted_VR_pass_jet, process):

    trijet_mass_SR_fail = (semiboosted_SR_fail_fatjet[:,0]+semiboosted_SR_fail_fatjet[:,1]+semiboosted_SR_fail_jet[:,0]['i0']+semiboosted_SR_fail_jet[:,0]['i1']).mass
    trijet_mass_SR_pass = (semiboosted_SR_pass_fatjet[:,0]+semiboosted_SR_pass_fatjet[:,1]+semiboosted_SR_pass_jet[:,0]['i0']+semiboosted_SR_pass_jet[:,0]['i1']).mass

    trijet_mass_VR_fail = (semiboosted_VR_fail_fatjet[:,0]+semiboosted_VR_fail_fatjet[:,1]+semiboosted_VR_fail_jet[:,0]['i0']+semiboosted_VR_fail_jet[:,0]['i1']).mass
    trijet_mass_VR_pass = (semiboosted_VR_pass_fatjet[:,0]+semiboosted_VR_pass_fatjet[:,1]+semiboosted_VR_pass_jet[:,0]['i0']+semiboosted_VR_pass_jet[:,0]['i1']).mass

    j3_SR_fail_bin = hist.axis.Regular(label=f"{label} Signal Fail Trijet Mass [GeV]", name="trijet_mass_SR_fail", bins=j3_bins, start=j3_start, stop=j3_stop)
    j3_SR_fail_hist = Hist(j3_SR_fail_bin, storage="weight")
    j3_SR_fail_hist.fill(trijet_mass_SR_fail=trijet_mass_SR_fail)

    j3_SR_pass_bin = hist.axis.Regular(label=f"{label} Signal Pass Trijet Mass [GeV]", name="trijet_mass_SR_pass", bins=j3_bins, start=j3_start, stop=j3_stop)
    j3_SR_pass_hist = Hist(j3_SR_pass_bin, storage="weight")
    j3_SR_pass_hist.fill(trijet_mass_SR_pass=trijet_mass_SR_pass)

    j3_VR_fail_bin = hist.axis.Regular(label=f"{label} Validation Fail Trijet Mass [GeV]", name="trijet_mass_VR_fail", bins=j3_bins, start=j3_start, stop=j3_stop)
    j3_VR_fail_hist = Hist(j3_VR_fail_bin, storage="weight")
    j3_VR_fail_hist.fill(trijet_mass_VR_fail=trijet_mass_VR_fail)

    j3_VR_pass_bin = hist.axis.Regular(label=f"{label} Validation Pass Trijet Mass [GeV]", name="trijet_mass_VR_pass", bins=j3_bins, start=j3_start, stop=j3_stop)
    j3_VR_pass_hist = Hist(j3_VR_pass_bin, storage="weight")
    j3_VR_pass_hist.fill(trijet_mass_VR_pass=trijet_mass_VR_pass)

    dijet1_mass_SR_fail = (semiboosted_SR_fail_fatjet[:,0]+semiboosted_SR_fail_fatjet[:,1]).mass
    dijet2_mass_SR_fail = (semiboosted_SR_fail_fatjet[:,0]+semiboosted_SR_fail_jet[:,0]['i0']+semiboosted_SR_fail_jet[:,0]['i1']).mass
    dijet3_mass_SR_fail = (semiboosted_SR_fail_fatjet[:,1]+semiboosted_SR_fail_jet[:,0]['i0']+semiboosted_SR_fail_jet[:,0]['i1']).mass
    dijet1_mass_SR_pass = (semiboosted_SR_pass_fatjet[:,0]+semiboosted_SR_pass_fatjet[:,1]).mass
    dijet2_mass_SR_pass = (semiboosted_SR_pass_fatjet[:,0]+semiboosted_SR_pass_jet[:,0]['i0']+semiboosted_SR_pass_jet[:,0]['i1']).mass
    dijet3_mass_SR_pass = (semiboosted_SR_pass_fatjet[:,1]+semiboosted_SR_pass_jet[:,0]['i0']+semiboosted_SR_pass_jet[:,0]['i1']).mass

    dijet1_mass_VR_fail = (semiboosted_VR_fail_fatjet[:,0]+semiboosted_VR_fail_fatjet[:,1]).mass
    dijet2_mass_VR_fail = (semiboosted_VR_fail_fatjet[:,0]+semiboosted_VR_fail_jet[:,0]['i0']+semiboosted_VR_fail_jet[:,0]['i1']).mass
    dijet3_mass_VR_fail = (semiboosted_VR_fail_fatjet[:,1]+semiboosted_VR_fail_jet[:,0]['i0']+semiboosted_VR_fail_jet[:,0]['i1']).mass
    dijet1_mass_VR_pass = (semiboosted_VR_pass_fatjet[:,0]+semiboosted_VR_pass_fatjet[:,1]).mass
    dijet2_mass_VR_pass = (semiboosted_VR_pass_fatjet[:,0]+semiboosted_VR_pass_jet[:,0]['i0']+semiboosted_VR_pass_jet[:,0]['i1']).mass
    dijet3_mass_VR_pass = (semiboosted_VR_pass_fatjet[:,1]+semiboosted_VR_pass_jet[:,0]['i0']+semiboosted_VR_pass_jet[:,0]['i1']).mass

    j2_SR_fail_bin = hist.axis.Regular(label=f"{label} Signal Fail Dijet Mass [GeV]", name="dijet_mass_SR_fail", bins=j2_bins, start=j2_start, stop=j2_stop)
    mjj_vs_mjjj_SR_fail = Hist(j3_SR_fail_bin, j2_SR_fail_bin, storage="weight")
    mjj_vs_mjjj_SR_fail.fill(dijet_mass_SR_fail=dijet1_mass_SR_fail,trijet_mass_SR_fail=trijet_mass_SR_fail)
    mjj_vs_mjjj_SR_fail.fill(dijet_mass_SR_fail=dijet2_mass_SR_fail,trijet_mass_SR_fail=trijet_mass_SR_fail)
    mjj_vs_mjjj_SR_fail.fill(dijet_mass_SR_fail=dijet3_mass_SR_fail,trijet_mass_SR_fail=trijet_mass_SR_fail)

    j2_SR_pass_bin = hist.axis.Regular(label=f"{label} Signal Pass Dijet Mass [GeV]", name="dijet_mass_SR_pass", bins=j2_bins, start=j2_start, stop=j2_stop)
    mjj_vs_mjjj_SR_pass = Hist(j3_SR_pass_bin, j2_SR_pass_bin, storage="weight")
    mjj_vs_mjjj_SR_pass.fill(dijet_mass_SR_pass=dijet1_mass_SR_pass,trijet_mass_SR_pass=trijet_mass_SR_pass)
    mjj_vs_mjjj_SR_pass.fill(dijet_mass_SR_pass=dijet2_mass_SR_pass,trijet_mass_SR_pass=trijet_mass_SR_pass)
    mjj_vs_mjjj_SR_pass.fill(dijet_mass_SR_pass=dijet3_mass_SR_pass,trijet_mass_SR_pass=trijet_mass_SR_pass)

    j2_VR_fail_bin = hist.axis.Regular(label=f"{label} Validation Fail Dijet Mass [GeV]", name="dijet_mass_VR_fail", bins=j2_bins, start=j2_start, stop=j2_stop)
    mjj_vs_mjjj_VR_fail = Hist(j3_VR_fail_bin, j2_VR_fail_bin, storage="weight")
    mjj_vs_mjjj_VR_fail.fill(dijet_mass_VR_fail=dijet1_mass_VR_fail,trijet_mass_VR_fail=trijet_mass_VR_fail)
    mjj_vs_mjjj_VR_fail.fill(dijet_mass_VR_fail=dijet2_mass_VR_fail,trijet_mass_VR_fail=trijet_mass_VR_fail)
    mjj_vs_mjjj_VR_fail.fill(dijet_mass_VR_fail=dijet3_mass_VR_fail,trijet_mass_VR_fail=trijet_mass_VR_fail)

    j2_VR_pass_bin = hist.axis.Regular(label=f"{label} Validation Pass Dijet Mass [GeV]", name="dijet_mass_VR_pass", bins=j2_bins, start=j2_start, stop=j2_stop)
    mjj_vs_mjjj_VR_pass = Hist(j3_VR_pass_bin, j2_VR_pass_bin, storage="weight")
    mjj_vs_mjjj_VR_pass.fill(dijet_mass_VR_pass=dijet1_mass_VR_pass,trijet_mass_VR_pass=trijet_mass_VR_pass)
    mjj_vs_mjjj_VR_pass.fill(dijet_mass_VR_pass=dijet2_mass_VR_pass,trijet_mass_VR_pass=trijet_mass_VR_pass)
    mjj_vs_mjjj_VR_pass.fill(dijet_mass_VR_pass=dijet3_mass_VR_pass,trijet_mass_VR_pass=trijet_mass_VR_pass)

    return j3_SR_fail_hist,j3_SR_pass_hist,j3_VR_fail_hist,j3_VR_pass_hist,mjj_vs_mjjj_SR_fail,mjj_vs_mjjj_SR_pass,mjj_vs_mjjj_VR_fail,mjj_vs_mjjj_VR_pass


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
    numberOfGenEvents = 0.
    # if MC sample
    if ("JetHT" not in process):
        numberOfGenEvents = getNumberOfGenEvents(input)
        variations        = acceptedVariations
    numberOfGenEventsAxis = hist.axis.Integer(0, 1, label="Number of generated events", underflow=False, overflow=False)
    numberOfGenEventsHisto = Hist(numberOfGenEventsAxis)
    numberOfGenEventsHisto[0] = numberOfGenEvents

    event_counts = {}
    first_bin = ("Total" if "JetHT" not in process else "Dataset")
    
    regions = ["SR_boosted", "VR_boosted", "SR_semiboosted", "VR_semiboosted"]
    for r in regions:
        event_counts[r] = {}
        event_counts[r][first_bin] = (numberOfGenEvents if "JetHT" not in process else getNumberOfEvents(input))   

    outHists = {}
    saveOnceDone = False
    saveOnceMCDone = False

    for variation in variations:

        boosted_SR_fail, boosted_SR_pass, boosted_VR_fail, boosted_VR_pass, semiboosted_SR_fail_fatjet, semiboosted_SR_pass_fatjet, semiboosted_SR_fail_jet, semiboosted_SR_pass_jet, semiboosted_VR_fail_fatjet, semiboosted_VR_pass_fatjet, semiboosted_VR_fail_jet, semiboosted_VR_pass_jet, semiboosted_eq2_SR_fail_fatjet, semiboosted_eq2_SR_pass_fatjet, semiboosted_eq2_SR_fail_jet, semiboosted_eq2_SR_pass_jet, semiboosted_eq2_VR_fail_fatjet, semiboosted_eq2_VR_pass_fatjet, semiboosted_eq2_VR_fail_jet, semiboosted_eq2_VR_pass_jet = Event_selection(input,process,event_counts,variation=variation,trigList=args.triggerList,refTrigList=args.refTriggerList,eventsToRead=None)

        if not saveOnceDone and variation in ["nominal","fromFile"]:
            # give priority to nominal if running both 'nominal' and 'fromFile'
            if variation=="nominal":
                saveOnceDone = True

            event_counts["SR_boosted"]["Fail"] = len(boosted_SR_fail)
            event_counts["SR_boosted"]["Pass"] = len(boosted_SR_pass)
            event_counts["VR_boosted"]["Fail"] = len(boosted_VR_fail)
            event_counts["VR_boosted"]["Pass"] = len(boosted_VR_pass)
            event_counts["SR_semiboosted"]["Fail"] = len(semiboosted_SR_fail_fatjet)
            event_counts["SR_semiboosted"]["Pass"] = len(semiboosted_SR_pass_fatjet)
            event_counts["VR_semiboosted"]["Fail"] = len(semiboosted_VR_fail_fatjet)
            event_counts["VR_semiboosted"]["Pass"] = len(semiboosted_VR_pass_fatjet)
            event_counts["SR_semiboosted"]["Fail"] += len(semiboosted_eq2_SR_fail_fatjet)
            event_counts["SR_semiboosted"]["Pass"] += len(semiboosted_eq2_SR_pass_fatjet)
            event_counts["VR_semiboosted"]["Fail"] += len(semiboosted_eq2_VR_fail_fatjet)
            event_counts["VR_semiboosted"]["Pass"] += len(semiboosted_eq2_VR_pass_fatjet)

            cutFlowHistos = {}
            for r in regions:
                cutFlowHistos[r] = ROOT.TH1D(f"cutFlowHisto_{r}", f"{r};Cut flow;Number of events", len(event_counts[r].keys()), 0., float(len(event_counts[r].keys())))
                for i, key in enumerate(event_counts[r].keys()):
                    cutFlowHistos[r].SetBinContent(i+1, event_counts[r][key])
                    cutFlowHistos[r].GetXaxis().SetBinLabel(i+1, key)
            
        j3_SR_fail_boosted,j3_SR_pass_boosted,j3_VR_fail_boosted,j3_VR_pass_boosted,mjj_vs_mjjj_SR_fail_boosted,mjj_vs_mjjj_SR_pass_boosted,mjj_vs_mjjj_VR_fail_boosted,mjj_vs_mjjj_VR_pass_boosted = plotboosted(boosted_SR_fail,boosted_SR_pass,boosted_VR_fail,boosted_VR_pass,process)                  
        j3_SR_fail_semiboosted,j3_SR_pass_semiboosted,j3_VR_fail_semiboosted,j3_VR_pass_semiboosted,mjj_vs_mjjj_SR_fail_semiboosted,mjj_vs_mjjj_SR_pass_semiboosted,mjj_vs_mjjj_VR_fail_semiboosted,mjj_vs_mjjj_VR_pass_semiboosted = plotsemiboosted("Semiboosted", semiboosted_SR_fail_fatjet, semiboosted_SR_pass_fatjet,semiboosted_SR_fail_jet, semiboosted_SR_pass_jet,semiboosted_VR_fail_fatjet,semiboosted_VR_pass_fatjet,semiboosted_VR_fail_jet,semiboosted_VR_pass_jet,process)
        j3_SR_fail_semiboosted_eq2,j3_SR_pass_semiboosted_eq2,j3_VR_fail_semiboosted_eq2,j3_VR_pass_semiboosted_eq2,mjj_vs_mjjj_SR_fail_semiboosted_eq2,mjj_vs_mjjj_SR_pass_semiboosted_eq2,mjj_vs_mjjj_VR_fail_semiboosted_eq2,mjj_vs_mjjj_VR_pass_semiboosted_eq2 = plotsemiboosted("Semiboosted_eq2", semiboosted_eq2_SR_fail_fatjet, semiboosted_eq2_SR_pass_fatjet,semiboosted_eq2_SR_fail_jet, semiboosted_eq2_SR_pass_jet,semiboosted_eq2_VR_fail_fatjet,semiboosted_eq2_VR_pass_fatjet,semiboosted_eq2_VR_fail_jet,semiboosted_eq2_VR_pass_jet,process)
        
        if (not saveOnceMCDone and "JetHT" not in process and variation in ["nominal","fromFile"]):
            saveOnceMCDone = True
            outHists[f"numberOfGenEventsHisto"] = numberOfGenEventsHisto

        suffix = ("" if variation=="fromFile" else f"_{variation}")

        outHists[f"j3_SR_pass_boosted{suffix}"] = j3_SR_pass_boosted
        outHists[f"j3_VR_pass_boosted{suffix}"] = j3_VR_pass_boosted
        outHists[f"mjj_vs_mjjj_SR_pass_boosted{suffix}"] = mjj_vs_mjjj_SR_pass_boosted
        outHists[f"mjj_vs_mjjj_VR_pass_boosted{suffix}"] = mjj_vs_mjjj_VR_pass_boosted
        outHists[f"j3_SR_fail_boosted{suffix}"] = j3_SR_fail_boosted
        outHists[f"j3_VR_fail_boosted{suffix}"] = j3_VR_fail_boosted
        outHists[f"mjj_vs_mjjj_SR_fail_boosted{suffix}"] = mjj_vs_mjjj_SR_fail_boosted
        outHists[f"mjj_vs_mjjj_VR_fail_boosted{suffix}"] = mjj_vs_mjjj_VR_fail_boosted
        outHists[f"j3_SR_pass_semiboosted{suffix}"] = j3_SR_pass_semiboosted
        outHists[f"j3_VR_pass_semiboosted{suffix}"] = j3_VR_pass_semiboosted
        outHists[f"mjj_vs_mjjj_SR_pass_semiboosted{suffix}"] = mjj_vs_mjjj_SR_pass_semiboosted
        outHists[f"mjj_vs_mjjj_VR_pass_semiboosted{suffix}"] = mjj_vs_mjjj_VR_pass_semiboosted
        outHists[f"j3_SR_fail_semiboosted{suffix}"] = j3_SR_fail_semiboosted
        outHists[f"j3_VR_fail_semiboosted{suffix}"] = j3_VR_fail_semiboosted
        outHists[f"mjj_vs_mjjj_SR_fail_semiboosted{suffix}"] = mjj_vs_mjjj_SR_fail_semiboosted
        outHists[f"mjj_vs_mjjj_VR_fail_semiboosted{suffix}"] = mjj_vs_mjjj_VR_fail_semiboosted
        outHists[f"j3_SR_pass_semiboosted_eq2{suffix}"] = j3_SR_pass_semiboosted_eq2
        outHists[f"j3_VR_pass_semiboosted_eq2{suffix}"] = j3_VR_pass_semiboosted_eq2
        outHists[f"mjj_vs_mjjj_SR_pass_semiboosted_eq2{suffix}"] = mjj_vs_mjjj_SR_pass_semiboosted_eq2
        outHists[f"mjj_vs_mjjj_VR_pass_semiboosted_eq2{suffix}"] = mjj_vs_mjjj_VR_pass_semiboosted_eq2
        outHists[f"j3_SR_fail_semiboosted_eq2{suffix}"] = j3_SR_fail_semiboosted_eq2
        outHists[f"j3_VR_fail_semiboosted_eq2{suffix}"] = j3_VR_fail_semiboosted_eq2
        outHists[f"mjj_vs_mjjj_SR_fail_semiboosted_eq2{suffix}"] = mjj_vs_mjjj_SR_fail_semiboosted_eq2
        outHists[f"mjj_vs_mjjj_VR_fail_semiboosted_eq2{suffix}"] = mjj_vs_mjjj_VR_fail_semiboosted_eq2
        # for r in regions:
                # fout[f"cutFlowHisto_{r}"] = cutFlowHistos[r] # this does not work properly (see [*])
        
    with uproot.recreate(os.path.join(output, "Histograms_{0}-{1}".format(process, ofile))) as fout:
        for histName in outHists:
            fout[histName] = outHists[histName]

    fout = ROOT.TFile.Open(os.path.join(output, "Histograms_{0}-{1}".format(process, ofile)), 'UPDATE')
    list_of_keys = copy.deepcopy(fout.GetListOfKeys()) # without deepcopy the processing time explodes, no idea why
    for myKey in list_of_keys:
        if re.match ('TH', myKey.GetClassName()):
            hname = myKey.GetName()
            if ("eq2" not in hname):
                continue
            h_eq2 = fout.Get(hname)
            h = fout.Get(hname.replace("_eq2", ""))
            h.Add(h_eq2)
            h.Write("", ROOT.TObject.kOverwrite)
            fout.Delete(hname + ";1")
    # [*] uproot has some issues with storing histograms with labelled bins (apparently only the first bin is stored) so resorting to plain ROOT here
    for r in regions:
        cutFlowHistos[r].Write()
    fout.Close()
    print("--- %s seconds ---" % (time.time() - start_time))
