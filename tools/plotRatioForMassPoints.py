import os


cfg = {
    "2016APV" : ["/users/ferencek/HHH/condor_jobs_XbbEffMaps_2016APV_a50db1b_20260820_124034/fit/", "2016APV"],
    "2016"    : ["/users/ferencek/HHH/condor_jobs_XbbEffMaps_2016_a50db1b_20260820_124100/fit/", "2016"],
    "2017"    : ["/users/ferencek/HHH/condor_jobs_XbbEffMaps_2017_a50db1b_20260820_124116/fit/", "2017"],
    "2018"    : ["/users/ferencek/HHH/condor_jobs_XbbEffMaps_2018_a50db1b_20260820_124128/fit/", "2018"]
}


official_samples_used = [
  (1000, 300), (1000, 600), (1000, 800),
  (1200, 300), (1200, 600), (1200, 800), (1200, 1000),
  (1600, 300), (1600, 600), (1600, 800), (1600, 1000), (1600, 1200), (1600, 1400),
  (2000, 300), (2000, 600), (2000, 800), (2000, 1000), (2000, 1200), (2000, 1600), (2000, 1800),
  (2500, 300), (2500, 600), (2500, 800), (2500, 1000), (2500, 1200), (2500, 1600), (2500, 2000), (2500, 2200), (2500, 2300),
  (3000, 300), (3000, 600), (3000, 800), (3000, 1000), (3000, 1200), (3000, 1600), (3000, 2000), (3000, 2500), (3000, 2800),
  (3500, 300), (3500, 600), (3500, 800), (3500, 1000), (3500, 1200), (3500, 1600), (3500, 2000), (3500, 2500), (3500, 2800), (3500, 3000), (3500, 3300),
  (4000, 300), (4000, 600), (4000, 800), (4000, 1000), (4000, 1200), (4000, 1600), (4000, 2000), (4000, 2500), (4000, 2800), (4000, 3000), (4000, 3500), (4000, 3800)
]


for year in cfg:
    for (mX, mY) in official_samples_used:
        inputFile  = os.path.join( cfg[year][0], f"XToYHTo6B_MX-{mX}_MY-{mY}_Histograms.root" )
        for r in ["SR", "VR"]:
            num = f"fatjet_eta_pt_xbbTag_{r}_*boosted_nominal"
            den = f"fatjet_eta_pt_all_{r}_*boosted_nominal"
            outputFile = os.path.join( cfg[year][1], f"ak8_eta_pt_xbbTagEff_{r}_XToYHTo6B_MX-{mX}_MY-{mY}" )

            cmd = f"python plotRatio.py -i {inputFile} -n {num} -d {den} -o {outputFile} --batch"

            #print(cmd)
            os.system(cmd)
