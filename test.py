#!/usr/bin/env python3
import subprocess, webbrowser, sys, time

PORT = 8000
URL = f"http://localhost:{PORT}/"

print(f"--- webriicola testing @ {URL} ---")
if "--open" in sys.argv or "-o" in sys.argv: 
    time.sleep(0.5)
    webbrowser.open(URL)
    print("Opening web browser...")

try:
    subprocess.run(["php", "-S", f"localhost:{PORT}"])
except KeyboardInterrupt:
    print("\nShutting down server")
