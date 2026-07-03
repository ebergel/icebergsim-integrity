"""Constitutional test — CONSTITUTION-LD.md L11: documents are exports too.

Every markdown file in this repository opens with the SOP-DOCS.md
frontmatter manifest. Red blocks merge. Exemptions are structural (paths),
never per-file. Lives at tests/constitutional/test_manifests.py.

Green from day one; keep it that way.
"""
from pathlib import Path

# Adjust parents[] to reach repo root from tests/constitutional/
REPO = Path(__file__).resolve().parents[2]

EXEMPT_DIRS = {"scratch", "node_modules", ".git", ".github", ".venv",
               "dist", "build", "site-packages", ".pytest_cache",
               "__pycache__", ".mypy_cache", ".ruff_cache", ".obsidian",
               "_templates"}
EXEMPT_FILES = {"LICENSE.md", "_about.md"}  # add "README.md" here if the landing file should stay bare

ISM = {"program", "rct", "integrity", "alfa", "classic", "ua"}
KIND = {"law", "sop", "seal", "map", "spec", "guide", "changelog",
        "session", "decision", "ledger", "quarry", "readme"}
STATUS = {"draft", "signed", "active", "blind", "exposed", "shelved",
          "superseded", "open", "decided", "parked", "dead"}
DATED_KINDS = {"seal", "changelog", "session", "decision", "ledger"}  # no version required


def _markdown_files():
    for p in sorted(REPO.rglob("*.md")):
        rel = p.relative_to(REPO)
        if any(part in EXEMPT_DIRS for part in rel.parts):
            continue
        if rel.name in EXEMPT_FILES:
            continue
        yield rel, p.read_text(encoding="utf-8")


def _parse_manifest(text):
    lines = text.splitlines()
    assert lines and lines[0].strip() == "---", "must open with '---' on line 1"
    fm, i = {}, 1
    while i < len(lines) and lines[i].strip() != "---":
        if ":" in lines[i]:
            key, val = lines[i].split(":", 1)
            fm[key.strip()] = val.strip()
        i += 1
    assert i < len(lines), "unterminated frontmatter (no closing '---')"
    return fm


def test_every_markdown_carries_a_manifest():
    problems, ids = [], {}
    for rel, text in _markdown_files():
        try:
            fm = _parse_manifest(text)
            for req in ("id", "title", "isbrs", "kind", "status", "date"):
                assert fm.get(req), f"missing '{req}'"
            assert fm["isbrs"] in ISM, f"isbrs '{fm['isbrs']}' not in the registry"
            assert fm["kind"] in KIND, f"kind '{fm['kind']}' unknown"
            assert fm["status"] in STATUS, f"status '{fm['status']}' unknown"
            if fm["kind"] not in DATED_KINDS:
                assert fm.get("version"), "artifact kinds require 'version' (semver)"
            if fm["id"] in ids:
                problems.append(f"{rel}: duplicate id '{fm['id']}' (also in {ids[fm['id']]})")
            ids[fm["id"]] = rel
        except AssertionError as e:
            problems.append(f"{rel}: {e}")
    assert not problems, "L11 manifest violations:\n" + "\n".join(f"  - {p}" for p in problems)
