#!/usr/bin/env python3
import http.server
import socketserver
from pathlib import Path

OUT = Path(__file__).parent / "out"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(OUT), **kwargs)

if __name__ == "__main__":
    with socketserver.TCPServer(("0.0.0.0", 5050), Handler) as httpd:
        print("Serving files from /out at http://0.0.0.0:5050")
        httpd.serve_forever()