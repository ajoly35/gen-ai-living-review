---
layout: default
lang: en
alt: /fr/vitals/
title: Research vitals
permalink: /vitals/
---

# Research vitals
{:.no_toc}

<p class="byline">Gen-AI, Jobs and Growth: A Living Review · Adrien Joly, London School of Economics · Dataset as of {{ site.data.vitals.as_of }}</p>

Where the research on generative AI, jobs and growth is heading, read off the studies in this review: how many there are, what designs they use, what answer they give, and what has been added lately. Every figure comes from the review's own dataset of studies, coded from the entries on this site, in the spirit of Jason Furman's [EconVitals](https://econvitals.org/) for the US economy. The dataset is in the page source (`_data/papers.yml`) and the table at the bottom.
{:.lead}

{% assign v = site.data.vitals %}
<div class="vitals vitals-grid">
{% for t in v.tiles.en %}<div class="vital"><div class="vital-value">{{ t.value }}</div><div class="vital-label">{{ t.label }}</div><div class="vital-compare">{{ t.compare }}</div></div>
{% endfor %}
</div>

<section class="vitals" markdown="1">

## Where the field is heading

<figure><img src="{{ '/assets/vitals/studies-by-year-en.svg' | relative_url }}" alt="Studies in the review by quarter of release, stacked by theme: employment and hiring, wages, growth and productivity, organisation and adoption, other."><figcaption>Studies in the review by year of the version cited, by theme. The first wave (2023 to 2024) is field experiments and growth theory; exposure designs on hiring arrive in 2025; growth models and organisation studies dominate 2026. Many references carry a year only, so the chart is yearly.</figcaption></figure>

<figure><img src="{{ '/assets/vitals/designs-en.svg' | relative_url }}" alt="Number of studies by research design, split between those meeting the review's causal standard and context pieces."><figcaption>Research designs. Blue: studies the review counts as causal evidence. Grey: context (descriptive work, theory, calibrated models, official releases).</figcaption></figure>

## What answer they give

<figure><img src="{{ '/assets/vitals/direction-by-design-en.svg' | relative_url }}" alt="For studies on employment, hiring or wages: the direction of the estimated effect of generative AI, by research design."><figcaption>Direction of the labour-market answer, by design. Orange: fewer jobs, fewer hires or lower pay. Grey: no significant effect. Blue: gains. The split follows the design: experiments measure output per worker and find gains; exposure designs measure hiring and find falls; total-employment designs find nothing yet.</figcaption></figure>

## What is being added

<figure><img src="{{ '/assets/vitals/added-by-week-en.svg' | relative_url }}" alt="Entries added to the living review by month, by theme."><figcaption>Papers added to Latest research by week since the section opened in October 2026, by theme. Entries dated before the site went live are counted in the week of 13 October.</figcaption></figure>

## Interactive dashboard

The [interactive dashboard]({{ '/vitals-dashboard/' | relative_url }}) (English only) covers the same ground from a second, independently coded ledger of 97 sources: four summary tiles, five written findings, charts of evidence and themes by year, a theme-by-answer heatmap, the timeline of the Latest research stream, and a filterable table of every source. The two codings were cross-checked: they agree on the direction of every shared labour-market study (one Swiss study was recoded to the review's "up to 27% more unemployed job seekers in exposed occupations"). Its data: `vitals-dashboard/field-ledger.csv`.

## The dataset

<details><summary>All {{ v.n_studies }} studies and {{ v.n_news }} news items, one line each</summary>
<table>
<thead><tr><th>Study</th><th>Date</th><th>Theme</th><th>Design</th><th>Causal</th><th>Direction</th><th>Headline</th></tr></thead>
<tbody>
{% assign ps = site.data.papers | sort: "date" | reverse %}
{% for p in ps %}<tr><td>{% if p.url %}<a href="{{ p.url }}">{% endif %}{{ p.authors }} ({{ p.year }})<br><span class="recent-note">{{ p.title }}</span>{% if p.url %}</a>{% endif %}</td><td>{{ p.date }}</td><td>{{ p.theme }}</td><td>{{ p.design }}</td><td>{% if p.causal %}yes{% else %}no{% endif %}</td><td>{{ p.direction }}</td><td>{{ p.magnitude }}</td></tr>
{% endfor %}
</tbody></table>
</details>

Coding rules: one line per study; theme and design as the review describes them; "causal" follows the review's own label; "direction" is the sign of the estimated effect of generative AI on the study's main labour outcome (negative: fewer jobs, hires or lower pay). Charts are rebuilt with `scripts/make_vitals.py` when the dataset changes. Corrections: a.p.joly@lse.ac.uk.

</section>
