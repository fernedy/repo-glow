import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import repo_glow


def make_repo(files):
    tmp = tempfile.mkdtemp()
    for name, content in files.items():
        path = os.path.join(tmp, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
    return tmp


GOOD_README = "# Project\n\n## Install\n\npip install thing\n\n## Usage\n\nRun `thing`.\n\n" + "x" * 1300


class ScoringTests(unittest.TestCase):
    def test_empty_repo_scores_zero(self):
        root = make_repo({})
        state = repo_glow.collect_state(root)
        score, results = repo_glow.score_state(state)
        self.assertEqual(score, 0)
        self.assertEqual(len(results), len(repo_glow.CHECKS))

    def test_perfect_repo_scores_100(self):
        root = make_repo({
            "README.md": GOOD_README,
            "LICENSE": "MIT",
            ".gitignore": "__pycache__/\n",
            "pyproject.toml": '[project]\nname = "thing"\ndescription = "A thing"\n',
            "CONTRIBUTING.md": "# Contributing\n",
            "CHANGELOG.md": "# Changelog\n",
            "CODE_OF_CONDUCT.md": "# Conduct\n",
            "SECURITY.md": "# Security\n",
            "tests/test_thing.py": "def test_x():\n    assert True\n",
            ".github/workflows/ci.yml": "name: ci\n",
            "docs/guide.md": "# Guide\n",
        })
        state = repo_glow.collect_state(root)
        score, results = repo_glow.score_state(state)
        self.assertEqual(score, 100, str([r for r in results if not r["ok"]]))

    def test_package_json_description_detected(self):
        root = make_repo({"package.json": '{"name": "x", "description": "does x"}\n'})
        state = repo_glow.collect_state(root)
        self.assertTrue(state["description"])

    def test_weights_sum_to_100(self):
        self.assertEqual(sum(w for _, w, _, _ in repo_glow.CHECKS), 100)

    def test_alternate_readme_case_detected(self):
        root = make_repo({"ReadMe.md": "# Hi\n"})
        state = repo_glow.collect_state(root)
        self.assertTrue(state["readme"].strip())

    def test_loose_test_file_detected(self):
        root = make_repo({"test_thing.py": "pass\n"})
        state = repo_glow.collect_state(root)
        self.assertTrue(state["tests"])


class ShareTests(unittest.TestCase):
    def test_badge_contains_score_and_color(self):
        badge = repo_glow.badge_markdown(95, "demo")
        self.assertIn("95%2F100", badge)
        self.assertIn("00A884", badge)

    def test_share_block_links_to_repo(self):
        block = repo_glow.share_block("/tmp/demo", 72)
        self.assertIn("github.com/fernedy/repo-glow", block)
        self.assertIn("72", block)

    def test_grades_ordered(self):
        self.assertIn("🌟", repo_glow.grade_for(95)[0])
        self.assertIn("✨", repo_glow.grade_for(75)[0])
        self.assertIn("💡", repo_glow.grade_for(55)[0])
        self.assertIn("🌑", repo_glow.grade_for(10)[0])


class FixTests(unittest.TestCase):
    def test_fix_creates_basics_once(self):
        root = make_repo({})
        rc = repo_glow.cmd_fix(root)
        self.assertEqual(rc, 0)
        self.assertTrue(os.path.isfile(os.path.join(root, "LICENSE")))
        self.assertTrue(os.path.isfile(os.path.join(root, ".gitignore")))
        self.assertTrue(os.path.isfile(os.path.join(root, "CONTRIBUTING.md")))
        # second run must not overwrite
        license_before = open(os.path.join(root, "LICENSE"), encoding="utf-8").read()
        repo_glow.cmd_fix(root)
        self.assertEqual(open(os.path.join(root, "LICENSE"), encoding="utf-8").read(), license_before)
        shutil.rmtree(root)

    def test_audit_missing_path_exit_code(self):
        self.assertEqual(repo_glow.cmd_audit("/nonexistent-path-xyz"), 2)


if __name__ == "__main__":
    unittest.main()
