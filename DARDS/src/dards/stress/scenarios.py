# E1 = .
# Macro stress scenario library.
# Defines deterministic transformations of MarketSnapshot
# representing historically plausible macro shocks.

from copy import deepcopy
from dards.types import MarketSnapshot


def gfc_2008(snapshot: MarketSnapshot) -> MarketSnapshot:
    """
    Equity collapse, duration rally, correlation inversion.
    """
    s = deepcopy(snapshot)

    s.returns["SPY"] = -0.05
    s.returns["TLT"] = 0.03

    s.vol["SPY"] = s.vol.get("SPY",0.15) * 2.0
    s.vol["TLT"] = s.vol.get("TLT",0.10) * 1.5

    s.corr[("SPY","TLT")] = -0.6
    s.corr[("TLT","SPY")] = -0.6

    return s


def covid_crash(snapshot: MarketSnapshot) -> MarketSnapshot:
    """
    Fast equity crash with volatility spike.
    """
    s = deepcopy(snapshot)

    s.returns["SPY"] = -0.08
    s.returns["TLT"] = 0.02

    s.vol["SPY"] = s.vol.get("SPY",0.15) * 3.0
    s.vol["TLT"] = s.vol.get("TLT",0.10) * 1.8

    return s


def rate_shock(snapshot: MarketSnapshot) -> MarketSnapshot:
    """
    Bond selloff, equity wobble, positive correlation regime.
    """
    s = deepcopy(snapshot)

    s.returns["SPY"] = -0.02
    s.returns["TLT"] = -0.04

    s.corr[("SPY","TLT")] = 0.4
    s.corr[("TLT","SPY")] = 0.4

    s.vol["TLT"] = s.vol.get("TLT",0.10) * 2.2

    return s


def stagflation(snapshot: MarketSnapshot) -> MarketSnapshot:
    """
    Both equities and bonds under pressure.
    """
    s = deepcopy(snapshot)

    s.returns["SPY"] = -0.03
    s.returns["TLT"] = -0.03

    s.vol["SPY"] = s.vol.get("SPY",0.15) * 1.7
    s.vol["TLT"] = s.vol.get("TLT",0.10) * 1.6

    s.corr[("SPY","TLT")] = 0.2
    s.corr[("TLT","SPY")] = 0.2

    return s


SCENARIOS = {
    "gfc_2008": gfc_2008,
    "covid_crash": covid_crash,
    "rate_shock": rate_shock,
    "stagflation": stagflation,
}