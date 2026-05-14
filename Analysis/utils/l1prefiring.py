
def add_l1prefiring_weight(events, weights):
    """
    L1 pre-firing weights
    More info: https://twiki.cern.ch/twiki/bin/viewauth/CMS/L1PrefiringWeightRecipe
    """
    weights.add(
        "L1Prefiring",
        weight=events.L1PreFiringWeight.Nom,
        weightUp=events.L1PreFiringWeight.Up,
        weightDown=events.L1PreFiringWeight.Dn,
    )
