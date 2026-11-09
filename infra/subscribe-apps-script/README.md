# Subscriptions with Google: GitHub Pages site, Apps Script list, Gmail sending

The site stays where it is. Only the list and the sending live in your Google account: a Google Sheet holds the
subscribers, an Apps Script web app is the `/api`, and Gmail sends the confirmation emails and the digests.
Same design as econvitals.org (own confirmed opt-in form, own list) and the same endpoints as the Cloudflare
version in `../subscribe-worker/`, so the site's sign-up form and the email workflow work with either.

```
reader → site form → POST <exec URL>?action=subscribe → row in the Sheet (pending) → confirmation email from Gmail
reader clicks → ?action=confirm&t=… → row confirmed → /subscribed/ page
GitHub Action (email.yml) → scripts/send_selfhosted.py → POST ?action=send (token in body) → one Gmail per confirmed reader
every email → unsubscribe link → ?action=unsubscribe&t=… → row unsubscribed
```

## Free Gmail or Google Workspace

| | Free Gmail account | Google Workspace (from about 6 EUR a month) |
|---|---|---|
| Sender | your @gmail.com address, display name "Gen-AI, Jobs and Growth" | any address on your domain, e.g. briefings@your-domain.tld (set `FROM_ALIAS` after adding it under Gmail > Settings > Accounts > "Send mail as") |
| Emails a day (MailApp quota, confirmations included) | 100 | 1,500 |
| Enough for | about 90 daily readers, or several hundred weekly ones | about 1,400 daily readers |
| Deliverability | good (Google signs), but bulk mail from a personal account can trip Gmail's own limits | good; SPF/DKIM come with the Workspace domain set-up |
| Code | identical | identical, plus the `FROM_ALIAS` property |

Over quota, the script sends what it can, records the number skipped in the `sends` sheet and returns it in the
JSON, so a run never fails silently. The LSE address cannot be the sender: Apps Script sends only from the Google
account that owns the script (or its verified aliases).

## Step 0: a dedicated Google account (yours to create, 5 minutes)
Decision of 9 November 2026: a separate free Gmail account, not the personal one. Create it at accounts.google.com
(a phone number is required for verification). Two constraints on the address:
- Gmail usernames allow only letters, digits and dots, no hyphens: `AI-economics-brief` is not possible. Candidates in
  order: `ai.economics.brief@gmail.com`, `aieconomicsbrief@gmail.com`, `genai.jobs.growth@gmail.com`,
  `economicsofai.brief@gmail.com`. Dots are ignored by Gmail, so `ai.economics.brief` and `aieconomicsbrief` are the
  same mailbox if one is taken the other is too.
- Set the account's display name to "AI Economics Brief" (the script's default `SENDER_NAME`), turn on 2-step
  verification, and set a recovery email to one of your own addresses.
New Gmail accounts can be rate-limited by Google in their first weeks (sometimes temporary 24-hour blocks).
Adrien's decision (9 Nov 2026): offer the daily rhythm from day one, no warm-up; if a send is blocked, the
`sends` sheet records the skipped count and the next run retries. Do everything below while logged into
that account only (open a private window), so the Sheet, the script and the web app belong to it.

## Two rules learned the hard way (9 November 2026)
1. **Never run `clasp create-deployment` or `clasp update-deployment` for the web app.** Both produce a deployment with only a
   library entry point (the web app URL answers 404 or a Drive "unable to open" page). Create the web app once in the editor
   (Deploy > New deployment > Web app) and publish new code with Deploy > Manage deployments > pencil > Version: New version >
   Deploy. `clasp push -f` is fine for uploading code; it changes nothing until a version is published.
2. **Never put a `script.google.com` link in an email.** When a reader is signed in to Google, the link is rewritten to a
   `/macros/u/N/s/...` path that the anonymous web app rejects. Confirmation and unsubscribe links therefore point to the
   site (`/subscribed/?t=…`, `/unsubscribed/?t=…`, French twins under `/fr/`), whose page calls `?action=confirm&json=1` with
   `fetch(..., {credentials: 'omit'})`, which carries no Google login and works. The one-click List-Unsubscribe POST from mail
   clients still hits the script URL directly, which works because mail clients send no Google cookies either.

## Audiences and tags
Subscribers tick one or more rhythms (daily, weekly, monthly) and one or both formats, stored as comma-separated lists in the `frequency` and `audience` cells (a send to tag `weekly-academic` reaches every confirmed reader whose lists contain `weekly` and `academic`). Formats: **general** (the plain-language brief: what it explores, why
it matters, how it fits the evidence, one chart) or **academic** (the full entry). The Sheet has an `audience` column; the send
tag is `freq[-academic][-fr]`, e.g. `daily`, `daily-academic`, `weekly-fr`, `monthly-academic-fr`. The email workflow builds and
sends the four variants per run. The general brief reads the `**In brief.**` block the routine writes under each entry (three
labelled lines) and falls back to the entry's own sentences when the block is missing (older entries).

## State on 9 November 2026 (done by Claude with Adrien in Chrome)
- Account `ai.economics.brief@gmail.com` created (display name AI Economics Brief); Apps Script API on for that account only.
- Sheet "Living review subscribers" (id `1rUSNVJqMPpqCQQ_iEX09J6MWlRpb7ooB4j_Rd0p2MYc`) with bound script `1K2tXlJe69b_O16lTQ6pNkGgWLJEevkNdcr2aszWXF7E8pmfjy7uedJIl`, code pushed with clasp, `setup()` run and permissions granted.
- Web app deployment "subscribe API v2" (the one to keep): `https://script.google.com/macros/s/AKfycbzNbccDjO406eqRFg-ntUJnTdtrUz3dboH-Y-lzjQYNaywWSiC5cU3hgSbRXF3Lxw/exec` (also in `.exec-url` and in `Config.gs` as `EXEC_URL`). v1 was broken by `clasp update-deployment` and deleted. `deploy.sh update` now only pushes code; publish the version in the editor.
- `_config.yml` `subscribe_api` set; GitHub secrets `SUBSCRIBE_API` and `SEND_TOKEN` set on ajoly35/gen-ai-living-review. Stats endpoint answers; a test subscription for a.p.joly@lse.ac.uk is pending confirmation.
- Site not yet committed or pushed.

## Set-up from scratch (about 20 minutes, logged in as the new account)
1. Create a Google Sheet named "Living review subscribers". Extensions > Apps Script. Replace the default code with `Code.gs`. Save.
2. Project settings (gear) > Script properties: `SITE_URL` = `https://ajoly35.github.io/gen-ai-living-review`, `SEND_TOKEN` = a long random string (`openssl rand -hex 32`), `SENDER_NAME` = `AI Economics Brief`, `REPLY_TO` = `a.p.joly@lse.ac.uk`. Workspace only: `FROM_ALIAS` = `briefings@your-domain.tld`.
3. Deploy > New deployment > type "Web app" > Execute as **Me**, Who has access **Anyone** > Deploy. Authorise the scopes (Sheets, Mail; Gmail too if `FROM_ALIAS` is set). Copy the URL ending in `/exec`.
4. Site: in `_config.yml`, `subscribe_api: "https://script.google.com/macros/s/…/exec"`. The sign-up box switches to the self-hosted form.
5. GitHub repository secrets: `SUBSCRIBE_API` (same URL) and `SEND_TOKEN` (same string). The email workflow sends through the Sheet from the next run.
6. Each time you change `Code.gs`, Deploy > Manage deployments > edit > New version (the URL stays the same).

## Test
```
curl -sL -X POST "<exec URL>?action=subscribe" -H 'Content-Type: text/plain' -d '{"email":"you@…","name":"Test","frequency":"daily","lang":"en"}'
# click the link in the email, then
curl -sL "<exec URL>?action=stats&token=<SEND_TOKEN>"
SUBSCRIBE_API="<exec URL>" SEND_TOKEN=… python3 -I scripts/send_selfhosted.py --html emails/2026-11-09-daily-en.html --text emails/2026-11-09-daily-en.txt --subject emails/2026-11-09-daily-en.subject --tag daily --dry-run
```
(`-L` matters: Apps Script answers with a redirect to the result.)

## Operating it
- The Sheet is the list: sort, filter, export to CSV, delete a row to remove someone. Columns: email, name, frequency, lang, status, token, created_at, confirmed_at, unsubscribed_at. A second sheet, `sends`, logs every send with recipients, sent and skipped.
- Readers change rhythm by signing up again with the same address (no new confirmation email once confirmed).
- Unsubscribe is a link in every email (one-click POST also accepted). Gmail adds its own unsubscribe header for bulk mail from Workspace accounts.
- If you later move to the Cloudflare version, export the Sheet and import it into D1; the form and the workflow need only the new URL.

Tested on 9 November 2026 with stubbed Google services (subscribe, bad address, honeypot, confirm, preference update keeping the name, unauthorised and authorised send, personalised unsubscribe link in HTML and text, dry run, quota exhaustion, one-click unsubscribe, stats, alias sending through GmailApp).
