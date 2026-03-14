# Z = --..
# Desk briefing generator.
# Converts the system decision into a short institutional-style memo.


from dards.types import Decision


def build_desk_brief(decision: Decision) -> str:
    """
    Produces a short desk-style narrative explaining
    the system's current capital posture.
    """

    lines = []

    lines.append("DARDS Capital Posture Brief")
    lines.append("----------------------------------")

    lines.append(f"Posture: {decision.posture}")
    lines.append(f"Risk regime: {decision.risk_stance}")
    lines.append(f"Confidence: {decision.confidence}")

    lines.append("")
    lines.append("Drivers:")

    for d in decision.key_drivers:
        lines.append(f"  • {d}")

    lines.append("")
    lines.append("Interpretation:")
    lines.append(decision.expression)

    lines.append("")
    lines.append("Model trade-offs:")

    for t in decision.tradeoffs:
        lines.append(f"  • {t}")

    return "\n".join(lines)