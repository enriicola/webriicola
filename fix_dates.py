import os
import json
import subprocess
import datetime

# Local directory relative to the script
target_dir = 'cat_photos'
output_file = 'photos.json'

def get_exif_date(path):
    try:
        # Get ALL properties from the image
        output = subprocess.check_output(
            ['identify', '-verbose', path],
            stderr=subprocess.DEVNULL
        ).decode()
        
        # We want to find a date that looks like YYYY:MM:DD or YYYY-MM-DD
        # and specifically NOT from 2026 (today) if possible.
        candidates = []
        for line in output.split('\n'):
            line = line.strip()
            if 'date' in line.lower() or 'time' in line.lower():
                # Extract something that looks like a date: 20XX:XX:XX or 20XX-XX-XX
                import re
                match = re.search(r'(20\d{2}[:/-]\d{2}[:/-]\d{2})', line)
                if match:
                    date_found = match.group(1)
                    # If it's a past year, it's a high-quality candidate
                    if not date_found.startswith('2026'):
                        return line.split(':', 1)[1].strip() if ':' in line else date_found
                    candidates.append(line.split(':', 1)[1].strip() if ':' in line else date_found)
        
        # If we only found 2026 dates, use the first one found
        if candidates:
            return candidates[0]
            
        # 2. Final resort: File system modification time
        ts = os.path.getmtime(path)
        return datetime.datetime.fromtimestamp(ts).strftime('%Y:%m:%d %H:%M:%S')
    except Exception:
        return "Unknown Date"

def main():
    if not os.path.exists(target_dir):
        print(f"Error: Directory '{target_dir}' not found.")
        return

    photos = []
    # Sort files to maintain cat_001, cat_002 order
    files = sorted(os.listdir(target_dir))

    print(f"Processing {len(files)} files in {target_dir}...")

    for f in files:
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(target_dir, f)
            date = get_exif_date(path)
            
            # The webapp expects the path relative to index.html
            photos.append({
                "url": f"cat_photos/{f}",
                "date": date
            })
            print(f"✓ {f}: {date}")

    with open(output_file, 'w') as out:
        json.dump(photos, out, indent=2)

    print(f"\nSuccessfully wrote {len(photos)} entries to {output_file}")

if __name__ == "__main__":
    main()
