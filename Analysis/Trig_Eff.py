import uproot
import ROOT as r
import json
import awkward as ak
import matplotlib.pyplot as plt
import hist
from hist import Hist
import numpy as np
import mplhep as hep
#from tdrStyle import setTDRStyle
#setTDRStyle()
def get2DTrigEff(hPass,hTot,outputFile,xTitle="",yTitle="",xLimits=[],yLimits=[],label=""):
    print(label)
    h1 = hPass.Clone()
    h1.SetDirectory(0)
    h2 = hTot.Clone()
    h2.SetDirectory(0)

    eff = r.TEfficiency(h1,h2)
    eff.SetTitle(";{0};{1}".format(xTitle,yTitle))
    c = r.TCanvas("a","a",1500,1500)
    c.cd()
    eff.Draw("COLZ")
    r.gPad.Update()

    legend = r.TLegend(0.18,0.8,0.45,1.0)
    legend.SetFillStyle(0)
    legend.SetLineWidth(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.04)
    legend.SetHeader(label)
    legend.Draw()
    r.gPad.Update()
    if(outputFile):
        c.SaveAs(outputFile)
    c.Close()
    return eff

def getTrigEff(hPass,hTot,outputFile="",xTitle="",yTitle="",color=0,xLimits=[],yLimits=[],printEffs=False):
    h1 = hPass.Clone()
    h1.SetDirectory(0)
    h2 = hTot.Clone()
    h2.SetDirectory(0)

    eff = r.TEfficiency(h1,h2)
    if(printEffs):
        print(xTitle)
        for i in range(1,h1.GetNbinsX()):
            print(h1.GetBinCenter(i),eff.GetEfficiency(i))
    eff.SetTitle(";{0};{1}".format(xTitle,yTitle))
    c = r.TCanvas("","",1500,1500)
    c.cd()
    if(color!=0):
        eff.SetLineColor(color)
    eff.SetLineWidth(3)
    eff.Draw("A")
    r.gPad.Update()
    g = eff.GetPaintedGraph()
    if(xLimits):
        g.GetXaxis().SetRangeUser(xLimits[0],xLimits[1])
    if(yLimits):
        g.GetYaxis().SetRangeUser(yLimits[0],yLimits[1])
    r.gPad.Update()
    if(outputFile):
        c.SaveAs(outputFile)
    return eff


data_rt = r.TFile.Open("/users/bchitrod/HHH_v1.0/H3PO/Analysis/Ref_HT250/fit/JetHT2017_Histograms.root")
dataj3_rt = data_rt.Get("j3_VR_fail_boosted")
dataj2_j3_rt = data_rt.Get("mjj_vs_mjjj_VR_fail_boosted")
datasbj3_rt = data_rt.Get("j3_VR_fail_semiboosted")
datasbj2_j3_rt = data_rt.Get("mjj_vs_mjjj_VR_fail_semiboosted")

data = r.TFile.Open("/users/bchitrod/HHH_v1.0/H3PO/Analysis/HT1050/fit/JetHT2017_Histograms.root")
dataj3_1050 = data.Get("j3_VR_fail_boosted")
dataj2_j3_1050 = data.Get("mjj_vs_mjjj_VR_fail_boosted")
datasbj3_1050 = data.Get("j3_VR_fail_semiboosted")
datasbj2_j3_1050 = data.Get("mjj_vs_mjjj_VR_fail_semiboosted")



get2DTrigEff(dataj2_j3_1050,dataj2_j3_rt,"results/Trigger_Efficiency_PFHT250/Data_PFHT1050_Boosted_VR_fail.pdf",xTitle="MJJJ",yTitle="MJJ",xLimits=[0,6000],yLimits=[0,4000],label="Data PFHT1050")
getTrigEff(dataj3_1050,dataj3_rt,outputFile="results/Trigger_Efficiency_PFHT250/Data_PFHT1050_J3_Boosted_VR_fail.pdf",xTitle="MJJJ",yTitle="Events",color=0,xLimits=[0,6000],yLimits=[0,1.2],printEffs=False)
get2DTrigEff(datasbj2_j3_1050,datasbj2_j3_rt,"results/Trigger_Efficiency_PFHT250/Data_PFHT1050_semiBoosted_VR_fail.pdf",xTitle="MJJJ",yTitle="MJJ",xLimits=[0,6000],yLimits=[0,4000],label="Data PFHT1050")
getTrigEff(datasbj3_1050,datasbj3_rt,outputFile="results/Trigger_Efficiency_PFHT250/Data_PFHT1050_J3_semiBoosted_VR_fail.pdf",xTitle="MJJJ",yTitle="Events",color=0,xLimits=[0,6000],yLimits=[0,1.2],printEffs=False)

