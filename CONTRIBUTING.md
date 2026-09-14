# Contributing

Thanks for your interest in improving **repo-glow**!

1. Fork the repo and create your branch from `main`.
2. Run the tests: `python -m unittest discover -v`.
3. Dogfooding rule: **your PR must not lower the Glow Score of this repo**
   (`python repo_glow.py audit .` before and after your changes).
4. Keep it dependency-free: stdlib only, Python 3.8+ compatible.
5. Open a Pull Request with a clear description of what and why.

## Ideas that would make great PRs

- `--json` output for CI integrations
- GitHub Action that comments the score on PRs
- New checks: topics hygiene, badge linting, `.env.example` presence
- i18n of the report (ES/EN output)
