Deux des résultats de la revue peuvent être suivis au fil de l'eau. La marge des embauches, où la revue trouve l'effet le plus net (section [« Dispositifs d'exposition : embauches et entrée »](#exposure-designs-hiring-and-entry)), apparaît d'abord dans les offres d'emploi. Le Laboratoire de l'Innovation et du Futur du Travail (LIFT, HEC Paris), dirigé par Antonin Bergeaud, publie un tableau de bord trimestriel de l'IA dans les offres d'emploi françaises, construit à partir de la base JOCAS de la Dares, qui collecte les offres d'emploi en ligne en France, les offres étant classées comme IA ou IA générative par apprentissage automatique (Delbouve et Bergeaud ; article compagnon Aghion, Bergeaud, Bunel et Delbouve 2025). Les chiffres clés ci-dessous sont lus en direct dans le fichier de données du tracker à chaque chargement de cette page.

<div class="tracker-cards" id="lift-cards" data-src="https://heclift.github.io/website/data/ai-trackers/diffusion-emploi/general_results.csv">
  <div class="tracker-card"><span class="tracker-value" data-key="Total IA offers">104,935</span><span class="tracker-label">Offres d'emploi IA depuis janvier 2019</span><span class="tracker-delta" data-key="Number of AI offers in last quarter" data-prefix="+" data-suffix=" le trimestre dernier">+652 le trimestre dernier</span></div>
  <div class="tracker-card"><span class="tracker-value" data-key="Total IA générative offers">4,593</span><span class="tracker-label">Offres d'emploi IA générative</span><span class="tracker-delta" data-key="Number of GenAI offers in last quarter" data-prefix="+" data-suffix=" le trimestre dernier">+111 le trimestre dernier</span></div>
  <div class="tracker-card"><span class="tracker-value" data-key="Number of firms with AI offers">3,301</span><span class="tracker-label">Entreprises ayant publié une offre IA</span><span class="tracker-delta" data-key="Number of new AI adopters in last quarter" data-prefix="+" data-suffix=" le trimestre dernier">+48 le trimestre dernier</span></div>
  <div class="tracker-card"><span class="tracker-value" data-key="Number of firms with GenAI offers">464</span><span class="tracker-label">Entreprises ayant publié une offre IA générative</span><span class="tracker-delta" data-key="Number of new GenAI adopters in last quarter" data-prefix="+" data-suffix=" le trimestre dernier">+27 le trimestre dernier</span></div>
</div>
<p class="tracker-note" id="lift-cards-note">Chiffres publiés par LIFT le 4 novembre 2026 ; actualisation en direct en attente.</p>

Dans les séries mensuelles du tracker, les offres demandant des compétences en IA générative sont passées de 83 en 2022 à 356 en 2023, 1,651 en 2024 et 2,434 sur les dix premiers mois de 2025. Les offres de compétences en IA traditionnelle (apprentissage automatique, hors catégories générative, vision et langage) ont chuté de 11,895 en 2022 à 7,946 en 2023, puis sont remontées à 9,652 sur les dix premiers mois de 2025. L'IA générative reste une petite partie des embauches en IA : environ une offre sur cinq en 2025, contre une sur 150 en 2022. Il s'agit de décomptes d'offres demandant des compétences en IA, qui suivent donc la demande de spécialistes de l'IA, et non l'effet de l'IA sur les autres emplois. La dernière observation mensuelle est octobre 2025, et le décompte cumulé propre au tableau de bord utilise une définition plus large que la somme de ses séries mensuelles. La baisse relative des embauches de jeunes dans les professions exposées rapportée par Bergeaud, Bertheau, et al. (2026) provient d'une autre source, le registre des embauches et des fins de contrat de la Dares, et n'apparaît pas dans ce tracker.

<div class="tracker-embed">
  <iframe src="https://heclift.github.io/website/en/ai-trackers/diffusion-emploi/index.html" title="Tracker LIFT : diffusion de l'IA dans les offres d'emploi françaises" loading="lazy" referrerpolicy="no-referrer"></iframe>
</div>
<p class="tracker-note">Intégré depuis LIFT. <a href="https://heclift.github.io/website/en/ai-trackers/diffusion-emploi/index.html">Ouvrir le tracker dans sa propre page</a> pour les onglets secteur, taille d'entreprise, profession, compétences et carte, chacun avec un téléchargement CSV.</p>

Pour le volet croissance de la revue, LIFT tient aussi un [tracker de la diffusion de l'IA dans la science et les brevets](https://heclift.github.io/website/en/ai-trackers/diffusion-science/index.html) (brevets de l'Office européen des brevets citant la recherche en IA et publications en IA, à partir de REGPAT, OpenAlex et patCit, mis à jour chaque année) et un [tracker de la productivité de long terme](https://heclift.github.io/website/en/innovation-data/productivite/index.html) (PIB par habitant, productivité horaire et productivité globale des facteurs pour 24 économies depuis 1890, à partir de la Long Term Productivity Database de Bergeaud, Cette et Lecat, version 2.7). Les séries de productivité s'arrêtent en 2024, avant qu'un quelconque effet de l'IA générative ait pu apparaître.

Sources : LIFT, [tracker de la diffusion de l'IA (emploi)](https://heclift.github.io/website/en/ai-trackers/diffusion-emploi/index.html), développé par Paul Delbouve (Collège de France, PSE, DGE) et Antonin Bergeaud (HEC Paris, LSE, CEPR), données mises à jour chaque trimestre ; Aghion, Philippe, Antonin Bergeaud, Simon Bunel et Paul Delbouve. 2025. "Diffusion de l'Intelligence Artificielle en France." LIFT Working Paper 2025-01, 10 juillet, à paraître dans *Économie et Statistique / Economics and Statistics*. [Lien](https://heclift.github.io/website/pubs/ai-tracker/).

<script>
(function () {
  var box = document.getElementById('lift-cards');
  if (!box || !window.fetch) return;
  fetch(box.getAttribute('data-src'), { cache: 'no-store' }).then(function (r) {
    if (!r.ok) throw new Error(r.status);
    return r.text();
  }).then(function (txt) {
    var d = {};
    txt.split(/\r?\n/).slice(1).forEach(function (line) {
      var i = line.lastIndexOf(',');
      if (i > 0) d[line.slice(0, i).trim()] = Number(line.slice(i + 1));
    });
    var fmt = new Intl.NumberFormat('en-GB');
    var n = 0;
    box.querySelectorAll('[data-key]').forEach(function (el) {
      var v = d[el.getAttribute('data-key')];
      if (typeof v === 'number' && !isNaN(v)) {
        el.textContent = (el.getAttribute('data-prefix') || '') + fmt.format(Math.round(v)) + (el.getAttribute('data-suffix') || '');
        n++;
      }
    });
    var note = document.getElementById('lift-cards-note');
    if (note && n) note.textContent = 'Chiffres lus dans le fichier de données de LIFT le ' + new Date().toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) + '. Décomptes cumulés depuis janvier 2019 ; le tracker est mis à jour chaque trimestre.';
  }).catch(function () { /* keep the figures published on 4 November 2026 */ });
})();
</script>
