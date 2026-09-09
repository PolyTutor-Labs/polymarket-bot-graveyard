# Learning Path

Use this repository as a **study sequence**, not as a trading playbook. None of the snapshots, paper ledgers, or shadow scores are presented as a method to take live.

Each stage has a reading goal and a question you should be able to answer before moving on.

## Stage 1 — Positioning

Read:

- [../README.md](../README.md) — What this is / is not, PolyTutor Labs, Historical Experiments
- [../DISCLAIMER.md](../DISCLAIMER.md)
- [../SECURITY.md](../SECURITY.md) (through the watchdog section)

Goal: you can state, in your own words, that this is a **failure-analysis archive** and that executing `watchdog.py` is out of bounds.

Check: What happened to the only wallet that touched real capital?

## Stage 2 — How the archive is shaped

Read [architecture.md](architecture.md) and walk the tree without executing it:

1. [`bots/README.md`](../bots/README.md) — version → folder map (v3 shares `02-phantom/`)
2. `bots/01-apex-shadow/` — risk primitives vs incomplete strategy stubs
3. `bots/02-phantom/` — analysis vs strategies
4. `bots/03-05-spectrix/` — oracle, schema, watchdog (open as text only)

Goal: you can explain “narrative + fragments + quality gates” without assuming a hidden live broker.

Check: Which two historical generations share a snapshot folder, and why?

## Stage 3 — How to read one experiment

Read [experiment-guide.md](experiment-guide.md), then complete **one** generation end to end:

| If you pick | Chapter | Snapshot |
| --- | --- | --- |
| Live-capital disaster | [journey/01-apex-and-shadow.md](journey/01-apex-and-shadow.md) | `bots/01-apex-shadow/` |
| Paper ledger vs database | [journey/02-phantom.md](journey/02-phantom.md) | `bots/02-phantom/analysis/` |
| Measurement that refused promotion | [journey/05-oracle-gap.md](journey/05-oracle-gap.md) | `bots/03-05-spectrix/oracle/` |

Use the guide’s skeleton: goal → hypothesis → what exists in-tree → what the autopsy recorded → death mode → what *not* to copy.

Check: Which number in that generation came from the database rather than the bot’s own report?

## Stage 4 — Recurring death modes

Read [lessons-learned.md](lessons-learned.md) and [`journey/99-lessons.md`](journey/99-lessons.md).

Then skim the remaining numbered chapters so you can see the same modes recur:

- [03-long-tail-sniper.md](journey/03-long-tail-sniper.md) — funnel + latency
- [04-maker-btc.md](journey/04-maker-btc.md) — static fair price + adverse selection
- [05-oracle-gap.md](journey/05-oracle-gap.md) — forward measurement, no graduation

Goal: you can name the seven death patterns without treating any leftover module as a fix.

Check: Why is a ~49% win rate with rare large wins not evidence of a forecast?

## Stage 5 — Measurement as a research control

Study, as text:

1. `bots/03-05-spectrix/oracle/calibration_gate.py` — Brier, sample size, realized edge, reliability trend, `graduated`
2. `bots/03-05-spectrix/oracle/divergence.py` — what was recorded for later scoring
3. [`AUTOPSY.md`](AUTOPSY.md) §2 v5 and §3 shadow table (Brier 0.2377; 0 graduated categories)

Optional: `bots/01-apex-shadow/strategy/safety_gate.py` as a **counter-example** (a gate that blocked exits).

Goal: you can describe a graduation rule as a *filter on honesty*, not as a green light for a venue.

Check: What would it mean, in this archive’s terms, if `graduated` stayed false?

## Stage 6 — Ops tax and watchdog

Read [watchdog-safety.md](watchdog-safety.md) and the watchdog subsection of [../SECURITY.md](../SECURITY.md).

Open `bots/03-05-spectrix/watchdog.py` **as documentation**: `restart_bot`, `send_alert`, `force_close_stale`, `main`. Do not run the file.

Goal: you can list the host side effects (process kill, Homebrew Postgres, AppleScript, `/tmp` state, SQL) and explain why Task-era packaging documents them instead of “fixing” the helper into a product.

Check: Which environment variables would make an accidental run more destructive?

## Stage 7 — Write a research note

Using [experiment-guide.md](experiment-guide.md), write a short note (even privately) for one generation:

- What was assumed
- What was actually measured
- What the snapshot still contains
- What you would need, and still would not have, before claiming an edge

Negative results count. See [../CONTRIBUTING.md](../CONTRIBUTING.md) if you want to share a post-mortem.

Do not add live routing, keys, or language that presents a snapshot as a method for extracting returns.

## After the path

- Re-read [`AUTOPSY.md`](AUTOPSY.md) with the seven patterns in mind.
- Quality-check the tree if you change docs: [getting-started.md](getting-started.md).
- Stop. There is no Stage “deploy.”
