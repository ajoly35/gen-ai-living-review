# Self-hosted subscriptions for the living review

What econvitals.org does: a static site, a `/api/subscribe` function of its own, confirmed opt-in, mail sent from
`briefings@econvitals.org`, no Substack or Mailchimp in the loop. This folder is the same design for a GitHub Pages
site. The list is yours (a SQLite database you can export), the form is on your site, the emails come from your
domain, and the daily/weekly/monthly sending is done by the repository's own workflow.

```
reader → site form (JSON POST) → Cloudflare Worker /api/subscribe → D1 row (pending) → confirmation email
reader clicks → /api/confirm → row confirmed → /subscribed/ page
GitHub Action (email.yml) → scripts/send_selfhosted.py → /api/send (bearer token) → one email per confirmed reader of that rhythm
every email → List-Unsubscribe headers + link → /api/unsubscribe → row unsubscribed
```

Why a Worker and not a mail server: the only part worth owning is the list and the form. Running your own SMTP
server gets you blocked by Gmail and Outlook within days; econvitals almost certainly sends through a relay too.
The Worker calls a transactional relay over HTTPS (Resend by default, Postmark as the alternative) that signs the
mail for your domain. You can swap the relay by editing one function (`sendBatch`).

## What you need (about one hour, once)

| Step | Where | Notes |
|---|---|---|
| 1. A domain | any registrar, about 10 EUR a year | Needed to send from your own address. `ajoly35.github.io` cannot sign mail. |
| 2. Cloudflare account (free) | dash.cloudflare.com | Workers: 100,000 requests a day free; D1: 5 GB free. More than enough. |
| 3. `npm i -g wrangler && wrangler login` | this folder | then `wrangler d1 create living-review-subscribers`, paste the id into `wrangler.toml`, `wrangler d1 execute living-review-subscribers --remote --file=schema.sql` |
| 4. Resend account (free: 3,000 emails a month, 100 a day; 20 USD a month for 50,000) | resend.com | Add your domain; Resend gives you three DNS records (SPF `TXT`, DKIM `TXT`, MX for bounces). Add a DMARC record too: `_dmarc TXT "v=DMARC1; p=quarantine; rua=mailto:you@..."`. Wait for "verified". |
| 5. Secrets | this folder | `wrangler secret put RESEND_API_KEY`, `wrangler secret put SEND_TOKEN` (any long random string: `openssl rand -hex 32`) |
| 6. Vars | `wrangler.toml` | set `MAIL_FROM` to `Gen-AI, Jobs and Growth <briefings@your-domain.tld>`; keep `ALLOWED_ORIGIN` as the GitHub Pages origin |
| 7. Deploy | `wrangler deploy` | prints the URL `https://living-review-subscribe.<account>.workers.dev`. Optional: `api.your-domain.tld` route once the domain's DNS is on Cloudflare. |
| 8. Site | `_config.yml` | `subscribe_api: "https://living-review-subscribe.<account>.workers.dev"` (no trailing slash). The sign-up box switches to the self-hosted form by itself. |
| 9. Repository secrets | GitHub → Settings → Secrets → Actions | `SUBSCRIBE_API` (same URL) and `SEND_TOKEN` (same string). The email workflow then sends through your list; without them it stays a dry run. |

## Test before telling anyone
```
curl -s -X POST https://<worker>/api/subscribe -H 'Content-Type: application/json' \
  -d '{"email":"you@your-domain.tld","name":"Test","frequency":"daily","lang":"en"}'      # -> confirmation email
# click the link, then:
curl -s -H "Authorization: Bearer $SEND_TOKEN" https://<worker>/api/stats
cd site && python3 -I scripts/build_email.py --latest 1 --kind daily --lang en --out /tmp/e
SUBSCRIBE_API=https://<worker> SEND_TOKEN=... python3 -I scripts/send_selfhosted.py --html /tmp/e/*-daily-en.html --text /tmp/e/*-daily-en.txt --subject /tmp/e/*-daily-en.subject --tag daily --dry-run
```
`--dry-run` asks the Worker to count recipients without sending. Drop it for a real send.

## Operating it
- **Export the list**: `wrangler d1 execute living-review-subscribers --remote --command "SELECT email,name,frequency,lang,status,created_at FROM subscribers" --json > subscribers.json`.
- **Add someone by hand** (they still get the confirmation email): POST to `/api/subscribe` with curl as above.
- **Rhythms**: `daily` goes out on each push that adds entries (about 05:00 London), `weekly` on Mondays 07:00 UTC, `monthly` on the 1st at 07:10 UTC; French readers are the same tags with `-fr`. Tags are set by the form; readers change them by signing up again with the same address.
- **Bounces and complaints**: Resend suppresses hard bounces itself. Check its dashboard monthly; delete dead rows with `wrangler d1 execute ... --command "DELETE FROM subscribers WHERE email='...'"`.
- **Costs at scale**: 300 readers × 1 daily email × 22 working days ≈ 6,600 emails a month: above Resend's free tier, so the 20 USD plan, or move the Worker's `sendBatch` to Amazon SES (0.10 USD per 1,000; needs an AWS account, a production-access request and SigV4 signing, which is why it is not the default).
- **Data protection**: the database holds email, optional name, rhythm, language, status, timestamps and a truncated hash of the IP at sign-up (anti-abuse). Confirmed opt-in, one-click unsubscribe and List-Unsubscribe headers meet the Gmail/Yahoo bulk-sender rules of 2024. Say in the site's footer where the data lives (Cloudflare, EU/US) if you want a privacy line.

## Alternatives, if you prefer
- **Netlify, like econvitals**: move the Jekyll site to Netlify (free), put `index.js` into `netlify/functions/subscribe.js` with Netlify Blobs or a hosted Postgres instead of D1. Same code shape, one more migration.
- **Buttondown**: keep the list on a third party; `_includes/signup.html` and `scripts/send_buttondown.py` still support it (`buttondown_username`, `BUTTONDOWN_API_KEY`). Zero infrastructure, but the list is not yours and the free tier stops at 100 readers.

## Files
`wrangler.toml` (config), `schema.sql` (two tables), `src/index.js` (the API, about 150 lines, no dependencies),
`../../scripts/send_selfhosted.py` (called by `.github/workflows/email.yml`), site pages `/subscribed/`, `/unsubscribed/` and their French twins.
Tested on 9 November 2026 with an in-memory database and a stubbed mail API (subscribe, bad email, honeypot, confirm, preference update, authorised and unauthorised send, personalised unsubscribe link and headers, one-click unsubscribe, stats, CORS preflight).
