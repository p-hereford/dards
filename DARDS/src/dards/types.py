# A = .-
# Core type contracts.
# Defines the structural objects the system reads and produces.
# Everything else in DARDS builds on these primitives.

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Tuple, Literal


# B = -...
# Domain identifiers and categorical decision vocabularies.

Asset = str

Posture = Literal["deploy","neutral","hold_back"]
RiskStance = Literal["risk_on","balanced","risk_off"]
Confidence = Literal["low","medium","high"]


# C = -.-.
# Market state snapshot.
# Represents observed behaviour — not forecasts — at a given point in time.

@dataclass(frozen=True)
class MarketSnapshot:
    asof: datetime
    prices: Dict[Asset,float]
    returns: Dict[Asset,float]
    vol: Dict[Asset,float]
    corr: Dict[Tuple[Asset,Asset],float]


# D = -..
# Decision object.
# Formal output of the engine translating market behaviour into posture,
# risk stance, and implementation-aware expression.

@dataclass(frozen=True)
class Decision:
    asof: datetime
    posture: Posture
    risk_stance: RiskStance
    confidence: Confidence
    expression: str
    tradeoffs: Tuple[str,...]
    key_drivers: Tuple[str,...]
