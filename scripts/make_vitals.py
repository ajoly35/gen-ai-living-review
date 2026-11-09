#!/usr/bin/env python3
"""Research vitals: charts and tiles describing where the literature is heading.
Reads _data/papers.yml (one item per study), writes assets/vitals/*.svg and *.png and _data/vitals.yml
(tiles and captions in English and French). Run: python3 scripts/make_vitals.py   (needs matplotlib, pyyaml)."""
import collections, datetime as dt, os, sys
import yaml
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "vitals"); os.makedirs(OUT, exist_ok=True)
papers_all = yaml.safe_load(open(os.path.join(ROOT, "_data", "papers.yml"), encoding="utf-8"))
# the vitals cover the GenAI period: studies from 2023 on (older classics cited by the growth review are kept in the table only)
papers = [p for p in papers_all if (p.get("year") or 0) >= 2023]
LIVE = dt.date(2026, 10, 17)  # the site went live; entries carrying an earlier proxy date were added after it
for p in papers:
    if p.get("added"):
        d = dt.date.fromisoformat(str(p["added"])[:10])
        if d < LIVE: p["added"] = LIVE.isoformat()
today = dt.date.today()

SURF = "#fcfcfb"; INK = "#1f1d1a"; MUTED = "#6b665e"; GRID = "#e4e0d8"
THEME_ORDER = ["employment", "wages", "growth", "organisation", "other"]
THEME_COL = {"employment": "#2a78d6", "wages": "#eb6834", "growth": "#9a5bd6", "organisation": "#2f9e63", "other": "#9c968c"}
THEME_LAB = {"en": {"employment": "Employment and hiring", "wages": "Wages", "growth": "Growth and productivity", "organisation": "Organisation and adoption", "other": "Other (education, theory, exposure)"},
             "fr": {"employment": "Emploi et embauches", "wages": "Salaires", "growth": "Croissance et productivité", "organisation": "Organisation et adoption", "other": "Autres (éducation, théorie, exposition)"}}
DIR_COL = {"negative": "#eb6834", "null": "#9c968c", "positive": "#2a78d6", "mixed": "#9a5bd6"}
DIR_LAB = {"en": {"negative": "Fewer jobs, hires or lower pay", "null": "No significant effect", "positive": "More jobs, output or pay", "mixed": "Mixed"},
           "fr": {"negative": "Moins d'emplois, d'embauches ou de salaire", "null": "Pas d'effet significatif", "positive": "Plus d'emplois, de production ou de salaire", "mixed": "Résultats mixtes"}}
DESIGN_ORDER = ["field-experiment", "lab-or-online-experiment", "survey-linked-registers", "exposure-did", "adoption-did", "synthetic-control-or-event-study", "online-labour-market", "structural-or-calibrated-model", "theory", "descriptive-or-survey", "growth-accounting-or-official", "news"]
DESIGN_LAB = {"en": {"field-experiment": "Field experiment", "lab-or-online-experiment": "Lab or online experiment", "survey-linked-registers": "Survey linked to registers", "exposure-did": "Exposure difference in differences", "adoption-did": "Firm adoption comparison", "synthetic-control-or-event-study": "Event study or synthetic control", "online-labour-market": "Online labour market", "structural-or-calibrated-model": "Calibrated model", "theory": "Theory", "descriptive-or-survey": "Descriptive or survey", "growth-accounting-or-official": "Growth accounting, official release", "news": "News item"},
              "fr": {"field-experiment": "Expérience de terrain", "lab-or-online-experiment": "Expérience en laboratoire ou en ligne", "survey-linked-registers": "Enquête appariée aux registres", "exposure-did": "Différence de différences par exposition", "adoption-did": "Comparaison d'entreprises adoptantes", "synthetic-control-or-event-study": "Étude d'événement ou contrôle synthétique", "online-labour-market": "Marché du travail en ligne", "structural-or-calibrated-model": "Modèle calibré", "theory": "Théorie", "descriptive-or-survey": "Descriptif ou enquête", "growth-accounting-or-official": "Comptabilité de la croissance, publication officielle", "news": "Article de presse"}}

def src(p): return p["source"] if isinstance(p.get("source"), list) else [p.get("source")]

def theme_group(p):
    t = p.get("theme") or "theory-other"
    if t in ("employment",): return "employment"
    if t == "wages": return "wages"
    if t in ("growth", "productivity"): return "growth"
    if t in ("organisation", "adoption-diffusion"): return "organisation"
    return "other"

def month(p):
    d = str(p.get("date") or "")
    return d[:7] if len(d) >= 7 else None

def quarter(m):
    y, mo = int(m[:4]), int(m[5:7]); return f"{y} Q{(mo - 1) // 3 + 1}"

def style(ax):
    ax.set_facecolor(SURF)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID); ax.tick_params(colors=MUTED, labelsize=9, length=0)
    ax.yaxis.grid(True, color=GRID, linewidth=.6); ax.set_axisbelow(True)

def save(fig, name):
    fig.patch.set_facecolor(SURF)
    for ext in ("svg", "png"): fig.savefig(os.path.join(OUT, f"{name}.{ext}"), dpi=180, bbox_inches="tight", facecolor=SURF)
    plt.close(fig)

plt.rcParams.update({"font.family": ["Helvetica Neue", "Arial", "DejaVu Sans"], "text.color": INK, "axes.labelcolor": MUTED})

studies = [p for p in papers if (p.get("design") != "news")]
news = [p for p in papers if p.get("design") == "news"]

# ---- Chart 1: studies by quarter of release, stacked by theme --------------------------------------
qs = sorted({str(p.get("year")) for p in studies if p.get("year")})
counts = {g: [sum(1 for p in studies if str(p.get("year")) == q and theme_group(p) == g) for q in qs] for g in THEME_ORDER}
for lang in ("en", "fr"):
    fig, ax = plt.subplots(figsize=(8.4, 4.2)); style(ax)
    bottom = [0] * len(qs)
    for g in THEME_ORDER:
        ax.bar(range(len(qs)), counts[g], bottom=bottom, color=THEME_COL[g], width=.72, label=THEME_LAB[lang][g], edgecolor=SURF, linewidth=1.5)
        bottom = [b + c for b, c in zip(bottom, counts[g])]
    for i, tot in enumerate(bottom):
        if tot: ax.text(i, tot + .25, str(tot), ha="center", va="bottom", fontsize=9, color=MUTED)
    ax.set_xticks(range(len(qs))); ax.set_xticklabels(qs, rotation=0, fontsize=8.5)
    ax.set_ylabel("Studies" if lang == "en" else "Études", fontsize=9)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left", ncol=1)
    save(fig, f"studies-by-year-{lang}")

# ---- Chart 2: research designs, causal or not --------------------------------------------------------
dcount = collections.Counter(p.get("design") for p in studies if p.get("design"))
designs = [d for d in DESIGN_ORDER if dcount.get(d)]
for lang in ("en", "fr"):
    fig, ax = plt.subplots(figsize=(8.4, 0.42 * len(designs) + 1.2)); style(ax); ax.xaxis.grid(True, color=GRID, linewidth=.6); ax.yaxis.grid(False)
    causal = [sum(1 for p in studies if p.get("design") == d and p.get("causal")) for d in designs]
    other = [dcount[d] - c for d, c in zip(designs, causal)]
    y = range(len(designs))[::-1]
    ax.barh(y, causal, color="#2a78d6", height=.62, label=("Meets the review's causal standard" if lang == "en" else "Au standard causal de la revue"))
    ax.barh(y, other, left=causal, color="#c9c3b8", height=.62, label=("Context: descriptive, theory, model" if lang == "en" else "Contexte : descriptif, théorie, modèle"))
    ax.set_yticks(list(y)); ax.set_yticklabels([DESIGN_LAB[lang][d] for d in designs], fontsize=9)
    for yi, c, o in zip(y, causal, other): ax.text(c + o + .15, yi, str(c + o), va="center", fontsize=9, color=MUTED)
    ax.legend(frameon=False, fontsize=8.5, loc="lower right")
    ax.set_xlabel("Studies" if lang == "en" else "Études", fontsize=9)
    save(fig, f"designs-{lang}")

# ---- Chart 3: direction of the labour-market answer, by design (causal studies on employment/wages) ----
lab = [p for p in studies if theme_group(p) in ("employment", "wages") and p.get("direction") in DIR_COL]
dirs = ["negative", "null", "mixed", "positive"]
d3 = [d for d in DESIGN_ORDER if any(p.get("design") == d for p in lab)]
for lang in ("en", "fr"):
    fig, ax = plt.subplots(figsize=(8.4, 0.5 * len(d3) + 1.4)); style(ax); ax.xaxis.grid(True, color=GRID, linewidth=.6); ax.yaxis.grid(False)
    y = range(len(d3))[::-1]; left = [0] * len(d3)
    for dr in dirs:
        vals = [sum(1 for p in lab if p.get("design") == d and p.get("direction") == dr) for d in d3]
        ax.barh(y, vals, left=left, color=DIR_COL[dr], height=.62, label=DIR_LAB[lang][dr], edgecolor=SURF, linewidth=1.5)
        for yi, l, v in zip(y, left, vals):
            if v: ax.text(l + v / 2, yi, str(v), ha="center", va="center", fontsize=8.5, color="white" if dr != "null" else INK)
        left = [l + v for l, v in zip(left, vals)]
    ax.set_yticks(list(y)); ax.set_yticklabels([DESIGN_LAB[lang][d] for d in d3], fontsize=9)
    ax.legend(frameon=False, fontsize=8.5, loc="lower right", ncol=2)
    ax.set_xlabel("Studies on employment, hiring or wages" if lang == "en" else "Études sur l'emploi, les embauches ou les salaires", fontsize=9)
    save(fig, f"direction-by-design-{lang}")

# ---- Chart 4: what is added to the living review, by month and theme (since the site went live) -----
added = [p for p in papers if p.get("added") and "latest" in src(p)]
def week(p):
    d = dt.date.fromisoformat(str(p["added"])[:10]); d = d - dt.timedelta(days=d.weekday()); return d.isoformat()
ams = sorted({week(p) for p in added})
for lang in ("en", "fr"):
    fig, ax = plt.subplots(figsize=(8.4, 3.6)); style(ax)
    bottom = [0] * len(ams)
    for g in THEME_ORDER:
        vals = [sum(1 for p in added if week(p) == m and theme_group(p) == g) for m in ams]
        ax.bar(range(len(ams)), vals, bottom=bottom, color=THEME_COL[g], width=.6, label=THEME_LAB[lang][g], edgecolor=SURF, linewidth=1.5)
        bottom = [b + v for b, v in zip(bottom, vals)]
    for i, t in enumerate(bottom): ax.text(i, t + .3, str(t), ha="center", fontsize=9, color=MUTED)
    ax.set_xticks(range(len(ams))); ax.set_xticklabels([("w/c " if lang=="en" else "sem. ") + m[8:10] + "/" + m[5:7] for m in ams], fontsize=8.5)
    ax.set_ylabel("Entries added" if lang == "en" else "Entrées ajoutées", fontsize=9)
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")
    save(fig, f"added-by-week-{lang}")

# ---- Tiles ------------------------------------------------------------------------------------------
n = len(studies); n_causal = sum(1 for p in studies if p.get("causal"))
lab_causal = [p for p in lab if p.get("causal")]
neg = sum(1 for p in lab_causal if p["direction"] == "negative"); nul = sum(1 for p in lab_causal if p["direction"] == "null"); pos = sum(1 for p in lab_causal if p["direction"] == "positive")
entry = [p for p in lab_causal if "hir" in str(p.get("outcome", "")).lower() or "entry" in str(p.get("outcome", "")).lower() or "junior" in str(p.get("outcome", "")).lower() or "young" in str(p.get("population", "")).lower()]
entry_neg = sum(1 for p in entry if p["direction"] == "negative")
last30 = sum(1 for p in papers if "latest" in src(p) and p.get("added") and (today - dt.date.fromisoformat(str(p["added"])[:10])).days <= 30)
growth = [p for p in studies if theme_group(p) == "growth"]
months_ago = [ (today.year - int(month(p)[:4])) * 12 + today.month - int(month(p)[5:7]) for p in studies if month(p)]
median_age = sorted(months_ago)[len(months_ago) // 2] if months_ago else None
countries = collections.Counter(str(p.get("country") or "").split(",")[0].strip() for p in studies if p.get("country"))
top_c = ", ".join(f"{c} {k}" for c, k in countries.most_common(3))

tiles = {
 "en": [
  {"value": str(n), "label": "studies in the review", "compare": f"{n_causal} meet the causal standard; {len(news)} news items kept as context"},
  {"value": f"{neg}/{len(lab_causal)}", "label": "causal labour-market studies finding fewer jobs, hires or lower pay", "compare": f"{nul} find no effect, {pos} find gains"},
  {"value": f"{entry_neg}/{len(entry)}", "label": "causal studies of hiring, entry or young workers that find a fall", "compare": f"{sum(1 for p in entry if p['direction']=='null')} find no effect, {sum(1 for p in entry if p['direction']=='positive')} find more hiring"},
  {"value": str(len(growth)), "label": "growth and productivity studies", "compare": "mostly calibrated models and growth accounting, few causal estimates"},
  {"value": str(last30), "label": "papers added to Latest research in the last 30 days", "compare": "one paper a morning when there is one"},
  {"value": f"{median_age} mo" if median_age is not None else "n/a", "label": "median age of the version cited", "compare": top_c},
 ],
 "fr": [
  {"value": str(n), "label": "études dans la revue", "compare": f"{n_causal} au standard causal ; {len(news)} articles de presse gardés pour le contexte"},
  {"value": f"{neg}/{len(lab_causal)}", "label": "études causales sur le travail trouvant moins d'emplois, d'embauches ou de salaire", "compare": f"{nul} sans effet, {pos} avec des gains"},
  {"value": f"{entry_neg}/{len(entry)}", "label": "études causales sur les embauches, l'entrée ou les jeunes qui trouvent une baisse", "compare": f"{sum(1 for p in entry if p['direction']=='null')} sans effet, {sum(1 for p in entry if p['direction']=='positive')} avec plus d'embauches"},
  {"value": str(len(growth)), "label": "études sur la croissance et la productivité", "compare": "surtout des modèles calibrés et de la comptabilité de la croissance"},
  {"value": str(last30), "label": "articles ajoutés aux Articles récents en 30 jours", "compare": "un article par matin quand il y en a un"},
  {"value": f"{median_age} mois" if median_age is not None else "n/a", "label": "âge médian de la version citée", "compare": top_c},
 ]}
yaml.safe_dump({"as_of": today.isoformat(), "n_studies": n, "n_news": len(news), "tiles": tiles}, open(os.path.join(ROOT, "_data", "vitals.yml"), "w", encoding="utf-8"), allow_unicode=True, sort_keys=False)
print("studies", n, "causal", n_causal, "news", len(news), "labour causal", len(lab_causal), "neg/null/pos", neg, nul, pos, "entry", entry_neg, len(entry), "growth", len(growth), "added30", last30)
print("designs", dict(dcount)); print("themes", collections.Counter(theme_group(p) for p in studies))
