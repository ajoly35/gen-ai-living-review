#!/usr/bin/env bash
# After deploy.sh and the permission click: wire the web app URL into the site and GitHub, and run a live test.
#   bash finish.sh https://script.google.com/macros/s/.../exec you@example.org
set -euo pipefail
cd "$(dirname "$0")"
URL="${1:?exec URL}"; TEST="${2:-}"
TOKEN=$(sed -n 's/.*SEND_TOKEN: *"\([^"]*\)".*/\1/p' Config.gs)
SITE="$(cd ../.. && pwd)"
python3 - "$SITE/_config.yml" "$URL" <<'PY'
import sys,re; p,url=sys.argv[1],sys.argv[2]; s=open(p).read()
s=re.sub(r'subscribe_api: *"[^"]*"', f'subscribe_api: "{url}"', s); open(p,"w").write(s); print("config: subscribe_api set")
PY
gh secret set SUBSCRIBE_API -R ajoly35/gen-ai-living-review -b "$URL" && echo "GitHub secret SUBSCRIBE_API set"
gh secret set SEND_TOKEN -R ajoly35/gen-ai-living-review -b "$TOKEN" && echo "GitHub secret SEND_TOKEN set (same value as Config.gs)"
echo "--- stats (should answer ok:true):"; curl -sL "$URL?action=stats&token=$TOKEN"; echo
if [ -n "$TEST" ]; then
  echo "--- subscribing $TEST (a confirmation email should arrive):"
  # python rather than curl: curl -L turns the POST redirect into a GET that Apps Script's echo endpoint rejects
  python3 - "$URL" "$TEST" <<'PY'
import sys,json,urllib.request
req=urllib.request.Request(sys.argv[1]+"?action=subscribe", data=json.dumps({"email":sys.argv[2],"name":"Test","frequency":"weekly","lang":"en"}).encode(), headers={"Content-Type":"text/plain;charset=UTF-8"}, method="POST")
print(urllib.request.urlopen(req, timeout=60).read().decode())
PY
fi
echo "Then: review 'git -C $SITE status', commit and push the site (your yes), and the next email run goes through the Sheet."
