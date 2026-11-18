"""Monthly refresh of the chapter 6 charts on /manuel/chapitre-6/ (run by .github/workflows/manuel-ch6.yml).

Downloads public OECD data, redraws the "original vs update" charts and writes the latest figures to
_data/manuel_ch6_charts.yml so the page text quotes them. Original series (from the published sources,
extracted once from their vector figures) and the Dealroom round-size panel are static CSVs in
assets/manuel-ch6/data/; Dealroom has no public API, so that panel is refreshed by hand.

Usage: python3 -I scripts/manuel_ch6_charts.py [--offline]   (--offline reuses the last downloaded CSVs)
Exit 0 on success; on a download failure it keeps the previous charts and exits 0 with a warning,
so a temporary OECD outage never breaks the site.
"""
import sys, json, datetime, pathlib, subprocess
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mt

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "assets" / "manuel-ch6"; DATA = A / "data"
URL_PDB = ("https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_PDB@DF_PDB,2.0/"
           "FRA+USA+DEU.A.GDPHRS._T.USD_PPP_H.LR.N._Z.PPP?startPeriod=2003&format=csvfilewithlabels")
PAYS = ["USA", "CAN", "SWE", "FRA", "FIN", "GBR", "NLD", "ESP", "DEU", "IRL", "ITA"]
NOMS = {"USA": "États-Unis", "CAN": "Canada", "SWE": "Suède", "FRA": "France", "FIN": "Finlande", "GBR": "Royaume-Uni",
        "NLD": "Pays-Bas", "ESP": "Espagne", "DEU": "Allemagne", "IRL": "Irlande", "ITA": "Italie"}
URL_VC = ("https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_VC@DF_VC_INV,1.0/"
          + "+".join(PAYS) + ".VC_INV_MKT.SEED+START+LATER.PT_B1GQ.A?startPeriod=2018&format=csvfilewithlabels")

plt.rcParams.update({"font.family": "serif", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#dddddd", "grid.linewidth": 0.5, "axes.axisbelow": True})
virg = lambda nd: mt.FuncFormatter(lambda v, _: f"{v:.{nd}f}".replace(".", ","))

def get(url, cache):
    if "--offline" not in sys.argv:
        tmp = cache.with_suffix(".tmp")
        r = subprocess.run(["curl", "-sfL", "--retry", "3", "--retry-delay", "10", "--retry-all-errors",
                            "--max-time", "180", "-A", "living-review-bot", "-o", str(tmp), url])
        try:
            if r.returncode != 0:
                raise RuntimeError(f"curl exit {r.returncode}")
            df = pd.read_csv(tmp)
            if len(df) == 0:
                raise ValueError("empty response")
            tmp.replace(cache)
            return df, True
        except Exception as e:  # keep last good copy
            print(f"WARNING: download failed for {cache.name}: {e}", file=sys.stderr)
            tmp.unlink(missing_ok=True)
    if not cache.exists():
        print(f"WARNING: no cached copy of {cache.name}; charts left unchanged", file=sys.stderr)
        sys.exit(0)
    return pd.read_csv(cache), False

def save(fig, name):
    fig.savefig(A / f"{name}.png", dpi=170, bbox_inches="tight"); plt.close(fig)

def main():
    today = datetime.date.today().isoformat()
    out = {"maj_le": today}
    # ---------- 6.4
    pdb, fresh64 = get(URL_PDB, DATA / "oecd_pdb_raw.csv")
    p = pdb[pdb.PRICE_BASE == "LR"].pivot_table(index="TIME_PERIOD", columns="REF_AREA", values="OBS_VALUE").dropna()
    g = pd.DataFrame({"year": p.index, "fr_us": (p.FRA / p.USA).values, "fr_de": (p.FRA / p.DEU).values})
    g.to_csv(DATA / "graph64_ocde.csv", index=False)
    g0 = pd.read_csv(DATA / "graph64_original_guadalupe2022.csv")
    fig, (b1, b2) = plt.subplots(1, 2, figsize=(10, 3.4))
    for ax, df, ttl in ((b1, g0, "Version du livre : corrigée de la composition de l'emploi, 2003-2019"),
                        (b2, g, f"Mise à jour : OCDE, non corrigée, 2003-{int(g.year.max())}")):
        ax.plot(df.year, df.fr_us, color="black", lw=1.6, label="France/États-Unis")
        ax.plot(df.year, df.fr_de, color="black", lw=1.6, ls="--", label="France/Allemagne")
        ax.axhline(1, color="#888", lw=0.8); ax.set_title(ttl, fontsize=8.5, loc="left")
        ax.xaxis.set_major_locator(mt.MultipleLocator(4)); ax.xaxis.set_major_formatter(mt.FormatStrFormatter("%d"))
        ax.yaxis.set_major_formatter(virg(2)); ax.set_xlim(2003, df.year.max())
    b1.set_ylabel("Productivité horaire relative (1 = égalité)"); b1.legend(frameon=False, fontsize=8)
    fig.text(0.01, -0.05, "Sources : Guadalupe, Jaravel, Philippon et Sraer (2022), Note du CAE n° 75, fig. 1 ; OCDE, base de données "
             f"sur la productivité (PIB par heure travaillée, PPA constantes de 2020), extraction du {today}. Ne pas raccorder les deux séries.", fontsize=7)
    save(fig, "graphique-6-4")
    last = g.iloc[-1]
    out["g64"] = {"annee": int(last.year), "fr_us": round(float(last.fr_us), 2), "fr_de": round(float(last.fr_de), 2),
                  "fr_us_2003": round(float(g.fr_us.iloc[0]), 2), "frais": fresh64}
    # ---------- 6.5
    vc, fresh65 = get(URL_VC, DATA / "oecd_vc_raw.csv")
    vc = vc[(vc.UNIT_MEASURE == "PT_B1GQ")]
    w = vc.pivot_table(index=["REF_AREA", "TIME_PERIOD"], columns="BUSINESS_DEVELOPMENT_STAGE", values="OBS_VALUE").reset_index()
    w["early"] = w.SEED + w.START; w["later"] = w.LATER; w["total"] = w.early + w.later
    full = w.dropna(subset=["total"]).groupby("TIME_PERIOD").REF_AREA.nunique()
    yr = int(full[full == len(PAYS)].index.max())
    cur = w[w.TIME_PERIOD == yr].set_index("REF_AREA").reindex(PAYS)
    cur[["early", "later", "total"]].assign(year=yr).to_csv(DATA / "graph65_gauche_ocde.csv")
    o_l = pd.read_csv(DATA / "graph65_left_original_2022.csv")
    o_r = pd.read_csv(DATA / "graph65_right_original_2000-2023.csv")
    d_r = pd.read_csv(DATA / "graph65_right_dealroom.csv"); d_r = d_r[d_r.period.astype(str) == "2025"]
    fig, axs = plt.subplots(2, 2, figsize=(11, 7))
    def stack(ax, e, l, labels, ttl):
        x = range(len(labels))
        ax.bar(x, e, color="#333333", width=0.7, edgecolor="white", lw=0.8, label="Amorçage/premiers stades")
        ax.bar(x, l, bottom=e, color="#aaaaaa", width=0.7, edgecolor="white", lw=0.8, label="Stades ultérieurs")
        ax.set_xticks(list(x)); ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
        ax.set_ylim(0, 0.75); ax.yaxis.set_major_formatter(mt.FuncFormatter(lambda v, _: f"{v:.1f} %".replace(".", ",")))
        ax.set_title(ttl, fontsize=9, loc="left"); ax.grid(axis="x", visible=False)
    stack(axs[0, 0], o_l.early_pct_gdp, o_l.later_pct_gdp, [NOMS[c] for c in PAYS], "Version du livre : capital-risque en % du PIB, 2022")
    stack(axs[0, 1], cur.early, cur.later, [NOMS[c] for c in PAYS], f"Mise à jour : capital-risque en % du PIB, {yr} (OCDE)")
    axs[0, 0].legend(frameon=False, fontsize=8); axs[0, 0].set_ylabel("% du PIB")
    def grouped(ax, vals, ttl):
        cats = ["1 à 4 M$", "4 à 15 M$", "15 à 100 M$", "100 M$ et plus"]; wd = 0.26
        for i, (lab, c) in enumerate((("États-Unis", "#222222"), ("Europe", "#888888"), ("Asie / reste du monde", "#cccccc"))):
            ax.bar([k + (i - 1) * wd for k in range(4)], vals[i], width=wd, color=c, edgecolor="white", lw=0.8, label=lab)
        ax.set_xticks(range(4)); ax.set_xticklabels(cats, fontsize=8); ax.set_ylim(0, 80)
        ax.set_title(ttl, fontsize=9, loc="left"); ax.grid(axis="x", visible=False)
    grouped(axs[1, 0], [o_r[o_r.region == r].share_pct.tolist() for r in ("USA", "Europe", "Asia")],
            "Version du livre : part du volume mondial par taille de tour, 2000-2023 (%)")
    grouped(axs[1, 1], [d_r.us_share_pct.tolist(), d_r.europe_share_pct.tolist(), d_r.rest_of_world_incl_asia_share_pct.tolist()],
            "Mise à jour : part du volume mondial par taille de tour, 2025 (%)")
    axs[1, 0].legend(frameon=False, fontsize=8)
    fig.text(0.01, -0.03, "Sources : à gauche, CAE et Conseil allemand des experts économiques (2024), fig. 6 (Dealroom 2023, OCDE ; valeurs extraites "
             f"de la figure publiée). À droite : OCDE, Venture capital investments, extraction du {today} ; Dealroom.co (données d'octobre 2026, mise à jour manuelle).\n"
             "En bas à droite, « reste du monde » inclut l'Asie (non publiée séparément) ; périodes et périmètres différents : comparer les écarts, pas les niveaux.", fontsize=7)
    fig.tight_layout(); save(fig, "graphique-6-5")
    us = cur.loc["USA", "total"]
    out["g65"] = {"annee": yr, "fr_fois": round(float(us / cur.loc["FRA", "total"]), 1),
                  "de_fois": round(float(us / cur.loc["DEU", "total"]), 1), "frais": fresh65}
    # ---------- 6.3 is static (digitised published figures); nothing to fetch
    lines = ["# Written by scripts/manuel_ch6_charts.py; do not edit by hand.", f"maj_le: {out['maj_le']}"]
    for k in ("g64", "g65"):
        lines.append(f"{k}:"); lines += [f"  {a}: {json.dumps(b)}" for a, b in out[k].items()]
    (ROOT / "_data" / "manuel_ch6_charts.yml").write_text("\n".join(lines) + "\n")
    print(json.dumps(out, ensure_ascii=False))

if __name__ == "__main__":
    main()
