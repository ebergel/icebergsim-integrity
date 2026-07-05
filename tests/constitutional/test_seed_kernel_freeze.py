"""Constitutional test — CONSTITUTION-LD.md L5 / Gate G1: the seed kernel
is frozen.

EB accepted seedkernel.py 0.1.0 on 2026-07-05. From that moment, any
change to the module crosses Gate G1. This test makes the freeze
executable: it pins the file's content hash, exactly as L11 pins exports.

If this test is red, the floor moved. Do NOT update the hash to make it
green — that is the one edit in this repository that is never free. The
hash changes only together with EB's explicit yes (G1), recorded in
CHANGELOG.md.
"""
import hashlib
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
KERNEL = REPO / "src" / "icebergsim_integrity" / "seedkernel.py"

# Accepted by EB 2026-07-05 (kernel 0.1.0).
ACCEPTED_SHA256 = "b01a1fcf533b13a5b6e79e68f4ddc14d37adf0cad735d9ed1cc62d0b8cd2e61d"


def test_seed_kernel_is_frozen():
    digest = hashlib.sha256(KERNEL.read_bytes()).hexdigest()
    assert digest == ACCEPTED_SHA256, (
        "seedkernel.py no longer matches the hash EB accepted on 2026-07-05.\n"
        "Any change to the seed kernel crosses Gate G1 (CONSTITUTION-LD.md L5).\n"
        "Revert the change, or take it to EB; only his yes updates this pin.\n"
        f"  accepted: {ACCEPTED_SHA256}\n"
        f"  found:    {digest}"
    )
