import ROOT

# here it is best to use unnormalized MC histograms which can be obtained as in the following example
# python combine_histograms.py -i /users/ferencek/HHH/condor_jobs_data_background_signal_20231220_123208 -p XToYHTo6B_MX-2500_MY-800 --skip_norm

def makePlot(path, histo, label, fname, logy=False):
    # histogram file
    f = ROOT.TFile.Open(path, 'READ')

    # histograms
    h = f.Get(histo)

    c = ROOT.TCanvas("c", "",1000,800)
    c.cd()

    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextFont(42)
    l.SetTextSize(0.04)
    l.SetTextAlign(12)

    h.Draw('histtext')
    l.DrawLatex(0.5, 0.85, label)
    
    if logy:
        c.SetLogy()
    
    c.SaveAs(fname)


if __name__ == '__main__':
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


    makePlot('/STORE/HHH/Histograms/2017/20231220_123208/XToYHTo6B_MX-2500_MY-800_Histograms_unnormalized.root', 'cutFlowHisto_SR_boosted', "m_{X}=2500 GeV, m_{Y}=800 GeV", 'cutFlowHisto_signal_SR_boosted.png')
    makePlot('/STORE/HHH/Histograms/2017/20231220_123208/XToYHTo6B_MX-2500_MY-800_Histograms_unnormalized.root', 'cutFlowHisto_SR_semiboosted', "m_{X}=2500 GeV, m_{Y}=800 GeV", 'cutFlowHisto_signal_SR_semiboosted.png')
    makePlot('/STORE/HHH/Histograms/2017/20231220_123208/JetHT_Histograms.root', 'cutFlowHisto_VR_boosted', "Data, JetHT, 2017", 'cutFlowHisto_data_VR_boosted.png', logy=True)
    makePlot('/STORE/HHH/Histograms/2017/20231220_123208/JetHT_Histograms.root', 'cutFlowHisto_VR_semiboosted', "Data, JetHT, 2017", 'cutFlowHisto_data_VR_semiboosted.png', logy=True)
