---
layout: default
lang: en
title: Productivity
permalink: /productivity/
---

# Productivity
{:.no_toc}

<p class="byline">Companion page to the productivity chapter · Adrien Joly, London School of Economics</p>

A reader's page for the productivity chapter: the terms the chapter uses and the recent papers on whether AI is moving them. Everything on this page is built from trackers of publicly available data and published papers. Sign up below for new papers on productivity.
{:.lead}

<p class="cta-row"><a class="btn btn-primary" href="#signup">Get new productivity papers by email</a> <a class="btn btn-secondary" href="{{ '/vitals/' | relative_url }}">Direction of the field</a></p>

## The terms, as the chapter uses them

- **Labour productivity** is output per hour worked. In the United States the series is for the nonfarm business sector, reported by the Bureau of Labor Statistics each quarter at an annual rate.
- **Total factor productivity (TFP)** is output per unit of all inputs, labour and capital together. Hulten's theorem says that, to a first approximation, a cost saving on some tasks raises TFP by their share of GDP times that saving. The aggregation studies in the growth review apply exactly this formula.
- **Unit labour costs** are compensation per hour divided by output per hour. When pay grows faster than productivity, unit labour costs rise, and the difference goes to prices or to the labour share.
- **Weak links.** When tasks are complements (an elasticity of substitution below one), output is held back by the tasks that improve most slowly, and spending shifts towards them. This is Baumol's cost disease and the reason task gains do not add up one for one.

## What the data show so far

AI raises output strongly on single tasks, much less on whole products, and not yet visibly in aggregate. Against randomised control groups, ChatGPT cut the time US professionals took on writing tasks by 40%, GitHub Copilot let programmers finish a coding task 55.8% faster, and customer support agents given an AI assistant resolved 14% more issues per hour. Across more than 500,000 GitHub developers, coding agents raised saved code changes by 240% but software releases by only 30%: review and release are the weak links. Executives perceive larger gains than revenues show, and financial markets price in more still. Sources and page references are in the growth review's section "What the data show so far".

## Evidence from the demand side

The table and two charts below are built from trackers of publicly available data and published papers; the table is updated automatically. They check one claim each month: firms that adopt AI or automation raise their employment, because the demand effect (cheaper, better products sell more) outweighs the replacement of tasks. Before generative AI, most causal firm-level studies support it, with adopters growing sales and employment in France (Aghion et al. 2025, semi-elasticity of about 0.05 after a few years), the United States (Babina et al. 2024, +18.1% employment over eight years per standard deviation of AI investment) and Finland (Hirvonen et al. 2025, +23% after robot and machine grants). These firms grow mostly by expanding and launching products; Babina et al. (2024) and Hirvonen et al. (2025) find no rise in measured productivity, and firm comparisons miss business taken from non-adopting rivals.

For generative AI, the first results are mixed. Adopters hire fewer juniors, with about 8% lower junior employment after eight quarters in the United States (Hosseini and Lichtinger 2025) and 17% to 25% fewer young permanent hires in France (Bergeaud et al. 2026, descriptive), while total employment ranges from about 11% below trend in Denmark (Bonin et al. 2026) to +10% among the top third of US AI spenders (Kharazian et al. 2026). Below, new studies are added monthly and classed "supports" (adopters grow employment), "mixed" or "contradicts", with their causal or descriptive design and an automatic count; two charts show French firm employment and young hires around adoption (Aghion et al. 2025; Bergeaud et al. 2026), and French hourly productivity relative to the US and Germany, composition-adjusted to 2019 (Guadalupe et al. 2022) and OECD unadjusted to 2025. Taking the claim to hold when most causal studies support it, it holds for earlier AI and automation, not yet for generative AI.

{% assign ds = site.data.demand_side %}{% assign gens = "pre-genai,genai" | split: "," %}
{% for gen in gens %}{% assign c = ds | where: "generation", gen | where: "design", "causal" %}{% assign s = c | where: "class", "supports" %}{% assign m = c | where: "class", "mixed" %}{% assign x = c | where: "class", "contradicts" %}
- **{% if gen == "genai" %}Generative AI{% else %}Earlier AI and automation{% endif %}:** {{ c.size }} causal studies, {{ s.size }} support, {{ m.size }} mixed, {{ x.size }} contradict. The claim {% assign half = c.size | divided_by: 2 %}{% if s.size > half %}**holds**{% else %}**does not hold yet**{% endif %}.{% endfor %}

<figure><img src="{{ '/assets/productivity/firm-ai-adoption-employment-en.png' | relative_url }}" alt="Left: employment and sales of French firms that adopted AI between 2017 and 2020, relative to non-adopters, 2014 to 2022. Right: hires of 21 to 29 year olds on permanent contracts at intensive generative-AI users in France, relative to other firms, 2021 to 2026."><figcaption>Firm employment around AI adoption in France. Left, earlier AI: adopters' employment rises by about 5% relative to non-adopters after adoption (Aghion et al. 2025, Figure 2, values extracted from the published figure). Right, generative AI: intensive users hire fewer young workers on permanent contracts from 2023 (Bergeaud et al. 2026, Figure 5, values read off the figure, precision about 0.01; descriptive). Bars are 95% confidence intervals. <a href="{{ '/assets/productivity/data/graph63_aghion2025_fig2.csv' | relative_url }}">Data, left</a> · <a href="{{ '/assets/productivity/data/graph63_lift2026_fig5_21-29ans.csv' | relative_url }}">data, right</a>.</figcaption></figure>

<figure><img src="{{ '/assets/productivity/france-relative-hourly-productivity-en.png' | relative_url }}" alt="French hourly labour productivity relative to the United States and Germany. Left: adjusted for employment composition, 2003 to 2019. Right: OECD, unadjusted, 2003 to 2025."><figcaption>French hourly productivity relative to the United States (solid) and Germany (dashed). Left: adjusted for employment composition, 2003 to 2019 (Guadalupe, Jaravel, Philippon and Sraer 2022, CAE Note 75, Figure 1). Right: OECD GDP per hour worked at constant 2020 PPP, not adjusted, 2003 to 2025. Same direction, different levels: without the adjustment France falls below the United States only in 2023. The two series should not be joined. <a href="{{ '/assets/productivity/data/graph64_guadalupe2022_cae75.csv' | relative_url }}">Data, left</a> · <a href="{{ '/assets/productivity/data/graph64_oecd_2003-2025.csv' | relative_url }}">data, right</a>.</figcaption></figure>

| Study | Country, period | AI | Design | Finding | Reading |
|---|---|---|---|---|---|
{% for e in ds %}| {% if e.url != "" %}[{{ e.citation }}]({{ e.url }}){% else %}{{ e.citation }}{% endif %} | {{ e.country }}, {{ e.period }} | {% if e.generation == "genai" %}Generative{% else %}Earlier{% endif %} | {{ e.design | capitalize }} | {{ e.finding }} | {{ e.class | capitalize }} |
{% endfor %}



## Added recently on this topic

{% assign pr = site.data.recent.productivity %}
<ul class="recent">
{% for e in pr %}<li><a href="{{ '/#' | append: e.anchor | relative_url }}">{{ e.title }}</a> <span class="recent-note">{{ e.note }}</span></li>
{% endfor %}
</ul>

{% include signup.html topic="productivity" %}
