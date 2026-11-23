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
            "Leave those tables empty",
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

    def test_plan_and_save_write_new_work_under_requests(self) -> None:
        plan = " ".join(
            (PLUGIN / "skills" / "tkmd-plan" / "SKILL.md").read_text(encoding="utf-8").split()
        )
        save = " ".join(
            (PLUGIN / "skills" / "tkmd-save" / "SKILL.md").read_text(encoding="utf-8").split()
        )

        for instruction in (
            "requests/<slug>/brief.md",
            "requests/<slug>/epics",
            "id: R-<slug>",
            "type: request",
            "status: <proposed|ready>",
            "requested_by:",
            "owner:",
            "created: <UTC YYYY-MM-DD>",
            "## Goal",
            "## Why",
            "## Done when",
            "## Out of scope",
            "## Open questions",
            "`aliases`",
            "never edit an existing request `brief.md`",
            "`epics/` and no `requests/`",
            "npx taskmark init",
            "Leave those tables empty",
            "allocate-id.py",
        ):
            self.assertIn(instruction, plan)

        for instruction in (
            "requests/<slug>/brief.md",
            "requests/<slug>/epics/...",
            "never edit its `brief.md`",
            "Goal, Why, Done when, Out of scope, Open questions",
            "`epics/` and no `requests/`",
            "npx taskmark init",
            "never edit an existing request `brief.md`",
        ):
            self.assertIn(instruction, save)

        for name in ("tkmd-plan-do", "tkmd-save-do"):
            skill = " ".join(
                (PLUGIN / "skills" / name / "SKILL.md").read_text(encoding="utf-8").split()
            )
            self.assertIn("requests/<slug>/brief.md", skill, name)
            self.assertIn("every request brief", skill, name)
            self.assertIn("A new request brief is context, not an implementation target", skill, name)

        for name in ("tkmd-plan", "tkmd-save"):
            command = " ".join(
                (PLUGIN / "commands" / f"{name}.md").read_text(encoding="utf-8").split()
            )
            self.assertIn("requests/<slug>/epics/...", command, name)
            self.assertIn("requests/<slug>/brief.md", command, name)
            self.assertIn("npx taskmark init", command, name)
        for name in ("tkmd-plan-do", "tkmd-save-do"):
            command = " ".join(
                (PLUGIN / "commands" / f"{name}.md").read_text(encoding="utf-8").split()
            )
            self.assertIn("existing or new request", command, name)

    def test_init_delegates_to_taskmark_cli(self) -> None:
        skill = " ".join(
            (PLUGIN / "skills" / "taskmark-init" / "SKILL.md").read_text(encoding="utf-8").split()
        )
        command = " ".join(
            (PLUGIN / "commands" / "tkmd-init.md").read_text(encoding="utf-8").split()
        )

        for instruction in (
            "npx taskmark init",
            "npx @taskmark/ui init",
            "let the user answer each prompt there",
            "GitHub or Bitbucket",
            "OpenAI or Claude key",
            "`AGENTS.md`",
            "`CLAUDE.md`",
            "migrates a legacy `epics/` board to requests",
            "initial reconciliation",
            "Do not hand-create board files when the CLI can run",
            "Only when `npx` cannot run at all",
            "`requests/` and `meetings/`",
            "Do not create `epics/` on a new board",
            "Tell the user to run `npx taskmark init` later",
        ):
            self.assertIn(instruction, skill)
        self.assertNotIn("Create the board directory and `epics/`", skill)

        for instruction in (
            "npx taskmark init",
            "GitHub or Bitbucket",
            "OpenAI or Claude key",
            "Do not hand-create board files",
            "`requests/`, `meetings/`",
            "npm/npx is unavailable",
        ):
            self.assertIn(instruction, command)

    def test_conventions_and_rules_describe_request_layout(self) -> None:
        conventions = " ".join(
            (PLUGIN / "skills" / "taskmark-conventions" / "SKILL.md")
            .read_text(encoding="utf-8")
            .split()
        )
        rule = " ".join(
            (PLUGIN / "rules" / "taskmark-conventions.mdc").read_text(encoding="utf-8").split()
        )
        memory = " ".join(
            (PLUGIN / "rules" / "taskmark-project-memory.mdc").read_text(encoding="utf-8").split()
        )

        for instruction in (
            "## Board layouts",
            "requests/<slug>/brief.md",
            "requests/<slug>/epics/",
            "requests/<slug>/log/",
            "meetings/<date>-<slug>.md",
            "`R-<slug>`",
            "Legacy board:",
            "`development`, `testing`, `production`",
            "never by agents",
            "Reconciliation belongs to the App",
        ):
            self.assertIn(instruction, conventions)
        for text in (rule, memory):
            self.assertIn("requests/<slug>/brief.md", text)
            self.assertIn("meetings/", text)
            self.assertIn("`epics/`", text)
        self.assertIn("Reconciliation belongs to the App", memory)
        self.assertIn("npx taskmark init", memory)

    def test_readmes_cover_requests_and_any_agent(self) -> None:
        for path in (ROOT / "README.md", PLUGIN / "README.md"):
            text = " ".join(path.read_text(encoding="utf-8").split())
            self.assertIn("https://taskmark.dev/docs/agents", text, str(path))
            self.assertIn("one integration", text, str(path))
            self.assertIn("brief.md", text, str(path))
            self.assertIn("npx taskmark init", text, str(path))

    def test_request_board_prose_has_no_dashes(self) -> None:
        paths = [
            ROOT / "README.md",
            PLUGIN / "README.md",
            *(PLUGIN / "rules").glob("*.mdc"),
            *(
                PLUGIN / "skills" / name / "SKILL.md"
                for name in (
                    "taskmark-init",
                    "taskmark-conventions",
                    "tkmd-plan",
                    "tkmd-save",
                    "tkmd-plan-do",
                    "tkmd-save-do",
                    "tkmd-do",
                    "tkmd-verify",
                )
            ),
            *(
                PLUGIN / "commands" / f"{name}.md"
                for name in ("tkmd-init", "tkmd-plan", "tkmd-save", "tkmd-plan-do", "tkmd-save-do")
            ),
        ]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("—", text, str(path))
            self.assertNotIn("–", text, str(path))

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

    def test_agents_treat_existing_items_as_read_only(self) -> None:
        do_skill = (PLUGIN / "skills" / "tkmd-do" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        memory = (PLUGIN / "rules" / "taskmark-project-memory.mdc").read_text(
            encoding="utf-8"
        )
        conventions = (PLUGIN / "skills" / "taskmark-conventions" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        normalized_do = " ".join(do_skill.split())
        self.assertIn("Never edit, rename, move, or delete any existing board file", normalized_do)
        self.assertIn("Do not log anything on the item", normalized_do)
        self.assertIn("`<id>-<short-slug>`", normalized_do)
        self.assertIn("npx taskmark hooks install", normalized_do)
        self.assertIn("Reconciliation belongs to the App", memory)
        self.assertIn("Reconciliation belongs to the App", conventions)
        self.assertNotIn("appends Prompt & feedback", conventions)
        self.assertNotIn("appends Prompt & feedback", memory)
        self.assertIn("no estimate or owner property", conventions)
        self.assertIn("closed Started → Ended intervals", conventions)
        self.assertIn("taskmark.writingLanguage", conventions)
        self.assertNotIn("Portuguese-only", conventions)
        self.assertIn("board writing language", memory)

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
            "Do not voluntarily stop after a subset",
            normalized_do_skill,
        )
        self.assertIn(
            "every open, non-cancelled, non-shelved descendant leaf",
            normalized_do_command,
        )
        self.assertIn(
            "report the whole target incomplete",
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

    def test_shelf_command_is_removed(self) -> None:
        self.assertFalse((PLUGIN / "skills" / "tkmd-shelf").exists())
        self.assertFalse((PLUGIN / "commands" / "tkmd-shelf.md").exists())
        for path in [*PLUGIN.rglob("*.md"), *PLUGIN.rglob("*.mdc"), *PLUGIN.rglob("*.json")]:
            if "node_modules" in path.parts:
                continue
            self.assertNotIn("tkmd-shelf", path.read_text(encoding="utf-8"), str(path))

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

    def test_sync_repos_detects_request_board_and_never_creates_epics(self) -> None:
        script = str(PLUGIN / "scripts" / "sync-taskmark-repos.sh")
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            # Existing request board inside a single product repo.
            repo = Path(tmp) / "product"
            board = repo / "taskmark"
            (board / "requests" / "careers" / "epics").mkdir(parents=True)
            subprocess.run(["git", "init", str(repo)], check=True, capture_output=True)
            out = subprocess.run(
                [script, str(repo)], check=True, capture_output=True, text=True
            ).stdout
            self.assertIn("Mode: single-project", out)
            self.assertIn(f"Canonical: {board.resolve()}", out)
            self.assertTrue((board / "REPOS.md").exists())
            self.assertFalse((board / "epics").exists())

            # Dedicated multi-repo board detected by requests/ alone.
            ws = Path(tmp) / "ws"
            for name in ("acme-api", "acme-web", "acme-taskmark"):
                (ws / name).mkdir(parents=True)
                subprocess.run(["git", "init", str(ws / name)], check=True, capture_output=True)
            (ws / "acme-taskmark" / "requests").mkdir()
            out = subprocess.run(
                [script, str(ws)], check=True, capture_output=True, text=True
            ).stdout
            self.assertIn("Mode: multi-project", out)
            self.assertIn("acme-taskmark", out)
            self.assertFalse((ws / "acme-taskmark" / "epics").exists())

            # A brand new board starts with requests/, not epics/.
            fresh = Path(tmp) / "fresh"
            fresh.mkdir()
            subprocess.run(["git", "init", str(fresh)], check=True, capture_output=True)
            subprocess.run([script, str(fresh)], check=True, capture_output=True)
            self.assertTrue((fresh / "taskmark" / "requests").is_dir())
            self.assertFalse((fresh / "taskmark" / "epics").exists())

    def test_verify_board_scans_request_items_but_not_briefs_logs_or_meetings(self) -> None:
        legacy_fm = "owner: Ada\nestimate_minutes: 12\n"
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            board = Path(tmp) / "acme-taskmark"
            request = board / "requests" / "careers"
            epic_dir = request / "epics" / "E-001-careers"
            items = epic_dir / "items"
            items.mkdir(parents=True)
            (request / "log").mkdir()
            (board / "meetings").mkdir()
            brief = (
                "---\nid: R-careers\ntype: request\ntitle: Careers\n"
                + legacy_fm
                + "---\n\n# Careers\n\n## Goal\n\nHire.\n\n## Stories\n\n- keep\n"
            )
            log = "---\nkind: note\nat: 2026-11-20T10:00:00Z\n" + legacy_fm + "---\nNote.\n"
            meeting = "---\nid: M-1\ntitle: Kickoff\n" + legacy_fm + "---\n## Summary\n"
            (request / "brief.md").write_text(brief, encoding="utf-8")
            (request / "log" / "2026-11-20-note.md").write_text(log, encoding="utf-8")
            (board / "meetings" / "2026-11-18-kickoff.md").write_text(meeting, encoding="utf-8")
            (epic_dir / "epic.md").write_text(
                "---\nid: E-001\ntype: epic\ntitle: Careers\nstatus: backlog\n"
                + legacy_fm
                + "---\n\n# E-001\n\n## Goal\n\nKeep.\n\n## Stories\n\n- S-001 child list\n",
                encoding="utf-8",
            )
            (items / "T-001-leaf.md").write_text(
                "---\nid: T-001\ntype: task\ntitle: Leaf\nstatus: done\nstage: production\n"
                + legacy_fm
                + "---\n\n# T-001\n\n## Work log\n\n| Actor | Started (UTC) | Ended (UTC) | Summary |\n"
                "|-------|---------------|-------------|---------|\n"
                "| Ada | 2026-01-01T00:00:00Z | 2026-01-01T00:10:00Z | Did work. |\n",
                encoding="utf-8",
            )
            legacy_epic = board / "epics" / "E-002-old"
            legacy_epic.mkdir(parents=True)
            (legacy_epic / "epic.md").write_text(
                "---\nid: E-002\ntype: epic\ntitle: Old\n" + legacy_fm + "---\n\n# E-002\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                ["python3", str(PLUGIN / "scripts" / "verify-board.py"), str(board)],
                check=True,
                capture_output=True,
                text=True,
            )
            report = json.loads(result.stdout)
            rewritten = set(report["rewritten"])
            self.assertIn("requests/careers/epics/E-001-careers/epic.md", rewritten)
            self.assertIn("requests/careers/epics/E-001-careers/items/T-001-leaf.md", rewritten)
            self.assertIn("epics/E-002-old/epic.md", rewritten)

            epic = (epic_dir / "epic.md").read_text(encoding="utf-8")
            self.assertNotIn("owner:", epic)
            self.assertNotIn("## Stories", epic)
            leaf = (items / "T-001-leaf.md").read_text(encoding="utf-8")
            self.assertNotIn("estimate_minutes:", leaf)
            self.assertIn("stage: production", leaf)
            self.assertIn("Did work.", leaf)
            self.assertNotIn("owner:", (legacy_epic / "epic.md").read_text(encoding="utf-8"))

            self.assertEqual((request / "brief.md").read_text(encoding="utf-8"), brief)
            self.assertEqual(
                (request / "log" / "2026-11-20-note.md").read_text(encoding="utf-8"), log
            )
            self.assertEqual(
                (board / "meetings" / "2026-11-18-kickoff.md").read_text(encoding="utf-8"),
                meeting,
            )
            self.assertTrue((board / "requests").is_dir())
            self.assertTrue((board / "meetings").is_dir())

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
                "## Stories\n\n- S-001 child list\n\n"
                "## Work log\n\n- legacy parent row\n",
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
            self.assertIn("legacy parent row", epic)
            self.assertIn("status: in_progress", epic)
            self.assertIn("id: E-001", epic)
            self.assertIn("## Goal", epic)
            leaf = (items / "T-001-leaf.md").read_text(encoding="utf-8")
            self.assertNotIn("owner:", leaf)
            self.assertIn("## Work log", leaf)
            self.assertIn("Did work.", leaf)


if __name__ == "__main__":
    unittest.main()

