---
layout: default
lang: en
title: Growth
permalink: /growth/
---

# AI and economic growth
{:.no_toc}

<p class="byline">Gen-AI, Jobs and Growth: A Living Review · Adrien Joly, London School of Economics · Figures update with EconVitals</p>

How AI could change the level and growth rate of output: the aggregation of measured task gains, the growth models in which AI automates goods and then ideas, and what GDP misses. This page pairs the companion growth review with the US investment and output series the scenarios run through, and lets you sign up for new papers on this topic.
{:.lead}

<p class="cta-row"><a class="btn btn-primary" href="#signup">Get new growth papers by email</a> <a class="btn btn-secondary" href="{{ '/#latest-research' | relative_url }}">Latest research</a></p>

## What the growth review finds

- **Single tasks, not yet aggregates.** AI cuts the time taken on individual tasks by 14% to 56% in randomised and staged roll-outs, much less on whole products, and not yet visibly in aggregate productivity. Human review and release become the weak links.
- **Next decade: tenths of a point.** Studies that add up measured task gains expect AI to add 0.06 to 0.7 percentage points a year to US total factor productivity growth over ten years; the gap comes from their inputs (exposure share, profitable share, cost saving). Past general purpose technologies added 0.8 to 1.3 points a year for a decade, with a long lag.
- **Acceleration needs capital or ideas.** Growth accelerates in the models only if the tasks that resist automation stop binding, through optimal saving or through automated research. Whether that happens is the main debate.
- **GDP misses part of it.** Free digital services, reorganisation costs and who owns the machines all sit outside measured output.

The growth review is a companion to the employment review and is referenced from the [Latest research]({{ '/#latest-research' | relative_url }}) entries marked "companion review".

{% include econvitals.html topic="growth" %}

Outside the United States: the Bank of England's [Monetary Policy Report](https://www.bankofengland.co.uk/monetary-policy-report/2026/november-2026), the ONS [GDP monthly estimate](https://www.ons.gov.uk/economy/grossdomesticproductgdp/bulletins/gdpmonthlyestimateuk/latest) and Eurostat's [GDP flash estimate](https://ec.europa.eu/eurostat/web/euro-indicators/national-accounts).

## Added recently on this topic

{% assign gr = site.data.recent.growth %}
<ul class="recent">
{% for e in gr %}<li><a href="{{ '/#' | append: e.anchor | relative_url }}">{{ e.title }}</a> <span class="recent-note">{{ e.note }}</span></li>
{% endfor %}
</ul>

{% include signup.html topic="growth" %}
