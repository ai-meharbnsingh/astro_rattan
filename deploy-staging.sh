#!/bin/bash
# deploy-staging.sh — AstroRattan STAGING deploy
# Usage: bash deploy-staging.sh
# Run from: /app/astro_rattan on the Hostinger VPS
# Staging site: http://145.223.21.39:3001
# Staging API:  http://145.223.21.39:8029

set -e

REPO_DIR="/app/astro_rattan"
FRONTEND_DIR="$REPO_DIR/frontend"
STAGING_DIST="$REPO_DIR/frontend/dist-staging"

echo ""
echo "=== AstroRattan STAGING Deploy === $(date)"
echo ""

# 1. Pull latest staging branch
echo "[1/5] Pulling staging branch..."
cd "$REPO_DIR"
git fetch origin
git checkout staging
git reset --hard origin/staging
echo "      $(git log --oneline -1)"

# 2. Build frontend into dist-staging (separate from production dist)
echo "[2/5] Building frontend (staging)..."
cd "$FRONTEND_DIR"
npm ci --silent
VITE_API_URL="" npm run build -- --outDir dist-staging
echo "      Built -> $STAGING_DIST"

# 3. Restart staging backend container
echo "[3/5] Restarting staging backend (port 8029)..."
cd "$REPO_DIR"
docker compose -f docker-compose.staging.yml up -d --build
echo "      Backend staging up"

# 4. Reload nginx
echo "[4/5] Reloading nginx..."
nginx -s reload
echo "      Nginx reloaded"

# 5. Health check
echo "[5/5] Health check..."
sleep 3
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8029/health)
echo "      Staging API health: $STATUS"

echo ""
echo "=== STAGING DEPLOYED ==="
echo "Commit  : $(git log --oneline -1)"
echo "Site    : http://145.223.21.39:3001"
echo "API     : http://145.223.21.39:8029"
echo "DB      : astrorattan_staging"
echo ""
