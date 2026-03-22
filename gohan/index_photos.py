import json
from pathlib import Path

# Configuration relative to this script location, not current working directory.
BASE_DIR = Path(__file__).resolve().parent
TARGET_DIR = BASE_DIR / 'imgs'
OUTPUT_FILE = BASE_DIR / 'photos.json'

def main():
    if not TARGET_DIR.exists():
        print(f"Error: Directory '{TARGET_DIR}' not found.")
        raise SystemExit(1)

    # Filter for image files and sort them
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    photos = [
        f"imgs/{f.name}"
        for f in sorted(TARGET_DIR.iterdir())
        if f.is_file() and f.suffix.lower() in valid_extensions
    ]

    # Write the simplified list of strings to photos.json
    with open(OUTPUT_FILE, 'w') as out:
        json.dump(photos, out, indent=2)

    print(f"Successfully indexed {len(photos)} photos to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
