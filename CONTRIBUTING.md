# Contributing

Thank you for helping improve this **PolyTutor Labs educational archive**.

This repository teaches through historical experiments and failures: **failure analysis → lessons learned → engineering education**. See [README.md](README.md) Attribution and [DISCLAIMER.md](DISCLAIMER.md).

Contributions should make the graveyard easier to study, safer to read, or clearer to cite — not turn it into a live service or a strategy kit.

## Accept

We welcome:

- **Documentation** — accuracy, architecture notes, learning guides, educational framing
- **Tests** — quality-infrastructure coverage (secret scanner, collection contracts, compile checks)
- **Educational improvements** — comments and explanations that do not claim a method for extracting returns
- **Research notes** — honest post-mortems, negative results, and market-microstructure context
- **Bug fixes** in packaging / CI / docs — including security issues reported without embedding secret values

Two existing discussion tracks:

- 🔬 **Autopsy & discussion** — challenge a diagnosis or share your own post-mortem via [share_postmortem.yml](.github/ISSUE_TEMPLATE/share_postmortem.yml).
- 📏 **Forward measurement** — if you fork a documented failure mode, shadow-validate on a large independent sample **before** claiming an edge, and report via [revive_strategy.yml](.github/ISSUE_TEMPLATE/revive_strategy.yml). A negative result is a valid result.

## Require

Every contribution must:

- **Include no secrets** — no API tokens, `.env` values, phone numbers, or private RPC URLs
- **Include no private keys** — no seed phrases, mnemonics, PEM/key material, or wallet dumps
- **Include no return claims** — no “risk-free,” “signals,” or “will extract returns” language in code, docs, or comments
- **Leave historical implementations intact** unless the change is explicitly packaging (docs, CI, scanners). Do not rewrite strategies, algorithms, or `watchdog.py` behavior to make a test or linter pass
- **Explain behavior changes** — say what a learner will observe differently

Do not add live order routing, wallet signing, or custody. Do not execute or “harden by rewriting” [`bots/03-05-spectrix/watchdog.py`](bots/03-05-spectrix/watchdog.py). Document risk instead; see [docs/watchdog-safety.md](docs/watchdog-safety.md).

## How to work

1. Read [docs/getting-started.md](docs/getting-started.md) and [docs/architecture.md](docs/architecture.md).
2. Keep paths repo-relative; do not hardcode a personal machine home directory.
3. Keep `watchdog.py` under `bots/03-05-spectrix/`.
4. Match existing documentation tone: educational archive, historical experiments, engineering lessons, research notes, failure analysis.
5. For switches on unions/enums in any new TypeScript, handle every variant (exhaustive `never` / `assert_never` style). Keep Python imports at the top of the file.

## Checks to run

This archive has **no** trading or P&L test suite. CI checks syntax, secrets, and docs. `pytest.ini` collects only `tests/` and excludes `bots/`.

```text
python3 -m compileall -q -x '(.venv|venv|__pycache__|\.git)' .
python3 scripts/security/check_secrets.py
python3 -m pytest
npx --yes markdownlint-cli2 "**/*.md" "#node_modules"
```

`pytest` is quality-infrastructure only (CI installs `pytest==8.3.4`). It is not an application dependency of the historical bots.

## Pull requests

- Describe the problem and the verified behavior after the change.
- Link any docs you updated (`README.md`, `docs/*`, `SECURITY.md`).
- If you change snapshot code, say so explicitly — those are not “docs-only.”
- Do not claim official Polymarket affiliation or investment advice.
- Do not treat paper ledgers, shadow scores, or a future `graduated` flag as a live-trading endorsement.

Prose lives under [CC BY 4.0](LICENSE-DOCS); code lives under [MIT](LICENSE).

## Security reports

Do not open a public issue that includes credential values. Follow [SECURITY.md](SECURITY.md). Private advisories: [security advisories](https://github.com/PolyTutor-Labs/polymarket-bot-graveyard/security/advisories/new).
