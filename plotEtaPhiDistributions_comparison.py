import ROOT
import copy
import numpy as np


colors = [1, 2, 8]
styles = [1, 2, 3]

data = {
	"JetHT": "~/condor_jobs_2017_background_20240923_122419/fit/JetHT_Histograms.root",
	"TTbar": "~/condor_jobs_2017_background_20240923_122419/fit/TTbar_Histograms.root",
	"mass": "~/condor_jobs_2017_background_20240923_122419/fit/XToYHTo6B_MX-4000_MY-300_Histograms.root", 
}



def makePlot(histo, hmax, x_min, x_max, proj=False):

    histos = []

    for label in data:

        print("\nProcessing {0}".format(label))
        

        f = ROOT.TFile.Open(data[label])

        if proj:
            histos.append( copy.deepcopy( ( f.Get(histo).ProjectionY(), label ) ) )
        else:
            histos.append( copy.deepcopy( ( f.Get(histo), label ) ) )
        
        f.Close()

    c = ROOT.TCanvas("c_{}".format(histo), "",1000,900)
    c.cd()

    frame = ROOT.TH1F("frame",";{0}".format("#phi" if "Phi" in histo else "#eta"),1000,x_min,x_max)
    frame.SetMaximum(hmax)
    frame.SetStats(0)
    frame.Draw()

    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextFont(42)
    l.SetTextSize(0.04)
    l.SetTextAlign(12)
#    mX_label = "{0} GeV".format(mX)
#    l.DrawLatex(0.6, 0.85, "m_{X}=" + mX_label)
#    mY_label = "{0} GeV".format(mY)
#    l.DrawLatex(0.6, 0.8, "m_{Y}=" + mY_label)
    
    l.DrawLatex(0.15, 0.82, histo)
    
    legend = ROOT.TLegend(.6,.5,.8,.75)
    legend.SetTextFont(42)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.04)
    legend.SetHeader("Process", "l")
    
    n = 0
    for (h, label) in histos:
        h.SetLineColor(colors[n])
        h.SetLineStyle(styles[n])
        h.SetLineWidth(2)
        h.DrawNormalized('histsame')
        legend.AddEntry(h,"{0}".format(label),"l")
        n += 1

    legend.Draw()

    #c.SaveAs(fname)
    
    fname = "comparison_by_processes_{0}.pdf".format(histo)
    c.Print(fname, "pdf")

if __name__ == '__main__':
    # to run in the batch mode (to prevent canvases from popping up)
    ROOT.gROOT.SetBatch()
    
    # suppress the statistics box
    ROOT.gStyle.SetOptStat(0)

    # set plot style
    ROOT.gROOT.SetStyle("Plain")
    ROOT.gStyle.SetPalette(57)

    ROOT.gStyle.SetPadTickX(1)  # to get the tick marks on the opposite side of the frame
    ROOT.gStyle.SetPadTickY(1)  # to get the tick marks on the opposite side of the frame

    # tweak margins
    ROOT.gStyle.SetPadTopMargin(0.1)
    ROOT.gStyle.SetPadBottomMargin(0.1)
    ROOT.gStyle.SetPadLeftMargin(0.12)
    ROOT.gStyle.SetPadRightMargin(0.1)

    # tweak axis title offsets
    ROOT.gStyle.SetTitleOffset(1.5, "Y")
    ROOT.gStyle.SetTitleOffset(1.25, "Z")

    # set nicer fonts
    ROOT.gStyle.SetTitleFont(42, "")
    ROOT.gStyle.SetTitleFont(42, "XYZ")
    ROOT.gStyle.SetLabelFont(42, "XYZ")
    ROOT.gStyle.SetTextFont(42)
    ROOT.gStyle.SetStatFont(42)
    ROOT.gROOT.ForceStyle()

    makePlot('deltaEta_SR_pass_boosted', 0.04, -5, 5)
    makePlot('deltaPhi_SR_pass_boosted', 0.3, -np.pi, np.pi)


