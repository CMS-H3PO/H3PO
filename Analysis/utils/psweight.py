import awkward as ak
import numpy as np


def add_ps_weights(events, weights):
    """
    Parton shower weights (ISR and FSR)
    """
    nom = ak.ones_like(weights.weight())

    isr_up = ak.ones_like(nom)
    isr_dn = ak.ones_like(nom)
    fsr_up = ak.ones_like(nom)
    fsr_dn = ak.ones_like(nom)

    ps_weights = events.PSWeight

    if ak.num(ps_weights[0], axis=0) == 4:
        isr_up = ps_weights[:, 0]  # ISR=2,   FSR=1
        isr_dn = ps_weights[:, 2]  # ISR=0.5, FSR=1

        fsr_up = ps_weights[:, 1]  # ISR=1, FSR=2
        fsr_dn = ps_weights[:, 3]  # ISR=1, FSR=0.5

    weights.add(
        name="ISRPartonShower",
        weight=nom,
        weightUp=isr_up,
        weightDown=isr_dn
    )
    
    weights.add(
        name="FSRPartonShower",
        weight=nom,
        weightUp=fsr_up,
        weightDown=fsr_dn
    )
