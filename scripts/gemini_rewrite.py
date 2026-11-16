#!/usr/bin/env python3
"""Have Gemini write the newsletter's prose, in place, before scripts/build_email.py runs.

The routine still finds, reads and checks the papers and writes the entries, briefs and monthly update.
This step only rewrites their prose paragraphs, in Adrien's voice, for the emails. It runs in the GitHub
runner's checkout and its changes are not committed: the site keeps the routine's text, the emails (and
their archive copy in emails/) get Gemini's.

Structure is never sent for rewriting: front matter, headings, HTML comments, Liquid, kramdown attribute
lines, images, tables, the provenance line under each entry heading, and link-only lines stay as they are.
Each rewritten paragraph is checked, and the routine's original is kept when a check fails:
  - same bold label at the start (**What it finds.** ...), same line count and line labels/bullets;
  - the same set of link URLs;
  - every number in the new text appears in the original (nothing invented);
  - no em-dash, no banned word; length between 50% and 160% of the original.

Usage (see .github/workflows/email.yml):
  gemini_rewrite.py entries added.md --lang en
  gemini_rewrite.py entries _includes/fr/latest.md --lang fr --only-anchors-from added.md
  gemini_rewrite.py briefs briefs --kind daily --lang en
  gemini_rewrite.py page updates/2026-11.md --lang en
Needs GEMINI_API_KEY; without it, does nothing. Model: GEMINI_MODEL (default gemini-4-carbon).
"""
import argparse, datetime as dt, http.client, json, os, re, sys, time, urllib.error, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_email import parse_entries  # same anchors as the email builder

MODEL = os.environ.get("GEMINI_MODEL", "gemini-4-carbon")
BANNED = ["delve", "leverage", "multifaceted", "furthermore", "moreover", "robust", "compelling",
          "navigate", "foster", "transformative", "pivotal"]
TECH = ["difference in differences", "difference-in-differences", "treatment", "exposure", "identification",
        "standard deviation", "regression", "instrument", "elasticity", "significant", "quintile",
        "heterogeneity", "counterfactual", "endogenous", "causal"]

SYSTEM = """You rewrite the prose of "Gen-AI, Jobs and Growth", the AI-and-work newsletter of Adrien Joly,
research fellow at the London School of Economics. Readers: economists, policy people and curious
non-specialists. It goes out under his name, so it must sound like a person, not like an AI.

You receive a JSON array of paragraphs. Return a JSON array of the same length, each item the rewritten
paragraph at the same position.

Hard rules, for every paragraph:
- Same meaning and the same facts. Use only the facts, figures, names, dates and citations already in it.
  Never add a number, study, claim or source. Keep every number exactly as written.
- Keep every Markdown link exactly: [text](url), url unchanged.
- If a paragraph starts with a bold label such as **What it finds.** or **In brief.**, keep that label
  exactly, at the start.
- If a paragraph has several lines (bullets, or lines like "What it explores: ..."), return the same
  number of lines, each starting with the same bullet or the same label before the colon.
- Same language as the input (English or French; French in a natural, non-literal register).
- No em-dashes or double hyphens. Use commas or split the sentence.
- Never use: delve, leverage, multifaceted, furthermore, moreover, robust, compelling, navigate, foster,
  transformative, pivotal.
- Plain, concrete words, short sentences, active verbs. Say what was compared with what. Each number keeps
  its reference point (compared with whom, since when).
- Roughly the same length as the original."""

GENERAL = """
This is the general-audience edition: no technical vocabulary at all (not "difference in differences",
"treatment", "exposure", "identification", "standard deviation", "regression", "instrument", "elasticity",
"significant", "quintile", "heterogeneity", "counterfactual", "endogenous", "causal"). Describe the comparison
in everyday words."""

URL = re.compile(r"\]\((https?://[^)\s]+|#[^)\s]+)\)")
NUM = re.compile(r"\d+(?:[.,]\d+)*")
LABEL = re.compile(r"^\s*(\*\*[^*]+\*\*|[-*]\s|\d+\.\s)")
PROTECT = ("#", "<", "{%", "{{", "{:", "![", "|")
usage = {"in": 0, "out": 0, "calls": 0}


def protected(block):
    s = block.lstrip()
    if s.startswith(PROTECT):
        return True
    words = re.sub(r"\[[^\]]*\]\([^)]*\)", " ", s)
    return len(re.findall(r"[A-Za-zÀ-ÿ]{2,}", words)) < 4      # link-only or near-empty lines


def line_key(line):
    m = LABEL.match(line)
    if m:
        return m.group(1).strip()
    m = re.match(r"^\s*([^:*\[\]]{2,40}):\s", line)               # "What it explores: ..."
    return m.group(1).strip().lower() if m else ""


def check(old, new, general):
    if not isinstance(new, str) or not new.strip():
        return "empty"
    if set(URL.findall(old)) != set(URL.findall(new)):
        return "links changed"
    if not set(NUM.findall(new)) <= set(NUM.findall(old)):
        return f"new number(s) {sorted(set(NUM.findall(new)) - set(NUM.findall(old)))}"
    ol, nl = old.strip().split("\n"), new.strip().split("\n")
    if len(ol) != len(nl) or [line_key(x) for x in ol] != [line_key(x) for x in nl]:
        return "lines or labels changed"
    if "—" in new or " -- " in new:
        return "em-dash"
    low = new.lower()
    bad = [w for w in BANNED if re.search(rf"\b{w}", low) and not re.search(rf"\b{w}", old.lower())]
    if general:
        bad += [w for w in TECH if w in low and w not in old.lower()]
    if bad:
        return f"banned/technical word(s) {bad}"
    if not 0.5 <= len(new) / max(len(old), 1) <= 1.6:
        return "length"
    return None


def gemini(paragraphs, general):
    key = os.environ["GEMINI_API_KEY"]
    body = {"systemInstruction": {"parts": [{"text": SYSTEM + (GENERAL if general else "")}]},
            "contents": [{"role": "user", "parts": [{"text": json.dumps(paragraphs, ensure_ascii=False)}]}],
            "generationConfig": {"responseMimeType": "application/json"}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type": "application/json", "x-goog-api-key": key})
    for attempt in range(3):                               # retry dropped connections and 5xx, not 4xx
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.load(r)
            break
        except urllib.error.HTTPError as e:
            if e.code < 500 or attempt == 2:
                raise
        except (OSError, http.client.HTTPException):
            if attempt == 2:
                raise
        time.sleep(5 * (attempt + 1))
    u = d.get("usageMetadata", {})
    usage["in"] += u.get("promptTokenCount", 0)
    usage["out"] += u.get("candidatesTokenCount", 0) + u.get("thoughtsTokenCount", 0)
    usage["calls"] += 1
    text = "".join(p.get("text", "") for p in d["candidates"][0]["content"]["parts"] if not p.get("thought"))
    out = json.loads(text)
    if not isinstance(out, list) or len(out) != len(paragraphs):
        raise ValueError("Gemini returned a different number of paragraphs")
    return out


def rewrite_text(text, general, keep_first=False, label=""):
    """Rewrite the prose paragraphs of a Markdown text; structure and failed paragraphs stay as they were."""
    blocks = re.split(r"(\n\s*\n)", text)               # keep the separators
    idx, first_seen = [], False
    for i, b in enumerate(blocks):
        if i % 2 or not b.strip():
            continue
        if keep_first and not first_seen and not b.lstrip().startswith(("#", "<!--")):
            first_seen = True                              # provenance line under an entry heading
            continue
        if not protected(b):
            idx.append(i)
    if not idx:
        return text, 0, 0
    try:
        new = gemini([blocks[i] for i in idx], general)
    except Exception as e:                                 # network, quota (402), bad JSON: keep everything
        print(f"::warning::{label}: Gemini failed ({e}); kept the routine's text")
        return text, 0, len(idx)
    done = 0
    for i, n in zip(idx, new):
        why = check(blocks[i], n, general)
        if why:
            print(f"{label}: kept original paragraph ({why}): {blocks[i][:70]!r}")
            continue
        lead = re.match(r"^\s*", blocks[i]).group(0)
        blocks[i] = lead + n.strip()
        done += 1
    return "".join(blocks), done, len(idx)


def split_front(raw):
    if raw.startswith("---"):
        _, head, body = raw.split("---", 2)
        return f"---{head}---", body
    return "", raw


def do_entries(path, lang, only_from):
    raw = open(path, encoding="utf-8").read()
    chunks = re.split(r"(?m)^(?=### )", raw)
    wanted = None
    if only_from:
        wanted = {e["anchor"] for e in parse_entries(open(only_from, encoding="utf-8").read(), "en")}
    tot = ok = 0
    for i, c in enumerate(chunks):
        if not c.startswith("### "):
            continue
        anchor = parse_entries(c, lang)[0]["anchor"]
        if wanted is not None and anchor not in wanted:
            continue
        chunks[i], d, n = rewrite_text(c, general=False, keep_first=True, label=f"{path}#{anchor[:40]}")
        ok += d; tot += n
    open(path, "w", encoding="utf-8").write("".join(chunks))
    return ok, tot


def do_page(path, general=True):
    front, body = split_front(open(path, encoding="utf-8").read())
    body, ok, tot = rewrite_text(body, general=general, label=path)
    open(path, "w", encoding="utf-8").write(front + body)
    return ok, tot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["entries", "briefs", "page"])
    ap.add_argument("path")
    ap.add_argument("--lang", default="en", choices=["en", "fr"])
    ap.add_argument("--kind", default="daily", choices=["daily", "weekly", "monthly"])
    ap.add_argument("--only-anchors-from")
    ap.add_argument("--date")
    a = ap.parse_args()
    if not os.environ.get("GEMINI_API_KEY"):
        print("no GEMINI_API_KEY: nothing rewritten"); return
    if not os.path.exists(a.path):
        print(f"{a.path}: missing, skipped"); return
    ok = tot = 0
    if a.mode == "entries":
        ok, tot = do_entries(a.path, a.lang, a.only_anchors_from)
    elif a.mode == "page":
        ok, tot = do_page(a.path)
    else:                                                   # the period's brief pages, as build_email.py picks them
        date = dt.date.fromisoformat(a.date) if a.date else dt.date.today()
        days = {"daily": 0, "weekly": 6, "monthly": 30}[a.kind]
        for fn in sorted(os.listdir(a.path)):
            m = re.match(r"(\d{4}-\d{2}-\d{2})\.md$", fn)
            if m and 0 <= (date - dt.date.fromisoformat(m.group(1))).days <= days:
                d, n = do_page(os.path.join(a.path, fn)); ok += d; tot += n
    pin, pout = (2.0, 10.0) if dt.date.today() < dt.date(2026, 12, 1) else (4.0, 20.0)
    cost = (usage["in"] * pin + usage["out"] * pout) / 1e6
    line = (f"Gemini ({MODEL}) rewrote {ok}/{tot} paragraphs in {a.path} [{a.lang}], {usage['calls']} call(s), "
            f"{usage['in']} in / {usage['out']} out tokens, about ${cost:.3f}")
    print(line)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8").write(f"- {line}\n")


if __name__ == "__main__":
    main()
