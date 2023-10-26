import importlib.resources
import contextlib
from coffea.lookup_tools import extractor
from coffea.jetmet_tools import JECStack, CorrectedJetsFactory, CorrectedMETFactory
import gzip
import cloudpickle

#Inspired by https://github.com/nsmith-/boostedhiggs/blob/cc/boostedhiggs/build_jec.py

jec_name_map = {
    'JetPt': 'pt',
    'JetMass': 'mass',
    'JetEta': 'eta',
    'JetA': 'area',
    'ptGenJet': 'pt_gen',
    'ptRaw': 'pt_raw',
    'massRaw': 'mass_raw',
    'Rho': 'event_rho',
    'METpt': 'pt',
    'METphi': 'phi',
    'JetPhi': 'phi',
    'UnClusteredEnergyDeltaX': 'MetUnclustEnUpDeltaX',
    'UnClusteredEnergyDeltaY': 'MetUnclustEnUpDeltaY',
}


def jet_factory_factory(files,path):
    ext = extractor()
    with contextlib.ExitStack() as stack:
        real_files = [path+f for f in files]
        ext.add_weight_sets([f"* * {file}" for file in real_files])
        ext.finalize()

    jec_stack = JECStack(ext.make_evaluator())
    return CorrectedJetsFactory(jec_name_map, jec_stack)



#UL 
#JEC from https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC#Recommended_for_MC
#JER from https://github.com/cms-jet/JRDatabase/tree/master/tarballs
fatjet_factory = {    
    "2016APVmc": jet_factory_factory(
        files=[
            "Summer19UL16APV_V7_MC_L1FastJet_AK8PFPuppi.jec.txt.gz",
            "Summer19UL16APV_V7_MC_L2Relative_AK8PFPuppi.jec.txt.gz",
            "Summer19UL16APV_V7_MC_L2L3Residual_AK8PFPuppi.jec.txt.gz",
            #"Summer19UL16APV_V7_MC_L2Residual_AK8PFPuppi.jec.txt.gz", #This one can actually be included, but does not affect result!
            "Summer19UL16APV_V7_MC_L3Absolute_AK8PFPuppi.jec.txt.gz",
            "Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.junc.txt.gz",
            "Summer19UL16APV_V7_MC_UncertaintySources_AK8PFPuppi.junc.txt.gz",
            "Summer20UL16APV_JRV3_MC_PtResolution_AK8PFPuppi.jr.txt.gz",
            "Summer20UL16APV_JRV3_MC_SF_AK8PFPuppi.jersf.txt.gz"
        ],path="../data/jec/2016APV/"
    ),
        "2016mc": jet_factory_factory(
        files=[
            "Summer19UL16_V7_MC_L1FastJet_AK8PFPuppi.jec.txt.gz",
            "Summer19UL16_V7_MC_L2Relative_AK8PFPuppi.jec.txt.gz",
            "Summer19UL16_V7_MC_L2L3Residual_AK8PFPuppi.jec.txt.gz",
            #"Summer19UL16_V7_MC_L2Residual_AK8PFPuppi.jec.txt.gz", #This one can actually be included, but does not affect result!
            "Summer19UL16_V7_MC_L3Absolute_AK8PFPuppi.jec.txt.gz",
            "Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.junc.txt.gz",
            "Summer19UL16_V7_MC_UncertaintySources_AK8PFPuppi.junc.txt.gz",
            "Summer20UL16_JRV3_MC_PtResolution_AK8PFPuppi.jr.txt.gz",
            "Summer20UL16_JRV3_MC_SF_AK8PFPuppi.jersf.txt.gz"
        ],path="../data/jec/2016/"
    ),
        "2017mc": jet_factory_factory(
        files=[
            "Summer19UL17_V5_MC_L1FastJet_AK8PFPuppi.jec.txt.gz",
            "Summer19UL17_V5_MC_L2Relative_AK8PFPuppi.jec.txt.gz",
            "Summer19UL17_V5_MC_L2L3Residual_AK8PFPuppi.jec.txt.gz",
            #"Summer19UL17_V5_MC_L2Residual_AK8PFPuppi.jec.txt.gz", #This one can actually be included, but does not affect result!
            "Summer19UL17_V5_MC_L3Absolute_AK8PFPuppi.jec.txt.gz",
            "Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.junc.txt.gz",
            "Summer19UL17_V5_MC_UncertaintySources_AK8PFPuppi.junc.txt.gz",
            "Summer19UL17_JRV3_MC_PtResolution_AK8PFPuppi.jr.txt.gz",
            "Summer19UL17_JRV3_MC_SF_AK8PFPuppi.jersf.txt.gz"
        ],path="../data/jec/2017/"
    ),
        "2018mc": jet_factory_factory(
        files=[
        "Summer19UL18_V5_MC_L1FastJet_AK8PFPuppi.jec.txt.gz",
        "Summer19UL18_V5_MC_L2Relative_AK8PFPuppi.jec.txt.gz",
        "Summer19UL18_V5_MC_L2L3Residual_AK8PFPuppi.jec.txt.gz",
        #"Summer19UL18_V5_MC_L2Residual_AK8PFPuppi.jec.txt.gz", #This one can actually be included, but does not affect result!
        "Summer19UL18_V5_MC_L3Absolute_AK8PFPuppi.jec.txt.gz",
        "Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.junc.txt.gz",
        "Summer19UL18_V5_MC_UncertaintySources_AK8PFPuppi.junc.txt.gz",
        "Summer19UL18_JRV2_MC_PtResolution_AK8PFPuppi.jr.txt.gz",
        "Summer19UL18_JRV2_MC_SF_AK8PFPuppi.jersf.txt.gz"

        ],path="../data/jec/2018/"
    ),
        "2016APVRunBCD": jet_factory_factory(
        files=[
        "Summer19UL16APV_RunBCD_V7_DATA_L1FastJet_AK8PFPuppi.jec.txt.gz",
        "Summer19UL16APV_RunBCD_V7_DATA_L2Relative_AK8PFPuppi.jec.txt.gz",
        "Summer19UL16APV_RunBCD_V7_DATA_L2L3Residual_AK8PFPuppi.jec.txt.gz",
        #"Summer19UL16APV_RunBCD_V7_DATA_L2Residual_AK8PFPuppi.jec.txt.gz",
        "Summer19UL16APV_RunBCD_V7_DATA_L3Absolute_AK8PFPuppi.jec.txt.gz",
        ],path="../data/jec/2016APV/"
    ),
        "2016APVRunEF": jet_factory_factory(
        files=[
        "Summer19UL16APV_RunEF_V7_DATA_L1FastJet_AK8PFPuppi.jec.txt.gz",
        "Summer19UL16APV_RunEF_V7_DATA_L2Relative_AK8PFPuppi.jec.txt.gz",
        "Summer19UL16APV_RunEF_V7_DATA_L2L3Residual_AK8PFPuppi.jec.txt.gz",
        #"Summer19UL16APV_RunEF_V7_DATA_L2Residual_AK8PFPuppi.jec.txt.gz",
        "Summer19UL16APV_RunEF_V7_DATA_L3Absolute_AK8PFPuppi.jec.txt.gz",
        ],path="../data/jec/2016APV/"
    ),
        "2016RunFGH": jet_factory_factory(
        files=[
        "Summer19UL16_RunFGH_V7_DATA_L1FastJet_AK8PFPuppi.jec.txt.gz",
        "Summer19UL16_RunFGH_V7_DATA_L2Relative_AK8PFPuppi.jec.txt.gz",
        "Summer19UL16_RunFGH_V7_DATA_L2L3Residual_AK8PFPuppi.jec.txt.gz",
        #"Summer19UL16_RunFGH_V7_DATA_L2Residual_AK8PFPuppi.jec.txt.gz",
        "Summer19UL16_RunFGH_V7_DATA_L3Absolute_AK8PFPuppi.jec.txt.gz",
        ],path="../data/jec/2016/"
    ),
        "2017RunB": jet_factory_factory(
        files=[
        "Summer19UL17_RunB_V5_DATA_L1FastJet_AK8PFPuppi.jec.txt.gz",
        "Summer19UL17_RunB_V5_DATA_L2Relative_AK8PFPuppi.jec.txt.gz",
        "Summer19UL17_RunB_V5_DATA_L2L3Residual_AK8PFPuppi.jec.txt.gz",
        #"Summer19UL17_RunB_V5_DATA_L2Residual_AK8PFPuppi.jec.txt.gz",
        "Summer19UL17_RunB_V5_DATA_L3Absolute_AK8PFPuppi.jec.txt.gz",
        ],path="../data/jec/2017/"
    ),
        "2017RunC": jet_factory_factory(
        files=[
        "Summer19UL17_RunC_V5_DATA_L1FastJet_AK8PFPuppi.jec.txt.gz",
        "Summer19UL17_RunC_V5_DATA_L2Relative_AK8PFPuppi.jec.txt.gz",
        "Summer19UL17_RunC_V5_DATA_L2L3Residual_AK8PFPuppi.jec.txt.gz",
        #"Summer19UL17_RunC_V5_DATA_L2Residual_AK8PFPuppi.jec.txt.gz",
        "Summer19UL17_RunC_V5_DATA_L3Absolute_AK8PFPuppi.jec.txt.gz",
        ],path="../data/jec/2017/"
    ),
        "2017RunD": jet_factory_factory(
        files=[
        "Summer19UL17_RunD_V5_DATA_L1FastJet_AK8PFPuppi.jec.txt.gz",
        "Summer19UL17_RunD_V5_DATA_L2Relative_AK8PFPuppi.jec.txt.gz",
        "Summer19UL17_RunD_V5_DATA_L2L3Residual_AK8PFPuppi.jec.txt.gz",
        #"Summer19UL17_RunD_V5_DATA_L2Residual_AK8PFPuppi.jec.txt.gz",
        "Summer19UL17_RunD_V5_DATA_L3Absolute_AK8PFPuppi.jec.txt.gz",
        ],path="../data/jec/2017/"
    ),
        "2017RunE": jet_factory_factory(
        files=[
        "Summer19UL17_RunE_V5_DATA_L1FastJet_AK8PFPuppi.jec.txt.gz",
        "Summer19UL17_RunE_V5_DATA_L2Relative_AK8PFPuppi.jec.txt.gz",
        "Summer19UL17_RunE_V5_DATA_L2L3Residual_AK8PFPuppi.jec.txt.gz",
        #"Summer19UL17_RunE_V5_DATA_L2Residual_AK8PFPuppi.jec.txt.gz",
        "Summer19UL17_RunE_V5_DATA_L3Absolute_AK8PFPuppi.jec.txt.gz",
        ],path="../data/jec/2017/"
    ),
        "2017RunF": jet_factory_factory(
        files=[
        "Summer19UL17_RunF_V5_DATA_L1FastJet_AK8PFPuppi.jec.txt.gz",
        "Summer19UL17_RunF_V5_DATA_L2Relative_AK8PFPuppi.jec.txt.gz",
        "Summer19UL17_RunF_V5_DATA_L2L3Residual_AK8PFPuppi.jec.txt.gz",
        #"Summer19UL17_RunF_V5_DATA_L2Residual_AK8PFPuppi.jec.txt.gz",
        "Summer19UL17_RunF_V5_DATA_L3Absolute_AK8PFPuppi.jec.txt.gz",
        ],path="../data/jec/2017/"
    ),
        "2018RunA": jet_factory_factory(
        files=[
        "Summer19UL18_RunA_V5_DATA_L1FastJet_AK8PFPuppi.jec.txt.gz",
        "Summer19UL18_RunA_V5_DATA_L2Relative_AK8PFPuppi.jec.txt.gz",
        "Summer19UL18_RunA_V5_DATA_L2L3Residual_AK8PFPuppi.jec.txt.gz",
        #"Summer19UL18_RunA_V5_DATA_L2Residual_AK8PFPuppi.jec.txt.gz",
        "Summer19UL18_RunA_V5_DATA_L3Absolute_AK8PFPuppi.jec.txt.gz",
        ],path="../data/jec/2018/"
    ),
        "2018RunB": jet_factory_factory(
        files=[
        "Summer19UL18_RunB_V5_DATA_L1FastJet_AK8PFPuppi.jec.txt.gz",
        "Summer19UL18_RunB_V5_DATA_L2Relative_AK8PFPuppi.jec.txt.gz",
        "Summer19UL18_RunB_V5_DATA_L2L3Residual_AK8PFPuppi.jec.txt.gz",
        #"Summer19UL18_RunB_V5_DATA_L2Residual_AK8PFPuppi.jec.txt.gz",
        "Summer19UL18_RunB_V5_DATA_L3Absolute_AK8PFPuppi.jec.txt.gz",
        ],path="../data/jec/2018/"
    ),
        "2018RunC": jet_factory_factory(
        files=[
        "Summer19UL18_RunC_V5_DATA_L1FastJet_AK8PFPuppi.jec.txt.gz",
        "Summer19UL18_RunC_V5_DATA_L2Relative_AK8PFPuppi.jec.txt.gz",
        "Summer19UL18_RunC_V5_DATA_L2L3Residual_AK8PFPuppi.jec.txt.gz",
        #"Summer19UL18_RunC_V5_DATA_L2Residual_AK8PFPuppi.jec.txt.gz",
        "Summer19UL18_RunC_V5_DATA_L3Absolute_AK8PFPuppi.jec.txt.gz",
        ],path="../data/jec/2018/"
    ),
        "2018RunD": jet_factory_factory(
        files=[
        "Summer19UL18_RunD_V5_DATA_L1FastJet_AK8PFPuppi.jec.txt.gz",
        "Summer19UL18_RunD_V5_DATA_L2Relative_AK8PFPuppi.jec.txt.gz",
        "Summer19UL18_RunD_V5_DATA_L2L3Residual_AK8PFPuppi.jec.txt.gz",
        #"Summer19UL18_RunD_V5_DATA_L2Residual_AK8PFPuppi.jec.txt.gz",
        "Summer19UL18_RunD_V5_DATA_L3Absolute_AK8PFPuppi.jec.txt.gz",
        ],path="../data/jec/2018/"
    )

}

jet_factory = {    
    "2016APVmc": jet_factory_factory(
        files=[
            "Summer19UL16APV_V7_MC_L1FastJet_AK4PFchs.jec.txt.gz",
            "Summer19UL16APV_V7_MC_L2Relative_AK4PFchs.jec.txt.gz",
            "Summer19UL16APV_V7_MC_L2L3Residual_AK4PFchs.jec.txt.gz",
            #"Summer19UL16APV_V7_MC_L2Residual_AK4PFchs.jec.txt.gz", #This one can actually be included, but does not affect result!
            "Summer19UL16APV_V7_MC_L3Absolute_AK4PFchs.jec.txt.gz",
            "Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.junc.txt.gz",
            "Summer19UL16APV_V7_MC_UncertaintySources_AK4PFchs.junc.txt.gz",
            "Summer20UL16APV_JRV3_MC_PtResolution_AK4PFchs.jr.txt.gz",
            "Summer20UL16APV_JRV3_MC_SF_AK4PFchs.jersf.txt.gz"
        ],path="../data/jec/2016APV/"
    ),
        "2016mc": jet_factory_factory(
        files=[
            "Summer19UL16_V7_MC_L1FastJet_AK4PFchs.jec.txt.gz",
            "Summer19UL16_V7_MC_L2Relative_AK4PFchs.jec.txt.gz",
            "Summer19UL16_V7_MC_L2L3Residual_AK4PFchs.jec.txt.gz",
            #"Summer19UL16_V7_MC_L2Residual_AK4PFchs.jec.txt.gz", #This one can actually be included, but does not affect result!
            "Summer19UL16_V7_MC_L3Absolute_AK4PFchs.jec.txt.gz",
            "Summer19UL16_V7_MC_Uncertainty_AK4PFchs.junc.txt.gz",
            "Summer19UL16_V7_MC_UncertaintySources_AK4PFchs.junc.txt.gz",
            "Summer20UL16_JRV3_MC_PtResolution_AK4PFchs.jr.txt.gz",
            "Summer20UL16_JRV3_MC_SF_AK4PFchs.jersf.txt.gz"
        ],path="../data/jec/2016/"
    ),
        "2017mc": jet_factory_factory(
        files=[
            "Summer19UL17_V5_MC_L1FastJet_AK4PFchs.jec.txt.gz",
            "Summer19UL17_V5_MC_L2Relative_AK4PFchs.jec.txt.gz",
            "Summer19UL17_V5_MC_L2L3Residual_AK4PFchs.jec.txt.gz",
            #"Summer19UL17_V5_MC_L2Residual_AK4PFchs.jec.txt.gz", #This one can actually be included, but does not affect result!
            "Summer19UL17_V5_MC_L3Absolute_AK4PFchs.jec.txt.gz",
            "Summer19UL17_V5_MC_Uncertainty_AK4PFchs.junc.txt.gz",
            "Summer19UL17_V5_MC_UncertaintySources_AK4PFchs.junc.txt.gz",
            "Summer19UL17_JRV3_MC_PtResolution_AK4PFchs.jr.txt.gz",
            "Summer19UL17_JRV3_MC_SF_AK4PFchs.jersf.txt.gz"
        ],path="../data/jec/2017/"
    ),
        "2018mc": jet_factory_factory(
        files=[
        "Summer19UL18_V5_MC_L1FastJet_AK4PFchs.jec.txt.gz",
        "Summer19UL18_V5_MC_L2Relative_AK4PFchs.jec.txt.gz",
        "Summer19UL18_V5_MC_L2L3Residual_AK4PFchs.jec.txt.gz",
        #"Summer19UL18_V5_MC_L2Residual_AK4PFchs.jec.txt.gz", #This one can actually be included, but does not affect result!
        "Summer19UL18_V5_MC_L3Absolute_AK4PFchs.jec.txt.gz",
        "Summer19UL18_V5_MC_Uncertainty_AK4PFchs.junc.txt.gz",
        "Summer19UL18_V5_MC_UncertaintySources_AK4PFchs.junc.txt.gz",
        "Summer19UL18_JRV2_MC_PtResolution_AK4PFchs.jr.txt.gz",
        "Summer19UL18_JRV2_MC_SF_AK4PFchs.jersf.txt.gz"

        ],path="../data/jec/2018/"
    ),
        "2016APVRunBCD": jet_factory_factory(
        files=[
        "Summer19UL16APV_RunBCD_V7_DATA_L1FastJet_AK4PFchs.jec.txt.gz",
        "Summer19UL16APV_RunBCD_V7_DATA_L2Relative_AK4PFchs.jec.txt.gz",
        "Summer19UL16APV_RunBCD_V7_DATA_L2L3Residual_AK4PFchs.jec.txt.gz",
        #"Summer19UL16APV_RunBCD_V7_DATA_L2Residual_AK4PFchs.jec.txt.gz",
        "Summer19UL16APV_RunBCD_V7_DATA_L3Absolute_AK4PFchs.jec.txt.gz",
        ],path="../data/jec/2016APV/"
    ),
        "2016APVRunEF": jet_factory_factory(
        files=[
        "Summer19UL16APV_RunEF_V7_DATA_L1FastJet_AK4PFchs.jec.txt.gz",
        "Summer19UL16APV_RunEF_V7_DATA_L2Relative_AK4PFchs.jec.txt.gz",
        "Summer19UL16APV_RunEF_V7_DATA_L2L3Residual_AK4PFchs.jec.txt.gz",
        #"Summer19UL16APV_RunEF_V7_DATA_L2Residual_AK4PFchs.jec.txt.gz",
        "Summer19UL16APV_RunEF_V7_DATA_L3Absolute_AK4PFchs.jec.txt.gz",
        ],path="../data/jec/2016APV/"
    ),
        "2016RunFGH": jet_factory_factory(
        files=[
        "Summer19UL16_RunFGH_V7_DATA_L1FastJet_AK4PFchs.jec.txt.gz",
        "Summer19UL16_RunFGH_V7_DATA_L2Relative_AK4PFchs.jec.txt.gz",
        "Summer19UL16_RunFGH_V7_DATA_L2L3Residual_AK4PFchs.jec.txt.gz",
        #"Summer19UL16_RunFGH_V7_DATA_L2Residual_AK4PFchs.jec.txt.gz",
        "Summer19UL16_RunFGH_V7_DATA_L3Absolute_AK4PFchs.jec.txt.gz",
        ],path="../data/jec/2016/"
    ),
        "2017RunB": jet_factory_factory(
        files=[
        "Summer19UL17_RunB_V5_DATA_L1FastJet_AK4PFchs.jec.txt.gz",
        "Summer19UL17_RunB_V5_DATA_L2Relative_AK4PFchs.jec.txt.gz",
        "Summer19UL17_RunB_V5_DATA_L2L3Residual_AK4PFchs.jec.txt.gz",
        #"Summer19UL17_RunB_V5_DATA_L2Residual_AK4PFchs.jec.txt.gz",
        "Summer19UL17_RunB_V5_DATA_L3Absolute_AK4PFchs.jec.txt.gz",
        ],path="../data/jec/2017/"
    ),
        "2017RunC": jet_factory_factory(
        files=[
        "Summer19UL17_RunC_V5_DATA_L1FastJet_AK4PFchs.jec.txt.gz",
        "Summer19UL17_RunC_V5_DATA_L2Relative_AK4PFchs.jec.txt.gz",
        "Summer19UL17_RunC_V5_DATA_L2L3Residual_AK4PFchs.jec.txt.gz",
        #"Summer19UL17_RunC_V5_DATA_L2Residual_AK4PFchs.jec.txt.gz",
        "Summer19UL17_RunC_V5_DATA_L3Absolute_AK4PFchs.jec.txt.gz",
        ],path="../data/jec/2017/"
    ),
        "2017RunD": jet_factory_factory(
        files=[
        "Summer19UL17_RunD_V5_DATA_L1FastJet_AK4PFchs.jec.txt.gz",
        "Summer19UL17_RunD_V5_DATA_L2Relative_AK4PFchs.jec.txt.gz",
        "Summer19UL17_RunD_V5_DATA_L2L3Residual_AK4PFchs.jec.txt.gz",
        #"Summer19UL17_RunD_V5_DATA_L2Residual_AK4PFchs.jec.txt.gz",
        "Summer19UL17_RunD_V5_DATA_L3Absolute_AK4PFchs.jec.txt.gz",
        ],path="../data/jec/2017/"
    ),
        "2017RunE": jet_factory_factory(
        files=[
        "Summer19UL17_RunE_V5_DATA_L1FastJet_AK4PFchs.jec.txt.gz",
        "Summer19UL17_RunE_V5_DATA_L2Relative_AK4PFchs.jec.txt.gz",
        "Summer19UL17_RunE_V5_DATA_L2L3Residual_AK4PFchs.jec.txt.gz",
        #"Summer19UL17_RunE_V5_DATA_L2Residual_AK4PFchs.jec.txt.gz",
        "Summer19UL17_RunE_V5_DATA_L3Absolute_AK4PFchs.jec.txt.gz",
        ],path="../data/jec/2017/"
    ),
        "2017RunF": jet_factory_factory(
        files=[
        "Summer19UL17_RunF_V5_DATA_L1FastJet_AK4PFchs.jec.txt.gz",
        "Summer19UL17_RunF_V5_DATA_L2Relative_AK4PFchs.jec.txt.gz",
        "Summer19UL17_RunF_V5_DATA_L2L3Residual_AK4PFchs.jec.txt.gz",
        #"Summer19UL17_RunF_V5_DATA_L2Residual_AK4PFchs.jec.txt.gz",
        "Summer19UL17_RunF_V5_DATA_L3Absolute_AK4PFchs.jec.txt.gz",
        ],path="../data/jec/2017/"
    ),
        "2018RunA": jet_factory_factory(
        files=[
        "Summer19UL18_RunA_V5_DATA_L1FastJet_AK4PFchs.jec.txt.gz",
        "Summer19UL18_RunA_V5_DATA_L2Relative_AK4PFchs.jec.txt.gz",
        "Summer19UL18_RunA_V5_DATA_L2L3Residual_AK4PFchs.jec.txt.gz",
        #"Summer19UL18_RunA_V5_DATA_L2Residual_AK4PFchs.jec.txt.gz",
        "Summer19UL18_RunA_V5_DATA_L3Absolute_AK4PFchs.jec.txt.gz",
        ],path="../data/jec/2018/"
    ),
        "2018RunB": jet_factory_factory(
        files=[
        "Summer19UL18_RunB_V5_DATA_L1FastJet_AK4PFchs.jec.txt.gz",
        "Summer19UL18_RunB_V5_DATA_L2Relative_AK4PFchs.jec.txt.gz",
        "Summer19UL18_RunB_V5_DATA_L2L3Residual_AK4PFchs.jec.txt.gz",
        #"Summer19UL18_RunB_V5_DATA_L2Residual_AK4PFchs.jec.txt.gz",
        "Summer19UL18_RunB_V5_DATA_L3Absolute_AK4PFchs.jec.txt.gz",
        ],path="../data/jec/2018/"
    ),
        "2018RunC": jet_factory_factory(
        files=[
        "Summer19UL18_RunC_V5_DATA_L1FastJet_AK4PFchs.jec.txt.gz",
        "Summer19UL18_RunC_V5_DATA_L2Relative_AK4PFchs.jec.txt.gz",
        "Summer19UL18_RunC_V5_DATA_L2L3Residual_AK4PFchs.jec.txt.gz",
        #"Summer19UL18_RunC_V5_DATA_L2Residual_AK4PFchs.jec.txt.gz",
        "Summer19UL18_RunC_V5_DATA_L3Absolute_AK4PFchs.jec.txt.gz",
        ],path="../data/jec/2018/"
    ),
        "2018RunD": jet_factory_factory(
        files=[
        "Summer19UL18_RunD_V5_DATA_L1FastJet_AK4PFchs.jec.txt.gz",
        "Summer19UL18_RunD_V5_DATA_L2Relative_AK4PFchs.jec.txt.gz",
        "Summer19UL18_RunD_V5_DATA_L2L3Residual_AK4PFchs.jec.txt.gz",
        #"Summer19UL18_RunD_V5_DATA_L2Residual_AK4PFchs.jec.txt.gz",
        "Summer19UL18_RunD_V5_DATA_L3Absolute_AK4PFchs.jec.txt.gz",
        ],path="../data/jec/2018/"
    )
}

if __name__ == "__main__":
    oFile = "../data/jec/jme_UL_pickled.pkl"
    with gzip.open(oFile, "wb") as fout:
        cloudpickle.dump(
            {
                "fatjet_factory": fatjet_factory,
                "jet_factory"   : jet_factory,
            },
            fout
        )
    print("Created:", oFile)