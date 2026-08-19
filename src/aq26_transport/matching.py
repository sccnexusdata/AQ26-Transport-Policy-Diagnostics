from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class MatchCandidate:
    site_id: str
    site_type: str
    level: float
    trend: float
    traffic_intensity: float | None = None


def _scaled_difference(left: float, right: float, scale: float) -> float:
    return (left - right) / scale if scale else left - right


def distance(
    treated: MatchCandidate,
    control: MatchCandidate,
    *,
    level_scale: float = 1.0,
    trend_scale: float = 1.0,
    traffic_scale: float = 1.0,
) -> float:
    """Deterministic distance using only registered pre-intervention summaries."""
    if treated.site_type != control.site_type:
        return float("inf")
    terms = [
        _scaled_difference(treated.level, control.level, level_scale) ** 2,
        _scaled_difference(treated.trend, control.trend, trend_scale) ** 2,
    ]
    if treated.traffic_intensity is not None and control.traffic_intensity is not None:
        terms.append(
            _scaled_difference(
                treated.traffic_intensity,
                control.traffic_intensity,
                traffic_scale,
            ) ** 2
        )
    return sqrt(sum(terms))


def rank_controls(treated: MatchCandidate, controls: list[MatchCandidate]) -> list[tuple[str, float]]:
    ranked = [(candidate.site_id, distance(treated, candidate)) for candidate in controls]
    return sorted(ranked, key=lambda row: (row[1], row[0]))
