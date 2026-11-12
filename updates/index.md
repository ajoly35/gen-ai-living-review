---
layout: default
lang: en
alt: /fr/updates/
title: Monthly update
permalink: /updates/
---

# Monthly review update
{:.no_toc}

Once a month, the papers added to the living review are read again against the review as it stands, to answer two questions: **what truly deserves to enter the review**, and **does it change the overall picture**? Each update gives a verdict per study (add, mention, watch, not added), a status for each of the review's main ideas (holds, strengthened, nuanced, challenged), and the exact changes proposed to the text. Drafted by an AI assistant, then read and approved by Adrien Joly before it is published and sent. [Get it by email]({{ '/subscribe/' | relative_url }}) (choose "monthly").
{:.lead}

<ul class="emails">
{% assign us = site.pages | sort: "date" | reverse %}
{% for u in us %}{% if u.period and u.lang == "en" %}<li><a href="{{ u.url | relative_url }}">{{ u.title | remove: "Review update: " }}</a> · <strong>{{ u.verdict }}</strong>{% if u.adds %} · {{ u.adds }} added to the review{% endif %}</li>
{% endif %}{% endfor %}
</ul>

How studies are judged: [method]({{ '/updates/method/' | relative_url }}).
