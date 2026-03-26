#!/usr/bin/env python3
import subprocess, sys

PORT = 8001
URL = f"http://localhost:{PORT}/"

print(f"--- DISNEY MINUS (Text Only) ---")
print(f"Serving at: {URL}")

try:
    subprocess.run(["go", "run", "main.go"])
except KeyboardInterrupt:
    print("\nShutting down server")
