# Elderwood — bibliothèque du lore et règlement

Site **statique** (HTML / CSS / JS, aucun backend, aucune dépendance externe) qui affiche, directement lisibles, les 113 documents du pôle RP : règlements, lore, magie, créatures, familles, droit, métiers, trames, suivis MJ, outils staff…

- Accueil par grandes sections, navigation latérale, fil d'Ariane, sommaire automatique par page.
- Recherche plein texte instantanée (index construit dans le navigateur) avec filtres section / statut / accès.
- Glossaire (page + infobulles dans le texte) dont chaque définition est une **citation exacte** d'un document.
- Mode sombre / clair, mobile, impression propre.
- Badges de statut de rédaction et de niveau d'accès (public / joueurs / staff) sur chaque page.

## Structure

```
elderwood-site/
├── index.html            coquille de l'application
├── assets/               style.css, app.js
├── content/*.md          UNE page = UN fichier (en-tête de métadonnées, « --- », texte intégral)
├── pages.json            liste des pages (clé, section, titre, métadonnées)
├── config/
│   ├── site.json         ordre des sections, groupes de l'accueil, niveaux d'accès, archives, confidentialité
│   └── glossary.json     termes du glossaire (citations exactes + pages liées)
├── build.py              génère data/ à partir de content/ + pages.json (Python 3, bibliothèque standard)
├── data/                 GÉNÉRÉ : manifest.js, search.js, glossary.js, pages/<clé>.js
└── tests/e2e.js          vérification complète dans un navigateur (Playwright)
```

`data/` est déjà généré et versionné : le dossier est **prêt à héberger** tel quel sur n'importe quel hébergement statique (GitHub Pages, Netlify, Apache, Nginx…). Les données sont chargées par balises `<script>` : l'ouverture directe de `index.html` fonctionne aussi.

## Essayer en local

```bash
cd elderwood-site
python3 -m http.server 8765      # puis ouvrir http://127.0.0.1:8765/
```

## Ajouter ou mettre à jour une page

**Mettre à jour** : modifier `content/<clé>.md` (texte après la ligne `---`), puis `python3 build.py --check`.

**Ajouter** :

1. Créer `content/<clé>.md` :
   ```
   # Titre du document

   - Catégorie : Magie & maladies
   - Statut de rédaction : Validé
   - Mots-clés : mot1, mot2
   - Résumé officiel : …
   - Responsable : …
   - Niveau d’accès : Restreint, sur autorisation
   - Remarques : …

   ---

   Texte intégral du document…
   ```
   Les lignes de métadonnées absentes s'affichent « non documenté ».
2. Ajouter l'entrée dans `pages.json` : `{"k": "<clé>", "cat": "Magie & maladies", "title": "Titre", "m": {"red": "Validé", "kw": "mot1, mot2", "res": "…", "resp": "…", "acc": "…", "rem": "…", "dom": "Lore"}}` (`m` peut rester `{}`).
3. Facultatif, dans `config/site.json` : place dans la section (`order`), niveau d'accès (`access.public` / `access.joueurs`, **tout le reste est « staff »**), ancienne version (`archives`).
4. `python3 build.py --check` — le script s'arrête avec une erreur si `pages.json` et `content/` divergent, ou si un mot de la source n'apparaît pas dans la page générée.

Formats de texte reconnus : texte exporté de Google Docs (titres déduits : MAJUSCULES, « I. », « 1.2 », « Article 3. », « § 4 — », lignes courtes entre blancs ; puces ; numérotations ; **tableaux aplatis par l'export, reconstruits en vrais `<table>`**), feuilles de calcul (`##### FEUILLE: nom` + lignes `a | b | c`, ou CSV), tableaux Markdown/pandoc, `**gras**`, liens http(s). Le texte n'est jamais modifié : seule la mise en forme est déduite.

## Niveaux d'accès

Chaque page a un niveau : **public**, **joueurs** ou **staff** (badge sur la page, dans la fiche, filtre de recherche). Le sélecteur en haut à droite choisit l'affichage (par défaut « Joueurs ») : les pages staff ne sont ni dans la navigation, ni sur l'accueil, ni dans la recherche, ni dans le glossaire.

Classement appliqué (règle du brief, « en cas de doute : staff ») :

- **public** (3) : règlement intérieur élèves, commandes & raccourcis (×2) ;
- **joueurs** (23) : Bible du lore, Bestiaire, Encyclopédie draconique, Brûlebrume, Runomancie (lore + accords), Catalyseurs, Cristaux-Cœurs, Échoïde, Maladies magiques (v4), Objets magiques, Potions (×2), Sorts en jeu, Malédictions, Shedwood, 6 lores de familles « joueurs », règlement des professeurs ;
- **staff** (87) : tout le reste.

À valider : la Constitution et le Pacte du Voile sont « staff » faute de statut « Validé » (le brief les ouvre « une fois validée ») ; plusieurs documents *Validé* hors liste du brief sont aussi restés « staff » (Créatures des Maisons, Balais magiques, Matériaux des catalyseurs, Histoire de l'AMRU, métiers légaux et illégaux…). Pour en ouvrir un : l'ajouter à `access.joueurs` ou `access.public` dans `config/site.json`.

> ⚠️ **Le sélecteur n'est pas une protection d'accès** : toutes les pages sont dans `data/`. Pour une publication réellement ouverte, générez une version qui **ne contient pas** les pages staff :
> ```bash
> python3 build.py --audience joueurs   # → dist/joueurs/ (26 pages)
> python3 build.py --audience public    # → dist/public/  (3 pages)
> ```
> `dist/<niveau>/` est autonome (ni `content/` ni pages réservées) : c'est ce dossier qu'il faut publier.

## Confidentialité

Appliqué automatiquement par `build.py` (voir `config/site.json`, rubriques `redactions` et `withheld`) :

- la **fiche de candidature individuelle** `fiche-cordelia-ravenscroft` (données personnelles d'un joueur) n'est pas publiée : la page existe (pour que le décompte reste 113) mais indique « contenu non publié » — retirer la clé de `withheld` pour la republier ;
- adresses e-mail (une dans « Organisation Pôle RP – Familles », une adresse de groupe dans « Balais magiques ») remplacées par « [adresse e-mail non publiée] » ;
- pseudos Discord des colonnes « Discord » / « Contact » des feuilles (liste des professeurs, Gestion de l'école…) remplacés par « [non publié] » ;
- paramètres d'URL Google contenant un identifiant de compte (`ouid=…`) retirés.

Le rapport de `python3 build.py` liste chaque masquage. Les pseudos de staff de la colonne « Pseudo » (effectifs du pôle RP) sont conservés (pages staff).

## Glossaire

`config/glossary.json` : `{"term", "aliases", "cat", "cite": {"k": "<clé>", "from": "début exact", "to": "fin exacte"}, "pages": [...]}`. Le build **extrait la définition du texte source** (aucune reformulation) et échoue si la citation est introuvable. Une définition issue d'une page staff n'apparaît qu'au niveau staff. `"auto": false` désactive le soulignement automatique d'un terme trop courant.

## Vérifications

```bash
python3 build.py --check                       # décompte + intégrité mot à mot (source → page générée)
NODE_PATH=$(npm root -g) node tests/e2e.js     # serveur local lancé ; navigateur réel (Playwright)
```

`tests/e2e.js` contrôle : pages affichées = pages de `pages.json` (113), texte de chacune des 113 pages complet dans le navigateur, recherche (accents, filtres, phrases), niveaux d'accès, absence de données personnelles, aucune erreur console.

## Limites connues

- Les sources sont du texte brut : titres et tableaux sont **déduits** par heuristique. Le texte est complet, mais un titre peut être manqué ou un tableau mal découpé (en cas de doute, comparer avec le document d'origine).
- Les versions multiples (Brumval v1–v4, Aerwyn v1/v2, copies du Pacte, brouillons de Constitution) sont rangées en « Archives » ; les contradictions entre documents ne sont pas arbitrées.
- Documents du brief non lus (Notion, Canva, Miro, Boucles RP school, B.R.U.M.E…) : listés dans « À propos & sources », sans page.
