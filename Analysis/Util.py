import ROOT

def getNumberOfGenEvents(fname):
    froot = ROOT.TFile.Open(fname)
    myTree = froot.Runs
    total_events = 0
    for entry in myTree:
        total_events += entry.genEventCount
    return total_events

