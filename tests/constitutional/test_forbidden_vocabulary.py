"""Constitutional test — CONSTITUTION-LD.md L2: forbidden vocabulary on
output paths. No identifier in output-facing code may carry verdict
vocabulary: a flag is a reason to look, never a finding.

Scope: EVERY module in src/icebergsim_integrity/ is output-facing until
exempted below with a justification. Prose (docstrings, comments) is free
to discuss the mission; identifiers are not, because identifiers become
field names, and field names become accusations.

Red blocks merge.
"""
import ast
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PACKAGE = REPO / "src" / "icebergsim_integrity"

# Input-side modules exempt from the scan. Every entry needs a one-line
# justification (e.g. the honest-trial generator legitimately speaks in
# L8's "honest-messy" vocabulary). Empty today.
EXEMPT_MODULES: dict[str, str] = {}

FORBIDDEN = re.compile(
    r"fraud|honest|fabricat|falsif|forger|forged|fake|cheat|verdict"
    r"|guilt|innocent|tamper|manipulat|corrupt|malicious|suspect|suspicious"
    r"|accus",
    re.IGNORECASE,
)


def _identifiers(tree: ast.AST):
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            yield node.name, node.lineno
        elif isinstance(node, ast.Name):
            yield node.id, node.lineno
        elif isinstance(node, ast.Attribute):
            yield node.attr, node.lineno
        elif isinstance(node, ast.arg):
            yield node.arg, node.lineno
        elif isinstance(node, ast.keyword) and node.arg:
            yield node.arg, node.lineno
        elif isinstance(node, ast.alias):
            yield node.asname or node.name, node.lineno


def test_output_identifiers_carry_no_verdict_vocabulary():
    violations = []
    for path in sorted(PACKAGE.rglob("*.py")):
        rel = path.relative_to(PACKAGE)
        if str(rel) in EXEMPT_MODULES:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for name, lineno in _identifiers(tree):
            if FORBIDDEN.search(name):
                violations.append(f"{rel}:{lineno}: identifier '{name}'")
    assert not violations, "L2 verdict vocabulary in output paths:\n" + "\n".join(
        f"  - {v}" for v in violations
    )


def test_exemptions_are_justified():
    for module, why in EXEMPT_MODULES.items():
        assert (PACKAGE / module).exists(), f"exempt module {module} does not exist"
        assert len(why.strip()) >= 10, f"exemption for {module} needs a justification"
