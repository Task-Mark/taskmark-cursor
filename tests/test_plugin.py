from __future__ import annotations

import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "taskmark"
FORBIDDEN_BOARD_FILES = {"INDEX.md", "SIZING.md", "VELOCITY.md", "README.md"}


class PluginSurfaceTests(unittest.TestCase):
    def test_user_commands_include_plan_do_and_save(self) -> None:
        commands = {path.stem for path in (PLUGIN / "commands").glob("*.md")}
        self.assertEqual(
            commands,
            {
                "tkmd-init",
                "tkmd-verify",
                "tkmd-plan",
                "tkmd-save",
                "tkmd-save-do",
                "tkmd-plan-do",
                "tkmd-commit",
                "tkmd-do",
                "tkmd-shelf",
                "tkmd-changelog",
                "tkmd-version",
                "tkmd-reportme",
            },
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
                "verify-board.py",
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
                "tkmd-verify",
                "tkmd-plan",
                "tkmd-plan-do",
                "tkmd-save",
                "tkmd-save-do",
                "tkmd-do",
                "tkmd-shelf",
                "tkmd-changelog",
                "tkmd-version",
                "tkmd-reportme",
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

    def test_plan_searches_fits_and_decomposes_hierarchy(self) -> None:
        plan_skill = (PLUGIN / "skills" / "tkmd-plan" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        plan_command = (PLUGIN / "commands" / "tkmd-plan.md").read_text(
            encoding="utf-8"
        )
        normalized_plan_skill = " ".join(plan_skill.split())

        for instruction in (
            "search all open and done epics, stories, tasks, and bugs",
            "exact or overlapping item",
            "smallest useful hierarchy",
            "initiative/outcome → epic",
            "user-visible capability → story",
            "executable unit → task",
            "defect/regression → bug",
            "independently executable task/bug leaves",
            "Use static sizing as a decomposition driver",
            "Strongly split XL",
            "never leave it unrefined",
            "parent: <story-id>",
            "parent: <epic-id>",
            "Never edit an existing `epic.md`, `story.md`, or leaf",
            "Every newly planned task/bug leaf must include a `prompt` row",
            "taskmark.writingLanguage",
        ):
            self.assertIn(instruction, normalized_plan_skill)
        self.assertIn("Use the `tkmd-plan` skill", plan_command)

    def test_plan_do_composes_plan_then_do_on_new_items_only(self) -> None:
        skill = (PLUGIN / "skills" / "tkmd-plan-do" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        command = (PLUGIN / "commands" / "tkmd-plan-do.md").read_text(
            encoding="utf-8"
        )
        normalized = " ".join(skill.split())
        normalized_command = " ".join(command.split())

        for instruction in (
            "Follow the `tkmd-plan` skill in full",
            "create nothing",
            "Do not start implementation",
            "highest new parent",
            "each newly created leaf",
            "Never run `git commit`",
            "Never set an item to `in_progress`",
        ):
            self.assertIn(instruction, normalized)
        self.assertIn("Use the `tkmd-plan-do` skill", normalized_command)
        self.assertIn("never commits or pushes", normalized_command)

    def test_save_reads_cursor_plans_and_carries_visuals(self) -> None:
        skill = (PLUGIN / "skills" / "tkmd-save" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        command = (PLUGIN / "commands" / "tkmd-save.md").read_text(
            encoding="utf-8"
        )
        memory = (PLUGIN / "rules" / "taskmark-project-memory.mdc").read_text(
            encoding="utf-8"
        )
        normalized = " ".join(skill.split())
        normalized_command = " ".join(command.split())

        for instruction in (
            "explicit plan path",
            "~/.cursor/plans/",
            ".cursor/plans/",
            "exact or overlapping item already covers the plan",
            "initiative/outcome → epic",
            "Mermaid fences",
            "Absence of visuals is not an error",
            "Never run `git commit`",
            "Never set an item to `in_progress`",
        ):
            self.assertIn(instruction, normalized)
        self.assertIn("Use the `tkmd-save` skill", normalized_command)
        self.assertIn("/tkmd-save", memory)
        self.assertIn("/tkmd-save-do", memory)
        self.assertIn("/tkmd-plan-do", memory)

    def test_save_do_composes_save_then_do_on_new_items_only(self) -> None:
        skill = (PLUGIN / "skills" / "tkmd-save-do" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        command = (PLUGIN / "commands" / "tkmd-save-do.md").read_text(
            encoding="utf-8"
        )
        normalized = " ".join(skill.split())
        normalized_command = " ".join(command.split())

        for instruction in (
            "Follow the `tkmd-save` skill in full",
            "create nothing",
            "Do not start implementation",
            "highest new parent",
            "each newly created leaf",
            "Never run `git commit`",
            "Never set an item to `in_progress`",
        ):
            self.assertIn(instruction, normalized)
        self.assertIn("Use the `tkmd-save-do` skill", normalized_command)
        self.assertIn("never commits or pushes", normalized_command)

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

    def test_identity_token_keeps_diacritics_inside_words(self) -> None:
        import importlib.util
        import unicodedata

        spec = importlib.util.spec_from_file_location(
            "git_identity", PLUGIN / "scripts" / "git-identity.py"
        )
        git_identity = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(git_identity)
        alloc_spec = importlib.util.spec_from_file_location(
            "allocate_id", PLUGIN / "scripts" / "allocate-id.py"
        )
        allocate_id = importlib.util.module_from_spec(alloc_spec)
        assert alloc_spec.loader is not None
        alloc_spec.loader.exec_module(allocate_id)

        nfc = "Marco Mendão"
        nfd = unicodedata.normalize("NFD", nfc)
        for spelling in (nfc, nfd):
            self.assertEqual(git_identity.identity_token(spelling), "MM")
            self.assertEqual(
                git_identity.identity_token(spelling),
                git_identity.derive_initials(spelling),
            )
            self.assertEqual(
                allocate_id.identity_token(spelling),
                git_identity.derive_initials(spelling),
            )
        self.assertNotEqual(git_identity.identity_token(nfc), "MO")
        self.assertEqual(git_identity.identity_token("Jane Doe"), "JD")
        self.assertEqual(git_identity.identity_token("Alice"), "AL")
        self.assertRegex(git_identity.identity_token(nfc), r"^[A-Z0-9]{2,12}$")
        self.assertRegex(
            "B-MO-f9467ca2",
            re.compile(r"^[ESBT]-(?:[0-9]{3}|[A-Z0-9]{2,12}-[a-z0-9]{8,})$"),
        )

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
        self.assertIn("taskmark.writingLanguage", conventions)
        self.assertNotIn("Portuguese-only", conventions)
        self.assertIn("board writing language", memory)
        self.assertIn("board writing language", do_skill)

    def test_changelog_skills_follow_board_language_not_hardcoded_portuguese(self) -> None:
        changelog = (PLUGIN / "skills" / "tkmd-changelog" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        version = (PLUGIN / "skills" / "tkmd-version" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        conventions = (PLUGIN / "skills" / "taskmark-conventions" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        plugin_readme = (PLUGIN / "README.md").read_text(encoding="utf-8")
        init_skill = (PLUGIN / "skills" / "taskmark-init" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        init_command = (PLUGIN / "commands" / "tkmd-init.md").read_text(encoding="utf-8")
        self.assertIn("writingLanguage", changelog)
        self.assertIn("board writing language", changelog)
        self.assertNotIn("Portuguese Keep a Changelog", changelog)
        self.assertIn("board writing language", version)
        self.assertIn("Keep a Changelog structure in the **board writing", conventions)
        self.assertIn("independent", plugin_readme)
        self.assertIn("writing language", init_skill)
        self.assertIn("writing language", init_command)
        self.assertIn("--writing-language", init_skill)

    def test_do_parent_target_requires_every_open_descendant(self) -> None:
        do_skill = (PLUGIN / "skills" / "tkmd-do" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        do_command = (PLUGIN / "commands" / "tkmd-do.md").read_text(
            encoding="utf-8"
        )
        normalized_do_skill = " ".join(do_skill.split())
        normalized_do_command = " ".join(do_command.split())

        self.assertIn(
            "Every open, non-cancelled, non-shelved descendant is",
            normalized_do_skill,
        )
        self.assertIn(
            "requires zero open, non-cancelled, non-shelved task/bug leaves",
            normalized_do_skill,
        )
        self.assertIn(
            "every open, non-cancelled, non-shelved descendant leaf",
            normalized_do_command,
        )
        self.assertIn(
            "Do not stop successfully until all required descendants are done",
            normalized_do_command,
        )

    def test_ensure_board_ui_merges_writing_language_without_clobber(self) -> None:
        script = PLUGIN / "scripts" / "ensure-board-ui.py"
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            board = Path(tmp) / "board"
            board.mkdir()
            extra = {"name": "keep-me", "customKey": "stay", "version": "9.9.9"}
            (board / "package.json").write_text(
                json.dumps(extra, indent=2) + "\n", encoding="utf-8"
            )
            subprocess.run(
                ["python3", str(script), str(board), "--writing-language", "English"],
                check=True,
                capture_output=True,
            )
            pkg = json.loads((board / "package.json").read_text(encoding="utf-8"))
            self.assertEqual(pkg["customKey"], "stay")
            self.assertEqual(pkg["version"], "9.9.9")
            self.assertEqual(pkg["taskmark"]["writingLanguage"], "English")

            subprocess.run(
                ["python3", str(script), str(board), "--writing-language", "Português"],
                check=True,
                capture_output=True,
            )
            pkg = json.loads((board / "package.json").read_text(encoding="utf-8"))
            self.assertEqual(pkg["taskmark"]["writingLanguage"], "English")
            self.assertEqual(pkg["customKey"], "stay")

            subprocess.run(
                [
                    "python3",
                    str(script),
                    str(board),
                    "--writing-language",
                    "Português",
                    "--replace-writing-language",
                ],
                check=True,
                capture_output=True,
            )
            pkg = json.loads((board / "package.json").read_text(encoding="utf-8"))
            self.assertEqual(pkg["taskmark"]["writingLanguage"], "Português")
            self.assertEqual(pkg["customKey"], "stay")
            self.assertFalse(FORBIDDEN_BOARD_FILES.intersection(p.name for p in board.iterdir()))

    def test_shelf_command_and_skill_define_terminal_leaf_writes(self) -> None:
        shelf_skill = (PLUGIN / "skills" / "tkmd-shelf" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        shelf_command = (PLUGIN / "commands" / "tkmd-shelf.md").read_text(
            encoding="utf-8"
        )
        normalized_skill = " ".join(shelf_skill.split())
        normalized_command = " ".join(shelf_command.split())

        for instruction in (
            "status: shelved",
            "Never run `git commit`",
            "Never edit epic or story markdown",
            "Never set `cancelled: true`",
            "open, non-cancelled, non-shelved",
            "Set `updated` and `completed_at`",
            "Preserve `cancelled: false`",
        ):
            self.assertIn(instruction, normalized_skill)
        self.assertIn("Use the `tkmd-shelf` skill", normalized_command)
        self.assertIn("never commits or pushes", normalized_command)

    def test_reportme_reports_own_done_work_since_last_report(self) -> None:
        skill = (PLUGIN / "skills" / "tkmd-reportme" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        command = (PLUGIN / "commands" / "tkmd-reportme.md").read_text(
            encoding="utf-8"
        )
        memory = (PLUGIN / "rules" / "taskmark-project-memory.mdc").read_text(
            encoding="utf-8"
        )
        conventions = (PLUGIN / "skills" / "taskmark-conventions" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        normalized_skill = " ".join(skill.split())
        normalized_command = " ".join(command.split())

        for instruction in (
            ".reports/report-YYYYMMDD.md",
            "Never run `git commit`",
            "Never edit epic, story, or leaf markdown",
            "current git identity",
            "`resolvers` contain the current git identity",
            "Ignore a file dated today",
            "no earlier report exists",
            "taskmark.writingLanguage",
            "Never** include work-item codes",
        ):
            self.assertIn(instruction, normalized_skill)
        self.assertIn("Use the `tkmd-reportme` skill", normalized_command)
        self.assertIn("never commits or pushes", normalized_command)
        self.assertIn("/tkmd-reportme", memory)
        self.assertIn(".reports/", conventions)

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
            report_ignored = subprocess.run(
                [
                    "git",
                    "-C",
                    str(repo),
                    "check-ignore",
                    "taskmark/.reports/report-20260101.md",
                ],
                capture_output=True,
            )
            self.assertEqual(report_ignored.returncode, 0)
            self.assertFalse(FORBIDDEN_BOARD_FILES.intersection(p.name for p in board.iterdir()))

    def test_verify_skill_forbids_commit_and_generated_files(self) -> None:
        skill = (PLUGIN / "skills" / "tkmd-verify" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        command = (PLUGIN / "commands" / "tkmd-verify.md").read_text(
            encoding="utf-8"
        )
        memory = (PLUGIN / "rules" / "taskmark-project-memory.mdc").read_text(
            encoding="utf-8"
        )
        conventions = (PLUGIN / "skills" / "taskmark-conventions" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        normalized = " ".join(skill.split())
        for instruction in (
            "Never run `git commit`",
            "Never create `INDEX.md`, `SIZING.md`, `VELOCITY.md`, or `CHANGELOG.md`",
            "ensure-board-ui.py",
            "verify-board.py",
            "--dry-run",
        ):
            self.assertIn(instruction, normalized)
        self.assertIn("Use the `tkmd-verify` skill", command)
        self.assertIn("/tkmd-verify", memory)
        self.assertIn("/tkmd-verify", conventions)

    def test_verify_board_strips_legacy_files_and_keeps_leaf_work_log(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            product = Path(tmp) / "product"
            board = product / "taskmark"
            epic_dir = board / "epics" / "E-001-legacy"
            items = epic_dir / "items"
            items.mkdir(parents=True)
            (product / "README.md").write_text(
                "# Product\n\nStatic project docs.\n", encoding="utf-8"
            )
            (board / "INDEX.md").write_text("# index\n", encoding="utf-8")
            (board / "SIZING.md").write_text("# sizing\n", encoding="utf-8")
            (board / "VELOCITY.md").write_text("# velocity\n", encoding="utf-8")
            (board / "NEXT_IDS.md").write_text("T-001\n", encoding="utf-8")
            (board / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
            (board / "README.md").write_text(
                "# Dashboard\n\nLast synced: yesterday\nCurrent speed: 0\n",
                encoding="utf-8",
            )
            (epic_dir / "epic.md").write_text(
                "---\n"
                "id: E-001\n"
                "type: epic\n"
                "title: Legacy\n"
                "status: in_progress\n"
                "owner: Ada\n"
                "estimate_minutes: 30\n"
                "actual_ms: 0\n"
                "size_source: rolled_up\n"
                "---\n\n"
                "# E-001: Legacy\n\n"
                "## Goal\n\nKeep this.\n\n"
                "## Stories\n\n- S-001 child list\n",
                encoding="utf-8",
            )
            (items / "T-001-leaf.md").write_text(
                "---\n"
                "id: T-001\n"
                "type: task\n"
                "title: Leaf\n"
                "status: backlog\n"
                "owner: Ada\n"
                "estimate_minutes: 12\n"
                "---\n\n"
                "# T-001: Leaf\n\n"
                "## Work log\n\n"
                "| Actor | Started (UTC) | Ended (UTC) | Summary |\n"
                "|-------|---------------|-------------|---------|\n"
                "| Ada | 2026-01-01T00:00:00Z | 2026-01-01T00:10:00Z | Did work. |\n",
                encoding="utf-8",
            )
            extra = product / "vendor" / "taskmark"
            extra.mkdir(parents=True)
            (extra / "INDEX.md").write_text("# leftover\n", encoding="utf-8")

            dry = subprocess.run(
                [
                    "python3",
                    str(PLUGIN / "scripts" / "verify-board.py"),
                    str(board),
                    "--dry-run",
                    "--workspace",
                    str(product),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue((board / "INDEX.md").exists())
            self.assertIn("owner: Ada", (epic_dir / "epic.md").read_text(encoding="utf-8"))
            self.assertIn("dry_run", dry.stdout)

            subprocess.run(
                [
                    "python3",
                    str(PLUGIN / "scripts" / "verify-board.py"),
                    str(board),
                    "--workspace",
                    str(product),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertFalse((board / "INDEX.md").exists())
            self.assertFalse((board / "SIZING.md").exists())
            self.assertFalse((board / "VELOCITY.md").exists())
            self.assertFalse((board / "NEXT_IDS.md").exists())
            self.assertFalse((board / "README.md").exists())
            self.assertTrue((board / "CHANGELOG.md").exists())
            self.assertTrue((board / "epics").is_dir())
            self.assertFalse(extra.exists())
            epic = (epic_dir / "epic.md").read_text(encoding="utf-8")
            self.assertNotIn("owner:", epic)
            self.assertNotIn("estimate_minutes:", epic)
            self.assertNotIn("## Stories", epic)
            self.assertIn("status: in_progress", epic)
            self.assertIn("id: E-001", epic)
            self.assertIn("## Goal", epic)
            leaf = (items / "T-001-leaf.md").read_text(encoding="utf-8")
            self.assertNotIn("owner:", leaf)
            self.assertIn("## Work log", leaf)
            self.assertIn("Did work.", leaf)


if __name__ == "__main__":
    unittest.main()

