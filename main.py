#!/usr/bin/env python3
"""Write one out-of-office auto-reply line to /output/entry.txt.

Stdlib only. The output path can be overridden with the ENTRY_OUTPUT
environment variable (used by local testing).
"""

import os
import sys

MAX_ENTRY_CHARS = 140

ENTRY = (
    "Out of office until Monday. My inbox is being watched by my cat, "
    "who has already deleted three emails and feels no remorse."
)


def validate_entry(entry: str) -> None:
    """Reject entries that violate the bounty gate.

    Gate: 1-140 characters, plain ASCII, single line, no leading or
    trailing whitespace. Exits with a clear message on violation.
    """
    if not entry:
        sys.exit("error: entry is empty")
    if entry != entry.strip():
        sys.exit("error: entry has leading or trailing whitespace")
    if "\n" in entry or "\r" in entry:
        sys.exit("error: entry must be a single line")
    try:
        entry.encode("ascii")
    except UnicodeEncodeError:
        sys.exit("error: entry must be plain ASCII")
    if len(entry) > MAX_ENTRY_CHARS:
        sys.exit(
            f"error: entry is {len(entry)} chars, "
            f"over the {MAX_ENTRY_CHARS}-char limit"
        )


def main() -> None:
    validate_entry(ENTRY)
    path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY + "\n")


if __name__ == "__main__":
    main()
