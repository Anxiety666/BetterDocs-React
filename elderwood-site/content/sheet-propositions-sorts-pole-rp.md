# Propositions de sorts Pôle RP (feuille)

- Catégorie : Sorts
- Statut de rédaction : Possibilité de modifier 
- Mots-clés : spell, sort, GD, MJ, lore
- Résumé officiel : Document de liaison entre le pôle RP et le GD concernant les sorts.
- Niveau d’accès : Restreint, sur autorisation
- Remarques : MAJ :

---

##### FEUILLE: Vue d’ensemble
ELDERWOOD  /  Grimoire des sorts
ACADÉMIQUE • FAMILLES • MÉTIERS     /     Toutes les propositions, réunies au même endroit.
ENSEMBLE | ACADÉMIQUE | FAMILLE | MÉTIERS | PARAMÈTRES
Nom du spell | Type de suivi | Domaine / Famille / Métier | Palier d’obtention | Statut | Rang / Année
L'étoile du berger | Académique | Astronomie & Divination | Palier 4 | Brouillon | #REF!
L'appel de la nature (BAXTOF) | Académique | Zoomancie | Palier 4 | Brouillon | #N/A
Boussole astrale (BBC) | Académique | Astronomie & Divination | Palier 4 | Brouillon | #N/A
Balise Magique (BBC) | Académique | Astronomie & Divination | Palier 4 | Brouillon | #N/A
Aura astrale (BBC) | Académique | Astronomie & Divination | Palier 4 | Brouillon | #N/A
Etoiles Jumelles (BBC) | Académique | Astronomie & Divination | Palier 4 | Brouillon | #N/A
Présence illusoire (BBC) | Académique | Astronomie & Divination | Palier 4 | Brouillon | #N/A
Poussière révélatrice (BBC) | Académique | Astronomie & Divination | Palier 4 | Brouillon | #N/A
Ancre du destin (BBC) | Académique | Astronomie & Divination | Palier 4 | Brouillon | #N/A
Masque d'emprunt (BBC)  | Académique | Métamorphose | Palier 4 | Brouillon | #N/A
Nouvelle Parure (BBC) | Académique | Métamorphose | Palier 4 | Brouillon | #N/A
Trompe-l'oeil (BBC) | Académique | Métamorphose | Palier 4 | Brouillon | #N/A
Souffle de Vie (ELI) | Académique | Survie | Palier 4 | Brouillon | #N/A
Vision d'Aetherion (ELI) | Académique | Survie | Palier 4 | Brouillon | #N/A
Zone de soin (BBC) | Académique | Médimancie | Palier 4 | Brouillon | #N/A
Bouclier salvateur (KUMA) | Académique | Médimancie | Palier 4 | Brouillon | #N/A
Attirance vitale (BBC) | Académique | Médimancie | Palier 4 | Brouillon | #N/A
Cocon de survie (KUMA) | Académique | Médimancie | Palier 4 | Brouillon | #N/A
Flaque toxique (KUMA) | Académique | Médimancie | Palier 4 | Brouillon | #N/A
Chaîne d'attraction (BBC) | Académique | Survie | Palier 4 | Brouillon | #N/A
Ruée spectrale (BBC) | Académique | Arts défensifs | Palier 4 | Brouillon | #N/A
Pic de glace (BBC) | Académique | Arts du combat | Palier 4 | Brouillon | #N/A
Bouclier de feu (BBC) | Académique | Arts défensifs | Palier 4 | Brouillon | #N/A
L'étreinte du serpent (MEHIDI) | Académique | Métamorphose | Palier 4 | Brouillon | #N/A
Le cri de chauve-souris (MEHIDI) | Académique | Zoomancie | Palier 4 | Brouillon | #N/A
Le regard de la méduse (MEHIDI) | Académique | Métamorphose | Palier 4 | Brouillon | #N/A
Sleep lilia en deux temps | Académique | #N/A
Spell lissandra en deux temps | Académique | #N/A
Spell vlad (famille nocteran) | Académique | #N/A
Spell bombe zilean (belladorn) | Académique | #N/A
Stella aero (eclypse) | Académique | Astronomie & Divination | Palier 5 | Brouillon | #N/A
Nirvana Stellarum (eclypse) | Académique | Astronomie & Divination | Palier 4 | Brouillon | #N/A
Constella Vita (eclypse) | Académique | Astronomie & Divination | Palier 4 | Brouillon | #N/A
Entrave | Métier | Veilleur | À définir | Brouillon
Historia sort | Métier | Veilleur | À définir | Brouillon

##### FEUILLE: Sorts académiques
ELDERWOOD | Sorts académiques | Conception & développement | L’expérience en jeu
GRIMOIRE • PÔLE MJ | Une ligne par sort. Passer sur « À examiner » une fois la fiche prête. | Comportement du sort, hitbox, effets visuels, animation et son. | Les informations affichées aux joueurs.
ENSEMBLE | ACADÉMIQUE | FAMILLE | MÉTIERS | PARAMÈTRES
01  /  PROPOSITION | RETOUR GAME DESIGN | 02  /  ATTRIBUTION | 03  /  CÔTÉ DÉVELOPPEUR | 04  /  IN GAME UI/UX
Nom du spell | Statut | Retour Game Design | Domaine | Palier d’obtention | Instruction Dev P1 | Instruction Dev P2 | Instruction Dev P3 | Instruction Dev P4 | Taille Hitbox | VFX | Animation modèle joueur | SFX | Nom affiché | Domaine 2 | Description en jeu | Visuel de l’icône | Notes
L'étoile du berger | Brouillon | Astronomie & Divination | Palier 4 | Le joueur lance l’étoile devant lui. Sa caméra passe dans l’étoile et il la pilote librement dans la limite de portée. Son personnage reste immobile et vulnérable. | Une réactivation immobilise l’étoile à sa position. Le joueur continue de voir à travers elle et peut tourner la caméra, mais ne peut plus la déplacer. | Dernière réactivation : l’étoile se dissipe et le joueur retrouve immédiatement la caméra et le contrôle de son personnage. Le délai de récupération commence. | Petite | Petit noyau lumineux blanc bleuté, quelques pointes évoquant une étoile, traînée courte pendant le déplacement. Visible par les autres joueurs, sans éclairer toute la pièce. Dissipation en particules à la destruction. | Réutilisation d’une animation d’incantation, puis posture de concentration pendant le pilotage. Retour à la posture normale en quittant la vision. | Bruit simple de sort au lancement / Bruit constant d'ambiance (particule/étoiles) | L'étoile du berger | Astronomie & Divination | Fait naître une étoile lumineuse que le mage guide par la pensée. Son regard se lie à l’astre, lui permettant d’observer les lieux que celui-ci parcourt, tandis que son corps demeure immobile, plongé dans une profonde concentration. | Une étoile blanc bleuté à quatre branches au centre d’un œil stylisé argenté, sur fond bleu nuit. Halo léger et courte traînée lumineuse. .
L'appel de la nature (BAXTOF) | Brouillon | Zoomancie | Palier 4 | Le joueur émet une impulsion magique audible dans une zone autour de lui | Les créatures magiques présentes dans la zone sont attirées vers la source du sort, si elles étaient en combat leur "cible" n'a plus d'importances | L'effet cesse quand le joueur réactive la compétence ou après une durée de temps | Grosse | Ondes circulaires partant du joueur | Le joueur porte son catalyseur à sa bouche puis effectue un geste d'appel | L'Appel de la Nature | Zoomancie
Boussole astrale (BBC) | Brouillon | Astronomie & Divination | Palier 4 | Fait apparaître une aiguille lumineuse devant le lanceur. | Elle suit le joueur tout en indiquant le nord. | Réactivation pour la dissiper. | Petite | une étoile avec une pointe plus longue orientée vers le nord. | Réutilisation d’une animation d’incantation | Boussole Astrale | Astronomie & Divination | Une aiguille de lumière s’aligne sur le nord et accompagne les voyageurs égarés. | une étoile à quatre branches dont une pointe se prolonge.
Balise Magique (BBC) | Brouillon | Astronomie & Divination | Palier 4 | Pose une balise lumineuse au sol qui détecte et avertis le joueurs via une alerte quand une personne rentre dans la radius de la balise | Pose une seconde balise lumineuse au sol  | Réactivation pour dissiper la balise 1 | Réactivation pour dissiper la balise 2 | Petite | Balise argentée  | Geste de baguette vers l’endroit choisi. | Balise Magique | Astronomie & Divination | Fixe une balise au sol pour que les voyageurs puissent s'orienter ou être avertis d'un danger potentiel. | une balise lumineuse sur un sol
Aura astrale (BBC) | Brouillon | Astronomie & Divination | Palier 4 | Invoque autour du lanceur une aura remplie d'étoiles, qui lui permet d'augmenter ses chances de parer et de renvoyer les sorts qui lui sont lancés | Réactivation pour la dissiper | Aura Astrale | Astronomie & Divination
Etoiles Jumelles (BBC) | Brouillon | Astronomie & Divination | Palier 4 | Crée un lien avec une personne proche qui transfère une partie des dégats reçus à son binome | Après activation, chacun porte une petite étoile. Au-delà d’une distance définie, les étoiles se brisent et préviennent les deux joueurs. | Réactivation pour la dissiper. | Petite | Petite étoile à côté de chaque personnage qui s'évapore à la désactivation | incantation vers la cible. | Etoiles Jumelles | Astronomie & Divination | Accorde deux êtres sous un même signe céleste. Lorsque leurs chemins s’éloignent, leurs étoiles se brisent | Deux silhouette avec un lien entre les deux
Présence illusoire (BBC) | Brouillon | Astronomie & Divination | Palier 4 | le joueur place une copie de son personnage à un point visible et accessible, à quelques mètres. | le double reste immobile dans une posture prédéfinie. Il n’a aucune collision et disparaît lorsqu’il reçoit un sort. | Réactivation pour le dissiper. | Moyenne | Copie du personnage. Disparition en poussière étoilée. | incantation classique pour le lanceur -> posture d’attente existante pour le double. | Présence Illusoire | Astronomie & Divination | Matérialise un double illusoire, une projection spectrale de votre propre existence | Deux silhouettes décalées, dont une se disperse en étoiles
Poussière révélatrice (BBC) | Brouillon | Astronomie & Divination | Palier 4 | le joueur projette un cône de poussière étoilée devant lui, sur une courte portée, affectant les personnes présentes dans la zone. | les personnages touchés portent des particules lumineuses et laisse des traces sur le sol pendant une durée de X secondes. | Réactivation ou fin de durée : les particules attachées aux cibles disparaissent. | Moyenne | Jet de poussière argentée, puis scintillements sur les vêtements des personnages touchés. | balayage de baguette existant. | souffle sec au lancement, léger crépitement à l’impact. | Poussière Révélatrice | Astronomie & Divination | Répand une poussière d'étoiles qui s’accroche aux silhouettes et trahit leurs mouvements dans la pénombre. | Une silhouette sombre parsemée d’étoiles.
Ancre du destin (BBC) | Brouillon | Astronomie & Divination | Palier 4 | le joueur pose une ancre lumineuse à ses pieds. | une seconde activation, dans les limites proposées de X secondes et X mètres, lance une incantation interruptible avant le retour à l’ancre. | Réactivation ou fin de durée : Le personnage s'évapore en poussière d'étoiles et se téléporte à la balise après une incantation interruptible (il est possible d'annuler la canalisation pour stopper la réapparition). | Petite | étoile inscrite dans un cercle au sol. Au retour, le personnage se disperse puis se reforme en particules argentées. | geste vers le sol à la pose, posture de concentration avant le retour | Ancre du Destin | Astronomie & Divination | Attache votre destinée à une étoile immobile, vers laquelle vos pas pourront être rappelés. | Une étoile bleutée qui revient vers son centre/base, sur fond sombre.
Masque d'emprunt (BBC)  | Brouillon | Métamorphose | Palier 4 | le joueur enregistre le visage d'une cible (cheveux/couleurs des yeux/maquillage/tatouage/teint) | Le joueur change son visage avec celui de la cible pendant X minutes | Réactivation ou fin de durée : le visage reprend sa forme initiale | Petite | voile de fumée autour du visage pendant la transformation. | passage de baguette devant le visage. | bruit de fumée | Masque d'emprunt | Métamorphose | Remodèle les traits de votre visage pour vous donner une apparence d’emprunt. | Deux moitiés de visage différentes
Nouvelle Parure (BBC) | Brouillon | Métamorphose | Palier 4 | le joueur enregistre la tenue d'une cible | Le joueur change sa tenue avec celui de la cible pendant X minutes | Réactivation ou fin de durée : le joueurs reprend sa tenue initiale | Petite | Voile de fumée autour de la tenue ou animation du personnage qui tourne sur lui même avec switch de tenue pendant l'animation pour camouflés le changement brut de tenue | passage de baguette devant la tenue du personnage | Nouvelle Parure | Métamorphose | Remodèle l’étoffe que vous portez pour lui donner une nouvelle coupe et une nouvelle allure. | Une robe divisée en deux couleurs
Trompe-l'oeil (BBC) | Brouillon | Métamorphose | Palier 4 | le joueur choisit une forme parmi plusieurs meubles (ou via principe de prophunt) : une chaise, un tonneau, une caisse, une pile de livre, .... | son personnage est remplacé visuellement par l’objet. Il peut regarder autour de lui mais reste immobile et ne peut pas lancer de sort hormis celui-ci. | Réactivation, dégâts ou expiration : retour à la forme humaine. | Petite | petit nuage de fumée lors des deux transformations. | courte incantation avant disparition du personnage. | bruit de transformation, accompagné d’un son de bois. | Mobilier Vivant | Métamorphose | Adopte l’apparence d’un objet ordinaire pour se fondre dans le décor. | Un objet avec deux yeux.
Souffle de Vie (ELI) | Brouillon | Survie | Palier 4 | Le joueur désigne une zone pour déposer un feu de camp | Le joueur pose le feu de camp, les personnes présentes dans un radius déterminé récupére ainsi des PV | Après un certains temps ou nombre de PV rendu (Le feu de camp peut avoir un nombre de PV max a restauré), il disparait et le timer du sort redémarre. | Moyenne | Feu de camp avec une flamme de couleur bleu. | Geste de baguette vers l’endroit choisi. | Bruit de Souffle accompagné d'un craquement de bois. | Souffle de Vie | Survie | Du feu est né la vie | Un feu de camp au milieu d'une foret 
Vision d'Aetherion (ELI) | Brouillon | Survie | Palier 4 | Le joueur lance une vague de flux devant lui | Si dans un radius déterminé des ennemis ( Joueur, PNJ...) sont présents ils seront alors entourés d'un halo de couleur rouge pour les identifiers plus facilement | Après un certains temps, le halo se disparait et le timer du sort redémarre. | Grosse | Emission d'une onde de flux Orange très brillante (en forme d'oiseau, faucon, rapace?) devant le lanceur | Geste de baguette vers l’endroit choisi. | Bruit de rapace | Vision d'Aetherion | Survie | Tu feras apparaitre le danger | Une tête de rapace | C'est un sort incluant un peu du lore de la maison Falcon voir si cela ne dérange pas avec les sorts de Famille
Zone de soin (BBC) | Brouillon | Médimancie | Palier 4 | Le joueurs crée une zone de soin dans un radius de X autour de lui pendant X secondes, les entités qui pénètrent à l'intérieur sont soigné de X point de vie par secondes | La zone de soin disparait | Moyenne | Geste incantation classique | Bruit de heal et de création de zone | xxxxx | Médimancie | xxxxxxxxx | Un cercle vert magique autour d'un groupe de personne
Bouclier salvateur (KUMA) | Brouillon | Médimancie | Palier 4 | Le joueur crée un bouclier autour de lui, qui lui empêche de subir tous les types de CC pendant X secondes | le bouclier disparait après les X secondes | Petite | Une orbe en particule verte scintillante | Geste incantation classique | Médimancie | Créer un bouclier qui vous protège de tout les contrôles de foules pendant X secondes  | Orbe vert fait de petite lumière scintillante
Attirance vitale (BBC) | Brouillon | Médimancie | Palier 4 | Le joueur lance un sort sur sa cible, ce qui l'attire vers lui et la soin de X point de vie | Le joueur relance le sort et réactive l'effet, la cible est attiré et est soigner de X point de vie | Petite | Flux vert qui fini en anneau qui entoure la cible (comme une corde ou un lasso) | Incantation pour lancer le sort et mouvement de baguette vers le torse quand ça attire la cible | Atractio Vitae | Médimancie | Le lanceur projette un lasso vert qui soigne la cible et la tire vers lui. Le sort peut être réactivé pour l'attirer et la soigner une seconde fois. | Un personnage qui envoie le "lasso" vert sur une silhouette 
Cocon de survie (KUMA) | Brouillon | Médimancie | Palier 4 | le joueur lance un sort sur un allié, le transforme en cocon d'araignée. La personne est invulnérable pendant X secondes, et régenère ses HP de X%. | Le joueur transformé ne peux pas bouger, ni utiliser de compétence ou d'objet | après X secondes le joueur retrouve son apparence, sa mobilité, capacité.... | Petite | un cocon en toile d'araigné, d'une forme humaine, 100% opaque, on ne voit pu le joueur | Geste de baguette vers l’endroit choisi. | Bruit de scrétion de toile comme spider man | Médimancie | Emprisonne un allié dans un cocon d'araignée pour le rendre invulnérable pendant X secondes et le soigne de x% de ses points de vie | Cocon d'araignée en forme d'humain
Flaque toxique (KUMA) | Brouillon | Médimancie | Palier 4 | Le joueur crée une flaque de liquide toxique au sol d'un radius X mètres à l'endroit ciblé.  | Les ennemies qui pénètrent ou restent à l'intérieur subissent X dégâts de poison par seconde et sont ralenties de X %. | après X secondes la flaque disparait, fin du poison et fin du ralentissement | Moyenne | Flaque liquide violette avec des bulles comme une ébulition | Geste de baguette vers l’endroit choisi. | Bruit de sécrétion de venin d'un serpent | Médimancie | Lance une flaque de poison qui inflige X de dégats par seconde pendant X secondes et ralenti de X% | flaque de poison 
Brouillon | Médimancie | Palier 4
Chaîne d'attraction (BBC) | Brouillon | Survie | Palier 4 | Le lanceur crée une zone enflammée devant lui. Au bout de X secondes, des chaînes enflammées surgissent pour rammener toutes les cibles vers le centre en leur infligeant X dégâts. | Moyenne | Une zone de feu avec des chaines qui attire les cibles au centre de la zone  | Geste d'incantation classique | Bruit classique de zone enflammé, suivi d'un bruit de chaine métallique | Catena Ignis | Survie | Le lanceur fait surgir une zone de feu au sol dont les chaînes incandescentes se resserrent brutalement, attirant toutes les cibles au milieu et leur infligeant d'impitoyables brûlures. | Une zone de feu traversée par des chaînes.
Ruée spectrale (BBC) | Brouillon | Arts défensifs | Palier 4 | Le lanceur effectue une ruée dans la direction visé | Le lanceur peut réactiver le sort pour effectuer une seconde ruée | Petite | Une animation de ruée rapide du personnage avec des particules fines derrière lui pour appuyer sur le côté vitesse | Mouvement vif du corps ou de la baguette vers la trajectoire souhaitée | Bruit de mouvement rapide et éclat de particule | Passus Umbra | Arts défensifs | Le sorcier fend l'air et fonce vers l'avant dans une traînée de poussière spectrale. Avant même que l'ennemi ne réagisse, il peut réitérer sa charge pour enchaîner un second bond. | Une silhouette qui court avec des effets de vitesse derrière lui
Pic de glace (BBC) | Brouillon | Arts du combat | Palier 4 | Le lanceur envoie un pic de glace dans une direction, à l'impact le pic explose infligeant X dégats et crée une zone de givre autour qui slow les cibles qui passe à l'intérieur | Moyenne | Un pic de glace qui explose et crée une zone de givre au sol | Geste incantation classique ++ | Sifflement de vent glacial lors du vol, suivi d'un bruit d'explosion de cristal brisé et d'un craquement de glace qui gèle le sol | Glaciem Cuspis | Arts du combat | Le sorcier projette un épais pic de glace qui éclate violemment à l'impact. L'onde de choc tapisse le sol d'un gel arctique, ralentissant instantanément tous ceux qui tentent de le traverser | Un pic de glace foncant sur une cible
Bouclier de feu (BBC) | Brouillon | Arts défensifs | Palier 4 | Le lanceur s'enveloppe d'un bouclier de feu ce qui inflige X dégats/s de brûlures aux personnes qui lui envoie un sort lui infligeant des dégats pendant X secondes | A la réactivation, le bouclier explose et applique brûlures aux cibles proches du lanceur | A la fin de la durée, si aucune réactivation le bouclier disparait | Petite | Un bouclier en flamme ou une aura enflammé autour du lanceur et des VFX de brulures | Geste incantation de protection | Bruit de crépitement, et de brûlures | Scutum Ignis | Arts défensifs | Le sorcier dresse une barrière enflammée autour de lui qui consume les attaques ennemies et inflige de cruelles brûlures en retour. D'un geste sec, il peut faire détoner cette aura ardente dans un souffle dévastateur. | Une silhouette entourée d'un bouclier de flammes.
L'étreinte du serpent (MEHIDI) | Brouillon | Métamorphose | Palier 4 | Le lanceur projette une corde qui se transforme en serpent et étrangle la cible l'immobilisant pendant X sec et lui infligeant X dégats | Petite | Une corde projetter depuis le catalyseurs qui se transforme en serpent au contact de la cible | Geste de lancer classique | Bruit de serpent (crachat) / bruit de Lasso/fouet ? | Viperae Vinculum | Métamorphose | Le lanceur projette un lien magique qui se métamorphose en serpent et s'enroule autour de sa cible. La créature l'étrangle et l'immobilise pendant quelques secondes, lui infligeant des dégâts avant de disparaître. | Un serpent vert enroulé sur lui-même, avec la gueule entrouverte.
Le cri de chauve-souris (MEHIDI) | Brouillon | Zoomancie | Palier 4 | Le lanceur projette des ultra-sons sous forme d'onde dans une périmètre de X autour de lui ce qui effraie les cibles (principe de fear?) | Moyenne | Des anneaux d'ondes translucides se propagent autour du lanceur. | Geste de lancer classique | sifflement ultrasonique accompagné d'une résonance magique | Clamor Vespertillionis | Zoomancie | Le lanceur libère un cri ultrasonique qui perturbe les sens des ennemis à proximité. Les cibles touchées sont désorientées et incapables d'agir pendant quelques secondes. | Une Chauve-souris noire aux ailes déployées entourée d'ondes sonores violettes
Le regard de la méduse (MEHIDI) | Brouillon | Métamorphose | Palier 4 | ultia cassio  | Moyenne
Sleep lilia en deux temps
Spell lissandra en deux temps
Spell vlad (famille nocteran)
Spell bombe zilean (belladorn)
Stella aero (eclypse) | Brouillon | Astronomie & Divination | Palier 5 | se transformant en lumières d'étoiles pour se mouvoir dans les aires
Nirvana Stellarum (eclypse) | Brouillon | Astronomie & Divination | Palier 4 | sort créant une pluie d'étoile a la lueur blanche (aoe) |  crée des flammes blanche au sol a l'impact dans un rayon défini (aoe)
Constella Vita (eclypse) | Brouillon | Astronomie & Divination | Palier 4 | crée un pentacle lumineux blancs/bleuté a ses pied représentant une constellation | éclaire la zone | Heal les personnes présente dans la zone

##### FEUILLE: Sorts de famille
ELDERWOOD | Sorts de famille | Conception & développement | L’expérience en jeu
GRIMOIRE • PÔLE MJ | Une ligne par sort. Passer sur « À examiner » une fois la fiche prête. | Comportement du sort, hitbox, effets visuels, animation et son. | Les informations affichées aux joueurs.
ENSEMBLE | ACADÉMIQUE | FAMILLE | MÉTIERS | PARAMÈTRES
01  /  PROPOSITION | RETOUR GAME DESIGN | 02  /  ATTRIBUTION | 03  /  CÔTÉ DÉVELOPPEUR | 04  /  IN GAME UI/UX
Nom du spell | Statut | Retour Game Design | Famille | Palier d’obtention | Instruction Dev P1 | Instruction Dev P2 | Instruction Dev P3 | Taille Hitbox | VFX | Animation modèle joueur | SFX | Nom affiché | Catégorie / Matière | Rang / Année | Description en jeu | Nom affiché | Catégorie / Matière | Rang / Année | Description en jeu

##### FEUILLE: Sorts de métiers
ELDERWOOD | Sorts de métiers | Conception & développement | L’expérience en jeu
GRIMOIRE • PÔLE MJ | Une ligne par sort. Passer sur « À examiner » une fois la fiche prête. | Comportement du sort, hitbox, effets visuels, animation et son. | Les informations affichées aux joueurs.
ENSEMBLE | ACADÉMIQUE | FAMILLE | MÉTIERS | PARAMÈTRES
01  /  PROPOSITION | RETOUR GAME DESIGN | 02  /  ATTRIBUTION | 03  /  CÔTÉ DÉVELOPPEUR | 04  /  IN GAME UI/UX
Nom du spell | Statut | Retour Game Design | Métier | Palier d’obtention | Instruction Dev P1 | Instruction Dev P2 | Instruction Dev P3 | Taille Hitbox | VFX | Animation modèle joueur | SFX | Nom affiché | Catégorie / Matière | Rang / Année | Description en jeu | Nom affiché | Catégorie / Matière | Rang / Année | Description en jeu
Entrave | Brouillon | Veilleur | À définir | desarmer + menotte +
Historia sort | Brouillon | Veilleur | À définir | Voir l'historique des dernier sort lancer

##### FEUILLE: Sorts Illégaux
Nom du spell | Statut | Retour Game Design | Métier | Palier d’obtention | Instruction Dev P1 | Instruction Dev P2 | Instruction Dev P3 | Taille Hitbox | VFX | Animation modèle joueur | SFX | Nom affiché | Catégorie / Matière | Rang / Année | Description en jeu
Silencio | Brouillon | À définir | À définir

##### FEUILLE: Paramètres
ELDERWOOD  /  Référentiels
Compléter les domaines, familles, métiers et matières pour les retrouver dans les menus.
ENSEMBLE | ACADÉMIQUE | FAMILLE | MÉTIERS | PARAMÈTRES
Statuts | Types de suivi | Paliers | Rangs / Années | Domaines académiques | Catégories / Matières | Utilisation | Familles | Métiers
Brouillon | Académique | À définir | À définir | Sortilèges | P1, P2 et P3 conservent les intitulés du squelette développeur. | Valemont | Alchimiste
À examiner | Famille | Palier 1 | 1re année | Arts défensifs | Le palier du suivi et le rang du sort sont deux champs distincts. | Dravenholt | Baguettier
À modifier | Métier | Palier 2 | 2e année | Métamorphose | VFX, animation et SFX : décrire le besoin et coller un lien de référence si utile. | Hearthbane | Balaimancien
Validé GD | Palier 3 | 3e année | Astronomie & Divination | Listes des menus : E pour les domaines, H pour les familles et I pour les métiers. F reste réservé aux catégories / matières en jeu. | Caerwyn | Artisan (légal)
En développement | Palier 4 | 4e année | Runomancie | A à D : valeurs de référence. Pour changer ces choix, modifier le menu de la colonne dans l’onglet de sorts concerné. | Nocteran | Cuisine magique
À tester | Palier 5 | 5e année | Zoomancie | Glenhart | Botanique
Disponible en jeu | Arts du combat | Source : Organisations MJ, onglet Suivis MJ. Les deux suivis Artisan sont distingués par leur catégorie légale ou illégale. | Ravenscroft | Bucheron
Refusé | Arts et culture | Belladorn | Mineur
Survie | Ouvrir le catalogue des suivis MJ | Alchimiste illégal
Médimancie | Contrebandier
Artisan (illégal)
Pilleur
Veilleur
