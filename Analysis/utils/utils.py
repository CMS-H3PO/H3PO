import copy
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


def yearFromInputFile(inputFile):
    if("2016APV" in inputFile):
        return "2016APV"
    #Because 2016 repeats, ordering is important
    elif("2016" in inputFile):
        return "2016"
    elif("2017" in inputFile):
        return "2017"
    elif("2018" in inputFile):
        return "2018" 
    else:       
        raise ValueError('Could not determine year from input file: {0}'.format(inputFile))


def addCut(cuts, newCut, decision):
    cuts_ = copy.deepcopy(cuts)
    for k in cuts_.keys():
        cuts_[k][newCut] = decision

    return cuts_
