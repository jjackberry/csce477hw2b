#!/usr/bin/env python3
"""Serve the login page and repeat the email/password checks on the server."""

import json
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent


class LoginHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_POST(self):
        if urlparse(self.path).path != "/login":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length) if length else b""
        try:
            data = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._json(400, {"ok": False, "error": "Invalid request."})
            return

        email = data.get("email", "")
        password = data.get("password", "")
        if not isinstance(email, str) or not isinstance(password, str):
            self._json(400, {"ok": False, "error": "Invalid request."})
            return

        error = validate_login(email.strip(), password)
        if error:
            self._json(400, {"ok": False, "error": error})
            return

        self._json(401, {"ok": False, "error": "Invalid email or password."})

    def _json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def validate_login(email, password):
    if email == "" or password == "":
        return "Email and password are required."
    if "@" not in email:
        return "Email must contain @."
    if len(password) < 8:
        return "Password must be at least 8 characters."
    return ""


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8080), LoginHandler)
    print("Login form at http://127.0.0.1:8080")
    server.serve_forever()
