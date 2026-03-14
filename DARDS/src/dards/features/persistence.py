# O = ---
# Directional persistence measurement.
# Quantifies whether recent market movement is consistent rather than noisy.

from typing import List


def directional_persistence(returns: List[float]) -> float:
    """
    Measures directional consistency.

    Returns value in [-1, +1]

    +1 → consistently positive
    -1 → consistently negative
     0 → mixed / noisy
    """

    if not returns:
        return 0.0

    positives = sum(1 for r in returns if r > 0)
    negatives = sum(1 for r in returns if r < 0)

    total = positives + negatives

    if total == 0:
        return 0.0

    return (positives - negatives) / total