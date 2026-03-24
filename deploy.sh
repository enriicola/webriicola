#!/bin/bash

set -euo pipefail

SRC_PATH="/home/ubuntu/webriicola"
DEST_PATH="/var/www/html"

cd "$SRC_PATH" 

PRE_PULL_HEAD="$(git rev-parse HEAD)"
git pull --ff-only origin main 

if ! git diff --quiet "$PRE_PULL_HEAD" HEAD -- gohan/imgs/; then
    python3 "$SRC_PATH/gohan/index_photos.py"
fi

# sync to Nginx dest_path
sudo rsync -av --delete \
    --exclude='*git*' \
    --exclude='.jj*' \
    --exclude='*.sh' \
    --exclude='*.md' \
    --exclude='*.py' \
    "$SRC_PATH/" "$DEST_PATH/"

sudo chown -R www-data:www-data "$DEST_PATH"
sudo find "$DEST_PATH" -type d -exec chmod 755 {} +
sudo find "$DEST_PATH" -type f -exec chmod 644 {} +

echo -e "\nDeployed\n"