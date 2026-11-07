# Exercise the calculator over HTTP using Compose service-name DNS.
import json
import tempfile
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen


# Check real HTTP responses, arithmetic, database writes, and workspace permissions.
class CalculatorAPITest(unittest.TestCase):
    # Request JSON with a bounded timeout so a broken service fails promptly.
    def request(self, path):
        with urlopen("http://api:8000" + path, timeout=5) as response:
            return json.load(response)

    # Health checks must succeed before dependent tests start.
    def test_health(self):
        try:
            result = self.request("/health")
        except HTTPError as error:
            error.close()
            self.fail(f"Health endpoint returned HTTP {error.code}")
        self.assertEqual(result, {"status": "ok"})

    # Exercise the existing calculator and verify the database records each calculation.
    def test_addition_and_storage(self):
        for a, b, expected in ((2, 3, 5), (-2, 3, 1), (0, 0, 0)):
            result = self.request(f"/add?a={a}&b={b}")
            self.assertEqual(result["result"], expected)
            self.assertIn([a, b, expected], self.request("/history"))

    # Reject malformed operands without exposing an internal server error.
    def test_bad_input(self):
        for path in (
            "/add?a=oops&b=2",
            "/add?a=1",
            "/add?a=1&a=2&b=3",
            "/add?a=999999999999999999999&b=1",
            "/missing",
        ):
            with self.assertRaises(HTTPError) as error:
                self.request(path)
            self.assertEqual(error.exception.code, 404 if path == "/missing" else 400)
            error.exception.close()

    # The non-root test container must be able to write the mounted checkout.
    def test_workspace_mount(self):
        with tempfile.TemporaryDirectory(
            dir=Path(__file__).resolve().parent
        ) as directory:
            probe = Path(directory) / "probe"
            probe.write_text("compose bind mount works\n")
            self.assertEqual(probe.read_text(), "compose bind mount works\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
