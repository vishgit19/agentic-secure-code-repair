# Roadmap

This roadmap keeps the project—and the broader public engineering portfolio around it—focused on verifiable work instead of activity for activity's sake.

## Days 1–30: foundation

- [x] Publish an explainable scanner MVP with tests and CI.
- [x] Add contribution, conduct, and security guidance.
- [ ] Add SARIF output for GitHub code scanning.
- [ ] Add a `pyproject.toml` configuration section for include/exclude rules.
- [ ] Document false-positive examples for every rule.
- [ ] Complete the GitHub profile README and pin 4–6 representative repositories.

Success signal: a new contributor can install the project, understand a finding, run tests, and choose a scoped issue without private guidance.

## Days 31–60: evidence of engineering depth

- [ ] Create a benchmark corpus with vulnerable and fixed examples.
- [ ] Add property-based or fuzz tests for patch generation.
- [ ] Publish a short technical write-up explaining trust boundaries in automated repair.
- [ ] Submit two small, maintainer-requested pull requests to active Python security or developer-tooling projects.

Success signal: measurable recall/false-positive data and at least one externally reviewed contribution.

## Days 61–90: useful automation

- [ ] Add a GitHub Action that comments with a patch preview on pull requests.
- [ ] Evaluate an optional model-assisted explanation layer behind an explicit flag.
- [ ] Record repair decisions and confidence so every suggestion remains auditable.
- [ ] Tag a documented `v0.2.0` release.

Success signal: the project helps on a real repository and has a release another developer can reproduce.

## Weekly operating rhythm

- one focused project improvement with tests;
- one issue triage or documentation improvement;
- one hour reading contribution guides and reproducing an upstream issue;
- at most one upstream pull request, only when it solves a confirmed maintainer need;
- a Friday review of open issues, CI health, and next week's single priority.

The goal is not a perfect green contribution graph. The goal is a trail of work that a hiring manager or maintainer can inspect and trust.
