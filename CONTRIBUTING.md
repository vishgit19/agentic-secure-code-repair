# Contributing

Thanks for considering a contribution. This project is intentionally small, so a focused pull request with a clear test is more valuable than a broad rewrite.

## Good contributions

- a Python security rule with low false-positive risk;
- a failing test that demonstrates a real bug;
- clearer documentation or a reproducible example;
- output formats that help developers use findings in CI.

Please open an issue before starting a large change.

## Local setup

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

## Adding a rule

1. Give the rule a stable `SRxxx` identifier.
2. Explain the risky behavior in plain language.
3. Add positive and negative tests.
4. Offer a patch preview only if the replacement is narrow and reviewable.
5. Update the rule table in `README.md`.

## Pull requests

Keep commits focused and include the motivation, behavior change, and validation steps in the pull request description. By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).
