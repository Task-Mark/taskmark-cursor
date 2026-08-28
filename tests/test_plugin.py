from __future__ import annotations

import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "taskmark"
FORBIDDEN_BOARD_FILES = {"INDEX.md", "SIZING.md", "VELOCITY.md", "README.md"}


class PluginSurfaceTests(unittest.TestCase):
    def test_exactly_four_user_commands(self) -> None:
        commands = {path.stem for path in (PLUGIN / "commands").glob("*.md")}
        self.assertEqual(
            commands, {"tkmd-init", "tkmd-create", "tkmd-commit", "tkmd-do"}
        )

    def test_only_required_scripts_remain(self) -> None:
        scripts = {path.name for path in (PLUGIN / "scripts").iterdir()}
        self.assertEqual(
            scripts,
            {
                "allocate-id.py",
                "commit-all-repos.sh",
                "ensure-board-ui.py",
                "git-identity.py",
                "rsync-plugin-local.sh",
                "sync-taskmark-repos.sh",
            },
        )

    def test_only_required_skills_remain(self) -> None:
        skills = {
            path.parent.name for path in (PLUGIN / "skills").glob("*/SKILL.md")
        }
        self.assertEqual(
            skills,
            {
                "commit-all",
                "sync-plugin-local",
                "sync-taskmark-repos",
                "taskmark-conventions",
                "taskmark-init",
                "tkmd-create",
                "tkmd-do",
            },
        )
        self.assertFalse(
            any(path.is_file() for path in (ROOT / "examples" / "sample-board").rglob("*"))
        )
        self.assertFalse(
            any(
                path.is_file()
                for path in (PLUGIN / "examples" / "sample-board").rglob("*")
            )
        )

    def test_allocator_is_collision_resistant_and_legacy_compatible(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            board = Path(tmp)
            (board / "legacy.md").write_text("---\nid: T-297\n---\n", encoding="utf-8")
            values = {
                subprocess.check_output(
                    [
                        "python3",
                        str(PLUGIN / "scripts" / "allocate-id.py"),
                        "T",
                        str(board),
                        "--identity",
                        "MM",
                    ],
                    text=True,
                ).strip()
                for _ in range(20)
            }
            self.assertEqual(len(values), 20)
            self.assertTrue(all(re.fullmatch(r"T-MM-[a-f0-9]{8}", value) for value in values))
            accepted = re.compile(
                r"^[ESBT]-(?:[0-9]{3}|[A-Z0-9]{2,12}-[a-z0-9]{8,})$"
            )
            self.assertRegex("T-297", accepted)
            self.assertRegex(next(iter(values)), accepted)

    def test_agent_sessions_log_prompt_on_matching_leaf(self) -> None:
        do_skill = (PLUGIN / "skills" / "tkmd-do" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        memory = (PLUGIN / "rules" / "taskmark-project-memory.mdc").read_text(
            encoding="utf-8"
        )
        conventions = (PLUGIN / "skills" / "taskmark-conventions" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Prompt & feedback", do_skill)
        self.assertIn("Create a new leaf only when", do_skill)
        self.assertIn("Prompt & feedback", memory)
        self.assertIn("done leaf", conventions)
        self.assertIn("no estimate or owner property", conventions)
        self.assertIn("closed Started → Ended intervals", conventions)

    def test_init_helpers_create_only_storage_and_local_repos(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            repo = Path(tmp) / "product"
            board = repo / "taskmark"
            board.mkdir(parents=True)
            subprocess.run(["git", "init", str(repo)], check=True, capture_output=True)
            (board / "epics").mkdir()

            subprocess.run(
                [
                    "python3",
                    str(PLUGIN / "scripts" / "ensure-board-ui.py"),
                    str(board),
                    "--name",
                    "test-taskmark",
                ],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                [str(PLUGIN / "scripts" / "sync-taskmark-repos.sh"), str(repo)],
                check=True,
                capture_output=True,
            )

            self.assertTrue((board / "REPOS.md").exists())
            self.assertNotIn("Last synced", (board / "REPOS.md").read_text(encoding="utf-8"))
            ignored = subprocess.run(
                ["git", "-C", str(repo), "check-ignore", "taskmark/REPOS.md"],
                capture_output=True,
            )
            self.assertEqual(ignored.returncode, 0)
            self.assertFalse(FORBIDDEN_BOARD_FILES.intersection(p.name for p in board.iterdir()))


if __name__ == "__main__":
    unittest.main()
