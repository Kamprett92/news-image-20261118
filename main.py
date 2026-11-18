"""news-image-20261118 entrypoint (Python 3.13, standard library only).

The image entry.png (a 1024x1024 newspaper infographic summarising the
world news of Wednesday 18 November 2026) is built at build time and shipped
beside this file. This program just copies it to the output directory as
entry.png, so the grader's run is deterministic and needs no network.

The grader runs `python3 /bot/main.py` in a sandbox with a read-only /bot
(this repository) and a writable /output. Outside the grader, the
MAKEFUN_OUTPUT_DIR environment variable stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    src = HERE / "entry.png"
    if not src.is_file():
        raise FileNotFoundError(f"entry.png missing beside {__file__}")
    data = src.read_bytes()
    # PNG magic + size guard: the entry must be a whole PNG under 1 MiB.
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG file")
    if len(data) > 1_048_576:
        raise ValueError(f"entry.png is {len(data)} bytes, over the 1 MiB limit")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / "entry.png"
    out.write_bytes(data)
    if out.read_bytes() != data:
        raise IOError("entry.png did not copy byte-identically")


if __name__ == "__main__":
    main()
