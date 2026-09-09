# Architecture

This repository is an **educational archive** of historical bot fragments. It is not a deployable trading stack.

The original engines (an ~8,100-line v0/v1 tree, later `polybot` / SPECTRIX) are **not** present in full. What remains is a curated slice plus the written autopsy. Treat missing imports as evidence of sanitization, not as a homework item to “complete the product.”

## Identity

```text
Failure analysis  ->  lessons learned  ->  engineering education
```

The architecture to study is: **what was kept, what was removed, and why a reader still cannot place an order from this checkout.**

## High-level map

```text
docs/journey + docs/AUTOPSY.md     written record (hypothesis, dates, DB figures)
        |
        v
bots/01-apex-shadow                v0-v1 risk + early strategy excerpts
bots/02-phantom                    v2-v3 analysis + later strategy excerpts
bots/03-05-spectrix                v3-v5 oracle, schema, historical watchdog
        |
        v
scripts/ + tests/                  quality gates (compile, secrets, collection)
        |
        x
wallet client / CLOB execution     absent by design
```

## Snapshot series

The series map lives in [`bots/README.md`](../bots/README.md). Folders do **not** line up one-to-one with version numbers:

| Historical generation | Snapshot directory | Why they share a folder |
| --- | --- | --- |
| v0 Apex Predator, v1 Shadow Sniper | `bots/01-apex-shadow/` | Same early engine; risk and safety-gate excerpts survived |
| v2 Phantom | `bots/02-phantom/` | SPECTRIX 2.0 / `polybot` analysis and strategy interface |
| v3 Long-Tail Sniper | `bots/02-phantom/` | Same codebase; different scanner (scanner itself is not in-tree) |
| v4 Maker-Only BTC, v5 Oracle Gap | `bots/03-05-spectrix/` | Final SPECTRIX measurement and ops remnants |

`watchdog.py` stays under `bots/03-05-spectrix/`. Do not relocate it to `scripts/` or `src/`. See [watchdog-safety.md](watchdog-safety.md).

## Layer catalog (verified in-tree)

### Narrative layer

- [`docs/journey/`](journey/) — one chapter per generation, same skeleton each time.
- [`docs/AUTOPSY.md`](AUTOPSY.md) — closing record dated 2026-06-28. Figures are claimed to come from PostgreSQL, not from the bot’s self-report.

These files are **historical source material**. Educational wrapping lives in this file, [experiment-guide.md](experiment-guide.md), and [lessons-learned.md](lessons-learned.md).

### Risk fragments (`bots/01-apex-shadow/risk/`)

| Module | Role in the snapshot |
| --- | --- |
| `vpin.py` | Toxic-flow detector (informed flow vs you) |
| `kelly.py` | Fractional Kelly sizing helper |
| `cvar.py` | Tail-loss aware sizing helper |
| `limits.py` | Exposure / drawdown / daily-loss caps |

These modules are described in the v0/v1 README as having **no Polymarket-specific assumptions**. They still cannot trade: there is no position manager or venue client here.

### Early strategy fragments (`bots/01-apex-shadow/strategy/`)

| Module | Role in the snapshot |
| --- | --- |
| `base.py` | `Strategy` interface |
| `momentum_sniper.py` | Momentum detector — also a case study of boot-time false positives without warm-up |
| `safety_gate.py` | Pre-trade checks (VPIN halt, balance, inventory, daily cap, size cap) |

`safety_gate.py` imports `src.market_data.book_snapshot` and `src.risk.vpin`. Those packages are **not** in this tree. The v1 chapter records that the gate blocked selling and never enforced an exit. Read it as a lesson, not a template.

### Analysis fragments (`bots/02-phantom/analysis/`)

| Module | Role in the snapshot |
| --- | --- |
| `ensemble.py` | Three-model consensus helper (Claude / GPT / Gemini client libraries) |
| `calibration.py` | Confidence → calibrated probability helpers |
| `quant.py` | Expected-value style helpers |
| `win_probability.py` | Win-probability estimation helpers |

`ensemble.py` takes `anthropic_key`, `openai_key`, and `google_key` as **constructor parameters**. No live keys are committed. Wiring real keys would call third-party APIs (cost and privacy) and still cannot place a venue order from this snapshot. Implied imports include `polybot.analysis.prompts`, which is absent.

### Later strategy fragments (`bots/02-phantom/strategies/`)

`base.py`, `political.py`, and `snipe.py` show the fleet interface and two example strategies. They are incomplete. v3’s long-tail scanner is described in [journey/03-long-tail-sniper.md](journey/03-long-tail-sniper.md); the scanner implementation is not snapshotted.

### Measurement layer (`bots/03-05-spectrix/oracle/`)

| Module | Role in the snapshot |
| --- | --- |
| `calibration_gate.py` | Forward Brier / reliability / realized-edge gate; sets `graduated` |
| `divergence.py` | Records forecast-vs-book divergence for later scoring |

The gate’s own docstring says a category may only go live after **forward, out-of-sample** resolutions (not a backtest), with Brier, sample size, realized edge, and a reliability trend. In the autopsy, **zero** categories graduated. That refusal is the educational payload of v5.

`0.25` Brier is documented in-module as a coin-flip predictor; lower is better. Sports v5 landed at **0.2377** (n=332).

### Persistence remnant

`bots/03-05-spectrix/db/schema.sql` is DDL plus empty/zero seed rows (strategies / calibration). It is **not** a production dump: no wallet addresses, no credential rows, no tick history.

The autopsy refers to tables such as trades and oracle divergences. Use the schema as a map of what the historical service stored, not as a database to stand up for trading.

### Historical ops layer

`bots/03-05-spectrix/watchdog.py` is a launchd-era local helper:

- Health check against `http://127.0.0.1:8080`
- `pkill -9 -f "python3 -m polybot"` and `kill -9` of PIDs on port 8080
- `Popen` restart of `python3 -m polybot` (module **not** in this tree)
- AppleScript iMessage when `ALERT_PHONE` is set
- `brew services start postgresql@17`
- Parameterized `asyncpg` against `DATABASE_URL` (default `postgresql:///polybot`)
- Writes `/tmp/spectrix_watchdog_state.json` and a heartbeat file

Path defaults are portable (`BOT_DIR`, `PYTHON`, `PG_ISREADY`, `BREW`). **Behavior is unchanged on purpose.** Documented in [watchdog-safety.md](watchdog-safety.md) and [SECURITY.md](../SECURITY.md). Do not execute it.

## What was removed (by design)

The original public README and bot-folder notes agree on these absences:

- Wallet / signing / custody client
- Live CLOB execution and order-routing (“ghost orders” are narrative only)
- API keys, seed material, and remote password-bearing DSNs
- Streamlit dashboard, Docker deploy, and the aborted Rust execution layer (mentioned in the v0/v1 chapter; not present)
- Most of the 12 parallel v2 strategies and the v3 scanner
- The 5.76-million-tick and 2.55-million Chainlink datasets (cited in the autopsy; not stored here)

If a file `import`s `polybot.*` or `src.*`, the dependency is **missing**. That is expected.

## Data flow (historical, not runnable here)

The written record describes this loop. Only the marked pieces exist as code excerpts:

```text
Public market / sports / oracle data     (not vendored)
        |
        v
Strategy or ensemble intent              (fragments only)
        |
        v
Safety / calibration gate                (excerpts: safety_gate, calibration_gate)
        |
        v
Execution / wallet                       (REMOVED)
        |
        v
PostgreSQL trades + divergences          (schema only; no dump)
        |
        v
Watchdog + launchd                       (watchdog.py present; do not run)
```

For study, replace the missing execution box with: **read the chapter, then read the gate, then read the autopsy number.**

## Quality and security surfaces

These are part of the educational packaging, not part of the historical bots:

| Path | Role |
| --- | --- |
| `scripts/security/check_secrets.py` | Working-tree scan; prints path / line / pattern — never values |
| `tests/` | Quality-infra contracts (`compileall`, collection limited to `tests/`) |
| `.github/workflows/ci.yml` | Markdown lint, offline links, secret scan, compileall, pytest |
| `.env.example` | Placeholder names the snapshots actually read |

## Related reading

- [getting-started.md](getting-started.md) — how to inspect without executing ops helpers
- [experiment-guide.md](experiment-guide.md) — how to walk one generation
- [learning-path.md](learning-path.md) — staged sequence
- [../SECURITY.md](../SECURITY.md) — classification of each snapshot
