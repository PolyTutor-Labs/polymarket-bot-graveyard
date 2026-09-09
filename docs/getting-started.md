# Getting Started

This checkout is an **educational archive**. Getting started means learning how to *read* it safely — not installing a trading bot.

Nothing in these steps places an order, opens a wallet, or starts the historical SPECTRIX service.

## Before you clone

Read:

1. [../DISCLAIMER.md](../DISCLAIMER.md) — educational use only; not a recommendation to trade
2. [../SECURITY.md](../SECURITY.md) — secrets policy and snapshot classification
3. [watchdog-safety.md](watchdog-safety.md) — why `watchdog.py` must stay unexecuted

If your goal is live Polymarket automation, **stop**. This repository will not provide that, and the historical record is that the live attempts ended in losses and a banned wallet.

## What you need

| Activity | Requirement |
| --- | --- |
| Read the archive | A browser or editor |
| Inspect Python snapshots | Any editor; optional Python 3 to open files |
| Quality checks (same as CI) | Python 3.12 (or 3.x) plus `pytest==8.3.4` for the test job |

There is no application `requirements.txt` or `package.json`. Implied libraries inside `bots/` (`asyncpg`, LLM SDKs, `numpy`, `polybot.*`, `src.*`) are **not installed** and should stay that way for study.

## Clone

```text
git clone https://github.com/PolyTutor-Labs/polymarket-bot-graveyard.git
cd polymarket-bot-graveyard
```

You do **not** need to copy `.env.example` unless you are reading which names the historical watchdog accepted. If you do copy it, leave values empty. Never commit `.env`.

## Suggested first hour

Follow [learning-path.md](learning-path.md) Stage 1–3, or this shorter path:

1. This file and the root [README.md](../README.md) sections **What this repository is / is not**.
2. [architecture.md](architecture.md) — what exists vs what was removed.
3. [experiment-guide.md](experiment-guide.md) — how to read one generation.
4. [`journey/00-overview.md`](journey/00-overview.md) then **one** numbered chapter.
5. The matching folder under [`bots/`](../bots/) (see [bots/README.md](../bots/README.md)).
6. [lessons-learned.md](lessons-learned.md) and, when you want the raw figures, [`AUTOPSY.md`](AUTOPSY.md).

Do not start by running Python under `bots/`.

## Optional quality checks

These commands match [CONTRIBUTING.md](../CONTRIBUTING.md) and CI. They do not exercise strategy behavior.

```text
python3 -m compileall -q -x '(.venv|venv|__pycache__|\.git)' .
python3 scripts/security/check_secrets.py
python3 -m pytest
```

`pytest` collects only `tests/` (`pytest.ini` lists `bots` under `norecursedirs`). Collection must never include `watchdog.py`.

Markdown lint (CI uses Node 20):

```text
npx --yes markdownlint-cli2 "**/*.md" "#node_modules"
```

## Environment names (placeholders only)

[`.env.example`](../.env.example) lists names the SPECTRIX watchdog actually reads:

| Name | Historical use | Study rule |
| --- | --- | --- |
| `ALERT_PHONE` | iMessage target | Leave empty; never commit a number |
| `DATABASE_URL` | asyncpg DSN, default `postgresql:///polybot` | Do not point at a database you care about |
| `BOT_DIR` | Working directory for logs / `cwd` | Defaults to `bots/03-05-spectrix/` |
| `PYTHON` | Interpreter for a `polybot` restart | `polybot` is not in this tree |
| `PG_ISREADY` | Postgres liveness helper | Unused unless you execute the watchdog |
| `BREW` | Homebrew CLI | Unused unless you execute the watchdog |

LLM key **names** in comments (`ANTHROPIC_API_KEY`, and so on) document constructor parameters on `ensemble.py`. They are not read from the environment in this snapshot. Do not add real values.

## What not to run

| Path | Why |
| --- | --- |
| `bots/03-05-spectrix/watchdog.py` | Kills processes, may start Postgres, may send iMessage, may mutate SQL. See [watchdog-safety.md](watchdog-safety.md). |
| Any reconstructed “full bot” | Execution and wallet layers were removed. Reassembling them is outside this archive’s purpose. |
| Live order scripts against Polymarket | Not present; do not add them as if this were a product. |

## If an import fails

That is expected. Open the file as text and read the lesson in the matching journey chapter. Repairing imports so a snapshot “runs” is out of scope for this educational packaging.

## Next

- [learning-path.md](learning-path.md) — staged sequence
- [experiment-guide.md](experiment-guide.md) — one experiment at a time
- [../CONTRIBUTING.md](../CONTRIBUTING.md) — how to send research notes
