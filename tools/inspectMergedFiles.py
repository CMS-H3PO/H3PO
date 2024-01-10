import os
import ROOT


def inspectFiles(path, cut_flow):

    bin_total = 1

    for f in sorted(os.listdir(path)):
        # skip non-ROOT files
        if not f.endswith('.root'):
            continue
        
        print(f)
        
        file_path = os.path.join(path, f)

        rf = ROOT.TFile.Open(file_path)

        try:
            cf = rf.Get(cut_flow)
            totalCount = cf.GetBinContent(bin_total)
            print("Total count: {0}\n".format(totalCount))
        except:
            print("ERROR: Corrupt file. Cut flow histogram missing.\n")


if __name__ == '__main__':
    
    inspectFiles('/STORE/HHH/Histograms/2017/20231019_162502/', 'cutFlowHisto_SR_boosted')
    inspectFiles('/STORE/HHH/Histograms/2017/20231220_123208/', 'cutFlowHisto_SR_boosted')
