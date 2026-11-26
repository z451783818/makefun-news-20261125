#!/usr/bin/env python3
"""Build the v7 entry image by running main.py."""
import subprocess
import sys

if __name__ == "__main__":
    sys.exit(subprocess.call([sys.executable, "main.py"] + sys.argv[1:]))
