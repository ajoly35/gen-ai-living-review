---
layout: default
lang: fr
title: "Chapitre 6, la productivité : veille de mise à jour"
permalink: /manuel/chapitre-6/
noindex: true
description: "Passages du chapitre 6 susceptibles d'évoluer, données récentes et brouillons de mise à jour, actualisés automatiquement."
---

# Chapitre 6, la productivité : veille de mise à jour
{:.no_toc}

<p class="byline">Document de travail · Adrien Joly, London School of Economics · données au {{ site.data.manuel_ch6_charts.maj_le | date: "%d/%m/%Y" }}</p>

Cette page recense les passages du chapitre 6 consacré à la productivité susceptibles d'évoluer d'ici la prochaine édition, et propose de nouvelles sections, notamment sur la diffusion de l'IA en France. Chaque entrée résume le message en substance, présente les résultats des études et des publications parues depuis janvier 2025 (CAE, IPP, Insee, Institut français d'économie, DG Trésor, Banque de France, OCDE), et fournit un brouillon de paragraphe avec ses références. Les graphiques sont reconstruits à partir des sources publiques et mis en regard de leur version actualisée. L'ensemble repose sur des données publiques et des études publiées, avec vérification systématique des chiffres à la source. La page est actualisée chaque mois, automatiquement pour les graphiques tirés des séries de l'OCDE, après relecture pour les textes, et ne reproduit aucun texte de l'ouvrage.

## Comment lire cette page

- **Colonne 1, le passage.** Page du chapitre et message en substance. Aucun texte du livre n'est reproduit : les messages sont résumés.
- **Colonne 2, les données récentes.** Ce que disent les études et les publications des institutions depuis janvier 2025, chaque chiffre lu dans sa source. Le verdict indique si le message **tient**, est **renforcé**, **nuancé** ou **à corriger** ; « nouveau » signale une section à ajouter.
- **Colonne 3, le brouillon.** Un paragraphe proposé pour la prochaine édition, avec les références à ajouter juste en dessous.
- **Mise à jour.** *Auto* : le chiffre est actualisé chaque mois depuis la même source publique. *Manuel* : la formulation relève des auteurs.

## Passages susceptibles d'évoluer

<div class="ch6-wrap">
<table class="ch6">
<thead><tr><th>Passage du chapitre</th><th>Ce que disent les données récentes</th><th>Brouillon proposé et références</th></tr></thead>
<tbody>
{% for e in site.data.manuel_ch6 %}
<tr id="{{ e.id | downcase }}">
<td><strong>{{ e.page }}</strong><br><span class="ch6-sec">{{ e.section }}</span><br>{{ e.message }}</td>
<td><span class="ch6-v ch6-v-{{ e.verdict | replace: ' ', '-' | replace: 'é', 'e' | replace: 'à', 'a' }}">{{ e.verdict }}</span> <span class="ch6-maj">mise à jour {{ e.maj }}</span><br>{{ e.donnees | markdownify | remove: '<p>' | remove: '</p>' }}</td>
<td>{{ e.brouillon | markdownify }}<p class="ch6-refs-t">Références à ajouter</p><ul class="ch6-refs">{% for r in e.references %}<li>{{ r | markdownify | remove: '<p>' | remove: '</p>' }}</li>{% endfor %}</ul></td>
</tr>
{% endfor %}
</tbody>
</table>
</div>

## Graphiques : version du livre et mise à jour

Chaque graphique est reconstruit à partir de la source publique citée par le livre, puis mis en regard de sa version actualisée. Les données sont téléchargeables sous chaque figure.

{% assign g = site.data.manuel_ch6_charts %}
<figure><img src="{{ '/assets/manuel-ch6/graphique-6-3.png' | relative_url }}" alt="À gauche, emploi et ventes des entreprises françaises ayant adopté l'IA entre 2017 et 2020, écart aux non-adoptantes, 2014 à 2022. À droite, embauches en CDI de 21 à 29 ans chez les utilisatrices intensives d'IA générative, écart aux autres entreprises, 2021 à 2026."><figcaption><strong>Graphique 6.3.</strong> À gauche, la version du livre : l'emploi des entreprises adoptantes progresse d'environ 5 % par rapport aux non-adoptantes après l'adoption (Aghion et al., 2025, fig. 2, valeurs extraites de la figure publiée). À droite, la mise à jour pour l'IA générative : les utilisatrices intensives embauchent moins de jeunes en CDI depuis 2023 (Bergeaud et al., 2026, fig. 5, valeurs lues sur la figure, précision d'environ 0,01 ; résultat descriptif selon les auteurs). Barres : intervalles de confiance à 95 %. Graphique mis à jour à chaque nouvelle étude, à la main. <a href="{{ '/assets/manuel-ch6/data/graph63_aghion2025_fig2.csv' | relative_url }}">Données, gauche</a> · <a href="{{ '/assets/manuel-ch6/data/graph63_lift2026_fig5_21-29ans.csv' | relative_url }}">données, droite</a>.</figcaption></figure>

<figure><img src="{{ '/assets/manuel-ch6/graphique-6-4.png' | relative_url }}" alt="Productivité horaire de la France rapportée aux États-Unis et à l'Allemagne. À gauche, corrigée de la composition de l'emploi, 2003 à 2019. À droite, OCDE, non corrigée, jusqu'à la dernière année disponible."><figcaption><strong>Graphique 6.4.</strong> À gauche, la version du livre, corrigée de la composition de l'emploi (Guadalupe et al., 2022). À droite, la série de l'OCDE, non corrigée, actualisée chaque mois : la productivité horaire française passe de {{ g.g64.fr_us_2003 | replace: '.', ',' }} fois celle des États-Unis en 2003 à {{ g.g64.fr_us | replace: '.', ',' }} en {{ g.g64.annee }}. Même tendance, niveaux différents : sans correction, la France ne passe sous les États-Unis qu'en 2023. Les deux séries ne doivent pas être raccordées. <a href="{{ '/assets/manuel-ch6/data/graph64_original_guadalupe2022.csv' | relative_url }}">Données, gauche</a> · <a href="{{ '/assets/manuel-ch6/data/graph64_ocde.csv' | relative_url }}">données, droite</a>.</figcaption></figure>

<figure><img src="{{ '/assets/manuel-ch6/graphique-6-5.png' | relative_url }}" alt="Capital-risque en pourcentage du PIB par pays et par stade, 2022 et dernière année ; part du volume mondial par taille de tour, 2000-2023 et 2025."><figcaption><strong>Graphique 6.5.</strong> En haut, capital-risque en % du PIB : en {{ g.g65.annee }}, il est {{ g.g65.fr_fois | replace: '.', ',' }} fois plus faible en France qu'aux États-Unis, et {{ g.g65.de_fois | replace: '.', ',' }} fois plus faible en Allemagne (OCDE, actualisé chaque mois). En bas, part du volume mondial par taille de tour (Dealroom, actualisé à la main) : sur les tours de plus de 100 M$, l'Europe ne capte que 9 % du volume mondial en 2025 (périodes et périmètres différents de la version du livre : comparer les écarts, pas les niveaux). À gauche, la version du livre (CAE et Conseil allemand des experts économiques, 2024). <a href="{{ '/assets/manuel-ch6/data/graph65_gauche_ocde.csv' | relative_url }}">Données OCDE</a> · <a href="{{ '/assets/manuel-ch6/data/graph65_right_dealroom.csv' | relative_url }}">données Dealroom</a> · <a href="{{ '/assets/manuel-ch6/data/graph65_left_original_2022.csv' | relative_url }}">version du livre</a>.</figcaption></figure>

L'effet de demande de l'encadré 6.2 est suivi en continu, étude par étude, sur la page [Productivity]({{ '/productivity/#evidence-from-the-demand-side' | relative_url }}) (en anglais).

## Partis pris concurrents dans le débat public

<div class="ch6-wrap">
<table class="ch6">
<thead><tr><th>Débat</th><th>Position concurrente</th><th>Qui la porte</th><th>Chiffre principal</th></tr></thead>
<tbody>
{% for p in site.data.manuel_ch6_partis %}<tr><td>{{ p.debat }}</td><td>{{ p.position }}</td><td>{{ p.qui }}</td><td>{{ p.chiffre }}</td></tr>
{% endfor %}
</tbody>
</table>
</div>

## Sources suivies

Institutions françaises : Conseil d'analyse économique, Institut français d'économie (ex-OFCE et CEPII), Institut des politiques publiques, Insee, Dares, DG Trésor, Banque de France, Conseil national de productivité, Haut-commissariat à la Stratégie et au Plan (CNEPI), Cour des comptes, Sénat, Comité de surveillance des investissements d'avenir, Autorité de la concurrence, MESR-SIES, LIFT (HEC Paris). Institutions internationales : OCDE, FMI, BCE, Banque d'Angleterre, BLS, Bruegel. Recherche : NBER, CEPR, SSRN et revues à comité de lecture. Débat public : Institut Montaigne, Fondation iFRAP, Coe-Rexecode, Fondation Jean-Jaurès, Institut Avant-garde, Cepremap, La Fabrique de l'industrie, Conseil national de l'industrie, AmCham France. Données : OCDE (productivité, R&D, capital-risque), Dealroom.

Les graphiques tirés de l'OCDE sont actualisés le 2 de chaque mois ; les textes, le 16, par une proposition relue avant publication.
