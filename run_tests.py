#!/usr/bin/env python3
"""Run pytest tests."""
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/", "-v"],
    cwd="/workspaces/skills-getting-started-with-github-copilot"
)
sys.exit(result.returncode)
