import correctionlib
import os

#years = ["2016APV_2016"]
#years = ["2017_2018"]
years = ["2016APV_2016", "2017_2018"]
#channels = ["boosted"]
#channels = ["semiboosted"]
channels = ["boosted", "semiboosted"]

for year in years:
    for channel in channels:
        cset = correctionlib.CorrectionSet.from_file(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../data/trigger/trigger_sf_{year}.json")
        )

        sf_cset = f"trigger_efficiency_sf_{year}_{channel}"
        print("\nSF set:", sf_cset)

        sf = cset[sf_cset]

        pts = [500.0, 800.0, 1000.0, 1500.0, 2500.0, 3000.0]

        for pt in pts:
            sf_nominal = sf.evaluate(pt, "nominal")
            sf_up      = sf.evaluate(pt, "up")
            sf_down    = sf.evaluate(pt, "down")

            print("\npT:", pt)
            print("Nominal:", sf_nominal)
            print("Up:", sf_up)
            print("Down:", sf_down)
