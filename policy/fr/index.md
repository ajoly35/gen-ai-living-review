---
layout: default
lang: fr
alt: /policy/
title: Brief politiques publiques
permalink: /fr/policy/
---

# IA et travail : le brief politiques publiques
{:.no_toc}

Ce qui est fait, et ce qui pourrait l'être, face aux effets de l'IA sur l'emploi : orientation des élèves et des étudiants, soutien aux jeunes sans emploi, formation, embauche. Chaque brief s'ouvre sur les chiffres officiels du chômage en France, au Royaume-Uni et aux États-Unis, et sur deux indicateurs de l'IA au travail. Écrit par un assistant IA à partir de sources officielles lues le jour même, sans relecture avant publication. [Le recevoir par courriel]({{ '/fr/subscribe/' | relative_url }}).
{:.lead}

## Les chiffres du jour

{% include employment-table-fr.md %}

## Tous les briefs

<ul class="emails">
{% assign bs = site.pages | sort: "date" | reverse %}
{% for b in bs %}{% if b.date and b.lang == "fr" and b.permalink contains "/policy/" %}<li><a href="{{ b.url | relative_url }}">{{ b.date | date: "%-d %B %Y" }}</a> · {{ b.headline }}</li>
{% endif %}{% endfor %}
</ul>
