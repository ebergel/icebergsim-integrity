"""Banned output vocabulary — the single definition L2 enforcement shares.

A flag is a reason to look, never a finding. Output-facing names — Python
identifiers, statistic names, reference names, detail keys, string values,
module filenames — must not carry judgment vocabulary. This module owns
the banned list; the schema enforces it at runtime and the constitutional
scan enforces it over source. One definition, so the two cannot drift.

Matching is token-based: names are split on non-alphanumeric boundaries
and camelCase, then each token is checked exactly against BANNED_TOKENS
or by prefix against BANNED_STEMS. Tokens, not substrings, so that e.g.
"shame", "triggered" or "foreground" never match while "lie_score" does.
The collapsed name (alphanumerics only) is also checked by prefix, so
compounds like "cherrypicked" cannot hide behind their own boundaries.
"""
from __future__ import annotations

import re

# Exact tokens: short words where prefix matching would overreach.
BANNED_TOKENS = frozenset({
    "lie", "lies", "lied", "liar", "liars", "lying",
    "fake", "faked", "fakes", "faking", "phony", "hoax",
    "sham", "shams", "bogus", "rigged", "rigging",
    "cooked", "doctored", "fudge", "fudged", "fudging",
    "crook", "crooked", "culprit", "criminal",
    "guilt", "guilty", "innocent", "innocence",
    "cheat", "cheats", "cheated", "cheater", "cheating",
    "forged", "forger", "forgery", "forgeries", "forging",
})

# Prefix stems: word families where every continuation is judgment-shaped.
BANNED_STEMS = (
    "fraud", "honest", "dishonest", "fabricat", "falsif",
    "tamper", "manipulat", "corrupt", "malicious",
    "suspect", "suspicious", "accus", "incrimin", "exonerat",
    "decept", "deceiv", "deceit", "misconduct", "counterfeit",
    "illegitim", "cherrypick", "verdict",
)

_TOKEN_SPLIT = re.compile(r"[^a-zA-Z0-9]+|(?<=[a-z0-9])(?=[A-Z])")


def banned_tokens_in(name: str) -> tuple[str, ...]:
    """Every banned token the given name carries; empty means clean."""
    tokens = [t.lower() for t in _TOKEN_SPLIT.split(name) if t]
    hits = [
        t
        for t in tokens
        if t in BANNED_TOKENS or any(t.startswith(s) for s in BANNED_STEMS)
    ]
    collapsed = "".join(tokens)
    if any(collapsed.startswith(s) for s in BANNED_STEMS) and collapsed not in hits:
        hits.append(collapsed)
    return tuple(dict.fromkeys(hits))
