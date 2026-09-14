# Glow Score methodology / Metodología

The Glow Score (0–100) is the sum of 14 weighted checks:

| Check | Weight |
|-------|--------|
| README.md exists | 15 |
| README has clear sections (≥3 headings) | 10 |
| README is substantial (>1200 chars) | 5 |
| LICENSE present | 15 |
| .gitignore present | 5 |
| CI workflow configured (`.github/workflows/*.yml`) | 10 |
| Tests found (`tests/`, `test/` or `test_*.py`) | 10 |
| Packaging metadata (pyproject/setup/package.json/…) | 7 |
| Project description declared | 5 |
| CONTRIBUTING.md | 5 |
| docs/ folder | 3 |
| CHANGELOG.md | 4 |
| CODE_OF_CONDUCT.md | 3 |
| SECURITY.md | 3 |
| **Total** | **100** |

Grades: 90+ 🌟 Glow Master · 70+ ✨ Shiny · 50+ 💡 Getting there · <50 🌑 Dark mode.

## Design principles

- **Local only.** No network calls, no telemetry, no accounts.
- **Stdlib only.** One Python file, any interpreter ≥3.8.
- **Actionable.** Every failed check prints the exact fix.
