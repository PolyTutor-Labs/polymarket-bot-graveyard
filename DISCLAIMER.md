# Disclaimer

**Educational archive only.**

This repository is a PolyTutor Labs **failure-analysis** packaging of historical Polymarket bot experiments. It is not a commercial trading product, not a broker, not a signal service, and not an official Polymarket product or affiliate.

**This repository is not:**

- a live trading product or hosted service
- a collection of strategies to take to a venue
- a source of investment, legal, or tax advice
- a forecast of future market results

**Trading involves risk.** The historical author lost real capital on the only generations that used a live wallet (v0 and v1). Automated trading can lose money quickly. Nothing in the snapshots, journey chapters, autopsy figures, or educational guides is a recommendation to trade with real funds.

**Historical, paper, and shadow figures do not predict future results.** Paper ledgers in this archive disagreed with database columns. Shadow scores near a coin flip were treated as a reason to **refuse** live intent. Any apparent edge can vanish out of sample.

**The code is illustrative, not operational.** Folders under `bots/` are sanitized, partial snapshots. The execution and wallet layers were removed. They will not trade as-is, by design.

**Historical ops helpers are unsafe to execute.** `bots/03-05-spectrix/watchdog.py` can kill processes, send iMessage via AppleScript, start local services, and mutate a database. It is a historical implementation, not a production control. See [SECURITY.md](SECURITY.md) and [docs/watchdog-safety.md](docs/watchdog-safety.md).

**No warranty.** Code is provided “as is” under the MIT License. Writing is provided under CC BY 4.0. See [LICENSE](LICENSE) and [LICENSE-DOCS](LICENSE-DOCS).

**Legal restrictions apply.** Prediction markets such as Polymarket are restricted or prohibited for residents of many jurisdictions (including, at various times, the United States). You are responsible for the laws that apply to you.

By using this repository you accept that you do so at your own risk, and that the authors and PolyTutor Labs accept no liability for losses or consequences arising from it.

Upstream archive: [https://github.com/Hiberius/polymarket-bot-graveyard](https://github.com/Hiberius/polymarket-bot-graveyard).
