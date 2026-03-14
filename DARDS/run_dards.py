# G1 = --.
# DARDS system entrypoint.
# Executes the full decision pipeline, rolling backtest,
# performance reporting, stress harness and run archiving.

import sys
from pathlib import Path

# Ensure src-layout imports work when running as script
sys.path.append(str(Path(__file__).resolve().parent / "src"))

from datetime import datetime, timezone
from pprint import pprint

from dards.data.mock_provider import MockMarketDataProvider
from dards.data.mock_corr import build_mock_correlation
from dards.data.validators import validate_snapshot
from dards.data.assembler import assemble_snapshot

from dards.engine.decision import form_decision
from dards.engine.pipeline import run_pipeline
from dards.engine.backtest import run_backtest

from dards.reporting.performance_report import build_performance_report
from dards.reporting.desk_brief import build_desk_brief
from dards.reporting.run_archive import save_run_archive

from dards.stress.runner import run_stress


def build_snapshot():
    """
    Constructs a validated MarketSnapshot from the mock environment.
    Simulates a single decision timestamp.
    """

    provider = MockMarketDataProvider()
    corr = build_mock_correlation()

    decision_time = datetime.now(timezone.utc)

    raw = provider.load_snapshot(decision_time)
    validate_snapshot(raw)

    return assemble_snapshot(decision_time, raw, corr)


def run_current_decision(snapshot):
    """
    Runs decision + allocation for the current snapshot.
    """

    decision = form_decision(snapshot)
    weights, risk_scale = run_pipeline(snapshot)

    print("\n=== DARDS CURRENT DECISION ===")

    pprint({
        "asof": str(snapshot.asof),
        "posture": decision.posture,
        "risk_stance": decision.risk_stance,
        "confidence": decision.confidence,
        "weights": weights,
        "risk_scale": risk_scale,
    })

    print("\n=== DESK BRIEF ===")
    print(build_desk_brief(decision))

    return decision, weights, risk_scale


def run_backtest_block():
    """
    Runs rolling capital simulation.
    """

    snapshots = [build_snapshot() for _ in range(30)]

    results = run_backtest(snapshots)
    report = build_performance_report(results)

    print("\n=== DARDS PERFORMANCE REPORT ===")
    pprint(report)

    return report


def run_stress_block(snapshot):
    """
    Executes macro shock scenarios.
    """

    stress_results = run_stress(snapshot)

    print("\n=== DARDS STRESS HARNESS ===")
    pprint(stress_results)

    return stress_results


def main():

    snapshot = build_snapshot()

    decision, weights, risk_scale = run_current_decision(snapshot)

    report = run_backtest_block()

    stress_results = run_stress_block(snapshot)

    # --- archive experiment run ---
    archive_data = {
        "timestamp": str(datetime.now(timezone.utc)),
        "decision": decision.expression,
        "weights": weights,
        "risk_scale": risk_scale,
        "performance_report": report,
        "stress_results": stress_results,
    }

    path = save_run_archive(archive_data)

    print("\n=== RUN ARCHIVED ===")
    print(path)


if __name__ == "__main__":
    main()