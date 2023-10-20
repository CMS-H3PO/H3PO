import ROOT

def getNumberOfGenEvents(fname):
    froot = ROOT.TFile.Open(fname, 'READ')
    myTree = froot.Runs
    total_events = 0
    for entry in myTree:
        total_events += entry.genEventCount
    froot.Close()
    return total_events

def getNumberOfEvents(fname):
    froot = ROOT.TFile.Open(fname, 'READ')
    myTree = froot.Events
    total_events = myTree.GetEntriesFast()
    froot.Close()
    return total_events
