/* Elderwood — bibliothèque du lore : application statique (aucune dépendance). */
(function () {
  'use strict';

  var EW = window.EW || {};
  var M = EW.manifest;
  var GL = EW.glossary || [];
  var CONTRA = EW.contradictions || [];
  var view = document.getElementById('view');
  if (!M) { view.innerHTML = '<p class="notice">Données introuvables (data/manifest.js). Lancez <code>python3 build.py</code>.</p>'; return; }

  /* ------------------------------------------------------------------ utilitaires */
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var LEVELS = ['public', 'joueurs', 'staff'];
  var maxAudience = M.audience ? LEVELS.indexOf(M.audience) : 2;
  var LNAME = M.levels || { public: 'Public', joueurs: 'Joueurs', staff: 'Staff' };

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function fold(s) {
    return String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/œ/g, 'oe').replace(/æ/g, 'ae').replace(/’/g, "'");
  }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { } return null; }
  function plural(n, a, b) { return n + ' ' + (n > 1 ? b : a); }
  function debounce(fn, ms) { var t; return function () { var a = arguments, c = this; clearTimeout(t); t = setTimeout(function () { fn.apply(c, a); }, ms); }; }

  /* ------------------------------------------------------------------ état */
  var pageByKey = {}, catByName = {}, catBySlug = {};
  M.pages.forEach(function (p) { pageByKey[p.k] = p; });
  M.categories.forEach(function (c) { catByName[c.name] = c; catBySlug[c.slug] = c; });

  var mode = store('ew-mode');
  if (LEVELS.indexOf(mode) < 0 || LEVELS.indexOf(mode) > maxAudience) mode = maxAudience >= 1 ? 'joueurs' : 'public';
  function modeIdx() { return LEVELS.indexOf(mode); }
  function visible(p) { return LEVELS.indexOf(p.a) <= modeIdx(); }
  function visiblePages() { return M.pages.filter(visible); }
  function catPages(c) { return c.keys.map(function (k) { return pageByKey[k]; }).filter(function (p) { return p && visible(p); }); }
  function visibleCats() { return M.categories.filter(function (c) { return catPages(c).length; }); }

  function sClass(s) {
    if (!s) return 's-none';
    return { 'Validé': 's-valide', 'En cours de rédaction': 's-encours', 'À modifier': 's-amodifier', 'Possibilité de modifier': 's-possible' }[s] || 's-none';
  }
  function statusBadge(p) { return '<span class="badge ' + sClass(p.s) + '" title="Statut de rédaction">' + esc(p.s || 'Statut non documenté') + '</span>'; }
  function accessBadge(p) { return '<span class="badge a-' + p.a + '" title="Niveau d\'accès sur ce site">' + esc(LNAME[p.a] || p.a) + '</span>'; }
  function badges(p, extra) {
    return '<div class="badges">' + accessBadge(p) + (p.wiki ? '<span class="badge wiki">Wiki officiel</span>' : statusBadge(p)) + (p.arch ? '<span class="badge arch">Archive (ancienne version)</span>' : '') + (extra || '') + '</div>';
  }
  function nd(v) { return v ? esc(v) : '<span class="nd">non documenté</span>'; }
  function pageHref(k, anchor, q) { return '#/p/' + encodeURIComponent(k) + (anchor ? '/' + encodeURIComponent(anchor) : '') + (q ? '?q=' + encodeURIComponent(q) : ''); }

  /* ------------------------------------------------------------------ chargement des pages */
  var pending = {};
  function loadScript(src) {
    return new Promise(function (res, rej) {
      var s = document.createElement('script'); s.src = src; s.async = true;
      s.onload = function () { res(); }; s.onerror = function () { rej(new Error('échec ' + src)); };
      document.head.appendChild(s);
    });
  }
  function loadPage(k) {
    if (EW.pages && EW.pages[k]) return Promise.resolve(EW.pages[k]);
    if (pending[k]) return pending[k];
    pending[k] = loadScript('data/pages/' + encodeURIComponent(k) + '.js').then(function () { return EW.pages[k]; });
    pending[k].catch(function () { delete pending[k]; });
    return pending[k];
  }

  /* ------------------------------------------------------------------ recherche plein texte */
  var Search = (function () {
    var state = 'idle', promise = null, docs = [], terms = [], inv = Object.create(null), df = Object.create(null), foldedCache = [], idxOf = {};
    var VAR = { a: 'aàâäáãåā', e: 'eéèêëē', i: 'iîïíìī', o: 'oôöóòõō', u: 'uùûüúū', c: 'cç', y: 'yÿý', n: 'nñ' };

    function words(s) { return fold(s).match(/[a-z0-9]+/g) || []; }
    function srcOf(t) {
      var out = '';
      for (var i = 0; i < t.length; i++) {
        var ch = t[i], nx = t[i + 1];
        if (ch === 'o' && nx === 'e') { out += '(?:o[eéèêëē]|œ)'; i++; continue; }
        if (ch === 'a' && nx === 'e') { out += '(?:ae|æ)'; i++; continue; }
        out += VAR[ch] ? '[' + VAR[ch] + ']' : ch;
      }
      return out;
    }
    function regexFor(toks, prefix) {
      if (!toks.length) return null;
      var alt = toks.map(function (t) { return srcOf(t); }).join('|');
      try { return new RegExp('(?<![\\p{L}\\p{N}])(?:' + alt + ')' + (prefix === false ? '(?![\\p{L}\\p{N}])' : '[\\p{L}\\p{N}]*'), 'giu'); }
      catch (e) { return new RegExp('(' + alt + ')', 'gi'); }
    }

    function ready() {
      if (state === 'ready') return Promise.resolve();
      if (promise) return promise;
      state = 'loading';
      promise = (EW.search ? Promise.resolve() : loadScript('data/search.js')).then(function () {
        docs = EW.search;
        return new Promise(function (resolve) {
          var i = 0, N = docs.length;
          (function chunk() {
            var stop = Math.min(N, i + 6);
            for (; i < stop; i++) addDoc(i);
            if (i < N) setTimeout(chunk, 0); else { terms = Object.keys(inv).sort(); state = 'ready'; resolve(); }
          })();
        });
      });
      return promise;
    }
    function addDoc(i) {
      var d = docs[i], p = pageByKey[d.k]; idxOf[d.k] = i;
      var w = Object.create(null), cnt = Object.create(null), b = words(d.x), j, t;
      for (j = 0; j < b.length; j++) cnt[b[j]] = (cnt[b[j]] || 0) + 1;
      for (t in cnt) w[t] = 1 + Math.log(cnt[t]);
      if (p) {
        words(p.t).forEach(function (x) { w[x] = (w[x] || 0) + 6; });
        words(p.kw || '').forEach(function (x) { w[x] = (w[x] || 0) + 3; });
        words(p.res || '').forEach(function (x) { w[x] = (w[x] || 0) + 1.5; });
      }
      for (t in w) { (inv[t] || (inv[t] = [])).push([i, w[t]]); }
    }
    function lowerBound(a, x) { var lo = 0, hi = a.length; while (lo < hi) { var m = (lo + hi) >> 1; if (a[m] < x) lo = m + 1; else hi = m; } return lo; }
    function expand(tok) {
      var out = [];
      if (inv[tok]) out.push([tok, 1]);
      if (tok.length >= 2) {
        for (var i = lowerBound(terms, tok); i < terms.length && terms[i].indexOf(tok) === 0 && out.length < 60; i++) if (terms[i] !== tok) out.push([terms[i], 0.7]);
      }
      return out;
    }
    function foldedText(i) { return foldedCache[i] || (foldedCache[i] = fold(docs[i].x)); }

    /* filtres : {c: catégorie, s: statut ('' = tous, 'none' = non documenté), a: niveau d'accès} */
    function run(q, f) {
      f = f || {};
      var toks = Array.from(new Set(words(q))).filter(function (t) { return t.length >= 2 || /\d/.test(t); });
      var N = docs.length, scores = Object.create(null), hit = Object.create(null), partial = false;
      var pass = function (i) {
        var p = pageByKey[docs[i].k]; if (!p || !visible(p)) return false;
        if (f.c && p.c !== f.c) return false;
        if (f.a && p.a !== f.a) return false;
        if (f.s) { if (f.s === 'none' ? !!p.s : p.s !== f.s) return false; }
        return true;
      };
      if (!toks.length) {
        var all = []; for (var i = 0; i < N; i++) if (pass(i)) all.push({ k: docs[i].k, score: 0, i: i });
        return { results: all, toks: [], partial: false };
      }
      toks.forEach(function (t) {
        var ex = expand(t);
        ex.forEach(function (e) {
          var post = inv[e[0]], idf = Math.log(1 + N / post.length);
          for (var j = 0; j < post.length; j++) {
            var di = post[j][0], sc = post[j][1] * idf * e[1], key = di + ':' + t;
            if (!hit[key] || hit[key] < sc) { scores[di] = (scores[di] || 0) + sc - (hit[key] || 0); hit[key] = sc; }
          }
        });
      });
      var res = [];
      Object.keys(scores).forEach(function (k) {
        var di = +k; if (!pass(di)) return;
        var n = 0; toks.forEach(function (t) { if (hit[di + ':' + t]) n++; });
        res.push({ k: docs[di].k, score: scores[di], n: n, i: di });
      });
      var full = res.filter(function (r) { return r.n === toks.length; });
      if (!full.length && res.length) { partial = true; full = res; } else if (full.length) { /* ET strict */ }
      // bonus : expression exacte et titre
      var phrase = toks.join(' ');
      full.forEach(function (r) {
        var p = pageByKey[r.k];
        if (toks.length > 1 && foldedText(r.i).replace(/[^a-z0-9]+/g, ' ').indexOf(phrase) >= 0) r.score *= 1.6;
        var ft = fold(p.t).replace(/[^a-z0-9]+/g, ' ');
        if (ft.indexOf(phrase) >= 0) r.score *= 1.5;
        if (partial) r.score *= r.n / toks.length;
      });
      full.sort(function (a, b) { return b.score - a.score || (pageByKey[a.k].t < pageByKey[b.k].t ? -1 : 1); });
      return { results: full, toks: toks, partial: partial };
    }

    /* extrait autour des occurrences, avec <mark> */
    function snippet(i, toks, len) {
      var text = docs[i].x, re = regexFor(toks), m, pos = [], guard = 0;
      if (!re) return '';
      len = len || 230;
      while ((m = re.exec(text)) && guard++ < 400) { pos.push({ i: m.index, l: m[0].length, t: fold(m[0]).slice(0, 3) }); if (m[0].length === 0) re.lastIndex++; }
      if (!pos.length) return esc(text.slice(0, len).replace(/\s+/g, ' ')) + '…';
      var best = pos[0], bs = -1;
      pos.slice(0, 120).forEach(function (p) {
        var seen = {}, c = 0; pos.forEach(function (q) { if (Math.abs(q.i - p.i) < len / 2 && !seen[q.t]) { seen[q.t] = 1; c++; } });
        if (c > bs) { bs = c; best = p; }
      });
      var a = Math.max(0, best.i - Math.floor(len * 0.35)), b = Math.min(text.length, a + len);
      var sp = text.indexOf(' ', a); if (a > 0 && sp > -1 && sp < a + 25) a = sp + 1;
      var seg = text.slice(a, b), out = '', last = 0, r2 = regexFor(toks), mm;
      while ((mm = r2.exec(seg))) { out += esc(seg.slice(last, mm.index)) + '<mark>' + esc(mm[0]) + '</mark>'; last = mm.index + mm[0].length; if (!mm[0].length) r2.lastIndex++; }
      out += esc(seg.slice(last));
      return (a > 0 ? '… ' : '') + out.replace(/\s*\n+\s*/g, ' ') + (b < text.length ? ' …' : '');
    }
    return { ready: ready, run: run, snippet: snippet, regexFor: regexFor, words: words, isReady: function () { return state === 'ready'; }, srcOf: srcOf };
  })();

  /* ------------------------------------------------------------------ barre latérale */
  function renderSidebar(cur) {
    var h = '<a class="sn-home' + (cur.type === 'home' ? ' current' : '') + '" href="#/">Accueil</a>';
    var used = {};
    M.groups.forEach(function (g) {
      var cats = g.cats.map(function (n) { return catByName[n]; }).filter(function (c) { return c && catPages(c).length; });
      if (!cats.length) return;
      if (!(cats.length === 1 && cats[0].name === g.titre)) h += '<div class="sn-group">' + esc(g.titre) + '</div>';
      cats.forEach(function (c) { used[c.name] = 1; h += sideCat(c, cur); });
    });
    var rest = visibleCats().filter(function (c) { return !used[c.name]; });
    if (rest.length) { h += '<div class="sn-group">Autres</div>'; rest.forEach(function (c) { h += sideCat(c, cur); }); }
    h += '<div class="sn-group">Outils</div><a class="sn-home' + (cur.type === 'gloss' ? ' current' : '') + '" href="#/glossaire">Glossaire</a>' +
      '<a class="sn-home' + (cur.type === 'search' ? ' current' : '') + '" href="#/recherche">Recherche avancée</a>' +
      '<a class="sn-home' + (cur.type === 'contra' ? ' current' : '') + '" href="#/contradictions">Contradictions connues</a>' +
      '<a class="sn-home' + (cur.type === 'missing' ? ' current' : '') + '" href="#/non-disponible">Contenu non disponible</a>' +
      '<a class="sn-home' + (cur.type === 'about' ? ' current' : '') + '" href="#/a-propos">À propos & sources</a>';
    $('#sideNav').innerHTML = h;
    var curEl = $('#sideNav a.current'); if (curEl && curEl.closest('.sn-list')) { try { curEl.scrollIntoView({ block: 'nearest' }); } catch (e) { } }
  }
  function wikiTree(ps) {
    var by = {}, roots = [];
    ps.forEach(function (p) { by[p.u] = { p: p, kids: [] }; });
    ps.forEach(function (p) {
      var segs = p.u.split('/'), par = null;
      for (var i = segs.length - 1; i >= 1 && !par; i--) par = by[segs.slice(0, i).join('/')] || null;
      (par ? par.kids : roots).push(by[p.u]);
    });
    return roots;
  }
  function hasKey(n, k) { return n.p.k === k || n.kids.some(function (x) { return hasKey(x, k); }); }
  function treeHtml(nodes, curKey) {
    return '<ul class="sn-tree">' + nodes.map(function (n) {
      var a = '<a href="' + pageHref(n.p.k) + '"' + (curKey === n.p.k ? ' class="current" aria-current="page"' : '') + '>' + esc(n.p.t) + '</a>';
      if (!n.kids.length) return '<li>' + a + '</li>';
      return '<li><details' + (hasKey(n, curKey) ? ' open' : '') + '><summary>' + a + '</summary>' + treeHtml(n.kids, curKey) + '</details></li>';
    }).join('') + '</ul>';
  }
  function sideCat(c, cur) {
    var ps = catPages(c), open = (cur.type === 'cat' && cur.slug === c.slug) || (cur.type === 'page' && pageByKey[cur.key] && pageByKey[cur.key].c === c.name);
    if (ps.length && ps[0].wiki) {
      return '<details class="sn-cat"' + (open ? ' open' : '') + '><summary><a href="#/c/' + c.slug + '" style="color:inherit;text-decoration:none">' + esc(c.name) + '</a><span class="sn-count">' + ps.length + '</span></summary>' +
        '<div class="sn-wiki">' + treeHtml(wikiTree(ps), cur.type === 'page' ? cur.key : '') + '</div></details>';
    }
    var main = ps.filter(function (p) { return !p.arch; }), arch = ps.filter(function (p) { return p.arch; });
    function li(p) {
      return '<li><a href="' + pageHref(p.k) + '"' + (cur.type === 'page' && cur.key === p.k ? ' class="current" aria-current="page"' : '') + '>' +
        '<span class="pip ' + sClass(p.s) + '" title="' + esc(p.s || 'Statut non documenté') + '"></span><span>' + esc(p.t) + '</span>' +
        (p.a !== 'public' && modeIdx() > 0 && p.a === 'staff' ? '<span class="lvl-tag a-staff" title="Réservé au staff">staff</span>' : '') + '</a></li>';
    }
    return '<details class="sn-cat"' + (open ? ' open' : '') + '><summary><a href="#/c/' + c.slug + '" style="color:inherit;text-decoration:none">' + esc(c.name) + '</a><span class="sn-count">' + ps.length + '</span></summary>' +
      '<ul class="sn-list">' + main.map(li).join('') + (arch.length ? '<li class="sn-arch">Archives</li>' + arch.map(li).join('') : '') + '</ul></details>';
  }

  /* ------------------------------------------------------------------ vues */
  var QUICK = [
    ['wiki-accueil', 'Wiki officiel'], ['wiki-reglement', 'Règlement (wiki)'], ['reglement-eleves-30-10-26', 'Règlement des élèves'], ['reglement-professeurs-30-10-26', 'Points de Maison & sanctions'],
    ['commandes-raccourcis-A', 'Commandes du jeu'], ['bible-du-lore', 'Bible du lore'], ['bestiaire-30-10-26', 'Bestiaire'],
    ['constitution-peines-amendes', 'Peines et amendes'], ['suivi-mj-v1', 'Paliers T1–T5 & XP'], ['reglement-illegal', 'Règlement illégal']
  ];
  function catBlurb(c) {
    var ps = catPages(c).filter(function (p) { return !p.arch; });
    var names = ps.slice(0, 3).map(function (p) { return p.t; });
    return esc(names.join(' · ')) + (ps.length > 3 ? ' …' : '');
  }
  function homeView() {
    var vp = visiblePages(), vc = visibleCats();
    var h = '<section class="hero"><div class="orn" aria-hidden="true">✦ ✦ ✦</div><h1>Elderwood</h1><p>' + esc(M.subtitle) + '</p>' +
      '<div class="hero-search"><label class="sr-only" for="hq">Rechercher</label><input id="hq" type="search" placeholder="Rechercher dans tous les documents…" autocomplete="off"></div>' +
      '<div class="stats">' + plural(vp.length, 'document', 'documents') + ' · ' + plural(vc.length, 'section', 'sections') + ' · affichage « ' + esc(LNAME[mode]) + ' »</div>';
    var q = QUICK.filter(function (x) { return pageByKey[x[0]] && visible(pageByKey[x[0]]); });
    if (q.length) h += '<div class="quick" aria-label="Accès rapides">' + q.map(function (x) { return '<a href="' + pageHref(x[0]) + '">' + esc(x[1]) + '</a>'; }).join('') + '</div>';
    h += '</section>';
    M.groups.forEach(function (g) {
      var cats = g.cats.map(function (n) { return catByName[n]; }).filter(function (c) { return c && catPages(c).length; });
      if (!cats.length) return;
      h += '<section class="group"><h2>' + esc(g.titre) + '</h2><div class="cards">' + cats.map(function (c) {
        return '<a class="card" href="#/c/' + c.slug + '"><h3>' + esc(c.name) + '</h3><span class="n">' + plural(catPages(c).length, 'document', 'documents') + '</span><p>' + catBlurb(c) + '</p></a>';
      }).join('') + '</div></section>';
    });
    return { html: h, title: M.title, after: function () { bindHeroSearch(); } };
  }
  function bindHeroSearch() {
    var hq = $('#hq'); if (!hq) return;
    hq.addEventListener('focus', function () { Search.ready(); });
    hq.addEventListener('keydown', function (e) { if (e.key === 'Enter') { location.hash = '#/recherche?q=' + encodeURIComponent(hq.value); } });
  }

  function itemHtml(p, snip) {
    return '<li><a class="item" href="' + pageHref(p.k, '', snip && snip.q) + '"><h3>' + esc(p.t) + '</h3><div class="cat">' + esc(p.c) + '</div>' +
      (snip && snip.html ? '<p class="snip">' + snip.html + '</p>' : '<p class="sum">' + (p.res ? esc(p.res) : '<span class="nd">Résumé non documenté</span>') + '</p>') +
      badges(p) + '</a></li>';
  }
  function catView(slug) {
    var c = catBySlug[slug];
    if (!c || !catPages(c).length) return notFound();
    var ps = catPages(c), main = ps.filter(function (p) { return !p.arch; }), arch = ps.filter(function (p) { return p.arch; });
    if (ps[0] && ps[0].wiki) {
      var tree = function (nodes) {
        return '<ul class="wtree">' + nodes.map(function (n) {
          return '<li><a href="' + pageHref(n.p.k) + '"><strong>' + esc(n.p.t) + '</strong></a>' + (n.kids.length ? tree(n.kids) : '') + '</li>';
        }).join('') + '</ul>';
      };
      return { html: '<nav class="crumbs" aria-label="Fil d\'Ariane"><a href="#/">Accueil</a><span class="sep">›</span><span aria-current="page">' + esc(c.name) + '</span></nav>' +
        '<h1 class="page-title">' + esc(c.name) + '</h1><p class="result-meta">' + plural(ps.length, 'page', 'pages') + ' · reprise intégrale du wiki public, dans l\'arborescence d\'origine.</p>' + tree(wikiTree(ps)), title: c.name + ' — Elderwood' };
    }
    var h = '<nav class="crumbs" aria-label="Fil d\'Ariane"><a href="#/">Accueil</a><span class="sep">›</span><span aria-current="page">' + esc(c.name) + '</span></nav>' +
      '<h1 class="page-title">' + esc(c.name) + '</h1><p class="result-meta">' + plural(ps.length, 'document', 'documents') + ' · <a href="#/recherche?c=' + encodeURIComponent(c.name) + '">Rechercher dans cette section</a></p>' +
      '<ul class="list">' + main.map(function (p) { return itemHtml(p); }).join('') + '</ul>';
    if (arch.length) h += '<h2 class="sub-h">Archives (anciennes versions)</h2><ul class="list">' + arch.map(function (p) { return itemHtml(p); }).join('') + '</ul>';
    return { html: h, title: c.name + ' — Elderwood' };
  }
  function notFound() {
    return { html: '<h1 class="page-title">Page introuvable</h1><p class="notice">Ce document n\'existe pas ou n\'est pas disponible dans ce niveau d\'affichage. <a href="#/">Retour à l\'accueil</a></p>', title: 'Introuvable — Elderwood' };
  }

  function metaCard(p) {
    var kws = (p.kw || '').split(',').map(function (x) { return x.trim(); }).filter(Boolean);
    if (p.wiki) {
      return '<details class="meta-card"><summary>Fiche de la page</summary><dl>' +
        '<dt>Section</dt><dd><a href="#/c/' + catByName[p.c].slug + '">' + esc(p.c) + '</a></dd>' +
        '<dt>Accès sur ce site</dt><dd>' + accessBadge(p) + '</dd>' +
        '<dt>Page d\'origine</dt><dd><a href="https://wiki.elderwood-rp.com/' + esc(p.u) + '" target="_blank" rel="noopener noreferrer">wiki.elderwood-rp.com/' + esc(p.u) + '</a> <span class="nd">(le contenu est entièrement repris ici)</span></dd>' +
        '<dt>Longueur</dt><dd>' + p.w.toLocaleString('fr-FR') + ' mots · ≈ ' + Math.max(1, Math.round(p.w / 220)) + ' min de lecture</dd></dl></details>';
    }
    return '<details class="meta-card" open><summary>Fiche du document</summary><dl>' +
      '<dt>Section</dt><dd><a href="#/c/' + catByName[p.c].slug + '">' + esc(p.c) + '</a></dd>' +
      '<dt>Statut de rédaction</dt><dd>' + statusBadge(p) + '</dd>' +
      '<dt>Accès sur ce site</dt><dd>' + accessBadge(p) + '</dd>' +
      '<dt>Accès d\'origine</dt><dd>' + nd(p.acc_src) + '</dd>' +
      '<dt>Responsable</dt><dd>' + nd(p.resp) + '</dd>' +
      '<dt>Domaine</dt><dd>' + nd(p.dom) + '</dd>' +
      '<dt>Résumé officiel</dt><dd>' + nd(p.res) + '</dd>' +
      '<dt>Mots-clés</dt><dd>' + (kws.length ? '<span class="chips">' + kws.map(function (k) { return '<a class="chip" href="#/recherche?q=' + encodeURIComponent(k) + '">' + esc(k) + '</a>'; }).join('') + '</span>' : '<span class="nd">non documenté</span>') + '</dd>' +
      '<dt>Remarques</dt><dd>' + nd(p.rem) + '</dd>' +
      '<dt>Longueur</dt><dd>' + p.w.toLocaleString('fr-FR') + ' mots · ≈ ' + Math.max(1, Math.round(p.w / 220)) + ' min de lecture</dd>' +
      '</dl></details>';
  }
  function tocHtml(toc, cls) {
    return '<ol>' + toc.map(function (t) { return '<li class="l' + t.l + '"><a href="' + pageHref(cur.key, t.id) + '" data-id="' + esc(t.id) + '">' + esc(t.t) + '</a></li>'; }).join('') + '</ol>';
  }
  var cur = { type: 'home' };

  function pageView(key, anchor, q) {
    var p = pageByKey[key];
    if (!p) return notFound();
    if (!visible(p)) {
      return {
        html: '<h1 class="page-title">' + esc(p.t) + '</h1>' + badges(p) +
          '<div class="banner lvl-staff"><strong>Document réservé au niveau « ' + esc(LNAME[p.a]) + ' ».</strong> Il n\'apparaît pas dans la navigation du niveau « ' + esc(LNAME[mode]) + ' ». ' +
          '<p><button class="btn" id="unlock" type="button">Afficher le niveau « ' + esc(LNAME[p.a]) + ' »</button></p>' +
          '<p class="nd">Ce choix ne sert qu\'à filtrer l\'affichage : ce n\'est pas une protection d\'accès. Pour un site réellement public, générez la version « joueurs » ou « public » (voir le README).</p></div>',
        title: p.t + ' — Elderwood', after: function () { $('#unlock').addEventListener('click', function () { setMode(p.a); }); }
      };
    }
    var c = catByName[p.c];
    var h = '<nav class="crumbs" aria-label="Fil d\'Ariane"><a href="#/">Accueil</a><span class="sep">›</span><a href="#/c/' + c.slug + '">' + esc(p.c) + '</a><span class="sep">›</span><span aria-current="page">' + esc(p.t) + '</span></nav>' +
      '<h1 class="page-title">' + esc(p.t) + '</h1>' + badges(p);
    if (p.s === 'En cours de rédaction' || p.s === 'À modifier') h += '<div class="banner ' + sClass(p.s) + '"><strong>Statut : ' + esc(p.s) + '.</strong> Le contenu de ce document n\'est pas définitif.</div>';
    if (p.arch) h += '<div class="banner arch"><strong>Archive.</strong> Ancienne version conservée pour mémoire ; consulter la version la plus récente de la même section.</div>';
    if (p.sheet) h += '<div class="banner arch"><strong>Feuille de calcul.</strong> Un onglet = un tableau (triable, filtrable). Le fichier d\'origine est exporté en valeurs : les cellules vides ne sont pas conservées, des lignes peuvent donc sembler décalées par rapport à l\'en-tête.</div>';
    if (p.a === 'staff') h += '<div class="banner lvl-staff"><strong>Document staff.</strong> Réservé au pôle RP / staff, ne pas diffuser aux joueurs.</div>';
    h += metaCard(p).replace('<details class="meta-card" open>', window.innerWidth < 900 ? '<details class="meta-card">' : '<details class="meta-card" open>');
    h += '<div id="docHost"><p class="loading">Chargement du document…</p></div>';
    return {
      html: h, title: p.t + ' — Elderwood', after: function () {
        loadPage(key).then(function (d) {
          if (cur.type !== 'page' || cur.key !== key) return;
          var host = $('#docHost'); if (!host) return;
          var toc = d.toc || [], hasToc = toc.length >= 3;
          var ps = catPages(c).filter(function (x) { return !x.arch === !p.arch; }), ix = ps.indexOf(p);
          var prev = ps[ix - 1], next = ps[ix + 1];
          host.innerHTML = (hasToc ? '<details class="toc-inline"><summary>Sommaire de la page</summary>' + tocHtml(toc) + '</details>' : '') +
            '<div class="doc-layout"><article class="doc" id="doc" lang="fr">' + d.html + '</article>' +
            (hasToc ? '<aside class="toc-aside" aria-label="Sommaire"><h2>Sommaire</h2>' + tocHtml(toc) + '</aside>' : '') + '</div>' +
            '<nav class="pn" aria-label="Documents voisins">' +
            (prev ? '<a class="prev" href="' + pageHref(prev.k) + '"><small>← Précédent</small>' + esc(prev.t) + '</a>' : '<span></span>') +
            (next ? '<a class="next" href="' + pageHref(next.k) + '"><small>Suivant →</small>' + esc(next.t) + '</a>' : '<span></span>') + '</nav>';
          view.classList.toggle('has-toc', hasToc);
          enhanceDoc($('#doc'), key, anchor, q);
        }).catch(function () {
          var host = $('#docHost'); if (host) host.innerHTML = '<p class="notice">Impossible de charger ce document (<code>data/pages/' + esc(key) + '.js</code>). Vérifiez que le dossier <code>data/</code> est bien publié avec le site.</p>';
        });
      }
    };
  }

  /* ------------------------------------------------------------------ enrichissement d'un document affiché */
  function enhanceDoc(root, key, anchor, q) {
    if (!root) return;
    // ancres de titres
    $$('h2[id],h3[id],h4[id]', root).forEach(function (h) {
      var a = document.createElement('a'); a.className = 'anchor'; a.href = pageHref(key, h.id); a.setAttribute('aria-label', 'Lien vers cette section'); a.textContent = '¶';
      h.appendChild(a);
    });
    enhanceSheets(root);
    enhanceTables(root);
    linkGlossary(root);
    if (q) highlight(root, q);
    setupSpy(root);
    var target = null;
    if (anchor) { target = document.getElementById(anchor); }
    else if (q) { target = $('mark', root); }
    if (target) { revealTab(target); setTimeout(function () { target.scrollIntoView({ block: 'center' }); }, 30); }
  }

  /* feuilles de calcul : un onglet par tableau */
  function activateTab(panel) {
    var root = panel.parentNode;
    $$('.sheet-tab', root).forEach(function (t) { t.hidden = t !== panel; });
    $$('.sheet-tabbar [role=tab]', root).forEach(function (b) { var on = b.getAttribute('data-for') === panel.getAttribute('data-i'); b.setAttribute('aria-selected', on ? 'true' : 'false'); b.tabIndex = on ? 0 : -1; });
  }
  function revealTab(el) { var t = el.closest && el.closest('.sheet-tab'); if (t && t.hidden) activateTab(t); }
  function enhanceSheets(root) {
    var tabs = $$('.sheet-tab', root);
    if (tabs.length < 2) return;
    var bar = document.createElement('div'); bar.className = 'sheet-tabbar'; bar.setAttribute('role', 'tablist'); bar.setAttribute('aria-label', 'Onglets de la feuille');
    tabs.forEach(function (t, i) {
      t.setAttribute('data-i', i); t.setAttribute('role', 'tabpanel');
      var b = document.createElement('button'); b.type = 'button'; b.setAttribute('role', 'tab'); b.setAttribute('data-for', i); b.textContent = t.getAttribute('data-tab') || ('Onglet ' + (i + 1));
      b.addEventListener('click', function () { activateTab(t); });
      b.addEventListener('keydown', function (e) {
        var j = e.key === 'ArrowRight' ? i + 1 : e.key === 'ArrowLeft' ? i - 1 : -1;
        if (j >= 0 && j < tabs.length) { e.preventDefault(); activateTab(tabs[j]); $$('.sheet-tabbar button', root)[j].focus(); }
      });
      bar.appendChild(b);
    });
    tabs[0].parentNode.insertBefore(bar, tabs[0]);
    activateTab(tabs[0]);
  }

  function enhanceTables(root) {
    $$('.tbl-wrap', root).forEach(function (wrap) {
      var t = wrap.querySelector('table'), rows = $$('tbody tr', t);
      var isData = t.classList.contains('data-table');
      if (rows.length < (isData ? 3 : 8)) return;
      t.classList.add('sortable');
      var tools = document.createElement('div'); tools.className = 'tbl-tools';
      tools.innerHTML = '<label>Filtrer le tableau <input type="search" placeholder="Filtrer…" aria-label="Filtrer les lignes du tableau"></label><span class="cnt" aria-live="polite">' + plural(rows.length, 'ligne', 'lignes') + '</span>';
      wrap.parentNode.insertBefore(tools, wrap);
      var input = tools.querySelector('input'), cnt = tools.querySelector('.cnt');
      var cache = rows.map(function (r) { return fold(r.textContent); });
      input.addEventListener('input', function () {
        var v = fold(input.value).trim(), n = 0;
        rows.forEach(function (r, i) { var ok = !v || cache[i].indexOf(v) >= 0; r.hidden = !ok; if (ok) n++; });
        cnt.textContent = v ? n + ' / ' + rows.length + ' lignes' : plural(rows.length, 'ligne', 'lignes');
      });
      $$('thead th', t).forEach(function (th, ci) {
        th.tabIndex = 0;
        var sortIt = function () {
          var dir = th.getAttribute('aria-sort') === 'ascending' ? 'descending' : 'ascending';
          $$('thead th', t).forEach(function (x) { x.removeAttribute('aria-sort'); }); th.setAttribute('aria-sort', dir);
          var body = t.tBodies[0], arr = $$('tr', body);
          var num = arr.every(function (r) { var v = (r.cells[ci] || {}).textContent || ''; return !v.trim() || /^[\s±+\-−]*\d+([.,]\d+)?/.test(v); });
          arr.sort(function (a, b) {
            var x = (a.cells[ci] || {}).textContent || '', y = (b.cells[ci] || {}).textContent || '', r;
            if (num) { r = parseFloat((x.match(/-?\d+([.,]\d+)?/) || [0])[0].toString().replace(',', '.')) - parseFloat((y.match(/-?\d+([.,]\d+)?/) || [0])[0].toString().replace(',', '.')); }
            else r = x.localeCompare(y, 'fr', { numeric: true, sensitivity: 'base' });
            return dir === 'ascending' ? r : -r;
          });
          arr.forEach(function (r) { body.appendChild(r); });
        };
        th.addEventListener('click', sortIt);
        th.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); sortIt(); } });
      });
    });
  }

  function textNodes(root, skip) {
    var out = [], w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        for (var e = n.parentNode; e && e !== root; e = e.parentNode) if (skip.test(e.nodeName) || (e.classList && (e.classList.contains('gl') || e.classList.contains('anchor')))) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    while (w.nextNode()) out.push(w.currentNode);
    return out;
  }
  function highlight(root, q) {
    var toks = Array.from(new Set(Search.words(q))).filter(function (t) { return t.length >= 2 || /\d/.test(t); });
    var re = Search.regexFor(toks); if (!re) return;
    var n = 0;
    textNodes(root, /^(SCRIPT|STYLE|MARK)$/).forEach(function (node) {
      if (n > 400) return;
      var s = node.nodeValue, m, last = 0, frag = null; re.lastIndex = 0;
      while ((m = re.exec(s))) {
        if (!m[0].length) { re.lastIndex++; continue; }
        frag = frag || document.createDocumentFragment();
        frag.appendChild(document.createTextNode(s.slice(last, m.index)));
        var mk = document.createElement('mark'); mk.textContent = m[0]; frag.appendChild(mk); last = m.index + m[0].length; n++;
      }
      if (frag) { frag.appendChild(document.createTextNode(s.slice(last))); node.parentNode.replaceChild(frag, node); }
    });
  }

  /* glossaire : première occurrence de chaque terme, avec infobulle (définition = citation exacte de la source) */
  var glCache = null;
  function glossaryRegex() {
    var entries = GL.filter(function (g) { return g.auto !== false && LEVELS.indexOf(g.a) <= modeIdx(); }), map = {}, list = [];
    entries.forEach(function (g) {
      [g.term].concat(g.aliases || []).forEach(function (t) { var f = fold(t); if (!map[f]) { map[f] = g; list.push(f); } });
    });
    list.sort(function (a, b) { return b.length - a.length; });
    if (!list.length) return null;
    var src = list.map(function (f) {
      var out = '';
      for (var i = 0; i < f.length; i++) {
        var ch = f[i], nx = f[i + 1];
        if (ch === 'o' && nx === 'e') { out += '(?:o[eéèêëē]|œ)'; i++; }
        else if (ch === ' ') out += '\\s+';
        else if (ch === "'") out += "['’]";
        else if (ch === '-') out += '[-‑–]';
        else if ('aeiouycn'.indexOf(ch) >= 0) out += '[' + ({ a: 'aàâäáãåā', e: 'eéèêëē', i: 'iîïíìī', o: 'oôöóòõō', u: 'uùûüúū', c: 'cç', y: 'yÿý', n: 'nñ' })[ch] + ']';
        else out += ch.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      }
      return out;
    }).join('|');
    return { re: new RegExp('(?<![\\p{L}\\p{N}_-])(?:' + src + ')(?![\\p{L}\\p{N}_-])', 'iu'), map: map };
  }
  function linkGlossary(root) {
    if (!GL.length) return;
    var gx = glossaryRegex(); if (!gx) return;
    var seen = {};
    textNodes(root, /^(H1|H2|H3|H4|H5|A|SCRIPT|STYLE|MARK|TH|BUTTON|INPUT)$/).forEach(function (node) {
      if (node.parentNode.closest && node.parentNode.closest('.doc-toc')) return;   // pas de lien dans les sommaires recopiés
      var s = node.nodeValue, pos = 0, frag = null, m, rest;
      while (pos < s.length) {
        rest = s.slice(pos); m = gx.re.exec(rest); if (!m) break;
        var g = gx.map[fold(m[0]).replace(/\s+/g, ' ').replace(/[‑–]/g, '-')] || gx.map[fold(m[0])];
        var start = pos + m.index, end = start + m[0].length;
        if (!g || seen[g.id]) { pos = end; continue; }
        seen[g.id] = 1; frag = frag || document.createDocumentFragment();
        frag.appendChild(document.createTextNode(s.slice(frag._last || 0, start)));
        var sp = document.createElement('span'); sp.className = 'gl'; sp.tabIndex = 0; sp.setAttribute('data-g', g.id); sp.textContent = m[0]; frag.appendChild(sp);
        frag._last = end; pos = end;
      }
      if (frag) { frag.appendChild(document.createTextNode(s.slice(frag._last || 0))); node.parentNode.replaceChild(frag, node); }
    });
  }
  var tip = document.getElementById('glTip'), tipFor = null, tipTimer;
  function glById(id) { for (var i = 0; i < GL.length; i++) if (GL[i].id === id) return GL[i]; return null; }
  function showTip(el) {
    var g = glById(el.getAttribute('data-g')); if (!g) return;
    clearTimeout(tipTimer); tipFor = el;
    var src = pageByKey[g.k];
    tip.innerHTML = '<strong>' + esc(g.term) + '</strong>' + esc(g['def']) +
      '<div class="gl-src">Source : ' + (src && visible(src) ? '<a href="' + pageHref(g.k) + '">' + esc(src.t) + '</a>' : esc(src ? src.t : g.k)) + ' · <a href="#/glossaire?t=' + encodeURIComponent(g.id) + '">Glossaire</a></div>';
    tip.hidden = false;
    var r = el.getBoundingClientRect(), tw = tip.offsetWidth, th = tip.offsetHeight;
    var left = Math.min(Math.max(8, r.left), window.innerWidth - tw - 8), top = r.bottom + 8;
    if (top + th > window.innerHeight - 8) top = Math.max(8, r.top - th - 8);
    tip.style.left = left + 'px'; tip.style.top = top + 'px';
  }
  function hideTip(now) { clearTimeout(tipTimer); tipTimer = setTimeout(function () { tip.hidden = true; tipFor = null; }, now ? 0 : 180); }
  document.addEventListener('mouseover', function (e) { var el = e.target.closest && e.target.closest('.gl'); if (el) showTip(el); else if (e.target.closest && e.target.closest('#glTip')) clearTimeout(tipTimer); });
  document.addEventListener('mouseout', function (e) { if (e.target.closest && (e.target.closest('.gl') || e.target.closest('#glTip'))) hideTip(); });
  document.addEventListener('focusin', function (e) { var el = e.target.closest && e.target.closest('.gl'); if (el) showTip(el); });
  document.addEventListener('focusout', function (e) { if (e.target.closest && e.target.closest('.gl')) hideTip(); });
  document.addEventListener('click', function (e) { var el = e.target.closest && e.target.closest('.gl'); if (el) { if (tipFor === el && !tip.hidden) hideTip(true); else showTip(el); } else if (!(e.target.closest && e.target.closest('#glTip'))) hideTip(true); });
  window.addEventListener('scroll', function () { if (!tip.hidden) hideTip(true); }, { passive: true });

  /* images du wiki : si le chargement échoue (hors ligne, wiki indisponible), le texte reste intact */
  document.addEventListener('error', function (e) { var t = e.target; if (t && t.tagName === 'IMG' && t.classList.contains('wimg')) { t.classList.add('wimg-broken'); t.alt = 'Image non chargée'; } }, true);

  /* sommaire : surbrillance de la section courante */
  var spy = null;
  function setupSpy(root) {
    if (spy) spy.disconnect();
    var links = {}; $$('.toc-aside a[data-id]').forEach(function (a) { links[a.getAttribute('data-id')] = a; });
    var heads = $$('h2[id],h3[id]', root).filter(function (h) { return links[h.id]; });
    if (!heads.length || !('IntersectionObserver' in window)) return;
    var active = null;
    spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { if (active) active.classList.remove('active'); active = links[e.target.id]; if (active) { active.classList.add('active'); var box = active.closest('.toc-aside'); if (box) { var r = active.getBoundingClientRect(), b = box.getBoundingClientRect(); if (r.top < b.top || r.bottom > b.bottom) box.scrollTop += r.top - b.top - 40; } } }
      });
    }, { rootMargin: '-70px 0px -70% 0px', threshold: 0 });
    heads.forEach(function (h) { spy.observe(h); });
  }

  /* ------------------------------------------------------------------ recherche : vue + suggestions */
  function opt(v, label, sel) { return '<option value="' + esc(v) + '"' + (sel ? ' selected' : '') + '>' + esc(label) + '</option>'; }
  function searchView(params) {
    var q = params.get('q') || '', fc = params.get('c') || '', fs = params.get('s') || '', fa = params.get('a') || '';
    var statuses = ['Validé', 'Possibilité de modifier', 'En cours de rédaction', 'À modifier'];
    var h = '<h1 class="page-title">Recherche</h1>' +
      '<form class="filters" id="sform" role="search">' +
      '<label class="grow">Mots à rechercher<input id="sq" type="search" value="' + esc(q) + '" placeholder="ex. Résonance, sanctions, Brumval…" autocomplete="off"></label>' +
      '<label>Section<select id="sc">' + opt('', 'Toutes', !fc) + visibleCats().map(function (c) { return opt(c.name, c.name, c.name === fc); }).join('') + '</select></label>' +
      '<label>Statut<select id="ss">' + opt('', 'Tous', !fs) + statuses.map(function (s) { return opt(s, s, s === fs); }).join('') + opt('none', 'Statut non documenté', fs === 'none') + '</select></label>' +
      '<label>Accès<select id="sa">' + opt('', 'Tous (niveau affiché)', !fa) + LEVELS.slice(0, modeIdx() + 1).map(function (l) { return opt(l, LNAME[l], l === fa); }).join('') + '</select></label>' +
      '<button class="btn" type="submit">Rechercher</button></form>' +
      '<div id="sres"><p class="loading">Préparation de l\'index de recherche…</p></div>';
    return {
      html: h, title: 'Recherche — Elderwood', after: function () {
        var go = function () {
          var u = new URLSearchParams(); var v = { q: $('#sq').value.trim(), c: $('#sc').value, s: $('#ss').value, a: $('#sa').value };
          Object.keys(v).forEach(function (k) { if (v[k]) u.set(k, v[k]); });
          location.hash = '#/recherche' + (u.toString() ? '?' + u.toString() : '');
        };
        $('#sform').addEventListener('submit', function (e) { e.preventDefault(); go(); });
        ['sc', 'ss', 'sa'].forEach(function (id) { $('#' + id).addEventListener('change', go); });
        $('#sq').focus({ preventScroll: true });
        Search.ready().then(function () {
          if (cur.type !== 'search') return;
          var r = Search.run(q, { c: fc, s: fs, a: fa }), shown = 0, step = 25;
          var box = $('#sres'); if (!box) return;
          var head = '<p class="result-meta" role="status">' + plural(r.results.length, 'document trouvé', 'documents trouvés') + (q ? ' pour « ' + esc(q) + ' »' : '') +
            (r.partial ? ' — aucun document ne contient tous les mots ; résultats partiels affichés.' : '') + '</p>';
          if (!r.results.length) { box.innerHTML = head + '<div class="empty">Aucun résultat. Essayez d\'autres mots, retirez un filtre ou passez au niveau « Staff » (menu en haut à droite) pour inclure les documents staff.</div>'; return; }
          box.innerHTML = head + '<ul class="list" id="rlist"></ul><p><button class="btn ghost" id="more" type="button" hidden>Afficher plus de résultats</button></p>';
          var list = $('#rlist'), more = $('#more');
          function add() {
            var html = '';
            r.results.slice(shown, shown + step).forEach(function (x) { html += itemHtml(pageByKey[x.k], q ? { html: Search.snippet(x.i, r.toks), q: q } : null); });
            list.insertAdjacentHTML('beforeend', html); shown = Math.min(r.results.length, shown + step); more.hidden = shown >= r.results.length;
          }
          more.addEventListener('click', add); add();
        });
      }
    };
  }

  var sg = { box: null, input: null, items: [], idx: -1, token: 0 };
  function initSuggest() {
    sg.box = $('#suggest'); sg.input = $('#q');
    var doSuggest = debounce(function () {
      var q = sg.input.value.trim(), tk = ++sg.token;
      if (q.length < 2) { closeSuggest(); return; }
      openSuggest('<div class="sg-empty">Recherche…</div>');
      Search.ready().then(function () {
        if (tk !== sg.token) return;
        var r = Search.run(q, {}), top = r.results.slice(0, 7);
        if (!top.length) { openSuggest('<div class="sg-empty">Aucun résultat pour « ' + esc(q) + ' ».</div><div class="sg-foot">Les documents staff ne sont pas inclus dans ce niveau d\'affichage.</div>'); sg.items = []; return; }
        sg.items = top.map(function (x) { return x.k; });
        var h = top.map(function (x, i) {
          var p = pageByKey[x.k];
          return '<a class="sg-item" role="option" id="sg' + i + '" aria-selected="false" href="' + pageHref(p.k, '', q) + '"><div class="sg-title">' + esc(p.t) + '<span class="sg-cat">' + esc(p.c) + '</span></div><div class="sg-snip">' + Search.snippet(x.i, r.toks, 150) + '</div></a>';
        }).join('') + '<div class="sg-foot">' + plural(r.results.length, 'résultat', 'résultats') + ' — Entrée pour tout afficher avec filtres</div>';
        openSuggest(h); sg.idx = -1;
      });
    }, 90);
    sg.input.addEventListener('input', doSuggest);
    sg.input.addEventListener('focus', function () { Search.ready(); if (sg.input.value.trim().length >= 2) doSuggest(); });
    sg.input.addEventListener('keydown', function (e) {
      var els = $$('.sg-item', sg.box);
      if (e.key === 'ArrowDown' && els.length) { e.preventDefault(); sg.idx = (sg.idx + 1) % els.length; mark(els); }
      else if (e.key === 'ArrowUp' && els.length) { e.preventDefault(); sg.idx = (sg.idx - 1 + els.length) % els.length; mark(els); }
      else if (e.key === 'Escape') { closeSuggest(); }
      else if (e.key === 'Enter') {
        e.preventDefault();
        if (sg.idx >= 0 && els[sg.idx]) { location.hash = els[sg.idx].getAttribute('href'); closeSuggest(); }
        else { location.hash = '#/recherche?q=' + encodeURIComponent(sg.input.value.trim()); closeSuggest(); }
      }
    });
    document.addEventListener('click', function (e) { if (!e.target.closest('.search-box')) closeSuggest(); });
    sg.box.addEventListener('click', function (e) { if (e.target.closest('.sg-item')) closeSuggest(); });
    function mark(els) { els.forEach(function (el, i) { el.setAttribute('aria-selected', i === sg.idx ? 'true' : 'false'); }); if (els[sg.idx]) { els[sg.idx].scrollIntoView({ block: 'nearest' }); sg.input.setAttribute('aria-activedescendant', els[sg.idx].id); } }
  }
  function openSuggest(h) { sg.box.innerHTML = h; sg.box.hidden = false; sg.input.setAttribute('aria-expanded', 'true'); }
  function closeSuggest() { sg.box.hidden = true; sg.input.setAttribute('aria-expanded', 'false'); sg.token++; }

  /* ------------------------------------------------------------------ glossaire (page) */
  function glossaryView(params) {
    var entries = GL.filter(function (g) { return LEVELS.indexOf(g.a) <= modeIdx(); }), letters = {};
    entries.forEach(function (g) { letters[fold(g.term)[0].toUpperCase()] = 1; });
    var h = '<h1 class="page-title">Glossaire</h1><p class="result-meta">' + plural(entries.length, 'terme', 'termes') + '. Chaque définition est une citation exacte d\'un document du site (la source est indiquée), jamais une reformulation.</p>' +
      '<div class="filters"><label class="grow">Filtrer les termes<input id="gq" type="search" placeholder="ex. Flux, maison, runes…" autocomplete="off"></label></div>' +
      '<div class="az" id="az">' + Object.keys(letters).sort().map(function (l) { return '<button type="button" data-l="' + l + '">' + l + '</button>'; }).join('') + '</div><div id="glist"></div>';
    return {
      html: h, title: 'Glossaire — Elderwood', after: function () {
        var letter = '', gq = $('#gq'), want = params.get('t') || '';
        function draw() {
          var v = fold(gq.value).trim(), html = '';
          entries.forEach(function (g) {
            var hay = fold(g.term + ' ' + (g.aliases || []).join(' ') + ' ' + g['def'] + ' ' + (g.cat || ''));
            if (v && hay.indexOf(v) < 0) return;
            if (letter && fold(g.term)[0].toUpperCase() !== letter) return;
            var src = pageByKey[g.k];
            html += '<article class="gl-entry" id="g-' + esc(g.id) + '"><h3>' + esc(g.term) + '<small>' + esc(g.cat || '') + (g.aliases && g.aliases.length ? ' · aussi : ' + esc(g.aliases.join(', ')) : '') + '</small></h3>' +
              '<blockquote>' + esc(g['def']) + '</blockquote><div class="src">Source : ' + (src && visible(src) ? '<a href="' + pageHref(g.k) + '">' + esc(src.t) + '</a>' : esc(src ? src.t : g.k)) +
              (g.pages && g.pages.length ? ' · Voir aussi : ' + g.pages.filter(function (k) { return pageByKey[k] && visible(pageByKey[k]); }).map(function (k) { return '<a href="' + pageHref(k) + '">' + esc(pageByKey[k].t) + '</a>'; }).join(', ') : '') + '</div></article>';
          });
          $('#glist').innerHTML = html || '<div class="empty">Aucun terme.</div>';
        }
        gq.addEventListener('input', draw);
        $$('#az button').forEach(function (b) { b.addEventListener('click', function () { var l = b.getAttribute('data-l'); letter = letter === l ? '' : l; $$('#az button').forEach(function (x) { x.classList.toggle('on', x.getAttribute('data-l') === letter); }); draw(); }); });
        draw();
        if (want) { var el = document.getElementById('g-' + want); if (el) { el.scrollIntoView({ block: 'center' }); el.style.outline = '2px solid var(--gold)'; } }
      }
    };
  }

  /* ------------------------------------------------------------------ contradictions connues / contenu non disponible */
  function contraView() {
    var h = '<h1 class="page-title">Contradictions connues</h1><p class="result-meta">Quand deux documents se contredisent, le site affiche les deux passages tels quels et ne tranche pas. Les extraits sont des citations exactes ; la mention « Signalé » reprend l\'information transmise avec le dossier.</p>';
    CONTRA.forEach(function (c) {
      var shown = c.items.filter(function (i) { return LEVELS.indexOf(i.a) <= modeIdx(); }), hid = c.items.length - shown.length;
      var links = c.links.filter(function (l) { return LEVELS.indexOf(l.a) <= modeIdx(); });
      h += '<section class="contra"><h2>' + esc(c.titre) + '</h2><p><strong>Signalé :</strong> ' + esc(c.note) + '</p>' +
        shown.map(function (i) {
          var p = pageByKey[i.k];
          return '<blockquote>' + esc(i.text) + '</blockquote><p class="src">Source : <a href="' + pageHref(i.k) + '">' + esc(p.t) + '</a> ' + accessBadge(p) + '</p>';
        }).join('') +
        (hid ? '<p class="nd">' + plural(hid, 'extrait provient', 'extraits proviennent') + ' de documents d\'un niveau supérieur (passez au niveau « Staff » pour les voir).</p>' : '') +
        (links.length ? '<p>Documents concernés : ' + links.map(function (l) { return '<a href="' + pageHref(l.k) + '">' + esc(pageByKey[l.k].t) + '</a>'; }).join(' · ') + '</p>' : '') +
        (c.check && shown.length ? '<p class="check"><strong>Constat sur cet instantané :</strong> ' + esc(c.check) + '</p>' : '') + '</section>';
    });
    return { html: h, title: 'Contradictions connues — Elderwood' };
  }
  function missingView() {
    var h = '<h1 class="page-title">Contenu non disponible</h1><p class="result-meta">Ces documents n\'ont <strong>pas pu être lus</strong> : ils ne sont pas repris sur ce site et rien n\'est supposé de leur contenu.</p>' +
      '<div class="doc"><h2>Hors de portée de l\'export</h2><ul>' +
      '<li>Cinq guides Notion de suivis MJ : Notion exige JavaScript, le contenu n\'a pas pu être récupéré.</li>' +
      '<li>Organigramme des métiers : document Canva, non lisible par export.</li>' +
      '<li>Organigramme légal : document Miro, non lisible par export.</li></ul>' +
      '<h2>Non partagés avec le compte utilisé pour l\'export</h2><ul>' +
      '<li>Boucles RP school</li><li>B.R.U.M.E</li><li>Guide candidatures naissance famille</li><li>Suivi familles non officielles</li><li>Suivi des lieux in-game</li></ul>' +
      '<p>Contenu de chacun : <span class="nd">non documenté</span>. Dès qu\'un de ces documents est partagé ou exporté, il peut être ajouté (voir le README).</p></div>';
    return { html: h, title: 'Contenu non disponible — Elderwood' };
  }

  /* ------------------------------------------------------------------ à propos */
  function aboutView() {
    var rows = M.categories.map(function (c) {
      var all = c.keys.length, vis = catPages(c).length;
      return '<tr><td>' + esc(c.name) + '</td><td>' + all + '</td><td>' + vis + '</td></tr>';
    }).join('');
    var lv = LEVELS.slice(0, maxAudience + 1).map(function (l) { return '<tr><td>' + accessBadge({ a: l }) + '</td><td>' + M.pages.filter(function (p) { return p.a === l; }).length + '</td></tr>'; }).join('');
    var h = '<h1 class="page-title">À propos & sources</h1>' +
      '<div class="doc"><p>Cette bibliothèque reprend, sans résumé ni reformulation, les documents de travail du serveur RP Elderwood (lore, règlements, outils du pôle RP) ainsi que son wiki public. ' + esc(M.snapshot) + ' : les documents d\'origine continuent d\'évoluer.</p>' +
      '<h2>Niveaux d\'accès</h2><p>Chaque page porte un badge <em>Public</em>, <em>Joueurs</em> ou <em>Staff</em>. Le sélecteur en haut à droite choisit le niveau affiché : par défaut « Joueurs », les documents staff n\'apparaissent ni dans la navigation, ni sur l\'accueil, ni dans la recherche. Dans le doute, un document est classé « Staff ». <strong>Ce filtre n\'est pas une protection</strong> : pour publier sans les pages staff, générer la version « joueurs » ou « public » (voir le README).</p>' +
      '<h2>Statuts de rédaction</h2><div class="badges"><span class="badge s-valide">Validé</span><span class="badge s-possible">Possibilité de modifier</span><span class="badge s-encours">En cours de rédaction</span><span class="badge s-amodifier">À modifier</span><span class="badge s-none">Statut non documenté</span></div>' +
      '<h2>À savoir</h2><ul><li>Plusieurs versions d\'un même document coexistent (Brumval v1 à v4, Aerwyn v1/v2, copies du Pacte du Voile, brouillons de Constitution) : la version la plus récente est listée en premier, les anciennes sont rangées dans « Archives ».</li>' +
      '<li>Des contradictions entre documents sont possibles (par exemple règlement et lore) : le site ne tranche pas.</li>' +
      '<li>Les feuilles de calcul ne sont reprises qu\'en valeurs, et seulement le premier onglet pour certaines.</li>' +
      '<li>Une information absente de la source est affichée « non documenté ».</li>' +
      '<li>Les fiches de candidature individuelles, les adresses e-mail et les pseudos Discord des tableaux ne sont pas publiés.</li></ul>' +
      '<h2>Documents non intégrés</h2><p>Plusieurs documents n\'ont pas pu être lus : voir <a href="#/non-disponible">Contenu non disponible</a>. Les divergences entre documents sont listées dans <a href="#/contradictions">Contradictions connues</a>.</p>' +
      '<h2>Wiki officiel</h2><p>La section « Wiki officiel WikiWood (public) » reprend les pages du wiki public (wiki.elderwood-rp.com) dans leur arborescence d\'origine. Le wiki change souvent : cette copie est un instantané. Les images du wiki sont chargées depuis le wiki lui-même.</p>' +
      '<h2>Contrôle des volumes</h2><p>' + plural(M.count, 'page', 'pages') + ' dans ce build ; ' + plural(visiblePages().length, 'page affichée', 'pages affichées') + ' au niveau « ' + esc(LNAME[mode]) + ' ».</p>' +
      '<div class="tbl-wrap"><table class="doc-table"><thead><tr><th>Niveau</th><th>Pages</th></tr></thead><tbody>' + lv + '</tbody></table></div>' +
      '<div class="tbl-wrap"><table class="doc-table"><thead><tr><th>Section</th><th>Pages (build)</th><th>Pages affichées</th></tr></thead><tbody>' + rows + '</tbody></table></div></div>';
    return { html: h, title: 'À propos — Elderwood' };
  }

  /* ------------------------------------------------------------------ routage */
  function parseHash() {
    var raw = location.hash.replace(/^#/, ''), qi = raw.indexOf('?'), path = qi >= 0 ? raw.slice(0, qi) : raw, qs = qi >= 0 ? raw.slice(qi + 1) : '';
    var parts = path.split('/').filter(Boolean).map(function (x) { try { return decodeURIComponent(x); } catch (e) { return x; } });
    return { parts: parts, params: new URLSearchParams(qs) };
  }
  var lastKey = null;
  function route() {
    var r = parseHash(), p = r.parts, out, scrollTop = true;
    closeNav();
    var routeKey = p.slice(0, 2).join('/');
    if (p[0] === 'p' && p[1]) {
      cur = { type: 'page', key: p[1] };
      if (lastKey === routeKey && $('#doc') && p[2] && !r.params.get('q')) { var t = document.getElementById(p[2]); if (t) { revealTab(t); t.scrollIntoView({ block: 'start' }); renderSidebar(cur); return; } }
      out = pageView(p[1], p[2], r.params.get('q')); scrollTop = !p[2];
    } else if (p[0] === 'c' && p[1]) { cur = { type: 'cat', slug: p[1] }; out = catView(p[1]); }
    else if (p[0] === 'recherche') { cur = { type: 'search' }; out = searchView(r.params); }
    else if (p[0] === 'glossaire') { cur = { type: 'gloss' }; out = glossaryView(r.params); }
    else if (p[0] === 'a-propos') { cur = { type: 'about' }; out = aboutView(); }
    else if (p[0] === 'contradictions') { cur = { type: 'contra' }; out = contraView(); }
    else if (p[0] === 'non-disponible') { cur = { type: 'missing' }; out = missingView(); }
    else { cur = { type: 'home' }; out = homeView(); }
    lastKey = routeKey;
    view.classList.remove('has-toc');
    view.innerHTML = out.html;
    document.title = out.title || M.title;
    renderSidebar(cur);
    if (scrollTop) window.scrollTo(0, 0);
    if (out.after) out.after();
    if (cur.type !== 'search') $('#q').value = $('#q').value;   // conserve la saisie
    var m = $('#main'); if (m && scrollTop) { m.focus({ preventScroll: true }); }
  }

  /* ------------------------------------------------------------------ interface : thème, niveau, menu */
  function closeNav() { document.body.classList.remove('nav-open'); $('#scrim').hidden = true; $('#menuBtn').setAttribute('aria-expanded', 'false'); }
  function setMode(m) {
    mode = m; store('ew-mode', m); $('#modeSel').value = m; footer(); glCache = null;
    var wasPage = cur.type === 'page'; lastKey = null; route();
    if (!wasPage) window.scrollTo(0, 0);
  }
  function footer() {
    $('#footStats').textContent = plural(visiblePages().length, 'document affiché', 'documents affichés') + ' sur ' + M.count;
    $('#footSnap').textContent = M.snapshot;
  }
  function init() {
    var sel = $('#modeSel');
    sel.innerHTML = LEVELS.slice(0, maxAudience + 1).map(function (l) { return '<option value="' + l + '">' + esc(LNAME[l]) + '</option>'; }).join('');
    sel.value = mode;
    if (maxAudience === 0) $('.mode').hidden = true;
    sel.addEventListener('change', function () { setMode(sel.value); });
    $('#themeBtn').addEventListener('click', function () {
      var t = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', t); store('ew-theme', t);
    });
    $('#printBtn').addEventListener('click', function () { window.print(); });
    $('#menuBtn').addEventListener('click', function () {
      var open = !document.body.classList.contains('nav-open');
      document.body.classList.toggle('nav-open', open); $('#scrim').hidden = !open; $('#menuBtn').setAttribute('aria-expanded', String(open));
    });
    $('#scrim').addEventListener('click', closeNav);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { closeNav(); hideTip(true); }
      if (e.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test((document.activeElement || {}).nodeName)) { e.preventDefault(); $('#q').focus(); }
    });
    window.addEventListener('beforeprint', function () { $$('details').forEach(function (d) { d.setAttribute('data-was', d.open ? '1' : '0'); d.open = true; }); });
    window.addEventListener('afterprint', function () { $$('details[data-was]').forEach(function (d) { d.open = d.getAttribute('data-was') === '1'; d.removeAttribute('data-was'); }); });
    initSuggest(); footer();
    window.addEventListener('hashchange', route);
    route();
  }
  window.EWApp = { Search: Search, setMode: setMode, visiblePages: visiblePages, manifest: M };
  init();
})();
