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
  echo "Code pushed. Now publish it: in the editor, Deploy > Manage deployments > pencil > Version: New version > Deploy."
  echo "(Do NOT use clasp deploy / update-deployment: they strip the web app entry point and the URL answers 404.)"
  $CLASP open-script || true; exit 0
fi
echo "1/5 Login with the NEW account (ai.economics.brief@gmail.com or the one you created)."
$CLASP login
echo "2/5 Creating the Google Sheet 'Living review subscribers' with its bound script..."
$CLASP create --type sheets --title "Living review subscribers" --rootDir . | tee .create.log
echo "3/5 Pushing Code.gs, Config.gs, appsscript.json..."
$CLASP push -f
echo "4/5 In the editor that opens: pick the function 'setup', press Run, accept the permissions (Sheets + send mail)."
echo "5/5 Then Deploy > New deployment > type Web app > execute as Me, access Anyone > Deploy, and copy the /exec URL."
echo "    Put it in Config.gs as EXEC_URL, run 'bash deploy.sh update', publish the new version in the editor, then:"
echo "    bash finish.sh <exec URL> your-test-address@example.org"
$CLASP open-script || true
