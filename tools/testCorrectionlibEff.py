import correctionlib

cset = correctionlib.CorrectionSet.from_file(
    "xbbtag_particleNetMD_XbbvsQCD_eff_2017_SR_XToYHTo6B.json"
)

eff_corr = cset["xbbtag_particleNetMD_XbbvsQCD_eff_2017_SR_XToYHTo6B"]

# ...
# ix=5, iy=60, eta=-0.2, pt=2975.00, ROOT=0.892207, JSON=0.892207
# ix=6, iy=6, eta=0.2, pt=275.00, ROOT=0.561497, JSON=0.561497
# ...
# ix=6, iy=60, eta=0.2, pt=2975.00, ROOT=0.735749, JSON=0.735749
# ix=7, iy=6, eta=0.8, pt=275.00, ROOT=0.537623, JSON=0.537623
# ...

jets_eta = [0.2, 0.2, 0.2, 0.2]
jets_pt =  [150., 275., 2975., 3100.]


eff_nom = eff_corr.evaluate(
    jets_eta,
    jets_pt,
    "nominal",
)

eff_stat_up = eff_corr.evaluate(
    jets_eta,
    jets_pt,
    "statUp",
)

eff_stat_down = eff_corr.evaluate(
    jets_eta,
    jets_pt,
    "statDown",
) 

print(eff_nom)
print(eff_stat_up)
print(eff_stat_down)
