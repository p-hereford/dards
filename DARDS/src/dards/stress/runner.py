# F1 = ..-.
# Stress runner.
# Executes the DARDS decision pipeline under predefined macro scenarios
# and returns structured JSON-style output suitable for dashboards or APIs.

from typing import Dict

from dards.types import MarketSnapshot
from dards.engine.pipeline import run_pipeline
from dards.features.risk_pressure import compute_risk_pressure
from dards.engine.risk_budget import target_volatility
from dards.engine.decision import form_decision

from dards.stress.scenarios import SCENARIOS


def run_stress(
    snapshot: MarketSnapshot,
    peak_equity: float = 100.0,
    current_equity: float = 100.0,
) -> Dict[str, Dict]:
    """
    Runs all defined stress scenarios against a baseline snapshot.

    Returns structured dictionary suitable for JSON export.
    """

    results: Dict[str, Dict] = {}

    # Baseline decision
    baseline_decision = form_decision(snapshot)
    baseline_pressure = compute_risk_pressure(snapshot)
    baseline_target_vol = target_volatility(
        pressure=baseline_pressure,
        confidence=baseline_decision.confidence,
    )

    baseline_weights, baseline_scale = run_pipeline(
        snapshot,
        peak_equity=peak_equity,
        current_equity=current_equity,
    )

    results["baseline"] = {
        "risk_state": baseline_decision.risk_stance,
        "posture": baseline_decision.posture,
        "confidence": baseline_decision.confidence,
        "target_vol": baseline_target_vol,
        "risk_scale": baseline_scale,
        "weights": baseline_weights,
    }

    # Scenario runs
    for name, scenario in SCENARIOS.items():

        stressed_snapshot = scenario(snapshot)

        decision = form_decision(stressed_snapshot)
        pressure = compute_risk_pressure(stressed_snapshot)

        target_vol = target_volatility(
            pressure=pressure,
            confidence=decision.confidence,
        )

        weights, scale = run_pipeline(
            stressed_snapshot,
            peak_equity=peak_equity,
            current_equity=current_equity,
        )

        results[name] = {
            "risk_state": decision.risk_stance,
            "posture": decision.posture,
            "confidence": decision.confidence,
            "target_vol": target_vol,
            "risk_scale": scale,
            "weights": weights,
        }

    return results