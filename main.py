#!/usr/bin/env python3
"""make.fun news-image-20261125 v7 — front-page newspaper of 25 Nov 2026.

Standard library only: the grading container installs nothing before it
runs ("standard library only: nothing is installed before it runs"), so
this program must not import Pillow or any other third-party package.
It copies the repo's pre-rendered asset.png (1024x1024, 50 verified
stories) to entry.png in the output dir. A straight byte copy is
deterministic by construction.

Usage: python3 main.py [--output DIR]
The output dir defaults to /output (the only writable directory in the
grading container, where the repo is mounted read-only); it can also be
given with --output or the MAKEFUN_OUTPUT_DIR environment variable.
"""
import argparse
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    # Grading runs main.py bare (no --output, no MAKEFUN_OUTPUT_DIR) with
    # the repo mounted read-only and only /output writable, so the default
    # must be the absolute /output, never a path inside the repo.
    out_dir = args.output or os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"

    asset_path = os.path.join(HERE, "asset.png")
    if not os.path.isfile(asset_path):
        print("error: asset.png not found next to main.py", file=sys.stderr)
        sys.exit(1)
    with open(asset_path, "rb") as f:
        data = f.read()
    print("asset.png bytes=%d sha256=%s" % (len(data),
          hashlib.sha256(data).hexdigest()))

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as f:
        f.write(data)
    print("entry.png -> %s" % out_path)


if __name__ == "__main__":
    main()
