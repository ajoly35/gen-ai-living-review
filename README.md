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
