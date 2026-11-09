#!/usr/bin/env bash
# Deploy the subscription web app into the dedicated Google account, with clasp (Google's Apps Script CLI).
# Run from this folder, in a terminal, logged out of other Google accounts in the browser that opens.
#   bash deploy.sh            # first time: login, create Sheet + script, push, deploy, open for the one permission click
#   bash deploy.sh update     # later: push code changes and publish a new version at the same URL
set -euo pipefail
cd "$(dirname "$0")"
[ -f Config.gs ] || { echo "Config.gs missing: cp Config.example.gs Config.gs and fill SEND_TOKEN"; exit 1; }
CLASP="npx --yes @google/clasp@2"
if [ "${1:-}" = update ]; then
  $CLASP push -f
  ID=$(sed -n 's/.*"deploymentId": *"\([^"]*\)".*/\1/p' .deploy.json 2>/dev/null | head -1)
  [ -n "$ID" ] && $CLASP deploy -i "$ID" -d "web app $(date +%F)" || $CLASP deploy -d "web app $(date +%F)"
  echo "Updated. URL unchanged."; exit 0
fi
echo "1/5 Login with the NEW account (ai.economics.brief@gmail.com or the one you created)."
$CLASP login
echo "2/5 Creating the Google Sheet 'Living review subscribers' with its bound script..."
$CLASP create --type sheets --title "Living review subscribers" --rootDir . | tee .create.log
echo "3/5 Pushing Code.gs, Config.gs, appsscript.json..."
$CLASP push -f
echo "4/5 Deploying as a web app (access: anyone, runs as you)..."
$CLASP deploy -d "web app $(date +%F)" | tee .deploy.log
ID=$(grep -o -- '- [A-Za-z0-9_-]\{20,\}' .deploy.log | head -1 | sed 's/^- //')
echo "{\"deploymentId\": \"$ID\"}" > .deploy.json
URL="https://script.google.com/macros/s/$ID/exec"
echo
echo "5/5 ONE MANUAL CLICK: the editor opens. Pick the function 'setup' in the toolbar, press Run, accept the permissions"
echo "    (Sheets + send mail). That stores the settings and authorises Gmail. Then come back and run:"
echo "    bash finish.sh $URL your-test-address@example.org"
$CLASP open || true
echo "$URL" > .exec-url
