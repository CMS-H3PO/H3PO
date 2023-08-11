import os
import uproot
import ROOT
import json
import awkward as ak
import matplotlib.pyplot as plt
import hist
from hist import Hist
from coffea.nanoevents import NanoEventsFactory, BaseSchema
import coffea.processor as processor
from coffea.processor import accumulate
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import numpy as np
import mplhep as hep
from ACR_Selection import *

def plotboosted(boostedSignal_0btag, boostedSignal_1btag,boostedCR_0btag,boostedCR_1btag,scale,process):

    trijet_mass_Signal0btag = (boostedSignal_0btag[:,0]+boostedSignal_0btag[:,1]+boostedSignal_0btag[:,2]).mass
    trijet_mass_Signal1btag = (boostedSignal_1btag[:,0]+boostedSignal_1btag[:,1]+boostedSignal_1btag[:,2]).mass

    trijet_mass_CR0btag = (boostedCR_0btag[:,0]+boostedCR_0btag[:,1]+boostedCR_0btag[:,2]).mass
    trijet_mass_CR1btag = (boostedCR_1btag[:,0]+boostedCR_1btag[:,1]+boostedCR_1btag[:,2]).mass

    j3_sig0btag_bin = hist.axis.Regular(label="Boosted Signal Trijet Mass with 0 btagged fatjet [GeV]", name="trijet_mass_sig0btag", bins=120, start=0, stop=6000)
    j3_sig0btag_hist = Hist(j3_sig0btag_bin)
    j3_sig0btag_hist.fill(trijet_mass_sig0btag=trijet_mass_Signal0btag)
    j3_sig0btag_hist *= scale

    j3_sig1btag_bin = hist.axis.Regular(label="Boosted Signal Trijet Mass with atleast 1 btagged fatjet [GeV]", name="trijet_mass_sig1btag", bins=120, start=0, stop=6000)
    j3_sig1btag_hist = Hist(j3_sig1btag_bin)
    j3_sig1btag_hist.fill(trijet_mass_sig1btag=trijet_mass_Signal1btag)
    j3_sig1btag_hist *= scale

    j3_CR0btag_bin = hist.axis.Regular(label="Boosted Validation Trijet Mass with 0 btagged fatjet [GeV]", name="trijet_mass_CR0btag", bins=120, start=0, stop=6000)
    j3_CR0btag_hist = Hist(j3_CR0btag_bin)
    j3_CR0btag_hist.fill(trijet_mass_CR0btag=trijet_mass_CR0btag)
    j3_CR0btag_hist *= scale

    j3_CR1btag_bin = hist.axis.Regular(label="Boosted Validation Trijet Mass with atleast 1 btagged fatjet [GeV]", name="trijet_mass_CR1btag", bins=120, start=0, stop=6000)
    j3_CR1btag_hist = Hist(j3_CR1btag_bin)
    j3_CR1btag_hist.fill(trijet_mass_CR1btag=trijet_mass_CR1btag)
    j3_CR1btag_hist *= scale

    dijet1_mass_Signal0btag = (boostedSignal_0btag[:,0]+boostedSignal_0btag[:,1]).mass
    dijet2_mass_Signal0btag = (boostedSignal_0btag[:,0]+boostedSignal_0btag[:,2]).mass
    dijet3_mass_Signal0btag = (boostedSignal_0btag[:,1]+boostedSignal_0btag[:,2]).mass
    dijet1_mass_Signal1btag = (boostedSignal_1btag[:,0]+boostedSignal_1btag[:,1]).mass
    dijet2_mass_Signal1btag = (boostedSignal_1btag[:,0]+boostedSignal_1btag[:,2]).mass
    dijet3_mass_Signal1btag = (boostedSignal_1btag[:,1]+boostedSignal_1btag[:,2]).mass

    dijet1_mass_CR0btag = (boostedCR_0btag[:,0]+boostedCR_0btag[:,1]).mass
    dijet2_mass_CR0btag = (boostedCR_0btag[:,0]+boostedCR_0btag[:,2]).mass
    dijet3_mass_CR0btag = (boostedCR_0btag[:,1]+boostedCR_0btag[:,2]).mass
    dijet1_mass_CR1btag = (boostedCR_1btag[:,0]+boostedCR_1btag[:,1]).mass
    dijet2_mass_CR1btag = (boostedCR_1btag[:,0]+boostedCR_1btag[:,2]).mass
    dijet3_mass_CR1btag = (boostedCR_1btag[:,1]+boostedCR_1btag[:,2]).mass

    j2_sig0btag_bin = hist.axis.Regular(label="Dijet Mass [GeV]", name="dijet_mass", bins=80, start=0, stop=4000)
    mjj_vs_mjjj_sig0btag = Hist(j3_sig0btag_bin, j2_sig0btag_bin)
    mjj_vs_mjjj_sig0btag.fill(dijet_mass=dijet1_mass_Signal0btag,trijet_mass_sig0btag=trijet_mass_Signal0btag)
    mjj_vs_mjjj_sig0btag.fill(dijet_mass=dijet2_mass_Signal0btag,trijet_mass_sig0btag=trijet_mass_Signal0btag)
    mjj_vs_mjjj_sig0btag.fill(dijet_mass=dijet3_mass_Signal0btag,trijet_mass_sig0btag=trijet_mass_Signal0btag)
    mjj_vs_mjjj_sig0btag *= scale

    j2_sig1btag_bin = hist.axis.Regular(label="Dijet Mass [GeV]", name="dijet_mass", bins=80, start=0, stop=4000)
    mjj_vs_mjjj_sig1btag = Hist(j3_sig1btag_bin, j2_sig1btag_bin)
    mjj_vs_mjjj_sig1btag.fill(dijet_mass=dijet1_mass_Signal1btag,trijet_mass_sig1btag=trijet_mass_Signal1btag)
    mjj_vs_mjjj_sig1btag.fill(dijet_mass=dijet2_mass_Signal1btag,trijet_mass_sig1btag=trijet_mass_Signal1btag)
    mjj_vs_mjjj_sig1btag.fill(dijet_mass=dijet3_mass_Signal1btag,trijet_mass_sig1btag=trijet_mass_Signal1btag)
    mjj_vs_mjjj_sig1btag *= scale

    j2_CR0btag_bin = hist.axis.Regular(label="Dijet Mass [GeV]", name="dijet_mass", bins=80, start=0, stop=4000)
    mjj_vs_mjjj_CR0btag = Hist(j3_CR0btag_bin, j2_CR0btag_bin)
    mjj_vs_mjjj_CR0btag.fill(dijet_mass=dijet1_mass_CR0btag,trijet_mass_CR0btag=trijet_mass_CR0btag)
    mjj_vs_mjjj_CR0btag.fill(dijet_mass=dijet2_mass_CR0btag,trijet_mass_CR0btag=trijet_mass_CR0btag)
    mjj_vs_mjjj_CR0btag.fill(dijet_mass=dijet3_mass_CR0btag,trijet_mass_CR0btag=trijet_mass_CR0btag)
    mjj_vs_mjjj_CR0btag *= scale

    j2_CR1btag_bin = hist.axis.Regular(label="Dijet Mass [GeV]", name="dijet_mass", bins=80, start=0, stop=4000)
    mjj_vs_mjjj_CR1btag = Hist(j3_CR1btag_bin, j2_CR1btag_bin)
    mjj_vs_mjjj_CR1btag.fill(dijet_mass=dijet1_mass_CR1btag,trijet_mass_CR1btag=trijet_mass_CR1btag)
    mjj_vs_mjjj_CR1btag.fill(dijet_mass=dijet2_mass_CR1btag,trijet_mass_CR1btag=trijet_mass_CR1btag)
    mjj_vs_mjjj_CR1btag.fill(dijet_mass=dijet3_mass_CR1btag,trijet_mass_CR1btag=trijet_mass_CR1btag)
    mjj_vs_mjjj_CR1btag *= scale

    return j3_sig0btag_hist,j3_sig1btag_hist,j3_CR0btag_hist,j3_CR1btag_hist,mjj_vs_mjjj_sig0btag,mjj_vs_mjjj_sig1btag,mjj_vs_mjjj_CR0btag,mjj_vs_mjjj_CR1btag

def plotsemiboosted(semiboostedSignalfj_0btag, semiboostedSignalfj_1btag,semiboostedSignalj_0btag, semiboostedSignalj_1btag,semiboostedCRfj_0btag,semiboostedCRfj_1btag,semiboostedCRj_0btag,semiboostedCRj_1btag,scale,process):

    tri_mass_Signal0btag = (semiboostedSignalfj_0btag[:,0]+semiboostedSignalfj_0btag[:,1]+semiboostedSignalj_0btag['i0']+semiboostedSignalj_0btag['i1']).mass
    tri_mass_Signal1btag = (semiboostedSignalfj_1btag[:,0]+semiboostedSignalfj_1btag[:,1]+semiboostedSignalj_1btag['i0']+semiboostedSignalj_1btag['i1']).mass

    tri_mass_CR0btag = (semiboostedCRfj_0btag[:,0]+semiboostedCRfj_0btag[:,1]+semiboostedCRj_0btag['i0']+semiboostedCRj_0btag['i1']).mass
    tri_mass_CR1btag = (semiboostedCRfj_1btag[:,0]+semiboostedCRfj_1btag[:,1]+semiboostedCRj_1btag['i0']+semiboostedCRj_1btag['i1']).mass

    trijet_mass_Signal0btag = []
    trijet_mass_Signal1btag = []
    trijet_mass_CR0btag = []
    trijet_mass_CR1btag = []
    for t in tri_mass_Signal0btag:
        for i in t:
            trijet_mass_Signal0btag.append(i)
    for t in tri_mass_Signal1btag:
        for i in t:
            trijet_mass_Signal1btag.append(i)
    for t in tri_mass_CR0btag:
        for i in t:
            trijet_mass_CR0btag.append(i)
    for t in tri_mass_CR1btag:
        for i in t:
            trijet_mass_CR1btag.append(i)

    j3_sig0btag_bin = hist.axis.Regular(label="semiBoosted Signal Trijet Mass with 0 btagged fatjet [GeV]", name="trijet_mass_sig0btag", bins=120, start=0, stop=6000)
    j3_sig0btag_hist = Hist(j3_sig0btag_bin)
    j3_sig0btag_hist.fill(trijet_mass_sig0btag=trijet_mass_Signal0btag)
    j3_sig0btag_hist *= scale

    j3_sig1btag_bin = hist.axis.Regular(label="semiBoosted Signal Trijet Mass with atleast 1 btagged fatjet [GeV]", name="trijet_mass_sig1btag", bins=120, start=0, stop=6000)
    j3_sig1btag_hist = Hist(j3_sig1btag_bin)
    j3_sig1btag_hist.fill(trijet_mass_sig1btag=trijet_mass_Signal1btag)
    j3_sig1btag_hist *= scale

    j3_CR0btag_bin = hist.axis.Regular(label="semiBoosted Validation Trijet Mass with 0 btagged fatjet [GeV]", name="trijet_mass_CR0btag", bins=120, start=0, stop=6000)
    j3_CR0btag_hist = Hist(j3_CR0btag_bin)
    j3_CR0btag_hist.fill(trijet_mass_CR0btag=trijet_mass_CR0btag)
    j3_CR0btag_hist *= scale

    j3_CR1btag_bin = hist.axis.Regular(label="semiBoosted Validation Trijet Mass with atleast 1 btagged fatjet [GeV]", name="trijet_mass_CR1btag", bins=120, start=0, stop=6000)
    j3_CR1btag_hist = Hist(j3_CR1btag_bin)
    j3_CR1btag_hist.fill(trijet_mass_CR1btag=trijet_mass_CR1btag)
    j3_CR1btag_hist *= scale

    dijet1_mass_Signal0btag = (semiboostedSignalfj_0btag[:,0]+semiboostedSignalfj_0btag[:,1]).mass
    di2_mass_Signal0btag = (semiboostedSignalfj_0btag[:,0]+semiboostedSignalj_0btag['i0']+semiboostedSignalj_0btag['i1']).mass
    di3_mass_Signal0btag = (semiboostedSignalfj_0btag[:,1]+semiboostedSignalj_0btag['i0']+semiboostedSignalj_0btag['i1']).mass
    dijet1_mass_Signal1btag = (semiboostedSignalfj_1btag[:,0]+semiboostedSignalfj_1btag[:,1]).mass
    di2_mass_Signal1btag = (semiboostedSignalfj_1btag[:,0]+semiboostedSignalj_1btag['i0']+semiboostedSignalj_1btag['i1']).mass
    di3_mass_Signal1btag = (semiboostedSignalfj_1btag[:,1]+semiboostedSignalj_1btag['i0']+semiboostedSignalj_1btag['i1']).mass

    dijet1_mass_CR0btag = (semiboostedCRfj_0btag[:,0]+semiboostedCRfj_0btag[:,1]).mass
    di2_mass_CR0btag = (semiboostedCRfj_0btag[:,0]+semiboostedCRj_0btag['i0']+semiboostedCRj_0btag['i1']).mass
    di3_mass_CR0btag = (semiboostedCRfj_0btag[:,1]+semiboostedCRj_0btag['i0']+semiboostedCRj_0btag['i1']).mass
    dijet1_mass_CR1btag = (semiboostedCRfj_1btag[:,0]+semiboostedCRfj_1btag[:,1]).mass
    di2_mass_CR1btag = (semiboostedCRfj_1btag[:,0]+semiboostedCRj_1btag['i0']+semiboostedCRj_1btag['i1']).mass
    di3_mass_CR1btag = (semiboostedCRfj_1btag[:,1]+semiboostedCRj_1btag['i0']+semiboostedCRj_1btag['i1']).mass

    dijet2_mass_Signal0btag = []
    dijet3_mass_Signal0btag = []
    dijet2_mass_Signal1btag = []
    dijet3_mass_Signal1btag = []
    dijet2_mass_CR0btag = []
    dijet3_mass_CR0btag = []
    dijet2_mass_CR1btag = []
    dijet3_mass_CR1btag = []

    for d in di2_mass_Signal0btag:
        for i in d:
            dijet2_mass_Signal0btag.append(i)
    for d in di3_mass_Signal0btag:
        for i in d:
            dijet3_mass_Signal0btag.append(i)
    for d in di2_mass_Signal1btag:
        for i in d:
            dijet2_mass_Signal1btag.append(i)
    for d in di3_mass_Signal1btag:
        for i in d:
            dijet3_mass_Signal1btag.append(i)
    for d in di2_mass_CR0btag:
        for i in d:
            dijet2_mass_CR0btag.append(i)
    for d in di3_mass_CR0btag:
        for i in d:
            dijet3_mass_CR0btag.append(i)
    for d in di2_mass_CR1btag:
        for i in d:
            dijet2_mass_CR1btag.append(i)
    for d in di3_mass_CR1btag:
        for i in d:
            dijet3_mass_CR1btag.append(i)

    j2_sig0btag_bin = hist.axis.Regular(label="Dijet Mass [GeV]", name="dijet_mass", bins=80, start=0, stop=4000)
    mjj_vs_mjjj_sig0btag = Hist(j3_sig0btag_bin, j2_sig0btag_bin)
    mjj_vs_mjjj_sig0btag.fill(dijet_mass=dijet1_mass_Signal0btag,trijet_mass_sig0btag=trijet_mass_Signal0btag)
    mjj_vs_mjjj_sig0btag.fill(dijet_mass=dijet2_mass_Signal0btag,trijet_mass_sig0btag=trijet_mass_Signal0btag)
    mjj_vs_mjjj_sig0btag.fill(dijet_mass=dijet3_mass_Signal0btag,trijet_mass_sig0btag=trijet_mass_Signal0btag)
    mjj_vs_mjjj_sig0btag *= scale

    j2_sig1btag_bin = hist.axis.Regular(label="Dijet Mass [GeV]", name="dijet_mass", bins=80, start=0, stop=4000)
    mjj_vs_mjjj_sig1btag = Hist(j3_sig1btag_bin, j2_sig1btag_bin)
    mjj_vs_mjjj_sig1btag.fill(dijet_mass=dijet1_mass_Signal1btag,trijet_mass_sig1btag=trijet_mass_Signal1btag)
    mjj_vs_mjjj_sig1btag.fill(dijet_mass=dijet2_mass_Signal1btag,trijet_mass_sig1btag=trijet_mass_Signal1btag)
    mjj_vs_mjjj_sig1btag.fill(dijet_mass=dijet3_mass_Signal1btag,trijet_mass_sig1btag=trijet_mass_Signal1btag)
    mjj_vs_mjjj_sig1btag *= scale

    j2_CR0btag_bin = hist.axis.Regular(label="Dijet Mass [GeV]", name="dijet_mass", bins=80, start=0, stop=4000)
    mjj_vs_mjjj_CR0btag = Hist(j3_CR0btag_bin, j2_CR0btag_bin)
    mjj_vs_mjjj_CR0btag.fill(dijet_mass=dijet1_mass_CR0btag,trijet_mass_CR0btag=trijet_mass_CR0btag)
    mjj_vs_mjjj_CR0btag.fill(dijet_mass=dijet2_mass_CR0btag,trijet_mass_CR0btag=trijet_mass_CR0btag)
    mjj_vs_mjjj_CR0btag.fill(dijet_mass=dijet3_mass_CR0btag,trijet_mass_CR0btag=trijet_mass_CR0btag)
    mjj_vs_mjjj_CR0btag *= scale

    j2_CR1btag_bin = hist.axis.Regular(label="Dijet Mass [GeV]", name="dijet_mass", bins=80, start=0, stop=4000)
    mjj_vs_mjjj_CR1btag = Hist(j3_CR1btag_bin, j2_CR1btag_bin)
    mjj_vs_mjjj_CR1btag.fill(dijet_mass=dijet1_mass_CR1btag,trijet_mass_CR1btag=trijet_mass_CR1btag)
    mjj_vs_mjjj_CR1btag.fill(dijet_mass=dijet2_mass_CR1btag,trijet_mass_CR1btag=trijet_mass_CR1btag)
    mjj_vs_mjjj_CR1btag.fill(dijet_mass=dijet3_mass_CR1btag,trijet_mass_CR1btag=trijet_mass_CR1btag)
    mjj_vs_mjjj_CR1btag *= scale

    return j3_sig0btag_hist,j3_sig1btag_hist,j3_CR0btag_hist,j3_CR1btag_hist,mjj_vs_mjjj_sig0btag,mjj_vs_mjjj_sig1btag,mjj_vs_mjjj_CR0btag,mjj_vs_mjjj_CR1btag


if __name__ == "__main__":
    from argparse import ArgumentParser
    
    parser = ArgumentParser(description="Do -h to see usage")
    parser.add_argument('-s', '--sample', help='Sample name', default="QCD2000")
    parser.add_argument('-i', '--input', help='Input file')
    parser.add_argument('-o', '--output', help='Output directory')
    args = parser.parse_args()
    
    process = args.sample
    input = args.input
    output = args.output
    year = "2017"
    oFile = process
    print(process)
    boostedSignal_0btag, boostedSignal_1btag = Signal_boosted(input,process,eventsToRead=None)
    boostedCR_0btag,boostedCR_1btag = Validation_boosted(input,process,eventsToRead=None)
    semiboostedSignalfj_0btag, semiboostedSignalfj_1btag,semiboostedSignalj_0btag, semiboostedSignalj_1btag = Signal_semiboosted(input,process,eventsToRead=None)
    semiboostedCRfj_0btag,semiboostedCRfj_1btag,semiboostedCRj_0btag,semiboostedCRj_1btag = Validation_semiboosted(input,process,eventsToRead=None)
    if ((process != "JetHT2017B")&(process != "JetHT2017C")&(process != "JetHT2017D")&(process != "JetHT2017E")&(process != "JetHT2017F")):
        scale = normalizeProcess(process,year)
    if ((process == "JetHT2017B")|(process == "JetHT2017C")|(process == "JetHT2017D")|(process == "JetHT2017E")|(process == "JetHT2017F")):
        scale = 1
    j3_sig0btag_hist,j3_sig1btag_hist,j3_CR0btag_hist,j3_CR1btag_hist,mjj_vs_mjjj_sig0btag,mjj_vs_mjjj_sig1btag,mjj_vs_mjjj_CR0btag,mjj_vs_mjjj_CR1btag = plotboosted(boostedSignal_0btag,boostedSignal_1btag,boostedCR_0btag,boostedCR_1btag,scale,process)
    j3_sig0btag_sb_hist,j3_sig1btag_sb_hist,j3_CR0btag_sb_hist,j3_CR1btag_sb_hist,mjj_vs_mjjj_sig0btag_sb,mjj_vs_mjjj_sig1btag_sb,mjj_vs_mjjj_CR0btag_sb,mjj_vs_mjjj_CR1btag_sb = plotsemiboosted(semiboostedSignalfj_0btag, semiboostedSignalfj_1btag,semiboostedSignalj_0btag, semiboostedSignalj_1btag,semiboostedCRfj_0btag,semiboostedCRfj_1btag,semiboostedCRj_0btag,semiboostedCRj_1btag,scale,process)
    with uproot.recreate(os.path.join(output, "{0}_Boosted_pass_50.root".format(process))) as fout:
        fout[f"j3_sig_hist"] = j3_sig1btag_hist
        fout[f"j3_CR_hist"] = j3_CR1btag_hist
        fout[f"mjj_vs_mjjj_sig"] = mjj_vs_mjjj_sig1btag
        fout[f"mjj_vs_mjjj_CR"] = mjj_vs_mjjj_CR1btag
    with uproot.recreate(os.path.join(output, "{0}_Boosted_fail_50.root".format(process))) as fout:
        fout[f"j3_sig_hist"] = j3_sig0btag_hist
        fout[f"j3_CR_hist"] = j3_CR0btag_hist
        fout[f"mjj_vs_mjjj_sig"] = mjj_vs_mjjj_sig0btag
        fout[f"mjj_vs_mjjj_CR"] =mjj_vs_mjjj_CR0btag
    with uproot.recreate(os.path.join(output, "{0}_semiBoosted_pass_50.root".format(process))) as fout:
        fout[f"j3_sig_sb_hist"] = j3_sig1btag_sb_hist
        fout[f"j3_CR_sb_hist"] = j3_CR1btag_sb_hist
        fout[f"mjj_vs_mjjj_sig_sb"] = mjj_vs_mjjj_sig1btag_sb
        fout[f"mjj_vs_mjjj_CR_sb"] = mjj_vs_mjjj_CR1btag_sb
    with uproot.recreate(os.path.join(output, "{0}_semiBoosted_fail_50.root".format(process))) as fout:
        fout[f"j3_sig_sb_hist"] = j3_sig0btag_sb_hist
        fout[f"j3_CR_sb_hist"] = j3_CR0btag_sb_hist
        fout[f"mjj_vs_mjjj_sig_sb"] = mjj_vs_mjjj_sig0btag_sb
        fout[f"mjj_vs_mjjj_CR_sb"] =mjj_vs_mjjj_CR0btag_sb


