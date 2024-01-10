import ROOT
import copy


mass_points = [
  (2500, 600), (2500, 800), (2500, 1200), (2500, 2000)
]

colors = [1, 2, 8, 4, 6, 7, 9]
styles = [1, 2, 3, 4, 5, 6, 7]

# this one is broken for plotting mjj, no idea why exactly
#def makePlot(path, histo, fname, hmax, x_min, x_max, proj=False):

    #c = ROOT.TCanvas("c", "",1000,900)
    #c.cd()

    #frame = ROOT.TH1F()

    #legend = ROOT.TLegend(.6,.5,.8,.75)
    #legend.SetTextFont(42)
    #legend.SetBorderSize(0)
    #legend.SetFillColor(0)
    #legend.SetFillStyle(0)
    #legend.SetTextSize(0.04)
    #legend.SetHeader("m_{Y} [GeV]", "l")
    
    #histos = []

    #n = 0
    #for (mX, mY) in mass_points:
        #sample = 'XToYHTo6B_MX-{0}_MY-{1}'.format(mX, mY)

        #print("\nProcessing {0}...".format(sample))
        
        #file_path = '{0}/{1}_Histograms.root'.format(path, sample)

        #f = ROOT.TFile.Open(file_path)

        #if proj:
              #h = copy.deepcopy(f.Get(histo).ProjectionY())
        #else:
              #h = copy.deepcopy(f.Get(histo))
        
        #if (n==0):
            #frame = copy.deepcopy(ROOT.TH1F("frame",";{0} [GeV]".format("m_{jjj}" if "j3" in histo else "m_{jj}"),1000,x_min,x_max))
            #frame.SetMaximum(hmax)
            #frame.SetStats(0)
            #frame.Draw()

        #h.SetLineColor(colors[n])
        #h.SetLineStyle(styles[n])
        #h.SetLineWidth(2)
        #legend.AddEntry(h,"{0}".format(mY),"l")
        #h.DrawNormalized('histsame')

        #histos.append(h)

        #n += 1
      
    #legend.Draw()

    #l = ROOT.TLatex()
    #l.SetNDC()
    #l.SetTextFont(42)
    #l.SetTextSize(0.04)
    #l.SetTextAlign(12)
    #l.DrawLatex(0.6, 0.83, "m_{X}=2500 GeV")

    #c.SaveAs(fname)

# version that works
def makePlot(path, histo, fname, hmax, x_min, x_max, proj=False):

    histos = []

    for (mX, mY) in mass_points:
        sample = 'XToYHTo6B_MX-{0}_MY-{1}'.format(mX, mY)

        print("\nProcessing {0}...".format(sample))
        
        file_path = '{0}/{1}_Histograms.root'.format(path, sample)

        f = ROOT.TFile.Open(file_path)

        if proj:
            histos.append((copy.deepcopy(f.Get(histo).ProjectionY()), mY))
        else:
            histos.append((copy.deepcopy(f.Get(histo)), mY))
        
        f.Close()

    c = ROOT.TCanvas("c_{}".format(histo), "",1000,900)
    c.cd()

    frame = ROOT.TH1F("frame",";{0} [GeV]".format("m_{jjj}" if "j3" in histo else "m_{jj}"),1000,x_min,x_max)
    frame.SetMaximum(hmax)
    frame.SetStats(0)
    frame.Draw()

    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextFont(42)
    l.SetTextSize(0.04)
    l.SetTextAlign(12)
    l.DrawLatex(0.6, 0.83, "m_{X}=2500 GeV")
    
    legend = ROOT.TLegend(.6,.5,.8,.75)
    legend.SetTextFont(42)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.04)
    legend.SetHeader("m_{Y} [GeV]", "l")
    
    n = 0
    for (h, mY) in histos:
        h.SetLineColor(colors[n])
        h.SetLineStyle(styles[n])
        h.SetLineWidth(2)
        h.DrawNormalized('histsame')
        legend.AddEntry(h,"{0}".format(mY),"l")
        n += 1

    legend.Draw()

    c.SaveAs(fname)


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
    
    makePlot('/STORE/HHH/Histograms/2017/20231220_123208/', 'j3_SR_pass_boosted_nominal', 'j3_SR_pass_boosted.png', 0.18, 0, 5500)
    makePlot('/STORE/HHH/Histograms/2017/20231220_123208/', 'j3_SR_pass_semiboosted_nominal', 'j3_SR_pass_semiboosted.png', 0.18, 0, 5500)
    makePlot('/STORE/HHH/Histograms/2017/20231220_123208/', 'mjj_vs_mjjj_SR_pass_boosted_nominal', 'j2_SR_pass_boosted.png', 0.16, 0, 3500, True)
    makePlot('/STORE/HHH/Histograms/2017/20231220_123208/', 'mjj_vs_mjjj_SR_pass_semiboosted_nominal', 'j2_SR_pass_semiboosted.png', 0.16, 0, 3500, True)
