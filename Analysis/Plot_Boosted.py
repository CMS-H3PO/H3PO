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


mjjj_sig0btag = ROOT.THStack("mjjj_sig0btag","MJJJ Boosted Signal Region 0 btag")
c1 = ROOT.TCanvas('c1', 'c1')

fin1 = ROOT.TFile.Open("./rootfiles/semiBoosted_TTbar.root")
TTbarj3_sig0btag = fin1.Get("j3_sig0btag_sb_hist")
TTbarj3_sig0btag.SetFillColor(806)
TTbarj3_sig0btag.Sumw2()
mjjj_sig0btag.Add(TTbarj3_sig0btag)

fin2 = ROOT.TFile.Open("./rootfiles/Boosted_QCD.root")
QCDj3_sig0btag = fin2.Get("j3_sig0btag_hist")    
QCDj3_sig0btag.Sumw2()
QCDj3_sig0btag.SetFillColor(856)
mjjj_sig0btag.Add(QCDj3_sig0btag)

sig = ROOT.TFile.Open("./rootfiles/Boosted_Signal.root")
signal_sig0btag = sig.Get("j3_sig0btag_hist")
signal_sig0btag.SetLineColor(2)

data = ROOT.TFile.Open("./rootfiles/Boosted_Data.root")
data_sig0btag = data.Get("j3_sig0btag_hist")
data_sig0btag.SetMarkerStyle(20)

mjjj_sig0btag.Draw("hist")

signal_sig0btag.Draw("HIST L SAME")
data_sig0btag.Draw('sameAEPZ')

legend = ROOT.TLegend(0.65,0.75,0.9,0.9)
legend.SetBorderSize(1)
legend.SetFillColor(0)
legend.AddEntry(QCDj3_sig0btag, "QCD")
legend.AddEntry(TTbarj3_sig0btag, "TTbar")
legend.AddEntry(signal_sig0btag, "Signal", "l")
legend.Draw()
mjjj_sig0btag.GetYaxis().SetTitle("Event Count")
mjjj_sig0btag.GetYaxis().SetTitleOffset(1.2)
mjjj_sig0btag.GetXaxis().SetTitle("MJJJ")
c1.Update()
c1.SaveAs("MJJJ_Boosted_Signal0btag.png")

mjjj_sig1btag = ROOT.THStack("mjjj_sig1btag","MJJJ Boosted Signal Region 1 btag")
c2 = ROOT.TCanvas('c2', 'c2')

TTbarj3_sig1btag = fin1.Get("j3_sig1btag_sb_hist")
TTbarj3_sig1btag.SetFillColor(806)
TTbarj3_sig1btag.Sumw2()
mjjj_sig1btag.Add(TTbarj3_sig1btag)

QCDj3_sig1btag = fin2.Get("j3_sig1btag_hist")
QCDj3_sig1btag.Sumw2()
QCDj3_sig1btag.SetFillColor(856)
mjjj_sig1btag.Add(QCDj3_sig1btag)

signal_sig1btag = sig.Get("j3_sig1btag_hist")
signal_sig1btag.SetLineColor(2)

data_sig1btag = data.Get("j3_sig1btag_hist")
data_sig1btag.SetMarkerStyle(20)

mjjj_sig1btag.SetMaximum(350)
mjjj_sig1btag.Draw("hist")

data_sig1btag.Draw('sameAEPZ')

signal_sig1btag.Draw("HIST L SAME")
legend = ROOT.TLegend(0.65,0.75,0.9,0.9)
legend.SetBorderSize(1)
legend.SetFillColor(0)
legend.AddEntry(QCDj3_sig1btag, "QCD")
legend.AddEntry(TTbarj3_sig1btag, "TTbar")
legend.AddEntry(signal_sig1btag, "Signal", "l")
legend.Draw()
mjjj_sig1btag.GetYaxis().SetTitle("Event Count")
mjjj_sig1btag.GetYaxis().SetTitleOffset(1.2)
mjjj_sig1btag.GetXaxis().SetTitle("MJJJ")
c2.Update()
c2.SaveAs("MJJJ_Boosted_Signal1btag.png")


mjjj_CR0btag = ROOT.THStack("mjjj_CR0btag","MJJJ Boosted Control Region 0 btag")
c1 = ROOT.TCanvas('c1', 'c1')

TTbarj3_CR0btag = fin1.Get("j3_CR0btag_sb_hist")
TTbarj3_CR0btag.SetFillColor(806)
TTbarj3_CR0btag.Sumw2()
mjjj_CR0btag.Add(TTbarj3_CR0btag)

QCDj3_CR0btag = fin2.Get("j3_CR0btag_hist")
QCDj3_CR0btag.Sumw2()
QCDj3_CR0btag.SetFillColor(856)
mjjj_CR0btag.Add(QCDj3_CR0btag)

Signal_CR0btag = sig.Get("j3_CR0btag_hist")
Signal_CR0btag.SetLineColor(2)

data_CR0btag = data.Get("j3_CR0btag_hist")
data_CR0btag.SetMarkerStyle(20)

mjjj_CR0btag.SetMaximum(3000)
mjjj_CR0btag.Draw("hist")
data_CR0btag.Draw('sameAEPZ')
Signal_CR0btag.Draw("HIST L SAME")
legend = ROOT.TLegend(0.65,0.75,0.9,0.9)
legend.SetBorderSize(1)
legend.SetFillColor(0)
legend.AddEntry(QCDj3_CR0btag, "QCD")
legend.AddEntry(TTbarj3_CR0btag, "TTbar")
legend.AddEntry(Signal_CR0btag, "Signal", "l")
legend.AddEntry(data_CR0btag, "Data")
legend.Draw()
mjjj_CR0btag.GetYaxis().SetTitle("Event Count")
mjjj_CR0btag.GetYaxis().SetTitleOffset(1.2)
mjjj_CR0btag.GetXaxis().SetTitle("MJJJ")

c1.SaveAs("MJJJ_Boosted_CR0btag.png")

mjjj_CR1btag = ROOT.THStack("mjjj_CR1btag","MJJJ Boosted Control Region 1 btag")
c1 = ROOT.TCanvas('c1', 'c1')

TTbarj3_CR1btag = fin1.Get("j3_CR1btag_sb_hist")
TTbarj3_CR1btag.SetFillColor(806)
TTbarj3_CR1btag.Sumw2()
mjjj_CR1btag.Add(TTbarj3_CR1btag)

QCDj3_CR1btag = fin2.Get("j3_CR1btag_hist")
QCDj3_CR1btag.Sumw2()
QCDj3_CR1btag.SetFillColor(856)
mjjj_CR1btag.Add(QCDj3_CR1btag)

Signal_CR1btag = sig.Get("j3_CR1btag_hist")
Signal_CR1btag.SetLineColor(2)

data_CR1btag = data.Get("j3_CR1btag_hist")
data_CR1btag.SetMarkerStyle(20)

mjjj_CR1btag.SetMaximum(3000)
mjjj_CR1btag.Draw("hist")
data_CR1btag.Draw('sameAEPZ')
Signal_CR1btag.Draw("HIST L SAME")
legend = ROOT.TLegend(0.65,0.75,0.9,0.9)
legend.SetBorderSize(1)
legend.SetFillColor(0)
legend.AddEntry(QCDj3_CR1btag, "QCD")
legend.AddEntry(TTbarj3_CR1btag, "TTbar")
legend.AddEntry(Signal_CR1btag, "Signal", "l")
legend.AddEntry(data_CR1btag, "Data")
legend.Draw()
mjjj_CR1btag.GetYaxis().SetTitle("Event Count")
mjjj_CR1btag.GetYaxis().SetTitleOffset(1.2)
mjjj_CR1btag.GetXaxis().SetTitle("MJJJ")

c1.SaveAs("MJJJ_Boosted_CR1btag.png")
