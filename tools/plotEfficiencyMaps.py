import ROOT
import copy


mass_points = [
  (1200, 300), (1200, 600), (1200, 800), (1200, 1000),
  (1500, 300), (1500, 600), (1500, 800), (1500, 1000), (1500, 1300),
  (2000, 300), (2000, 600), (2000, 900), (2000, 1100), (2000, 1300), (2000, 1600),
  (2500, 300), (2500, 600), (2500, 800), (2500, 1000), (2500, 1300), (2500, 1600), (2500, 1800),
  (3000, 300), (3000, 600), (3000, 800), (3000, 1000), (3000, 1300), (3000, 1600), (3000, 1800), (3000, 2600), (3000, 2800),
  (3500, 300), (3500, 600), (3500, 700), (3500, 1100), (3500, 1300), (3500, 1600), (3500, 2000), (3500, 2500), (3500, 2800),
  (4000, 300), (4000, 600), (4000, 800), (4000, 1000), (4000, 1300), (4000, 1600), (4000, 2000), (4000, 2200), (4000, 2500), (4000, 2800)
]


def makePlot(path, cut_flow, step, hmax):

    selection = 'boosted'
    if 'semiboosted' in cut_flow:
        selection = 'semiboosted'

    gr_limit = copy.deepcopy(ROOT.TGraph2D())
    gr_limit.SetTitle(";m_{X} [GeV];m_{Y} [GeV];Selection efficiency (" + selection + ", " + step + ")")

    max_eff = 0.
    bin_total = 1
    bin_step = -1
    n = 0
    for (mX, mY) in mass_points:
        sample = 'XToYHTo6B_MX-{0}_MY-{1}'.format(mX, mY)

        print("\nProcessing {0}...".format(sample))
        
        file_path = '{0}/{1}_Histograms.root'.format(path, sample)

        f = ROOT.TFile.Open(file_path)

        cf = f.Get(cut_flow)
        if (bin_step==-1):
            axis = cf.GetXaxis()
            for b in range(1, axis.GetNbins() + 1):
                if axis.GetBinLabel(b) == step:
                    bin_step = b
                    break

        totalCount = cf.GetBinContent(bin_total)
        passCount = cf.GetBinContent(bin_step)
        eff = passCount/totalCount
        if eff > max_eff:
            max_eff = eff

        print("eff = {0}".format(eff))
        
        gr_limit.SetPoint(n,mX,mY,eff)
        
        n += 1

    print("\nMaximum efficiency: {0}\n".format(max_eff))

    c = ROOT.TCanvas("c", "",1000,900)
    c.cd()

    gr_limit.SetMinimum(0.)
    gr_limit.SetMaximum(hmax)

    gr_limit.Draw("cont4z")

    #c.SetLogz()

    c.SaveAs('Signal_efficiency_map_{0}_{1}.png'.format(selection, step))


if __name__ == '__main__':
    # to run in the batch mode (to prevent canvases from popping up)
    ROOT.gROOT.SetBatch()

    # set plot style
    ROOT.gROOT.SetStyle("Plain")
    ROOT.gStyle.SetPalette(57)

    ROOT.gStyle.SetPadTickX(1)  # to get the tick marks on the opposite side of the frame
    ROOT.gStyle.SetPadTickY(1)  # to get the tick marks on the opposite side of the frame

    # tweak margins
    ROOT.gStyle.SetPadTopMargin(0.1);
    ROOT.gStyle.SetPadBottomMargin(0.1);
    ROOT.gStyle.SetPadLeftMargin(0.12);
    ROOT.gStyle.SetPadRightMargin(0.16);

    # tweak axis title offsets
    ROOT.gStyle.SetTitleOffset(1.5, "Y");
    ROOT.gStyle.SetTitleOffset(1.25, "Z");

    # set nicer fonts
    ROOT.gStyle.SetTitleFont(42, "")
    ROOT.gStyle.SetTitleFont(42, "XYZ")
    ROOT.gStyle.SetLabelFont(42, "XYZ")
    ROOT.gStyle.SetTextFont(42)
    ROOT.gStyle.SetStatFont(42)
    ROOT.gROOT.ForceStyle()
    
    makePlot('/STORE/HHH/Histograms/2017/20231019_162502/', 'cutFlowHisto_SR_boosted', 'Pass', 0.25)
    makePlot('/STORE/HHH/Histograms/2017/20231019_162502/', 'cutFlowHisto_SR_semiboosted', 'Pass', 0.25)
    makePlot('/STORE/HHH/Histograms/2017/20231019_162502/', 'cutFlowHisto_SR_boosted', 'Fail', 0.004)
    makePlot('/STORE/HHH/Histograms/2017/20231019_162502/', 'cutFlowHisto_SR_semiboosted', 'Fail', 0.004)
