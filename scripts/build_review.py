"""Rebuild the review body and references for the public site from the LaTeX source.

usage: python3 -I scripts/build_review.py <review.tex> <references.bib>
Writes _includes/review.md and _includes/references-review.md. Run from site/.
Edits in PUBLIC_EDITS keep material that is not for circulation off the public page.
"""
import re, subprocess, sys, pathlib, tempfile

PUBLIC_EDITS = [
    # Ando et al. (2026, IMF) is "preliminary, please do not circulate": private copy only.
    ("; comparing occupations within the same economy, industry and month across 110 economies, \\citet{ando2026labor} find postings in more exposed occupations down nearly 10\\%", ""),
]
EXCLUDE_KEYS = {"ando2026labor"}

tex_path, bib_path = map(pathlib.Path, sys.argv[1:3])
tex = tex_path.read_text()
for old, new in PUBLIC_EDITS:
    if old not in tex:
        sys.exit(f"public edit no longer matches the source, check it by hand: {old[:60]}...")
    tex = tex.replace(old, new)
if any(re.search(r"\\cite[pt]?\*?(\[[^]]*\])?\{[^}]*" + k, tex) for k in EXCLUDE_KEYS):
    sys.exit("an excluded paper is still cited; add a PUBLIC_EDITS entry")
tex = re.sub(r"^\\renewcommand\{\\(sub)?section\}.*\n", "", tex, flags=re.M)
labels = dict((m.group(2), m.group(1)) for m in re.finditer(r"\\(?:sub)?section\{([^}]*)\}\s*\\label\{([^}]*)\}", tex))
labels = {k: v for v, k in [(v, k) for k, v in labels.items()]}

with tempfile.TemporaryDirectory() as d:
    src = pathlib.Path(d, "r.tex"); src.write_text(tex)
    md = subprocess.run(["pandoc", str(src), "-f", "latex", "-t", "gfm", "--citeproc",
                         f"--bibliography={bib_path.resolve()}", "--wrap=none"],
                        capture_output=True, text=True, check=True).stdout

def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
md = re.sub(r'<a href="#([^"]+)"[^>]*>[^<]*</a>',
            lambda m: f'[“{labels.get(m.group(1), m.group(1))}”](#{slug(labels.get(m.group(1), m.group(1)))})', md)
md = re.sub(r"Sections?\u00a0", lambda m: m.group(0).lower().replace("\u00a0", " "), md)
md = re.sub(r'<span id="[^"]*"[^>]*></span>\n?', "", md)
md = re.sub(r'<span class="nocase">([^<]*)</span>', r"\1", md)
md = re.sub(r"``` math\n(.*?)\n```", lambda m: "\n\n$$\n" + m.group(1).rstrip(",").strip() + "\n$$\n\n", md, flags=re.S)
md = re.sub(r"\$`([^`]*)`\$", r"$$\1$$", md)          # kramdown inline maths
md = md.replace("\\$", "&#36;")
md = re.sub(r'<div class="multicols">.*?</div>\n*', "", md, flags=re.S)
body, _, refs = md.partition('<div id="refs"')
notes = re.findall(r"^\[\^\d+\]: .*$", body, flags=re.M)
body = re.sub(r"^\[\^\d+\]: .*\n?", "", body, flags=re.M).strip()
body = re.sub(r"^(#+) ", lambda m: "#" + m.group(1) + " ", body, flags=re.M)
refs = re.sub(r"<[^>]+>", "", refs)
refs = "\n\n".join(l.strip() for l in refs.split("\n") if l.strip())
refs = re.sub(r" \.(?=\s|$)", ".", refs)
pathlib.Path("_includes/review.md").write_text(body + "\n\n" + "\n".join(notes) + "\n")
pathlib.Path("_includes/references-review.md").write_text(refs + "\n")
print("wrote _includes/review.md and _includes/references-review.md")
