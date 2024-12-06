import ROOT
import copy


mass_points = [
  (1000, 300), (1000, 600), (1000, 800),
  (1200, 300), (1200, 600), (1200, 800), (1200, 1000),
  (1300, 300), (1300, 350), (1300, 400), (1300, 450), (1300, 500),
  (1400, 300), (1400, 350), (1400, 400), (1400, 450), (1400, 500),
  (1500, 300), (1500, 350), (1500, 400), (1500, 450), (1500, 500),
  (1600, 300), (1600, 350), (1600, 400), (1600, 450), (1600, 500), (1600, 600), (1600, 800), (1600, 1000), (1600, 1200), (1600, 1400),
  (1700, 300), (1700, 350), (1700, 400), (1700, 450), (1700, 500),
  (1800, 300), (1800, 350), (1800, 400), (1800, 450), (1800, 500),
  (1900, 300), (1900, 350), (1900, 400), (1900, 450), (1900, 500),
  (2000, 300), (2000, 350), (2000, 400), (2000, 450), (2000, 500), (2000, 600), (2000, 800), (2000, 1000), (2000, 1200), (2000, 1600), (2000, 1800),
  (2200, 300), (2200, 350), (2200, 400), (2200, 450), (2200, 500), (2200, 600),
  (2400, 300), (2400, 350), (2400, 400), (2400, 450), (2400, 500), (2400, 600),
  (2500, 300), (2500, 350), (2500, 400), (2500, 450), (2500, 500), (2500, 600), (2500, 700), (2500, 800), (2500, 1000), (2500, 1200), (2500, 1600), (2500, 2000), (2500, 2200),
  (2600, 300), (2600, 350), (2600, 400), (2600, 450), (2600, 500), (2600, 600), (2600, 700), (2600, 800),
  (2800, 300), (2800, 350), (2800, 400), (2800, 450), (2800, 500), (2800, 600), (2800, 700), (2800, 800),
  (3000, 300), (3000, 350), (3000, 400), (3000, 450), (3000, 500), (3000, 600), (3000, 700), (3000, 800), (3000, 1000), (3000, 1200), (3000, 1600), (3000, 2000), (3000, 2500), (3000, 2800),
  (3500, 300), (3500, 350), (3500, 400), (3500, 450), (3500, 500), (3500, 600), (3500, 700), (3500, 800), (3500, 1000), (3500, 1200), (3500, 1600), (3500, 2000), (3500, 2500), (3500, 2800),
  (4000, 300), (4000, 350), (4000, 400), (4000, 450), (4000, 500), (4000, 600), (4000, 700), (4000, 800), (4000, 900), (4000, 1000), (4000, 1200), (4000, 1600), (4000, 2000), (4000, 2500), (4000, 2800)
]




def makePlot(path, cut_flow, step, hmax, label):

    gr_limit = copy.deepcopy(ROOT.TGraph2D())
    gr_limit.SetTitle(";m_{X} [GeV];m_{Y} [GeV];Selection efficiency (boosted, " + step + ")")

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

    c.SaveAs('Signal_efficiency_map_modified_{0}_{1}.png'.format(step, label))


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
    
    makePlot('~/condor_jobs_2017_background_20241122_160118/fit', 'cutFlowHisto_SR_boosted', 'Pass', 0.45, "2017_old")
    makePlot('~/condor_jobs_2017_background_20241122_160118/fit', 'cutFlowHisto_SR_boosted', 'Fail', 0.035, "2017_old")

    makePlot('~/condor_jobs_2017_background_20241122_162804/fit', 'cutFlowHisto_SR_boosted', 'Pass', 0.5, "2017_new")
    makePlot('~/condor_jobs_2017_background_20241122_162804/fit', 'cutFlowHisto_SR_boosted', 'Fail', 0.055, "2017_new")

    makePlot('~/Run2_old/latest', 'cutFlowHisto_SR_boosted', 'Pass', 0.4, "Run2_old")
    makePlot('~/Run2_old/latest', 'cutFlowHisto_SR_boosted', 'Fail', 0.035, "Run2_old")

    makePlot('~/Run2_new/latest', 'cutFlowHisto_SR_boosted', 'Pass', 0.5, "Run2_new")
    makePlot('~/Run2_new/latest', 'cutFlowHisto_SR_boosted', 'Fail', 0.055, "Run2_new")

