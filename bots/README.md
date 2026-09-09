# Bot series

Sanitized, non-runnable excerpts from six failed generations. This is a failure archive for study — not a trading framework and not a `src/strategies/` layout.

| Series | Snapshot | Narrative |
|--------|----------|-----------|
| v0 Apex Predator + v1 Shadow Sniper | [`01-apex-shadow/`](01-apex-shadow/) | [`docs/journey/01-apex-and-shadow.md`](../docs/journey/01-apex-and-shadow.md) |
| v2 Phantom | [`02-phantom/`](02-phantom/) | [`docs/journey/02-phantom.md`](../docs/journey/02-phantom.md) |
| v3 Long-Tail Sniper | [`02-phantom/`](02-phantom/) (same codebase, different scanner) | [`docs/journey/03-long-tail-sniper.md`](../docs/journey/03-long-tail-sniper.md) |
| v4 Maker-Only BTC + v5 Oracle Gap | [`03-05-spectrix/`](03-05-spectrix/) | [`docs/journey/04-maker-btc.md`](../docs/journey/04-maker-btc.md), [`docs/journey/05-oracle-gap.md`](../docs/journey/05-oracle-gap.md) |

`03-05-spectrix/watchdog.py` stays in that snapshot. Do not relocate it into `scripts/` or `src/`. It is a historical automation helper (process kill/restart, AppleScript alerts). Documented in [SECURITY.md](../SECURITY.md#watchdog-historical-automation) — do not run it against a live host.
