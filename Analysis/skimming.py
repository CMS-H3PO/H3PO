import uproot
import awkward as ak
from coffea.nanoevents import NanoEventsFactory, BaseSchema, NanoAODSchema
import numpy as np
import ROOT as r
from argparse import ArgumentParser
import os
import sys
import time
from condor.paths import H3_DIR
from coffea.lumi_tools import LumiMask

def isMC(events):
    if events['run'][0] < 100000:
        return True
    else:
        return False

def getYearFromRun(events):
    runNo = events['run'][0]
    if(runNo < 294927):#Run in 2017 golden json name
        return 2016
    elif(runNo < 314472):#Run in 2018 golden json name
        return 2017
    else:
        return 2018

def getGoldenJson(dataYear):
    if(dataYear==2016):
        jsonPath = os.path.join(H3_DIR,"../data/LumiJson/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt")
    elif(dataYear==2017):
        jsonPath = os.path.join(H3_DIR,"../data/LumiJson/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt")
    else:
        jsonPath = os.path.join(H3_DIR,"../data/LumiJson/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt")
    
    return jsonPath        


def is_rootcompat(a):
    """Is it a flat or 1-d jagged array?"""
    t = ak.type(a)
    if isinstance(t, ak._ext.ArrayType):
        if isinstance(t.type, ak._ext.PrimitiveType):
            return True
        if isinstance(t.type, ak._ext.ListType) and isinstance(t.type.type, ak._ext.PrimitiveType):
            return True
    return False

def uproot_writeable(events):
    """Restrict to columns that uproot can write compactly"""
    out = {}
    for bname in events.fields:
        if events[bname].fields:
            out[bname] = ak.zip(
                {
                    n: ak.packed(ak.without_parameters(events[bname][n]))
                    for n in events[bname].fields
                    if is_rootcompat(events[bname][n])
                }
            )
        else:
            out[bname] = ak.packed(ak.without_parameters(events[bname]))
    return out

def skim(inputFile,outputFile,eventsToRead=None):
    print("Skimming {0}".format(inputFile))
    events = NanoEventsFactory.from_root(inputFile,schemaclass=NanoAODSchema,entry_stop=eventsToRead).events()
    mcFlag = isMC(events)
    ptCut  = 200
    massCut = 50
    etaCut = 2.5
    print("MC flag is {0}".format(mcFlag))

    if not mcFlag:
        dataYear    = getYearFromRun(events)
        goldenJson  = getGoldenJson(dataYear)
        lumiMask    = LumiMask(goldenJson)(events['run'], events['luminosityBlock'])


    ptMask       = events.FatJet.pt>ptCut
    massMask     = ((events.FatJet.msoftdrop>massCut) | (events.FatJet.particleNet_mass>massCut))
    etaMask      = np.abs(events.FatJet.eta)<etaCut

    #We require at least two FatJets satisfying pt, eta and mass requirements
    #This allows for 3+0 or 2+1 (AK8Jet+AK4Jet topologies)
    skimmingMask = ak.sum(ptMask & massMask & etaMask, axis=1)>1
    if mcFlag:
        skimmed      = events[skimmingMask]
    else:
        skimmed      = events[skimmingMask & lumiMask]
    
    with uproot.recreate(outputFile) as fout:
        # ignore exception due to empty skim
        try:
            fout["Events"] = uproot_writeable(skimmed)
        except ValueError as e:
            if 'zero-size array' in str(e):
                print("WARNING: Empty skim. Ignoring ValueError:", e)
            else:
                raise
        except:
            raise

def copyRunsTree(inputFile,outputFile):
    print("Storing Runs tree in {0}".format(outputFile))
    #Save Runs tree
    #Copying TTrees with uproot is not yet supported so we use ROOT directly
    inputFile  = r.TFile.Open(inputFile)
    runsTree   = inputFile.Get("Runs")
    outputFile = r.TFile.Open(outputFile,"UPDATE")
    outputFile.cd()
    runsTree.CloneTree().Write()
    outputFile.Close()
    inputFile.Close()

def localCopy(inputLFN):
    xrdcpCMD = "xrdcp root://cms-xrd-global.cern.ch//{0} .".format(inputLFN)
    print(xrdcpCMD)
    result = os.system(xrdcpCMD)
    if result:
        print("File copying failed. Exiting")
        sys.exit(1)

parser = ArgumentParser()
parser.add_argument('-i', '--input', metavar='IFILE', action='store',
                default   =   '',
                dest      =   'input',
                help      =   'A root file or text file with multiple root file locations to analyze')
parser.add_argument('-o', '--odir', metavar='ODIR', action='store',
                default   =   '',
                dest      =   'outputDir',
                help      =   'Output directory path.')

(options, args) = parser.parse_known_args()
start_time      = time.time()

if(".txt" in options.input):
    inputFiles  = open(options.input, 'r')
    lines       = inputFiles.readlines()
    for iFile in lines:
        iFile    = iFile.rstrip()#Remove trailing newline
        localCopy(iFile)
        fileName = iFile.split("/")[-1]
        odir = options.outputDir
        if not os.path.exists(odir):
            print("CREATING DIR: ", odir)
            os.makedirs(odir)

        skim(fileName,os.path.join(odir,fileName),eventsToRead=None)
        copyRunsTree(fileName,os.path.join(odir,fileName))
        print("Removing local file {0}".format(fileName))
        os.system("rm {0}".format(fileName))


else:
    localCopy(options.input)
    fileName = options.input.split("/")[-1]
    odir = options.outputDir
    if not os.path.exists(odir):
        print("CREATING DIR: ", odir)
        os.makedirs(odir)

    skim(fileName,os.path.join(odir,fileName),eventsToRead=None)
    copyRunsTree(fileName,os.path.join(odir,fileName))
    print("Removing local file {0}".format(fileName))
    os.system("rm {0}".format(fileName))

print ('%s sec'%(time.time()-start_time))
