#!/usr/bin/env python3
import json
import urllib.request
import os
import subprocess

API_URL = "http://localhost:8001/api/videos"

def get_videos():
    try:
        with urllib.request.urlopen(API_URL) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return []

def main():
    print("--- DISNEY MINUS TUI BROWSER ---")
    videos = get_videos()
    if not videos:
        print("No videos found. Is the server running? (run ./run.py)")
        return

    # Sort videos by group
    videos.sort(key=lambda x: (x['group'], x['title']))

    current_group = ""
    for i, v in enumerate(videos):
        if v['group'] != current_group:
            current_group = v['group']
            print(f"\n[{current_group}]")
        print(f"  {i:3}: {v['title']}")

    print("\n" + "="*30)
    choice = input("Select video number (or 'q' to quit): ")
    if choice.lower() == 'q':
        return

    try:
        idx = int(choice)
        video = videos[idx]
        url = f"http://localhost:8001/{video['path']}"
        print(f"\nSelected: {video['title']}")
        print(f"Stream URL: {url}")
        print(f"VLC URL:    vlc://{url}")
        
        play = input("\nTry to open in local VLC? (y/n): ")
        if play.lower() == 'y':
            # Try common vlc commands
            opened = False
            for cmd in ['vlc', 'cvlc', 'nvlc']:
                try:
                    subprocess.Popen([cmd, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    print(f"Launched {cmd}!")
                    opened = True
                    break
                except FileNotFoundError:
                    continue
            if not opened:
                print("Could not find VLC locally. Please copy the URL above.")
    except (ValueError, IndexError):
        print("Invalid choice.")

if __name__ == "__main__":
    main()
