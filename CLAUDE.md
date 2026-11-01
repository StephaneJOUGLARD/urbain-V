# Consignes pour Claude — site URBAIN V

Site vitrine d'URBAIN V (rénovation immobilière de prestige, 163 cours de la Libération, 38100 Grenoble), domaine urbain-v.fr. Le propriétaire (Stéphane Jouglard) écrit en français : répondre et rédiger en français.

## Déploiement

- La branche `main` est déployée automatiquement sur l'hébergement OVH (intégration Git + webhook GitHub). Tout ce qui est publié sur `main` part en ligne : ne publier qu'un site vérifié.
- Site statique, sans étape de compilation : les fichiers du dépôt sont servis tels quels par Apache (`.htaccess` à la racine).
- Après une modification de `assets/css/site.css` ou `assets/js/site.js`, incrémenter le paramètre `?v=` de leurs liens dans **toutes** les pages (cache navigateur d'un mois).

## Structure

- Une page = un dossier avec `index.html` (adresses propres : `/investir/`, `/contact/`…), plus `index.html` (accueil) et `404.html`.
- L'en-tête, le pied de page et le sprite SVG du logo sont recopiés à l'identique dans chaque page : toute modification de l'un d'eux doit être reportée dans toutes les pages. La page active du menu est marquée par le script via `<body data-page="…">` et les attributs `data-nav`.
- Liens vers une section : `/operations/#avant-premiere`, `/savoir-faire/#methode`, `/investir/#dispositifs`. Le formulaire de contact se présélectionne avec `/contact/?objet=acquerir|investir|ceder|partenariat|autre`.
- Les planches dessinées (`data-draw="…"`) sont générées en SVG par `assets/js/site.js`.
- Nouvelle page : la créer sur le modèle d'une page existante (balises `<head>` complètes : titre, description, canonique, Open Graph), l'ajouter au menu et au pied de page de toutes les pages, et à `sitemap.xml`.
- Avant chaque publication : lancer `python3 tools/verifier.py` (blocs communs identiques, liens internes, balises, sitemap) et contrôler le rendu (bureau et mobile, thème clair et sombre).

## Charte graphique

- Couleurs du logotype : anthracite `#2B363F` (textes, bandeaux sombres) et vert `#439E70` (emblème, « V », accents). Vert approfondi `#2A7350` pour les petits textes sur fond clair, vert clair `#6FC398` pour les petits textes sur fond sombre. Toutes les couleurs sont des variables CSS dans `:root`, avec un thème sombre.
- Logotype officiel (fichiers sources dans le Drive « URBAIN V / URBAIN V LOGOTYPE ») : version couleur sur fond clair ; sur fond sombre, « URBAIN » en blanc avec l'étoile et le « V » en vert (planche « AXE 1 » du graphiste). Ne pas redessiner ni recomposer le logo ; l'étoile seule sert d'emblème (filigrane, favicon).
- Polices : EB Garamond (titres), Roboto Slab (petites capitales, en écho au logotype), Jost (texte courant).
- Baseline : « Restaurer · Sublimer · Transmettre ».

## Contenu : règles du propriétaire

- Ne pas parler de Novelia (Novelia Résidences, Novelia Aménagement) ni de CGBI sur le site. Seule exception : la phrase sur l'origine dans La Maison (« URBAIN V est née au sein du Groupe Novelia… »).
- Aucune réalisation n'est encore livrée : les photos Unsplash sont des illustrations, jamais présentées comme des opérations URBAIN V. Tenir à jour la liste des photographes dans les mentions légales.
- Ne pas inventer de chiffres, de références ou de promesses. Les informations fiscales (page Investir) sont datées et accompagnées d'un avertissement : les revérifier à chaque loi de finances.
- Coordonnées : téléphone et e-mail encore « à compléter ». Formulaires en mode démonstration (aucun envoi) : ne jamais afficher qu'un message a été envoyé tant qu'un envoi réel n'est pas branché.
