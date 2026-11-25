"""make.fun bounty: Sum up 25 November's world news in one image.

Writes one image to /output/entry.png.
Deterministic: copies the bundled asset.png with no network,
no timestamps and no randomness, so two runs write identical bytes.
Only the Python standard library is used.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "asset.png")
DST = "/output/entry.png"


def main():
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    with open(DST, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print(f"Wrote {DST} ({os.path.getsize(DST)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
