#!/usr/bin/env python3
"""Send a built email through the self-hosted subscription API: the Cloudflare Worker (infra/subscribe-worker) or the
Apps Script web app (infra/subscribe-apps-script; SUBSCRIBE_API is then the .../exec URL on script.google.com).
Usage: send_selfhosted.py --html FILE --text FILE --subject FILE|TEXT --tag daily|weekly|monthly[-fr] [--dry-run]
Needs SUBSCRIBE_API (e.g. https://living-review-subscribe.<account>.workers.dev or https://api.your-domain.tld)
and SEND_TOKEN in the environment. Without them it prints what it would send and exits 0."""
import argparse, json, os, sys, urllib.request
ap = argparse.ArgumentParser()
ap.add_argument("--html", required=True); ap.add_argument("--text"); ap.add_argument("--subject", required=True)
ap.add_argument("--tag", default="weekly"); ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()
html = open(a.html, encoding="utf-8").read()
text = open(a.text, encoding="utf-8").read() if a.text and os.path.exists(a.text) else ""
subject = open(a.subject, encoding="utf-8").read().strip() if os.path.exists(a.subject) else a.subject
api, tok = os.environ.get("SUBSCRIBE_API", "").rstrip("/"), os.environ.get("SEND_TOKEN")
payload = {"subject": subject, "html": html, "text": text, "tag": a.tag, "dry_run": a.dry_run}
if not api or not tok:
    print("DRY RUN (no SUBSCRIBE_API / SEND_TOKEN):", json.dumps({k: v for k, v in payload.items() if k not in ("html", "text")}), f"{len(html)} chars"); sys.exit(0)
if "script.google.com" in api:   # Apps Script cannot read request headers: token travels in the body; the reply comes after a redirect
    payload["token"] = tok
    req = urllib.request.Request(f"{api}?action=send", data=json.dumps(payload).encode(), headers={"Content-Type": "text/plain;charset=UTF-8"}, method="POST")
else:
    req = urllib.request.Request(f"{api}/api/send", data=json.dumps(payload).encode(), headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(req, timeout=120) as r:
    out = json.loads(r.read().decode()); print(json.dumps(out)); sys.exit(0 if out.get("ok") else 1)
