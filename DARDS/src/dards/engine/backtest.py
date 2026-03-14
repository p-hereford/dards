# B1 = -...
# Rolling backtest harness.
# Simulates capital evolution through time using the DARDS pipeline.
# Produces equity path, realised returns, drawdown series, realised vol, and vol compliance.

from typing import Dict, List
from dards.types import MarketSnapshot

from dards.engine.pipeline import run_pipeline
from dards.engine.risk_budget import target_volatility
from dards.features.risk_pressure import compute_risk_pressure
from dards.engine.risk_metrics import realised_vol, vol_compliance


def run_backtest(
    snapshots: List[MarketSnapshot],
    initial_capital: float = 100.0,
    max_turnover: float = 0.25,
    vol_window: int = 20,
    annualisation: int = 252,
    vol_tolerance: float = 0.15,
) -> Dict[str, List[float]]:
    """
    Executes DARDS over a sequence of snapshots.

    Returns:
        {
            "equity": [...],
            "returns": [...],
            "drawdown": [...],
            "risk_scale": [...],
            "target_vol": [...],
            "realised_vol": [...],
            "vol_gap": [...],
            "vol_within": [...]
        }
    """

    equity = initial_capital
    peak = initial_capital
    prev_weights: Dict[str, float] = {}

    equity_path: List[float] = []
    returns_path: List[float] = []
    drawdown_path: List[float] = []
    risk_scale_path: List[float] = []

    target_vol_path: List[float] = []
    realised_vol_path: List[float] = []
    vol_gap_path: List[float] = []
    vol_within_path: List[float] = []

    for snapshot in snapshots:

        weights, scale = run_pipeline(
            snapshot=snapshot,
            prev_weights=prev_weights,
            peak_equity=peak,
            current_equity=equity,
            max_turnover=max_turnover,
        )

        # Portfolio return: w · r
        period_return = sum(
            weights.get(a,0.0) * snapshot.returns.get(a,0.0)
            for a in weights
        )

        equity *= (1.0 + period_return)
        peak = max(peak, equity)
        drawdown = (equity / peak) - 1.0

        equity_path.append(equity)
        returns_path.append(period_return)
        drawdown_path.append(drawdown)
        risk_scale_path.append(scale)

        # Target vol for this period (recomputed consistently with pipeline inputs)
        pressure = compute_risk_pressure(snapshot)
        decision = None  # not required for target vol reconstruction here
        # Confidence lives in decision; pipeline already used it. For now, approximate via risk_scale.
        # Institutional note: we will expose confidence explicitly later in reporting.
        # We treat risk_scale=1.0 as normal confidence baseline.
        confidence = "medium" if scale >= 0.5 else "low"
        target = target_volatility(pressure=pressure, confidence=confidence)

        target_vol_path.append(target)

        rv = realised_vol(returns_path, window=vol_window, annualisation=annualisation)
        within, gap = vol_compliance(rv, target, tolerance=vol_tolerance)

        realised_vol_path.append(rv)
        vol_gap_path.append(gap)
        vol_within_path.append(1.0 if within else 0.0)

        prev_weights = weights

    return {
        "equity": equity_path,
        "returns": returns_path,
        "drawdown": drawdown_path,
        "risk_scale": risk_scale_path,
        "target_vol": target_vol_path,
        "realised_vol": realised_vol_path,
        "vol_gap": vol_gap_path,
        "vol_within": vol_within_path,
    }