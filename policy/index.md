---
layout: default
lang: en
alt: /fr/policy/
title: Policy brief
permalink: /policy/
---

# AI and work: the policy brief
{:.no_toc}

What is being done, and what could be done, about the effects of AI on jobs: guidance for pupils and students, support for young people out of work, training, hiring. Each brief opens with the official unemployment figures for France, the United Kingdom and the United States, and two trackers of AI at work. Written by an AI assistant from official sources read that day, not reviewed before it appears. [Get it by email]({{ '/subscribe/' | relative_url }}).
{:.lead}

## The numbers today

{% include employment-table-en.md %}

## All policy briefs

<ul class="emails">
{% assign bs = site.pages | sort: "date" | reverse %}
{% for b in bs %}{% if b.date and b.lang == "en" and b.permalink contains "/policy/" %}<li><a href="{{ b.url | relative_url }}">{{ b.date | date: "%-d %B %Y" }}</a> · {{ b.headline }}</li>
{% endif %}{% endfor %}
</ul>
