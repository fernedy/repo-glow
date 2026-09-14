#!/usr/bin/env python3
"""
repo-glow — Audit how shiny your repository looks and get a Glow Score (0-100).

Zero dependencies. Python 3.8+. Stdlib only.

Usage:
    python repo_glow.py audit <path> [--share]
    python repo_glow.py fix <path>
    python repo_glow.py fix <path> --ai

Exit codes: 0 = ok, 1 = usage error, 2 = path not found.
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys

SCORE_TARGET = 100

# (key, weight, title, hint) — total weight must equal SCORE_TARGET
CHECKS = [
    ("readme",          15, "README.md exists",                 "Add a README.md — it is the front door of your repo."),
    ("readme_sections", 10, "README has clear sections",        "Add markdown headings (## Quickstart, ## Install...)."),
    ("readme_depth",     5, "README is substantial",            "Explain what, why and how in your README (>1200 chars)."),
    ("license",         15, "LICENSE present",                  "Add a LICENSE so others know they can use it."),
    ("gitignore",        5, ".gitignore present",               "Add a .gitignore (IDE folders and pycache leak easily)."),
    ("ci",              10, "CI workflow configured",           "Add .github/workflows/*.yml so tests run on every push."),
    ("tests",           10, "Tests found",                      "Add tests/ or test_*.py — trust is built on tests."),
    ("packaging",        7, "Packaging metadata",               "Add pyproject.toml / setup.py / package.json."),
    ("description",      5, "Project description declared",     "Declare a description in packaging metadata."),
    ("contributing",     5, "CONTRIBUTING.md present",          "Tell contributors how to help."),
    ("docs_dir",         3, "docs/ folder",                     "Move long-form docs into docs/."),
    ("changelog",        4, "CHANGELOG.md present",             "Track notable changes in a CHANGELOG.md."),
    ("conduct",          3, "Code of Conduct present",          "Add CODE_OF_CONDUCT.md for a healthy community."),
    ("security",         3, "SECURITY.md present",              "Add SECURITY.md with a disclosure contact."),
]

GRADE_ICONS = [
    (90, "🌟 Glow Master", "00A884"),
    (70, "✨ Shiny",        "00C896"),
    (50, "💡 Getting there", "F5A623"),
    (0,  "🌑 Dark mode",    "9C27B0"),
]


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def _heading_count(text):
    return len(re.findall(r"^#{1,6}\s+\S", text, flags=re.MULTILINE))


def collect_state(root):
    """Gather every fact the scoring needs from a repo directory."""
    state = {"root": root}
    readme = ""
    for name in ("README.md", "readme.md", "Readme.md", "README.rst", "README.txt", "ReadMe.md"):
        p = os.path.join(root, name)
        if os.path.isfile(p):
            readme = _read(p)
            break
    state["readme"] = readme
    state["readme_sections"] = _heading_count(readme)

    state["license"] = any(
        os.path.isfile(os.path.join(root, n))
        for n in ("LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE", "license")
    )
    state["gitignore"] = os.path.isfile(os.path.join(root, ".gitignore"))

    wf_dir = os.path.join(root, ".github", "workflows")
    state["ci"] = os.path.isdir(wf_dir) and any(
        f.endswith((".yml", ".yaml")) for f in os.listdir(wf_dir)
    )

    state["tests"] = os.path.isdir(os.path.join(root, "tests")) or os.path.isdir(
        os.path.join(root, "test")
    ) or bool(
        [f for f in os.listdir(root) if f.startswith("test_") and f.endswith(".py")]
    )

    packaging = [n for n in ("pyproject.toml", "setup.py", "setup.cfg", "package.json", "Cargo.toml", "go.mod")
                 if os.path.isfile(os.path.join(root, n))]
    state["packaging"] = bool(packaging)

    description = ""
    pj = os.path.join(root, "package.json")
    if os.path.isfile(pj):
        try:
            with open(pj, "r", encoding="utf-8", errors="replace") as fh:
                description = (json.load(fh).get("description") or "").strip()
        except (ValueError, OSError):
            pass
    if not description:
        pt = os.path.join(root, "pyproject.toml")
        if os.path.isfile(pt):
            m = re.search(r'^description\s*=\s*"([^"]+)"', _read(pt), flags=re.MULTILINE)
            if m:
                description = m.group(1).strip()
    state["description"] = bool(description)

    state["contributing"] = os.path.isfile(os.path.join(root, "CONTRIBUTING.md"))
    state["docs_dir"] = os.path.isdir(os.path.join(root, "docs"))
    state["changelog"] = any(
        os.path.isfile(os.path.join(root, n))
        for n in ("CHANGELOG.md", "CHANGES.md", "HISTORY.md")
    )
    state["conduct"] = any(
        os.path.isfile(os.path.join(root, n))
        for n in ("CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.md")
    )
    state["security"] = os.path.isfile(os.path.join(root, "SECURITY.md"))
    return state


def score_state(state):
    """Return (total_score, [results]) with one result per check."""
    results = []
    for key, weight, title, hint in CHECKS:
        if key == "readme":
            ok = bool(state["readme"].strip())
        elif key == "readme_sections":
            ok = state["readme_sections"] >= 3
        elif key == "readme_depth":
            ok = len(state["readme"]) >= 1200
        else:
            ok = bool(state.get(key))
        results.append({"key": key, "weight": weight, "title": title,
                        "hint": hint, "ok": ok, "points": weight if ok else 0})
    return sum(r["points"] for r in results), results


def grade_for(score):
    for threshold, label, color in GRADE_ICONS:
        if score >= threshold:
            return label, color
    return GRADE_ICONS[-1][1], GRADE_ICONS[-1][2]


def badge_markdown(score, repo="repo-glow"):
    _, color = grade_for(score)
    return f"![{repo} glow score](https://img.shields.io/badge/repo_glow-{score}%2F100-{color}?style=flat-square&logo=github)"


def share_block(root, score):
    name = os.path.basename(os.path.abspath(root)) or "my-repo"
    label, _ = grade_for(score)
    return (
        f"<!-- repo-glow share block: paste this in your README, PR or post -->\n"
        f"### {name} — {label}\n"
        f"{badge_markdown(score, name)}\n\n"
        f"Audited with [repo-glow](https://github.com/fernedy/repo-glow) — "
        f"zero dependencies, one command: `python repo_glow.py audit . --share`"
    )


def bar(score, width=30):
    filled = round(width * score / SCORE_TARGET)
    return "[" + "█" * filled + "░" * (width - filled) + "]"


def c(text, code):
    if sys.stdout.isatty():
        return f"\033[{code}m{text}\033[0m"
    return text


def cmd_audit(root, share=False):
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        print(c(f"error: not a directory: {root}", "1;31"))
        return 2
    state = collect_state(root)
    score, results = score_state(state)
    label, color = grade_for(score)
    print()
    print(c(f"  ✨ REPO GLOW — {os.path.basename(root)}", "1;36"))
    print(f"  {bar(score)}  {c(str(score) + '/100', '1;37')}  {label}")
    print()
    for r in results:
        mark = c("✔", "1;32") if r["ok"] else c("✘", "1;31")
        pts = f"+{r['points']:>2}"
        print(f"  {mark} {pts}  {r['title']}")
        if not r["ok"]:
            print(c(f"        ↳ {r['hint']}", "90"))
    print()
    if share:
        print(c("  --- share block (copy from the line below) ---", "1;35"))
        print()
        print(share_block(root, score))
        print()
    else:
        print(c("  Tip: run with --share to get a badge block for your README.", "90"))
        print()
    return 0


MIT_TEMPLATE = """MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

GITIGNORE_TEMPLATE = """__pycache__/
*.py[cod]
.venv/
venv/
.env
.idea/
.vscode/
dist/
build/
*.egg-info/
node_modules/
.DS_Store
"""

CONTRIBUTING_TEMPLATE = """# Contributing

Thanks for your interest in improving this project!

1. Fork the repo and create your branch from `main`.
2. Run the tests: `python -m unittest discover -v` (or your project's runner).
3. Keep the repo shiny: `python repo_glow.py audit .` should not drop in score.
4. Open a Pull Request with a clear description.
"""


def _write_if_absent(path, content):
    if os.path.exists(path):
        return False
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return True


def ai_description(root):
    """Optional AI mode: ask a local agent CLI (e.g. `opencode`) for a one-liner."""
    prompt = (
        "Read the repository at " + os.path.abspath(root) + ". "
        "Write ONE sentence (max 120 chars) describing what this project does, "
        "for a GitHub repo 'About' field. Output only the sentence."
    )
    for argv in (["opencode", "run", prompt],):
        try:
            out = subprocess.run(argv, capture_output=True, text=True, timeout=120)
            text = (out.stdout or "").strip()
            if out.returncode == 0 and text:
                return text.splitlines()[0][:140]
        except (OSError, subprocess.TimeoutExpired):
            continue
    return None


def cmd_fix(root, use_ai=False):
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        print(c(f"error: not a directory: {root}", "1;31"))
        return 2
    created = []
    if _write_if_absent(os.path.join(root, "LICENSE"),
                        MIT_TEMPLATE.format(year=datetime.date.today().year, author="Your Name")):
        created.append("LICENSE (MIT) — remember to set your name")
    if _write_if_absent(os.path.join(root, ".gitignore"), GITIGNORE_TEMPLATE):
        created.append(".gitignore")
    if _write_if_absent(os.path.join(root, "CONTRIBUTING.md"), CONTRIBUTING_TEMPLATE):
        created.append("CONTRIBUTING.md")
    if created:
        for item in created:
            print(c(f"  ✔ created {item}", "1;32"))
    else:
        print("  Nothing to create — LICENSE, .gitignore and CONTRIBUTING.md already exist.")
    if use_ai:
        print(c("  🤖 asking the local agent for a description...", "1;35"))
        desc = ai_description(root)
        if desc:
            print(c(f"  AI suggestion: {desc}", "1;36"))
            print(c("  → set it with: gh repo edit --description \"<text>\"", "90"))
        else:
            print(c("  No local agent CLI available (tried: opencode). Skipping AI step.", "90"))
    before, _ = score_state(collect_state(root))
    print(f"  Glow score is now {before}/100 — run `python repo_glow.py audit .` for details.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="repo-glow",
        description="Audit how shiny your repository looks. Zero dependencies.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_audit = sub.add_parser("audit", help="score a repository (0-100)")
    p_audit.add_argument("path", nargs="?", default=".", help="repo path (default: .)")
    p_audit.add_argument("--share", action="store_true",
                         help="print a shareable markdown badge block")

    p_fix = sub.add_parser("fix", help="create the missing basics (LICENSE, .gitignore, CONTRIBUTING)")
    p_fix.add_argument("path", nargs="?", default=".", help="repo path (default: .)")
    p_fix.add_argument("--ai", action="store_true",
                       help="ask a local agent CLI (opencode) for a repo description")

    args = parser.parse_args(argv)
    if args.command == "audit":
        return cmd_audit(args.path, share=args.share)
    return cmd_fix(args.path, use_ai=args.ai)


if __name__ == "__main__":
    sys.exit(main())
