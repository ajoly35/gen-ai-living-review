---
layout: default
lang: en
title: Past emails
permalink: /emails/
---

# Past emails
{:.no_toc}

Every email sent to subscribers, newest first, as HTML (open in a browser, print to PDF), as Markdown to paste into a newsletter, and as plain text. Built by the email workflow from the entries added that day, week or month.
{:.lead}

{% assign files = site.static_files | where_exp: "f", "f.path contains '/emails/'" | sort: "path" | reverse %}
<ul class="emails">
{% for f in files %}{% if f.extname == ".html" %}{% assign stem = f.basename %}<li><a href="{{ f.path | relative_url }}">{{ stem }}</a> · <a href="{{ f.path | replace: '.html', '.paste.txt' | relative_url }}">Markdown (paste into Substack)</a> · <a href="{{ f.path | replace: '.html', '.txt' | relative_url }}">text</a></li>
{% endif %}{% endfor %}
</ul>
