/* Refresh the EconVitals tiles from the public data repository the site itself reads
   (econvitals/econvitals-data, data/dashboard.json, updated after each release). The HTML
   already holds a snapshot, so a failed fetch leaves the page as published. */
(function () {
  var panel = document.querySelector('[data-ev-topic]');
  if (!panel || !window.fetch) return;
  var URL = 'https://raw.githubusercontent.com/econvitals/econvitals-data/main/data/dashboard.json';

  function pct(v, d) { return v == null ? null : (Math.round(v * Math.pow(10, d)) / Math.pow(10, d)).toFixed(d) + '%'; }
  function signed(v, d) { if (v == null) return null; var s = pct(v, d); return v > 0 ? '+' + s : s; }
  function k(v) { return v == null ? null : (v > 0 ? '+' : '') + Math.round(v) + 'k'; }
  function row(blocks, label) {
    for (var i = 0; i < blocks.length; i++) for (var j = 0; j < blocks[i].rows.length; j++)
      if (blocks[i].rows[j].label === label) return blocks[i].rows[j];
    return null;
  }
  function grp(groups, label) {
    for (var i = 0; i < groups.length; i++) for (var j = 0; j < groups[i].rows.length; j++)
      if (groups[i].rows[j].label === label) return groups[i].rows[j];
    return null;
  }
  function set(key, value, period) {
    if (value == null) return;
    var el = panel.querySelector('[data-ev="' + key + '"]');
    if (el) el.textContent = value;
    var p = panel.querySelector('[data-ev="' + key + '_period"]');
    if (p && period) p.textContent = period;
  }

  fetch(URL, { cache: 'no-cache' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
    if (!d || !d.sections) return;
    var s = d.sections, lab = s.labor || {}, gdp = s.gdp || {}, wages = s.wages || {};
    var rates = lab.rates && lab.rates.blocks ? lab.rates.blocks : [];
    var pay = lab.payroll_averages && lab.payroll_averages.rows ? lab.payroll_averages.rows : [];
    var table = gdp.table && gdp.table.groups ? gdp.table.groups : [];
    var r;

    if ((r = pay.filter(function (x) { return x.label === 'Total nonfarm'; })[0])) set('payrolls', k(r.m1), r.through);
    if ((r = pay.filter(function (x) { return x.label === 'Information'; })[0])) set('info_payrolls', k(r.m1), r.through);
    if ((r = row(rates, 'Unemployment rate'))) set('unemployment', pct(r.latest, 1), r.through);
    if ((r = row(rates, 'Hires rate'))) set('hires_rate', pct(r.latest, 1), r.through);
    if ((r = (wages.rows || []).filter(function (x) { return x.label === 'Real AHE (total private)'; })[0])) set('real_ahe', signed(r.ann_12, 1), '12 months to ' + r.through);

    if ((r = grp(table, 'GDP'))) set('gdp', pct(r.latest_q, 1), r.through + ', annual rate');
    if ((r = grp(table, 'Business fixed investment'))) set('bfi', pct(r.latest_q, 1), r.through + ', annual rate');
    if ((r = grp(table, 'Imports'))) set('imports', pct(r.latest_q, 1), r.through + ', annual rate');
    if ((r = grp(table, 'Productivity'))) set('productivity', pct(r.latest_q, 1), r.through + ', annual rate');
    if ((r = grp(table, 'Unit labor costs'))) set('ulc', signed(r.latest_q, 1), r.through + ', annual rate');
    if ((r = grp(table, 'Compensation per hour'))) set('comp_hour', pct(r.q4q4, 1), '4 quarters to ' + r.through);
    if (gdp.trackers && gdp.trackers.items) {
      var c = gdp.trackers.items.filter(function (x) { return x.composite; })[0];
      if (c) set('gdp_tracker', pct(c.value, 1), c.quarter + ', EconVitals composite');
    }
    if (d.meta && d.meta.generated_at) {
      var t = new Date(d.meta.generated_at);
      if (!isNaN(t)) set('as_of', t.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' }));
    }
  }).catch(function () { /* keep the snapshot */ });
})();
