# Q = --.-
# System integrity tests.
# Verifies that the DARDS pipeline, backtest engine,
# reporting layer and stress harness execute end-to-end.

from datetime import datetime, timezone

from dards.data.mock_provider import MockMarketDataProvider
from dards.data.mock_corr import build_mock_correlation
from dards.data.validators import validate_snapshot
from dards.data.assembler import assemble_snapshot

from dards.engine.pipeline import run_pipeline
from dards.engine.backtest import run_backtest
from dards.reporting.performance_report import build_performance_report
from dards.stress.runner import run_stress


# ---------- helper ----------

def _build_snapshot():
    """
    Builds a validated MarketSnapshot using the mock provider.
    """
    provider = MockMarketDataProvider()
    corr = build_mock_correlation()

    decision_time = datetime.now(timezone.utc)

    raw = provider.load_snapshot(decision_time)
    validate_snapshot(raw)

    snapshot = assemble_snapshot(decision_time, raw, corr)

    return snapshot


# ---------- pipeline test ----------

def test_mock_snapshot_runs():

    snapshot = _build_snapshot()

    weights, scale = run_pipeline(snapshot)

    assert isinstance(weights, dict)
    assert isinstance(scale, float)
    assert len(weights) > 0

    for w in weights.values():
        assert isinstance(w, float)


# ---------- backtest test ----------

def test_backtest_runs():

    snapshots = [_build_snapshot() for _ in range(20)]

    results = run_backtest(snapshots)

    assert len(results["equity"]) == 20
    assert len(results["returns"]) == 20
    assert len(results["drawdown"]) == 20
    assert len(results["risk_scale"]) == 20


# ---------- report test ----------

def test_report_builds():

    snapshots = [_build_snapshot() for _ in range(30)]

    results = run_backtest(snapshots)

    report = build_performance_report(results)

    assert "CAGR" in report
    assert "Max_Drawdown" in report
    assert "Vol_Compliance_Ratio" in report


# ---------- stress harness test ----------

def test_stress_runner():

    snapshot = _build_snapshot()

    results = run_stress(snapshot)

    assert "baseline" in results
    assert "gfc_2008" in results
    assert "covid_crash" in results
    assert "rate_shock" in results
    assert "stagflation" in results