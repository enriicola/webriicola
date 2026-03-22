#!/bin/bash

set -euo pipefail

LOG_FILE="/home/ubuntu/deploy.log"
REPO_PATH="/home/ubuntu/webriicola"
DEST_PATH="/var/www/html"
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

cd "$REPO_PATH" || { echo -e "${RED}Error: folder not found${NC}"; exit 1; }

# Deterministic deploy source: fetch + reset avoids server-side merge commits
git fetch --prune origin main | tee -a "$LOG_FILE"

if ! git rev-parse --verify --quiet origin/main >/dev/null; then
    echo -e "${RED}Error: invalid git ref: origin/main${NC}" | tee -a "$LOG_FILE"
    exit 1
fi

# photos have to be indexed after the reset, in order to not be overwritten by the reset itself
INDEX_PHOTOS=0
if ! git diff --quiet HEAD origin/main -- gohan/imgs/; then
    INDEX_PHOTOS=1
fi

git reset --hard origin/main | tee -a "$LOG_FILE"

if [[ "$INDEX_PHOTOS" -eq 1 ]]; then
    python3 "$REPO_PATH/gohan/index_photos.py" | tee -a "$LOG_FILE"
fi

# sync to Nginx dest_path
sudo -n rsync -av --delete \
    --exclude='.git/' \
    --exclude='.gitignore' \
    --exclude='deploy.sh' \
    --exclude='test.py' \
    --exclude='README.md' \
    --exclude='*.py' \
    "$REPO_PATH/" "$DEST_PATH/" | tee -a "$LOG_FILE"

sudo -n chown -R www-data:www-data "$DEST_PATH"
sudo -n find "$DEST_PATH" -type d -exec chmod 755 {} +
sudo -n find "$DEST_PATH" -type f -exec chmod 644 {} +

# No reload required for static file updates; just ensure nginx is running
sudo -n systemctl is-active --quiet nginx | tee -a "$LOG_FILE"

echo -e "${GREEN}Deployed\n${NC}"