#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261125 bounty (v6).

Copies the pre-rendered front page (asset.png, produced by
build_image.py) into /output/entry.png. Standard library only, no
network access, fully deterministic.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "asset.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    if len(sys.argv) > 1 and sys.argv[1] == "--output":
        out_dir = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst)


if __name__ == "__main__":
    main()
