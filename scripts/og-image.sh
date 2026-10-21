#!/usr/bin/env sh
# Régénère static/images/og-legal-smart.png (aperçu LinkedIn et réseaux) avec Chrome ou Chromium.
set -e
cd "$(dirname "$0")/.."
CHROME="${CHROME:-$(command -v google-chrome || command -v chromium || command -v chromium-browser)}"
"$CHROME" --headless=new --disable-gpu --no-sandbox --hide-scrollbars --allow-file-access-from-files \
  --window-size=1200,630 --screenshot="$PWD/static/images/og-legal-smart.png" "file://$PWD/scripts/og-image.html"
