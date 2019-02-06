#!/usr/bin/env python3

import sys
import time
import subprocess

PYTHON = sys.executable

try:
    while True:
        cmd = [PYTHON, "main.py"]
        cp = subprocess.run(cmd)

        if cp.returncode != 0:
            print("Program exited unexpectedly, sleeping before restart")
            time.sleep(3)
except (SystemExit, KeyboardInterrupt):
    pass
