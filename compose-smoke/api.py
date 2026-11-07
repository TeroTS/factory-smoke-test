# Serve the calculator fixture over HTTP and persist calculation history in a SQLite volume.
import json
import os
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from calculator import add

DATABASE = os.environ.get("SMOKE_DATABASE", "/data/calculator.sqlite3")


# Route fixture requests; reject invalid operands and return bounded internal-error responses.
class Handler(BaseHTTPRequestHandler):
    # Return JSON for health, integer addition, and stored history; commit before responding.
    def do_GET(self):
        url = urlsplit(self.path)
        status = 200
        try:
            with sqlite3.connect(DATABASE, timeout=5) as database:
                if url.path == "/health":
                    database.execute("SELECT 1 FROM calculations LIMIT 1")
                    payload = {"status": "ok"}
                elif url.path == "/history":
                    payload = database.execute(
                        "SELECT a, b, result FROM calculations ORDER BY rowid"
                    ).fetchall()
                elif url.path == "/add":
                    args = parse_qs(url.query, strict_parsing=True)
                    if set(args) != {"a", "b"} or any(
                        len(values) != 1 for values in args.values()
                    ):
                        raise ValueError("Expected one a and one b")
                    a, b = int(args["a"][0]), int(args["b"][0])
                    result = add(a, b)
                    database.execute(
                        "INSERT INTO calculations VALUES (?, ?, ?)", (a, b, result)
                    )
                    payload = {"result": result}
                else:
                    status, payload = 404, {"error": "not found"}
        except (ValueError, OverflowError):
            status, payload = 400, {"error": "expected two SQLite-range integers"}
        except sqlite3.Error:
            status, payload = 500, {"error": "database unavailable"}
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


# Initialize durable storage before listening; startup errors fail the container.
if __name__ == "__main__":
    with sqlite3.connect(DATABASE) as database:
        database.execute(
            "CREATE TABLE IF NOT EXISTS calculations (a INTEGER, b INTEGER, result INTEGER)"
        )
    ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
