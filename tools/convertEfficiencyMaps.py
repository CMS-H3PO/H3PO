# written by ChatGPT

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Callable

import math
import ROOT

import correctionlib
import correctionlib.schemav2 as cs


# ============================================================================
# Configuration
# ============================================================================

@dataclass
class EfficiencyMapConfig:

    # ------------------------------------------------------------------------
    # ROOT input
    # ------------------------------------------------------------------------

    root_file: str

    numerator_hist: str
    denominator_hist: str

    # ------------------------------------------------------------------------
    # correctionlib metadata
    # ------------------------------------------------------------------------

    correction_name: str = "efficiency"

    description: str = (
        "MC tagging efficiency"
    )

    version: int = 1

    # ------------------------------------------------------------------------
    # Input variable corresponding to ROOT X axis
    # ------------------------------------------------------------------------

    x_name: str = "eta"

    x_type: str = "real"

    x_description: str = (
        "Jet pseudorapidity"
    )

    # ------------------------------------------------------------------------
    # Input variable corresponding to ROOT Y axis
    # ------------------------------------------------------------------------

    y_name: str = "pt"

    y_type: str = "real"

    y_description: str = (
        "Jet transverse momentum [GeV]"
    )

    # ------------------------------------------------------------------------
    # Systematic input
    # ------------------------------------------------------------------------

    systematic_name: str = "systematic"

    systematic_description: str = (
        "Efficiency variation"
    )

    nominal_label: str = "nominal"
    stat_up_label: str = "statUp"
    stat_down_label: str = "statDown"

    # ------------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------------

    output_name: str = "efficiency"

    output_type: str = "real"

    output_description: str = (
        "MC tagging efficiency"
    )

    # ------------------------------------------------------------------------
    # Under/overflow treatment
    #
    # "error"
    # "clamp"
    # ------------------------------------------------------------------------

    flow: str = "error"

    # ------------------------------------------------------------------------
    # Empty bins
    # ------------------------------------------------------------------------

    allow_empty_bins: bool = False

    # ------------------------------------------------------------------------
    # Efficiency validation
    # ------------------------------------------------------------------------

    validate_efficiency: bool = True

    efficiency_min: float = 0.0
    efficiency_max: float = 1.0

    # ------------------------------------------------------------------------
    # Treatment of statistical variations
    #
    # If True:
    #
    #   statUp   = min(eff + sigma, 1)
    #   statDown = max(eff - sigma, 0)
    #
    # If False, the raw Gaussian variations are stored.
    # ------------------------------------------------------------------------

    clip_variations: bool = True

    # ------------------------------------------------------------------------
    # Statistical uncertainty calculation
    #
    # If numerator_is_subset=True:
    #
    #   Cov(N,D) = Sumw2_num
    #
    # If False:
    #
    #   Cov(N,D) = 0
    #
    # The former is the appropriate choice when numerator is literally
    # obtained by selecting a subset of the events entering denominator.
    # ------------------------------------------------------------------------

    numerator_is_subset: bool = True
    
    # ------------------------------------------------------------------------
    # Verbose printout
    # ------------------------------------------------------------------------

    verbose: bool = False


# ============================================================================
# ROOT helpers
# ============================================================================

def open_histogram(
    root_file: str,
    histogram_name: str,
):
    """
    Read a ROOT histogram and detach it from the file.
    """

    root_file_obj = ROOT.TFile.Open(root_file)

    if not root_file_obj or root_file_obj.IsZombie():
        raise OSError(
            f"Could not open ROOT file: {root_file}"
        )

    hist = root_file_obj.Get(histogram_name)

    if not hist:
        root_file_obj.Close()

        raise KeyError(
            f"Histogram '{histogram_name}' "
            f"not found in '{root_file}'"
        )

    if not hist.InheritsFrom("TH2"):
        root_file_obj.Close()

        raise TypeError(
            f"'{histogram_name}' is not a TH2"
        )

    # Clone so the histogram survives closing the ROOT file.
    hist = hist.Clone(
        f"{hist.GetName()}_clone"
    )

    hist.SetDirectory(0)

    root_file_obj.Close()

    return hist


def get_edges(axis):
    """
    Return ROOT histogram bin edges.
    """

    n = axis.GetNbins()

    edges = [
        float(axis.GetBinLowEdge(i))
        for i in range(1, n + 1)
    ]

    edges.append(
        float(axis.GetBinUpEdge(n))
    )

    return edges


def check_same_binning(
    numerator,
    denominator,
):
    """
    Verify that numerator and denominator have identical binning.
    """

    nx_num = numerator.GetXaxis().GetNbins()
    ny_num = numerator.GetYaxis().GetNbins()

    nx_den = denominator.GetXaxis().GetNbins()
    ny_den = denominator.GetYaxis().GetNbins()

    if nx_num != nx_den or ny_num != ny_den:
        raise ValueError(
            "Numerator and denominator have "
            "different numbers of bins."
        )

    x_num = get_edges(numerator.GetXaxis())
    x_den = get_edges(denominator.GetXaxis())

    y_num = get_edges(numerator.GetYaxis())
    y_den = get_edges(denominator.GetYaxis())

    if x_num != x_den:
        raise ValueError(
            "Numerator and denominator have "
            "different X-axis binning."
        )

    if y_num != y_den:
        raise ValueError(
            "Numerator and denominator have "
            "different Y-axis binning."
        )


# ============================================================================
# Efficiency calculation
# ============================================================================

def calculate_efficiency(
    numerator: float,
    denominator: float,
    numerator_sumw2: float,
    denominator_sumw2: float,
    numerator_is_subset: bool = True,
):
    """
    Calculate weighted efficiency and its statistical uncertainty.

    epsilon = N / D

    For numerator being a subset of denominator:

        Cov(N,D) = Sumw2_N

    and therefore:

        Var(epsilon)
          = S_N / D^2
          + N^2 S_D / D^4
          - 2 N S_N / D^3

    where

        S_N = sum(w_i^2) for numerator
        S_D = sum(w_i^2) for denominator.

    If numerator_is_subset=False, covariance is assumed to be zero.
    """

    if denominator == 0:
        return None, None

    efficiency = numerator / denominator

    if numerator_is_subset:

        covariance = numerator_sumw2

    else:

        covariance = 0.0

    variance = (
        numerator_sumw2 / denominator**2
        + (
            numerator**2
            * denominator_sumw2
            / denominator**4
        )
        - (
            2.0
            * numerator
            * covariance
            / denominator**3
        )
    )

    # Numerical roundoff can occasionally produce a tiny
    # negative variance.
    variance = max(variance, 0.0)

    uncertainty = math.sqrt(variance)

    return efficiency, uncertainty


# ============================================================================
# Build efficiency maps
# ============================================================================

def build_efficiency_maps(
    numerator,
    denominator,
    config: EfficiencyMapConfig,
):
    """
    Construct nominal, statUp and statDown maps.
    """

    check_same_binning(
        numerator,
        denominator,
    )

    nx = numerator.GetXaxis().GetNbins()
    ny = numerator.GetYaxis().GetNbins()

    nominal = []
    stat_up = []
    stat_down = []

    # Useful for diagnostics.
    uncertainties = []

    for ix in range(1, nx + 1):

        for iy in range(1, ny + 1):

            n = float(
                numerator.GetBinContent(ix, iy)
            )

            d = float(
                denominator.GetBinContent(ix, iy)
            )

            sumw2_n = float(
                numerator.GetBinError(ix, iy)
            ) ** 2

            sumw2_d = float(
                denominator.GetBinError(ix, iy)
            ) ** 2

            # ------------------------------------------------------------
            # Empty bin
            # ------------------------------------------------------------

            if d == 0:

                if config.allow_empty_bins:
                    nominal.append(0.0)
                    stat_up.append(0.0)
                    stat_down.append(0.0)
                    uncertainties.append(0.0)
                    continue

                raise ValueError(
                    f"Zero denominator in bin "
                    f"(x={ix}, y={iy})"
                )

            # ------------------------------------------------------------
            # Efficiency and uncertainty
            # ------------------------------------------------------------

            efficiency, uncertainty = calculate_efficiency(
                numerator=n,
                denominator=d,
                numerator_sumw2=sumw2_n,
                denominator_sumw2=sumw2_d,
                numerator_is_subset=config.numerator_is_subset,
            )

            # ------------------------------------------------------------
            # Validate
            # ------------------------------------------------------------

            if config.validate_efficiency:

                if not (
                    config.efficiency_min
                    <= efficiency
                    <= config.efficiency_max
                ):
                    raise ValueError(
                        f"Efficiency outside allowed range "
                        f"in bin ({ix}, {iy}): "
                        f"{efficiency}"
                    )

            # ------------------------------------------------------------
            # Statistical variations
            # ------------------------------------------------------------

            up = efficiency + uncertainty
            down = efficiency - uncertainty

            if config.clip_variations:

                up = min(
                    up,
                    config.efficiency_max,
                )

                down = max(
                    down,
                    config.efficiency_min,
                )

            # ------------------------------------------------------------
            # Flat correctionlib arrays
            # ------------------------------------------------------------

            nominal.append(float(efficiency))
            stat_up.append(float(up))
            stat_down.append(float(down))
            uncertainties.append(float(uncertainty))

    return (
        nominal,
        stat_up,
        stat_down,
        uncertainties,
    )


# ============================================================================
# Make MultiBinning
# ============================================================================

def make_multibinning(
    config: EfficiencyMapConfig,
    x_edges,
    y_edges,
    content,
):
    """
    Construct a correctionlib MultiBinning node.
    """

    return cs.MultiBinning(
        nodetype="multibinning",

        inputs=[
            config.x_name,
            config.y_name,
        ],

        edges=[
            x_edges,
            y_edges,
        ],

        content=content,

        flow=config.flow,
    )


# ============================================================================
# Build correction
# ============================================================================

def make_correction(
    config: EfficiencyMapConfig,
):
    """
    Construct the complete correctionlib Correction object.
    """

    # ------------------------------------------------------------------------
    # Read histograms
    # ------------------------------------------------------------------------

    numerator = open_histogram(
        config.root_file,
        config.numerator_hist,
    )

    denominator = open_histogram(
        config.root_file,
        config.denominator_hist,
    )

    check_same_binning(
        numerator,
        denominator,
    )

    # ------------------------------------------------------------------------
    # Extract edges
    # ------------------------------------------------------------------------

    x_edges = get_edges(
        numerator.GetXaxis()
    )

    y_edges = get_edges(
        numerator.GetYaxis()
    )

    # ------------------------------------------------------------------------
    # Calculate maps
    # ------------------------------------------------------------------------

    (
        nominal,
        stat_up,
        stat_down,
        uncertainties,
    ) = build_efficiency_maps(
        numerator,
        denominator,
        config,
    )

    # ------------------------------------------------------------------------
    # Construct MultiBinnings
    # ------------------------------------------------------------------------

    nominal_node = make_multibinning(
        config,
        x_edges,
        y_edges,
        nominal,
    )

    stat_up_node = make_multibinning(
        config,
        x_edges,
        y_edges,
        stat_up,
    )

    stat_down_node = make_multibinning(
        config,
        x_edges,
        y_edges,
        stat_down,
    )

    # ------------------------------------------------------------------------
    # Category containing nominal/statUp/statDown
    # ------------------------------------------------------------------------

    systematic_node = cs.Category(
        nodetype="category",

        input=config.systematic_name,

        content=[
            {
                "key": config.nominal_label,
                "value": nominal_node,
            },
            {
                "key": config.stat_up_label,
                "value": stat_up_node,
            },
            {
                "key": config.stat_down_label,
                "value": stat_down_node,
            },
        ],
    )

    # ------------------------------------------------------------------------
    # Input variables
    # ------------------------------------------------------------------------

    x_variable = cs.Variable(
        name=config.x_name,
        type=config.x_type,
        description=config.x_description,
    )

    y_variable = cs.Variable(
        name=config.y_name,
        type=config.y_type,
        description=config.y_description,
    )

    systematic_variable = cs.Variable(
        name=config.systematic_name,
        type="string",
        description=config.systematic_description,
    )

    output_variable = cs.Variable(
        name=config.output_name,
        type=config.output_type,
        description=config.output_description,
    )

    # ------------------------------------------------------------------------
    # Final Correction
    # ------------------------------------------------------------------------

    correction = cs.Correction(
        name=config.correction_name,

        description=config.description,

        version=config.version,

        inputs=[
            x_variable,
            y_variable,
            systematic_variable,
        ],

        output=output_variable,

        data=systematic_node,
    )

    return (
        correction,
        numerator,
        denominator,
        uncertainties,
    )


# ============================================================================
# Write correctionlib JSON
# ============================================================================

def write_json(
    correction,
    output_file: str,
):
    """
    Write correction to a correctionlib JSON file.
    """

    cset = cs.CorrectionSet(
        schema_version=2,
        corrections=[
            correction,
        ],
    )

    output_file = Path(output_file)

    with output_file.open("w") as f:
        f.write(
            cset.model_dump_json(
                indent=2
            )
        )


# ============================================================================
# Validation
# ============================================================================

def validate_json(
    json_file: str,
):
    """
    Reload JSON through correctionlib.
    """

    cset = correctionlib.CorrectionSet.from_file(
        json_file
    )

    return cset


def validate_against_root(
    correction,
    numerator,
    denominator,
    config: EfficiencyMapConfig,
    tolerance: float = 1e-12,
):
    """
    Compare correctionlib nominal efficiency against
    the efficiency calculated directly from ROOT histograms.
    """

    xaxis = numerator.GetXaxis()
    yaxis = numerator.GetYaxis()

    nx = xaxis.GetNbins()
    ny = yaxis.GetNbins()

    max_difference = 0.0

    for ix in range(1, nx + 1):

        x = xaxis.GetBinCenter(ix)

        for iy in range(1, ny + 1):

            y = yaxis.GetBinCenter(iy)

            n = numerator.GetBinContent(
                ix,
                iy,
            )

            d = denominator.GetBinContent(
                ix,
                iy,
            )

            if d == 0:
                continue

            expected = n / d

            actual = correction.evaluate(
                x,
                y,
                config.nominal_label,
            )

            difference = abs(
                expected - actual
            )

            max_difference = max(
                max_difference,
                difference,
            )

            if config.verbose:
                print(
                    f"ix={ix}, iy={iy}, "
                    f"eta={x:.1f}, pt={y:.2f}, "
                    f"ROOT={expected:.6f}, "
                    f"JSON={actual:.6f}"
                )

            if difference > tolerance:

                raise RuntimeError(
                    f"ROOT/correctionlib mismatch "
                    f"in bin ({ix}, {iy}): "
                    f"ROOT={expected}, "
                    f"JSON={actual}"
                )

    return max_difference


# ============================================================================
# High-level interface
# ============================================================================

def convert_efficiency_map(
    config: EfficiencyMapConfig,
    output_file: str,
):
    """
    Complete conversion:
        ROOT numerator + denominator
            ->
        correctionlib JSON
    """

    (
        correction,
        numerator,
        denominator,
        uncertainties,
    ) = make_correction(config)

    # ------------------------------------------------------------------------
    # Write JSON
    # ------------------------------------------------------------------------

    write_json(
        correction,
        output_file,
    )

    # ------------------------------------------------------------------------
    # Reload JSON
    # ------------------------------------------------------------------------

    cset = validate_json(
        output_file
    )

    correction_from_json = cset[
        config.correction_name
    ]

    # ------------------------------------------------------------------------
    # Validate nominal values
    # ------------------------------------------------------------------------

    max_difference = validate_against_root(
        correction_from_json,
        numerator,
        denominator,
        config,
    )

    # ------------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------------

    max_uncertainty = max(uncertainties)

    print(
        f"Created: {output_file}"
    )

    print(
        f"Correction: {config.correction_name}"
    )

    print(
        f"Maximum ROOT/JSON difference: "
        f"{max_difference:.3e}"
    )

    print(
        f"Maximum MC statistical uncertainty: "
        f"{max_uncertainty:.6g}"
    )

    return cset 


# main routine
def main():
  
    years =   ["2016APV", "2016", "2017", "2018"]
    regions = ["SR", "VR"]

    for year in years:
        for region in regions:
            config = EfficiencyMapConfig(

                root_file=f"ak8_eta_pt_xbbTagEff_{year}_{region}_XToYHTo6B.root",

                numerator_hist=f"ak8_eta_pt_xbbTagEff_{year}_{region}_XToYHTo6B_num",

                denominator_hist=f"ak8_eta_pt_xbbTagEff_{year}_{region}_XToYHTo6B_den",

                correction_name=f"xbbtag_particleNetMD_XbbvsQCD_eff_{year}_{region}_XToYHTo6B",

                description=(
                    "ParticleNet Xbb MC tagging efficiency "
                    "for Run 2 simulation of XToYHTo6B"
                ),

                version=1,

                x_name="eta",
                x_description="Jet pseudorapidity",

                y_name="pt",
                y_description="Jet transverse momentum [GeV]",

                systematic_name="systematic",

                output_name="efficiency",

                # Fail loudly if a jet is outside the map.
                #flow="error",
                # or simply extrapolate
                flow="clamp",

                # Numerator is a subset of denominator.
                numerator_is_subset=True,

                # Don't silently accept e.g. efficiency = 1.04.
                validate_efficiency=True,

                # Limit statistical variations to physical efficiency range.
                clip_variations=True,

                allow_empty_bins=True,
                
                verbose=False
            )

            convert_efficiency_map(
                config,
                f"xbbtag_particleNetMD_XbbvsQCD_eff_{year}_{region}_XToYHTo6B.json",
            )

if __name__ == '__main__':
    main()
