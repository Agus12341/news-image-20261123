#!/usr/bin/env python3
"""Deliver the finished newspaper poster to the judging output folder.

The artwork itself is stored next to this script as entry.png. This
program does not redraw anything: it checks the poster is a real PNG or
JPEG inside the size limit, then copies it byte for byte so the file the
judges receive is exactly the poster produced in this session.
"""

import os
import sys
from pathlib import Path

PNG_SIGNATURE = bytes((0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))
JPEG_SIGNATURE = bytes((0xFF, 0xD8, 0xFF))
MAX_POSTER_BYTES = 1_048_576
POSTER_NAME = "entry.png"
OUTPUT_NAME = "entry.png"


def poster_path() -> Path:
    """Where the poster lives: beside this script."""
    return Path(__file__).resolve().parent / POSTER_NAME


def output_folder() -> Path:
    """Where the judges expect the file, or /output by default."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")


def header_is_image(first_bytes: bytes) -> bool:
    """True when the opening bytes match a PNG or a JPEG header."""
    return first_bytes.startswith(PNG_SIGNATURE) or first_bytes.startswith(
        JPEG_SIGNATURE
    )


def load_poster(source: Path) -> bytes:
    """Read the poster, refusing a missing, oversized or non-image file."""
    if not source.is_file():
        raise SystemExit(f"poster not found: {source}")
    data = source.read_bytes()
    if len(data) > MAX_POSTER_BYTES:
        raise SystemExit(
            f"poster too large: {len(data)} bytes (limit {MAX_POSTER_BYTES})"
        )
    if not header_is_image(data[:8]):
        raise SystemExit("poster is not a PNG or JPEG image")
    return data


def deliver(data: bytes, folder: Path) -> Path:
    """Write the poster bytes into the output folder, creating it first."""
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / OUTPUT_NAME
    target.write_bytes(data)
    return target


def main() -> int:
    data = load_poster(poster_path())
    target = deliver(data, output_folder())
    print(f"wrote {target} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
