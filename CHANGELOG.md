# Changelog

All notable public-release changes to this PolyTutor Labs educational packaging
are recorded here.

This project is a **failure-analysis archive** for engineering education.
Entries describe repository, documentation, and packaging work only. They do
not claim live trading success, production readiness, or future results.

## [0.1.0] — 2026-09-09

First PolyTutor Labs public educational release of
`polymarket-bot-graveyard` (version `0.1.0`).

The checkout remains a **historical archive**. Sanitized snapshots under
`bots/` are incomplete by design. There is no live order routing, no wallet
client, and no deploy pipeline in this release.

### PolyTutor transformation

- Educational packaging of the existing open-source graveyard
  ([Hiberius/polymarket-bot-graveyard](https://github.com/Hiberius/polymarket-bot-graveyard)).
- Attribution, disclaimer, and archive-not-product framing added for public
  learners.
- Curriculum identity: failure analysis → lessons learned → engineering
  education.

### Organization

- Repository layout cleaned for study: narrative under `docs/`, sanitized
  snapshots under `bots/01-apex-shadow/`, `bots/02-phantom/`, and
  `bots/03-05-spectrix/`.
- Historical `watchdog.py` stays in the SPECTRIX snapshot (not moved to
  `scripts/` or `src/`).

### Portability

- Snapshot path defaults resolve from the repository (`BOT_DIR`, `PYTHON`,
  `PG_ISREADY`, `BREW`) rather than a developer machine home directory.
- Watchdog **behavior** is unchanged on purpose.

### Security

- `SECURITY.md` policy for secrets, snapshot classification, and private
  advisory reporting.
- `SECURITY_AUDIT.md` is a preserved historical pre-transform audit (not a
  live operations runbook).
- `.env*` gitignored except `.env.example` placeholders.
- `python scripts/security/check_secrets.py` plus CI quality gates.

### Testing

- Quality-infrastructure pytest under `tests/` only (`pytest.ini` excludes
  `bots/`).
- Public quality commands: `pytest`, `python -m compileall`,
  `python scripts/security/check_secrets.py`, markdown lint, offline internal
  link check.
- No suite replays historical bot behavior or reports a trading result.

### Documentation

- Learner docs: getting started, architecture, learning path, experiment
  guide, lessons learned, and watchdog safety.
- Original journey chapters and autopsy retained as historical source.
- `CONTRIBUTING.md` and `DISCLAIMER.md`.

### Release packaging

- No application `package.json` or `pyproject.toml` — this archive is not an
  installable trading product. Version `0.1.0` is recorded in `VERSION` and
  this changelog only.
- Dual license retained: MIT for `bots/`, CC BY 4.0 for writing.
- CI remains archive quality checks with `permissions: contents: read`.
  There is no deploy job.

[0.1.0]: https://github.com/PolyTutor-Labs/polymarket-bot-graveyard/releases/tag/v0.1.0
