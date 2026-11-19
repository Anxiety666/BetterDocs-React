# ELDERWOOD RP : dossier complet pour construire le site du lore

Version du 19/11/2026. Préparé pour Antonio Tomassi (staff / support lore). Contient 212 documents (2606 Ko de texte), tous issus de ses Google Docs, feuilles et PDF.

## 0. Mission pour Claude (à lire en premier)

Construire un site web (statique, un seul dossier, sans backend) qui affiche **tout le contenu** des documents ci-dessous, **directement lisible sur les pages**, sans aucun lien vers Google Drive. Les liens Drive d'origine ne doivent PAS servir de contenu : tout est copié ici.

### Ce que le site doit offrir
1. Accueil sombre et soigné (thème école de magie, ambiance Elderwood), avec les 20 grandes sections en cartes.
2. Une page par document, avec le texte complet, un sommaire automatique, le statut de rédaction, le responsable et le niveau d'accès (voir §3).
3. Recherche plein texte instantanée sur tout le site (index construit côté navigateur, ex. lunr.js ou fuse.js), avec filtre par section.
4. Navigation : menu latéral par section, fil d'Ariane, boutons précédent/suivant, mode clair/sombre, lisible sur téléphone.
5. Chaque feuille de calcul (préfixe `sheet-`) s'affiche en vrai tableau HTML triable et filtrable.
6. Un glossaire automatique (§4) : survol d'un terme du lore = définition courte.
7. Marquer visiblement les pages « en cours de rédaction », « à modifier », ou brouillon.

### Contraintes
- Tout le texte reste dans le site (fichiers `.md` ou JSON chargés au démarrage). Aucune dépendance à Drive, Notion, Canva ou Miro.
- Respecter les niveaux d'accès (§3) : proposer un mode « public joueurs » et un mode « staff » (simple bascule + mot de passe côté client, ou deux builds). Ne jamais mélanger les pages staff dans le build public.
- Ne rien inventer : si une information manque, afficher « à compléter » plutôt que d'improviser du lore.
- Français, ton neutre dans l'interface, textes du lore laissés tels quels.
- Les textes ci-dessous viennent d'un export texte brut : les titres ne sont pas balisés. Détecter les titres par heuristique (lignes courtes en MAJUSCULES ou suivies d'un paragraphe, numérotations « 1. », « I - », « Article N ») et les rendre en `h2`/`h3`.

## 1. Plan du site

### Lore général (2)
- **Bible du Lore (édition élèves 1.0, 16/07/2026)** → `bible-du-lore` · Possibilité de modifier  · 142 Ko
- **Elderwood les Origines de la Magie** → `origines-magie` · À modifier · 171 Ko

### Magie & maladies (10)
- **Brûlebrume** → `brulebrume` · Validé · 11 Ko
- **Dictionnaire des accords consacrés, Runomancie** → `runomancie-dico-accords` · Validé · 17 Ko
- **Dictionnaire des maladies** → `dictionnaire-maladies` · Possibilité de modifier  · 8 Ko
- **La Lycanthropie (v.4)** → `lycanthropie-v4` · Possibilité de modifier  · 19 Ko
- **Les maladies magiques (v.4)** → `maladies-v4` · Possibilité de modifier  · 22 Ko
- **Lore Runomancie Elderwood** → `runomancie-lore` · Validé · 16 Ko
- **MALÉDICTIONS (SORT)** → `maledictions` · Validé · 5 Ko
- **Magie proscrite** → `magie-proscrite` · En cours de rédaction · 22 Ko
- **Magie proscrite, la Métamorphose** → `magie-proscrite-metamorphose` · Validé · 8 Ko
- **Échoïde** → `echoide` · Validé · 4 Ko

### Créatures & bestiaire (3)
- **Bestiaire 30/10/26** → `bestiaire-30-10-26` · Validé · 94 Ko
- **Encyclopédie draconique (PDF)** → `encyclopedie-draconique` · Validé · 98 Ko
- **Les créatures des Maisons 30/10/2026** → `creatures-des-maisons` · Validé · 14 Ko

### Objets & Reliques (8)
- **Balais Magiques - Elderwood** → `balais-magiques` · Validé · 9 Ko
- **Boutique Baguette** → `boutique-baguette` · À modifier · 4 Ko
- **Elderwood - Catalyseurs** → `catalyseurs` · Validé · 9 Ko
- **Elderwood - Les Cristaux-Cœurs** → `cristaux-coeurs` · Validé · 38 Ko
- **Elderwood - Matériaux des Catalyseurs** → `materiaux-catalyseurs` · Validé · 7 Ko
- **Elderwood : Objets Magiques** → `objets-magiques` · Possibilité de modifier  · 110 Ko
- **Itemisation (feuille)** → `sheet-itemisation` · 38 Ko
- **Reliques de Maison et Artefacts communs** → `reliques-maison-artefacts` · En cours de rédaction · 2 Ko

### Potions (2)
- **Liste des potions 30/10/2026** → `potions-30-10-26` · En cours de rédaction · 11 Ko
- **Livre des potions enseignées 30/10/2026** → `livre-potions-enseignees` · En cours de rédaction · 5 Ko

### Sorts (3)
- **Propositions de sorts MJ (feuille)** → `sheet-propositions-sorts-mj` · 10 Ko
- **Propositions de sorts Pôle RP (feuille)** → `sheet-propositions-sorts-pole-rp` · Possibilité de modifier  · 25 Ko
- **Sort pour l'équipe lore (PDF)** → `sorts-equipe-lore` · Possibilité de modifier  · 15 Ko

### Familles & maisons (9)
- **Cordelia Ravenscroft** → `fiche-cordelia-ravenscroft` · Validé · 11 Ko
- **DA FAMILLE (lore des familles)** → `lore-des-familles` · Possibilité de modifier  · 145 Ko
- **Lore Belladorn (joueurs)** → `lore-belladorne` · Validé · 4 Ko
- **Lore Caerwyn (joueurs)** → `lore-caerwyn` · Validé · 5 Ko
- **Lore DDM Maisons** → `lore-ddm-maisons` · 44 Ko
- **Lore Dravenholt (joueurs)** → `maison-dravenholt` · Validé · 4 Ko
- **Lore Hearthbane (joueurs)** → `lore-hearthbane` · Validé · 5 Ko
- **Lore Ravenscroft (joueurs)** → `maison-ravenscroft` · Validé · 4 Ko
- **Lore Valemont (joueurs)** → `maison-valemont` · Validé · 4 Ko

### Lieux & institutions (3)
- **Histoire de l'AMRU & idée de Lois** → `histoire-amru-lois` · Validé · 21 Ko
- **Police Magique AMRU** → `police-magique-amru` · 21 Ko
- **Shedwood** → `shedwood` · Validé · 13 Ko

### Droit & Constitution (7)
- **Annexe de la Constitution Magique (peines et amendes)** → `constitution-annexe-peines` · 29 Ko
- **Brouillon Constitution magique** → `constitution-brouillon` · 10 Ko
- **Constitution + peines et amendes** → `constitution-peines-amendes` · 20 Ko
- **Constitution magique (Règlement légal)** → `constitution-reglement-legal` · En cours de rédaction · 10 Ko
- **Constitution magique – Le Pacte du Voile** → `pacte-du-voile` · 11 Ko
- **Pacte du Voile (autre copie 04/11)** → `pacte-du-voile-copie` · 11 Ko
- **Partie IV constitution** → `constitution-partie-IV` · 10 Ko

### Règlements (4)
- **Autorisations & Permissions** → `autorisations-permissions` · 2 Ko
- **Règlement de l'équipe staff** → `reglement-staff` · 8 Ko
- **Règlement intérieur de l'Académie, Professeurs 30/10/2026** → `reglement-professeurs-30-10-26` · Validé · 22 Ko
- **Règlement intérieur de l'Académie, Élèves 30/10/2026** → `reglement-eleves-30-10-26` · Validé · 11 Ko

### Cours & pédagogie (4)
- **Boîte à phrases du professeur (v2)** → `boite-a-phrases-prof` · 24 Ko
- **Cours de sortilèges 1re année : Alarion** → `cours-sortileges-alarion` · 13 Ko
- **Fiche professeur** → `fiche-professeur-nov-2026` · Validé · 1 Ko
- **Liste des professeurs (onglet 1, CSV)** → `sheet-prof-tableau` · Possibilité de modifier  · 8 Ko

### Métiers légaux (2)
- **Dossiers Métiers Légaux (création d'entreprises légales)** → `dossiers-metiers-legaux` · Validé · 11 Ko
- **Métier Apothicaire** → `metier-apothicaire` · Validé · 16 Ko

### Illégal (11)
- **Alchimiste (illégal)** → `metier-alchimiste` · Validé · 4 Ko
- **Alchimiste, potions (progression)** → `alchimiste-potions-progression` · Possibilité de modifier  · 7 Ko
- **Braconnier** → `metier-braconnier` · Possibilité de modifier  · 5 Ko
- **Contrebandier** → `metier-contrebandier` · Validé · 5 Ko
- **Fabricant de reliques illégales** → `metier-fabricant-reliques` · Validé · 5 Ko
- **Items jobs illégaux V1 (onglet 1)** → `sheet-items-jobs-illegaux` · Validé · 30 Ko
- **Livre des potions illégal** → `livre-potions-illegal` · Validé · 8 Ko
- **Pilleur** → `metier-pilleur` · Validé · 4 Ko
- **Reliques maudites** → `reliques-maudites` · À modifier · 6 Ko
- **Règlement Illégal (V1 titre, lien Bibliothèque)** → `reglement-illegal` · En cours de rédaction · 11 Ko
- **Sacs contrebandier** → `sacs-contrebandier` · Possibilité de modifier  · 1 Ko

### Trames (9)
- **Trame 2 : Le professeur qui parle à l'envers** → `trame2-professeur-a-lenvers` · 21 Ko
- **Trame : Le hibou égaré** → `trame-hibou-egare` · 20 Ko
- **Trame Héritier de Brumval (v3)** → `trame-heritier-brumval-v3` · 16 Ko
- **Trame Héritier de Brumval v1** → `trame-heritier-brumval-v1` · 7 Ko
- **Trame Héritier de Brumval v2** → `trame-heritier-brumval-v2` · 10 Ko
- **Trame élue : l'Héritage d'Aerwyn (v1)** → `trame-heritage-aerwyn-v1` · 25 Ko
- **Trame élue : l'Héritier d'Aerwyn (v2)** → `trame-heritier-aerwyn-v2` · 23 Ko
- **Trame élue : l'Héritier de Brumval (v4)** → `trame-heritier-brumval-v4` · 21 Ko
- **Trame élue : l'Héritier de Falcon (v7)** → `trame-heritier-falcon-v7` · 16 Ko

### Suivis MJ (8)
- **SMJ Hulgo Elderwood** → `smj-hulgo` · 35 Ko
- **Suivi Médicomagie** → `suivi-medicomagie` · 40 Ko
- **Suivi Sortilèges – Worex** → `suivi-sortileges-worex` · 10 Ko
- **Suivi Zoomancie illégale** → `suivi-zoomancie-illegale` · 15 Ko
- **Suivie MJ Elderwood V1** → `suivi-mj-v1` · 74 Ko
- **Suivie Métamorphose – Nervoz** → `suivi-metamorphose-nervoz` · 62 Ko
- **Suivie astronomie et divination** → `suivi-astronomie-divination` · 54 Ko
- **perso mj Arthur Bellamy** → `perso-mj-arthur-bellamy` · 7 Ko

### Questions de lore (2)
- **Elderwood – Questions de lore** → `questions-de-lore` · 38 Ko
- **Elderwood – Questions de lore à trancher** → `questions-de-lore-a-trancher` · 38 Ko

### Staff & organisation (14)
- **Dossier HRP : Atelier et formation** → `hrp-atelier-formation` · Validé · 31 Ko
- **Dossier HRP : Évolutions poste MJ** → `dossier-hrp-evolutions-mj` · 2 Ko
- **Dossiers HRP : Réorganisation recrutement (parrainage)** → `hrp-reorganisation-recrutement` · Validé · 11 Ko
- **ElderWood - Organisations MJ (feuille)** → `sheet-organisations-mj` · À modifier · 16 Ko
- **Gestion de l'École (feuille)** → `sheet-gestion-ecole` · Possibilité de modifier  · 18 Ko
- **LIVRET DES FORMATIONS** → `livret-formations` · 39 Ko
- **MJ** → `sheet-suivi-joueurs-mj` · Possibilité de modifier  · <1 Ko
- **Organisation Pôle Lore (feuille)** → `sheet-organisation-pole-lore` · En cours de rédaction · 16 Ko
- **Organisation Pôle RP (feuille)** → `sheet-organisation-pole-rp` · 12 Ko
- **Organisation Pôle RP - Civil/Légal (feuille)** → `sheet-pole-rp-civil-legal` · Possibilité de modifier  · 10 Ko
- **Organisation Pôle RP – Familles (onglet 1)** → `sheet-organisation-familles` · Possibilité de modifier  · 8 Ko
- **Organisation Pôle RP – Illégal (onglet 1)** → `sheet-organisation-illegal` · Possibilité de modifier  · 8 Ko
- **Recrutement MJ** → `recrutement-mj` · Validé · 2 Ko
- **Régles** → `regles` · 11 Ko

### Modèles & templates (10)
- **Copie de MODÈLE SUIVI (gabarit suivi académique, restylé)** → `modele-suivi-academique` · 4 Ko
- **MODÈLE SUIVI à copier-coller 18/11 (source du gabarit)** → `modele-suivi-copier-coller-18-11` · 6 Ko
- **Squelette Naissance Famille v1** → `squelette-naissance-famille` · Possibilité de modifier  · 1 Ko
- **Squelette suivi MJ** → `squelette-suivi-mj` · Possibilité de modifier  · 21 Ko
- **Template création spell** → `template-creation-spell` · Possibilité de modifier  · 1 Ko
- **Template création vidéo** → `template-creation-video` · Possibilité de modifier  · 1 Ko
- **Template dossiers HRP** → `template-dossier-hrp` · Possibilité de modifier  · <1 Ko
- **Template dossiers RP** → `template-dossier-rp` · Possibilité de modifier  · <1 Ko
- **Template entreprise** → `template-entreprise` · Validé · 1 Ko
- **Template suivie / trame** → `template-suivi-trame` · Possibilité de modifier  · 5 Ko

### Jeu (commandes) (2)
- **Commandes & Raccourcis Importants** → `commandes-raccourcis-B` · 1 Ko
- **Commandes & Raccourcis Importants (Greatowl)** → `commandes-raccourcis-A` · <1 Ko

### Wiki officiel WikiWood (public) (99)
- **AMRU** → `wiki-amru` · 1 Ko
- **Accueil** → `wiki-accueil` · 2 Ko
- **Aetherion** → `wiki-bestiaire--rang-s--aetherion` · 3 Ko
- **Akkorokamui** → `wiki-bestiaire--rang-s--akkorokamui` · 3 Ko
- **Algue Commune** → `wiki-herbier--plantes-innofensives--algue-commune` · 2 Ko
- **Angélique d'Elderwood** → `wiki-herbier--plantes-surveillees--angelique-delderwood` · 5 Ko
- **Araignée d'Ether** → `wiki-bestiaire--rang-aa--araignee-dether` · 4 Ko
- **Armoise Lunaire** → `wiki-herbier--plantes-innofensives--armoise-lunaire` · 2 Ko
- **Baie de Lyandrelle** → `wiki-herbier--plantes-surveillees--baie-de-lyandrelle` · 3 Ko
- **Bondiluce** → `wiki-bestiaire--rang-a--bondiluce` · 1 Ko
- **Bonne-Haleine des Landes** → `wiki-herbier--plantes-innofensives--bonne-haleine-des-landes` · 4 Ko
- **Braisière des coteaux** → `wiki-herbier--plantes-innofensives--braisiere-des-coteaux` · 3 Ko
- **Brisecerat** → `wiki-bestiaire--rang-a--brisecerat` · 1 Ko
- **Cactus-Tonneau des serres** → `wiki-herbier--plantes-innofensives--cactus-tonneau-des-serres` · 5 Ko
- **Champignon Brun** → `wiki-herbier--plantes-innofensives--champignon-brun` · 2 Ko
- **Champignon Phosphorescent** → `wiki-herbier--plantes-innofensives--champignon-phosphorescent` · 2 Ko
- **Cheminante des grèves** → `wiki-herbier--plantes-surveillees--cheminante-des-greves` · 4 Ko
- **Chronologie** → `wiki-chronologie` · 2 Ko
- **Dame de l'heure** → `wiki-herbier--plantes-innofensives--dame-de-lheure` · 4 Ko
- **Dictame de Crète** → `wiki-herbier--plantes-innofensives--dictame-de-crete` · 2 Ko
- **Discpline et sanctions** → `wiki-reglement-hrp--discpline-et-sanctions` · 3 Ko
- **Délieuse des rocailles** → `wiki-herbier--plantes-innofensives--delieuse-des-rocailles` · 3 Ko
- **Echomys** → `wiki-bestiaire--rang-a--echomys` · 4 Ko
- **Entités** → `wiki-bestiaire--entites` · <1 Ko
- **Ephyr** → `wiki-bestiaire--rang-s--ephyr` · 3 Ko
- **Famille Belladorn** → `wiki-familles-notables--famille-belladorn` · 5 Ko
- **Famille Caerwyn** → `wiki-familles-originelles--famille-caerwyn` · 6 Ko
- **Famille Dravenholt** → `wiki-familles-originelles--famille-dravenholt` · 5 Ko
- **Famille Hearthbane** → `wiki-familles-originelles--famille-hearthbane` · 6 Ko
- **Famille Ravenscroft** → `wiki-familles-notables--famille-ravenscroft` · 5 Ko
- **Famille Valemont** → `wiki-familles-originelles--famille-valemont` · 5 Ko
- **Familles Notables** → `wiki-familles-notables` · <1 Ko
- **Familles Originelles** → `wiki-familles-originelles` · 2 Ko
- **Folumix** → `wiki-bestiaire--rang-aa--folumix` · 1 Ko
- **Fougère mâle** → `wiki-herbier--plantes-surveillees--fougere-male` · 4 Ko
- **Glossaire** → `wiki-glossaire` · 1 Ko
- **Golem Runique** → `wiki-bestiaire--rang-aaa--golem-runique` · 2 Ko
- **Golem Sylvestre** → `wiki-bestiaire--rang-aaa--golem-sylvestre` · 3 Ko
- **Gourde d'Office** → `wiki-herbier--plantes-innofensives--gourde-doffice` · 3 Ko
- **Gratte Mur / Arcanophage** → `wiki-bestiaire--rang-aa--gratte-mur-arcanophage` · 1 Ko
- **Griffon** → `wiki-bestiaire--rang-a-2--griffon` · 4 Ko
- **Guide de candidature** → `wiki-guide-de-candidature` · 5 Ko
- **Herbier** → `wiki-herbier` · <1 Ko
- **Histoire d'Elderwood** → `wiki-histoire-delderwood` · <1 Ko
- **Jackalope** → `wiki-bestiaire--rang-a--jackalope` · 1 Ko
- **L'Écho** → `wiki-principes-fondamentaux--lecho` · <1 Ko
- **L'Échoïde** → `wiki-bestiaire--entites--les-echoides` · 4 Ko
- **L'île, hors du château** → `wiki-les-lieux--lile-hors-du-chateau` · 2 Ko
- **La Résonance** → `wiki-principes-fondamentaux--la-resonance` · 1 Ko
- **La Source** → `wiki-les-lieux--la-source` · <1 Ko
- **Le Bestiaire** → `wiki-bestiaire` · <1 Ko
- **Le Flux** → `wiki-principes-fondamentaux--le-flux` · <1 Ko
- **Le Voile** → `wiki-principes-fondamentaux--le-voile` · 1 Ko
- **Le château** → `wiki-les-lieux--le-chateau` · 1 Ko
- **Les couleurs du Flux** → `wiki-principes-fondamentaux--les-couleurs-du-flux` · 3 Ko
- **Les formes de magie** → `wiki-principes-fondamentaux--les-formes-de-magie` · 1 Ko
- **Les lieux** → `wiki-les-lieux` · <1 Ko
- **Les maisons** → `wiki-les-maisons` · 1 Ko
- **Les statuts magiques** → `wiki-principes-fondamentaux--les-statuts-magiques` · 2 Ko
- **Lexique RP** → `wiki-reglement--lexique-rp` · 6 Ko
- **Maison Aerwyn** → `wiki-les-maisons--maison-aerwyn` · 2 Ko
- **Maison Brumval** → `wiki-les-maisons--maison-brumval` · 1 Ko
- **Maison Falcon** → `wiki-les-maisons--maison-falcon` · 1 Ko
- **Maison Venatrix** → `wiki-les-maisons--maison-venatrix` · 2 Ko
- **Mange-Lumière / Luciphage** → `wiki-bestiaire--rang-aa--mange-lumiere-luciphage` · 1 Ko
- **Matriarche (Araignée d'Ether)** → `wiki-bestiaire--rang-aaaa--matriarche` · 4 Ko
- **Menthe Poivrée** → `wiki-herbier--plantes-innofensives--menthe-poivree` · 2 Ko
- **Misa** → `wiki-bestiaire--rang-a--misa` · 1 Ko
- **Multaille** → `wiki-bestiaire--rang-aa--multaille` · 1 Ko
- **Mycollin** → `wiki-bestiaire--rang-a--mycollin` · 3 Ko
- **Obligeante des haies** → `wiki-herbier--plantes-innofensives--obligeante-des-haies` · 4 Ko
- **Ornicabal** → `wiki-bestiaire--rang-aaa--ornicabal` · 1 Ko
- **Papillodactyle** → `wiki-bestiaire--rang-a--papillodactyle` · 2 Ko
- **Pastenague** → `wiki-bestiaire--rang-a--pastenague` · 1 Ko
- **Patiente des murs** → `wiki-herbier--plantes-innofensives--patiente-des-murs` · 4 Ko
- **Personnages illustres** → `wiki-personnages` · 4 Ko
- **Peseuse commune** → `wiki-herbier--plantes-innofensives--peseuse-commune` · 3 Ko
- **Plantes innoffensives** → `wiki-herbier--plantes-innofensives` · 2 Ko
- **Plantes surveillées** → `wiki-herbier--plantes-surveillees` · <1 Ko
- **Pleurote des ombres** → `wiki-herbier--plantes-innofensives--pleurote-des-ombres` · 1 Ko
- **Points de maison** → `wiki-reglement-hrp--points-de-maison` · 4 Ko
- **Praedacornis** → `wiki-bestiaire--rang-aa--praedacornis` · 1 Ko
- **Prenante des rives** → `wiki-herbier--plantes-innofensives--prenante-des-rives` · 3 Ko
- **Principes fondamentaux** → `wiki-principes-fondamentaux` · 1 Ko
- **Radicule** → `wiki-bestiaire--rang-a--radicule` · 1 Ko
- **Rang A** → `wiki-bestiaire--rang-a-2` · <1 Ko
- **Rang B** → `wiki-bestiaire--rang-aaaa` · 1 Ko
- **Rang C** → `wiki-bestiaire--rang-aaa` · 1 Ko
- **Rang D** → `wiki-bestiaire--rang-aa` · 1 Ko
- **Rang E** → `wiki-bestiaire--rang-a` · 2 Ko
- **Rang S** → `wiki-bestiaire--rang-s` · <1 Ko
- **Règlement** → `wiki-reglement` · <1 Ko
- **Règlement RP** → `wiki-reglement--reglement-rp` · 3 Ko
- **Règlement général** → `wiki-reglement--reglement-general` · 4 Ko
- **Règlement intérieur** → `wiki-reglement-hrp` · 7 Ko
- **Scalvignus** → `wiki-bestiaire--rang-aa--scalvignus` · 1 Ko
- **Shpouts** → `wiki-bestiaire--rang-a--shpouts` · 2 Ko
- **Valdorn** → `wiki-bestiaire--rang-s--valdorn` · 3 Ko
- **Zones RPK** → `wiki-reglement--zones-rpk` · <1 Ko

## 2. Fiche de chaque document

Pour chaque document : section, statut, mots-clés, résumé officiel, responsable, accès. Le texte complet suit en §6.

### Lore général

**Bible du Lore (édition élèves 1.0, 16/07/2026)** (`bible-du-lore`)
- Statut : Possibilité de modifier 
- Mots-clés : bible, lore, important
- Résumé : Lore connu des joueurs.
- Responsable : Theronx
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

**Elderwood les Origines de la Magie** (`origines-magie`)
- Statut : À modifier
- Mots-clés : histoire, lore, origine, elderwood, ressonance,
- Accès : Restreint, sur autorisation
- Remarque : Je ne comprends pas le thème du document ni sa fonction :/ dsl !

### Magie & maladies

**Brûlebrume** (`brulebrume`)
- Statut : Validé
- Mots-clés : brulebrume, lore, histoire
- Résumé : Histoire de Brulebrûme
- Responsable : Theronx
- Accès : Restreint, sur autorisation
- Remarque : MAJ :  CTRL + F

**Dictionnaire des accords consacrés, Runomancie** (`runomancie-dico-accords`)
- Statut : Validé
- Mots-clés : dictionnaire, rune, runique, accords
- Résumé : Dictionaire des accords consacrés de runomancie connus 
- Responsable : Waika
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

**Dictionnaire des maladies** (`dictionnaire-maladies`)
- Statut : Possibilité de modifier 
- Mots-clés : maladie, élève, médicomancie, apothicaire, créatures
- Résumé : Dictionnaire des maladies
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

**La Lycanthropie (v.4)** (`lycanthropie-v4`)
- Statut : Possibilité de modifier 
- Mots-clés : lycanthropie, origine, traitement, symptomes
- Résumé : Origine, symptome & Traitement de la Lycanthropie
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

**Les maladies magiques (v.4)** (`maladies-v4`)
- Statut : Possibilité de modifier 
- Mots-clés : maladies, magiques, lore
- Résumé : Dictionnaire des maladies
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

**Lore Runomancie Elderwood** (`runomancie-lore`)
- Statut : Validé
- Mots-clés : rune, runique, dictionnaire
- Résumé : L'étude des runes
- Responsable : Waika
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

**MALÉDICTIONS (SORT)** (`maledictions`)
- Statut : Validé
- Mots-clés : magie, spell, sorts, malédiction
- Résumé : Liste des sorts maudits.
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

**Magie proscrite** (`magie-proscrite`)
- Statut : En cours de rédaction
- Mots-clés : magie, interdiction, incidents
- Résumé : Document détaillant le phénomène de distortion.
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

**Magie proscrite, la Métamorphose** (`magie-proscrite-metamorphose`)
- Statut : Validé
- Mots-clés : magie, interdiction, distortion, méthamorphose
- Résumé : Document expliquant le fonctionnement et les limites de la méthamorphose, ainsi que les raisons de son interdiction.
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

**Échoïde** (`echoide`)
- Statut : Validé
- Mots-clés : céature, magique, rune, runique
- Résumé : Desription de la créature magique
- Responsable : Waika
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

### Créatures & bestiaire

**Bestiaire 30/10/26** (`bestiaire-30-10-26`)
- Statut : Validé
- Mots-clés : bestiaire, animaux, catégories, créatures, magiques
- Résumé : Les Bêtes du monde magique
- Accès : Restreint, sur autorisation
- Remarque : ✅ 30/10/2026  Barre de recherche

**Encyclopédie draconique (PDF)** (`encyclopedie-draconique`)
- Statut : Validé
- Mots-clés : langue, ressonnance, dragon, rune, runomancie
- Résumé : Le langage draconique expliqué
- Responsable : Theronx
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

**Les créatures des Maisons 30/10/2026** (`creatures-des-maisons`)
- Statut : Validé
- Mots-clés : classification, 5, créatures, Brumval, Aerwyn, Falcon, Venatrix
- Résumé : Créatures représentants les maisons.
- Accès : Restreint, sur autorisation
- Remarque : ✅ 30/10/2026

### Objets & Reliques

**Balais Magiques - Elderwood** (`balais-magiques`)
- Statut : Validé
- Mots-clés : vendeur, balais, métier
- Résumé : Boucle de fabrication, progression et fonctionnement du métier lié aux balais.
- Responsable : PAS D'ACCÈS
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Boutique Baguette** (`boutique-baguette`)
- Statut : À modifier
- Mots-clés : vendeur, magasin, baguettes, création, métier
- Résumé : Boucle de fabrication, progression et fonctionnement du métier de baguettier et vendeur de baguettes.
- Responsable : COPIE
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Elderwood - Catalyseurs** (`catalyseurs`)
- Statut : Validé
- Mots-clés : synthèse, lore, composant, fabrication, rôle
- Résumé : Les catalyseurs en profondeur
- Responsable : Waika
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

**Elderwood - Les Cristaux-Cœurs** (`cristaux-coeurs`)
- Statut : Validé
- Mots-clés : cristaux, matériaux
- Résumé : Les différents cristal-coeur en fonction des matériaux
- Responsable : Waika
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

**Elderwood - Matériaux des Catalyseurs** (`materiaux-catalyseurs`)
- Statut : Validé
- Mots-clés : matériaux, catalyseurs
- Résumé : Les différents matériaux des catalyseurs
- Responsable : Waika
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

**Elderwood : Objets Magiques** (`objets-magiques`)
- Statut : Possibilité de modifier 
- Mots-clés : liste, item, objet, magie, in game, ig
- Résumé : Liste détaillée et complète des objets magiques.
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

**Itemisation (feuille)** (`sheet-itemisation`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Reliques de Maison et Artefacts communs** (`reliques-maison-artefacts`)
- Statut : En cours de rédaction
- Résumé : EN COURS DE RÉDACTION | À PROTÉGER
- Accès : Restreint, sur autorisation

### Potions

**Liste des potions 30/10/2026** (`potions-30-10-26`)
- Statut : En cours de rédaction
- Mots-clés : recettes, ingérdients, métiers, élèves, cursus, matière, potion, effet, cooldown
- Résumé : Liste des potions (avec leurs caractéristiques et recettes complètes).
- Accès : Commun au Pôle RP
- Remarque : ✅ 30/10/2026

**Livre des potions enseignées 30/10/2026** (`livre-potions-enseignees`)
- Statut : En cours de rédaction
- Mots-clés : chaudron, école, cursus, professeur, potion, baguette, ingrédients, recettes
- Résumé : Document regroupant la liste des recettes et caractéristiques détaillées de toutes les potions de niveau T1.
- Accès : Restreint, sur autorisation
- Remarque : ✅ 30/10/2026

### Sorts

**Propositions de sorts MJ (feuille)** (`sheet-propositions-sorts-mj`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Propositions de sorts Pôle RP (feuille)** (`sheet-propositions-sorts-pole-rp`)
- Statut : Possibilité de modifier 
- Mots-clés : spell, sort, GD, MJ, lore
- Résumé : Document de liaison entre le pôle RP et le GD concernant les sorts.
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

**Sort pour l'équipe lore (PDF)** (`sorts-equipe-lore`)
- Statut : Possibilité de modifier 
- Mots-clés : sort, dev, devellopement, plateau, guide
- Résumé : Listes des différents sorts disponibles en jeu.
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

### Familles & maisons

**Cordelia Ravenscroft** (`fiche-cordelia-ravenscroft`)
- Statut : Validé
- Mots-clés : Famille, personnage, lore, Cordelia, Ravenscroft
- Résumé : Fiche du personnage remplie par la joueuse.
- Accès : Restreint, sur autorisation
- Remarque : MàJ :  CTRL + F

**DA FAMILLE (lore des familles)** (`lore-des-familles`)
- Statut : Possibilité de modifier 
- Mots-clés : lore, famille, important
- Résumé : Histoire et informations importantes sur chaque famille.
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Lore Belladorn (joueurs)** (`lore-belladorne`)
- Statut : Validé
- Mots-clés : Famille, description, lore, Belladorne
- Résumé : Lore de la famille (connu des joueurs).
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Lore Caerwyn (joueurs)** (`lore-caerwyn`)
- Statut : Validé
- Mots-clés : Famille, description, lore, Caerwyn
- Résumé : Lore de la famille (connu des joueurs).
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Lore DDM Maisons** (`lore-ddm-maisons`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Lore Dravenholt (joueurs)** (`maison-dravenholt`)
- Statut : Validé
- Mots-clés : Famille, description, lore, Dravenholt
- Résumé : Lore de la famille (connu des joueurs).
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Lore Hearthbane (joueurs)** (`lore-hearthbane`)
- Statut : Validé
- Mots-clés : Famille, description, lore, Hearthbane
- Résumé : Lore de la famille (connu des joueurs).
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Lore Ravenscroft (joueurs)** (`maison-ravenscroft`)
- Statut : Validé
- Mots-clés : Famille, description, lore, Ravenscroft
- Résumé : Lore de la famille (connu des joueurs).
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Lore Valemont (joueurs)** (`maison-valemont`)
- Statut : Validé
- Mots-clés : Famille, description, lore, Falcon
- Résumé : Lore de la famille (connu des joueurs).
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

### Lieux & institutions

**Histoire de l'AMRU & idée de Lois** (`histoire-amru-lois`)
- Statut : Validé
- Mots-clés : ministère, article, lois, juridique, reglement
- Résumé : Ce document regroupe l'histoire de l'AMRU ainsi que l'ensemble de ses lois.
- Responsable : Demande accès en cours
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Police Magique AMRU** (`police-magique-amru`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Shedwood** (`shedwood`)
- Statut : Validé
- Mots-clés : lieu, village, shedwood, lore, AMRU, métiers
- Résumé : Description et informations importantes concernant le village de Shedwood.
- Accès : Restreint, sur autorisation

### Droit & Constitution

**Annexe de la Constitution Magique (peines et amendes)** (`constitution-annexe-peines`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Brouillon Constitution magique** (`constitution-brouillon`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Constitution + peines et amendes** (`constitution-peines-amendes`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Constitution magique (Règlement légal)** (`constitution-reglement-legal`)
- Statut : En cours de rédaction
- Mots-clés : règlement, lois
- Responsable : OK
- Accès : Restreint, sur autorisation

**Constitution magique – Le Pacte du Voile** (`pacte-du-voile`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Pacte du Voile (autre copie 04/11)** (`pacte-du-voile-copie`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Partie IV constitution** (`constitution-partie-IV`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

### Règlements

**Autorisations & Permissions** (`autorisations-permissions`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Règlement de l'équipe staff** (`reglement-staff`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Règlement intérieur de l'Académie, Professeurs 30/10/2026** (`reglement-professeurs-30-10-26`)
- Statut : Validé
- Mots-clés : reglement, interieur, classe, élèves, fôret interdite,
- Résumé : Réglement intérieur de l'académie d'Elderwood. Discipline et sanctions, système de points, guide à destination de l'ensemble du personnel d'Elderwood.
- Accès : Restreint, sur autorisation
- Remarque : ✅ 30/10/2026

**Règlement intérieur de l'Académie, Élèves 30/10/2026** (`reglement-eleves-30-10-26`)
- Statut : Validé
- Mots-clés : fonctionnement, sanction, école, punitions, élève, parents, adultes, profs, professeurs
- Résumé : Règlement intérieur, discipline et sanctions, système de points des maisons. Document à destination des élèves
- Accès : Restreint, sur autorisation
- Remarque : ✅ 30/10/2026

### Cours & pédagogie

**Boîte à phrases du professeur (v2)** (`boite-a-phrases-prof`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Cours de sortilèges 1re année : Alarion** (`cours-sortileges-alarion`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Fiche professeur** (`fiche-professeur-nov-2026`)
- Statut : Validé
- Résumé : Fiche préparation 1ere et 2ieme année avec les profs NOV 2026
- Responsable : Édéa
- Accès : Restreint, sur autorisation
- Remarque : ✅ 01/11/2026

**Liste des professeurs (onglet 1, CSV)** (`sheet-prof-tableau`)
- Statut : Possibilité de modifier 
- Mots-clés : tableur, matière, school, profs
- Résumé : Liste des professeurs ainsi que leur lore.
- Responsable : COPIE
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

### Métiers légaux

**Dossiers Métiers Légaux (création d'entreprises légales)** (`dossiers-metiers-legaux`)
- Statut : Validé
- Mots-clés : modèle, fiche, demande, candidat, candidature, métier, légal, civil
- Résumé : Ce document permet à un joueur ou à un groupe de présenter un projet lié à un métier légal du plateau.
- Responsable : J - BBC
- Accès : Commun au Pôle RP
- Remarque : 01/11/2026

**Métier Apothicaire** (`metier-apothicaire`)
- Statut : Validé
- Mots-clés : potion, progression, suivi, légal
- Résumé : Boucle de fabrication, progression et fonctionnement du métier lié aux potions.
- Responsable : COPIE
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

### Illégal

**Alchimiste (illégal)** (`metier-alchimiste`)
- Statut : Validé
- Mots-clés : potion, progression, suivi, illégal
- Résumé : Boucle de fabrication, progression et fonctionnement du métier lié aux potions (illégal).
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Alchimiste, potions (progression)** (`alchimiste-potions-progression`)
- Statut : Possibilité de modifier 
- Mots-clés : progression, alchimie, ingédients
- Résumé : Ce document détaille les différentes recettes de potions accessible en fonction du niveau atteint par le joueur en alchimie.
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Braconnier** (`metier-braconnier`)
- Statut : Possibilité de modifier 
- Mots-clés : braconnage, progression, suivi, illégal
- Résumé : Progression et fonctionnement du métier lié au braconnage.
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Contrebandier** (`metier-contrebandier`)
- Statut : Validé
- Mots-clés : contrebande, vente, progression, suivi, illégal
- Résumé : Boucle de vente, progression et fonctionnement du métier lié au pillage.
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Fabricant de reliques illégales** (`metier-fabricant-reliques`)
- Statut : Validé
- Mots-clés : reliques, progression, suivi, illégal
- Résumé : Boucle de fabrication, progression et fonctionnement du métier lié aux reliques (illégal).
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Items jobs illégaux V1 (onglet 1)** (`sheet-items-jobs-illegaux`)
- Statut : Validé
- Mots-clés : item, illégal, composants, schémas, reliques, services, consommables, entrées, sorties
- Résumé : Liste des items très détaillée pour chaque métier illégal.
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Livre des potions illégal** (`livre-potions-illegal`)
- Statut : Validé
- Mots-clés : livre, spells, interdit, grimoire
- Résumé : Livre et recette des potions illégales.
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Pilleur** (`metier-pilleur`)
- Statut : Validé
- Mots-clés : pilleur, progression, suivi, illégal
- Résumé : Progression et fonctionnement du métier lié au pillage.
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Reliques maudites** (`reliques-maudites`)
- Statut : À modifier
- Mots-clés : dégâts, malédiction, sorts, spells
- Résumé : Liste d'objets maudits ayant des effets positifs ou négatifs pour leur propriétaire.
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Règlement Illégal (V1 titre, lien Bibliothèque)** (`reglement-illegal`)
- Statut : En cours de rédaction
- Mots-clés : regles, procès, HRP, activité vols, groupes
- Résumé : Principes appliqués sur le serveur en ce qui concerne l'ensemble des activités illégales.
- Responsable : Blade
- Accès : Restreint, sur autorisation
- Remarque : MàJ :  Barre de recherche

**Sacs contrebandier** (`sacs-contrebandier`)
- Statut : Possibilité de modifier 
- Mots-clés : progression, métier, contrebande, récompenses
- Résumé : Ce document détaille le contenu de chaque sac (en fonction du niveau atteint par le joueur) ainsi que de ses statistiques associées.
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

### Trames

**Trame 2 : Le professeur qui parle à l'envers** (`trame2-professeur-a-lenvers`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Trame : Le hibou égaré** (`trame-hibou-egare`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Trame Héritier de Brumval (v3)** (`trame-heritier-brumval-v3`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Trame Héritier de Brumval v1** (`trame-heritier-brumval-v1`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Trame Héritier de Brumval v2** (`trame-heritier-brumval-v2`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Trame élue : l'Héritage d'Aerwyn (v1)** (`trame-heritage-aerwyn-v1`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Trame élue : l'Héritier d'Aerwyn (v2)** (`trame-heritier-aerwyn-v2`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Trame élue : l'Héritier de Brumval (v4)** (`trame-heritier-brumval-v4`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Trame élue : l'Héritier de Falcon (v7)** (`trame-heritier-falcon-v7`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

### Suivis MJ

**SMJ Hulgo Elderwood** (`smj-hulgo`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Suivi Médicomagie** (`suivi-medicomagie`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Suivi Sortilèges – Worex** (`suivi-sortileges-worex`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Suivi Zoomancie illégale** (`suivi-zoomancie-illegale`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Suivie MJ Elderwood V1** (`suivi-mj-v1`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Suivie Métamorphose – Nervoz** (`suivi-metamorphose-nervoz`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Suivie astronomie et divination** (`suivi-astronomie-divination`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**perso mj Arthur Bellamy** (`perso-mj-arthur-bellamy`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

### Questions de lore

**Elderwood – Questions de lore** (`questions-de-lore`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Elderwood – Questions de lore à trancher** (`questions-de-lore-a-trancher`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

### Staff & organisation

**Dossier HRP : Atelier et formation** (`hrp-atelier-formation`)
- Statut : Validé
- Mots-clés : atelier, formation, dossier, organisation, méthode, processus
- Résumé : Mises en place d'atelier pour améliorer les compétence des MJ, avec des formation obligatoire pour les nouveaux comme apprendre les outils et doc MJ.
- Responsable : SRP - Hulgo
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Dossier HRP : Évolutions poste MJ** (`dossier-hrp-evolutions-mj`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Dossiers HRP : Réorganisation recrutement (parrainage)** (`hrp-reorganisation-recrutement`)
- Statut : Validé
- Mots-clés : nouveau, MJ, candidat, recrutement
- Résumé : Attribution de parrain pour guider au début, page de annonce recrutement refaite et kit d'accueil MJ.
- Responsable : SRP - Hulgo
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**ElderWood - Organisations MJ (feuille)** (`sheet-organisations-mj`)
- Statut : À modifier
- Mots-clés : Organisation, pôle MJ
- Résumé : Document utilisé dans le précédent pôle MJ. 
- Responsable : SRP - Hulgo
- Accès : Restreint, sur autorisation
- Remarque : MàJ nécessaire ?

**Gestion de l'École (feuille)** (`sheet-gestion-ecole`)
- Statut : Possibilité de modifier 
- Mots-clés : école, gestion, tableur, cursus, maisons, professeurs, spells
- Résumé : Document partagé avec le GD.
- Responsable : Ajouté en editor ais pas owner
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**LIVRET DES FORMATIONS** (`livret-formations`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**MJ** (`sheet-suivi-joueurs-mj`)
- Statut : Possibilité de modifier 
- Mots-clés : Tableur, suivi, joueurs
- Résumé : Classeur permettant le suivi des joueurs.
- Responsable : SRP - Hulgo
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Organisation Pôle Lore (feuille)** (`sheet-organisation-pole-lore`)
- Statut : En cours de rédaction
- Accès : Restreint, sur autorisation

**Organisation Pôle RP (feuille)** (`sheet-organisation-pole-rp`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Organisation Pôle RP - Civil/Légal (feuille)** (`sheet-pole-rp-civil-legal`)
- Statut : Possibilité de modifier 
- Mots-clés : suivi, pôle, civil, MJ
- Résumé : Liste des suivis Civil
- Responsable : SRP - MJ - Civil
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

**Organisation Pôle RP – Familles (onglet 1)** (`sheet-organisation-familles`)
- Statut : Possibilité de modifier 
- Mots-clés : suivi, MJ, famille
- Résumé : Liste des suivis des familles
- Responsable : SRP - MJ - Famille
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

**Organisation Pôle RP – Illégal (onglet 1)** (`sheet-organisation-illegal`)
- Statut : Possibilité de modifier 
- Mots-clés : suivi, pôle, illégal, MJ
- Résumé : Liste des suivis Illégal
- Responsable : SRP - MJ - Illégal
- Accès : Restreint, sur autorisation
- Remarque : MAJ :

**Recrutement MJ** (`recrutement-mj`)
- Statut : Validé
- Mots-clés : recrutement, MJ, méthode
- Résumé : Document de référence pour gérer le processus de recrutement des MJ.
- Responsable : SRP - Hulgo
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Régles** (`regles`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

### Modèles & templates

**Copie de MODÈLE SUIVI (gabarit suivi académique, restylé)** (`modele-suivi-academique`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**MODÈLE SUIVI à copier-coller 18/11 (source du gabarit)** (`modele-suivi-copier-coller-18-11`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Squelette Naissance Famille v1** (`squelette-naissance-famille`)
- Statut : Possibilité de modifier 
- Mots-clés : modèle, template, candidature, famille, naissance
- Résumé : Modèle de candidature pour une naissance famille.
- Responsable : SRP - MJ - Famille
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Squelette suivi MJ** (`squelette-suivi-mj`)
- Statut : Possibilité de modifier 
- Mots-clés : règles, fonctionnement, mod-le, organisation, suivi, rrp, srp
- Résumé : Document de référence concernant les suivis MJ à destination du staff pôle RP.
- Responsable : SRP - Hulgo
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Template création spell** (`template-creation-spell`)
- Statut : Possibilité de modifier 
- Mots-clés : modèle, règle, lore, MJ, spell, sorts
- Résumé : Il vous permet de crée vos spell pour les suivis, attention, il faudra reporter vos idées dans le tableau : Propositions de sorts MJ.
- Responsable : SRP - Hulgo
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Template création vidéo** (`template-creation-video`)
- Statut : Possibilité de modifier 
- Mots-clés : modèle, template, vidéo, création, MJ
- Résumé : Modèle de fichier à compléter pour toute demande de création de vidéo.
- Responsable : SRP - Hulgo
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Template dossiers HRP** (`template-dossier-hrp`)
- Statut : Possibilité de modifier 
- Mots-clés : modèle, template, MJ, HRP
- Résumé : Modèle de fichier à compléter pour tout dossier HRP
- Responsable : SRP - Hulgo
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Template dossiers RP** (`template-dossier-rp`)
- Statut : Possibilité de modifier 
- Mots-clés : modèle, template, MJ, RP
- Résumé : Modèle de fichier à compléter pour tout dossier HR
- Responsable : SRP - Hulgo
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

**Template entreprise** (`template-entreprise`)
- Statut : Validé
- Mots-clés : modèle, fiche, création, joueur, entreprise, légal, illégal
- Résumé : Squelette de demande de création d'entreprise.
- Accès : Commun au Pôle RP
- Remarque : 01/11/2026

**Template suivie / trame** (`template-suivi-trame`)
- Statut : Possibilité de modifier 
- Mots-clés : modèle, template, MJ, suivi, trame
- Résumé : Modèle de fichier à compléter pour tout suivi de joueur.
- Responsable : SRP - Hulgo
- Accès : Restreint, sur autorisation
- Remarque : MàJ :

### Jeu (commandes)

**Commandes & Raccourcis Importants** (`commandes-raccourcis-B`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Commandes & Raccourcis Importants (Greatowl)** (`commandes-raccourcis-A`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

### Wiki officiel WikiWood (public)

**AMRU** (`wiki-amru`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Accueil** (`wiki-accueil`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Aetherion** (`wiki-bestiaire--rang-s--aetherion`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Akkorokamui** (`wiki-bestiaire--rang-s--akkorokamui`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Algue Commune** (`wiki-herbier--plantes-innofensives--algue-commune`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Angélique d'Elderwood** (`wiki-herbier--plantes-surveillees--angelique-delderwood`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Araignée d'Ether** (`wiki-bestiaire--rang-aa--araignee-dether`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Armoise Lunaire** (`wiki-herbier--plantes-innofensives--armoise-lunaire`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Baie de Lyandrelle** (`wiki-herbier--plantes-surveillees--baie-de-lyandrelle`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Bondiluce** (`wiki-bestiaire--rang-a--bondiluce`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Bonne-Haleine des Landes** (`wiki-herbier--plantes-innofensives--bonne-haleine-des-landes`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Braisière des coteaux** (`wiki-herbier--plantes-innofensives--braisiere-des-coteaux`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Brisecerat** (`wiki-bestiaire--rang-a--brisecerat`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Cactus-Tonneau des serres** (`wiki-herbier--plantes-innofensives--cactus-tonneau-des-serres`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Champignon Brun** (`wiki-herbier--plantes-innofensives--champignon-brun`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Champignon Phosphorescent** (`wiki-herbier--plantes-innofensives--champignon-phosphorescent`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Cheminante des grèves** (`wiki-herbier--plantes-surveillees--cheminante-des-greves`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Chronologie** (`wiki-chronologie`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Dame de l'heure** (`wiki-herbier--plantes-innofensives--dame-de-lheure`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Dictame de Crète** (`wiki-herbier--plantes-innofensives--dictame-de-crete`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Discpline et sanctions** (`wiki-reglement-hrp--discpline-et-sanctions`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Délieuse des rocailles** (`wiki-herbier--plantes-innofensives--delieuse-des-rocailles`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Echomys** (`wiki-bestiaire--rang-a--echomys`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Entités** (`wiki-bestiaire--entites`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Ephyr** (`wiki-bestiaire--rang-s--ephyr`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Famille Belladorn** (`wiki-familles-notables--famille-belladorn`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Famille Caerwyn** (`wiki-familles-originelles--famille-caerwyn`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Famille Dravenholt** (`wiki-familles-originelles--famille-dravenholt`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Famille Hearthbane** (`wiki-familles-originelles--famille-hearthbane`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Famille Ravenscroft** (`wiki-familles-notables--famille-ravenscroft`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Famille Valemont** (`wiki-familles-originelles--famille-valemont`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Familles Notables** (`wiki-familles-notables`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Familles Originelles** (`wiki-familles-originelles`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Folumix** (`wiki-bestiaire--rang-aa--folumix`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Fougère mâle** (`wiki-herbier--plantes-surveillees--fougere-male`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Glossaire** (`wiki-glossaire`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Golem Runique** (`wiki-bestiaire--rang-aaa--golem-runique`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Golem Sylvestre** (`wiki-bestiaire--rang-aaa--golem-sylvestre`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Gourde d'Office** (`wiki-herbier--plantes-innofensives--gourde-doffice`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Gratte Mur / Arcanophage** (`wiki-bestiaire--rang-aa--gratte-mur-arcanophage`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Griffon** (`wiki-bestiaire--rang-a-2--griffon`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Guide de candidature** (`wiki-guide-de-candidature`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Herbier** (`wiki-herbier`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Histoire d'Elderwood** (`wiki-histoire-delderwood`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Jackalope** (`wiki-bestiaire--rang-a--jackalope`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**L'Écho** (`wiki-principes-fondamentaux--lecho`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**L'Échoïde** (`wiki-bestiaire--entites--les-echoides`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**L'île, hors du château** (`wiki-les-lieux--lile-hors-du-chateau`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**La Résonance** (`wiki-principes-fondamentaux--la-resonance`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**La Source** (`wiki-les-lieux--la-source`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Le Bestiaire** (`wiki-bestiaire`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Le Flux** (`wiki-principes-fondamentaux--le-flux`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Le Voile** (`wiki-principes-fondamentaux--le-voile`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Le château** (`wiki-les-lieux--le-chateau`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Les couleurs du Flux** (`wiki-principes-fondamentaux--les-couleurs-du-flux`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Les formes de magie** (`wiki-principes-fondamentaux--les-formes-de-magie`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Les lieux** (`wiki-les-lieux`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Les maisons** (`wiki-les-maisons`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Les statuts magiques** (`wiki-principes-fondamentaux--les-statuts-magiques`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Lexique RP** (`wiki-reglement--lexique-rp`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Maison Aerwyn** (`wiki-les-maisons--maison-aerwyn`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Maison Brumval** (`wiki-les-maisons--maison-brumval`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Maison Falcon** (`wiki-les-maisons--maison-falcon`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Maison Venatrix** (`wiki-les-maisons--maison-venatrix`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Mange-Lumière / Luciphage** (`wiki-bestiaire--rang-aa--mange-lumiere-luciphage`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Matriarche (Araignée d'Ether)** (`wiki-bestiaire--rang-aaaa--matriarche`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Menthe Poivrée** (`wiki-herbier--plantes-innofensives--menthe-poivree`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Misa** (`wiki-bestiaire--rang-a--misa`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Multaille** (`wiki-bestiaire--rang-aa--multaille`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Mycollin** (`wiki-bestiaire--rang-a--mycollin`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Obligeante des haies** (`wiki-herbier--plantes-innofensives--obligeante-des-haies`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Ornicabal** (`wiki-bestiaire--rang-aaa--ornicabal`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Papillodactyle** (`wiki-bestiaire--rang-a--papillodactyle`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Pastenague** (`wiki-bestiaire--rang-a--pastenague`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Patiente des murs** (`wiki-herbier--plantes-innofensives--patiente-des-murs`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Personnages illustres** (`wiki-personnages`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Peseuse commune** (`wiki-herbier--plantes-innofensives--peseuse-commune`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Plantes innoffensives** (`wiki-herbier--plantes-innofensives`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Plantes surveillées** (`wiki-herbier--plantes-surveillees`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Pleurote des ombres** (`wiki-herbier--plantes-innofensives--pleurote-des-ombres`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Points de maison** (`wiki-reglement-hrp--points-de-maison`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Praedacornis** (`wiki-bestiaire--rang-aa--praedacornis`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Prenante des rives** (`wiki-herbier--plantes-innofensives--prenante-des-rives`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Principes fondamentaux** (`wiki-principes-fondamentaux`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Radicule** (`wiki-bestiaire--rang-a--radicule`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Rang A** (`wiki-bestiaire--rang-a-2`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Rang B** (`wiki-bestiaire--rang-aaaa`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Rang C** (`wiki-bestiaire--rang-aaa`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Rang D** (`wiki-bestiaire--rang-aa`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Rang E** (`wiki-bestiaire--rang-a`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Rang S** (`wiki-bestiaire--rang-s`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Règlement** (`wiki-reglement`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Règlement RP** (`wiki-reglement--reglement-rp`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Règlement général** (`wiki-reglement--reglement-general`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Règlement intérieur** (`wiki-reglement-hrp`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Scalvignus** (`wiki-bestiaire--rang-aa--scalvignus`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Shpouts** (`wiki-bestiaire--rang-a--shpouts`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Valdorn** (`wiki-bestiaire--rang-s--valdorn`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

**Zones RPK** (`wiki-reglement--zones-rpk`)
- (hors Bibliothèque du pôle RP : pas de métadonnées officielles)

## 3. Niveaux d'accès (à respecter dans le site)

Dans la Bibliothèque du pôle RP, presque tous les documents sont « Restreint, sur autorisation ». Règle proposée :
- **Public joueurs :** Bible du Lore, Bestiaire, Brûlebrume, Runomancie (lore + dictionnaire), Draconique, Catalyseurs, Cristaux-Cœurs, Échoïdes, Maladies magiques, Objets magiques, Potions, Sorts in game, Malédictions, Shedwood, lore des familles « connu des joueurs » (Valemont, Dravenholt, Ravenscroft, Belladorne, Caerwyn, Hearthbane), règlements intérieurs, Constitution (une fois validée), Commandes du jeu.
- **Staff / pôle RP uniquement :** tout ce qui est suivi MJ, trames, organisation du pôle, templates, dossiers HRP, recrutement, liste des professeurs (CONFIDENTIEL), « DA FAMILLE » (lore complet des familles, secrets inclus), documents Illégal (règlement, métiers, reliques maudites, potions illégales), questions de lore à trancher, Reliques de Maison (« à protéger »), Magie proscrite, Règlement staff, Autorisations & Permissions.
- En cas de doute : staff. Antonio tranchera.

## 4. Glossaire de départ (à enrichir depuis les textes)

Écho, Résonance, Flux, Distorsion (discipline Altération), Runomancie, accords consacrés, Catalyseur, Cristal-Cœur, Échoïde, Dissonant, Brûlebrume, AMRU (voir « Histoire de l’AMRU & idée de Lois » et « Police Magique AMRU »), Pacte du Voile, Shedwood, maisons : Brumval, Aerwyn, Falcon, Venatrix. Maisons-familles : Valemont, Dravenholt, Ravenscroft, Belladorne, Caerwyn, Hearthbane. Tiers de progression : T1 Initiation (0–99 XP), T2 Révélation (100–199), T3 Ascension (200–299), T4 Transcendance (300–399), T5 Maître (400–500). Échelle des punitions : personnel hors professeurs 1–3, intendants 1–5, directeurs de Maison 1–7, directeur + adjoint 1–8 ; la direction valide dès 25 points.

## 5. Avertissements sur les sources

- Instantané du 18–19/11/2026. Les Google Docs évoluent.
- Plusieurs versions d'un même doc coexistent (Brumval v1 à v4, Aerwyn v1/v2, copies du Pacte du Voile, deux brouillons de Constitution). Afficher la version la plus récente en premier et ranger les anciennes dans « Archives ».
- Des docs liés n'ont pas pu être lus (non partagés ou Notion/Canva/Miro) : Boucles RP school, B.R.U.M.E, guide candidatures naissance, familles non officielles, suivi des lieux in-game, 5 guides Notion de suivis MJ, organigrammes Canva et Miro. Prévoir des pages vides « contenu à venir » pour eux.
- Les feuilles de calcul ne sont lues qu'en valeurs, et seulement le premier onglet pour certaines.
- Contradictions possibles entre documents (ex. règlement vs lore) : ne pas arbitrer, signaler.

## 6. TEXTE INTÉGRAL DES DOCUMENTS

Chaque document est délimité par `<<< DOC key >>>` … `<<< FIN key >>>` pour un découpage automatique.

