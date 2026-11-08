# Consignes pour Claude — site URBAIN V

Site vitrine d'URBAIN V (rénovation immobilière de prestige, 163 cours de la Libération, 38100 Grenoble), domaine urbain-v.fr. Le propriétaire (Stéphane Jouglard) écrit en français : répondre et rédiger en français.

## Déploiement

- La branche `main` est déployée automatiquement sur l'hébergement OVH (intégration Git + webhook GitHub). Tout ce qui est publié sur `main` part en ligne : ne publier qu'un site vérifié.
- Le propriétaire veut modifier son site directement depuis Claude, avec mise en ligne automatique : une fois la modification contrôlée (`python3 tools/verifier.py` et rendu), la publier directement sur `main`, sans demande de fusion à valider. Lui indiquer ensuite en une phrase ce qui a été mis en ligne.
- Site statique, sans étape de compilation : les fichiers du dépôt sont servis tels quels par Apache (`.htaccess` à la racine).
- Après une modification de `assets/css/site.css` ou `assets/js/site.js`, incrémenter le paramètre `?v=` de leurs liens dans **toutes** les pages (cache navigateur d'un mois).

## Structure

- Une page = un dossier avec `index.html` (adresses propres : `/investir/`, `/contact/`…), plus `index.html` (accueil) et `404.html`.
- L'en-tête, le pied de page et le sprite SVG du logo sont recopiés à l'identique dans chaque page : toute modification de l'un d'eux doit être reportée dans toutes les pages. La page active du menu est marquée par le script via `<body data-page="…">` et les attributs `data-nav`.
- Liens vers une section : `/operations/#avant-premiere`, `/savoir-faire/#methode`, `/savoir-faire/#performance`, `/investir/#dispositifs`, `/investir/#calendrier`, `/investir/#questions`, `/#actualites`, `/#questions`. Le formulaire de contact se présélectionne avec `/contact/?objet=acquerir|investir|ceder|partenariat|autre`.
- Les planches dessinées (`data-draw="…"`) sont générées en SVG par `assets/js/site.js`.
- Documents à télécharger : plaquette de présentation (`/documents/urbain-v-plaquette-2026.pdf`, proposée sur `/la-maison/#plaquette`) et guide de la fiscalité 2026 (`/documents/urbain-v-guide-fiscalite-2026.pdf`, sur `/investir/#guide`). Ce sont des versions allégées pour le web ; les versions d'impression sont dans le Drive « URBAIN V ». Sources et procédure : `tools/documents/LISEZMOI.md`. Après remplacement d'un PDF, incrémenter `?v=` de ses liens et mettre à jour le poids indiqué ; le guide fiscal se revérifie à chaque loi de finances, comme la page Investir.
- Actualités : `/actualites/` (liste) et `/actualites/<slug>/` (une page par actualité) sont **générées** par `python3 tools/actualites/build.py` à partir de `tools/actualites/articles.json` et de `tools/actualites/contenu/<slug>.html`. Le script reprend l’en-tête, le pied de page et les versions CSS/JS de `index.html`, et régénère aussi le bloc « Actualités » de l’accueil (entre `<!-- actualites:debut -->` et `<!-- actualites:fin -->`), le flux `/actualites/flux.xml`, les entrées `/actualites/` du sitemap et `/llms.txt`. Ne pas modifier ces fichiers à la main ; après toute modification de l’en-tête ou du pied de page, relancer le script. Procédure et règles (sources officielles, dates, textes en cours d’examen présentés comme tels) : `tools/actualites/LISEZMOI.md`. La rubrique est mise à jour chaque mois par une tâche planifiée.
- Référencement (Google et assistants IA) : chaque page porte son mot-clé principal dans le `<title>`, la description, le `h1` (le surtitre `.eyebrow` est placé dans le `h1`) et le premier paragraphe. FAQ en `<details>` avec données structurées FAQPage au texte identique au texte visible (accueil, Investir) ; données Organization et WebSite sur l’accueil ; `/llms.txt` résume le site pour les assistants. Mots-clés prioritaires (volumes mensuels Google France, nov. 2026) : rénovation appartement (22 200), rénovation énergétique (9 900), investissement locatif (6 600), déficit foncier (3 600), loi Jeanbrun (3 600), loi Denormandie (2 900), loi Malraux (1 900), défiscalisation immobilière (880), immobilier de prestige (480), défiscalisation monument historique (390), immeuble ancien, appartement ancien rénové. Les intégrer naturellement, sans bourrage ; « réhabilitation » est très peu recherché, préférer « rénovation » dans les titres.
- Réseaux sociaux : page LinkedIn https://www.linkedin.com/company/104622185/ (pied de page, bloc « Réseaux sociaux » de l'accueil, coordonnées de la page Contact, `sameAs` des données structurées). Instagram et Facebook restent « Bientôt » tant que les comptes n'existent pas.
- Images de la signature e-mail de Stéphane Jouglard : `assets/img/signature/` (`urbain-v-logo.png`, `bandeau.jpg`, `linkedin.png`). Les e-mails envoyés y font référence par leur adresse : ne pas les renommer, les déplacer ni les supprimer. `linkedin.png` est le logo « In » officiel de LinkedIn (fichier fourni par Stéphane, Drive « URBAIN V / Logos LinkedIn »), seulement redimensionné : ne pas le redessiner ni le recolorer.
- Nouvelle page : la créer sur le modèle d'une page existante (balises `<head>` complètes : titre, description, canonique, Open Graph), l'ajouter au menu et au pied de page de toutes les pages, et à `sitemap.xml`.
- Avant chaque publication : lancer `python3 tools/verifier.py` (blocs communs identiques, liens internes, balises, sitemap) et contrôler le rendu (bureau et mobile, thème clair et sombre).

## Charte graphique

- Couleurs du logotype : anthracite `#2B363F` (textes, bandeaux sombres) et vert `#439E70` (emblème, « V », accents). Vert approfondi `#2A7350` pour les petits textes sur fond clair, vert clair `#6FC398` pour les petits textes sur fond sombre. Toutes les couleurs sont des variables CSS dans `:root`, avec un thème sombre.
- Logotype officiel (fichiers sources dans le Drive « URBAIN V / URBAIN V LOGOTYPE ») : version couleur sur fond clair ; sur fond sombre, « URBAIN » en blanc avec l'étoile et le « V » en vert (planche « AXE 1 » du graphiste). Ne pas redessiner ni recomposer le logo ; l'étoile seule sert d'emblème (filigrane, favicon).
- Polices : EB Garamond (titres), Roboto Slab (petites capitales, en écho au logotype), Jost (texte courant).
- Baseline : « Restaurer · Sublimer · Transmettre ».

## Contenu : règles du propriétaire

- Ne pas parler de Novelia (Novelia Résidences, Novelia Aménagement) ni de CGBI sur le site. Deux exceptions seulement : la phrase sur l'origine dans La Maison (« URBAIN V est née au sein du Groupe Novelia… ») et les mentions légales, où le site est édité par GROUPE NOVELIA, qui exploite la marque commerciale URBAIN V (déposée à l'INPI, n° national 24 5031295).
- Mentions légales : éditeur GROUPE NOVELIA (SARL au capital de 2 700 000 €, RCS Grenoble 948 146 691, siège 53 chemin du Boutey, 38560 Champ-sur-Drac, d'après Pappers) ; directeur de la publication : Stéphane Jouglard ; hébergeur : OVH SAS.
- Territoire : ne pas trop mettre Grenoble en avant (elle reste l'adresse des bureaux). Mettre en avant le Dauphiné (Isère, Drôme, Hautes-Alpes) comme territoire d'origine et la capacité d'intervention dans tout le grand quart sud-est de la France.
- Aucune réalisation n'est encore livrée : les photos Unsplash sont des illustrations, jamais présentées comme des opérations URBAIN V. Tenir à jour la liste des photographes dans les mentions légales.
- Ne pas inventer de chiffres, de références ou de promesses. Les informations fiscales (page Investir) sont datées et accompagnées d'un avertissement : les revérifier à chaque loi de finances.
- Coordonnées : e-mail contact@urbain-v.fr (boîte à créer chez OVH, opérationnelle une fois le domaine basculé sur les serveurs DNS d'OVH) ; téléphone 06 83 48 06 15 (page Contact, mentions légales et pied de page). Formulaires en mode démonstration (aucun envoi) : ne jamais afficher qu'un message a été envoyé tant qu'un envoi réel n'est pas branché.
