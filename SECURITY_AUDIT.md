# Pre-PolyTutor Security Audit

| Field | Value |
|-------|-------|
| **Repository (source)** | https://github.com/Hiberius/polymarket-bot-graveyard |
| **Future target (not created)** | PolyTutor-Labs/polymarket-bot-graveyard |
| **Audit clone path** | `/workspace/polytutor-labs/polymarket-bot-graveyard-audit` |
| **Audit branch (local only)** | `security-audit-before-polytutor` |
| **Upstream HEAD audited** | `ab0176a` (`ci: bump actions/setup-node from 6 to 7 (#1)`) on top of `f0e596b` |
| **Audit date** | 2026-09-08 (America/New_York) |
| **Scope** | Phase 1 Repo #5 — inventory, secrets, malware, CI/CD, deps, artifacts, env — **no** source fixes, history rewrite, dependency upgrades, or org/repo creation |
| **Overall risk** | **LOW** (with Medium findings to remediate during PolyTutor transform) |

```
Approved for PolyTutor transformation: YES
```

---

## 1. Repository inventory

### Git status / remotes / branch

- Fresh clone; working tree clean before audit artifact.
- Remote: `origin` → `https://github.com/Hiberius/polymarket-bot-graveyard` (fetch/push).
- Branches: `main`, local `security-audit-before-polytutor` (not pushed).
- History is shallow in content: **2 commits** only (initial content + Dependabot Actions bump). No orphan history rewrite performed (per limits).

### Tree summary (44 tracked non-git files)

| Area | Contents |
|------|----------|
| Root docs | `README.md`, `CONTRIBUTING.md`, `DISCLAIMER.md`, `SECURITY.md`, `LICENSE`, `LICENSE-DOCS` |
| CI / meta | `.github/workflows/ci.yml`, `.github/dependabot.yml`, issue templates, `.gitignore`, `.editorconfig`, `.markdownlint.json` |
| Narrative | `journey/*.md` (8), `docs/AUTOPSY.md`, `assets/timeline.svg` |
| Code snapshots | `bots/01-apex-shadow/` (risk + strategy Python), `bots/02-phantom/` (analysis + strategies), `bots/03-05-spectrix/` (oracle, `watchdog.py`, `db/schema.sql`) |

**Notable absences:** no `package.json` / lockfile, no `requirements.txt` / `pyproject.toml` / `Pipfile`, no Docker/compose, no `.env` / `.env.example`, no wallet/client/execution layer (consistent with stated “sanitized snapshot” design).

Largest blobs: `bots/03-05-spectrix/db/schema.sql` (~43 KB DDL), `watchdog.py` (~21 KB), strategy modules, autopsy docs. No large binary blobs in git object inventory.

---

## 2. Secret audit

**Policy followed:** secret *values* are never printed here — only path, severity, and remediation.

### Scan coverage

- Filename patterns: `.env*`, `*.pem`, `*.key`, wallets/credentials/keystore — **none present** in working tree.
- Content patterns (API/auth tokens, PEM headers, AWS-style keys, GitHub PATs, long hex wallet material, mnemonics) across source/docs — **no live credential literals found**.
- High-entropy string candidates in Python reduced to **non-secret hardcoded local paths** in `watchdog.py` (see §3 / §6).
- Git history: only the two public commits; no secret-named files ever added; no `.env` / PEM / wallet files in `git ls-files`.
- `bots/02-phantom/analysis/ensemble.py`: LLM client keys accepted as **constructor parameters** (`anthropic_key`, `openai_key`, `google_key`) — injection pattern, not hardcoded secrets.
- `watchdog.py`: `ALERT_PHONE` and `DATABASE_URL` from environment (defaults empty / local socket DSN `postgresql:///polybot` — not a password-bearing remote URL).

| Finding | Path | Severity | Remediation |
|---------|------|----------|-------------|
| No hardcoded API keys / private keys / seeds / PATs detected | (repo-wide) | — | Keep constructor/env injection; add `.env.example` with **placeholder-only** names during transform |
| Local macOS username path embeds operator identity | `bots/03-05-spectrix/watchdog.py` | **Medium** (PII / path disclosure, not a cryptographic secret) | Replace with env var (e.g. `BOT_DIR`) or neutral placeholder before PolyTutor-Labs public mirror |
| Author personal email in git metadata | commit author `hiberius@gmail.com` | **Low** (already public on GitHub) | Optional: document provenance; do **not** rewrite history in this audit phase |
| Missing `.env.example` | repo root | **Low** | Add placeholder template listing `DATABASE_URL`, `ALERT_PHONE`, LLM keys — no real values |

**Verdict:** No Critical secret exposures found. Safe to proceed with transform if Medium PII path is sanitized as part of PolyTutor work (not done in this audit).

---

## 3. Malicious code review

Reviewed all Python under `bots/` plus SQL schema for wallet theft, remote exfiltration, RCE, obfuscation, and unexpected binaries.

| Check | Result |
|-------|--------|
| Wallet / key theft (`eth_account`, `from_mnemonic`, signing, `0x`+40 hex addresses) | **Not found** |
| Obfuscation (`marshal`, `zlib.decompress`+exec, heavy `\x` packing, `__builtins__` abuse) | **Not found** |
| Compiled binaries / ELF / PE / Mach-O | **Not found** (docs + Python + SQL + SVG + YAML only) |
| Outbound C2 / unexpected webhooks | Only localhost `http://127.0.0.1:8080` in watchdog; docs link to GitHub/Polymarket/Anthropic/Creative Commons |
| `eval` / `exec` on untrusted input | **Not found** (SQL helpers named `db_exec` use parameterized asyncpg) |

### Notable operational code (not malware; risk if someone runs it)

| Finding | Path | Severity | Notes / remediation |
|---------|------|----------|---------------------|
| Broad process control via `subprocess` (`pkill`, `kill -9`, `brew services`, `Popen` restart) | `bots/03-05-spectrix/watchdog.py` | **Medium** | Illustrative ops watchdog for a local SPECTRIX install. Document “do not run against production”; gate behind explicit env; prefer no default auto-kill in educational forks |
| AppleScript iMessage send via `osascript` | same file | **Medium** | Partial sanitization present (`_sanitize_applescript`). Still shell-adjacent; keep phone from env only; consider removing messaging from public teaching fork or stubbing it |
| Hardcoded absolute path under `/Users/...` | same file | **Medium** | Operator machine fingerprint; parameterize |
| Imports of absent packages (`polybot.*`, `src.*`, `asyncpg`, LLM SDKs, `numpy`) | multiple bot modules | **Info** | Confirms snapshots are **non-runnable as-is** (reduces accidental live trading risk) |

**Verdict:** No evidence of intentional malicious / theft malware. Residual risk is **operational** if a reader executes `watchdog.py` on a real host.

---

## 4. CI/CD security review

File: `.github/workflows/ci.yml`

| Control | Observation |
|---------|-------------|
| Triggers | `push` to `main`, all `pull_request`, `workflow_dispatch` |
| Permissions | Top-level `permissions: contents: read` — **good** least privilege |
| Jobs | Markdown lint (`markdownlint-cli2` via `npx --yes`); internal link check (`lycheeverse/lychee-action@v2` with `--offline`) |
| Secrets in CI | None referenced |
| Supply chain | Actions pinned to **major tags** (`actions/checkout@v7`, `actions/setup-node@v7`, `lycheeverse/lychee-action@v2`), **not** immutable commit SHAs |
| Dependabot | `.github/dependabot.yml` — `github-actions` weekly only |

| Finding | Severity | Remediation |
|---------|----------|-------------|
| Third-party Actions not SHA-pinned | **Medium** | Pin to full commit SHAs; keep Dependabot for updates |
| `npx --yes markdownlint-cli2` pulls latest CLI at runtime | **Low** | Pin CLI version in workflow or commit a minimal package.json (transform phase) |
| No code/security scanning (CodeQL, gitleaks, dependency review for app deps) | **Low** / Info | Acceptable for docs-heavy archive; add secret scanning when PolyTutor adds runtime deps |

Issue templates correctly steer secret reports to private advisories.

---

## 5. Dependency review (no upgrades performed)

- **Application dependency manifests:** none present → no lockfile CVEs to score in-tree.
- **Implied / incomplete imports** (not vendored): `numpy`, `structlog`, `anthropic`, `openai`, `google.genai`, `asyncpg`, internal `polybot.*` / `src.*` — educational fragments only.
- **CI-only:** Node 20 + ephemeral `markdownlint-cli2`; GitHub Actions ecosystem via Dependabot.
- **Audit action:** inventory only — **no upgrades, no installs to “fix”**.

| Finding | Severity | Remediation |
|---------|----------|-------------|
| Incomplete dependency story for teaching forks | **Low** | When PolyTutor adds runnable labs, introduce pinned manifests + SBOM/ Dependabot for that ecosystem |

---

## 6. Data / artifact classification

| Artifact | Classification | Rationale |
|----------|----------------|-----------|
| `journey/`, `docs/AUTOPSY.md`, `README.md`, licenses, disclaimer | **SAFE** | Intentional public post-mortem narrative (includes approximate loss figures; no credentials) |
| `assets/timeline.svg` | **SAFE** | Diagram only |
| Curated strategy/risk/oracle `.py` snapshots | **SAFE** | Sanitized, incomplete, no wallet layer |
| `bots/03-05-spectrix/db/schema.sql` | **SAFE** | DDL + empty/zero seed rows for strategies/calibration — **no** production row dumps, addresses, or secrets |
| `bots/03-05-spectrix/watchdog.py` hardcoded `/Users/<username>/...` path | **REMOVE / REDACT BEFORE PUBLIC RELEASE** (under PolyTutor-Labs) | Local operator identity disclosure |
| Live `.env`, wallets, PEM, DB dumps, logs | **N/A (absent)** | Correctly gitignored; must stay out of future commits |
| Git author personal email | **ACCEPT / DOCUMENT** | Already public upstream; history rewrite forbidden in this phase |

---

## 7. Environment review

| Item | Status |
|------|--------|
| `.env` / `.env.*` committed | **None** |
| `.env.example` | **Missing** |
| `.gitignore` secrets section | **Good**: `.env`, `.env.*` with `!.env.example`, `*.pem`, `*.key`, `wallets.json`, `secrets/`, plus `data/`, venvs, logs |
| Runtime config in code | Env for phone/DB URL; hardcoded `BOT_DIR` / Homebrew paths / localhost API — machine-specific, should be env-driven in transform |

---

## 8. Findings summary (by severity)

### Critical

- None.

### High

- None (no confirmed leaked credentials or wallet-theft malware).

### Medium

1. **PII / path disclosure** — hardcoded macOS home path in `bots/03-05-spectrix/watchdog.py`.
2. **Destructive local process management** — `pkill` / `kill -9` / unsupervised bot restart in same file (unsafe if executed).
3. **AppleScript messaging side channel** — iMessage via `osascript` (env-gated phone; residual injection/ops risk).
4. **CI Actions not SHA-pinned** — supply-chain hardening gap.

### Low / Info

- No `.env.example`; personal email in git authors; unpinned `npx` linter; incomplete import graph (by design); no app Dependabot ecosystem.

---

## 9. Approval decision

**Overall risk: LOW.**

The repository matches its own `SECURITY.md` claims: archival, sanitized, non-runnable trading snapshots with no detected live secrets or malicious payload. Medium items should be addressed **during** PolyTutor transformation (redact path, stub/harden watchdog side effects, pin Actions) but do **not** block starting the transform from this audited tree.

```
Approved for PolyTutor transformation: YES
```

### Explicit non-actions (per brief)

- Did **not** create `PolyTutor-Labs/polymarket-bot-graveyard`.
- Did **not** rewrite/orphan git history.
- Did **not** reorganize or modify source beyond adding this file.
- Did **not** upgrade dependencies or “fix” bugs.
- Did **not** push any branch to upstream.

### Audit blockers

- Nothing blocked completion. One broad secret-scan process hung and was terminated; coverage was completed via scoped ripgrep, entropy heuristics, git history/file listing, and manual review of all Python/SQL/CI paths.

---

*End of pre-PolyTutor Phase 1 Repo #5 security audit.*
