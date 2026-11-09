#!/usr/bin/env python3
"""Send a built email through Buttondown (https://buttondown.com, API v1).
Usage: send_buttondown.py --html FILE --subject FILE|TEXT [--tag daily|weekly|monthly] [--dry-run]
Needs BUTTONDOWN_API_KEY in the environment. With --tag, only subscribers carrying that tag receive it.
Without a key, prints what would be sent and exits 0 (so the workflow stays green before the account exists)."""
import argparse, json, os, sys, urllib.request
ap = argparse.ArgumentParser()
ap.add_argument("--html", required=True); ap.add_argument("--subject", required=True)
ap.add_argument("--tag"); ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()
body = open(a.html, encoding="utf-8").read()
subject = open(a.subject, encoding="utf-8").read().strip() if os.path.exists(a.subject) else a.subject
key = os.environ.get("BUTTONDOWN_API_KEY")
payload = {"subject": subject, "body": body, "status": "about_to_send", "email_type": "public"}
if a.tag: payload["included_tags"] = [a.tag]
if not key or a.dry_run:
    print("DRY RUN (no BUTTONDOWN_API_KEY)" if not key else "DRY RUN", json.dumps({k: v for k, v in payload.items() if k != "body"}), f"{len(body)} chars of HTML")
    sys.exit(0)
req = urllib.request.Request("https://api.buttondown.com/v1/emails", data=json.dumps(payload).encode(),
                             headers={"Authorization": f"Token {key}", "Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(req, timeout=60) as r:
    print(r.status, r.read()[:300].decode())
