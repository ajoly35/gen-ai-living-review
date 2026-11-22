#!/usr/bin/env python3
"""Read the public figures behind the policy brief's "The numbers" block and write them to the site.

Sources (all public, no key):
  France          INSEE BDM, ILO unemployment rate, quarterly, seasonally adjusted, France excluding Mayotte
                  (series 001688527 all ages, 001688537 under 25)
  United Kingdom  ONS Labour Force Survey, three-month rolling rate, seasonally adjusted
                  (MGSX aged 16 and over, MGWY aged 16 to 24)
  United States   BLS Current Population Survey, monthly, seasonally adjusted
                  (LNS14000000 aged 16 and over, LNS14024887 aged 16 to 24)
  AI at work, US  GenAI Adoption Tracker (Bick, Blandin and Deming; Real-Time Population Survey)
  AI hiring, FR   LIFT (HEC Paris) AI job postings tracker, built on the Dares JOCAS database

Writes
  _data/employment.json                    the figures (Jekyll: site.data.employment)
  _includes/employment-table-en.md, -fr.md the block as Markdown, included by the policy pages and
                                           inlined into the policy email by scripts/build_email.py
A source that cannot be read, or whose layout has changed, keeps its previous figures: nothing is ever
estimated or filled in. Exit code 0 unless no figures exist at all.

Usage: fetch_trackers.py [--root SITE_DIR] [--offline]   (--offline: only rebuild the Markdown from the JSON)
"""
import argparse, csv, datetime as dt, http.client, io, json, os, re, sys, time, urllib.request

UA = {"User-Agent": "employment-trackers/1.0"}
INSEE = "https://bdm.insee.fr/series/sdmx/data/SERIES_BDM/{}?lastNObservations=6"
ONS = "https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/timeseries/{}/lms/data"
BLS = "https://api.bls.gov/publicAPI/v1/timeseries/data/{}"
ADOPT = "https://www.genaiadoptiontracker.com/"
LIFT = "https://heclift.github.io/website/data/ai-trackers/diffusion-emploi/offers_total.csv"   # monthly series
# Not general_results.csv: its headline counts (104,935 AI postings; 652 and 111 "last quarter") do not match LIFT's
# own monthly series (checked 22/11/2026), so the block is built from the series and says where it ends.

PAGES = {
    "fr": "https://www.insee.fr/fr/statistiques/serie/001688527",
    "uk": "https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment",
    "us": "https://www.bls.gov/cps/",
    "adoption": ADOPT,
    "lift": "https://heclift.github.io/website/en/ai-trackers/diffusion-emploi/index.html",
}
EN_M = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
FR_M = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
ONS_M = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


def get(url):
    for attempt in range(4):                                    # the ONS files are large and sometimes cut short
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return r.read().decode("utf-8-sig")
        except (OSError, http.client.HTTPException):
            if attempt == 3:
                raise
            time.sleep(3 * (attempt + 1))


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


# ---- France: INSEE, quarterly ----
def insee(idbank):
    obs = dict(re.findall(r'TIME_PERIOD="(\d{4}-Q\d)" OBS_VALUE="([^"]*)"', get(INSEE.format(idbank))))
    last = max(obs)
    y, q = int(last[:4]), last[-1]
    return last, fnum(obs[last]), fnum(obs.get(f"{y - 1}-Q{q}"))


def france():
    p, v, v0 = insee("001688527")
    p2, y, y0 = insee("001688537")
    if p != p2 or v is None or y is None:
        raise ValueError("INSEE: the two series do not share a latest quarter")
    q = int(p[-1])
    return dict(key="fr", period=p, period_en=f"Q{q} {p[:4]}", period_fr=f"T{q} {p[:4]}",
                all=v, all_prev=v0, youth=y, youth_prev=y0)


# ---- United Kingdom: ONS, three-month rolling, labelled by the middle month ----
def ons(code):
    months = json.loads(get(ONS.format(code)))["months"]
    by = {m["date"]: fnum(m["value"]) for m in months}
    last = months[-1]["date"]                                   # e.g. "2026 AUG" = July to September 2026
    y, mon = last.split()
    return last, by[last], by.get(f"{int(y) - 1} {mon}")


def uk():
    p, v, v0 = ons("mgsx")
    p2, y, y0 = ons("mgwy")
    if p != p2 or v is None or y is None:
        raise ValueError("ONS: the two series do not share a latest period")
    year, mon = p.split()
    year, i = int(year), ONS_M.index(mon)
    a, b = (i - 1) % 12, (i + 1) % 12                           # first and last month of the three
    ya = year - 1 if i == 0 else year
    yb = year + 1 if i == 11 else year
    en = f"{EN_M[a]}{'' if ya == yb else ' ' + str(ya)} to {EN_M[b]} {yb}"
    fr = f"{FR_M[a]}{'' if ya == yb else ' ' + str(ya)} à {FR_M[b]} {yb}"
    return dict(key="uk", period=p, period_en=en, period_fr=fr, all=v, all_prev=v0, youth=y, youth_prev=y0)


# ---- United States: BLS, monthly ----
def bls(series):
    d = json.loads(get(BLS.format(series)))
    if d.get("status") != "REQUEST_SUCCEEDED":
        raise ValueError(f"BLS: {d.get('message')}")
    rows = {(r["year"], r["period"]): fnum(r["value"]) for r in d["Results"]["series"][0]["data"] if r["period"].startswith("M")}
    last = max(k for k, v in rows.items() if v is not None)
    return last, rows[last], rows.get((str(int(last[0]) - 1), last[1]))


def usa():
    p, v, v0 = bls("LNS14000000")
    p2, y, y0 = bls("LNS14024887")
    if p != p2:
        raise ValueError("BLS: the two series do not share a latest month")
    m = int(p[1][1:]) - 1
    return dict(key="us", period=f"{p[0]}-{m + 1:02d}", period_en=f"{EN_M[m]} {p[0]}", period_fr=f"{FR_M[m]} {p[0]}",
                all=v, all_prev=v0, youth=y, youth_prev=y0)


# ---- GenAI Adoption Tracker (same reading as assets/trackers.js) ----
WAVE = re.compile(r"^(\d{1,2})/(\d{2})$")


def adoption():
    rows = list(csv.reader(io.StringIO(get(ADOPT + "GenAI_All.csv"))))
    head = {}
    for r in rows:
        if not r or WAVE.match(r[0]):
            continue
        name, filled = r[0].strip(), list(r)
        if name != "Statistic":
            for j in range(2, len(filled)):
                if filled[j] == "":
                    filled[j] = filled[j - 1]
        head[name] = filled

    def col(sample, use):
        for j in range(1, len(head["Statistic"])):
            if (head["Sample"][j], head["genAI Use"][j], head["Frequency"][j], head["Statistic"][j]) == (sample, use, "Share Using GenAI", "Mean"):
                return j
        raise ValueError("GenAI_All.csv: columns not found")

    c_any, c_work = col("All", "Any"), col("Employed", "For Work")
    waves = [(r[0], fnum(r[c_any]), fnum(r[c_work])) for r in rows if r and WAVE.match(r[0])]
    waves = [w for w in waves if w[1] is not None and w[2] is not None]
    key, any_, work = waves[-1]
    m = WAVE.match(key)
    mm, yy = int(m.group(1)), int(m.group(2))
    prev = next((w for w in waves if WAVE.match(w[0]) and int(WAVE.match(w[0]).group(1)) == mm and int(WAVE.match(w[0]).group(2)) == yy - 1), None)
    return dict(wave=f"20{yy:02d}-{mm:02d}", wave_en=f"{EN_M[mm - 1]} 20{yy:02d}", wave_fr=f"{FR_M[mm - 1]} 20{yy:02d}",
                any=round(any_, 1), work=round(work, 1),
                any_prev=round(prev[1], 1) if prev else None, work_prev=round(prev[2], 1) if prev else None)


def lift():
    rows = list(csv.DictReader(io.StringIO(get(LIFT))))
    cats = ["ia générative", "ia générale", "cv", "nlp"]           # mutually exclusive categories in LIFT's series
    months = {}
    for r in rows:
        y, m = int(float(r["annee"])), int(float(r["mois"]))
        months[(y, m)] = {c: fnum(r.get(c)) or 0.0 for c in cats}
    if not months:
        raise ValueError("LIFT: empty series")
    end = max(months)
    quarters = {}
    for (y, m), v in months.items():
        quarters.setdefault((y, (m - 1) // 3 + 1), []).append(v)
    full = [k for k, v in quarters.items() if len(v) == 3]
    qy, qn = max(full)
    q = quarters[(qy, qn)]
    return dict(genai_total=int(round(sum(v["ia générative"] for v in months.values()))),
                ai_total=int(round(sum(sum(v.values()) for v in months.values()))),
                genai_quarter=int(round(sum(v["ia générative"] for v in q))),
                ai_quarter=int(round(sum(sum(v.values()) for v in q))),
                end=f"{end[0]}-{end[1]:02d}", end_en=f"{EN_M[end[1] - 1]} {end[0]}", end_fr=f"{FR_M[end[1] - 1]} {end[0]}",
                quarter_en=f"Q{qn} {qy}", quarter_fr=f"{qn}e trimestre {qy}" if qn > 1 else f"1er trimestre {qy}")


# ---- Markdown block ----
def pct(v, lang):
    if v is None:
        return "n/a" if lang == "en" else "n.d."
    s = f"{v:.1f}"
    return s + "%" if lang == "en" else s.replace(".", ",") + " %"


def count(v, lang):
    return f"{v:,}" if lang == "en" else f"{v:,}".replace(",", " ")


def day(iso, lang):
    d = dt.date.fromisoformat(iso)
    return f"{d.day} {EN_M[d.month - 1]} {d.year}" if lang == "en" else f"{d.day} {FR_M[d.month - 1]} {d.year}"


def table(data, lang):
    en = lang == "en"
    names = {"fr": "France", "uk": "United Kingdom" if en else "Royaume-Uni", "us": "United States" if en else "États-Unis"}
    src = {"fr": "INSEE", "uk": "ONS", "us": "BLS"}
    head = (["Country", "Unemployment rate", "A year earlier", "Young people", "A year earlier", "Period"] if en else
            ["Pays", "Taux de chômage", "Un an plus tôt", "Jeunes", "Un an plus tôt", "Période"])
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for c in data["countries"]:
        out.append("| " + " | ".join([names[c["key"]], pct(c["all"], lang), pct(c["all_prev"], lang), pct(c["youth"], lang),
                                      pct(c["youth_prev"], lang), c["period_en"] if en else c["period_fr"]]) + " |")
    links = ", ".join(f"[{src[c['key']]}]({PAGES[c['key']]})" for c in data["countries"])
    if en:
        out += ["", f"Official unemployment rates, seasonally adjusted, read on {day(data['updated'], lang)} from {links}. "
                    "Young people: under 25 in France, 16 to 24 in the United Kingdom and the United States. France is quarterly, "
                    "the United Kingdom a three-month average, the United States monthly, so compare each country with itself a year "
                    "earlier, not with the others. \"n/a\": no figure was published for that period. These rates cover the whole labour "
                    "market: they do not isolate the effect of AI."]
    else:
        out += ["", f"Taux de chômage officiels, corrigés des variations saisonnières, lus le {day(data['updated'], lang)} auprès de : {links}. "
                    "Jeunes : moins de 25 ans en France, 16 à 24 ans au Royaume-Uni et aux États-Unis. La France est trimestrielle, "
                    "le Royaume-Uni une moyenne sur trois mois, les États-Unis mensuels : comparez chaque pays à lui-même un an plus "
                    "tôt, pas aux autres. « n.d. » : aucun chiffre publié pour cette période. Ces taux couvrent tout le marché du "
                    "travail : ils n'isolent pas l'effet de l'IA."]
    a, l = data.get("adoption"), data.get("lift")
    bullets = []
    if a:
        prev = "" if a.get("work_prev") is None else (f", against {pct(a['work_prev'], lang)} a year earlier" if en else f", contre {pct(a['work_prev'], lang)} un an plus tôt")
        bullets.append((f"- **AI at work, United States.** {pct(a['work'], lang)} of employed adults used generative AI for work in {a['wave_en']}{prev} "
                        f"([GenAI Adoption Tracker]({PAGES['adoption']}), Bick, Blandin and Deming).") if en else
                       (f"- **L'IA au travail, États-Unis.** {pct(a['work'], lang)} des personnes en emploi utilisaient l'IA générative pour leur travail en {a['wave_fr']}{prev} "
                        f"([GenAI Adoption Tracker]({PAGES['adoption']}), Bick, Blandin et Deming)."))
    if l and l.get("end"):
        bullets.append((f"- **AI hiring, France.** {count(l['genai_total'], lang)} job postings asking for generative AI skills from January 2019 to {l['end_en']}, "
                        f"{count(l['genai_quarter'], lang)} of them in {l['quarter_en']}; {count(l['ai_total'], lang)} postings for AI skills of any kind "
                        f"([LIFT tracker]({PAGES['lift']}), HEC Paris, monthly series built from the Dares JOCAS database; the series ends in {l['end_en']}). "
                        "These count demand for AI specialists, not the effect of AI on other jobs.") if en else
                       (f"- **Embauches en IA, France.** {count(l['genai_total'], lang)} offres d'emploi demandant des compétences en IA générative de janvier 2019 à {l['end_fr']}, "
                        f"dont {count(l['genai_quarter'], lang)} au {l['quarter_fr']} ; {count(l['ai_total'], lang)} offres pour des compétences en IA de tout type "
                        f"([tracker LIFT]({PAGES['lift']}), HEC Paris, série mensuelle construite à partir de la base JOCAS de la Dares ; la série s'arrête en {l['end_fr']}). "
                        "Ces chiffres mesurent la demande de spécialistes de l'IA, pas l'effet de l'IA sur les autres emplois."))
    return "\n".join(out + ([""] + bullets if bullets else [])) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--offline", action="store_true")
    a = ap.parse_args()
    path = os.path.join(a.root, "_data", "employment.json")
    old = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    data = dict(old)
    if not a.offline:
        prev = {c["key"]: c for c in old.get("countries", [])}
        countries, fresh = [], 0
        for key, fn in (("fr", france), ("uk", uk), ("us", usa)):
            try:
                countries.append(fn()); fresh += 1
            except Exception as e:                              # keep the last figures read
                print(f"::warning::{key}: {e}; kept the previous figures", file=sys.stderr)
                if key in prev:
                    countries.append(prev[key])
        data["countries"] = countries
        for key, fn in (("adoption", adoption), ("lift", lift)):
            try:
                data[key] = fn(); fresh += 1
            except Exception as e:
                print(f"::warning::{key}: {e}; kept the previous figures", file=sys.stderr)
        if fresh:
            data["updated"] = dt.date.today().isoformat()
    if not data.get("countries"):
        print("no figures at all", file=sys.stderr); sys.exit(1)
    json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(path, "a").write("\n")
    for lang in ("en", "fr"):
        open(os.path.join(a.root, "_includes", f"employment-table-{lang}.md"), "w", encoding="utf-8").write(table(data, lang))
    print(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    main()
