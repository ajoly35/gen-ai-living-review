---
layout: default
lang: en
title: Productivity
permalink: /productivity/
---

# Productivity
{:.no_toc}

<p class="byline">Companion page to the productivity chapter · Adrien Joly, London School of Economics · Figures update with EconVitals</p>

A reader's page for the productivity chapter: the terms the chapter uses, the current US record for each of them, and the recent papers on whether AI is moving them. Sign up below for new papers on productivity.
{:.lead}

<p class="cta-row"><a class="btn btn-primary" href="#signup">Get new productivity papers by email</a> <a class="btn btn-secondary" href="#indicators">Current figures</a></p>

## The terms, as the chapter uses them

- **Labour productivity** is output per hour worked. The US series below is for the nonfarm business sector, reported by the Bureau of Labor Statistics each quarter at an annual rate.
- **Total factor productivity (TFP)** is output per unit of all inputs, labour and capital together. Hulten's theorem says that, to a first approximation, a cost saving on some tasks raises TFP by their share of GDP times that saving. The aggregation studies in the growth review apply exactly this formula.
- **Unit labour costs** are compensation per hour divided by output per hour. When pay grows faster than productivity, unit labour costs rise, and the difference goes to prices or to the labour share.
- **Weak links.** When tasks are complements (an elasticity of substitution below one), output is held back by the tasks that improve most slowly, and spending shifts towards them. This is Baumol's cost disease and the reason task gains do not add up one for one.

## What the data show so far

AI raises output strongly on single tasks, much less on whole products, and not yet visibly in aggregate. Against randomised control groups, ChatGPT cut the time US professionals took on writing tasks by 40%, GitHub Copilot let programmers finish a coding task 55.8% faster, and customer support agents given an AI assistant resolved 14% more issues per hour. Across more than 500,000 GitHub developers, coding agents raised saved code changes by 240% but software releases by only 30%: review and release are the weak links. Executives perceive larger gains than revenues show, and financial markets price in more still. Sources and page references are in the growth review's section "What the data show so far".

{% include econvitals.html topic="productivity" %}

Outside the United States: the ONS [labour productivity release](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/labourproductivity/bulletins/labourproductivity/latest), the Bank of England's [Monetary Policy Report](https://www.bankofengland.co.uk/monetary-policy-report/2026/november-2026) (AI and UK productivity, November 2026) and the OECD [Productivity Statistics](https://www.oecd.org/en/data/datasets/productivity-statistics.html).

## Added recently on this topic

{% assign pr = site.data.recent.productivity %}
<ul class="recent">
{% for e in pr %}<li><a href="{{ '/#' | append: e.anchor | relative_url }}">{{ e.title }}</a> <span class="recent-note">{{ e.note }}</span></li>
{% endfor %}
</ul>

{% include signup.html topic="productivity" %}
