from pathlib import Path

import pytest

from aq26_transport.evidence import EvidenceValidationError, verify_manifest
from aq26_transport.matching import MatchCandidate, rank_controls
from aq26_transport.protocol import load_protocol, protocol_sha256


ROOT = Path(__file__).resolve().parents[1]


def test_registered_protocol_is_valid_and_hashable():
    path = ROOT / "protocol" / "london-ulez-v1.yml"
    protocol = load_protocol(path)
    assert protocol["status"] == "registered_pre_analysis"
    assert len(protocol_sha256(path)) == 64


def test_missing_governed_evidence_fails_closed(tmp_path):
    manifest = {"files": [{"path": "air_quality.csv", "sha256": "0" * 64}]}
    with pytest.raises(EvidenceValidationError, match="missing"):
        verify_manifest(tmp_path, manifest)


def test_matching_is_site_type_constrained_and_deterministic():
    treated = MatchCandidate("LONDON_A", "roadside", 42.0, -0.5, 30000.0)
    controls = [
        MatchCandidate("CONTROL_B", "roadside", 41.0, -0.45, 29000.0),
        MatchCandidate("CONTROL_A", "roadside", 41.0, -0.45, 29000.0),
        MatchCandidate("BACKGROUND", "urban_background", 42.0, -0.5, 30000.0),
    ]
    ranked = rank_controls(treated, controls)
    assert ranked[0][0] == "CONTROL_A"
    assert ranked[1][0] == "CONTROL_B"
    assert ranked[-1][1] == float("inf")
