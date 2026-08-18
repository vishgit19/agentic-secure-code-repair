# Agentic Secure Code Repair

A small, inspectable Python security scanner that finds risky code patterns and proposes reviewable repairs. The current MVP is deliberately deterministic: it favors explainable findings and patch previews over opaque, automatic rewrites.

> Status: early MVP. Use the output as review guidance, not as a substitute for a security audit.

## Why this project exists

Security tooling is most useful when developers can understand and trust the change it proposes. This project experiments with a repair loop built around three ideas:

1. detect a concrete risky pattern;
2. explain why it matters and point to the exact line;
3. generate a patch only when the change is narrow enough to review safely.

## What it detects

| Rule | Pattern | Severity | Patch preview |
| --- | --- | --- | --- |
| `SR001` | `eval(...)` or `exec(...)` | high | no |
| `SR002` | `subprocess` with `shell=True` | high | no |
| `SR003` | TLS verification disabled with `verify=False` | high | yes |
| `SR004` | Flask-style `debug=True` | medium | yes |
| `SR005` | unsafe `yaml.load(...)` call | medium | no |
| `SR006` | MD5 or SHA-1 used through `hashlib` | medium | no |
| `SR007` | likely hard-coded secret assignment | high | no |
| `SR008` | unsafe `pickle.load(...)` or `pickle.loads(...)` | high | no |

The rules are intentionally conservative and may produce false positives. Findings that require semantic judgment do not receive automatic patches.

## Quick start

Requires Python 3.10 or newer.

```bash
python -m pip install -e .
secure-repair scan examples/vulnerable.py
```

Write machine-readable results:

```bash
secure-repair scan src --format json
```

Generate a unified diff containing only the supported repair previews:

```bash
secure-repair scan src --patch secure-repair.patch
git apply --check secure-repair.patch
```

The tool never changes source files in place.

## Example

```text
examples/vulnerable.py:9:4 SR003 high TLS certificate verification is disabled
  repair: replace `verify=False` with `verify=True`
examples/vulnerable.py:13:4 SR004 medium Debug mode is enabled
  repair: replace `debug=True` with `debug=False`
```

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

The CI workflow runs the test suite on Python 3.10 through 3.13.

## Project direction

See [ROADMAP.md](ROADMAP.md) for the public 90-day plan and [CONTRIBUTING.md](CONTRIBUTING.md) for ways to help. Small, well-tested rules and clear documentation improvements are especially welcome.

## Security

Please read [SECURITY.md](SECURITY.md) before reporting a vulnerability in the tool itself.

## License

MIT
