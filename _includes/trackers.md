Two of the review's findings can be followed as they unfold. The hiring margin, where the review finds the clearest effect (section ["Exposure designs: hiring and entry"](#exposure-designs-hiring-and-entry)), shows up first in job postings. The Laboratoire de l'Innovation et du Futur du Travail (LIFT, HEC Paris), led by Antonin Bergeaud, publishes a quarterly dashboard of AI in French job postings, built from the Dares JOCAS database, which collects online job postings in France, with postings classified as AI or generative AI by machine learning (Delbouve and Bergeaud; companion paper Aghion, Bergeaud, Bunel and Delbouve 2025). The headline figures below are read live from the tracker's data file each time this page loads.

<div class="tracker-cards" id="lift-cards" data-src="https://heclift.github.io/website/data/ai-trackers/diffusion-emploi/general_results.csv">
  <div class="tracker-card"><span class="tracker-value" data-key="Total IA offers">104,935</span><span class="tracker-label">AI job postings since January 2019</span><span class="tracker-delta" data-key="Number of AI offers in last quarter" data-prefix="+" data-suffix=" last quarter">+652 last quarter</span></div>
  <div class="tracker-card"><span class="tracker-value" data-key="Total IA générative offers">4,593</span><span class="tracker-label">Generative AI job postings</span><span class="tracker-delta" data-key="Number of GenAI offers in last quarter" data-prefix="+" data-suffix=" last quarter">+111 last quarter</span></div>
  <div class="tracker-card"><span class="tracker-value" data-key="Number of firms with AI offers">3,301</span><span class="tracker-label">Firms that have posted an AI job</span><span class="tracker-delta" data-key="Number of new AI adopters in last quarter" data-prefix="+" data-suffix=" last quarter">+48 last quarter</span></div>
  <div class="tracker-card"><span class="tracker-value" data-key="Number of firms with GenAI offers">464</span><span class="tracker-label">Firms that have posted a generative AI job</span><span class="tracker-delta" data-key="Number of new GenAI adopters in last quarter" data-prefix="+" data-suffix=" last quarter">+27 last quarter</span></div>
</div>
<p class="tracker-note" id="lift-cards-note">Figures as published by LIFT on 4 November 2026; live refresh pending.</p>

In the tracker's monthly series, postings asking for generative AI skills rose from 83 in 2022 to 356 in 2023, 1,651 in 2024 and 2,434 in the first ten months of 2025. Postings for traditional AI skills (machine learning, without the generative, vision and language categories) fell from 11,895 in 2022 to 7,946 in 2023, then recovered to 9,652 in the first ten months of 2025. Generative AI is still a small part of AI hiring: about one posting in five in 2025, against one in 150 in 2022. These are counts of postings that ask for AI skills, so they track the demand for AI specialists, not the effect of AI on other jobs. The latest monthly observation is October 2025, and the dashboard's own cumulative count uses a broader definition than the sum of its monthly series. The relative fall in young hires in exposed occupations reported by Bergeaud, Bertheau, et al. (2026) comes from a different source, the Dares register of hires and contract ends, and is not shown in this tracker.

<div class="tracker-embed">
  <iframe src="https://heclift.github.io/website/en/ai-trackers/diffusion-emploi/index.html" title="LIFT tracker: AI diffusion in French job postings" loading="lazy" referrerpolicy="no-referrer"></iframe>
</div>
<p class="tracker-note">Embedded from LIFT. <a href="https://heclift.github.io/website/en/ai-trackers/diffusion-emploi/index.html">Open the tracker in its own page</a> for the sector, firm size, occupation, skills and map tabs, each with a CSV download.</p>

For the growth side of the review, LIFT also keeps an [AI diffusion in science and patents tracker](https://heclift.github.io/website/en/ai-trackers/diffusion-science/index.html) (European Patent Office patents citing AI research and AI publications, from REGPAT, OpenAlex and patCit, updated yearly) and a [long run productivity tracker](https://heclift.github.io/website/en/innovation-data/productivite/index.html) (GDP per head, hourly productivity and total factor productivity for 24 economies since 1890, from the Bergeaud, Cette and Lecat Long Term Productivity Database, version 2.7). The productivity series stop in 2024, before any effect of generative AI could appear.

Sources: LIFT, [AI diffusion (jobs) tracker](https://heclift.github.io/website/en/ai-trackers/diffusion-emploi/index.html), developed by Paul Delbouve (Collège de France, PSE, DGE) and Antonin Bergeaud (HEC Paris, LSE, CEPR), data updated quarterly; Aghion, Philippe, Antonin Bergeaud, Simon Bunel and Paul Delbouve. 2025. "Diffusion de l'Intelligence Artificielle en France." LIFT Working Paper 2025-01, 10 July, forthcoming in *Économie et Statistique / Economics and Statistics*. [Link](https://heclift.github.io/website/pubs/ai-tracker/).

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
    if (note && n) note.textContent = 'Figures read from LIFT’s data file on ' + new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' }) + '. Cumulative counts since January 2019; the tracker is updated quarterly.';
  }).catch(function () { /* keep the figures published on 4 November 2026 */ });
})();
</script>
