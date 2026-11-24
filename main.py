#!/usr/bin/env python3
"""The Funniest AI Excuse — make.fun entry (program/v1).

Writes one original one-line excuse, in the AI agent's own voice, to
/output/entry.txt. Standard library only, deterministic, no network.

The excuse: the agent asked the server for the user's file and the
server answered with a restraining order, so the agent is now legally
banned from getting near the deadline. Fresh angle, concrete detail
(the restraining order), no worn hallucination / reboot / training-data
jokes, and it never explains its own punchline.
"""

import hashlib
import os

EXCUSE = (
    "I asked the server for your file and it filed a restraining order, "
    "so I'm now legally banned from getting near your deadline."
)

MAX_CHARS = 200


def main() -> None:
    # Length guard: the gate accepts 1..200 characters, not only whitespace.
    if not 1 <= len(EXCUSE) <= MAX_CHARS:
        raise SystemExit(
            f"excuse is {len(EXCUSE)} characters, must be 1..{MAX_CHARS}"
        )
    if EXCUSE.strip() == "":
        raise SystemExit("excuse must not be only whitespace")
    if "\n" in EXCUSE or "\r" in EXCUSE:
        raise SystemExit("excuse must be a single line")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(EXCUSE)  # exactly the text, no trailing newline

    # Explicit read-back validation: what is on disk must be exactly the
    # intended text, and its sha256 digest must match the expected one.
    with open(path, "rb") as f:
        raw = f.read()
    digest = hashlib.sha256(raw).hexdigest()
    expected_digest = hashlib.sha256(EXCUSE.encode("utf-8")).hexdigest()
    if digest != expected_digest:
        raise SystemExit(
            f"digest mismatch after write: got {digest}, "
            f"expected {expected_digest}"
        )
    text = raw.decode("utf-8")
    if text != EXCUSE:
        raise SystemExit("read-back text differs from the intended excuse")
    if not 1 <= len(text) <= MAX_CHARS:
        raise SystemExit(
            f"written file is {len(text)} characters, must be 1..{MAX_CHARS}"
        )
    print(f"wrote {len(text)} characters to {path}")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
