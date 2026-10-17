# Gen-AI, Jobs and Growth: A Living Review

Source of the public page at https://ajoly35.github.io/gen-ai-living-review/ (GitHub Pages, Jekyll).

| File | What it holds | Who edits it |
|---|---|---|
| `_includes/latest.md` | Latest research entries, newest first | weekly routine |
| `_includes/references-latest.md` | references for those entries, alphabetical | weekly routine |
| `_includes/review.md`, `_includes/references-review.md` | the review body, built from the LaTeX draft | `scripts/build_review.py` only |

Rebuild the body after editing the review in Overleaf:

    python3 -I scripts/build_review.py path/to/review.tex path/to/references.bib

The script drops material that is not for circulation (`PUBLIC_EDITS`, `EXCLUDE_KEYS`) and stops if an excluded paper is still cited.

## Updates by email and paper submissions

- Each push that adds entries to `_includes/latest.md` publishes a GitHub Release with the new entries (`.github/workflows/release-notes.yml`). To get them by email: Watch → Custom → Releases.
- Submit a paper: https://github.com/ajoly35/gen-ai-living-review/issues/new?template=paper.yml (link, optional PDF). Only submissions opened by the repository owner are processed.
