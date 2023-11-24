import ROOT

# here it is best to use unnormalized histograms which can be obtained as in the following example
# python combine_histograms.py -i /users/ferencek/HHH/condor_jobs_data_background_signal_20231019_162502 -p XToYHTo6B_MX-2500_MY-800 --skip_norm

# to run in the batch mode (to prevent canvases from popping up)
ROOT.gROOT.SetBatch()

# suppress the statistics box
ROOT.gStyle.SetOptStat(0)

# set nicer fonts
ROOT.gStyle.SetTitleFont(42, "")
ROOT.gStyle.SetTitleFont(42, "XYZ")
ROOT.gStyle.SetLabelFont(42, "XYZ")
ROOT.gStyle.SetTextFont(42)
ROOT.gStyle.SetStatFont(42)
ROOT.gROOT.ForceStyle()

    
# histogram file
f = ROOT.TFile.Open('XToYHTo6B_MX-2500_MY-800_Histograms.root', 'READ')

# histograms
h_b  = f.Get('cutFlowHisto_SR_boosted')
h_sb = f.Get('cutFlowHisto_SR_semiboosted')


c = ROOT.TCanvas("c", "",1000,800)
c.cd()

l = ROOT.TLatex()
l.SetNDC()
l.SetTextFont(42)
l.SetTextSize(0.04)
l.SetTextAlign(12)

h_b.Draw('histtext')
l.DrawLatex(0.5, 0.85, "m_{X}=2500 GeV, m_{Y}=800 GeV")
  
c.SaveAs('cutFlowHisto_SR_boosted.png')

h_sb.Draw('histtext')
l.DrawLatex(0.5, 0.85, "m_{X}=2500 GeV, m_{Y}=800 GeV")

c.SaveAs('cutFlowHisto_SR_semiboosted.png')
