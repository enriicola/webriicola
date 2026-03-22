#!/usr/bin/env python3
import http.server, webbrowser, sys

PORT = 8000
URL = f"http://localhost:{PORT}/"

print(f"--- webriicola testing @ {URL} ---")
if "--open" in sys.argv or "-o" in sys.argv: 
    webbrowser.open(URL)
    print("Opening web browser...")

# http.server.test handles the server loop and address reuse automatically
http.server.test(http.server.SimpleHTTPRequestHandler, port=PORT)
