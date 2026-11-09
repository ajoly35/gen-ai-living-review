#!/usr/bin/env python3
"""Build a clean email (HTML, plain text and Markdown) from Latest research entries.

Inputs
  --added FILE     markdown with the newly added entries (as cut out of _includes/latest.md by git diff)
  --latest N       or: take the N newest entries of _includes/latest.md (dry runs, digests)
  --lang en|fr     language of the entries and of the fixed strings (fr reads _includes/fr/)
  --kind daily|weekly|monthly   wording of the lead
  --audience general|academic   general = plain-language brief (what it explores, why it matters, how it fits the evidence, one chart);
                                academic = the full entries (default general)
  --out DIR        where to write <date>-<kind>-<lang>.{html,txt,md}
Nothing is sent here; see send_buttondown.py.
"""
import argparse, datetime as dt, html, os, re, sys

SITE = "https://ajoly35.github.io/gen-ai-living-review"
S = {
 "en": dict(brand="Gen-AI, Jobs and Growth", lead_daily="One new study on AI and work, checked against its full text.",
   lead_weekly="The studies added to the living review this week.", lead_monthly="The studies added to the living review this month.",
   finds="What it finds", fits="Why it matters", caveat="Caveat", main="Main ideas", paper="Read the paper",
   review="Read the full review", recent="Recent papers", submit="Send a paper", unsub="Unsubscribe",
   news="News item, reported as context", by="A living review maintained by Adrien Joly, London School of Economics.",
   disclaimer="Entries are written by an AI assistant from the paper itself and are not reviewed before they are sent. Figures are taken from the paper; the review's own assessment is in the caveat.",
   subject_daily="New study: ", subject_weekly="This week in AI and work: ", subject_monthly="This month in AI and work: ",
   brief_daily="Today's new research on AI and work, in plain words.", brief_weekly="This week's new research on AI and work, in plain words.", brief_monthly="This month's new research on AI and work, in plain words.",
   explores="What it explores", matters="Why it matters", fits_ev="How it fits the evidence", chart="Where the evidence stands",
   chart_caption="Studies on jobs, hiring or pay, by research design. Orange: fewer jobs, hires or lower pay. Grey: no measurable effect. Blue: gains. Experiments measure output per worker and find gains; studies of who gets hired find falls; studies of total employment find nothing yet.",
   full="Full entry", general_subject="AI and work, in brief: ", fr_path=""),
 "fr": dict(brand="IA générative, emploi et croissance", lead_daily="Une nouvelle étude sur l'IA et le travail, vérifiée sur son texte intégral.",
   lead_weekly="Les études ajoutées à la revue vivante cette semaine.", lead_monthly="Les études ajoutées à la revue vivante ce mois-ci.",
   finds="Ce que l'étude trouve", fits="Pourquoi c'est important", caveat="Limite", main="Idées principales", paper="Lire l'article",
   review="Lire la revue complète", recent="Articles récents", submit="Proposer un article", unsub="Se désabonner",
   news="Article de presse, donné pour le contexte", by="Une revue vivante tenue par Adrien Joly, London School of Economics.",
   disclaimer="Les entrées sont rédigées par un assistant IA à partir de l'article lui-même et ne sont pas relues avant envoi. Les chiffres viennent de l'article ; l'appréciation de la revue est dans la limite.",
   subject_daily="Nouvelle étude : ", subject_weekly="Cette semaine, IA et travail : ", subject_monthly="Ce mois-ci, IA et travail : ",
   brief_daily="La nouvelle recherche du jour sur l'IA et le travail, en mots simples.", brief_weekly="La recherche de la semaine sur l'IA et le travail, en mots simples.", brief_monthly="La recherche du mois sur l'IA et le travail, en mots simples.",
   explores="Ce qu'elle explore", matters="Pourquoi c'est important", fits_ev="Ce que cela change aux preuves", chart="Où en sont les preuves",
   chart_caption="Études sur l'emploi, les embauches ou les salaires, par dispositif. Orange : moins d'emplois, d'embauches ou de salaire. Gris : pas d'effet mesurable. Bleu : gains. Les expériences mesurent la production par travailleur et trouvent des gains ; les études sur qui est embauché trouvent des baisses ; celles sur l'emploi total ne trouvent rien encore.",
   full="Entrée complète", general_subject="IA et travail, en bref : ", fr_path="fr/"),
}
LABELS = {"en": ("What it finds.", "Where it fits.", "Caveat."), "fr": ("Ce que l'étude trouve.", "Où cela se place.", "Limite.")}

def md_inline(s, lang):
    """Minimal Markdown to HTML for one paragraph: links, bold, italics, maths, entities."""
    s = re.sub(r"\$\$(.*?)\$\$", r"\1", s)
    s = s.replace("&#36;", "$")
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\(#([a-z0-9\-]+)\)", lambda m: f'<a href="{SITE}/{S[lang]["fr_path"]}#{m.group(2)}">{m.group(1)}</a>', s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r"<em>\1</em>", s)
    return s

def md_plain(s):
    s = re.sub(r"\$\$(.*?)\$\$", r"\1", s).replace("&#36;", "$")
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", s)
    return s.replace("**", "").replace("*", "")

def parse_entries(text, lang):
    out = []
    for chunk in re.split(r"^### ", text, flags=re.M)[1:]:
        lines = chunk.strip().split("\n")
        heading = lines[0].strip()
        hid = re.sub(r"\s*\{#([^}]+)\}\s*$", "", heading)
        m = re.search(r"\{#([^}]+)\}\s*$", heading)
        anchor = m.group(1) if m else kramdown_id(hid)
        paras = [p.strip() for p in re.split(r"\n\s*\n", "\n".join(lines[1:])) if p.strip() and not p.strip().startswith("<!--")]
        kind = "paper"
        if "kind: news" in chunk[:900] or any(k in (paras[0] if paras else "") for k in ("News report", "News analysis", "Article de presse", "Analyse journalistique", "Reportage")):
            kind = "news"
        e = dict(title=hid, anchor=anchor, kind=kind, provenance=paras[0] if paras else "", finds="", fits="", caveat="", other=[], brief={})
        f, w, c = LABELS[lang]
        bl = "**In brief.**" if lang == "en" else "**En bref.**"
        for p in paras[1:]:
            if p.startswith("**" + f + "**"): e["finds"] = p[len(f) + 4:].strip()
            elif p.startswith("**" + w + "**"): e["fits"] = p[len(w) + 4:].strip()
            elif p.startswith("**" + c + "**"): e["caveat"] = p[len(c) + 4:].strip()
            elif p.startswith(bl):
                for line in p[len(bl):].strip().split("\n"):
                    m = re.match(r"\s*[-*]?\s*\*?\*?([^:*]+?)\*?\*?\s*:\s*(.+)$", line)
                    if m: e["brief"][m.group(1).strip().lower()] = m.group(2).strip()
            else: e["other"].append(p)
        m = re.search(r"\[(?:Paper|Report|Article|Rapport)\]\((https?://[^)\s]+)\)", e["provenance"])
        e["url"] = m.group(1) if m else None
        out.append(e)
    return out

def kramdown_id(h):
    h = re.sub(r"[^\w\s-]", "", h.lower().replace("’", "").replace("'", ""))
    h = re.sub(r"\s+", "-", h.strip())
    return h

def main_ideas(path):
    if not os.path.exists(path): return []
    items = [l[2:].strip() for l in open(path, encoding="utf-8") if l.startswith("- ")]
    return items

def first_sentence(x):
    m = re.match(r"(.+?[.!?])(\s|$)", x or "")
    return (m.group(1) if m else (x or "")).strip()

def brief_lines(e, lang):
    """The three plain-language lines: from the routine's In brief block when present, else from the entry itself."""
    b = e.get("brief") or {}
    keys = {"en": (("what it explores", "explores"), ("why it matters", "matters"), ("how it fits the evidence", "how it fits", "fits")),
            "fr": (("ce qu'elle explore", "explore"), ("pourquoi c'est important", "important"), ("ce que cela change aux preuves", "preuves"))}[lang]
    def pick(names):
        for k, v in b.items():
            if any(n in k for n in names): return v
        return None
    explores = pick(keys[0]) or first_sentence(e["finds"])
    matters = pick(keys[1]) or first_sentence(e["fits"])
    rest = e["fits"][len(first_sentence(e["fits"])):].strip() if e["fits"] else ""
    fits = pick(keys[2]) or rest or first_sentence(e["caveat"])
    return explores, matters, fits

def build(entries, lang, kind, ideas, date, audience="academic"):
    t = S[lang]
    lead = t["lead_" + kind] if audience == "academic" else t["brief_" + kind]
    first = entries[0]["title"] if entries else ""
    subject = (t["subject_" + kind] if audience == "academic" else t["general_subject"]) + re.sub(r'^(.*?\(\d{4}\)),?\s*"?(.*?)"?$', r"\2", first)[:110]
    if audience == "general": return build_general(entries, lang, kind, ideas, date, lead, subject)
    # --- HTML (inline styles, no tables) ---
    H = []
    H.append(f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(subject)}</title></head>')
    H.append('<body style="margin:0;background:#fbfaf7;color:#1f1d1a;font:17px/1.6 Georgia,\'Times New Roman\',serif;">')
    H.append('<div style="max-width:600px;margin:0 auto;padding:28px 20px 40px;">')
    H.append(f'<p style="margin:0 0 4px;font:600 13px/1.4 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;letter-spacing:.04em;text-transform:uppercase;color:#7a2e1f;">{t["brand"]}</p>')
    H.append(f'<p style="margin:0 0 22px;font:13px/1.4 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#6b665e;">{date.strftime("%-d %B %Y") if lang=="en" else fr_date(date)} · {html.escape(lead)}</p>')
    for e in entries:
        H.append('<div style="border-left:3px solid #7a2e1f;background:#f3f0ea;border-radius:0 6px 6px 0;padding:14px 18px 6px;margin:0 0 22px;">')
        title = md_inline(e["title"], lang)
        if e["url"]: title = f'<a href="{e["url"]}" style="color:#1f1d1a;text-decoration:none;">{title}</a>'
        H.append(f'<h2 style="margin:0 0 8px;font:600 19px/1.3 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;">{title}</h2>')
        prov = md_inline(e["provenance"], lang)
        if e["kind"] == "news": prov = f'<em>{t["news"]}.</em> ' + prov
        H.append(f'<p style="margin:0 0 12px;font-size:14px;color:#6b665e;">{prov}</p>')
        if e["finds"]: H.append(f'<p style="margin:0 0 12px;"><strong style="font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;font-size:14px;">{t["finds"]}.</strong> {md_inline(e["finds"], lang)}</p>')
        if e["fits"]: H.append(f'<p style="margin:0 0 12px;"><strong style="font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;font-size:14px;">{t["fits"]}.</strong> {md_inline(e["fits"], lang)}</p>')
        for p in e["other"]: H.append(f'<p style="margin:0 0 12px;">{md_inline(p, lang)}</p>')
        if e["caveat"]: H.append(f'<p style="margin:0 0 12px;font-size:14px;color:#6b665e;"><strong>{t["caveat"]}.</strong> {md_inline(e["caveat"], lang)}</p>')
        links = [f'<a href="{e["url"]}" style="color:#7a2e1f;">{t["paper"]}</a>'] if e["url"] else []
        links.append(f'<a href="{SITE}/{t["fr_path"]}latest/#{e["anchor"]}" style="color:#7a2e1f;">{t["recent"]}</a>')
        H.append(f'<p style="margin:0 0 10px;font:14px -apple-system,Segoe UI,Helvetica,Arial,sans-serif;">{" · ".join(links)}</p></div>')
    if ideas:
        H.append('<div style="background:#f3f0ea;border-radius:6px;padding:12px 18px 8px;margin:6px 0 22px;">')
        H.append(f'<p style="margin:0 0 6px;font:600 12px/1.4 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;letter-spacing:.04em;text-transform:uppercase;color:#6b665e;">{t["main"]}</p><ul style="margin:0;padding-left:18px;font-size:15px;">')
        for it in ideas:
            it = re.sub(r"^\*(.+?)\*", r"<strong>\1</strong>", html.escape(it, quote=False))
            H.append(f'<li style="margin:5px 0;">{it}</li>')
        H.append('</ul></div>')
    H.append(f'<p style="font:14px/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#6b665e;margin:0 0 8px;"><a href="{SITE}/{t["fr_path"]}" style="color:#7a2e1f;">{t["review"]}</a> · <a href="https://github.com/ajoly35/gen-ai-living-review/issues/new?template=paper.yml" style="color:#7a2e1f;">{t["submit"]}</a> · <a href="{{{{ unsubscribe_url }}}}" style="color:#7a2e1f;">{t["unsub"]}</a></p>')
    H.append(f'<p style="font:12px/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#6b665e;margin:0;">{t["by"]} {t["disclaimer"]}</p>')
    H.append('</div></body></html>')
    # --- plain text ---
    T = [t["brand"].upper(), lead, ""]
    for e in entries:
        T += [md_plain(e["title"]), md_plain(e["provenance"]), ""]
        if e["finds"]: T += [f'{t["finds"]}. ' + md_plain(e["finds"]), ""]
        if e["fits"]: T += [f'{t["fits"]}. ' + md_plain(e["fits"]), ""]
        if e["caveat"]: T += [f'{t["caveat"]}. ' + md_plain(e["caveat"]), ""]
        if e["url"]: T += [e["url"]]
        T += [f'{SITE}/{t["fr_path"]}latest/#{e["anchor"]}', "", "—" * 30, ""]
    if ideas: T += [t["main"].upper()] + ["- " + md_plain(i) for i in ideas] + [""]
    T += [f'{t["review"]}: {SITE}/{t["fr_path"]}', f'{t["unsub"]}: {{{{ unsubscribe_url }}}}', "", t["by"], t["disclaimer"]]
    # --- markdown (Substack paste) ---
    M = [f"# {subject}", "", f"*{lead}*", ""]
    for e in entries:
        M += [f"## {e['title']}", "", e["provenance"], ""]
        if e["finds"]: M += [f"**{t['finds']}.** {e['finds']}", ""]
        if e["fits"]: M += [f"**{t['fits']}.** {e['fits']}", ""]
        if e["caveat"]: M += [f"*{t['caveat']}.* {e['caveat']}", ""]
    if ideas: M += [f"### {t['main']}", ""] + ["- " + i for i in ideas] + [""]
    M += [f"[{t['review']}]({SITE}/{t['fr_path']}) · [{t['submit']}](https://github.com/ajoly35/gen-ai-living-review/issues/new?template=paper.yml)", "", f"*{t['by']} {t['disclaimer']}*"]
    return subject, "\n".join(H), "\n".join(T), "\n".join(M)

def build_general(entries, lang, kind, ideas, date, lead, subject):
    """General-audience brief: per study, three plain lines; one standing chart; main ideas; links to the full entries."""
    t = S[lang]; site = f"{SITE}/{t['fr_path']}"
    H = [f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(subject)}</title></head>',
         '<body style="margin:0;background:#fbfaf7;color:#1f1d1a;font:17px/1.6 Georgia,\'Times New Roman\',serif;"><div style="max-width:600px;margin:0 auto;padding:28px 20px 40px;">',
         f'<p style="margin:0 0 4px;font:600 13px/1.4 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;letter-spacing:.04em;text-transform:uppercase;color:#7a2e1f;">{t["brand"]}</p>',
         f'<p style="margin:0 0 22px;font:13px/1.4 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#6b665e;">{date.strftime("%-d %B %Y") if lang=="en" else fr_date(date)} · {html.escape(lead)}</p>']
    T = [t["brand"].upper(), lead, ""]; M = [f"# {subject}", "", f"*{lead}*", ""]
    for e in entries:
        explores, matters, fits = brief_lines(e, lang)
        title = md_inline(e["title"], lang)
        if e["url"]: title = f'<a href="{e["url"]}" style="color:#1f1d1a;text-decoration:none;">{title}</a>'
        H.append('<div style="border-left:3px solid #7a2e1f;background:#f3f0ea;border-radius:0 6px 6px 0;padding:14px 18px 8px;margin:0 0 22px;">')
        H.append(f'<h2 style="margin:0 0 10px;font:600 19px/1.3 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;">{title}</h2>')
        if e["kind"] == "news": H.append(f'<p style="margin:0 0 10px;font-size:14px;color:#6b665e;"><em>{t["news"]}.</em></p>')
        for lab, txt in ((t["explores"], explores), (t["matters"], matters), (t["fits_ev"], fits)):
            if txt: H.append(f'<p style="margin:0 0 10px;"><strong style="font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;font-size:13px;letter-spacing:.03em;text-transform:uppercase;color:#6b665e;display:block;">{lab}</strong>{md_inline(txt, lang)}</p>')
        links = ([f'<a href="{e["url"]}" style="color:#7a2e1f;">{t["paper"]}</a>'] if e["url"] else []) + [f'<a href="{site}latest/#{e["anchor"]}" style="color:#7a2e1f;">{t["full"]}</a>']
        H.append(f'<p style="margin:4px 0 8px;font:14px -apple-system,Segoe UI,Helvetica,Arial,sans-serif;">{" · ".join(links)}</p></div>')
        T += [md_plain(e["title"]), ""] + [f"{lab}: {md_plain(txt)}" for lab, txt in ((t["explores"], explores), (t["matters"], matters), (t["fits_ev"], fits)) if txt] + [(e["url"] or ""), f"{site}latest/#{e['anchor']}", "", "—" * 30, ""]
        M += [f"## {e['title']}", ""] + [f"**{lab}.** {txt}" for lab, txt in ((t["explores"], explores), (t["matters"], matters), (t["fits_ev"], fits)) if txt] + ["", f"[{t['full']}]({site}latest/#{e['anchor']})" + (f" · [{t['paper']}]({e['url']})" if e["url"] else ""), ""]
    chart = f"{SITE}/assets/vitals/direction-by-design-{lang}.png"
    H.append(f'<p style="margin:0 0 6px;font:600 12px/1.4 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;letter-spacing:.04em;text-transform:uppercase;color:#6b665e;">{t["chart"]}</p>')
    H.append(f'<a href="{site}vitals/"><img src="{chart}" alt="{html.escape(t["chart_caption"])}" style="width:100%;height:auto;border:1px solid #e4e0d8;border-radius:6px;background:#fff;"></a>')
    H.append(f'<p style="margin:6px 0 22px;font:13px/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#6b665e;">{html.escape(t["chart_caption"])}</p>')
    T += [t["chart"].upper(), t["chart_caption"], chart, ""]; M += [f"### {t['chart']}", "", f"![{t['chart_caption']}]({chart})", "", t["chart_caption"], ""]
    if ideas:
        H.append('<div style="background:#f3f0ea;border-radius:6px;padding:12px 18px 8px;margin:6px 0 22px;">')
        H.append(f'<p style="margin:0 0 6px;font:600 12px/1.4 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;letter-spacing:.04em;text-transform:uppercase;color:#6b665e;">{t["main"]}</p><ul style="margin:0;padding-left:18px;font-size:15px;">')
        for it in ideas:
            li = re.sub(r"^\*(.+?)\*", r"<strong>\1</strong>", html.escape(it, quote=False))
            H.append(f'<li style="margin:5px 0;">{li}</li>')
        H.append('</ul></div>'); T += [t["main"].upper()] + ["- " + md_plain(i) for i in ideas] + [""]; M += [f"### {t['main']}", ""] + ["- " + i for i in ideas] + [""]
    H.append(f'<p style="font:14px/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#6b665e;margin:0 0 8px;"><a href="{site}" style="color:#7a2e1f;">{t["review"]}</a> · <a href="https://github.com/ajoly35/gen-ai-living-review/issues/new?template=paper.yml" style="color:#7a2e1f;">{t["submit"]}</a> · <a href="{{{{ unsubscribe_url }}}}" style="color:#7a2e1f;">{t["unsub"]}</a></p>')
    H.append(f'<p style="font:12px/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#6b665e;margin:0;">{t["by"]} {t["disclaimer"]}</p></div></body></html>')
    T += [f'{t["review"]}: {site}', f'{t["unsub"]}: {{{{ unsubscribe_url }}}}', "", t["by"], t["disclaimer"]]
    M += [f"[{t['review']}]({site}) · [{t['submit']}](https://github.com/ajoly35/gen-ai-living-review/issues/new?template=paper.yml)", "", f"*{t['by']} {t['disclaimer']}*"]
    return subject, "\n".join(H), "\n".join(T), "\n".join(M)

FR_MONTHS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
def fr_date(d): return f"{d.day} {FR_MONTHS[d.month-1]} {d.year}"

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--added"); ap.add_argument("--latest", type=int)
    ap.add_argument("--lang", default="en", choices=["en", "fr"]); ap.add_argument("--kind", default="daily", choices=["daily", "weekly", "monthly"])
    ap.add_argument("--out", default="emails"); ap.add_argument("--date", default=None)
    ap.add_argument("--audience", default="general", choices=["general", "academic"])
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args()
    date = dt.date.fromisoformat(a.date) if a.date else dt.date.today()
    src = os.path.join(a.root, "_includes", S[a.lang]["fr_path"], "latest.md")
    if a.added: text = open(a.added, encoding="utf-8").read()
    else: text = open(src, encoding="utf-8").read()
    entries = parse_entries(text, a.lang)
    if a.latest: entries = entries[: a.latest]
    if a.added and a.lang == "fr":
        # map added English headings to their French entries by anchor
        en = {e["anchor"]: e for e in parse_entries(open(a.added, encoding="utf-8").read(), "en")}
        fr = parse_entries(open(src, encoding="utf-8").read(), "fr")
        entries = [e for e in fr if e["anchor"] in en] or entries
    if not entries: print("no entries", file=sys.stderr); sys.exit(3)
    ideas = main_ideas(os.path.join(a.root, "_includes", S[a.lang]["fr_path"], "main-ideas.md"))
    subject, H, T, M = build(entries, a.lang, a.kind, ideas, date, a.audience)
    os.makedirs(a.out, exist_ok=True)
    base = os.path.join(a.out, f"{date.isoformat()}-{a.kind}{'-academic' if a.audience == 'academic' else ''}-{a.lang}")
    open(base + ".html", "w", encoding="utf-8").write(H); open(base + ".txt", "w", encoding="utf-8").write(T); open(base + ".paste.txt", "w", encoding="utf-8").write(M)
    open(base + ".subject", "w", encoding="utf-8").write(subject)
    print(base, "|", subject, "|", len(entries), "entries")
