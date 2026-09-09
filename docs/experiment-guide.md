# Experiment Guide

This guide is how to study a **historical experiment** in this archive. It is not a protocol for running bots, collecting an edge, or placing orders.

The original chapters already use a stable skeleton. Reuse it. Add one extra column: **what is still in the tree**.

## The skeleton

For each generation, write (or read) these six fields, then a seventh:

| Field | Question |
| --- | --- |
| Goal | What was the operator trying to build? |
| Hypothesis | What inefficiency was assumed? |
| Build | What was implemented, and in what mode (live / paper / shadow)? |
| Outcome | What did the **database** (or other external record) show? |
| Death | Proximate bugs vs root cause |
| Survived | Which idea is reusable for a *different* problem? |
| In-tree | Which files remain, and which layers were removed? |

Chapters live in [`journey/`](journey/). Snapshots live in [`bots/`](../bots/). Figures that claim to be definitive are in [`AUTOPSY.md`](AUTOPSY.md).

## Rules of evidence

1. **Prefer the autopsy over the bot’s report.** The Phantom raw paper ledger (+$2,491.86) disagreed with `adjusted_pnl` (+$649.11). Both were paper. Neither was live capital.
2. **Mode is part of the result.** v0/v1 were live. v2–v4 were paper. v5 was shadow-only (measurement, no trade intent). Do not collapse those.
3. **Small n is noise.** The lessons chapter treats paper ledgers on the order of 50–100 trades as insufficient. v5’s sports sample (n=332) was large enough to look like a coin flip (Brier 0.2377 vs 0.25).
4. **Payoff shape is not a forecast.** A ~49% win rate with rare large wins can be the price of buying NO cheaply, not predictive skill. Split by regime; check correlation (v5 BTC–Deribit strikes resolved together).
5. **Missing code is data.** If the scanner or wallet client is absent, do not invent it in your notes.

Do not treat any field in this guide as a recommendation to trade.

## How to walk one generation

1. Read the numbered chapter in `docs/journey/`.
2. Open the matching snapshot README, then the two or three files the chapter actually discusses.
3. Copy the autopsy subsection for that version into your notes (numbers only; keep the mode).
4. Fill the skeleton. If a cell would require a missing module, write “not in snapshot.”
5. Name the death pattern using [lessons-learned.md](lessons-learned.md). One generation can match several patterns.
6. Stop before “how I would run this live.” That question is out of scope.

## Catalog (v0–v5)

The following summaries are **research notes**. They rest on the journey chapters and the 2026-06-28 autopsy. They do not claim a method that works going forward.

### v0 — Apex Predator (29 Mar 2026, ~4 hours, live)

- **Hypothesis:** Quote both sides with Avellaneda–Stoikov and capture spread on binary markets.
- **Build:** Full engine shipped to a live wallet on day one (chapter: ~8,100 lines, dashboard, Docker, risk stack). Snapshot keeps risk helpers and strategy stubs only.
- **Outcome:** About −$20. Spreads up to 129%. Wrong USDC contract (native vs USDC.e). 56,000+ rejected orders. Wallet flagged.
- **Death:** Unvalidated market maker + no rate limit + wrong settlement asset.
- **In-tree:** `bots/01-apex-shadow/risk/*`, `strategy/base.py`.

### v1 — Shadow Sniper (30 Mar–5 Apr 2026, 6 days, live)

- **Hypothesis:** Event-driven edges (copy-wallet, momentum, neg-risk, cross-venue) would succeed where making failed.
- **Build:** Four strategies on the **same** wallet. Safety gate present; automatic sell path not.
- **Outcome:** About −$40 of ~$57 remaining. Nine buys, zero sells. Wallet banned (spam from v0).
- **Death:** Exit never implemented; gate too strict to sell and too loose to force a close. Root cause: live capital before paper validation.
- **In-tree:** `momentum_sniper.py` (boot false positives), `safety_gate.py` (the broken gate).

After v1 the autopsy states: **zero** live trades in the database. All later numbers are paper or shadow.

### v2 — Phantom (11 Apr–4 May 2026, paper)

- **Hypothesis:** A three-model consensus plus Chainlink context can forecast BTC 5-minute UP/DOWN better than chance.
- **Build:** `polybot` fleet; Phantom as the headline strategy. Keys injected as constructor parameters.
- **Outcome (DB):** 238 paper trades. Raw `pnl` +$2,491.86 (called out as the lie). `adjusted_pnl` +$649.11, still paper. UP split 87% in an uptrend; DOWN split 50%.
- **Death:** Short-horizon BTC book already priced by professional desks; paper ledger was directional exposure. T−30s prices left little net-of-fee room.
- **In-tree:** `bots/02-phantom/analysis/ensemble.py` and calibration helpers; `strategies/*` excerpts. Most of the 12 parallel strategies are absent.

### v3 — Long-Tail Sniper (26 Apr–4 May 2026, never live)

- **Hypothesis:** Slower political / sports / pop books (480+ markets) are human-priced and therefore exploitable.
- **Build:** Scanner plus a multi-tier model evaluator on the Phantom-era codebase.
- **Outcome (DB):** 65 `long_tail_sniper` rows, P&L about 0. Funnel 13,860 signals → 75 tier-0 → 12 orders → **0 fills**.
- **Death:** Broken funnel plus 2–11s model latency versus a sub-second window.
- **In-tree:** Same `02-phantom` folder. The scanner itself is **not** snapshotted — the chapter is the primary artifact.

### v4 — Maker-Only BTC (4 May–1 Jun 2026, 55 days paper)

- **Hypothesis:** A Chainlink lookup-table fair price plus a maker rebate can earn the spread on BTC 5m/15m/1h without a directional forecast.
- **Build:** Maker path, rebate after the 30 Mar fee change, circuit breakers. Never cut over to live.
- **Outcome (DB):** `maker_btc_5m` n=1,585. Raw `pnl` −$58.34. `adjusted_pnl` **−$277.09**.
- **Death:** LUT calibrated in one regime (13–25 Apr) and used later; rebate did not cover adverse selection. Large ops tax (pagination, dead watchdog, macOS sleep) documented in the autopsy.
- **In-tree:** `bots/03-05-spectrix/` (oracle + watchdog + schema). The LUT and maker loop are **not** fully present.

### v5 — Oracle Gap (1 Jun–28 Jun 2026, shadow only)

- **Hypothesis:** If you measure forward on real resolutions first, you will know whether any category deserves a live intent.
- **Build:** Shadow observatory, in-game feed, goal-lag stopwatch, lag microscope (5.76M ticks cited), BTC–Deribit comparison, calibration gate.
- **Outcome (DB):** Sports Brier **0.2377** (n=332), realized edge **−2.86pp**, “would have won” 48.2%. BTC–Deribit n=35, win rate **49%**. Graduated categories **0 / 4**. Live intents **0**.
- **Death:** No edge to promote. The gate did its job by refusing. Goal-lag curves lacked an event anchor (semi-unusable).
- **In-tree:** `oracle/calibration_gate.py`, `oracle/divergence.py`, `db/schema.sql`. Tick data is **not** stored here.

## Paper, shadow, and live

| Mode | Meaning in this archive | Used by |
| --- | --- | --- |
| Live | Real wallet, real fills, real losses | v0, v1 only |
| Paper | Simulated or dry-run fills; ledger can still lie | v2, v3, v4 |
| Shadow | Record forecast vs outcome; no trade intent | v5 |

When you write notes, put the mode in the same sentence as the number.

## What a useful note looks like

```text
Experiment: v4 Maker-Only BTC
Mode: paper (55 days)
Hypothesis: rebate + LUT fair price covers inventory risk
DB figure: adjusted_pnl -277.09 on 1,585 maker_btc_5m rows
In-tree: calibration/oracle remnants; maker loop not snapshotted
Death patterns: static fair price; ops tax; assumed edge never validated forward
Not claimed: that a different LUT would have worked
```

## Sharing work

If you publish a note, follow [../CONTRIBUTING.md](../CONTRIBUTING.md):

- No secrets, keys, or phone numbers
- No language that presents a snapshot as a live method
- Negative results are first-class

Issue templates for discussion and forward measurement remain under [`.github/ISSUE_TEMPLATE/`](../.github/ISSUE_TEMPLATE/). Forward measurement, if you do it in a fork, is still research — not a product launch.
