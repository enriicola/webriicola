import os
import json

# Configuration
target_dir = 'cat_photos'
output_file = 'photos.json'

def main():
    if not os.path.exists(target_dir):
        print(f"Error: Directory '{target_dir}' not found.")
        return

    # Filter for image files and sort them
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    photos = [
        f"{target_dir}/{f}" 
        for f in sorted(os.listdir(target_dir)) 
        if f.lower().endswith(valid_extensions)
    ]

    # Write the simplified list of strings to photos.json
    with open(output_file, 'w') as out:
        json.dump(photos, out, indent=2)

    print(f"Successfully indexed {len(photos)} photos to {output_file}")

if __name__ == "__main__":
    main()
