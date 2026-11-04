# Documents imprimables : plaquette et guide de la fiscalité

Sources des PDF publiés dans `/documents/` (versions allégées pour le web). Les versions d'impression, avec les images en pleine définition, sont rangées dans le Drive « URBAIN V ». Ce dossier n'est pas accessible en ligne : `.htaccess` bloque `tools/`.

## Fichiers

- `plaquette.html`, `guide.html` : gabarits A4, une `<section class="page">` par page. Les styles propres à chaque document sont dans leur balise `<style>`.
- `print.css` : charte commune (couleurs, polices, planches, folios, carte, échelle DPE).
- `render.js` : insère les planches (`{{plate:…}}`) et la carte (`{{map}}`), puis imprime le PDF avec Chromium (Playwright). Il signale les éléments qui débordent de leur page.
- `plates/` : dessins des planches, extraits du site par `extract_plates.js` (à relancer si `assets/js/site.js` change).
- `make_map.py` : carte du Dauphiné et du grand quart sud-est (départements, projection conique conforme de Lambert).
- `cover_gradient.py` : intègre le dégradé des couvertures dans la photo elle-même. Le haut de l'image reste intact, puis la photo se fond dans le vert #2A7350 et l'anthracite #2B363F. Aucun effet de transparence dans le PDF, pour un rendu identique dans tous les lecteurs.
- `images.txt` : nom de fichier → identifiant Unsplash de chaque photo.

## Régénérer les PDF

1. Copier ce dossier dans un dossier de travail, puis y installer les polices : `npm install @fontsource/eb-garamond @fontsource/roboto-slab @fontsource/jost` (Playwright est déjà installé dans l'environnement).
2. Photos : pour chaque ligne de `images.txt`, télécharger `https://images.unsplash.com/<identifiant>?w=1600&q=80&fm=jpg&fit=max` vers `img/<nom>.jpg` (largeur 2400 pour `hero`, `facade-blanche`, `haussmann-arbres` et `balcons-ferronnerie`).
3. Couvertures (photos sources : `hero` en 2800 px de large, `facade-blanche` en 3600 px, dans `img-hi/`) :
   - plaquette : `python3 cover_gradient.py img-hi/hero.jpg img/hero-cover.jpg '{"size":[2480,3508],"position":[0.5,0.35],"blend":[[0,0],[0.44,0],[0.62,0.86],[0.74,0.92],[0.86,1],[1,1]],"desat":[[0,0],[0.44,0],[0.58,1],[1,1]],"color":[[0,"green"],[0.74,"green"],[0.86,"anthracite"],[1,"anthracite"]]}'`
   - guide : `python3 cover_gradient.py img-hi/facade-blanche.jpg img/facade-blanche-cover.jpg '{"size":[2480,2079],"position":[0.5,0.42],"blend":[[0,0],[0.42,0],[0.70,0.86],[1,1]],"desat":[[0,0],[0.42,0],[0.62,1],[1,1]],"color":[[0,"green"],[1,"green"]]}'`
4. Carte : télécharger `departements-version-simplifiee.geojson` (dépôt GitHub gregoiredavid/france-geojson) dans `geo/`, puis `python3 make_map.py geo/departements-version-simplifiee.geojson build/map.svg.html`.
5. Impression : `node render.js plaquette build/plaquette.pdf` et `node render.js guide build/guide.pdf`.
6. Version web : réduire les photos dans `img-web/` (1500 px au plus, couvertures en 1240 px de large, JPEG qualité 80), remplacer `src="img/` par `src="img-web/` dans une copie des gabarits, imprimer, puis copier les PDF vers `/documents/` sous les mêmes noms.
7. Vignettes : page 1 de chaque PDF en 400 × 566 px, au format WebP, dans `assets/img/docs/`.
8. Sur le site : incrémenter `?v=` des liens de téléchargement (pages La Maison et Investir) et mettre à jour le poids indiqué.

## Contenu

- Mêmes règles que le site (voir `CLAUDE.md`) : Novelia n'apparaît que dans la phrase sur l'origine et dans les mentions légales ; les photos sont des illustrations ; aucun chiffre ni aucune promesse inventés.
- Le guide de la fiscalité est daté (informations à jour au 1er novembre 2026) : le revérifier à chaque loi de finances, comme la page Investir.
- L'éditorial de la plaquette est signé Stéphane Jouglard.
