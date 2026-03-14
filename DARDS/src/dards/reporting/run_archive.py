# R1 = .-.
# Run archive system.
# Saves each DARDS execution to a timestamped JSON file
# for experiment reproducibility.

import json
from datetime import datetime, timezone
from pathlib import Path


def save_run_archive(data: dict):

    runs_dir = Path("runs")
    runs_dir.mkdir(exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y_%m_%d_%H_%M_%S")

    path = runs_dir / f"dards_run_{timestamp}.json"

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    return path