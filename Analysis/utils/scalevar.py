import awkward as ak


def add_scalevar_7pt(events, weights):
    """
    Renormalization and factorization scale variations (0.5, 1.0, 2.0) for the scales varied independently
    excluding the extreme opposite combinations (muR=0.5, muF=2.0 and muR=2.0, muF=0.5)
    """
    nom = ak.ones_like(weights.weight())
    up  = ak.ones_like(nom)
    dn  = ak.ones_like(nom)

    lhe_weights = getattr(events, "LHEScaleWeight", None)

    if lhe_weights is None:
        weights.add('scalevar_7pt', nom)
        return
 
    try:
        # signal samples drop the nominal case (muR=1.0, muF=1.0)
        if len(lhe_weights[0])==8:
            selected = lhe_weights[:, [0, # muR=0.5, muF=0.5
                                      1,  # muR=0.5, muF=1.0
                                      #2,  # muR=0.5, muF=2.0
                                      3,  # muR=1.0, muF=0.5
                                      4,  # muR=1.0, muF=2.0
                                      #5,  # muR=2.0, muF=0.5
                                      6,  # muR=2.0, muF=1.0
                                      7]] # muR=2.0, muF=2.0
        else:
            selected = lhe_weights[:, [0, # muR=0.5, muF=0.5
                                      1,  # muR=0.5, muF=1.0
                                      #2,  # muR=0.5, muF=2.0
                                      3,  # muR=1.0, muF=0.5
                                      #4,  # muR=1.0, muF=1.0
                                      5,  # muR=1.0, muF=2.0
                                      #6,  # muR=2.0, muF=0.5
                                      7,  # muR=2.0, muF=1.0
                                      8]] # muR=2.0, muF=2.0
        up = ak.max(selected, axis=1)
        dn = ak.min(selected, axis=1)
    except Exception as e:
        print("Scale variation structure unexpected:", e)
        print("Scale variation vector has length ", len(lhe_weights[0]))

    weights.add(
        name='scalevar_7pt',
        weight=nom,
        weightUp=up,
        weightDown=dn
    )


def add_scalevar_3pt(events, weights):
    """
    Renormalization and factorization scale variations (0.5, 1.0, 2.0) for the scales varied together (muR = muF)
    """
    nom = ak.ones_like(weights.weight())
    up  = ak.ones_like(nom)
    dn  = ak.ones_like(nom)

    lhe_weights = getattr(events, "LHEScaleWeight", None)

    if lhe_weights is None:
        weights.add('scalevar_3pt', nom)
        return

    try:
        # signal samples drop the nominal case (muR=1.0, muF=1.0)
        if len(lhe_weights[0])==8:
            selected = lhe_weights[:, [0, # muR=0.5, muF=0.5
                                      7]] # muR=2.0, muF=2.0
        else:      
            selected = lhe_weights[:, [0, # muR=0.5, muF=0.5
                                      #4,  # muR=1.0, muF=1.0
                                      8]] # muR=2.0, muF=2.0
        up = ak.max(selected, axis=1)
        dn = ak.min(selected, axis=1)
    except Exception as e:
        print("Scale variation structure unexpected:", e)

    weights.add(
        name='scalevar_3pt',
        weight=nom,
        weightUp=up,
        weightDown=dn
    )
