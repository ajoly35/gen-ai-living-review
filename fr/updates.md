---
layout: default
lang: fr
alt: /updates/
title: Bilan mensuel
permalink: /fr/updates/
---

# Bilan mensuel de la revue
{:.no_toc}

Une fois par mois, les articles ajoutés à la revue vivante sont relus au regard de la revue telle qu'elle est, pour répondre à deux questions : **qu'est-ce qui mérite vraiment d'entrer dans la revue**, et **est-ce que cela change le tableau d'ensemble** ? Chaque bilan donne un verdict par étude (ajout, mention, à suivre, non retenue), un statut pour chacune des idées principales de la revue (tient, renforcée, nuancée, remise en cause) et les modifications de texte proposées. Rédigé par un assistant IA, puis relu et validé par Adrien Joly avant publication et envoi. [Le recevoir par email]({{ '/fr/subscribe/' | relative_url }}) (choisir « mensuel »).
{:.lead}

<ul class="emails">
{% assign us = site.pages | sort: "date" | reverse %}
{% for u in us %}{% if u.period and u.lang == "fr" %}<li><a href="{{ u.url | relative_url }}">{{ u.title | remove: "Bilan de la revue : " }}</a> · <strong>{{ u.verdict }}</strong>{% if u.adds %} · {{ u.adds }} ajout(s) à la revue{% endif %}</li>
{% endif %}{% endfor %}
</ul>

Comment les études sont jugées : [méthode]({{ '/fr/updates/method/' | relative_url }}).
