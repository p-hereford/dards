# Z = --..
# Synthetic correlation builder.
# Produces a structurally complete symmetric correlation matrix
# for the mock environment.

from typing import Dict, Tuple
import random

from dards.data.universe import OBSERVATION_UNIVERSE


def build_mock_correlation() -> Dict[Tuple[str, str], float]:
    """
    Returns a full symmetric correlation dictionary.

    Diagonal = 1.0
    Off-diagonal = structured random values within realistic macro bands.
    """

    corr: Dict[Tuple[str, str], float] = {}

    assets = list(OBSERVATION_UNIVERSE)

    for i in assets:
        for j in assets:

            if i == j:
                corr[(i, j)] = 1.0
                continue

            # Macro-like correlation structure
            # Equities moderately correlated
            # Equity vs duration mildly negative
            if ("SPY" in i and "TLT" in j) or ("TLT" in i and "SPY" in j):
                value = random.uniform(-0.5, -0.1)
            else:
                value = random.uniform(0.1, 0.6)

            corr[(i, j)] = value

    return corr