# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Ecosystem audit (`scripts/ecosystem-audit.py`) + Cursor Automation prompts (`.cursor/automations/`); Actions workflow is **manual dispatch only** (no cron).
- Actions budget doc (`docs/ecosystem/actions-budget.md`).
- Benchmark history snapshots (`data/history/`, `scripts/record-benchmark-history.py`) with ratio deltas between ingests.
- Agent-kit sync and release-notes policy (roadmap v1.1.0).
