# Watchdog Safety

`bots/03-05-spectrix/watchdog.py` is a **historical ops helper** from a local SPECTRIX install (launchd, five-minute cadence, heartbeat, self-restart).

It is kept in the snapshot **on purpose** so learners can see the “ops tax” death pattern. It is **not** production-ready. Task 10 documents risk only. The file is **not** modified, disabled, or rewritten here.

**Do not run this file** against a live trading stack, a shared machine, or any database you care about.

Policy classification: [../SECURITY.md](../SECURITY.md#watchdog-historical-automation). Pre-transform findings: [../SECURITY_AUDIT.md](../SECURITY_AUDIT.md) §3 / §8.

## Why it exists in the archive

The autopsy and [`journey/99-lessons.md`](journey/99-lessons.md) describe weeks spent on macOS sleep, TCC, app-nap, dead watchdogs, and huge error logs — more time keeping a process alive than testing whether a signal existed.

Read `watchdog.py` as evidence of that tax: health checks, unsupervised restarts, messaging, and SQL housekeeping around a bot module (`python3 -m polybot`) that is **not in this tree**.

## Side effects if executed

Behavior below is what the file still does. Packaging did not remove `pkill`, `kill`, AppleScript, or Homebrew service start.

| Historical behavior | Risk on a real host |
| --- | --- |
| `pkill -9 -f "python3 -m polybot"` | Destroys any matching local process |
| `lsof -ti:8080` then `kill -9` | Kills whatever holds port 8080, not only a SPECTRIX bot |
| `subprocess.Popen([PYTHON, "-m", "polybot"], cwd=BOT_DIR, …)` | Unsupervised restart; `polybot` is absent here, but a similarly named module on `PYTHONPATH` could start |
| AppleScript via `osascript` when `ALERT_PHONE` is set | Sends iMessage; `_sanitize_applescript` is a partial historical mitigation, not a production control |
| `[BREW, "services", "start", "postgresql@17"]` | Starts a local Postgres service without confirmation |
| `asyncpg` on `DATABASE_URL` (default `postgresql:///polybot`) | `force_close_stale` and related helpers **mutate** rows (status / P&L bookkeeping) |
| Writes `LOG_FILE` under `BOT_DIR/data/`, plus `/tmp/spectrix_watchdog_state.json` and a heartbeat file | Host filesystem side effects |
| HTTP GET `http://127.0.0.1:8080/health` | Localhost only in source; still a live probe if something listens |

SQL helpers (`db_exec` / `db_fetch_val`) are parameterized. That reduces injection risk; it does **not** make unsupervised `UPDATE`s safe.

## Environment knobs (placeholders)

Names from [`.env.example`](../.env.example) and the file header:

| Variable | Default in snapshot | Danger if set carelessly |
| --- | --- | --- |
| `ALERT_PHONE` | empty (alerts skipped) | Real number → iMessage attempts |
| `DATABASE_URL` | `postgresql:///polybot` | A remote or shared DSN → mutated production-like data |
| `BOT_DIR` | `bots/03-05-spectrix/` | Wrong directory → logs / `cwd` / restart target |
| `PYTHON` | `python3` on `PATH` or current interpreter | Restart uses this binary |
| `PG_ISREADY` | `pg_isready` on `PATH` | False sense of DB health |
| `BREW` | `brew` on `PATH` | Service start uses this binary |

Leave `.env` uncreated for study. Never commit phone numbers or password-bearing URLs.

## Thresholds (historical constants)

These numbers are **in the source** for reading. They are not recommended operations settings.

- Stale force-close: 30 hours (weather path: 72 hours)
- Auto-disable after 25 trades if win rate &lt; 20%
- Balance-drift alert threshold: 100
- Scheduled summaries at local hours 8, 15, 23
- Alert cooldowns: 300s critical, 3600s warning

Changing them would be a bot/ops rewrite and is out of scope.

## How to study it (without running)

1. Read this page and the watchdog section of [../SECURITY.md](../SECURITY.md).
2. Open the module docstring (educational warning is already there from earlier hardening).
3. Read `restart_bot`, `send_alert`, `check_postgres`, `force_close_stale`, and `main` as text.
4. Connect it to death pattern 7 in [lessons-learned.md](lessons-learned.md).

Quality tests explicitly refuse to collect `watchdog.py` (`pytest.ini` + `tests/test_quality_gates.py`).

## What this archive will not do

- Will not disable `pkill` / `kill` / AppleScript / `brew services`
- Will not move the file to `scripts/` or stub it into a “safe” CLI
- Will not present it as an orchestration product

If you need process supervision for some other project, use a purpose-built supervisor. Do not copy this helper onto a host.

## Reporting

If you believe a committed secret or a more serious operational foot-gun was missed, follow [../SECURITY.md](../SECURITY.md) (private advisory — do not paste values).
