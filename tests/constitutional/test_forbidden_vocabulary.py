"""Constitutional test — CONSTITUTION-LD.md L2: forbidden vocabulary on
output paths. No identifier, string constant, or module filename in
output-facing code may carry verdict vocabulary: a flag is a reason to
look, never a finding.

Scope: EVERY module in src/icebergsim_integrity/ is output-facing until
exempted below with a justification. Docstrings are excluded — prose may
discuss the mission; names may not, because identifiers and string
constants become field names, and field names become accusations.

The banned list itself lives in icebergsim_integrity.vocabulary — one
definition shared with the schema's runtime validation. The corpus tests
below pin that list in both directions, so it cannot be quietly weakened.

Red blocks merge.
"""
import ast
from pathlib import Path

import pytest

from icebergsim_integrity.vocabulary import banned_tokens_in

REPO = Path(__file__).resolve().parents[2]
PACKAGE = REPO / "src" / "icebergsim_integrity"

# Modules exempt from the scan. Every entry needs a one-line justification.
EXEMPT_MODULES: dict[str, str] = {
    "vocabulary.py": "defines the banned list itself; its strings are the ban, not output",
}


def _docstring_nodes(tree: ast.AST) -> set[int]:
    """ids of Constant nodes that are docstrings (first statement strings)."""
    found: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(
            node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            body = node.body
            if (
                body
                and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)
            ):
                found.add(id(body[0].value))
    return found


def _scannable_names(tree: ast.AST):
    """Every name-bearing surface: identifiers and non-docstring strings."""
    docstrings = _docstring_nodes(tree)
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
        elif (
            isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and id(node) not in docstrings
        ):
            yield node.value, node.lineno


def test_output_names_carry_no_verdict_vocabulary():
    violations = []
    for path in sorted(PACKAGE.rglob("*.py")):
        rel = path.relative_to(PACKAGE)
        if str(rel) in EXEMPT_MODULES:
            continue
        if hits := banned_tokens_in(path.stem):
            violations.append(f"{rel}: module name: {hits}")
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for name, lineno in _scannable_names(tree):
            if hits := banned_tokens_in(name):
                violations.append(f"{rel}:{lineno}: {name!r}: {hits}")
    assert not violations, "L2 verdict vocabulary in output paths:\n" + "\n".join(
        f"  - {v}" for v in violations
    )


def test_exemptions_are_justified():
    for module, why in EXEMPT_MODULES.items():
        assert (PACKAGE / module).exists(), f"exempt module {module} does not exist"
        assert len(why.strip()) >= 10, f"exemption for {module} needs a justification"


# --- Pin the banned list in both directions, so it cannot drift ------------

MUST_FIRE = [
    "fraud_probability", "honest_score", "dishonesty", "isFabricated",
    "falsified", "deception_score", "deceived", "deceitful",
    "misconduct_index", "doctored_data", "rigged", "lie_score", "liar",
    "lying_flag", "counterfeit_ratio", "bogus", "sham_result", "fudged",
    "cooked", "crooked", "verdict_field", "guilty", "innocent", "cheated",
    "forgery", "tampering_evidence", "manipulated", "corrupted",
    "suspicious_score", "suspect_trial", "accused", "exonerated",
    "incriminating", "illegitimate", "cherry_picked", "fake_data", "hoax",
    "phony", "malicious", "culprit", "criminal",
]

MUST_PASS = [
    "allocation_discrepancy_count", "degenerate_at_zero", "verification",
    "forensics", "false_alarm", "committed_seed", "null_replicates",
    "reach", "anomaly", "flag_rate", "regime", "statistic",
    "reference_distribution", "messy_null", "supplied", "shame", "shampoo",
    "triggered", "foreground", "forgetting_factor", "believe", "applied",
]


@pytest.mark.parametrize("name", MUST_FIRE)
def test_banned_corpus_fires(name):
    assert banned_tokens_in(name), f"{name!r} must be caught"


@pytest.mark.parametrize("name", MUST_PASS)
def test_legitimate_corpus_passes(name):
    assert not banned_tokens_in(name), f"{name!r} must not be caught"
