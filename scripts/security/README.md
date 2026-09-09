# Security scripts

Educational-repo helpers. Not a production security platform.

| Script | Purpose |
|--------|---------|
| [`check_secrets.py`](check_secrets.py) | Working-tree scan for likely committed secrets. Prints path / line / pattern name only — **never values**. |

```text
python3 scripts/security/check_secrets.py
```

Exit `0` if clean, `1` if a finding is reported. See [`SECURITY.md`](../../SECURITY.md).
