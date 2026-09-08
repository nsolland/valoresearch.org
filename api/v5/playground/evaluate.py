"""
VALO Gate Evaluation API — Vercel Serverless
Requires API key for write access.
"""
import os
import json
import hashlib
import time
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_POST(self):
        api_key = os.environ.get("VALO_API_KEY")
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode() if content_length > 0 else "{}"

        try:
            data = json.loads(body)
        except:
            data = {}

        auth_header = self.headers.get("Authorization", "")
        provided_key = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else ""

        if api_key and provided_key != api_key:
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid API key"}).encode())
            return

        # Simple evaluation: just echo back with hash
        content = data.get("content", "")
        h = hashlib.sha256(content.encode()).hexdigest()[:16]

        result = {
            "hash": h,
            "timestamp": time.time(),
            "status": "evaluated",
            "content_length": len(content),
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
