# Lessons Learned

Engineering lessons from six historical experiments that were shut down. This is a **failure analysis**, not a list of methods to reuse on a venue.

The original synthesis is [`journey/99-lessons.md`](journey/99-lessons.md). The closing autopsy is [`AUTOPSY.md`](AUTOPSY.md). This page restates those findings for classroom use and avoids treating leftover modules as a trading kit.

## The throughline

Every generation started from a similar belief: *prediction-market books are inefficient, and better tooling will find the gap.*

Every generation found something else: the gap was already closed, the sample was noise, the ledger was an artifact, or the signal was a coin flip under a forward score.

The last generation is the one that treated “no” as a valid output. That is the educational core of the archive.

## Seven death patterns

These recur across v0–v5. They are ordered the way the original lessons chapter orders them: by how expensive they were.

### 1. Assumed edge, live first

A paper ledger on a few dozen or a hundred trades is a weak test. v0 and v1 skipped even that and used a live wallet. After the ban, later versions still promoted paper noise into belief.

**Lesson:** Separate *code that runs* from *a claim that a signal exists*. Validate forward, out of sample, net of fees, across regimes. v5’s gate is the in-tree picture of that rule (`calibration_gate.py`).

### 2. Liquid books are already worked

The autopsy’s load-bearing claim: liquid Polymarket books are arbitraged by professional desks. By about thirty seconds before resolution the price is already tight. Retail margin after fees is described as approximately zero.

**Lesson:** “I can see the mispricing” is a hypothesis to measure, not a default. v2’s short-horizon BTC book is the case study.

### 3. Signal slower than the window

A three-model call is recorded at 2–11 seconds. The windows these experiments chased were often under a second. v3’s funnel produced 13,860 signals and **zero** fills.

**Lesson:** If the decision arrives after the book has moved, you do not have a usable signal — you have a log line.

### 4. Static fair price on a moving market

v4’s lookup table was calibrated in one April window and used for weeks afterward. Adjusted paper P&L was **negative**.

**Lesson:** A fair-value table that is not re-estimated can invert. A rebate does not automatically pay for adverse selection.

### 5. Payoff shape mistaken for skill

v5 BTC–Deribit: win rate 49% on 35 correlated resolutions. Large rare wins versus smaller frequent losses matched buying NO at a low price — a mechanical payoff, not a demonstrated forecast. Independent sample size was smaller than the row count.

**Lesson:** Split by side and regime. Ask whether the “edge” is just the contract’s payoff.

### 6. Pivot faster than a honest sample

Six versions in three months. The lessons chapter states that an honest validation needs on the order of 30+ days *per category*. The patience budget ran out first.

**Lesson:** A new idea is not evidence. Re-read the autopsy before starting a seventh generation.

### 7. Ops tax larger than the research question

macOS sleep, TCC prompts, app-nap, dead watchdogs, broken pagination, 100 MB logs. v4 spent more calendar on staying alive than on showing an edge.

**Lesson:** If most of the work is uptime, ask whether there is anything that deserves to be up. The historical watchdog is preserved as that warning — see [watchdog-safety.md](watchdog-safety.md).

## What the measurements support

These are **historical measurements** from the autopsy, not forecasts:

| Claim in the record | Support cited |
| --- | --- |
| Short-horizon BTC / crypto on this venue showed no retail edge for this operator | Died in v0, v2, v4, and v5 Deribit; external 2026 notes on a shrinking arb window and higher dynamic fees |
| Static sports price comparison looked like a coin flip | Brier 0.2377 on 332 resolutions; realized edge −2.86pp |
| BTC–Deribit gap was not a clean arb | Win rate 49%; risk-neutral option probability ≠ real-world probability |
| Copy-trading “smart” wallets was judged a losing imitation | Discussed in June; **never built** — absence is the lesson |
| Shadow-first gating can refuse a live intent | 0 / 4 categories graduated |

## What is reusable — for a different problem

The original lessons page is explicit: leftover engineering is for **some other** research problem, not for repeating these venue bets.

| Artifact | Why it is still interesting | Why it is not a product |
| --- | --- | --- |
| `calibration_gate.py` | Honest promotion rule (Brier, n, realized edge, reliability) | Graduation never flipped true here |
| Risk helpers (VPIN, Kelly, CVaR, limits) | Pure sizing / toxicity math | No execution layer |
| `safety_gate.py` | Shows a gate that blocked the exit | Historical bug, not a template |
| `ensemble.py` | Constructor-injected keys; shrinkage toward the book | Latency vs window; no venue client |
| `schema.sql` | What a research DB might store | Empty seeds; no dump |
| `watchdog.py` | Case study in process babysitting | Unsafe to execute |

The 5.76M CLOB ticks and 2.55M Chainlink prints are **cited**, not shipped.

## Habits the archive tries to teach

- Read `adjusted_pnl` (or the equivalent) from storage. Do not trust a process that grades itself.
- Write the mode next to every number (live / paper / shadow).
- Keep secrets out of the tree ([../SECURITY.md](../SECURITY.md)).
- Document the death. A well-measured “no” is the deliverable.

## What this page does not say

It does not say that a larger sample, a faster model, or a different rebate would have worked. It does not recommend repeating the live v0/v1 path. It does not treat `graduated = TRUE` in some future fork as permission to trade.

For the first-person original, read [`journey/99-lessons.md`](journey/99-lessons.md). For how to apply the skeleton to one generation, read [experiment-guide.md](experiment-guide.md).
