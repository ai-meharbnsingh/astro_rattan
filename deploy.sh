#!/bin/bash
# deploy.sh — AstroRattan production deploy
# Usage: bash deploy.sh
# Run from: /app/astro_rattan on the Hostinger VPS

set -e

REPO_DIR="/app/astro_rattan"
FRONTEND_DIR="$REPO_DIR/frontend"
PROD_DIST="/var/www/astrorattan/dist"

echo ""
echo "=== AstroRattan Deploy === $(date)"
echo ""

# 1. Pull latest code
echo "[1/4] Pulling latest code..."
cd "$REPO_DIR"
git fetch origin
git checkout main
git reset --hard origin/main
echo "      $(git log --oneline -1)"

# 2. Build frontend directly (output -> frontend/dist, served by nginx)
echo "[2/4] Building frontend..."
cd "$FRONTEND_DIR"
npm ci --silent
npm run build
echo "      Built -> $FRONTEND_DIR/dist"
echo "      Syncing -> $PROD_DIST"
mkdir -p "$PROD_DIST"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete "$FRONTEND_DIR/dist/" "$PROD_DIST/"
else
  rm -rf "$PROD_DIST"/*
  cp -R "$FRONTEND_DIR/dist/"* "$PROD_DIST/"
fi

# 3. Restart backend container
echo "[3/4] Restarting backend..."
cd "$REPO_DIR"
docker compose up -d --build backend
echo "      Backend up"

# 4. Reload nginx (picks up new frontend/dist immediately)
echo "[4/4] Reloading nginx..."
nginx -s reload
echo "      Nginx reloaded"

echo ""
echo "=== DEPLOYED ==="
echo "Commit : $(git log --oneline -1)"
echo "Site   : https://astrorattan.com"
echo ""
