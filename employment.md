---
layout: default
lang: en
title: Employment
permalink: /employment/
---

# Generative AI and employment
{:.no_toc}

<p class="byline">Gen-AI, Jobs and Growth: A Living Review · Adrien Joly, London School of Economics</p>

What generative AI has done so far to employment, hiring, hours and wages, from the causal studies since 2023, with heterogeneity by experience and age. This page sums up the review's findings on the topic and lets you sign up for new papers on it.
{:.lead}

<p class="cta-row"><a class="btn btn-primary" href="#signup">Get new employment papers by email</a> <a class="btn btn-secondary" href="{{ '/#applied-micro-evidence' | relative_url }}">Read the review</a></p>

## What the review finds

- **Fewer hires, not layoffs.** Exposed occupations and adopting firms cut junior hiring while the stock of jobs barely moves; within Swedish employers, employment of 22 to 25 year olds in highly exposed occupations was 5.5% lower by early 2025 than in less exposed ones. Section [“Exposure designs: hiring and entry”]({{ '/#exposure-designs-hiring-and-entry' | relative_url }}).
- **Novices gain most inside the firm.** In field experiments the least experienced workers gain the largest share of output, which is why the fall in junior hiring is a puzzle the theory section resolves. Section [“Field experiments”]({{ '/#field-experiments' | relative_url }}) and [“Why these patterns: theory”]({{ '/#why-these-patterns-theory' | relative_url }}).
- **Wages move less than hours.** Exposure lowers relative wages only where supply, not demand, moves pay. Section [“Exposure designs: wages”]({{ '/#exposure-designs-wages' | relative_url }}).
- **Who decides matters.** Management practices and reorganisation, not access to the tool, set how deeply firms use AI. Section [“Organisation: who decides how AI is used”]({{ '/#organisation-who-decides-how-ai-is-used' | relative_url }}).

The one-line summary, with each parameter's status, is in [Main patterns]({{ '/#main-patterns' | relative_url }}).



## Added recently on this topic

{% assign emp = site.data.recent.employment %}
<ul class="recent">
{% for e in emp %}<li><a href="{{ '/#' | append: e.anchor | relative_url }}">{{ e.title }}</a> <span class="recent-note">{{ e.note }}</span></li>
{% endfor %}
</ul>

{% include signup.html topic="employment" %}
