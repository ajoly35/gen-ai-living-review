---
layout: default
lang: fr
alt: /briefs/
title: Briefs
permalink: /fr/briefs/
---

# IA et travail, en bref
{:.no_toc}

Le brief quotidien pour les lecteurs qui ne sont pas économistes : ce qui est nouveau, comment cela s'assemble avec ce que l'on sait déjà, une idée d'un article clé expliquée en mots de tous les jours, et un graphique. Écrit chaque matin par un assistant IA à partir d'articles vérifiés sur leur texte intégral, sans relecture avant publication. [Le recevoir par courriel]({{ '/fr/subscribe/' | relative_url }}).
{:.lead}

<ul class="emails">
{% assign bs = site.pages | where_exp: "p", "p.permalink contains '/fr/briefs/' and p.date" | sort: "date" | reverse %}
{% for b in bs %}<li><a href="{{ b.url | relative_url }}">{{ b.date | date: "%-d %B %Y" }}</a> · {{ b.title | remove: "IA et travail, en bref : " }}</li>
{% endfor %}
</ul>
