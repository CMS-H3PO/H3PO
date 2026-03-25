import copy


# analysis regions
regions = ["SR_boosted", "VR_boosted", "SR_semiboosted", "VR_semiboosted"]

# selection cuts
cuts =  {
    regions[0]: {"Trigger": True, "Preselection_ge3fj": True, "Mass_cut_SR_boosted": True, "SR_boosted_Pass": True},
    regions[1]: {"Trigger": True, "Preselection_ge3fj": True, "Mass_cut_VR_boosted": True, "VR_boosted_Pass": True},
    regions[2]: {"Trigger": True, "Preselection_ge2fj": True, "Mass_cut_SR_semiboosted": True, "Preselection_jets": True, "Away_jets_SR_semiboosted": True, "Good_dijet_SR_semiboosted": True, "SR_semiboosted_Pass": True},
    regions[3]: {"Trigger": True, "Preselection_ge2fj": True, "Mass_cut_VR_semiboosted": True, "Preselection_jets": True, "Away_jets_VR_semiboosted": True, "Good_dijet_VR_semiboosted": True, "VR_semiboosted_Pass": True},
}

cuts_Pass = cuts

cuts_Fail = copy.deepcopy(cuts_Pass)
for r in ["SR", "VR"]:
    for ch in ["boosted", "semiboosted"]:
        cuts_Fail[f"{r}_{ch}"][f"{r}_{ch}_Pass"] = False

preselection_boosted = {k:v for k, v in list(cuts[regions[0]].items())[0:2]}

preselection_semiboosted = {k:v for k, v in list(cuts[regions[2]].items())[0:2]}
