# Daily policy brief

One file a day, `policy/YYYY-MM-DD.md` (English) and `policy/fr/YYYY-MM-DD.md` (French). Each is a Jekyll page
(`/policy/YYYY-MM-DD/`, `/fr/policy/YYYY-MM-DD/`) and the body of that day's policy email
(`scripts/build_email.py --audience policy --brief-dir policy`, sent to the tags `daily-policy` and `daily-policy-fr`
by `.github/workflows/policy-email.yml`). Fact briefs and Gemini drafts of hand-written issues: `policy/_briefs/`
(not published). Routine prompt: `../routines/policy-daily-routine.md` (project folder).

Why it exists (Adrien, 17 Nov 2026): readers are getting anxious about what AI does to jobs. The brief and the
digest say what the research finds; this edition says what is being done and what could be done: pupil and student
guidance, support for young people out of work, training, hiring incentives, reporting rules.

## The numbers
`scripts/fetch_trackers.py` reads, with no key, INSEE (France), ONS (United Kingdom) and BLS (United States) for the
unemployment rate of all ages and of young people, the GenAI Adoption Tracker of Bick, Blandin and Deming (share of
employed US adults using generative AI for work) and the LIFT job postings tracker (France). It writes
`_data/employment.json` and the block `_includes/employment-table-en.md` / `-fr.md`. `.github/workflows/trackers.yml`
runs it every morning. A source that cannot be read keeps its last figures; nothing is estimated. The page includes
the block with `{% include employment-table-en.md %}`; the email builder inlines the same file.
Never type a tracker figure by hand in a page: quote it from `_data/employment.json`.

## Shape (keep the headings; the builder and the pages rely on them)
1. Front matter: layout, lang, alt, title "AI and work, the policy brief: D Month YYYY", headline (at most 70 characters,
   shown in the list of briefs), permalink, date.
2. `# AI and work: the policy brief` + byline.
3. `## Today in three lines` (3 bullets).
4. `## The numbers`: the include line alone, then one paragraph reading the table (what moved, compared with a year
   earlier, and what the table cannot show).
5. `## What governments are doing`: one `###` per measure or proposal (a sentence, with the country), then
   **What it is.**, **Who it reaches.**, **What the evidence says.**, then the source links. One to three items.
6. `## What could be done`: one or two `###` options, each **The problem.**, **The option.**, **What we do not know.**
   Options are described, with who proposes them and what the review's evidence implies; the brief does not campaign.
7. `## Read more`.

## Rules
- Every measure comes from a primary source read that day (government page, bill text, official release, central
  bank or statistical office note) or, failing that, a named news agency report; the link is in the item. State
  whether it is announced, funded, voted or in force, and the date. Nothing from memory or from a search snippet.
- A measure not designed around AI (most youth employment plans) is described as such.
- Evidence sentences come from the review (`_includes/review.md`, `_includes/latest.md`, `_data/papers.yml`), with
  the comparison group and date of each number.
- No technical vocabulary (same list as `briefs/README.md`), no em-dashes.
- 450 to 650 words without the numbers block.
- No email on a day with nothing new: the routine writes a page only when there is a new measure, a new official
  release in the table, or a new study with a direct policy implication.
