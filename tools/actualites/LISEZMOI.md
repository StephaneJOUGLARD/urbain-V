# Rubrique Actualités — mode d’emploi

La rubrique `/actualites/` recense les actualités juridiques et techniques sur la rénovation et la
réhabilitation des logements anciens (fiscalité, DPE, aides, copropriété, urbanisme, normes).
Elle est **générée** : ne jamais modifier à la main `actualites/`, `llms.txt`, le bloc « Actualités »
de l’accueil ni les entrées `/actualites/` du sitemap.

## Fichiers

- `articles.json` : une entrée par actualité (titre, dates, rubrique, chapô, points « À retenir »,
  mots-clés, sources, liens internes). L’ordre d’affichage suit `date_tri` (la plus récente d’abord).
- `contenu/<slug>.html` : le corps de l’actualité, en HTML simple (`<h2>`, `<p>`, `<ul>`), avec
  les espaces insécables de la typographie française (`&nbsp;` avant `:` `;` `?` `!` `%` `€`).
- `llms-modele.md` : modèle de `/llms.txt` (résumé du site destiné aux assistants IA).
- `build.py` : génère les pages, le flux RSS `actualites/flux.xml`, le bloc de l’accueil, le sitemap
  et `llms.txt`. L’en-tête, le pied de page et les versions CSS/JS sont repris de `index.html`.

## Ajouter ou mettre à jour une actualité

1. Rechercher l’actualité et la **vérifier sur une source officielle ou primaire** : Légifrance,
   ministères (ecologie.gouv.fr, economie.gouv.fr), service-public.fr, impots.gouv.fr, ANIL, ADEME,
   Anah / France Rénov’, Banque des Territoires, Assemblée nationale, Sénat. Un article de presse
   seul ne suffit pas pour un chiffre ou une date.
2. Écrire l’entrée dans `articles.json` et le corps dans `contenu/<slug>.html` :
   - slug en minuscules, sans accents, avec le mot-clé principal (ex. `loi-jeanbrun-2026-…`) ;
   - `titre` ≤ 110 caractères, `titre_seo` ≤ 75 caractères environ, `description` ≤ 165 caractères ;
   - au moins une source avec son URL, son éditeur et sa date ;
   - `publie_le` = date de mise en ligne, `mis_a_jour_le` = date de la dernière vérification.
3. Lancer `python3 tools/actualites/build.py`, puis `python3 tools/verifier.py`.
4. Contrôler le rendu (liste, article, accueil ; bureau et mobile ; thème clair et sombre).
5. Publier sur `main`.

## Règles de contenu

- Ne rien inventer : chaque chiffre, date ou condition doit figurer dans une source citée.
- Un texte en cours d’examen (projet ou proposition de loi, projet de loi de finances) est présenté
  comme tel (« en cours d’examen », « pourrait ») ; mettre l’actualité à jour après son adoption.
- Quand une règle évolue, mettre à jour l’actualité concernée (et `mis_a_jour_le`) plutôt que de
  laisser une information périmée ; vérifier aussi la page Investir et le guide de la fiscalité.
- Ton : informatif, sobre, sans promesse. Rappeler que l’éligibilité d’une opération dépend du
  bien et des travaux, sans affirmer qu’une opération URBAIN V sera éligible à un dispositif.
- Ne pas parler de Novelia ni de CGBI ; ne pas trop mettre Grenoble en avant.
- Mots-clés à intégrer naturellement lorsqu’ils sont pertinents (volumes Google France, nov. 2026) :
  rénovation énergétique, investissement locatif, déficit foncier, loi Jeanbrun, loi Denormandie,
  loi Malraux, défiscalisation immobilière, DPE, MaPrimeRénov’, immeuble ancien, appartement ancien rénové.
- Rythme : une à deux actualités par mois, en retirant au besoin les plus anciennes devenues sans
  objet (une actualité retirée de `articles.json` est supprimée du site par `build.py`).
