import os
import uproot
import awkward as ak
import hist
from hist import Hist
from Selection import *
from Util import *

def plotboosted(boosted_SR_fail, boosted_SR_pass,boosted_VR_fail,boosted_VR_pass,scale,process):

    trijet_mass_SR_fail = (boosted_SR_fail[:,0]+boosted_SR_fail[:,1]+boosted_SR_fail[:,2]).mass
    trijet_mass_SR_pass = (boosted_SR_pass[:,0]+boosted_SR_pass[:,1]+boosted_SR_pass[:,2]).mass

    trijet_mass_VR_fail = (boosted_VR_fail[:,0]+boosted_VR_fail[:,1]+boosted_VR_fail[:,2]).mass
    trijet_mass_VR_pass = (boosted_VR_pass[:,0]+boosted_VR_pass[:,1]+boosted_VR_pass[:,2]).mass

    j3_SR_fail_bin = hist.axis.Regular(label="Boosted Signal Fail Trijet Mass [GeV]", name="trijet_mass_SR_fail", bins=120, start=0, stop=6000)
    j3_SR_fail_hist = Hist(j3_SR_fail_bin)
    j3_SR_fail_hist.fill(trijet_mass_SR_fail=trijet_mass_SR_fail)
    j3_SR_fail_hist *= scale

    j3_SR_pass_bin = hist.axis.Regular(label="Boosted Signal Pass Trijet Mass [GeV]", name="trijet_mass_SR_pass", bins=120, start=0, stop=6000)
    j3_SR_pass_hist = Hist(j3_SR_pass_bin)
    j3_SR_pass_hist.fill(trijet_mass_SR_pass=trijet_mass_SR_pass)
    j3_SR_pass_hist *= scale

    j3_VR_fail_bin = hist.axis.Regular(label="Boosted Validation Fail Trijet Mass [GeV]", name="trijet_mass_VR_fail", bins=120, start=0, stop=6000)
    j3_VR_fail_hist = Hist(j3_VR_fail_bin)
    j3_VR_fail_hist.fill(trijet_mass_VR_fail=trijet_mass_VR_fail)
    j3_VR_fail_hist *= scale

    j3_VR_pass_bin = hist.axis.Regular(label="Boosted Validation Pass Trijet Mass [GeV]", name="trijet_mass_VR_pass", bins=120, start=0, stop=6000)
    j3_VR_pass_hist = Hist(j3_VR_pass_bin)
    j3_VR_pass_hist.fill(trijet_mass_VR_pass=trijet_mass_VR_pass)
    j3_VR_pass_hist *= scale

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

    j2_SR_fail_bin = hist.axis.Regular(label="Boosted Signal Fail Dijet Mass [GeV]", name="dijet_mass_SR_fail", bins=80, start=0, stop=4000)
    mjj_vs_mjjj_SR_fail = Hist(j3_SR_fail_bin, j2_SR_fail_bin)
    mjj_vs_mjjj_SR_fail.fill(dijet_mass_SR_fail=dijet1_mass_SR_fail,trijet_mass_SR_fail=trijet_mass_SR_fail)
    mjj_vs_mjjj_SR_fail.fill(dijet_mass_SR_fail=dijet2_mass_SR_fail,trijet_mass_SR_fail=trijet_mass_SR_fail)
    mjj_vs_mjjj_SR_fail.fill(dijet_mass_SR_fail=dijet3_mass_SR_fail,trijet_mass_SR_fail=trijet_mass_SR_fail)
    mjj_vs_mjjj_SR_fail *= scale

    j2_SR_pass_bin = hist.axis.Regular(label="Boosted Signal Pass Dijet Mass [GeV]", name="dijet_mass_SR_pass", bins=80, start=0, stop=4000)
    mjj_vs_mjjj_SR_pass = Hist(j3_SR_pass_bin, j2_SR_pass_bin)
    mjj_vs_mjjj_SR_pass.fill(dijet_mass_SR_pass=dijet1_mass_SR_pass,trijet_mass_SR_pass=trijet_mass_SR_pass)
    mjj_vs_mjjj_SR_pass.fill(dijet_mass_SR_pass=dijet2_mass_SR_pass,trijet_mass_SR_pass=trijet_mass_SR_pass)
    mjj_vs_mjjj_SR_pass.fill(dijet_mass_SR_pass=dijet3_mass_SR_pass,trijet_mass_SR_pass=trijet_mass_SR_pass)
    mjj_vs_mjjj_SR_pass *= scale

    j2_VR_fail_bin = hist.axis.Regular(label="Boosted Validation Fail Dijet Mass [GeV]", name="dijet_mass_VR_fail", bins=80, start=0, stop=4000)
    mjj_vs_mjjj_VR_fail = Hist(j3_VR_fail_bin, j2_VR_fail_bin)
    mjj_vs_mjjj_VR_fail.fill(dijet_mass_VR_fail=dijet1_mass_VR_fail,trijet_mass_VR_fail=trijet_mass_VR_fail)
    mjj_vs_mjjj_VR_fail.fill(dijet_mass_VR_fail=dijet2_mass_VR_fail,trijet_mass_VR_fail=trijet_mass_VR_fail)
    mjj_vs_mjjj_VR_fail.fill(dijet_mass_VR_fail=dijet3_mass_VR_fail,trijet_mass_VR_fail=trijet_mass_VR_fail)
    mjj_vs_mjjj_VR_fail *= scale

    j2_VR_pass_bin = hist.axis.Regular(label="Boosted Validation Pass Dijet Mass [GeV]", name="dijet_mass_VR_pass", bins=80, start=0, stop=4000)
    mjj_vs_mjjj_VR_pass = Hist(j3_VR_pass_bin, j2_VR_pass_bin)
    mjj_vs_mjjj_VR_pass.fill(dijet_mass_VR_pass=dijet1_mass_VR_pass,trijet_mass_VR_pass=trijet_mass_VR_pass)
    mjj_vs_mjjj_VR_pass.fill(dijet_mass_VR_pass=dijet2_mass_VR_pass,trijet_mass_VR_pass=trijet_mass_VR_pass)
    mjj_vs_mjjj_VR_pass.fill(dijet_mass_VR_pass=dijet3_mass_VR_pass,trijet_mass_VR_pass=trijet_mass_VR_pass)
    mjj_vs_mjjj_VR_pass *= scale

    return j3_SR_fail_hist,j3_SR_pass_hist,j3_VR_fail_hist,j3_VR_pass_hist,mjj_vs_mjjj_SR_fail,mjj_vs_mjjj_SR_pass,mjj_vs_mjjj_VR_fail,mjj_vs_mjjj_VR_pass


def plotsemiboosted(semiboosted_SR_fail_fatjet, semiboosted_SR_pass_fatjet,semiboosted_SR_fail_jet, semiboosted_SR_pass_jet,semiboosted_VR_fail_fatjet,semiboosted_VR_pass_fatjet,semiboosted_VR_fail_jet,semiboosted_VR_pass_jet,scale,process):

    trijet_mass_SR_fail = (semiboosted_SR_fail_fatjet[:,0]+semiboosted_SR_fail_fatjet[:,1]+semiboosted_SR_fail_jet[:,0]['i0']+semiboosted_SR_fail_jet[:,0]['i1']).mass
    trijet_mass_SR_pass = (semiboosted_SR_pass_fatjet[:,0]+semiboosted_SR_pass_fatjet[:,1]+semiboosted_SR_pass_jet[:,0]['i0']+semiboosted_SR_pass_jet[:,0]['i1']).mass

    trijet_mass_VR_fail = (semiboosted_VR_fail_fatjet[:,0]+semiboosted_VR_fail_fatjet[:,1]+semiboosted_VR_fail_jet[:,0]['i0']+semiboosted_VR_fail_jet[:,0]['i1']).mass
    trijet_mass_VR_pass = (semiboosted_VR_pass_fatjet[:,0]+semiboosted_VR_pass_fatjet[:,1]+semiboosted_VR_pass_jet[:,0]['i0']+semiboosted_VR_pass_jet[:,0]['i1']).mass

    j3_SR_fail_bin = hist.axis.Regular(label="semiBoosted Signal Fail Trijet Mass [GeV]", name="trijet_mass_SR_fail", bins=120, start=0, stop=6000)
    j3_SR_fail_hist = Hist(j3_SR_fail_bin)
    j3_SR_fail_hist.fill(trijet_mass_SR_fail=trijet_mass_SR_fail)
    j3_SR_fail_hist *= scale

    j3_SR_pass_bin = hist.axis.Regular(label="semiBoosted Signal Pass Trijet Mass [GeV]", name="trijet_mass_SR_pass", bins=120, start=0, stop=6000)
    j3_SR_pass_hist = Hist(j3_SR_pass_bin)
    j3_SR_pass_hist.fill(trijet_mass_SR_pass=trijet_mass_SR_pass)
    j3_SR_pass_hist *= scale

    j3_VR_fail_bin = hist.axis.Regular(label="semiBoosted Validation Fail Trijet Mass [GeV]", name="trijet_mass_VR_fail", bins=120, start=0, stop=6000)
    j3_VR_fail_hist = Hist(j3_VR_fail_bin)
    j3_VR_fail_hist.fill(trijet_mass_VR_fail=trijet_mass_VR_fail)
    j3_VR_fail_hist *= scale

    j3_VR_pass_bin = hist.axis.Regular(label="semiBoosted Validation Pass Trijet Mass [GeV]", name="trijet_mass_VR_pass", bins=120, start=0, stop=6000)
    j3_VR_pass_hist = Hist(j3_VR_pass_bin)
    j3_VR_pass_hist.fill(trijet_mass_VR_pass=trijet_mass_VR_pass)
    j3_VR_pass_hist *= scale

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

    j2_SR_fail_bin = hist.axis.Regular(label="Semiboosted Signal Fail Dijet Mass [GeV]", name="dijet_mass_SR_fail", bins=80, start=0, stop=4000)
    mjj_vs_mjjj_SR_fail = Hist(j3_SR_fail_bin, j2_SR_fail_bin)
    mjj_vs_mjjj_SR_fail.fill(dijet_mass_SR_fail=dijet1_mass_SR_fail,trijet_mass_SR_fail=trijet_mass_SR_fail)
    mjj_vs_mjjj_SR_fail.fill(dijet_mass_SR_fail=dijet2_mass_SR_fail,trijet_mass_SR_fail=trijet_mass_SR_fail)
    mjj_vs_mjjj_SR_fail.fill(dijet_mass_SR_fail=dijet3_mass_SR_fail,trijet_mass_SR_fail=trijet_mass_SR_fail)
    mjj_vs_mjjj_SR_fail *= scale

    j2_SR_pass_bin = hist.axis.Regular(label="Semiboosted Signal Pass Dijet Mass [GeV]", name="dijet_mass_SR_pass", bins=80, start=0, stop=4000)
    mjj_vs_mjjj_SR_pass = Hist(j3_SR_pass_bin, j2_SR_pass_bin)
    mjj_vs_mjjj_SR_pass.fill(dijet_mass_SR_pass=dijet1_mass_SR_pass,trijet_mass_SR_pass=trijet_mass_SR_pass)
    mjj_vs_mjjj_SR_pass.fill(dijet_mass_SR_pass=dijet2_mass_SR_pass,trijet_mass_SR_pass=trijet_mass_SR_pass)
    mjj_vs_mjjj_SR_pass.fill(dijet_mass_SR_pass=dijet3_mass_SR_pass,trijet_mass_SR_pass=trijet_mass_SR_pass)
    mjj_vs_mjjj_SR_pass *= scale

    j2_VR_fail_bin = hist.axis.Regular(label="Semiboosted Validation Fail Dijet Mass [GeV]", name="dijet_mass_VR_fail", bins=80, start=0, stop=4000)
    mjj_vs_mjjj_VR_fail = Hist(j3_VR_fail_bin, j2_VR_fail_bin)
    mjj_vs_mjjj_VR_fail.fill(dijet_mass_VR_fail=dijet1_mass_VR_fail,trijet_mass_VR_fail=trijet_mass_VR_fail)
    mjj_vs_mjjj_VR_fail.fill(dijet_mass_VR_fail=dijet2_mass_VR_fail,trijet_mass_VR_fail=trijet_mass_VR_fail)
    mjj_vs_mjjj_VR_fail.fill(dijet_mass_VR_fail=dijet3_mass_VR_fail,trijet_mass_VR_fail=trijet_mass_VR_fail)
    mjj_vs_mjjj_VR_fail *= scale

    j2_VR_pass_bin = hist.axis.Regular(label="Semiboosted Validation Pass Dijet Mass [GeV]", name="dijet_mass_VR_pass", bins=80, start=0, stop=4000)
    mjj_vs_mjjj_VR_pass = Hist(j3_VR_pass_bin, j2_VR_pass_bin)
    mjj_vs_mjjj_VR_pass.fill(dijet_mass_VR_pass=dijet1_mass_VR_pass,trijet_mass_VR_pass=trijet_mass_VR_pass)
    mjj_vs_mjjj_VR_pass.fill(dijet_mass_VR_pass=dijet2_mass_VR_pass,trijet_mass_VR_pass=trijet_mass_VR_pass)
    mjj_vs_mjjj_VR_pass.fill(dijet_mass_VR_pass=dijet3_mass_VR_pass,trijet_mass_VR_pass=trijet_mass_VR_pass)
    mjj_vs_mjjj_VR_pass *= scale

    return j3_SR_fail_hist,j3_SR_pass_hist,j3_VR_fail_hist,j3_VR_pass_hist,mjj_vs_mjjj_SR_fail,mjj_vs_mjjj_SR_pass,mjj_vs_mjjj_VR_fail,mjj_vs_mjjj_VR_pass


if __name__ == "__main__":
    from argparse import ArgumentParser
    
    parser = ArgumentParser(description="Do -h to see usage")
    parser.add_argument('-s', '--sample', help='Sample name', default="QCD2000")
    parser.add_argument('-i', '--input', help='Input file')
    parser.add_argument('-o', '--output', help='Output directory')
    args = parser.parse_args()
    
    process=args.sample
    input=args.input
    output=args.output
    ofile = os.path.basename(input)
    print(process)
    year = "2017"
    boosted_SR_fail, boosted_SR_pass = Signal_boosted(input,process,eventsToRead=None)                                                                                              
    boosted_VR_fail,boosted_VR_pass = Validation_boosted(input,process,eventsToRead=None)                                                                                                   
    semiboosted_SR_fail_fatjet, semiboosted_SR_pass_fatjet,semiboosted_SR_fail_jet, semiboosted_SR_pass_jet = Signal_semiboosted(input,process,eventsToRead=None)
    semiboosted_VR_fail_fatjet,semiboosted_VR_pass_fatjet,semiboosted_VR_fail_jet,semiboosted_VR_pass_jet = Validation_semiboosted(input,process,eventsToRead=None)

    scale = 1
    numberOfGenEvents = 0.
    if ("JetHT" not in process):
        numberOfGenEvents = getNumberOfGenEvents(input)
    numberOfGenEventsAxis = hist.axis.Integer(0, 1, underflow=False, overflow=False)
    numberOfGenEventsHisto = Hist(numberOfGenEventsAxis)
    numberOfGenEventsHisto[0] = numberOfGenEvents
    
    j3_SR_fail_boosted,j3_SR_pass_boosted,j3_VR_fail_boosted,j3_VR_pass_boosted,mjj_vs_mjjj_SR_fail_boosted,mjj_vs_mjjj_SR_pass_boosted,mjj_vs_mjjj_VR_fail_boosted,mjj_vs_mjjj_VR_pass_boosted = plotboosted(boosted_SR_fail,boosted_SR_pass,boosted_VR_fail,boosted_VR_pass,scale,process)                  
    j3_SR_fail_semiboosted,j3_SR_pass_semiboosted,j3_VR_fail_semiboosted,j3_VR_pass_semiboosted,mjj_vs_mjjj_SR_fail_semiboosted,mjj_vs_mjjj_SR_pass_semiboosted,mjj_vs_mjjj_VR_fail_semiboosted,mjj_vs_mjjj_VR_pass_semiboosted = plotsemiboosted(semiboosted_SR_fail_fatjet, semiboosted_SR_pass_fatjet,semiboosted_SR_fail_jet, semiboosted_SR_pass_jet,semiboosted_VR_fail_fatjet,semiboosted_VR_pass_fatjet,semiboosted_VR_fail_jet,semiboosted_VR_pass_jet,scale,process)
    with uproot.recreate(os.path.join(output, "Histograms_{0}-{1}".format(process, ofile))) as fout:
        fout[f"j3_SR_pass_boosted"] = j3_SR_pass_boosted
        fout[f"j3_VR_pass_boosted"] = j3_VR_pass_boosted
        fout[f"mjj_vs_mjjj_SR_pass_boosted"] = mjj_vs_mjjj_SR_pass_boosted
        fout[f"mjj_vs_mjjj_VR_pass_boosted"] = mjj_vs_mjjj_VR_pass_boosted
        fout[f"j3_SR_fail_boosted"] = j3_SR_fail_boosted
        fout[f"j3_VR_fail_boosted"] = j3_VR_fail_boosted
        fout[f"mjj_vs_mjjj_SR_fail_boosted"] = mjj_vs_mjjj_SR_fail_boosted
        fout[f"mjj_vs_mjjj_VR_fail_boosted"] = mjj_vs_mjjj_VR_fail_boosted
        fout[f"j3_SR_pass_semiboosted"] = j3_SR_pass_semiboosted
        fout[f"j3_VR_pass_semiboosted"] = j3_VR_pass_semiboosted
        fout[f"mjj_vs_mjjj_SR_pass_semiboosted"] = mjj_vs_mjjj_SR_pass_semiboosted
        fout[f"mjj_vs_mjjj_VR_pass_semiboosted"] = mjj_vs_mjjj_VR_pass_semiboosted
        fout[f"j3_SR_fail_semiboosted"] = j3_SR_fail_semiboosted
        fout[f"j3_VR_fail_semiboosted"] = j3_VR_fail_semiboosted
        fout[f"mjj_vs_mjjj_SR_fail_semiboosted"] = mjj_vs_mjjj_SR_fail_semiboosted
        fout[f"mjj_vs_mjjj_VR_fail_semiboosted"] = mjj_vs_mjjj_VR_fail_semiboosted
        fout[f"numberOfGenEventsHisto"] = numberOfGenEventsHisto
