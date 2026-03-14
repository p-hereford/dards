# D1 = -..
# Institutional performance report.
# Produces PM-style summary metrics from backtest output.

from typing import Dict, List
import math


def _cagr(equity: List[float], periods_per_year: int = 252) -> float:
    if not equity:
        return 0.0

    total_periods = len(equity)
    if total_periods < 2:
        return 0.0

    start = equity[0]
    end = equity[-1]

    if start <= 0:
        return 0.0

    years = total_periods / periods_per_year
    if years <= 0:
        return 0.0

    return (end / start) ** (1.0 / years) - 1.0


def _max_drawdown(drawdown_series: List[float]) -> float:
    if not drawdown_series:
        return 0.0
    return min(drawdown_series)


def _avg(x: List[float]) -> float:
    if not x:
        return 0.0
    return sum(x) / len(x)


def build_performance_report(results: Dict[str, List[float]]) -> Dict[str, float]:
    """
    Converts backtest output into a concise institutional metric set.
    """

    equity = results.get("equity", [])
    returns = results.get("returns", [])
    drawdown = results.get("drawdown", [])
    risk_scale = results.get("risk_scale", [])
    realised_vol = results.get("realised_vol", [])
    vol_within = results.get("vol_within", [])

    report = {
        "CAGR": _cagr(equity),
        "Max_Drawdown": _max_drawdown(drawdown),
        "Average_Risk_Scale": _avg(risk_scale),
        "Average_Realised_Vol": _avg(realised_vol),
        "Vol_Compliance_Ratio": _avg(vol_within),
        "Average_Return": _avg(returns),
    }

    return report
