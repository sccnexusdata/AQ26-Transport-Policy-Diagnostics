from __future__ import annotations

import hashlib
import json
from pathlib import Path


class EvidenceValidationError(RuntimeError):
    """Raised when an upstream AQ26 evidence package cannot be trusted."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest(path: Path) -> dict:
    if not path.is_file():
        raise EvidenceValidationError(f"Parent manifest missing: {path}")
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvidenceValidationError(f"Parent manifest is unreadable: {exc}") from exc
    if not isinstance(manifest, dict):
        raise EvidenceValidationError("Parent manifest must be a JSON object")
    return manifest


def verify_manifest(bundle_dir: Path, manifest: dict) -> dict[str, str]:
    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        raise EvidenceValidationError("Parent manifest contains no governed files")

    verified: dict[str, str] = {}
    for entry in files:
        if not isinstance(entry, dict):
            raise EvidenceValidationError("Invalid parent manifest file entry")
        relative = entry.get("path")
        expected = str(entry.get("sha256") or "").lower()
        if not relative or len(expected) != 64:
            raise EvidenceValidationError("Manifest file entry lacks path or SHA-256")
        candidate = (bundle_dir / relative).resolve()
        try:
            candidate.relative_to(bundle_dir.resolve())
        except ValueError as exc:
            raise EvidenceValidationError(f"Manifest path escapes evidence bundle: {relative}") from exc
        if not candidate.is_file():
            raise EvidenceValidationError(f"Governed evidence file missing: {relative}")
        actual = sha256_file(candidate)
        if actual != expected:
            raise EvidenceValidationError(f"SHA-256 mismatch for {relative}")
        verified[str(relative)] = actual
    return verified
