/**
 * Self-hosted subscriptions for the living review, Google version: Apps Script web app + Google Sheet + Gmail.
 * Same design as econvitals.org/subscribe (own confirmed opt-in form, own list, own sender) with Google as the server.
 * Endpoints (one URL, the web app's /exec, with ?action=):
 *   POST ?action=subscribe   body JSON {name, email, frequency, lang, audience, hp}  -> confirmation email (link to SITE_URL/subscribed/?t=)
 *   GET  ?action=confirm&t=TOKEN[&json=1]   -> status confirmed; json=1 answers JSON (used by the site page), else redirects
 *   GET  ?action=unsubscribe&t=TOKEN  -> status unsubscribed, redirect to /unsubscribed/   (POST also accepted)
 *   POST ?action=send        body JSON {token, subject, html, text, tag, dry_run}  -> tag = daily|weekly|monthly[-academic][-fr]
 *   GET  ?action=stats&token=...      -> counts and remaining Gmail quota
 * Script properties (Project settings > Script properties): SITE_URL, SEND_TOKEN, SENDER_NAME, REPLY_TO, and on Workspace
 * optionally FROM_ALIAS (a "Send mail as" address such as briefings@your-domain.tld; needs the Gmail scope on first run).
 * Deploy: Deploy > New deployment > Web app, "Execute as: Me", "Who has access: Anyone". Copy the /exec URL.
 */
var FREQ = ["daily", "weekly", "monthly"], LANG = ["en", "fr"];
var HEAD = ["email", "name", "frequency", "lang", "status", "token", "created_at", "confirmed_at", "unsubscribed_at", "audience"];
var AUD = ["general", "academic"];
var P = PropertiesService.getScriptProperties();
// Settings: Script properties first, then the CONFIG object of Config.gs (pushed by clasp). setup() copies CONFIG into the properties.
function cfg(k) { var v = P.getProperty(k); if (v) return v; return (typeof CONFIG !== "undefined" && CONFIG[k]) ? CONFIG[k] : null; }
function setup() {
  if (typeof CONFIG !== "undefined") Object.keys(CONFIG).forEach(function (k) { P.setProperty(k, CONFIG[k]); });
  sheet("subscribers"); sheet("sends");                      // create the two tabs
  Logger.log("Properties set: " + Object.keys(P.getProperties()).join(", ") + ". Mail quota left today: " + MailApp.getRemainingDailyQuota());
}

var T = {
  en: { subject: "Confirm your subscription: Gen-AI, Jobs and Growth", already: "You are already subscribed; your preferences were updated.",
        pending: "Check your inbox: a confirmation email is on its way.", bad: "Please enter a valid email address.",
        body: function (name, url, f) { return "<p>Hello" + (name ? " " + esc(name) : "") + ",</p><p>One click to confirm that you want the living review's emails (" + FL.en[f] + "):</p>" +
          "<p><a href=\"" + url + "\" style=\"display:inline-block;padding:10px 16px;background:#7a2e1f;color:#fff;border-radius:6px;text-decoration:none;\">Confirm my subscription</a></p>" +
          "<p style=\"color:#6b665e;font-size:14px;\">If you did not ask for this, ignore this message and nothing will be sent. To keep the emails out of spam, add this sender to your contacts. Adrien Joly, London School of Economics.</p>"; } },
  fr: { subject: "Confirmez votre inscription : IA générative, emploi et croissance", already: "Vous êtes déjà inscrit ; vos préférences ont été mises à jour.",
        pending: "Regardez votre boîte de réception : un courriel de confirmation arrive.", bad: "Merci d'indiquer une adresse valide.",
        body: function (name, url, f) { return "<p>Bonjour" + (name ? " " + esc(name) : "") + ",</p><p>Un clic pour confirmer que vous souhaitez recevoir les courriels de la revue vivante (" + FL.fr[f] + ") :</p>" +
          "<p><a href=\"" + url + "\" style=\"display:inline-block;padding:10px 16px;background:#7a2e1f;color:#fff;border-radius:6px;text-decoration:none;\">Confirmer mon inscription</a></p>" +
          "<p style=\"color:#6b665e;font-size:14px;\">Si vous n'êtes pas à l'origine de cette demande, ignorez ce message : rien ne sera envoyé. Pour éviter le dossier spam, ajoutez cet expéditeur à vos contacts. Adrien Joly, London School of Economics.</p>"; } }
};
var FL = { en: { daily: "each new study, in the morning", weekly: "one digest on Mondays", monthly: "one digest on the 1st of the month" },
           fr: { daily: "chaque nouvelle étude, le matin", weekly: "un résumé le lundi", monthly: "un résumé le 1er du mois" } };

function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
function out(obj) { return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON); }
function redirect(url) { return HtmlService.createHtmlOutput('<meta http-equiv="refresh" content="0;url=' + esc(url) + '"><p><a href="' + esc(url) + '">Continue</a></p>'); }
function token() { var s = ""; for (var i = 0; i < 48; i++) s += Math.floor(Math.random() * 16).toString(16); return s; }
function now() { return new Date().toISOString(); }
function selfUrl() { return cfg("EXEC_URL") || ScriptApp.getService().getUrl(); }   // EXEC_URL pinned in Config.gs: getUrl() is not reliable across deployments

function mail_(to, subject, html, text) {
  var opts = { htmlBody: html, name: cfg("SENDER_NAME") || "AI Economics Brief", replyTo: cfg("REPLY_TO") || "" };
  var alias = cfg("FROM_ALIAS");               // e.g. briefings@your-domain.tld, configured in Gmail > Settings > Accounts > Send mail as
  if (alias) { opts.from = alias; GmailApp.sendEmail(to, subject, text, opts); } else MailApp.sendEmail(Object.assign({ to: to, subject: subject, body: text }, opts));
}
function quota_() { return MailApp.getRemainingDailyQuota(); }

function sheet(name) {
  var ss = SpreadsheetApp.getActiveSpreadsheet(); var sh = ss.getSheetByName(name);
  if (!sh) { sh = ss.insertSheet(name); sh.appendRow(name === "subscribers" ? HEAD : ["sent_at", "tag", "subject", "recipients", "sent", "note"]); }
  return sh;
}
function rows() { var sh = sheet("subscribers"); var v = sh.getDataRange().getValues(); var o = [];
  for (var i = 1; i < v.length; i++) { var r = {}; HEAD.forEach(function (h, j) { r[h] = v[i][j]; }); r._row = i + 1; o.push(r); } return o; }
function setCell(row, col, val) { sheet("subscribers").getRange(row, HEAD.indexOf(col) + 1).setValue(val); }

function doGet(e) { var a = (e.parameter.action || ""); 
  if (a === "confirm") return confirm_(e.parameter.t, e.parameter.json === "1");
  if (a === "unsubscribe") return unsubscribe_(e.parameter.t, false, e.parameter.json === "1");
  if (a === "stats") return stats_(e.parameter.token);
  return ContentService.createTextOutput("living-review subscribe API (Apps Script)"); }
function doPost(e) { var a = (e.parameter.action || ""); var b = {};
  try { b = JSON.parse(e.postData && e.postData.contents || "{}"); } catch (err) { b = e.parameter || {}; }
  if (a === "subscribe") return subscribe_(b);
  if (a === "send") return send_(b);
  if (a === "unsubscribe") return unsubscribe_(e.parameter.t || b.t, true, false);
  return out({ ok: false, message: "Not found" }); }

function subscribe_(b) {
  var lang = LANG.indexOf(b.lang) >= 0 ? b.lang : "en"; var t = T[lang];
  if (b.hp) return out({ ok: true, message: t.pending });                       // honeypot: pretend
  var email = String(b.email || "").trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.length > 254) return out({ ok: false, message: t.bad });
  var name = String(b.name || "").trim().slice(0, 120), freq = FREQ.indexOf(b.frequency) >= 0 ? b.frequency : "weekly", aud = AUD.indexOf(b.audience) >= 0 ? b.audience : "general";
  var lock = LockService.getScriptLock(); lock.waitLock(10000);
  try {
    var all = rows(), r = null; for (var i = 0; i < all.length; i++) if (all[i].email === email) r = all[i];
    if (r && r.status === "confirmed") { if (name) setCell(r._row, "name", name); setCell(r._row, "frequency", freq); setCell(r._row, "lang", lang); setCell(r._row, "audience", aud); return out({ ok: true, message: t.already }); }
    var tok = r ? r.token : token();
    if (r) { if (name) setCell(r._row, "name", name); setCell(r._row, "frequency", freq); setCell(r._row, "lang", lang); setCell(r._row, "audience", aud); setCell(r._row, "status", "pending"); }
    else sheet("subscribers").appendRow([email, name, freq, lang, "pending", tok, now(), "", "", aud]);
  } finally { lock.releaseLock(); }
  var url = siteUrl_(lang) + "subscribed/?t=" + tok, html = t.body(name, url, freq);
  mail_(email, t.subject, html, html.replace(/<[^>]+>/g, " ") + "\n" + url);
  return out({ ok: true, message: t.pending });
}
function siteUrl_(lang) { return cfg("SITE_URL") + "/" + (lang === "fr" ? "fr/" : ""); }
function find_(tok) { var all = rows(); for (var i = 0; i < all.length; i++) if (tok && all[i].token === tok) return all[i]; return null; }
function confirm_(tok, asJson) { var r = find_(tok); if (!r) return asJson ? out({ ok: false, message: "unknown" }) : ContentService.createTextOutput("Unknown or expired link.");
  if (r.status !== "confirmed") { setCell(r._row, "status", "confirmed"); setCell(r._row, "confirmed_at", now()); }
  return asJson ? out({ ok: true, status: "confirmed", lang: r.lang, frequency: r.frequency, audience: r.audience || "general" }) : redirect(siteUrl_(r.lang) + "subscribed/"); }
function unsubscribe_(tok, isPost, asJson) { var r = find_(tok); if (!r) return asJson ? out({ ok: false, message: "unknown" }) : ContentService.createTextOutput("Unknown link.");
  setCell(r._row, "status", "unsubscribed"); setCell(r._row, "unsubscribed_at", now());
  if (asJson) return out({ ok: true, status: "unsubscribed", lang: r.lang });
  if (isPost) return ContentService.createTextOutput("Unsubscribed");
  return redirect(siteUrl_(r.lang) + "unsubscribed/"); }

function send_(b) {
  if (!b.token || b.token !== cfg("SEND_TOKEN")) return out({ ok: false, message: "Unauthorised" });
  var tag = String(b.tag || "weekly"), lang = /-fr$/.test(tag) ? "fr" : "en", rest = tag.replace(/-fr$/, "");
  var aud = /-academic$/.test(rest) ? "academic" : "general", freq = rest.replace(/-academic$/, "");
  if (FREQ.indexOf(freq) < 0 || !b.subject || !b.html) return out({ ok: false, message: "Need subject, html and a valid tag (freq[-academic][-fr])" });
  var list = rows().filter(function (r) { return r.status === "confirmed" && r.frequency === freq && r.lang === lang && ((r.audience || "general") === aud); });
  var quota = quota_(), sent = 0, skipped = 0, base = selfUrl();
  for (var i = 0; i < list.length; i++) {
    if (b.dry_run) { sent++; continue; }
    if (quota - sent <= 0) { skipped++; continue; }                                   // Gmail: 100/day free, 1,500/day Workspace
    var unsub = siteUrl_(lang) + "unsubscribed/?t=" + list[i].token;
    var fill = function (x) { return String(x).split("{{ unsubscribe_url }}").join(unsub).split("{{ name }}").join(list[i].name || ""); };
    mail_(list[i].email, b.subject, fill(b.html), fill(b.text || " "));
    sent++;
  }
  if (!b.dry_run) sheet("sends").appendRow([now(), tag, b.subject, list.length, sent, skipped ? skipped + " skipped: daily Gmail quota reached" : ""]);
  return out({ ok: true, tag: tag, audience: aud, recipients: list.length, sent: sent, skipped: skipped, quota_left: quota - (b.dry_run ? 0 : sent), dry_run: !!b.dry_run });
}
function stats_(tok) { if (!tok || tok !== cfg("SEND_TOKEN")) return out({ ok: false });
  var c = {}; rows().forEach(function (r) { var k = r.status + "/" + r.frequency + "/" + (r.audience || "general") + "/" + r.lang; c[k] = (c[k] || 0) + 1; });
  return out({ ok: true, subscribers: c, quota_left_today: quota_() }); }
