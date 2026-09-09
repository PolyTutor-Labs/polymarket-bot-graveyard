# Security Policy

This repository is an **archived experiment / historical implementation / educational reference**.

It is a failure-analysis graveyard: what was tried, why it died, and what an engineer can learn. It is **not** a production trading platform, live trading service, deployment framework, or supported runtime.

Keep `SECURITY_AUDIT.md` as the pre-PolyTutor audit record. This file is the public policy after Task 8 hardening.

## Reporting

- **A leaked secret or sensitive data in this repo:** report privately via GitHub's
  [Report a vulnerability](https://github.com/PolyTutor-Labs/polymarket-bot-graveyard/security/advisories/new)
  feature, or open a minimal issue that does **not** paste the sensitive value.
- **In your own contributions:** never include real keys, wallet material, private RPC URLs, phone numbers, or database dumps in issues or PRs.

## No secrets by construction

Before publication, tracked files were scanned for secrets (private keys, API keys, wallet seeds, password-bearing connection strings, tokens). API credentials in the historical code are constructor parameters or environment variables and were never hardcoded as live values.

Re-scan locally (prints path / line / pattern name only — never values):

```text
python3 scripts/security/check_secrets.py
```

Placeholders for names this snapshot actually reads live in [`.env.example`](.env.example). Copy to `.env` if you must experiment locally. Never commit `.env`.

If you believe something sensitive slipped through, please report it privately.

## Historical bot code — classify, do not rewrite

Snapshots under `bots/` stay as historical implementations. Task 8 does **not** rewrite strategies, algorithms, or ops helpers. Classification only:

| Snapshot | Class | Notes |
|----------|-------|-------|
| `bots/01-apex-shadow/risk/*` | **SAFE (educational)** | Risk math (VPIN, Kelly, CVaR, limits). No wallet / signing / execution layer. |
| `bots/01-apex-shadow/strategy/*` | **SAFE (educational, incomplete)** | Strategy interfaces and detectors. Incomplete on purpose; cannot trade as-is. |
| `bots/02-phantom/analysis/*` | **SAFE (key-injection)** | LLM clients take constructor parameters (`anthropic_key`, `openai_key`, `google_key`). No hardcoded credentials. Wiring real keys would call third-party APIs (cost / privacy) but still cannot place trades from this snapshot. |
| `bots/02-phantom/strategies/*` | **SAFE (educational, incomplete)** | Strategy fragments. No execution or wallet client. |
| `bots/03-05-spectrix/oracle/*` | **SAFE (educational)** | Calibration / divergence measurement. The honest "no edge" gate. |
| `bots/03-05-spectrix/db/schema.sql` | **SAFE** | DDL plus empty/zero seed rows. No production dumps, addresses, or credentials. |
| `bots/03-05-spectrix/watchdog.py` | **HISTORICAL / DO NOT RUN LIVE** | Local macOS ops helper from the SPECTRIX era. See [Watchdog](#watchdog-historical-automation). Behavior is unchanged on purpose. |

Implied imports (`numpy`, `structlog`, `anthropic`, `openai`, `google.genai`, `asyncpg`, internal `polybot.*` / `src.*`) are **not vendored**. Fragments are non-runnable as a trading stack. That incompleteness is a safety property, not a defect to "fix."

## Watchdog historical automation

`bots/03-05-spectrix/watchdog.py` is a **historical ops helper** from a local SPECTRIX install (launchd + heartbeat + self-restart). It is **not production-ready**.

Task 8 documents risk only. It does **not** remove `pkill` / `kill`, does **not** remove AppleScript, and does **not** rewrite watchdog architecture. Portable path resolution from Task 7 (`BOT_DIR`, `PYTHON`, `PG_ISREADY`, `BREW`) is unchanged.

If someone executes this file on a real host, residual operational risks include:

| Historical behavior (kept) | Risk if executed |
|----------------------------|------------------|
| `pkill -9 -f "python3 -m polybot"` and `kill -9` of PIDs on port 8080 | Destroys matching local processes; unsupervised restart via `Popen` |
| AppleScript iMessage via `osascript` when `ALERT_PHONE` is set | Shell-adjacent messaging; phone must stay in env, never committed |
| `brew services start postgresql@17` | Starts a local database service without confirmation |
| `DATABASE_URL` (default `postgresql:///polybot`) | Local socket DSN only in the snapshot — do not point this at a real remote database |
| Writes `/tmp/spectrix_watchdog_state.json` and a heartbeat file | Host filesystem side effects |
| Parameterized `asyncpg` helpers (`db_exec` / `db_fetch_val`) | SQL is parameterized (not `eval`/`exec`); still mutates whatever DB it can reach |

`_sanitize_applescript` is a historical partial mitigation, not a production control. Treat the file as an educational reference for "more time was spent keeping the bot alive than finding an edge."

**Do not run `watchdog.py` against a live trading stack, a shared machine, or any database you care about.**

## Data and artifacts

| Artifact | Decision | Rationale |
|----------|----------|-----------|
| `docs/`, `README.md`, licenses, disclaimer | **SAFE** | Intentional public post-mortem (approximate loss figures; no credentials) |
| `assets/timeline.svg` | **SAFE** | Diagram only |
| Curated `bots/**/*.py` snapshots | **SAFE** (watchdog: do-not-run) | Sanitized, incomplete, no wallet layer |
| `bots/03-05-spectrix/db/schema.sql` | **SAFE** | Schema + zero seeds, not a dump |
| `.env.example` | **SAFE** | Placeholder names only |
| `SECURITY_AUDIT.md` | **SAFE** | Historical audit; keep as-is |
| Live `.env`, wallets, PEM/key material, DB dumps, logs | **REMOVE / NEVER COMMIT** | Gitignored; must stay out of history |

Nothing currently tracked needed deletion for public educational release. Keep unsafe artifacts out with `.gitignore` and `scripts/security/check_secrets.py`.

## Environment

| Item | Policy |
|------|--------|
| `.env` / `.env.*` | Gitignored (`!.env.example`) |
| `.env.example` | Placeholder names only — empty or local-socket examples, never real values |
| Extra ignore rules | PEM/P12/keystore/wallet/dump/SSH identity files |

## CI

`.github/workflows/ci.yml` stays a docs lint + offline link check. Least privilege: `permissions: contents: read` (no `contents: write`). Third-party Actions are **SHA-pinned** (mutable major tags are not used). Dependabot remains `github-actions` only. This is not a production deploy pipeline.

## Dependencies

There is no application lockfile. Implied libraries are educational fragments. Task 8 does **not** upgrade dependencies. No security-critical in-tree CVE to patch.

## Supported

There is no supported runtime and no security patch cadence. This is a record of software that has been shut down. Fixes here are for **safe public educational reading**, not for making the bots trade.
