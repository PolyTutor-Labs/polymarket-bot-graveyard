# Polymarket Bot Graveyard

**PolyTutor Labs · Educational archive**

A failure-analysis archive of six historical Polymarket bot experiments (March–June 2026). The curriculum is **failure analysis → lessons learned → engineering education**.

This repository is a **learning resource**. It is not a live trading service, not a production bot, and not investment advice.

[![CI](https://github.com/PolyTutor-Labs/polymarket-bot-graveyard/actions/workflows/ci.yml/badge.svg)](https://github.com/PolyTutor-Labs/polymarket-bot-graveyard/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Docs: CC BY 4.0](https://img.shields.io/badge/Docs-CC%20BY%204.0-lightgrey.svg)](LICENSE-DOCS)

> Educational packaging of [Hiberius/polymarket-bot-graveyard](https://github.com/Hiberius/polymarket-bot-graveyard).
> Study the experiments. Do not treat the snapshots as a trading desk. See [DISCLAIMER.md](DISCLAIMER.md).

## What this repository is

An **educational archive** of historical implementations that were built, measured, and shut down.

Use it to study:

- how an assumed edge was specified, implemented, and later refuted
- why paper ledgers and self-reported P&L can disagree with a database
- how a calibration gate can refuse to promote a signal that looks like a coin flip
- how operational automation (a local watchdog) can cost more attention than the research question

## What this repository is not

This repository is **not**:

- a production trading platform or live service
- a collection of strategies to run with real funds
- a signal service or investment, legal, or tax advice
- a playbook for extracting an edge from Polymarket

Historical paper, shadow, and live figures in the autopsy are **research notes**, not a forecast of future results.

## PolyTutor Labs

This project is maintained by **PolyTutor Labs** as an educational packaging of an existing open-source graveyard.

PolyTutor work on this repository includes:

- repository organization
- portability (repository-relative paths)
- security hardening and a published security audit
- test and quality-gate stabilization
- educational documentation

The original experiment code and first-person autopsy were not authored from scratch here. See [Attribution](#attribution).

This archive is **not affiliated with Polymarket**.

## About This Project

Between 29 March and 28 June 2026 the original author built six generations of automated Polymarket bots. Live capital was used only in the first two weeks (v0 and v1). Those runs ended in roughly **$40–$47** of losses and a **wallet ban** after tens of thousands of rejected orders. Everything after that was paper or shadow measurement.

The last generation (v5, Oracle Gap) was built to measure a signal against real outcomes **before** any live intent. Forward sports calibration landed near a coin flip (Brier **0.2377** on 332 resolutions). The gate set `graduated = FALSE` on every category and no live trade was placed after the ban.

The snapshots under `bots/` are **sanitized, incomplete excerpts**. The execution layer, wallet client, and credentials were removed on purpose. They will not trade as-is.

## What You Will Learn

- How to read a failed experiment as engineering evidence: hypothesis, implementation, outcome, death mode.
- Why shipping unvalidated strategies to a live wallet makes it impossible to separate bugs from a missing edge.
- Why a positive paper ledger on a small sample is noise, and why a bot’s self-report can disagree with `adjusted_pnl` in a database.
- How latency (for example a 2–11s multi-model call) can exceed a sub-second repricing window.
- How a static fair-price table can invert when the market regime changes.
- How a calibration / graduation gate is used as a **research control**, not as permission to trade.
- How a local ops watchdog (process kill, restarts, messaging) becomes an infrastructure tax — and why this archive tells you **not** to run it.

This project does **not** teach a method for extracting returns from prediction markets.

## Features

Verified in the current tree:

- Six documented historical experiments (v0–v5) with a shared chapter skeleton: goal → hypothesis → build → outcome → death → what survived
- Sanitized snapshots: risk primitives, analysis fragments, oracle measurement, and a SQL schema
- A first-person autopsy with figures read from PostgreSQL on 2026-06-28 ([`docs/AUTOPSY.md`](docs/AUTOPSY.md))
- A historical SPECTRIX watchdog kept **in place** as an ops case study — documented, not rewritten
- Quality infrastructure: `python -m compileall`, `scripts/security/check_secrets.py`, and pytest limited to `tests/`
- Published security policy and pre-PolyTutor audit ([SECURITY.md](SECURITY.md), [SECURITY_AUDIT.md](SECURITY_AUDIT.md))

There is no application lockfile and no live order router in this checkout.

## Historical Experiments

Each row is a **research note**, not a performance claim. Modes and figures come from the autopsy and journey chapters.

| # | Codename | What was tried | How it ended | Engineering lesson |
|---|----------|----------------|--------------|--------------------|
| v0 | Apex Predator | Avellaneda–Stoikov market maker on binary markets | ~4 hours live; ~−$20; 56,000+ rejected orders; wallet flagged | Do not send a market maker live without a paper warm-up |
| v1 | Shadow Sniper | Copy-wallet, momentum, neg-risk, cross-venue | 6 days live; bought 9 times with no auto-exit; same wallet banned | Design the exit path before the entry path |
| v2 | Phantom | BTC 5-minute UP/DOWN plus a 3-model consensus | Paper only. Raw ledger +$2,491.86 vs `adjusted_pnl` +$649.11; UP split rode a trend | A short paper ledger can be directional exposure, not a measured forecast |
| v3 | Long-Tail Sniper | Scanner over 480+ slower markets | Funnel 13,860 signals → 0 fills; model latency 2–11s vs window &lt;1s | Elegant design still fails if plumbing and latency do not match the book |
| v4 | Maker-Only BTC | Chainlink fair-price maker + rebate on BTC 5m/15m/1h | 55 days paper; `adjusted_pnl` **−$277.09** | A rebate does not automatically cover adverse selection |
| v5 | Oracle Gap | Measure forward on real outcomes before any live intent | Sports Brier 0.2377 (n=332); BTC–Deribit win rate 49% (n=35); **0** graduated categories | An honest gate that refuses promotion is a successful research instrument |

Timeline diagram: [`assets/timeline.svg`](assets/timeline.svg). How to study a generation: [docs/experiment-guide.md](docs/experiment-guide.md).

## Architecture Overview

This checkout is an **archive of fragments**, not a running desk.

```text
Historical narrative (docs/journey, docs/AUTOPSY.md)
        |
        v
Sanitized snapshots (bots/)
        |
        v
Study / quality gates only
        x  no wallet, no live router
```

| Layer | Location | What is actually here |
| --- | --- | --- |
| Narrative | `docs/journey/`, `docs/AUTOPSY.md` | Chronological failure analysis and database figures |
| Risk fragments | `bots/01-apex-shadow/risk/` | VPIN, Kelly, CVaR, hard limits — no signing or execution |
| Early strategy fragments | `bots/01-apex-shadow/strategy/` | Base class, momentum detector, safety gate (incomplete) |
| Analysis fragments | `bots/02-phantom/analysis/` | Ensemble, calibration, quantitative helpers (LLM keys are constructor args) |
| Later strategy fragments | `bots/02-phantom/strategies/` | Interface plus political / snipe excerpts |
| Measurement | `bots/03-05-spectrix/oracle/` | Calibration gate and divergence recording |
| Historical ops | `bots/03-05-spectrix/watchdog.py` | Local launchd-era helper — **do not run** |
| Schema | `bots/03-05-spectrix/db/schema.sql` | DDL and zero seeds, not a production dump |

Removed on purpose: wallet client, order execution, live credentials, and the rest of the original engine. Details: [docs/architecture.md](docs/architecture.md).

## Repository Structure

```text
polymarket-bot-graveyard/
├── README.md
├── CONTRIBUTING.md
├── DISCLAIMER.md
├── SECURITY.md
├── SECURITY_AUDIT.md          # pre-PolyTutor audit; keep as-is
├── CHANGELOG.md               # public educational release notes (v0.1.0)
├── FINAL_REPORT.md            # Task 11 release checklist
├── VERSION                    # 0.1.0
├── LICENSE                    # MIT (code under bots/)
├── LICENSE-DOCS               # CC BY 4.0 (writing)
├── pytest.ini                 # collects tests/ only; excludes bots/
├── .env.example               # placeholder names only
├── docs/
│   ├── architecture.md
│   ├── getting-started.md
│   ├── learning-path.md
│   ├── experiment-guide.md
│   ├── lessons-learned.md
│   ├── watchdog-safety.md
│   ├── AUTOPSY.md             # original closing autopsy
│   └── journey/               # original chronological chapters
├── bots/
│   ├── 01-apex-shadow/
│   ├── 02-phantom/
│   └── 03-05-spectrix/        # includes watchdog.py (stay here)
├── scripts/security/
│   └── check_secrets.py
├── tests/                     # quality-infrastructure only
└── assets/timeline.svg
```

## Getting Started

This archive is for **reading and inspection**. It is not a start-the-bot tutorial.

Requirements for optional quality checks: Python 3.12 (CI version) and, for pytest, `pytest==8.3.4`.

```text
git clone https://github.com/PolyTutor-Labs/polymarket-bot-graveyard.git
cd polymarket-bot-graveyard
```

Then:

1. Read [DISCLAIMER.md](DISCLAIMER.md) and [SECURITY.md](SECURITY.md).
2. Follow [docs/learning-path.md](docs/learning-path.md).
3. Inspect snapshots under `bots/`. Do **not** execute `bots/03-05-spectrix/watchdog.py`.
4. Optionally run the quality commands in [Testing](#testing).

Full study setup: [docs/getting-started.md](docs/getting-started.md).

## Testing

There is **no** suite that replays historical bot behavior or claims a result. CI checks syntax, secrets, and docs.

```text
python3 -m compileall -q -x '(.venv|venv|__pycache__|\.git)' .
python3 scripts/security/check_secrets.py
python3 -m pytest
```

`pytest.ini` sets `testpaths = tests` and excludes `bots/`. Markdown lint and offline internal-link checks run in [.github/workflows/ci.yml](.github/workflows/ci.yml).

## Documentation

| Document | Topic |
| --- | --- |
| [docs/getting-started.md](docs/getting-started.md) | How to study this archive |
| [docs/architecture.md](docs/architecture.md) | Snapshot layers and what was removed |
| [docs/learning-path.md](docs/learning-path.md) | Staged study sequence |
| [docs/experiment-guide.md](docs/experiment-guide.md) | How to read one historical experiment |
| [docs/lessons-learned.md](docs/lessons-learned.md) | Engineering lessons from the six deaths |
| [docs/watchdog-safety.md](docs/watchdog-safety.md) | Why the historical watchdog must not be run |
| [docs/journey/00-overview.md](docs/journey/00-overview.md) | Original chronological chapters |
| [docs/AUTOPSY.md](docs/AUTOPSY.md) | Original closing autopsy (database figures) |
| [SECURITY.md](SECURITY.md) | Secrets policy, snapshot classification, watchdog risks |
| [SECURITY_AUDIT.md](SECURITY_AUDIT.md) | Pre-PolyTutor audit record (keep as-is) |
| [CONTRIBUTING.md](CONTRIBUTING.md) | What contributions are accepted |
| [DISCLAIMER.md](DISCLAIMER.md) | Educational-use disclaimer |
| [CHANGELOG.md](CHANGELOG.md) | Public educational release notes (v0.1.0) |
| [FINAL_REPORT.md](FINAL_REPORT.md) | Task 11 public-release checklist |

## Risks and Limitations

- **Archive ≠ live system.** Snapshots import modules that are not vendored (`polybot.*`, `src.*`, `asyncpg`, LLM SDKs, `numpy`). That incompleteness is a safety property.
- **Watchdog is unsafe to execute.** `watchdog.py` can `pkill`/`kill` processes, start PostgreSQL via Homebrew, send iMessage via AppleScript, and mutate whatever database `DATABASE_URL` reaches. See [docs/watchdog-safety.md](docs/watchdog-safety.md).
- **Paper and shadow figures are not live results.** Phantom’s raw paper ledger was an accounting artifact. v4’s adjusted paper result was negative. v5 never placed a live intent.
- **Self-reports lied.** The original autopsy rule: read the database, not the bot’s own report.
- **Legal and market risk.** Prediction markets are restricted in many jurisdictions. Automated trading can lose money quickly. The historical author lost real capital on v0/v1.
- **No affiliation.** This is not a Polymarket product.

## Security

See [SECURITY.md](SECURITY.md). The frozen pre-transform audit is [SECURITY_AUDIT.md](SECURITY_AUDIT.md). Do not treat the audit as a live operations runbook.

```text
python3 scripts/security/check_secrets.py
```

Never commit `.env`, wallet material, phone numbers, or database dumps. Placeholder names live in [`.env.example`](.env.example).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Documentation, tests, educational improvements, research notes, and honest post-mortems are welcome. Do not add secrets, private keys, or claims that any snapshot is a method for extracting returns.

## Disclaimer

Educational archive only. Historical and paper figures do not predict future results. Nothing here is a recommendation to trade.

Full text: [DISCLAIMER.md](DISCLAIMER.md).

## Attribution

This repository is an educational packaging by **PolyTutor Labs** of the graveyard originally published as:

**[https://github.com/Hiberius/polymarket-bot-graveyard](https://github.com/Hiberius/polymarket-bot-graveyard)**

Upstream authors retain credit for the original experiments, snapshots, and autopsy writing. PolyTutor Labs organized, hardened, documented, and packaged this checkout for classroom and self-study use. We do **not** claim ownership of the original code. We are not affiliated with Polymarket or with the original authors unless they participate here separately.

## License

- **Code** (`bots/`): [MIT](LICENSE) — copyright Hiberius (2026)
- **Writing** (`docs/`, per-folder READMEs, this README): [CC BY 4.0](LICENSE-DOCS)
