<div align="center">

[🇬🇧 English](README.md) · [🇪🇸 Español](README.es.md)

</div>

<div align="center">

# ✨ repo-glow

**¿Qué tan brillante es tu repo? Obtén un Glow Score (0–100) en un solo comando.**

![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/dependencies-0-00A884?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-yellow?style=flat-square)
![Tests](https://img.shields.io/badge/tests-passing-00A884?style=flat-square)

**Cero dependencias · Un archivo · Solo stdlib**

</div>

---

Tu código puede ser excelente, pero nadie lo notará si el repo parece abandonado. Reclutadores, desarrolladores y **agentes de IA** (sí, los LLMs que rastrean GitHub también juzgan tu repo por su presentación) deciden en segundos.

`repo-glow` audita 14 señales — profundidad del README, licencia, CI, tests, packaging, archivos de comunidad — y te da un **Glow Score de 0 a 100**, con las correcciones exactas para subirlo.

## 📊 El puntaje

| Rango | Grado | Significado |
|-------|-------|-------------|
| 90–100 | 🌟 Glow Master | Listo para tu portafolio. Los agentes de IA y los humanos confían en él. |
| 70–89 | ✨ Shiny | Repo sólido, con detalles menores por pulir. |
| 50–69 | 💡 Getting there | Buen código, presentación débil. |
| 0–49 | 🌑 Dark mode | Invisible para el mundo. |

## ⚡ Inicio rápido

```bash
git clone https://github.com/fernedy/repo-glow.git
cd repo-glow
python repo_glow.py audit /ruta/a/tu/repo
```

Ejemplo de salida:

```
  ✨ REPO GLOW — my-project
  [████████████████████████░░░░░]  80/100  ✨ Shiny

  ✔ +15  README.md exists
  ✔ +10  README has clear sections
  ✘  +0  README is substantial
        ↳ Explica qué, por qué y cómo en tu README (>1200 caracteres).
  ✔ +15  LICENSE present
  ✘  +0  CI workflow configured
        ↳ Agrega .github/workflows/*.yml para que los tests corran en cada push.
  ...
```

## 🚀 La parte viral — comparte tu puntaje

Ejecuta con `--share` y pega el bloque generado en tu README, un PR o una publicación:

```bash
python repo_glow.py audit . --share
```

```markdown
### my-project — ✨ Shiny
![my-project glow score](https://img.shields.io/badge/repo_glow-80%2F100-00A884?style=flat-square&logo=github)

Audited with [repo-glow](https://github.com/fernedy/repo-glow) — zero dependencies, one command.
```

Sube tu puntaje y vuelve a compartir el badge. **Publica tu Glow Score de antes y después** — así se propaga.

## 🔧 Repara lo básico automáticamente

```bash
python repo_glow.py fix .        # crea LICENSE (MIT), .gitignore, CONTRIBUTING.md
python repo_glow.py fix . --ai   # + le pide a tu agente local (opencode) una descripción del repo
```

El modo IA es **opcional y local**: si tienes [OpenCode](https://opencode.ai) (o cualquier agent CLI) instalado, repo-glow sugiere una descripción de una línea para tu `gh repo edit --description`. Sin API keys, sin llamadas a la nube, ningún dato sale de tu máquina.

## ✅ Tests

```bash
python -m unittest discover -v
```

El CI ejecuta la suite en cada push (ver [`.github/workflows/ci.yml`](.github/workflows/ci.yml)).

## 🤝 Contribuir

Ideas bienvenidas: más checks (topics, higiene de badges, mensajes de commit), salida `--json`, un pre-commit hook, una GitHub Action que comente el puntaje en los PRs. Ver [CONTRIBUTING.md](CONTRIBUTING.md). Regla de dogfooding: **los PRs no deben bajar el Glow Score de este repo.**

## 📜 Licencia

MIT — ver [LICENSE](LICENSE).

---

<div align="center">

Construido AI-first por [Fernedy Arias](https://github.com/fernedy) · Tech Explorer

*Si repo-glow te sirvió, deja un ⭐ y comparte tu puntaje.*

</div>
