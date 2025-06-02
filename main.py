#!/usr/bin/env python3
import http.server
import socketserver
import signal
import socket
import sys
from pathlib import Path

OUT = Path(__file__).parent / "out"
PORT = 5052

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(OUT), **kwargs)

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def signal_handler(signum, frame):
    print("\nShutting down server...")
    sys.exit(0)

if __name__ == "__main__":
    if is_port_in_use(PORT):
        print(f"Error: Port {PORT} is already in use. Please free up the port or choose a different one.")
        sys.exit(1)

    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    with ReusableTCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Serving files from /out at http://0.0.0.0:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.server_close()