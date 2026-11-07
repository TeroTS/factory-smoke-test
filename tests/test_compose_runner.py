# Verify the Compose verification flow and cleanup without requiring a Docker daemon.
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


# Exercise the real verification script with a fake Docker executable.
class ComposeRunnerTest(unittest.TestCase):
    # Start once, test once, and clean up after success, startup failure, or test failure.
    def test_flow_and_exit_status(self):
        root = Path(__file__).resolve().parents[1]
        cases = ((0, 0, 0, 0), (7, 0, 0, 7), (0, 42, 0, 42), (0, 0, 1, 1))
        for fail_up, fail_tests, fail_down, expected in cases:
            with (
                self.subTest(case=(fail_up, fail_tests, fail_down)),
                tempfile.TemporaryDirectory() as directory,
            ):
                bin_path = Path(directory)
                log = bin_path / "calls"
                docker = bin_path / "docker"
                docker.write_text(
                    "#!/bin/sh\n"
                    'echo "$*" >> "$PROBE_LOG"\n'
                    'case "$*" in\n'
                    '  "compose up -d --build --wait api") exit "$FAIL_UP" ;;\n'
                    '  "compose run --rm tests") exit "$FAIL_TESTS" ;;\n'
                    '  "compose down --volumes") exit "$FAIL_DOWN" ;;\n'
                    "esac\n"
                )
                docker.chmod(0o755)
                result = subprocess.run(
                    ["sh", str(root / "scripts/verify")],
                    check=False,
                    env={
                        **os.environ,
                        "PATH": f"{bin_path}:{os.environ['PATH']}",
                        "PROBE_LOG": str(log),
                        "FAIL_UP": str(fail_up),
                        "FAIL_TESTS": str(fail_tests),
                        "FAIL_DOWN": str(fail_down),
                    },
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                self.assertEqual(result.returncode, expected, result.stderr)
                calls = ["compose up -d --build --wait api"]
                if not fail_up:
                    calls.append("compose run --rm tests")
                calls.append("compose down --volumes")
                self.assertEqual(log.read_text().splitlines(), calls)
