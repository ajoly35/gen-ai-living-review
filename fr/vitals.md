---
layout: default
lang: fr
alt: /vitals/
title: Signes vitaux de la recherche
permalink: /fr/vitals/
---

# Signes vitaux de la recherche
{:.no_toc}

<p class="byline">IA générative, emploi et croissance : une revue vivante · Adrien Joly, London School of Economics · Données au {{ site.data.vitals.as_of }}</p>

Où va la recherche sur l'IA générative, l'emploi et la croissance, lue dans les études de cette revue : combien il y en a, quels dispositifs elles utilisent, quelle réponse elles donnent, et ce qui s'ajoute. Chaque chiffre vient de la base de la revue, codée à partir des entrées de ce site, dans l'esprit d'[EconVitals](https://econvitals.org/) de Jason Furman pour l'économie américaine. La base est dans la source de la page (`_data/papers.yml`) et dans le tableau en bas.
{:.lead}

{% assign v = site.data.vitals %}
<div class="vitals vitals-grid">
{% for t in v.tiles.fr %}<div class="vital"><div class="vital-value">{{ t.value }}</div><div class="vital-label">{{ t.label }}</div><div class="vital-compare">{{ t.compare }}</div></div>
{% endfor %}
</div>

<section class="vitals" markdown="1">

## Où va le champ

<figure><img src="{{ '/assets/vitals/studies-by-year-fr.svg' | relative_url }}" alt="Études de la revue par trimestre de publication, empilées par thème."><figcaption>Études de la revue par année de la version citée, par thème. La première vague (2023-2024) est faite d'expériences de terrain et de théorie de la croissance ; les dispositifs d'exposition sur les embauches arrivent en 2025 ; les modèles de croissance et les études d'organisation dominent 2026. Beaucoup de références n'ont qu'une année, d'où un graphique annuel.</figcaption></figure>

<figure><img src="{{ '/assets/vitals/designs-fr.svg' | relative_url }}" alt="Nombre d'études par dispositif de recherche, selon qu'elles respectent ou non le standard causal de la revue."><figcaption>Dispositifs de recherche. En bleu : les études que la revue compte comme preuves causales. En gris : le contexte (travaux descriptifs, théorie, modèles calibrés, publications officielles).</figcaption></figure>

## Quelle réponse elles donnent

<figure><img src="{{ '/assets/vitals/direction-by-design-fr.svg' | relative_url }}" alt="Pour les études sur l'emploi, les embauches ou les salaires : sens de l'effet estimé de l'IA générative, par dispositif."><figcaption>Sens de la réponse sur le marché du travail, par dispositif. Orange : moins d'emplois, moins d'embauches ou salaires plus bas. Gris : pas d'effet significatif. Bleu : gains. Le partage suit le dispositif : les expériences mesurent la production par travailleur et trouvent des gains ; les dispositifs d'exposition mesurent les embauches et trouvent des baisses ; les dispositifs sur l'emploi total ne trouvent rien encore.</figcaption></figure>

## Ce qui s'ajoute

<figure><img src="{{ '/assets/vitals/added-by-week-fr.svg' | relative_url }}" alt="Entrées ajoutées à la revue vivante par mois, par thème."><figcaption>Articles ajoutés aux Articles récents par semaine depuis l'ouverture de la section en octobre 2026, par thème. Les entrées datées d'avant la mise en ligne sont comptées dans la semaine du 13 octobre.</figcaption></figure>

## Tableau de bord interactif

Le [tableau de bord interactif]({{ '/vitals-dashboard/' | relative_url }}) (en anglais seulement) couvre le même terrain à partir d'une seconde base codée indépendamment, de 97 sources : quatre tuiles, cinq constats rédigés, des graphiques des types de preuve et des thèmes par année, une carte thème × réponse, la chronologie du flux Articles récents et un tableau filtrable de toutes les sources. Les deux codages ont été confrontés : ils s'accordent sur le sens de chaque étude commune sur le marché du travail (une étude suisse a été recodée selon la revue : « jusqu'à 27 % de chômeurs en plus dans les professions exposées »). Ses données : `vitals-dashboard/field-ledger.csv`.

## La base

<details><summary>Les {{ v.n_studies }} études et {{ v.n_news }} articles de presse, une ligne chacun</summary>
<table>
<thead><tr><th>Étude</th><th>Date</th><th>Thème</th><th>Dispositif</th><th>Causal</th><th>Sens</th><th>Résultat phare</th></tr></thead>
<tbody>
{% assign ps = site.data.papers | sort: "date" | reverse %}
{% for p in ps %}<tr><td>{% if p.url %}<a href="{{ p.url }}">{% endif %}{{ p.authors }} ({{ p.year }})<br><span class="recent-note">{{ p.title }}</span>{% if p.url %}</a>{% endif %}</td><td>{{ p.date }}</td><td>{{ p.theme }}</td><td>{{ p.design }}</td><td>{% if p.causal %}oui{% else %}non{% endif %}</td><td>{{ p.direction }}</td><td>{{ p.magnitude }}</td></tr>
{% endfor %}
</tbody></table>
</details>

Règles de codage : une ligne par étude ; thème et dispositif tels que la revue les décrit ; « causal » suit l'étiquette de la revue ; « sens » est le signe de l'effet estimé de l'IA générative sur le principal résultat de travail de l'étude (négatif : moins d'emplois, d'embauches ou de salaire). Les graphiques sont refaits avec `scripts/make_vitals.py` quand la base change. Corrections : a.p.joly@lse.ac.uk.

</section>
