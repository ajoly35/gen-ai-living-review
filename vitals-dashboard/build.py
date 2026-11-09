"""Build index.html from field-ledger.csv and template.html."""
import csv, json, pathlib
here = pathlib.Path(__file__).parent
rows = list(csv.DictReader(open(here / "field-ledger.csv", encoding="utf-8")))
for r in rows:
    r["year"] = int(r["year"])
html = (here / "template.html").read_text(encoding="utf-8").replace("__DATA__", json.dumps(rows, ensure_ascii=False).replace("</", "<\\/"))
(here / "index.html").write_text(html, encoding="utf-8")
print(len(rows), "rows ->", here / "index.html")
