from condor.paths import *


datasets_data = {
  # year
  '2017':
  {
    # process: path
    "JetHT2017B": SKIM_DIR
  , "JetHT2017C": SKIM_DIR
  , "JetHT2017D": SKIM_DIR
  , "JetHT2017E": SKIM_DIR
  , "JetHT2017F": SKIM_DIR
  }
}


datasets_ttbar = {
  # year
  '2017':
  {
    # process: path
    "TTbarHadronic":     SKIM_DIR
  , "TTbarSemileptonic": SKIM_DIR
  }
}


datasets_qcd = {
  # year
  '2017':
  {
    # process: path
    "QCD500":  SKIM_DIR
  , "QCD700":  SKIM_DIR
  , "QCD2000": SKIM_DIR
  , "QCD1000": SKIM_DIR
  , "QCD1500": SKIM_DIR
  }
}
 

datasets_signal = {
  # year
  '2017':
  {
    # process: path
    "XToYHTo6B_MX-2400_MY-800":  SKIM_DIR
  }
}
  

# add it all up
datasets = datasets_data
for year in datasets:
  datasets[year].update(datasets_ttbar[year])
  datasets[year].update(datasets_qcd[year])
  datasets[year].update(datasets_signal[year])
