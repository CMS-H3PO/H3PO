import os
import copy
import re
import uproot
import awkward as ak
import hist
from hist import Hist
from Selection import *
from Util import *


j2_bins=120
j2_start=0
j2_stop=6000

j1_bins=120
j1_start=0
j1_stop=600

ht_bins=120
ht_start=0
ht_stop=6000

eta_bins=100
eta_start=-5
eta_stop=5

phi_bins = 100
phi_start = - np.pi
phi_stop = np.pi

version = "new"


def getTriggerEvtMask(events, trigList):
	refTriggerBits = np.array([events.HLT[t] for t in trigList if t in events.HLT.fields])
	return np.logical_or.reduce(refTriggerBits, axis=0)


def fillHistos(event_counts, extraHistos, SR_fail_fj, SR_pass_fj, VR_fail_fj, VR_pass_fj, SR_fail_e=None, SR_pass_e=None, VR_fail_e=None, VR_pass_e=None, refTrigList=None, trigList=None):
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



	particleNet_mass_SR_fail = ak.flatten(FatJetMass_pn(SR_fail_fj))
	particleNet_mass_SR_pass = ak.flatten(FatJetMass_pn(SR_pass_fj))
	particleNet_mass_VR_fail = ak.flatten(FatJetMass_pn(VR_fail_fj))
	particleNet_mass_VR_pass = ak.flatten(FatJetMass_pn(VR_pass_fj))

	softdrop_mass_SR_fail = ak.flatten(FatJetMass_sd(SR_fail_fj))
	softdrop_mass_SR_pass = ak.flatten(FatJetMass_sd(SR_pass_fj))
	softdrop_mass_VR_fail = ak.flatten(FatJetMass_sd(VR_fail_fj))
	softdrop_mass_VR_pass = ak.flatten(FatJetMass_sd(VR_pass_fj))



	pn_mass_SR_bin = hist.axis.Regular(label=f"Signal ParticleNet Mass [GeV]", name="pn_mass_SR", bins=j1_bins, start=j1_start, stop=j1_stop)
	sd_mass_SR_bin = hist.axis.Regular(label=f"Signal Softdrop Mass [GeV]", name="sd_mass_SR", bins=j1_bins, start=j1_start, stop=j1_stop)
	hists["sd_vs_pn_SR"] = Hist(pn_mass_SR_bin, sd_mass_SR_bin, storage="weight")
	hists["sd_vs_pn_SR"].fill(sd_mass_SR=softdrop_mass_SR_fail, pn_mass_SR=particleNet_mass_SR_fail)
	hists["sd_vs_pn_SR"].fill(sd_mass_SR=softdrop_mass_SR_pass, pn_mass_SR=particleNet_mass_SR_pass)



	pn_mass_VR_bin = hist.axis.Regular(label=f"Validation ParticleNet Mass [GeV]", name="pn_mass_VR", bins=j1_bins, start=j1_start, stop=j1_stop)
	sd_mass_VR_bin = hist.axis.Regular(label=f"Validation Softdrop Mass [GeV]", name="sd_mass_VR", bins=j1_bins, start=j1_start, stop=j1_stop)
	hists["sd_vs_pn_VR"] = Hist(pn_mass_VR_bin, sd_mass_VR_bin, storage="weight")
	hists["sd_vs_pn_VR"].fill(sd_mass_VR=softdrop_mass_VR_fail, pn_mass_VR=particleNet_mass_VR_fail)
	hists["sd_vs_pn_VR"].fill(sd_mass_VR=softdrop_mass_VR_pass, pn_mass_VR=particleNet_mass_VR_pass)








	dijet_mass_SR_fail = (SR_fail_fj[:,0]+SR_fail_fj[:,1]).mass
	dijet_mass_SR_pass = (SR_pass_fj[:,0]+SR_pass_fj[:,1]).mass
	dijet_mass_VR_fail = (VR_fail_fj[:,0]+VR_fail_fj[:,1]).mass
	dijet_mass_VR_pass = (VR_pass_fj[:,0]+VR_pass_fj[:,1]).mass


	if extraHistos:
		ht_SR_fail = SR_fail_fj[:,0].pt+SR_fail_fj[:,1].pt
		ht_SR_pass = SR_pass_fj[:,0].pt+SR_pass_fj[:,1].pt
		ht_VR_fail = VR_fail_fj[:,0].pt+VR_fail_fj[:,1].pt
		ht_VR_pass = VR_pass_fj[:,0].pt+VR_pass_fj[:,1].pt


	eta1_SR_fail = SR_fail_fj[:,0].eta
	eta2_SR_fail = SR_fail_fj[:,1].eta
	eta1_SR_pass = SR_pass_fj[:,0].eta
	eta2_SR_pass = SR_pass_fj[:,1].eta

	eta1_VR_fail = VR_fail_fj[:,0].eta
	eta2_VR_fail = VR_fail_fj[:,1].eta
	eta1_VR_pass = VR_pass_fj[:,0].eta
	eta2_VR_pass = VR_pass_fj[:,1].eta

	deltaEta_SR_fail = eta1_SR_fail - eta2_SR_fail
	deltaEta_SR_pass = eta1_SR_pass - eta2_SR_pass
	deltaEta_VR_fail = eta1_VR_fail - eta2_VR_fail
	deltaEta_VR_pass = eta1_VR_pass - eta2_VR_pass


	deltaPhi_SR_fail = SR_fail_fj[:,0].delta_phi(SR_fail_fj[:,1])	
	deltaPhi_SR_pass = SR_pass_fj[:,0].delta_phi(SR_pass_fj[:,1])
	deltaPhi_VR_fail = VR_fail_fj[:,0].delta_phi(VR_fail_fj[:,1])
	deltaPhi_VR_pass = VR_pass_fj[:,0].delta_phi(VR_pass_fj[:,1])



	j2_SR_fail_bin = hist.axis.Regular(label=f"Signal Fail Dijet Mass [GeV]", name="dijet_mass_SR_fail", bins=j2_bins, start=j2_start, stop=j2_stop)
	hists["j2_SR_fail"] = Hist(j2_SR_fail_bin, storage="weight")
	hists["j2_SR_fail"].fill(dijet_mass_SR_fail=dijet_mass_SR_fail)

	j2_SR_pass_bin = hist.axis.Regular(label=f"Signal Pass Dijet Mass [GeV]", name="dijet_mass_SR_pass", bins=j2_bins, start=j2_start, stop=j2_stop)
	hists["j2_SR_pass"] = Hist(j2_SR_pass_bin, storage="weight")
	hists["j2_SR_pass"].fill(dijet_mass_SR_pass=dijet_mass_SR_pass)

	j2_VR_fail_bin = hist.axis.Regular(label=f"Validation Fail Dijet Mass [GeV]", name="dijet_mass_VR_fail", bins=j2_bins, start=j2_start, stop=j2_stop)
	hists["j2_VR_fail"] = Hist(j2_VR_fail_bin, storage="weight")
	hists["j2_VR_fail"].fill(dijet_mass_VR_fail=dijet_mass_VR_fail)

	j2_VR_pass_bin = hist.axis.Regular(label=f"Validation Pass Dijet Mass [GeV]", name="dijet_mass_VR_pass", bins=j2_bins, start=j2_start, stop=j2_stop)
	hists["j2_VR_pass"] = Hist(j2_VR_pass_bin, storage="weight")
	hists["j2_VR_pass"].fill(dijet_mass_VR_pass=dijet_mass_VR_pass)

	if extraHistos:
		ht_SR_fail_bin = hist.axis.Regular(label=f"Signal Fail H_{{T}} [GeV]", name="ht_SR_fail", bins=ht_bins, start=ht_start, stop=ht_stop)
		hists["ht_vs_mjj_SR_fail"] = Hist(j2_SR_fail_bin, ht_SR_fail_bin, storage="weight")
		hists["ht_vs_mjj_SR_fail"].fill(ht_SR_fail=ht_SR_fail,dijet_mass_SR_fail=dijet_mass_SR_fail)

		eta_SR_fail_bin = hist.axis.Regular(label=f"Signal Fail Fat Jet #eta", name="eta_SR_fail", bins=eta_bins, start=eta_start, stop=eta_stop)
		hists["eta_SR_fail"] = Hist(eta_SR_fail_bin, storage="weight")
		hists["eta_SR_fail"].fill(eta_SR_fail=eta1_SR_fail)
		hists["eta_SR_fail"].fill(eta_SR_fail=eta2_SR_fail)

		ht_SR_pass_bin = hist.axis.Regular(label=f"Signal Pass H_{{T}} [GeV]", name="ht_SR_pass", bins=ht_bins, start=ht_start, stop=ht_stop)
		hists["ht_vs_mjj_SR_pass"] = Hist(j2_SR_pass_bin, ht_SR_pass_bin, storage="weight")
		hists["ht_vs_mjj_SR_pass"].fill(ht_SR_pass=ht_SR_pass,dijet_mass_SR_pass=dijet_mass_SR_pass)

		eta_SR_pass_bin = hist.axis.Regular(label=f"Signal Pass Fat Jet #eta", name="eta_SR_pass", bins=eta_bins, start=eta_start, stop=eta_stop)
		hists["eta_SR_pass"] = Hist(eta_SR_pass_bin, storage="weight")
		hists["eta_SR_pass"].fill(eta_SR_pass=eta1_SR_pass)
		hists["eta_SR_pass"].fill(eta_SR_pass=eta2_SR_pass)

		ht_VR_fail_bin = hist.axis.Regular(label=f"{label} Validation Fail H_{{T}} [GeV]", name="ht_VR_fail", bins=ht_bins, start=ht_start, stop=ht_stop)
		hists["ht_vs_mjj_VR_fail"] = Hist(j2_VR_fail_bin, ht_VR_fail_bin, storage="weight")
		hists["ht_vs_mjj_VR_fail"].fill(ht_VR_fail=ht_VR_fail,dijet_mass_VR_fail=dijet_mass_VR_fail)

		eta_VR_fail_bin = hist.axis.Regular(label=f"Validation Fail Fat Jet #eta", name="eta_VR_fail", bins=eta_bins, start=eta_start, stop=eta_stop)
		hists["eta_VR_fail"] = Hist(eta_VR_fail_bin, storage="weight")
		hists["eta_VR_fail"].fill(eta_VR_fail=eta1_VR_fail)
		hists["eta_VR_fail"].fill(eta_VR_fail=eta2_VR_fail)

		ht_VR_pass_bin = hist.axis.Regular(label=f"Validation Pass H_{{T}} [GeV]", name="ht_VR_pass", bins=ht_bins, start=ht_start, stop=ht_stop)
		hists["ht_vs_mjj_VR_pass"] = Hist(j2_VR_pass_bin, ht_VR_pass_bin, storage="weight")
		hists["ht_vs_mjj_VR_pass"].fill(ht_VR_pass=ht_VR_pass,dijet_mass_VR_pass=dijet_mass_VR_pass)

		eta_VR_pass_bin = hist.axis.Regular(label=f"Validation Pass Fat Jet #eta", name="eta_VR_pass", bins=eta_bins, start=eta_start, stop=eta_stop)
		hists["eta_VR_pass"] = Hist(eta_VR_pass_bin, storage="weight")
		hists["eta_VR_pass"].fill(eta_VR_pass=eta1_VR_pass)
		hists["eta_VR_pass"].fill(eta_VR_pass=eta2_VR_pass)


	jet1_higgs_SR_fail = SR_fail_fj[:,0][higgsCandidateMask_SR(SR_fail_fj[:,0], version)]
	jet2_higgs_SR_fail = SR_fail_fj[:,1][higgsCandidateMask_SR(SR_fail_fj[:,1], version)]
	jet1_y_SR_fail = SR_fail_fj[:,0][yCandidateMask_SR(SR_fail_fj[:,0], version)]
	jet2_y_SR_fail = SR_fail_fj[:,1][yCandidateMask_SR(SR_fail_fj[:,1], version)]


	jet1_higgs_SR_pass = SR_pass_fj[:,0][higgsCandidateMask_SR(SR_pass_fj[:,0], version)]
	jet2_higgs_SR_pass = SR_pass_fj[:,1][higgsCandidateMask_SR(SR_pass_fj[:,1], version)]
	jet1_y_SR_pass = SR_pass_fj[:,0][yCandidateMask_SR(SR_pass_fj[:,0], version)]
	jet2_y_SR_pass = SR_pass_fj[:,1][yCandidateMask_SR(SR_pass_fj[:,1], version)]


	jet1_higgs_VR_fail = VR_fail_fj[:,0][higgsCandidateMask_VR(VR_fail_fj[:,0], version)]
	jet2_higgs_VR_fail = VR_fail_fj[:,1][higgsCandidateMask_VR(VR_fail_fj[:,1], version)]
	jet1_y_VR_fail = VR_fail_fj[:,0][yCandidateMask_VR(VR_fail_fj[:,0], version)]
	jet2_y_VR_fail = VR_fail_fj[:,1][yCandidateMask_VR(VR_fail_fj[:,1], version)]


	jet1_higgs_VR_pass = VR_pass_fj[:,0][higgsCandidateMask_VR(VR_pass_fj[:,0], version)]
	jet2_higgs_VR_pass = VR_pass_fj[:,1][higgsCandidateMask_VR(VR_pass_fj[:,1], version)]
	jet1_y_VR_pass = VR_pass_fj[:,0][yCandidateMask_VR(VR_pass_fj[:,0], version)]
	jet2_y_VR_pass = VR_pass_fj[:,1][yCandidateMask_VR(VR_pass_fj[:,1], version)]



	jet1_higgs_mass_SR_fail = FatJetMass_pn(jet1_higgs_SR_fail)
	jet2_higgs_mass_SR_fail = FatJetMass_pn(jet2_higgs_SR_fail)
	jet1_y_mass_SR_fail = FatJetMass_sd(jet1_y_SR_fail)
	jet2_y_mass_SR_fail = FatJetMass_sd(jet2_y_SR_fail)

	jet1_higgs_mass_SR_pass = FatJetMass_pn(jet1_higgs_SR_pass)
	jet2_higgs_mass_SR_pass = FatJetMass_pn(jet2_higgs_SR_pass)
	jet1_y_mass_SR_pass = FatJetMass_sd(jet1_y_SR_pass)
	jet2_y_mass_SR_pass = FatJetMass_sd(jet2_y_SR_pass)

	jet1_higgs_mass_VR_fail = FatJetMass_pn(jet1_higgs_VR_fail)
	jet2_higgs_mass_VR_fail = FatJetMass_pn(jet2_higgs_VR_fail)
	jet1_y_mass_VR_fail = FatJetMass_sd(jet1_y_VR_fail)
	jet2_y_mass_VR_fail = FatJetMass_sd(jet2_y_VR_fail)

	jet1_higgs_mass_VR_pass = FatJetMass_pn(jet1_higgs_VR_pass)
	jet2_higgs_mass_VR_pass = FatJetMass_pn(jet2_higgs_VR_pass)
	jet1_y_mass_VR_pass = FatJetMass_sd(jet1_y_VR_pass)
	jet2_y_mass_VR_pass = FatJetMass_sd(jet2_y_VR_pass)




	j1_SR_fail_bin = hist.axis.Regular(label=f"Signal Fail Jet Mass [GeV]", name="jet_mass_SR_fail", bins=j1_bins, start=j1_start, stop=j1_stop)
	hists["mj_vs_mjj_SR_fail"] = Hist(j2_SR_fail_bin, j1_SR_fail_bin, storage="weight")
	hists["mj_vs_mjj_SR_fail"].fill(jet_mass_SR_fail=jet1_y_mass_SR_fail, dijet_mass_SR_fail=dijet_mass_SR_fail[yCandidateMask_SR(SR_fail_fj[:,0], version)])
	hists["mj_vs_mjj_SR_fail"].fill(jet_mass_SR_fail=jet2_y_mass_SR_fail, dijet_mass_SR_fail=dijet_mass_SR_fail[yCandidateMask_SR(SR_fail_fj[:,1], version)])

	hists["j1_higgs_mass_SR_fail"] = Hist(j1_SR_fail_bin, storage="weight")
	hists["j1_higgs_mass_SR_fail"].fill(jet_mass_SR_fail=jet1_higgs_mass_SR_fail)
	hists["j1_higgs_mass_SR_fail"].fill(jet_mass_SR_fail=jet2_higgs_mass_SR_fail)

	hists["j1_y_mass_SR_fail"] = Hist(j1_SR_fail_bin, storage="weight")
	hists["j1_y_mass_SR_fail"].fill(jet_mass_SR_fail=jet1_y_mass_SR_fail)
	hists["j1_y_mass_SR_fail"].fill(jet_mass_SR_fail=jet2_y_mass_SR_fail)




	j1_SR_pass_bin = hist.axis.Regular(label=f"Signal Pass Jet Mass [GeV]", name="jet_mass_SR_pass", bins=j1_bins, start=j1_start, stop=j1_stop)
	hists["mj_vs_mjj_SR_pass"] = Hist(j2_SR_pass_bin, j1_SR_pass_bin, storage="weight")
	hists["mj_vs_mjj_SR_pass"].fill(jet_mass_SR_pass=jet1_y_mass_SR_pass, dijet_mass_SR_pass=dijet_mass_SR_pass[yCandidateMask_SR(SR_pass_fj[:,0], version)])
	hists["mj_vs_mjj_SR_pass"].fill(jet_mass_SR_pass=jet2_y_mass_SR_pass, dijet_mass_SR_pass=dijet_mass_SR_pass[yCandidateMask_SR(SR_pass_fj[:,1], version)])

	hists["j1_higgs_mass_SR_pass"] = Hist(j1_SR_pass_bin, storage="weight")
	hists["j1_higgs_mass_SR_pass"].fill(jet_mass_SR_pass=jet1_higgs_mass_SR_pass)
	hists["j1_higgs_mass_SR_pass"].fill(jet_mass_SR_pass=jet2_higgs_mass_SR_pass)

	hists["j1_y_mass_SR_pass"] = Hist(j1_SR_pass_bin, storage="weight")
	hists["j1_y_mass_SR_pass"].fill(jet_mass_SR_pass=jet1_y_mass_SR_pass)
	hists["j1_y_mass_SR_pass"].fill(jet_mass_SR_pass=jet2_y_mass_SR_pass)



	j1_VR_fail_bin = hist.axis.Regular(label=f"Validation Fail Jet Mass [GeV]", name="jet_mass_VR_fail", bins=j1_bins, start=j1_start, stop=j1_stop)
	hists["mj_vs_mjj_VR_fail"] = Hist(j2_VR_fail_bin, j1_VR_fail_bin, storage="weight")
	hists["mj_vs_mjj_VR_fail"].fill(jet_mass_VR_fail=jet1_y_mass_VR_fail, dijet_mass_VR_fail=dijet_mass_VR_fail[yCandidateMask_VR(VR_fail_fj[:,0], version)])
	hists["mj_vs_mjj_VR_fail"].fill(jet_mass_VR_fail=jet2_y_mass_VR_fail, dijet_mass_VR_fail=dijet_mass_VR_fail[yCandidateMask_VR(VR_fail_fj[:,1], version)])

	hists["j1_higgs_mass_VR_fail"] = Hist(j1_VR_fail_bin, storage="weight")
	hists["j1_higgs_mass_VR_fail"].fill(jet_mass_VR_fail=jet1_higgs_mass_VR_fail)
	hists["j1_higgs_mass_VR_fail"].fill(jet_mass_VR_fail=jet2_higgs_mass_VR_fail)

	hists["j1_y_mass_VR_fail"] = Hist(j1_VR_fail_bin, storage="weight")
	hists["j1_y_mass_VR_fail"].fill(jet_mass_VR_fail=jet1_y_mass_VR_fail)
	hists["j1_y_mass_VR_fail"].fill(jet_mass_VR_fail=jet2_y_mass_VR_fail)



	j1_VR_pass_bin = hist.axis.Regular(label=f"Validation Pass Jet Mass [GeV]", name="jet_mass_VR_pass", bins=j1_bins, start=j1_start, stop=j1_stop)
	hists["mj_vs_mjj_VR_pass"] = Hist(j2_VR_pass_bin, j1_VR_pass_bin, storage="weight")
	hists["mj_vs_mjj_VR_pass"].fill(jet_mass_VR_pass=jet1_y_mass_VR_pass, dijet_mass_VR_pass=dijet_mass_VR_pass[yCandidateMask_VR(VR_pass_fj[:,0], version)])
	hists["mj_vs_mjj_VR_pass"].fill(jet_mass_VR_pass=jet2_y_mass_VR_pass, dijet_mass_VR_pass=dijet_mass_VR_pass[yCandidateMask_VR(VR_pass_fj[:,1], version)])

	hists["j1_higgs_mass_VR_pass"] = Hist(j1_VR_pass_bin, storage="weight")
	hists["j1_higgs_mass_VR_pass"].fill(jet_mass_VR_pass=jet1_higgs_mass_VR_pass)
	hists["j1_higgs_mass_VR_pass"].fill(jet_mass_VR_pass=jet2_higgs_mass_VR_pass)

	hists["j1_y_mass_VR_pass"] = Hist(j1_VR_pass_bin, storage="weight")
	hists["j1_y_mass_VR_pass"].fill(jet_mass_VR_pass=jet1_y_mass_VR_pass)
	hists["j1_y_mass_VR_pass"].fill(jet_mass_VR_pass=jet2_y_mass_VR_pass)





	deltaEta_SR_fail_bin = hist.axis.Regular(label=f"Signal Fail Delta #eta", name="deltaEta_SR_fail", bins=eta_bins, start=eta_start, stop=eta_stop)
	hists["deltaEta_SR_fail"] = Hist(deltaEta_SR_fail_bin, storage="weight")
	hists["deltaEta_SR_fail"].fill(deltaEta_SR_fail=deltaEta_SR_fail)

	deltaEta_SR_pass_bin = hist.axis.Regular(label=f"Signal Pass Delta #eta", name="deltaEta_SR_pass", bins=eta_bins, start=eta_start, stop=eta_stop)
	hists["deltaEta_SR_pass"] = Hist(deltaEta_SR_pass_bin, storage="weight")
	hists["deltaEta_SR_pass"].fill(deltaEta_SR_pass=deltaEta_SR_pass)

	deltaEta_VR_fail_bin = hist.axis.Regular(label=f"Validation Fail Delta #eta", name="deltaEta_VR_fail", bins=eta_bins, start=eta_start, stop=eta_stop)
	hists["deltaEta_VR_fail"] = Hist(deltaEta_VR_fail_bin, storage="weight")
	hists["deltaEta_VR_fail"].fill(deltaEta_VR_fail=deltaEta_VR_fail)

	deltaEta_VR_pass_bin = hist.axis.Regular(label=f"Validation Pass Delta #eta", name="deltaEta_VR_pass", bins=eta_bins, start=eta_start, stop=eta_stop)
	hists["deltaEta_VR_pass"] = Hist(deltaEta_VR_pass_bin, storage="weight")
	hists["deltaEta_VR_pass"].fill(deltaEta_VR_pass=deltaEta_VR_pass)




	deltaPhi_SR_fail_bin = hist.axis.Regular(label=f"Signal Fail Delta #phi", name="deltaPhi_SR_fail", bins=phi_bins, start=phi_start, stop=phi_stop)
	hists["deltaPhi_SR_fail"] = Hist(deltaPhi_SR_fail_bin, storage="weight")
	hists["deltaPhi_SR_fail"].fill(deltaPhi_SR_fail=deltaPhi_SR_fail)

	deltaPhi_SR_pass_bin = hist.axis.Regular(label=f"Signal Pass Delta #phi", name="deltaPhi_SR_pass", bins=phi_bins, start=phi_start, stop=phi_stop)
	hists["deltaPhi_SR_pass"] = Hist(deltaPhi_SR_pass_bin, storage="weight")
	hists["deltaPhi_SR_pass"].fill(deltaPhi_SR_pass=deltaPhi_SR_pass)

	deltaPhi_VR_fail_bin = hist.axis.Regular(label=f"Validation Fail Delta #phi", name="deltaPhi_VR_fail", bins=phi_bins, start=phi_start, stop=phi_stop)
	hists["deltaPhi_VR_fail"] = Hist(deltaPhi_VR_fail_bin, storage="weight")
	hists["deltaPhi_VR_fail"].fill(deltaPhi_VR_fail=deltaPhi_VR_fail)

	deltaPhi_VR_pass_bin = hist.axis.Regular(label=f"Validation Pass Delta #phi", name="deltaPhi_VR_pass", bins=phi_bins, start=phi_start, stop=phi_stop)
	hists["deltaPhi_VR_pass"] = Hist(deltaPhi_VR_pass_bin, storage="weight")
	hists["deltaPhi_VR_pass"].fill(deltaPhi_VR_pass=deltaPhi_VR_pass)

	return hists


def fillAllHistos(outHists, variation, event_counts, extraHistos, SR_fail_fj, SR_pass_fj, VR_fail_fj, VR_pass_fj, SR_fail_e=None, SR_pass_e=None, VR_fail_e=None, VR_pass_e=None, refTrigList=None, trigList=None):

	hists = {}
	hists["boosted"] = fillHistos(event_counts, extraHistos, SR_fail_fj, SR_pass_fj, VR_fail_fj, VR_pass_fj, SR_fail_e, SR_pass_e, VR_fail_e, VR_pass_e, refTrigList, trigList)


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

		SR_fail_e, SR_pass_e, SR_fail_fj, SR_pass_fj, VR_fail_e, VR_pass_e, VR_fail_fj, VR_pass_fj = Event_selection(input,process,event_counts,variation=variation, refTrigList=args.refTriggerList,trigList=args.triggerList,eventsToRead=None)

		# fill all histograms
		fillAllHistos(outHists, variation, event_counts, args.extra_histos, SR_fail_fj, SR_pass_fj, VR_fail_fj, VR_pass_fj)

		if not saveOnceDone and variation in ["nominal","fromFile"]:
			# give priority to 'nominal' if running both 'nominal' and 'fromFile'
			if variation=="nominal":
				saveOnceDone = True

			event_counts["SR_boosted"]["Fail"] = len(SR_fail_fj)
			event_counts["SR_boosted"]["Pass"] = len(SR_pass_fj)
			event_counts["VR_boosted"]["Fail"] = len(VR_fail_fj)
			event_counts["VR_boosted"]["Pass"] = len(VR_pass_fj)


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
