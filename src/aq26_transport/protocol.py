from __future__ import annotations

import hashlib
from pathlib import Path

import yaml


class ProtocolValidationError(RuntimeError):
    """Raised when the registered analysis protocol is invalid."""


def protocol_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_protocol(path: Path) -> dict:
    if not path.is_file():
        raise ProtocolValidationError(f"Protocol missing: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ProtocolValidationError("Protocol must be a YAML mapping")
    if data.get("schema") != "aq26_transport_policy_protocol_v1":
        raise ProtocolValidationError("Unsupported protocol schema")
    if data.get("study_period", {}).get("matching_uses_post_intervention_data") is not False:
        raise ProtocolValidationError("Post-intervention data are prohibited during matching")
    controls = data.get("control_selection") or {}
    if controls.get("pre_intervention_only") is not True:
        raise ProtocolValidationError("Control selection must be pre-intervention only")
    if not data.get("interventions"):
        raise ProtocolValidationError("At least one registered intervention is required")
    return data
