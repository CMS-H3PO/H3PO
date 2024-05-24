import ROOT
import copy


mass_points = [
  (1000, 300), (1000, 800),
  (1200, 300), (1200, 800), (1200, 1000),
  (1600, 300), (1600, 800), (1600, 1400),
  (2000, 300), (2000, 800), (2000, 1200), (2000, 1800),
  (2500, 600), (2500, 800), (2500, 1200), (2500, 2000),
  (3000, 600), (3000, 1000), (3000, 1600), (3000, 2500),
  (3500, 600), (3500, 1000), (3500, 1600), (3500, 2500),
  (4000, 600), (4000, 1000), (4000, 1600), (4000, 2800)
]

colors = [1, 2, 8, 4, 6, 7, 9]
styles = [1, 2, 3, 4, 5, 6, 7]
data = {
	"2016":"/STORE/HHH/Histograms/2016/20240224_100140",
	"2016APV":"/STORE/HHH/Histograms/2016APV/20240215_135412",
	"2017":"/STORE/HHH/Histograms/2017/20240211_172232",
	"2018":"/STORE/HHH/Histograms/2018/20240225_102238"
}


def makePlot(histo, mX, mY, hmax, x_min, x_max, proj=False):

    histos = []

    for year in data:
        sample = 'XToYHTo6B_MX-{0}_MY-{1}'.format(mX, mY)

        print("\nProcessing {0} from {1}...".format(sample, year))
        
        file_path = '{0}/{1}_Histograms.root'.format(data[year], sample)

        f = ROOT.TFile.Open(file_path)

        if proj:
            histos.append((copy.deepcopy(f.Get(histo).ProjectionY()), year))
        else:
            histos.append((copy.deepcopy(f.Get(histo)), year))
        
        f.Close()

    c = ROOT.TCanvas("c_{}_{}_{}".format(histo, mX, mY), "",1000,900)
    c.cd()
    
    if ((mX==1000 and mY==300) or (mX==1000 and mY==800) or (mX==1200 and mY==1000) or (mX==1600 and mY==800) or (mX==2000 and mY==1200)) :
         hmax = 0.2
    if (mX==1200 and mY==800):
         hmax = 0.25	

    frame = ROOT.TH1F("frame",";{0} [GeV]".format("m_{jjj}" if "j3" in histo else "m_{jj}"),1000,x_min,x_max)
    frame.SetMaximum(hmax)
    frame.SetStats(0)
    frame.Draw()

    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextFont(42)
    l.SetTextSize(0.04)
    l.SetTextAlign(12)
    mX_label = "{0} GeV".format(mX)
    l.DrawLatex(0.6, 0.85, "m_{X}=" + mX_label)
    mY_label = "{0} GeV".format(mY)
    l.DrawLatex(0.6, 0.8, "m_{Y}=" + mY_label)
    if "semiboosted" in histo:
        l.DrawLatex(0.15, 0.82, "SR pass semiboosted")
    elif "boosted" in histo:
        l.DrawLatex(0.15, 0.82, "SR pass boosted")
    
    legend = ROOT.TLegend(.6,.5,.8,.75)
    if ((mX==3500 and mY==1600) or (mX==3500 and mY==2500) or (mX==4000 and mY==1600) or (mX==4000 and mY==2800)) :
         legend = ROOT.TLegend(.2,.5,.4,.75)
    if ((mX==3500 and mY==1000) or (mX==4000 and mY==1000)) :
         legend = ROOT.TLegend(.7,.5,.9,.75)
    legend.SetTextFont(42)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.04)
    legend.SetHeader("Year", "l")
    
    n = 0
    for (h, year) in histos:
        h.SetLineColor(colors[n])
        h.SetLineStyle(styles[n])
        h.SetLineWidth(2)
        h.DrawNormalized('histsame')
        legend.AddEntry(h,"{0}".format(year),"l")
        n += 1

    legend.Draw()

    #c.SaveAs(fname)
    
    fname = "comparison_by_years/MX-{0}_MY-{1}_comparisons.pdf".format(mX, mY)
    if "j3_SR_pass_boosted" in histo:
        c.Print(fname+"(", "pdf")
    elif "mjj_vs_mjjj_SR_pass_semiboosted" in histo:
        c.Print(fname+")", "pdf")
    else:
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
    
    for (mX, mY) in mass_points:
	        makePlot('j3_SR_pass_boosted_nominal', mX, mY, 0.18, 0, 5500)
	        makePlot('j3_SR_pass_semiboosted_nominal', mX, mY, 0.18, 0, 5500)
	        makePlot('mjj_vs_mjjj_SR_pass_boosted_nominal', mX, mY, 0.16, 0, 3500, True)
	        makePlot('mjj_vs_mjjj_SR_pass_semiboosted_nominal', mX, mY, 0.16, 0, 3500, True)
