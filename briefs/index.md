---
layout: default
lang: en
alt: /fr/briefs/
title: Briefs
permalink: /briefs/
---

# AI and work, in brief
{:.no_toc}

The daily brief for readers who are not economists: what is new, how it fits with what we already know, one idea from a key paper explained in everyday words, and one chart. Written each morning by an AI assistant from papers checked against their full text, not reviewed before it appears. [Get it by email]({{ '/subscribe/' | relative_url }}).
{:.lead}

<ul class="emails">
{% assign bs = site.pages | sort: "date" | reverse %}
{% for b in bs %}{% if b.date and b.lang == "en" and b.permalink contains "/briefs/" %}<li><a href="{{ b.url | relative_url }}">{{ b.date | date: "%-d %B %Y" }}</a> · {{ b.title | remove: "AI and work, in brief: " }}{% if b.concept %} · <span class="recent-note">idea: {{ b.concept | replace: "-", " " }}</span>{% endif %}</li>
{% endif %}{% endfor %}
</ul>
