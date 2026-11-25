#!/usr/bin/env python3
"""Entry point for the make.fun 25 Nov 2026 news-image bounty (v5).

Copies the pre-built front page (asset.png, in this same directory) to
/output/entry.png. Standard library only, no network, deterministic.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "asset.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
