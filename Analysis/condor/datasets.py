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
    "XToYHTo6B_MX-2400_MY-800":   SKIM_DIR
  , "XToYHTo6B_MX-1200_MY-300":   SKIM_DIR
  , "XToYHTo6B_MX-1200_MY-600":   SKIM_DIR
  , "XToYHTo6B_MX-1200_MY-800":   SKIM_DIR
  , "XToYHTo6B_MX-1200_MY-1000":  SKIM_DIR
  , "XToYHTo6B_MX-1500_MY-300":   SKIM_DIR
  , "XToYHTo6B_MX-1500_MY-600":   SKIM_DIR
  , "XToYHTo6B_MX-1500_MY-800":   SKIM_DIR
  , "XToYHTo6B_MX-1500_MY-1000":  SKIM_DIR
  , "XToYHTo6B_MX-1500_MY-1300":  SKIM_DIR
  , "XToYHTo6B_MX-2000_MY-300":   SKIM_DIR
  , "XToYHTo6B_MX-2000_MY-600":   SKIM_DIR
  , "XToYHTo6B_MX-2000_MY-900":   SKIM_DIR
  , "XToYHTo6B_MX-2000_MY-1100":  SKIM_DIR
  , "XToYHTo6B_MX-2000_MY-1300":  SKIM_DIR
  , "XToYHTo6B_MX-2000_MY-1600":  SKIM_DIR
  , "XToYHTo6B_MX-2500_MY-300":   SKIM_DIR
  , "XToYHTo6B_MX-2500_MY-600":   SKIM_DIR
  , "XToYHTo6B_MX-2500_MY-800":   SKIM_DIR
  , "XToYHTo6B_MX-2500_MY-1000":  SKIM_DIR
  , "XToYHTo6B_MX-2500_MY-1300":  SKIM_DIR
  , "XToYHTo6B_MX-2500_MY-1600":  SKIM_DIR
  , "XToYHTo6B_MX-2500_MY-1800":  SKIM_DIR
  , "XToYHTo6B_MX-3000_MY-300":   SKIM_DIR
  , "XToYHTo6B_MX-3000_MY-600":   SKIM_DIR
  , "XToYHTo6B_MX-3000_MY-800":   SKIM_DIR
  , "XToYHTo6B_MX-3000_MY-1000":  SKIM_DIR
  , "XToYHTo6B_MX-3000_MY-1300":  SKIM_DIR
  , "XToYHTo6B_MX-3000_MY-1600":  SKIM_DIR
  , "XToYHTo6B_MX-3000_MY-1800":  SKIM_DIR
  , "XToYHTo6B_MX-3000_MY-2600":  SKIM_DIR
  , "XToYHTo6B_MX-3000_MY-2800":  SKIM_DIR
  , "XToYHTo6B_MX-3500_MY-300":   SKIM_DIR
  , "XToYHTo6B_MX-3500_MY-600":   SKIM_DIR
  , "XToYHTo6B_MX-3500_MY-700":   SKIM_DIR
  , "XToYHTo6B_MX-3500_MY-1100":  SKIM_DIR
  , "XToYHTo6B_MX-3500_MY-1300":  SKIM_DIR
  , "XToYHTo6B_MX-3500_MY-1600":  SKIM_DIR
  , "XToYHTo6B_MX-3500_MY-2000":  SKIM_DIR
  , "XToYHTo6B_MX-3500_MY-2500":  SKIM_DIR
  , "XToYHTo6B_MX-3500_MY-2800":  SKIM_DIR
  , "XToYHTo6B_MX-4000_MY-300":   SKIM_DIR
  , "XToYHTo6B_MX-4000_MY-600":   SKIM_DIR
  , "XToYHTo6B_MX-4000_MY-800":   SKIM_DIR
  , "XToYHTo6B_MX-4000_MY-1000":  SKIM_DIR
  , "XToYHTo6B_MX-4000_MY-1300":  SKIM_DIR
  , "XToYHTo6B_MX-4000_MY-1600":  SKIM_DIR
  , "XToYHTo6B_MX-4000_MY-2000":  SKIM_DIR
  , "XToYHTo6B_MX-4000_MY-2200":  SKIM_DIR
  , "XToYHTo6B_MX-4000_MY-2500":  SKIM_DIR
  , "XToYHTo6B_MX-4000_MY-2800":  SKIM_DIR
  }
}
  

# add it all up
datasets = datasets_data
for year in datasets:
  datasets[year].update(datasets_ttbar[year])
  datasets[year].update(datasets_qcd[year])
  datasets[year].update(datasets_signal[year])
