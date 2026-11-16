#!/usr/bin/env python3
# Tideboard API: one health endpoint. Standard library only, so the
# stock python image runs it with nothing to install.
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# The secret arrives as an environment variable (from tideboard.env)
TOKEN = os.environ.get("TIDEBOARD_API_TOKEN", "")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/health", "/api/health"):
            if not TOKEN:
                # No secret means misconfigured: say so with a 500
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"missing token\n")
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok","site":"NARR"}\n')
            return
        self.send_response(404)
        self.end_headers()

    def log_message(self, fmt, *args):
        return # keep per-request logs quiet

if __name__ == "__main__":
    # Listen on port 8000 inside the container only
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
