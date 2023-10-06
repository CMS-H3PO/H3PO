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

    for i in range(0,120):
        for j in range(0,80):
            if(h1.GetBinContent(i,j)>h2.GetBinContent(i,j)):
                print("pass ", h1.GetBinContent(i,j)," total ",h2.GetBinContent(i,j))
                xvalue = h1.GetBinContent(i,j)
                h1.SetBinContent(i,j,round(xvalue,10))
                h2.SetBinContent(i,j,round(xvalue,10))
                print(h1.GetBinContent(i,j))
                print(i,j)
                
    print("pass = ",h1.GetBinContent(69,55))
    print("total = ",h2.GetBinContent(69,55))
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
    for i in range(0,120):
        if(h1.GetBinContent(i)>h2.GetBinContent(i)):
            print("pass ", h1.GetBinContent(i)," total ",h2.GetBinContent(i))
            xvalue = h1.GetBinContent(i)
            h1.SetBinContent(i,round(xvalue,10))
            h2.SetBinContent(i,round(xvalue,10))
            print(h1.GetBinContent(i))
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


bkg_rt = r.TFile.Open("/users/bchitrod/HHH_v1.0/H3PO/Analysis/Ref_HT250_unweighted/fit/bkg.root")

bkgj3_rt = bkg_rt.Get("j3_VR_fail_boosted")
bkgj2_j3_rt = bkg_rt.Get("mjj_vs_mjjj_VR_fail_boosted")
bkgsbj3_rt = bkg_rt.Get("j3_VR_fail_semiboosted")
bkgsbj2_j3_rt = bkg_rt.Get("mjj_vs_mjjj_VR_fail_semiboosted")

bkg = r.TFile.Open("/users/bchitrod/HHH_v1.0/H3PO/Analysis/HT1050_unweighted/fit/bkg.root")
bkgj3_1050 = bkg.Get("j3_VR_fail_boosted")
bkgj2_j3_1050 = bkg.Get("mjj_vs_mjjj_VR_fail_boosted")
bkgsbj3_1050 = bkg.Get("j3_VR_fail_semiboosted")
bkgsbj2_j3_1050 = bkg.Get("mjj_vs_mjjj_VR_fail_semiboosted")

data_rt = r.TFile.Open("/users/bchitrod/HHH_v1.0/H3PO/Analysis/condor_jobs_20230926_105609/fit/JetHT2017_Histograms.root")
dataj3_rt = data_rt.Get("j3_VR_fail_boosted")
dataj2_j3_rt = data_rt.Get("mjj_vs_mjjj_VR_fail_boosted")
datasbj3_rt = data_rt.Get("j3_VR_fail_semiboosted")
datasbj2_j3_rt = data_rt.Get("mjj_vs_mjjj_VR_fail_semiboosted")

data = r.TFile.Open("/users/bchitrod/HHH_v1.0/H3PO/Analysis/Data_HT1050/fit/JetHT2017_Histograms.root")
dataj3_1050 = data.Get("j3_VR_fail_boosted")
dataj2_j3_1050 = data.Get("mjj_vs_mjjj_VR_fail_boosted")
datasbj3_1050 = data.Get("j3_VR_fail_semiboosted")
datasbj2_j3_1050 = data.Get("mjj_vs_mjjj_VR_fail_semiboosted")



get2DTrigEff(dataj2_j3_1050,dataj2_j3_rt,"results/Trigger_Efficiency/Data_PFHT1050_Boosted_VR_fail.pdf",xTitle="MJJJ",yTitle="MJJ",xLimits=[0,6000],yLimits=[0,4000],label="Data PFHT1050")
#get2DTrigEff(dataj2_j3_780,dataj2_j3_rt,"results/Trigger_Efficiency/Data_PFHT780_Boosted_VR_fail.pdf",xTitle="MJJJ",yTitle="MJJ",xLimits=[0,6000],yLimits=[0,4000],label="Data PFHT780")
get2DTrigEff(bkgj2_j3_1050,bkgj2_j3_rt,"results/Trigger_Efficiency/Bkg_PFHT1050_Boosted_VR_fail.png",xTitle="MJJJ",yTitle="MJJ",xLimits=[0,6000],yLimits=[0,4000],label="Bkg PFHT1050")
#get2DTrigEff(bkgj2_j3_780,bkgj2_j3_rt,"results/Trigger_Efficiency/Bkg_PFHT780_Boosted_VR_fail.pdf",xTitle="MJJJ",yTitle="MJJ",xLimits=[0,6000],yLimits=[0,4000],label="Bkg PFHT780")
getTrigEff(dataj3_1050,dataj3_rt,outputFile="results/Trigger_Efficiency/Data_PFHT1050_J3_Boosted_VR_fail.pdf",xTitle="MJJJ",yTitle="Events",color=0,xLimits=[0,6000],yLimits=[0,1.2],printEffs=False)
#getTrigEff(dataj3_780,dataj3_rt,outputFile="results/Trigger_Efficiency/Data_PFHT780_J3_Boosted_VR_fail.pdf",xTitle="MJJJ",yTitle="Events",color=0,xLimits=[0,6000],yLimits=[0,1.2],printEffs=False)
getTrigEff(bkgj3_1050,bkgj3_rt,outputFile="results/Trigger_Efficiency/Bkg_PFHT1050_J3_Boosted_VR_fail.png",xTitle="MJJJ",yTitle="Events",color=0,xLimits=[0,6000],yLimits=[0,1.2],printEffs=False)
#getTrigEff(bkgj3_780,bkgj3_rt,outputFile="results/Trigger_Efficiency/Bkg_PFHT780_J3_Boosted_VR_fail.pdf",xTitle="MJJJ",yTitle="Events",color=0,xLimits=[0,6000],yLimits=[0,1.2],printEffs=False)

get2DTrigEff(datasbj2_j3_1050,datasbj2_j3_rt,"results/Trigger_Efficiency/Data_PFHT1050_semiBoosted_VR_fail.pdf",xTitle="MJJJ",yTitle="MJJ",xLimits=[0,6000],yLimits=[0,4000],label="Data PFHT1050")
#get2DTrigEff(datasbj2_j3_780,datasbj2_j3_rt,"results/Trigger_Efficiency/Data_PFHT780_semiBoosted_VR_fail.pdf",xTitle="MJJJ",yTitle="MJJ",xLimits=[0,6000],yLimits=[0,4000],label="Data PFHT780")
get2DTrigEff(bkgsbj2_j3_1050,bkgsbj2_j3_rt,"results/Trigger_Efficiency/Bkg_PFHT1050_semiBoosted_VR_fail.png",xTitle="MJJJ",yTitle="MJJ",xLimits=[0,6000],yLimits=[0,4000],label="Bkg PFHT1050")
#get2DTrigEff(bkgsbj2_j3_780,bkgsbj2_j3_rt,"results/Trigger_Efficiency/Bkg_PFHT780_semiBoosted_VR_fail.pdf",xTitle="MJJJ",yTitle="MJJ",xLimits=[0,6000],yLimits=[0,4000],label="Bkg PFHT780")
getTrigEff(datasbj3_1050,datasbj3_rt,outputFile="results/Trigger_Efficiency/Data_PFHT1050_J3_semiBoosted_VR_fail.pdf",xTitle="MJJJ",yTitle="Events",color=0,xLimits=[0,6000],yLimits=[0,1.2],printEffs=False)
#getTrigEff(datasbj3_780,datasbj3_rt,outputFile="results/Trigger_Efficiency/Data_PFHT780_J3_semiBoosted_VR_fail.pdf",xTitle="MJJJ",yTitle="Events",color=0,xLimits=[0,6000],yLimits=[0,1.2],printEffs=False)
getTrigEff(bkgsbj3_1050,bkgsbj3_rt,outputFile="results/Trigger_Efficiency/Bkg_PFHT1050_J3_semiBoosted_VR_fail.png",xTitle="MJJJ",yTitle="Events",color=0,xLimits=[0,6000],yLimits=[0,1.2],printEffs=False)
##getTrigEff(bkgsbj3_780,bkgsbj3_rt,outputFile="results/Trigger_Efficiency/Bkg_PFHT780_J3_semiBoosted_VR_fail.pdf",xTitle="MJJJ",yTitle="Events",color=0,xLimits=[0,6000],yLimits=[0,1.2],printEffs=False)
