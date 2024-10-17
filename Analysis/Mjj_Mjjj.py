import os
import copy
import re
import uproot
import awkward as ak
import hist
from hist import Hist
from Selection import *
from Util import *


j1_bins=120
j1_start=0
j1_stop=500


version = "new"


def getTriggerEvtMask(events, trigList):
	refTriggerBits = np.array([events.HLT[t] for t in trigList if t in events.HLT.fields])
	return np.logical_or.reduce(refTriggerBits, axis=0)


def fillHistos(event_counts, extraHistos, fatjets, refTrigList=None, trigList=None):
	if refTrigList != None:
		# SR fail
		trigEvtMask = getTriggerEvtMask(SR_fail_e, refTrigList)
		SR_fail_e  =  SR_fail_e[trigEvtMask]
		SR_fail_fj = SR_fail_fj[trigEvtMask]

		# SR pass
		trigEvtMask = getTriggerEvtMask(SR_pass_e, refTrigList)
		SR_pass_e  =  SR_pass_e[trigEvtMask]
		SR_pass_fj = SR_pass_fj[trigEvtMask]

		# VR fail
		trigEvtMask = getTriggerEvtMask(VR_fail_e, refTrigList)
		VR_fail_e  =  VR_fail_e[trigEvtMask]
		VR_fail_fj = VR_fail_fj[trigEvtMask]

		# VR pass
		trigEvtMask = getTriggerEvtMask(VR_pass_e, refTrigList)
		VR_pass_e  =  VR_pass_e[trigEvtMask]
		VR_pass_fj = VR_pass_fj[trigEvtMask]


		# add reference trigger selection to the cut flow event counts
		event_counts["SR_boosted"]["Fail_refTrigger"] = len(SR_fail_fj)
		event_counts["SR_boosted"]["Pass_refTrigger"] = len(SR_pass_fj)
		event_counts["VR_boosted"]["Fail_refTrigger"] = len(VR_fail_fj)
		event_counts["VR_boosted"]["Pass_refTrigger"] = len(VR_pass_fj)


	if trigList != None:
		# SR fail
		trigEvtMask = getTriggerEvtMask(SR_fail_e, trigList)
		#SR_fail_e  =  SR_fail_e[trigEvtMask]
		SR_fail_fj = SR_fail_fj[trigEvtMask]

		# SR pass
		trigEvtMask = getTriggerEvtMask(SR_pass_e, trigList)
		#SR_pass_e  =  SR_pass_e[trigEvtMask]
		SR_pass_fj = SR_pass_fj[trigEvtMask]

		# VR fail
		trigEvtMask = getTriggerEvtMask(VR_fail_e, trigList)
		#VR_fail_e  =  VR_fail_e[trigEvtMask]
		VR_fail_fj = VR_fail_fj[trigEvtMask]

		# VR pass
		trigEvtMask = getTriggerEvtMask(VR_pass_e, trigList)
		#VR_pass_e  =  VR_pass_e[trigEvtMask]
		VR_pass_fj = VR_pass_fj[trigEvtMask]



		# add analysis trigger selection to the cut flow event counts
		event_counts["SR_boosted"]["Fail_trigger"] = len(SR_fail_fj)
		event_counts["SR_boosted"]["Pass_trigger"] = len(SR_pass_fj)
		event_counts["VR_boosted"]["Fail_trigger"] = len(VR_fail_fj)
		event_counts["VR_boosted"]["Pass_trigger"] = len(VR_pass_fj)


	hists = {}



	particleNet_mass = ak.flatten(FatJetMass_pn(fatjets)[:,0:2])
	softdrop_mass = ak.flatten(FatJetMass_sd(fatjets)[:,0:2])



	pn_mass_bin = hist.axis.Regular(label=f"ParticleNet Mass [GeV]", name="pn_mass", bins=j1_bins, start=j1_start, stop=j1_stop)
	sd_mass_bin = hist.axis.Regular(label=f"Softdrop Mass [GeV]", name="sd_mass", bins=j1_bins, start=j1_start, stop=j1_stop)
	hists["sd_vs_pn"] = Hist(pn_mass_bin, sd_mass_bin, storage="weight")
	hists["sd_vs_pn"].fill(sd_mass=softdrop_mass, pn_mass=particleNet_mass)



	return hists


def fillAllHistos(outHists, variation, event_counts, extraHistos, fatjets, refTrigList=None, trigList=None):

	hists = {}
	hists["boosted"] = fillHistos(event_counts, extraHistos, fatjets, refTrigList, trigList)


	selections = ["boosted"]
	suffix = ("" if variation=="fromFile" else f"_{variation}")
	if refTrigList != None or trigList != None:
		suffix += "_"
		if refTrigList != None and trigList == None:
			suffix += "ref"
		elif refTrigList != None and trigList != None:
			suffix += "refAndAn"
		else:
			suffix += "an"
		suffix += "Trig"

	for sel in selections:
		for hist in hists[sel]:
			outHists[f"{hist}_{sel}{suffix}"] = hists[sel][hist]

	return


if __name__ == "__main__":
	import time
	start_time = time.time()
	from argparse import ArgumentParser

	parser = ArgumentParser(description="Do -h to see usage")
	parser.add_argument('-s', '--sample', help='Sample name', default="QCD2000")
	parser.add_argument('-i', '--input', help='Input file')
	parser.add_argument('-o', '--output', help='Output directory')
	parser.add_argument("-j", "--jecVariations", dest="jecVariations",
                        help="Space-separated list of JEC variations (default: %(default)s). Use 'fromFile' to turn off the JEC re-application.",
                        nargs='*',
                        default=["nominal","jesUp","jesDown","jerUp","jerDown"],
                        metavar="JECVARS")
	parser.add_argument('-t', '--triggerList', help='Space-separated list of triggers (default: %(default)s);)',
                        nargs='*',
                        dest='triggerList',
                        default = None
                        )
	parser.add_argument("-r", "--refTriggerList", help="Space-separated list of reference triggers (default: %(default)s);)",
                        nargs="*",
                        dest="refTriggerList",
                        default = None
                        )
	parser.add_argument("--extra_histos", dest="extra_histos", action='store_true',
                        help="Switch for producing additional histograms (default: %(default)s)",
                        default=False)

	args = parser.parse_args()
    
	process=args.sample
	input=args.input
	output=args.output
	ofile = os.path.basename(input)
	print(process)
	yearFromInputFile(input)

	knownVariations = copy.deepcopy(parser.get_default('jecVariations'))
	knownVariations.append("fromFile")
	acceptedVariations = []
	unknownVariations = []

	for v in args.jecVariations:
		if v not in knownVariations:
			unknownVariations.append(v)
		else:
			acceptedVariations.append(v)
	if len(unknownVariations)>0:
		if len(acceptedVariations)==0:
			print("Unknown JEC variation(s) specified: {}. Defaulting to 'nominal'.".format(' '.join(unknownVariations)))
			acceptedVariations.append("nominal")
		else:
			print("Unknown JEC variation(s) specified: {}. Will be ignored.".format(' '.join(unknownVariations)))

	# special case of real data
	variations = [v for v in acceptedVariations if v in ["nominal","fromFile"]]
	if len(acceptedVariations)>0 and len(variations)==0:
		print("No appropriate JEC variation(s) for data specified. Defaulting to 'nominal'.")
		variations.append("nominal")
	numberOfGenEvents = 0.
	# if MC sample
	if ("JetHT" not in process):
		numberOfGenEvents = getNumberOfGenEvents(input)
		variations        = acceptedVariations
	numberOfGenEventsAxis = hist.axis.Integer(0, 1, label="Number of generated events", underflow=False, overflow=False)
	numberOfGenEventsHisto = Hist(numberOfGenEventsAxis)
	numberOfGenEventsHisto[0] = numberOfGenEvents

	event_counts = {}
	first_bin = ("Total" if "JetHT" not in process else "Dataset_and_skim")

	regions = ["SR_boosted", "VR_boosted"]
	for r in regions:
		event_counts[r] = {}
		event_counts[r][first_bin] = (numberOfGenEvents if "JetHT" not in process else getNumberOfEvents(input))   

	outHists = {}
	cutFlowHistos = {}
	saveOnceDone = False
	saveOnceMCDone = False

	for variation in variations:
		# save the total number of generated events for MC samples
		if not saveOnceMCDone and "JetHT" not in process and variation in ["nominal","fromFile"]:
			saveOnceMCDone = True
			outHists["numberOfGenEventsHisto"] = numberOfGenEventsHisto

		events, fatjets = Event_selection(input,process,event_counts,variation=variation, refTrigList=args.refTriggerList,trigList=args.triggerList,eventsToRead=None, version_of_selection="new")

		# fill all histograms
		fillAllHistos(outHists, variation, event_counts, args.extra_histos, fatjets)

		if not saveOnceDone and variation in ["nominal","fromFile"]:
			# give priority to 'nominal' if running both 'nominal' and 'fromFile'
			if variation=="nominal":
				saveOnceDone = True



			# if doing trigger efficiency studies
			if args.refTriggerList != None:
				fillAllHistos(outHists, variation, event_counts, args.extra_histos, SR_fail_fj, SR_pass_fj, VR_fail_fj, VR_pass_fj, SR_fail_e, SR_pass_e, VR_fail_e, VR_pass_e, args.refTriggerList)
				# if the analysis trigger(s) are applied as well
				if args.triggerList != None:
					fillAllHistos(outHists, variation, event_counts, args.extra_histos, SR_fail_fj, SR_pass_fj, VR_fail_fj, VR_pass_fj, SR_fail_e, SR_pass_e, VR_fail_e, VR_pass_e, args.refTriggerList, args.triggerList)

			# create and fill the cut flow histograms
			for r in regions:
				cutFlowHistos[r] = ROOT.TH1D(f"cutFlowHisto_{r}", f"{r};Cut flow;Number of events", len(event_counts[r].keys()), 0., float(len(event_counts[r].keys())))
				for i, key in enumerate(event_counts[r].keys()):
					cutFlowHistos[r].SetBinContent(i+1, event_counts[r][key])
					cutFlowHistos[r].GetXaxis().SetBinLabel(i+1, key)

	# save histograms to a ROOT file
	with uproot.recreate(os.path.join(output, "Histograms_{0}-{1}".format(process, ofile))) as fout:
		keys = sorted(outHists.keys())
		# if present, save numberOfGenEventsHisto first
		histName = "numberOfGenEventsHisto"
		if histName in keys:
			fout[histName] = outHists[histName]
			keys.remove(histName)
		# save all other histograms
		for histName in keys:
			fout[histName] = outHists[histName]
		#for r in regions:
			#fout[f"cutFlowHisto_{r}"] = cutFlowHistos[r] # this does not work properly (see [*])

	# re-open the ROOT file for some updates and storing additional histograms
	fout = ROOT.TFile.Open(os.path.join(output, "Histograms_{0}-{1}".format(process, ofile)), 'UPDATE')
	list_of_keys = copy.deepcopy(fout.GetListOfKeys()) # without deepcopy the processing time explodes, no idea why
	# sum up two sets of semiboosted histograms and delete the 'eq2' set
	for myKey in list_of_keys:
		if re.match ('TH', myKey.GetClassName()):
			hname = myKey.GetName()
			if ("eq2" not in hname):
				continue
			h_eq2 = fout.Get(hname)
			h = fout.Get(hname.replace("_eq2", ""))
			h.Add(h_eq2)
			h.Write("", ROOT.TObject.kOverwrite)
			fout.Delete(hname + ";1")
	# [*] uproot has some issues with storing histograms with labelled bins (apparently only the first bin is stored) so resorting to plain ROOT here
	for r in regions:
		cutFlowHistos[r].Write()
	fout.Close()
	print("--- %s seconds ---" % (time.time() - start_time))
