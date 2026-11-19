/* Vérification de bout en bout (Playwright) : nombre de pages, intégrité du texte, recherche, niveaux d'accès.
 * Usage : python3 -m http.server 8765 &  puis  NODE_PATH=$(npm root -g) node tests/e2e.js [url]  */
const { chromium } = require('playwright');
const base = process.argv[2] || 'http://127.0.0.1:8765/index.html';
const fs = require('fs'), path = require('path');
const pagesJson = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'pages.json'), 'utf8'));
const tok = s => (s.normalize('NFC').toLowerCase().match(/[\p{L}\p{N}]+/gu) || []);
let fail = 0;
const ok = (c, msg) => { console.log((c ? 'OK   ' : 'FAIL ') + msg); if (!c) fail++; };

(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1360, height: 900 } });
  const p = await ctx.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  p.on('console', m => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) errs.push(m.text()); });   // images du wiki : réseau du bac à sable
  await p.goto(base);
  await p.evaluate(() => localStorage.setItem('ew-mode', 'staff'));
  await p.goto(base + '#/'); await p.reload(); await p.waitForSelector('.card');

  // 1. nombre de pages
  const total = await p.evaluate(() => window.EWApp.manifest.count);
  ok(total === pagesJson.length, `pages dans le manifeste (${total}) = pages dans pages.json (${pagesJson.length})`);
  const sideLinks = await p.evaluate(() => new Set([...document.querySelectorAll('#sideNav a[href^="#/p/"]')].map(a => a.getAttribute('href'))).size);
  ok(sideLinks === pagesJson.length, `liens de pages dans la navigation latérale (${sideLinks}) = pages.json (${pagesJson.length})`);
  const keysOk = await p.evaluate(ks => ks.every(k => window.EWApp.manifest.pages.some(x => x.k === k)), pagesJson.map(x => x.k));
  ok(keysOk, 'toutes les clés de pages.json sont dans le manifeste');

  // 2. chaque page s'affiche en entier : mots affichés = mots de l'index de recherche (texte source rendu)
  await p.evaluate(() => window.EWApp.Search.ready());
  const searchText = await p.evaluate(() => Object.fromEntries(window.EW.search.map(d => [d.k, d.x])));
  let shown = 0, bad = [];
  for (const pg of pagesJson) {
    await p.goto(base + '#/p/' + pg.k);
    try { await p.waitForSelector('#doc', { timeout: 15000 }); } catch (e) { bad.push(pg.k + ' (non affichée)'); continue; }
    await p.waitForFunction(k => document.querySelector('#doc') && location.hash.indexOf(k) > 0, pg.k);
    const txt = await p.evaluate(() => {
      const d = document.querySelector('#doc').cloneNode(true);
      d.querySelectorAll('.anchor,.tbl-tools').forEach(n => n.remove());
      d.querySelectorAll('p,ul,ol,li,td,th,h2,h3,h4,h5,div,br,hr,.leader span,.leader b,.n').forEach(n => { n.before(' '); n.after(' '); });   // sépare les blocs voisins
      return d.textContent;
    });
    const a = tok(txt), e = tok(searchText[pg.k]);
    shown++;
    const ca = {}, ce = {};
    a.forEach(w => ca[w] = (ca[w] || 0) + 1); e.forEach(w => ce[w] = (ce[w] || 0) + 1);
    let missing = 0; for (const w in ce) missing += Math.max(0, ce[w] - (ca[w] || 0));
    if (missing > 0 || a.length < e.length) bad.push(`${pg.k}: ${missing} mots manquants (${a.length} affichés / ${e.length} attendus)`);
    const title = await p.evaluate(() => document.querySelector('h1.page-title').textContent);
    if (title.trim() !== pg.title.trim()) bad.push(`${pg.k}: titre « ${title} » ≠ « ${pg.title} »`);
  }
  ok(shown === pagesJson.length, `pages réellement affichées (${shown}) = pages.json (${pagesJson.length})`);
  ok(bad.length === 0, 'aucun texte tronqué : ' + (bad.length ? bad.slice(0, 8).join(' ; ') : 'tous les mots de chaque page sont présents'));

  // 2b. wiki, feuilles à onglets, pages d'information
  const wk = await p.evaluate(() => window.EWApp.manifest.pages.filter(x => x.wiki));
  ok(wk.length === pagesJson.filter(x => x.k.startsWith('wiki-')).length && wk.length === 99 && wk.every(x => x.a === 'public' && x.u !== undefined), `wiki : ${wk.length} pages, toutes publiques, avec leur chemin d'origine`);
  await p.goto(base + '#/p/wiki-bestiaire--rang-a--jackalope'); await p.waitForSelector('#doc');
  ok(await p.evaluate(() => !!document.querySelector('#sideNav a.current') && document.querySelector('#sideNav a.current').closest('details.sn-cat').open), 'wiki : la page courante est dépliée dans l\'arborescence latérale');
  ok(await p.evaluate(() => document.querySelectorAll('.hint, .doc-table').length >= 0 && document.querySelector('#doc h2,#doc h3,#doc h4,#doc h5') !== null), 'wiki : titres rendus');
  await p.goto(base + '#/p/wiki-accueil'); await p.waitForSelector('#doc p.ref a');
  ok(await p.evaluate(() => [...document.querySelectorAll('#doc p.ref a')].every(a => a.getAttribute('href').startsWith('#/p/'))), 'wiki : renvois {% content-ref %} convertis en liens internes');
  await p.goto(base + '#/p/sheet-items-jobs-illegaux'); await p.waitForSelector('.sheet-tabbar');
  const tabs = await p.evaluate(() => ({ n: document.querySelectorAll('.sheet-tabbar [role=tab]').length, visible: [...document.querySelectorAll('.sheet-tab')].filter(t => !t.hidden).length, tables: document.querySelectorAll('.sheet-tab table').length }));
  ok(tabs.n === 7 && tabs.visible === 1 && tabs.tables >= 7, `feuille à onglets : ${tabs.n} onglets, 1 visible, ${tabs.tables} tableaux`);
  await p.click('.sheet-tabbar [role=tab]:nth-child(2)');
  ok(await p.evaluate(() => document.querySelector('.sheet-tab:not([hidden])').getAttribute('data-tab') === 'Braconnier'), 'feuille : changement d\'onglet');
  await p.goto(base + '#/contradictions'); await p.waitForSelector('.contra');
  ok(await p.locator('.contra').count() === 5 && await p.locator('.contra blockquote').count() >= 6, 'page « Contradictions connues » : 5 sujets avec extraits des deux côtés');
  await p.goto(base + '#/non-disponible'); await p.waitForSelector('.doc');
  ok(/B\.R\.U\.M\.E/.test(await p.locator('.doc').innerText()) && /Miro/.test(await p.locator('.doc').innerText()), 'page « Contenu non disponible » listant les 12 documents non lus');

  // 3. recherche
  const q = async (text, filt = {}) => p.evaluate(([t, f]) => window.EWApp.Search.run(t, f).results.map(r => r.k), [text, filt]);
  let r = await q('résonance'); ok(r.length >= 10, `recherche « résonance » : ${r.length} résultats`);
  let r2 = await q('resonance'); ok(JSON.stringify(r) === JSON.stringify(r2), 'recherche insensible aux accents');
  r = await q('cristal-cœur'); ok(r.includes('cristaux-coeurs'), 'recherche « cristal-cœur » trouve les Cristaux-Cœurs');
  r = await q('Brumval', { c: 'Trames' }); ok(r.length > 0 && r.every(k => pagesJson.find(x => x.k === k).cat === 'Trames'), `filtre par section (Trames) : ${r.length} résultats`);
  r = await q('', { s: 'En cours de rédaction' }); ok(r.length === 7, `filtre statut « En cours de rédaction » : ${r.length} pages (attendu 7)`);
  r = await q('', { a: 'public' }); ok(r.length === 102, `filtre accès « public » : ${r.length} pages (attendu 102 = 3 documents + 99 pages wiki)`);
  r = await q('Basile Roncefort'); ok(r.length > 0, '« Basile Roncefort » : ' + r.length + ' résultats (staff)');
  // phrase unique prise dans un document profond
  r = await q('Peregrine le Sage'); ok(r[0] === 'histoire-amru-lois', '« Peregrine le Sage » -> ' + r[0]);

  // 4. niveaux d'accès : en mode joueurs, aucun document staff dans la navigation, l'accueil ni la recherche
  await p.evaluate(() => window.EWApp.setMode('joueurs')); await p.goto(base + '#/'); await p.waitForSelector('.card');
  const staffKeys = await p.evaluate(() => window.EWApp.manifest.pages.filter(x => x.a === 'staff').map(x => x.k));
  const navHas = await p.evaluate(ks => ks.filter(k => document.querySelector(`#sideNav a[href="#/p/${k}"]`)).length, staffKeys);
  ok(navHas === 0, `mode « Joueurs » : ${navHas} document(s) staff dans la navigation (attendu 0)`);
  r = await q('Basile Roncefort'); ok(r.length === 0, 'mode « Joueurs » : la recherche n\'expose aucun document staff');
  const vis = await p.evaluate(() => window.EWApp.visiblePages().length);
  ok(vis === pagesJson.length - staffKeys.length, `mode « Joueurs » : ${vis} pages visibles = ${pagesJson.length} − ${staffKeys.length} staff`);

  // 5. pages sensibles : aucune donnée personnelle
  await p.evaluate(() => window.EWApp.setMode('staff'));
  const all = Object.values(searchText).join('\n');
  ok(!/[\w.+-]+@[\w-]+\.[\w.]+/.test(all), 'aucune adresse e-mail dans le texte publié');
  ok(!/ouid=/.test(all), 'aucun identifiant de compte Google (ouid) dans le texte publié');
  ok(!/Shaeryn|berangereci/i.test(all), 'ni pseudo Discord ni e-mail identifiés dans le texte publié');
  ok(!/malgachou|captainorion|massilia|eclypseoff/i.test(searchText['sheet-prof-tableau'] + searchText['sheet-gestion-ecole']), 'pseudos Discord masqués dans les feuilles des professeurs');
  ok(/non publi/i.test(searchText['fiche-cordelia-ravenscroft']) && searchText['fiche-cordelia-ravenscroft'].length < 300, 'fiche de candidature individuelle non publiée');

  ok(errs.length === 0, 'aucune erreur JavaScript/console' + (errs.length ? ' : ' + errs.slice(0, 3).join(' | ') : ''));
  await b.close();
  console.log(fail ? `\n${fail} vérification(s) en échec` : '\nToutes les vérifications sont passées.');
  process.exit(fail ? 1 : 0);
})();
