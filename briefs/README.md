# Daily briefs (general audience)

One file a day, `briefs/YYYY-MM-DD.md` (English) and `briefs/fr/YYYY-MM-DD.md` (French), written by the morning routine.
Each is a Jekyll page (`/briefs/YYYY-MM-DD/`, `/fr/briefs/YYYY-MM-DD/`) and the body of that day's general-audience email
(`scripts/build_email.py --audience general --brief briefs/YYYY-MM-DD.md`). The weekly and monthly general digests stitch the
period's briefs together. `concepts.yml` is the rotation of ideas for the "One idea, explained" section.

Shape (keep the headings; the builder and the pages rely on them):
1. Front matter: layout, lang, alt, title "AI and work, in brief: D Month YYYY", permalink, date, concept key.
2. `# AI and work, in brief` + byline.
3. `## Today in three lines` (3 bullets).
4. `## New research, in plain words`: one `###` per new paper (its headline as a sentence), then **What it explores.**,
   **Why it matters.**, **How it fits the evidence.**, then links to the full entry and the paper.
5. `## How it fits together` (2 or 3 paragraphs tying the day's papers to the review's main ideas).
6. `## One idea, explained: <title>` (150 to 250 words, one everyday analogy, from the paper named in concepts.yml).
7. `## Where the evidence stands` (the direction-by-design chart and a one-paragraph reading that places today's papers).
8. `## Read more`.
No technical vocabulary anywhere in a brief: not "difference in differences", "treatment", "exposure", "identification",
"standard deviation", "regression", "instrument", "elasticity", "significant", "quintile", "heterogeneity", "counterfactual",
"endogenous", "causal". Say what was compared with what, in words.
