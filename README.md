<div align="center">

# ✨ repo-glow

**How shiny is your repo? Get a Glow Score (0–100) in one command.**

*¿Qué tan brillante es tu repo? Obtén un Glow Score (0–100) en un solo comando.*

![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/dependencies-0-00A884?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-yellow?style=flat-square)
![Tests](https://img.shields.io/badge/tests-passing-00A884?style=flat-square)

**Zero dependencies · One file · Stdlib only**

</div>

---

Your code may be great, but nobody will ever know if the repo looks abandoned. Recruiters, developers and **AI agents** (yes, LLMs crawling GitHub judge your repo by its presentation too) decide in seconds.

`repo-glow` audits 14 signals — README depth, license, CI, tests, packaging, community files — and gives you a **Glow Score from 0 to 100**, with the exact fixes to raise it.

Tu código puede ser excelente, pero nadie lo notará si el repo parece abandonado. Reclutadores, desarrolladores y **agentes de IA** (sí, los LLMs que rastrean GitHub también juzgan tu repo por su presentación) deciden en segundos.

`repo-glow` audita 14 señales — profundidad del README, licencia, CI, tests, packaging, archivos de comunidad — y te da un **Glow Score de 0 a 100**, con las correcciones exactas para subirlo.

## 📊 The score / El puntaje

| Range | Grade | Meaning |
|-------|-------|---------|
| 90–100 | 🌟 Glow Master | Portfolio-ready. AI agents and humans trust it. |
| 70–89 | ✨ Shiny | Solid repo, small gaps left. |
| 50–69 | 💡 Getting there | Good code, weak presentation. |
| 0–49 | 🌑 Dark mode | Invisible to the world. |

## ⚡ Quickstart / Inicio rápido

```bash
git clone https://github.com/fernedy/repo-glow.git
cd repo-glow
python repo_glow.py audit /path/to/your/repo
```

Sample output:

```
  ✨ REPO GLOW — my-project
  [████████████████████████░░░░░]  80/100  ✨ Shiny

  ✔ +15  README.md exists
  ✔ +10  README has clear sections
  ✘  +0  README is substantial
        ↳ Explain what, why and how in your README (>1200 chars).
  ✔ +15  LICENSE present
  ✘  +0  CI workflow configured
        ↳ Add .github/workflows/*.yml so tests run on every push.
  ...
```

## 🚀 The viral part — share your score

Run with `--share` and paste the generated block into your README, a PR or a social post:

```bash
python repo_glow.py audit . --share
```

```markdown
### my-project — ✨ Shiny
![my-project glow score](https://img.shields.io/badge/repo_glow-80%2F100-00A884?style=flat-square&logo=github)

Audited with [repo-glow](https://github.com/fernedy/repo-glow) — zero dependencies, one command.
```

Raise your score, re-share the badge. **Post your before/after Glow Score** — that is how this spreads.

## 🔧 Fix the basics automatically

```bash
python repo_glow.py fix .        # creates LICENSE (MIT), .gitignore, CONTRIBUTING.md
python repo_glow.py fix . --ai   # + asks your local agent (opencode) for a repo description
```

The AI mode is **optional and local**: if you have [OpenCode](https://opencode.ai) (or any agent CLI) installed, repo-glow suggests a one-line description for your `gh repo edit --description`. No API keys, no cloud calls, no data leaves your machine.

## ✅ Tested / Probado

```bash
python -m unittest discover -v
```

CI runs the suite on every push (see [`.github/workflows/ci.yml`](.github/workflows/ci.yml)).

## 🤝 Contributing / Contribuir

Ideas welcome: more checks (topics, badges hygiene, commit messages), `--json` output, a pre-commit hook, a GitHub Action that comments the score on PRs. See [CONTRIBUTING.md](CONTRIBUTING.md). Dogfooding rule: **PRs must not lower the Glow Score of this repo.**

## 📜 License / Licencia

MIT — see [LICENSE](LICENSE).

---

<div align="center">

Built AI-first by [Fernedy Arias](https://github.com/fernedy) · Tech Explorer

*If repo-glow helped you, drop a ⭐ and share your score.*

</div>
