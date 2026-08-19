# AQ26 Transport Policy Diagnostics

A small, reproducible research layer for testing transport-policy interventions against governed AQ26 evidence.

## Scientific role

This repository does **not** harvest the primary AQ26 evidence base and does not replace the Air Quality England Observatory. It consumes a versioned, validated evidence package produced upstream and performs protocol-defined comparative diagnostics.

The initial registered study is designed to ask whether monitored air-quality trajectories in London diverged from comparable non-intervention locations after ULEZ interventions.

The repository is intentionally narrow:

- no independent air-quality harvesting;
- no social publishing or website deployment;
- no AI-generated scientific conclusions;
- no copied AQ26 secret estate;
- no permanent raw-data archive;
- no causal language beyond what the registered method supports.

## Evidence boundary

AQ26 parent repository → validated immutable research export → hash verification → registered protocol → matched controls → intervention analysis → sensitivity checks → bounded conclusion.

The child analysis must fail closed if the parent evidence manifest is missing or inconsistent, if the registered protocol is invalid, if post-intervention observations leak into control selection, or if minimum analytical checks are not met.

## Initial methods

The v1 scaffold provides deterministic validation and matching primitives for:

- pre-intervention matched controls;
- difference-in-differences preparation;
- interrupted time-series preparation;
- sensitivity-analysis contracts;
- provenance and SHA-256 receipts.

Synthetic-control estimation may be added only after the evidence interface and simpler estimators are validated.

## Credentials

The scientific code requires no API keys. GitHub Actions uses the repository-scoped `GITHUB_TOKEN` supplied automatically by GitHub. A future narrowly scoped `AQ26_PARENT_READ_TOKEN` may be introduced only if private cross-repository evidence retrieval cannot be achieved safely without it.

## Status

Initial research scaffold. No ULEZ effect estimate or causal conclusion has yet been produced.
