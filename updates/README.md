# Monthly review updates

One page a month, `updates/YYYY-MM.md` (English) and `updates/fr/YYYY-MM.md` (French), drafted by the monthly
routine on the 1st, covering the previous calendar month. Pages: `/updates/YYYY-MM/`, `/fr/updates/YYYY-MM/`.

Why it exists (Xavier, 12 Nov 2026): the daily entries are too many to follow. Once a month, re-read what was
added and answer two questions only:
1. **What truly deserves to enter the main review?**
2. **Does it change our narrative or vision?**

## Workflow (approval gate)
1. 1st of the month, ~05:00 UTC: the routine writes both pages on a branch `update/YYYY-MM` and opens a pull
   request. It never pushes to `main` and never edits `_includes/review.md` or `main-ideas.md`.
2. Adrien reads the PR, edits if needed, and merges. **Merging is the approval.**
3. The merge triggers `.github/workflows/email.yml`: the monthly email (general and academic, EN and FR) is built
   from the update page and sent to monthly subscribers.
4. The "Proposed changes" are applied to the review (LaTeX draft, then `scripts/build_review.py`) in a separate
   step, only those Adrien keeps.
5. Fallback: if no update is merged by the 5th, the old entries digest goes out on the 5th.

## Verdicts: what "truly deserves to enter" means
A study is read against the review as it stands. Verdicts, at most **3 "Add"** a month:

| Verdict | Test (all must hold for Add) |
|---|---|
| **Add** | (a) meets the evidence standard: causal design, 2023 onwards, full text read; and (b) at least one of: changes the sign or size of a result the review states (by more than a third); first evidence for a country, population, outcome or design the review lacks; a cleaner or larger design than the study the review cites for the same claim; resolves an item the review lists as debated or unknown. |
| **Mention** | Meets the standard but only confirms an existing claim with a similar design: one clause or a grouped citation, no new paragraph. Theory papers and reviews of the evidence can earn Mention (never Add) when they sharpen a mechanism the review already uses (as Garicano and Rayo, or Imas and Schaal, do). |
| **Watch** | On the review's outcomes (employment, hiring, hours, wages) but not there yet: descriptive, preliminary, no full text, or one result awaiting replication. Re-read next month. |
| **Not added** | Off topic for the review (growth only, news), descriptive work not on its outcomes, or below the standard. Listed so the reader sees it was read; may be grouped by reason. |

## Narrative check: does it change the picture?
One row per Main idea, in the order of `_includes/main-ideas.md`. Status, one word:

| Status | Meaning |
|---|---|
| **Holds** | Nothing this month bears on it, or only Mention-level confirmation. |
| **Strengthened** | An Add-level study confirms it with a new country, design or outcome. |
| **Nuanced** | A study narrows it (holds for some groups, settings or periods, not others): the sentence needs a qualifier. |
| **Challenged** | An Add-level study contradicts it: the sentence needs rewriting, or the idea moves to "debated". |

The overall verdict (top of the page) is one of: **No change to the narrative**, **Narrative nuanced**,
**Narrative revised**. "Revised" only when at least one Main idea is Challenged.

## Page shape (keep the headings; the email builder relies on them)
1. Front matter: layout, lang, alt, title "Review update: Month YYYY", permalink, date (the day it is drafted),
   period ("YYYY-MM"), verdict (one of the three above), adds (number of Add).
2. `# Review update: Month YYYY` + a plain `<p class="byline">` line. No Liquid anywhere and absolute URLs only:
   the same file is the email body.
3. `## The month in one paragraph`: the overall verdict in bold first, then at most 120 words.
4. `## Does it change the picture?`: the Main ideas table (Main idea | Status | Why, at most 40 words | Studies).
5. `## What enters the review`: table (Study | Verdict | Where in the review | Why, at most 35 words), Add first.
6. `## Proposed changes to the review`: for each Add or Nuanced/Challenged idea, the exact sentence now and the
   proposed sentence, with the section it sits in. "None" is a valid section.
7. `## To watch`: Watch studies and open debates that moved, at most 5 bullets.
8. `## Studies read this month`: every entry added in the period, one line each, linking to the paper.
At most 900 words of prose before the last section (tables and URLs not counted). French page: same headings in French (`## Le mois en un
paragraphe`, `## Est-ce que cela change le tableau ?`, `## Ce qui entre dans la revue`, `## Modifications
proposées`, `## À suivre`, `## Études lues ce mois-ci`), same tables, same links.
