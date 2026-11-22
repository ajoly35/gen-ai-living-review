/* Live trackers section (index.md, fr/index.md; template _includes/trackers.md).
   Reads the two outside trackers' public CSV files when the page loads and
   replaces the figures printed in the page. If a file cannot be read or its
   layout has changed, the printed figures stay as they are.

   - US: GenAI Adoption Tracker (Project on Workforce at Harvard), three files.
   - France: LIFT (HEC Paris) AI job postings tracker, one file. */
(function (root) {
  'use strict';

  var WAVE = /^(\d{1,2})\/(\d{2})$/;

  // Minimal CSV reader (handles quoted cells, which the occupation files use).
  function parseCSV(txt) {
    var rows = [], row = [], cell = '', q = false;
    for (var i = 0; i < txt.length; i++) {
      var c = txt[i];
      if (q) {
        if (c === '"' && txt[i + 1] === '"') { cell += '"'; i++; }
        else if (c === '"') q = false;
        else cell += c;
      } else if (c === '"') q = true;
      else if (c === ',') { row.push(cell); cell = ''; }
      else if (c === '\n' || c === '\r') {
        if (c === '\r' && txt[i + 1] === '\n') i++;
        row.push(cell); cell = '';
        if (row.length > 1 || row[0] !== '') rows.push(row);
        row = [];
      } else cell += c;
    }
    row.push(cell);
    if (row.length > 1 || row[0] !== '') rows.push(row);
    return rows;
  }

  function num(s) {
    var v = (s === undefined || s === null || String(s).trim() === '') ? NaN : Number(s);
    return isFinite(v) ? v : NaN;
  }

  // GenAI_All.csv has four header rows (Sample, genAI Use, Frequency, Statistic);
  // the first three label a group of columns once and leave the rest blank.
  function usColumn(rows, sample, use, freq) {
    var head = {};
    rows.forEach(function (r) {
      if (WAVE.test(r[0])) return;
      var filled = r.slice(), name = r[0].trim();
      if (name !== 'Statistic') for (var j = 2; j < filled.length; j++) if (filled[j] === '') filled[j] = filled[j - 1];
      head[name] = filled;
    });
    if (!head['Sample'] || !head['genAI Use'] || !head['Frequency'] || !head['Statistic']) return -1;
    for (var j = 1; j < head['Statistic'].length; j++) {
      if (head['Sample'][j] === sample && head['genAI Use'][j] === use &&
          head['Frequency'][j] === freq && head['Statistic'][j] === 'Mean') return j;
    }
    return -1;
  }

  // Returns the survey waves in file order: [{key:'08/26', any, work, hours, saved}].
  function usWaves(allRows, hoursRows, savedRows) {
    var cAny = usColumn(allRows, 'All', 'Any', 'Share Using GenAI');
    var cWork = usColumn(allRows, 'Employed', 'For Work', 'Share Using GenAI');
    if (cAny < 0 || cWork < 0) throw new Error('GenAI_All.csv: columns not found');
    var waves = [], byKey = {};
    allRows.forEach(function (r) {
      if (!WAVE.test(r[0])) return;
      var w = { key: r[0], any: num(r[cAny]), work: num(r[cWork]), hours: NaN, saved: NaN };
      waves.push(w); byKey[w.key] = w;
    });
    function add(rows, field) {
      rows.forEach(function (r) { if (WAVE.test(r[0]) && byKey[r[0]]) byKey[r[0]][field] = num(r[1]); });
    }
    add(hoursRows, 'hours'); add(savedRows, 'saved');
    return waves.filter(function (w) { return !isNaN(w.any) || !isNaN(w.work); });
  }

  function usLatest(waves) {
    for (var i = waves.length - 1; i >= 0; i--) {
      var w = waves[i];
      if (!isNaN(w.any) && !isNaN(w.work) && !isNaN(w.hours) && !isNaN(w.saved)) return w;
    }
    return null;
  }

  function yearBefore(waves, w) {
    var m = WAVE.exec(w.key), yy = ('0' + (Number(m[2]) - 1)).slice(-2);
    for (var i = 0; i < waves.length; i++) {
      var k = WAVE.exec(waves[i].key);
      if (Number(k[1]) === Number(m[1]) && k[2] === yy) return waves[i];
    }
    return null;
  }

  function waveDate(key) {
    var m = WAVE.exec(key);
    return new Date(2000 + Number(m[2]), Number(m[1]) - 1, 1);
  }

  function formatters(lang) {
    var loc = lang === 'fr' ? 'fr-FR' : 'en-GB';
    var one = new Intl.NumberFormat(loc, { minimumFractionDigits: 1, maximumFractionDigits: 1 });
    var whole = new Intl.NumberFormat(loc, { maximumFractionDigits: 0 });
    return {
      loc: loc,
      pct: function (v) { return isNaN(v) ? '–' : one.format(v) + (lang === 'fr' ? ' %' : '%'); },
      signed: function (v) {
        var s = one.format(Math.abs(v));
        return (/[1-9]/.test(s) ? (v > 0 ? '+' : '−') : '') + s;
      },
      count: function (v) { return whole.format(Math.round(v)); },
      wave: function (key) { return waveDate(key).toLocaleDateString(loc, { month: 'long', year: 'numeric' }); },
      day: function (d) { return d.toLocaleDateString(loc, { day: 'numeric', month: 'long', year: 'numeric' }); }
    };
  }

  // LIFT general_results.csv: "Metric,Value", one metric per line.
  function liftValues(txt) {
    var d = {};
    txt.split(/\r?\n/).slice(1).forEach(function (line) {
      var i = line.lastIndexOf(',');
      if (i > 0) d[line.slice(0, i).trim()] = num(line.slice(i + 1));
    });
    return d;
  }

  // LIFT offers_total.csv: monthly counts, columns ",ia générative,ia générale,cv,nlp,annee,mois" (exclusive categories).
  // The headline file's posting counts do not match this series (checked 22/11/2026), so postings come from here.
  function liftSeries(txt) {
    var all = parseCSV(txt), cats = ['ia générative', 'ia générale', 'cv', 'nlp'], months = [], q = {};
    if (!all.length) return null;
    var head = all[0].map(function (h) { return h.trim(); });
    var rows = all.slice(1).map(function (a) { var o = {}; head.forEach(function (h, i) { o[h] = a[i]; }); return o; });
    rows.forEach(function (r) {
      var y = num(r.annee), m = num(r.mois);
      if (isNaN(y) || isNaN(m)) return;
      var v = {}, all = 0;
      cats.forEach(function (c) { v[c] = num(r[c]) || 0; all += v[c]; });
      months.push({ y: y, m: m, gen: v['ia générative'], all: all });
      var k = y * 10 + Math.floor((m - 1) / 3) + 1;
      (q[k] = q[k] || []).push({ gen: v['ia générative'], all: all });
    });
    if (!months.length) return null;
    var end = months.reduce(function (a, b) { return (b.y * 12 + b.m > a.y * 12 + a.m) ? b : a; });
    var full = Object.keys(q).map(Number).filter(function (k) { return q[k].length === 3; });
    if (!full.length) return null;
    var lk = Math.max.apply(null, full), lq = q[lk];
    var sum = function (arr, f) { return arr.reduce(function (s, x) { return s + x[f]; }, 0); };
    return { ai_total: sum(months, 'all'), genai_total: sum(months, 'gen'),
             ai_quarter: sum(lq, 'all'), genai_quarter: sum(lq, 'gen'),
             end: new Date(end.y, end.m - 1, 1), qYear: Math.floor(lk / 10), qNum: lk % 10 };
  }

  var api = { parseCSV: parseCSV, usWaves: usWaves, usLatest: usLatest, yearBefore: yearBefore,
              formatters: formatters, liftValues: liftValues, liftSeries: liftSeries };
  if (typeof module !== 'undefined' && module.exports) { module.exports = api; return; }

  // ---- Page wiring ----
  var doc = root.document;
  if (!doc || !root.fetch || !root.Intl) return;
  var f = formatters((doc.documentElement.lang || 'en').slice(0, 2));

  function text(url) {
    return root.fetch(url, { cache: 'no-store' }).then(function (r) {
      if (!r.ok) throw new Error(url + ' ' + r.status);
      return r.text();
    });
  }

  function note(id, vars) {
    var el = doc.getElementById(id), tpl = el && el.getAttribute('data-live');
    if (!tpl) return;
    Object.keys(vars).forEach(function (k) { tpl = tpl.split('{' + k + '}').join(vars[k]); });
    el.textContent = tpl;
  }

  function us() {
    var box = doc.getElementById('us-cards');
    if (!box) return;
    var base = box.getAttribute('data-src');
    Promise.all(['GenAI_All.csv', 'GenAI_HoursShare_All.csv', 'GenAI_TimeSav_All.csv'].map(function (name) {
      return text(base + name).then(parseCSV);
    })).then(function (files) {
      var waves = usWaves(files[0], files[1], files[2]);
      var last = usLatest(waves);
      if (!last) throw new Error('no complete wave');
      var prev = yearBefore(waves, last);
      box.querySelectorAll('.tracker-value[data-series]').forEach(function (el) {
        el.textContent = f.pct(last[el.getAttribute('data-series')]);
      });
      box.querySelectorAll('.tracker-delta[data-series]').forEach(function (el) {
        var k = el.getAttribute('data-series');
        if (prev && !isNaN(prev[k])) el.textContent = f.signed(last[k] - prev[k]) + (el.getAttribute('data-suffix') || '');
        else el.textContent = '';
      });
      var body = doc.getElementById('us-waves-body');
      if (body) {
        body.textContent = '';
        waves.slice().reverse().forEach(function (w) {
          var tr = doc.createElement('tr');
          [f.wave(w.key), f.pct(w.any), f.pct(w.work), f.pct(w.hours), f.pct(w.saved)].forEach(function (v, i) {
            var td = doc.createElement(i ? 'td' : 'th');
            if (!i) td.setAttribute('scope', 'row');
            td.textContent = v;
            tr.appendChild(td);
          });
          body.appendChild(tr);
        });
        var fold = doc.getElementById('us-waves');
        if (fold) fold.hidden = false;
      }
      note('us-cards-note', { wave: f.wave(last.key), date: f.day(new Date()) });
    }).catch(function () { /* keep the printed figures */ });
  }

  function lift() {
    var box = doc.getElementById('lift-cards');
    if (!box) return;
    var fr = f.loc === 'fr-FR';
    text(box.getAttribute('data-src')).then(function (txt) {
      var d = liftSeries(txt), n = 0;
      if (!d) throw new Error('LIFT: empty series');
      box.querySelectorAll('[data-key]').forEach(function (el) {
        var v = d[el.getAttribute('data-key')];
        if (typeof v === 'number' && !isNaN(v)) {
          el.textContent = (el.getAttribute('data-prefix') || '') + f.count(v) + (el.getAttribute('data-suffix') || '');
          n++;
        }
      });
      if (n) note('lift-cards-note', {
        date: f.day(new Date()),
        end: d.end.toLocaleDateString(f.loc, { month: 'long', year: 'numeric' }),
        quarter: fr ? (d.qNum === 1 ? '1er' : d.qNum + 'e') + ' trimestre ' + d.qYear : 'Q' + d.qNum + ' ' + d.qYear
      });
    }).catch(function () { /* keep the printed figures */ });
    var sumUrl = box.getAttribute('data-summary');
    if (sumUrl) text(sumUrl).then(function (txt) {
      var d = liftValues(txt);
      box.querySelectorAll('[data-sum]').forEach(function (el) {
        var v = d[el.getAttribute('data-sum')];
        if (typeof v === 'number' && !isNaN(v)) el.textContent = f.count(v);
      });
    }).catch(function () { /* keep the printed figures */ });
  }

  function start() { us(); lift(); }
  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', start); else start();
})(typeof window !== 'undefined' ? window : this);
