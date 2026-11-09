// Self-hosted subscription API for the Gen-AI living review (Cloudflare Worker + D1).
// Modelled on econvitals.org/subscribe: our own confirmed opt-in form, our own list, mail from our own domain.
// Endpoints
//   POST /api/subscribe        {name, email, frequency, lang, hp}  -> sends a confirmation email
//   GET  /api/confirm?t=TOKEN   -> status confirmed, redirect to SITE_URL/subscribed/
//   GET|POST /api/unsubscribe?t=TOKEN -> status unsubscribed (POST = RFC 8058 one-click), redirect to /unsubscribed/
//   POST /api/send   Bearer SEND_TOKEN  {subject, html, text, tag}  -> sends to confirmed subscribers of that tag
//   GET  /api/stats  Bearer SEND_TOKEN  -> counts
// Secrets: RESEND_API_KEY (or POSTMARK_TOKEN), SEND_TOKEN. Vars: SITE_URL, ALLOWED_ORIGIN, MAIL_FROM, REPLY_TO, PROVIDER.

const FREQ = new Set(["daily", "weekly", "monthly"]);
const LANG = new Set(["en", "fr"]);
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

const T = {
  en: {
    confirmSubject: "Confirm your subscription: Gen-AI, Jobs and Growth",
    confirmBody: (name, url, freq) => `<p>Hello${name ? " " + esc(name) : ""},</p>
<p>One click to confirm that you want the living review's emails (${freqLabel.en[freq]}):</p>
<p><a href="${url}" style="display:inline-block;padding:10px 16px;background:#7a2e1f;color:#fff;border-radius:6px;text-decoration:none;">Confirm my subscription</a></p>
<p style="color:#6b665e;font-size:14px;">If you did not ask for this, ignore this message and nothing will be sent. Adrien Joly, London School of Economics.</p>`,
    already: "You are already subscribed; your preferences were updated.",
    pending: "Check your inbox: a confirmation email is on its way.",
    bad: "Please enter a valid email address.",
  },
  fr: {
    confirmSubject: "Confirmez votre inscription : IA générative, emploi et croissance",
    confirmBody: (name, url, freq) => `<p>Bonjour${name ? " " + esc(name) : ""},</p>
<p>Un clic pour confirmer que vous souhaitez recevoir les courriels de la revue vivante (${freqLabel.fr[freq]}) :</p>
<p><a href="${url}" style="display:inline-block;padding:10px 16px;background:#7a2e1f;color:#fff;border-radius:6px;text-decoration:none;">Confirmer mon inscription</a></p>
<p style="color:#6b665e;font-size:14px;">Si vous n'êtes pas à l'origine de cette demande, ignorez ce message : rien ne sera envoyé. Adrien Joly, London School of Economics.</p>`,
    already: "Vous êtes déjà inscrit ; vos préférences ont été mises à jour.",
    pending: "Regardez votre boîte de réception : un courriel de confirmation arrive.",
    bad: "Merci d'indiquer une adresse valide.",
  },
};
const freqLabel = {
  en: { daily: "each new study, in the morning", weekly: "one digest on Mondays", monthly: "one digest on the 1st of the month" },
  fr: { daily: "chaque nouvelle étude, le matin", weekly: "un résumé le lundi", monthly: "un résumé le 1er du mois" },
};

function esc(s) { return String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
function cors(env, extra = {}) {
  return { "Access-Control-Allow-Origin": env.ALLOWED_ORIGIN || "*", "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
           "Access-Control-Allow-Headers": "Content-Type, Authorization", "Content-Type": "application/json; charset=utf-8", ...extra };
}
function json(env, obj, status = 200) { return new Response(JSON.stringify(obj), { status, headers: cors(env) }); }
function token() { const b = new Uint8Array(24); crypto.getRandomValues(b); return [...b].map(x => x.toString(16).padStart(2, "0")).join(""); }
async function sha(s) { const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s)); return [...new Uint8Array(d)].slice(0, 8).map(x => x.toString(16).padStart(2, "0")).join(""); }
function authed(req, env) { return (req.headers.get("Authorization") || "") === `Bearer ${env.SEND_TOKEN}`; }

// --- provider: one HTTP call per batch of up to 100 messages ---------------------------------------
async function sendBatch(env, messages) {
  // messages: [{to, subject, html, text, headers}]
  if ((env.PROVIDER || "resend") === "postmark") {
    const r = await fetch("https://api.postmarkapp.com/email/batch", { method: "POST",
      headers: { "X-Postmark-Server-Token": env.POSTMARK_TOKEN, "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(messages.map(m => ({ From: env.MAIL_FROM, To: m.to, ReplyTo: env.REPLY_TO, Subject: m.subject, HtmlBody: m.html, TextBody: m.text,
        Headers: Object.entries(m.headers || {}).map(([Name, Value]) => ({ Name, Value })), MessageStream: "broadcast" }))) });
    return { ok: r.ok, body: await r.text() };
  }
  const payload = messages.map(m => ({ from: env.MAIL_FROM, to: [m.to], reply_to: env.REPLY_TO, subject: m.subject, html: m.html, text: m.text, headers: m.headers || {} }));
  const url = messages.length === 1 ? "https://api.resend.com/emails" : "https://api.resend.com/emails/batch";
  const r = await fetch(url, { method: "POST", headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify(messages.length === 1 ? payload[0] : payload) });
  return { ok: r.ok, body: await r.text() };
}

// --- handlers ---------------------------------------------------------------------------------------
async function subscribe(req, env) {
  let b = {};
  const ct = req.headers.get("Content-Type") || "";
  if (ct.includes("json") || ct.includes("text/plain")) b = await req.json().catch(() => ({}));
  else { const f = await req.formData().catch(() => null); if (f) for (const [k, v] of f.entries()) b[k] = v; }
  const lang = LANG.has(b.lang) ? b.lang : "en";
  if (b.hp) return json(env, { ok: true, message: T[lang].pending }); // honeypot filled: pretend
  const email = String(b.email || "").trim().toLowerCase();
  if (!EMAIL.test(email) || email.length > 254) return json(env, { ok: false, message: T[lang].bad }, 400);
  const name = String(b.name || "").trim().slice(0, 120);
  const frequency = FREQ.has(b.frequency) ? b.frequency : "weekly";
  const ipHash = await sha((req.headers.get("CF-Connecting-IP") || "") + (env.SEND_TOKEN || ""));
  const row = await env.DB.prepare("SELECT id, status, token FROM subscribers WHERE email = ?").bind(email).first();
  if (row && row.status === "confirmed") {
    await env.DB.prepare("UPDATE subscribers SET name = COALESCE(NULLIF(?, ''), name), frequency = ?, lang = ? WHERE id = ?").bind(name, frequency, lang, row.id).run();
    return json(env, { ok: true, message: T[lang].already });
  }
  const tok = row ? row.token : token();
  if (row) await env.DB.prepare("UPDATE subscribers SET name = COALESCE(NULLIF(?, ''), name), frequency = ?, lang = ?, status = 'pending', ip_hash = ? WHERE id = ?").bind(name, frequency, lang, ipHash, row.id).run();
  else await env.DB.prepare("INSERT INTO subscribers (email, name, frequency, lang, token, ip_hash) VALUES (?, ?, ?, ?, ?, ?)").bind(email, name, frequency, lang, tok, ipHash).run();
  const confirmUrl = `${new URL(req.url).origin}/api/confirm?t=${tok}`;
  const html = T[lang].confirmBody(name, confirmUrl, frequency);
  const text = html.replace(/<[^>]+>/g, "").replace(/\s+\n/g, "\n") + `\n${confirmUrl}`;
  const r = await sendBatch(env, [{ to: email, subject: T[lang].confirmSubject, html, text }]);
  if (!r.ok) return json(env, { ok: false, message: "Mail provider error", detail: r.body.slice(0, 200) }, 502);
  return json(env, { ok: true, message: T[lang].pending });
}

async function confirm(req, env) {
  const t = new URL(req.url).searchParams.get("t") || "";
  const row = t && await env.DB.prepare("SELECT id, lang FROM subscribers WHERE token = ?").bind(t).first();
  if (!row) return new Response("Unknown or expired link.", { status: 404 });
  await env.DB.prepare("UPDATE subscribers SET status = 'confirmed', confirmed_at = datetime('now') WHERE id = ?").bind(row.id).run();
  return Response.redirect(`${env.SITE_URL}/${row.lang === "fr" ? "fr/" : ""}subscribed/`, 302);
}

async function unsubscribe(req, env) {
  const t = new URL(req.url).searchParams.get("t") || "";
  const row = t && await env.DB.prepare("SELECT id, lang FROM subscribers WHERE token = ?").bind(t).first();
  if (!row) return new Response("Unknown link.", { status: 404 });
  await env.DB.prepare("UPDATE subscribers SET status = 'unsubscribed', unsubscribed_at = datetime('now') WHERE id = ?").bind(row.id).run();
  if (req.method === "POST") return new Response("Unsubscribed", { status: 200 }); // one-click (List-Unsubscribe-Post)
  return Response.redirect(`${env.SITE_URL}/${row.lang === "fr" ? "fr/" : ""}unsubscribed/`, 302);
}

async function send(req, env) {
  if (!authed(req, env)) return json(env, { ok: false, message: "Unauthorised" }, 401);
  const b = await req.json().catch(() => ({}));
  const tag = String(b.tag || "weekly");               // daily | weekly | monthly, optional -fr suffix
  const frequency = tag.replace(/-fr$/, ""); const lang = tag.endsWith("-fr") ? "fr" : "en";
  if (!FREQ.has(frequency) || !b.subject || !b.html) return json(env, { ok: false, message: "Need subject, html and a valid tag" }, 400);
  const { results } = await env.DB.prepare("SELECT email, name, token FROM subscribers WHERE status = 'confirmed' AND frequency = ? AND lang = ?").bind(frequency, lang).all();
  const origin = new URL(req.url).origin; let sent = 0; const ids = [];
  for (let i = 0; i < results.length; i += 100) {
    const batch = results.slice(i, i + 100).map(s => {
      const unsub = `${origin}/api/unsubscribe?t=${s.token}`;
      const fill = x => String(x).replaceAll("{{ unsubscribe_url }}", unsub).replaceAll("{{ name }}", s.name || "");
      return { to: s.email, subject: b.subject, html: fill(b.html), text: fill(b.text || ""),
               headers: { "List-Unsubscribe": `<${unsub}>`, "List-Unsubscribe-Post": "List-Unsubscribe=One-Click" } };
    });
    if (b.dry_run) { sent += batch.length; continue; }
    const r = await sendBatch(env, batch);
    if (!r.ok) return json(env, { ok: false, sent, message: "Mail provider error", detail: r.body.slice(0, 300) }, 502);
    sent += batch.length; ids.push(r.body.slice(0, 200));
  }
  if (!b.dry_run) await env.DB.prepare("INSERT INTO sends (tag, subject, recipients, provider_ids) VALUES (?, ?, ?, ?)").bind(tag, b.subject, sent, ids.join("|")).run();
  return json(env, { ok: true, tag, recipients: results.length, sent, dry_run: !!b.dry_run });
}

async function stats(req, env) {
  if (!authed(req, env)) return json(env, { ok: false }, 401);
  const { results } = await env.DB.prepare("SELECT status, frequency, lang, COUNT(*) AS n FROM subscribers GROUP BY status, frequency, lang").all();
  const last = await env.DB.prepare("SELECT tag, subject, recipients, sent_at FROM sends ORDER BY id DESC LIMIT 10").all();
  return json(env, { ok: true, subscribers: results, last_sends: last.results });
}

export default {
  async fetch(req, env) {
    const { pathname } = new URL(req.url);
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors(env) });
    try {
      if (pathname === "/api/subscribe" && req.method === "POST") return await subscribe(req, env);
      if (pathname === "/api/confirm" && req.method === "GET") return await confirm(req, env);
      if (pathname === "/api/unsubscribe") return await unsubscribe(req, env);
      if (pathname === "/api/send" && req.method === "POST") return await send(req, env);
      if (pathname === "/api/stats" && req.method === "GET") return await stats(req, env);
      if (pathname === "/" ) return new Response("living-review subscribe API", { status: 200 });
      return json(env, { ok: false, message: "Not found" }, 404);
    } catch (e) { return json(env, { ok: false, message: "Server error", detail: String(e).slice(0, 200) }, 500); }
  },
};
