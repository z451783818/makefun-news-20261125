#!/usr/bin/env python3
"""Entry for make.fun bounty news-image-20261125.

Writes the bundled news image to /output/entry.png.
Python 3.13, standard library only, no network access.
Deterministic: the output bytes are identical on every run.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "asset.png")
DEST = "/output/entry.png"


def main():
    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    with open(DEST, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    size = os.path.getsize(DEST)
    print(f"Wrote {DEST} ({size} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
