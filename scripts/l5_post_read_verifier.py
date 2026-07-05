#!/usr/bin/env python3
"""CLI wrapper for the L5.06 no-live post-read verifier."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from memory_seam.l5_post_read_verifier import verify_l5_receipt_document  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify the L5.05 supervised one-read receipt without any additional reads."
    )
    parser.add_argument(
        "--receipt",
        type=Path,
        default=ROOT / "docs" / "l5-supervised-one-read-receipt.md",
        help="Committed report-safe #105 receipt artifact to verify.",
    )
    args = parser.parse_args(argv)

    result = verify_l5_receipt_document(args.receipt)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["hygiene_passed"] and result["posture_preserved"] else 1


if __name__ == "__main__":
    sys.exit(main())
