# X = -..-
# Execution pipeline.
# Orchestrates snapshot → decision → volatility target → drawdown guard → allocation → turnover control.

from typing import Dict, Tuple

from dards.types import MarketSnapshot
from dards.engine.decision import form_decision
from dards.engine.risk_budget import target_volatility
from dards.engine.vol_allocator import allocate_by_vol_target
from dards.engine.turnover import apply_turnover_control
from dards.engine.drawdown_guard import apply_drawdown_guard
from dards.features.risk_pressure import compute_risk_pressure


def run_pipeline(
    snapshot: MarketSnapshot,
    prev_weights: Dict[str, float] | None = None,
    peak_equity: float = 100.0,
    current_equity: float = 100.0,
    max_turnover: float = 0.25,
) -> Tuple[Dict[str, float], float]:
    """
    Executes full decision chain with drawdown awareness.

    Returns:
        (weights, applied_risk_scale)
    """

    # --- Decision layer ---
    decision = form_decision(snapshot)

    # --- Continuous pressure ---
    pressure = compute_risk_pressure(snapshot)

    # --- Volatility target ---
    base_target_vol = target_volatility(
        pressure=pressure,
        confidence=decision.confidence,
    )

    # --- Drawdown guard ---
    risk_scale, _ = apply_drawdown_guard(
        peak_equity=peak_equity,
        current_equity=current_equity,
    )

    adjusted_target_vol = base_target_vol * risk_scale

    # --- Raw allocation ---
    raw_weights = allocate_by_vol_target(
        snapshot=snapshot,
        decision=decision,
        target_vol=adjusted_target_vol,
    )

    # --- Turnover control ---
    adjusted_weights, _ = apply_turnover_control(
        prev=prev_weights or {},
        new=raw_weights,
        max_turnover=max_turnover,
    )

    return adjusted_weights, risk_scale