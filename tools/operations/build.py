"""Génère les pages des opérations du site URBAIN V.

Entrées (à éditer) :
  tools/operations/operations.json          fiche de chaque opération, dans l'ordre d'affichage
  tools/operations/contenu/<slug>.html      présentation de chaque opération (HTML)

Sorties (à ne pas modifier à la main) :
  operations/<slug>/index.html              une page par opération
  operations/index.html                     bloc « En projet »
                                            (entre <!-- operations:debut --> et <!-- operations:fin -->)
  sitemap.xml                               entrées /operations/<slug>/

L'en-tête, le pied de page, le sprite et les versions de site.css / site.js sont
repris de index.html : modifier d'abord l'accueil, puis relancer ce script.

Usage (depuis la racine du dépôt) : python3 tools/operations/build.py
"""
import datetime
import html
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'tools', 'operations')
OUT = os.path.join(ROOT, 'operations')
SITE = 'https://urbain-v.fr'
OG_IMAGE = SITE + '/assets/img/og-urbain-v.jpg'
MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août',
        'septembre', 'octobre', 'novembre', 'décembre']
NOMBRES = ['Aucune', 'Une', 'Deux', 'Trois', 'Quatre', 'Cinq', 'Six', 'Sept', 'Huit', 'Neuf', 'Dix']


def lire(*chemin):
    with open(os.path.join(*chemin), encoding='utf-8') as f:
        return f.read()


def ecrire(chemin, texte):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(texte)


def attr(texte):
    """Texte pour un attribut HTML."""
    return html.escape(texte, quote=True)


def visible(texte):
    """Texte visible : échappement, « 1er » et siècles (XVIIIe) en exposant."""
    texte = html.escape(texte, quote=False)
    texte = re.sub(r'\b1er\b', '1<sup>er</sup>', texte)
    return re.sub(r'\b(X{1,2}(?:IX|IV|V?I{0,3}))e\b', r'\1<sup>e</sup>', texte)


def date_fr(iso):
    d = datetime.date.fromisoformat(iso)
    jour = '1er' if d.day == 1 else str(d.day)
    return f'{jour} {MOIS[d.month - 1]} {d.year}'


def jsonld(objet):
    return json.dumps(objet, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def faits(lignes, retrait):
    return '\n'.join(f'{retrait}<div><dt>{visible(nom)}</dt><dd>{visible(valeur)}</dd></div>' for nom, valeur in lignes)


# --- Données -----------------------------------------------------------------

donnees = json.loads(lire(SRC, 'operations.json'))
operations = donnees['operations']
champs = ('slug', 'nom', 'ville', 'departement', 'code_postal', 'lieu', 'etiquette', 'regime', 'logements',
          'titre', 'titre_seo', 'description', 'chapo', 'carte', 'resume', 'fiche', 'sources', 'liens', 'maj')
erreurs = []
slugs = set()
for o in operations:
    for c in champs:
        if c not in o:
            erreurs.append(f"{o.get('slug', '?')} : champ manquant « {c} »")
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', o.get('slug', '')):
        erreurs.append(f"slug invalide : {o.get('slug')}")
    if o.get('slug') in slugs:
        erreurs.append(f"slug en double : {o.get('slug')}")
    slugs.add(o.get('slug'))
    if not os.path.isfile(os.path.join(SRC, 'contenu', o.get('slug', '') + '.html')):
        erreurs.append(f"{o.get('slug')} : contenu/{o.get('slug')}.html introuvable")
if erreurs:
    print('\n'.join(erreurs))
    sys.exit(1)

# --- Gabarit commun, repris de l'accueil -------------------------------------------

accueil = lire(ROOT, 'index.html')
sprite = re.search(r'<svg class="sprite".*?</svg>', accueil, re.S).group(0)
entete = re.search(r'<header class="site-header".*?</header>', accueil, re.S).group(0)
pied = re.search(r'<footer class="site-footer">.*?</footer>', accueil, re.S).group(0)
css = re.search(r'/assets/css/site\.css\?v=[^"]+', accueil).group(0)
js = re.search(r'/assets/js/site\.js\?v=[^"]+', accueil).group(0)

PAGE = '''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#2B363F">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="URBAIN V">
<meta property="og:title" content="{titre}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="Actualités · URBAIN V" href="/actualites/flux.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&amp;family=Jost:wght@300;400;500;600&amp;family=Roboto+Slab:wght@400;500&amp;display=swap">
<link rel="stylesheet" href="{css}">
<script type="application/ld+json">{jsonld}</script>
</head>
<body data-page="operations">
{sprite}

<button class="skip" type="button" data-skip>Aller au contenu</button>

{entete}

<main id="main" tabindex="-1">
{main}
</main>

{pied}

<script src="{js}" defer></script>
</body>
</html>
'''


def fil(*etapes):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': nom, 'item': lien} for i, (nom, lien) in enumerate(etapes)]}


# --- Pages des opérations ----------------------------------------------------------

for nom in os.listdir(OUT):
    chemin = os.path.join(OUT, nom)
    if os.path.isdir(chemin) and nom not in slugs:
        shutil.rmtree(chemin)  # opération retirée de operations.json

for o in operations:
    url = f'{SITE}/operations/{o["slug"]}/'
    corps = lire(SRC, 'contenu', o['slug'] + '.html').strip()
    sources = '\n'.join(
        f'            <li><a href="{attr(s["url"])}" target="_blank" rel="noopener">{visible(s["titre"])}</a>'
        f'<span> · {visible(s["editeur"])}</span></li>' for s in o['sources'])
    liens = '\n'.join(f'            <li><a href="{attr(l["url"])}">{visible(l["titre"])}</a></li>' for l in o['liens'])
    autres = ''.join(f'<a href="/operations/{a["slug"]}/"><small>Autre opération · {visible(a["ville"])}</small>'
                     f'{visible(a["nom"])}</a>' for a in operations if a is not o)
    main = f'''  <section class="page-hero band-night article-hero">
    <div class="wrap">
      <nav class="crumbs" aria-label="Fil d’Ariane"><a href="/">Accueil</a><span aria-hidden="true">/</span><a href="/operations/">Opérations</a><span aria-hidden="true">/</span><span>{visible(o["nom"])}</span></nav>
      <h1><span class="eyebrow">Opération en projet · {visible(o["lieu"])}</span>{visible(o["titre"])}</h1>
      <p class="lede">{visible(o["chapo"])}</p>
      <p class="article-dates">{visible(o["regime"])} · {o["logements"]} appartements</p>
    </div>
    <svg class="watermark" viewBox="0 0 64.45 64.45" aria-hidden="true"><use href="#embleme"/></svg>
  </section>

  <section class="band">
    <div class="wrap article">
      <article class="article-body">
{corps}
        <div class="article-sources">
          <h2>Sources</h2>
          <ul>
{sources}
          </ul>
        </div>
        <p class="article-note">Informations indicatives sur une opération en projet, à jour au {visible(date_fr(o["maj"]))}, susceptibles d’évoluer et non contractuelles&nbsp;; elles ne constituent pas une offre de vente. Les avantages fiscaux sont soumis à conditions et dépendent de la situation de chaque investisseur&nbsp;: ces informations ne constituent ni un conseil fiscal ni un conseil en investissement.</p>
        <nav class="article-nav" aria-label="Autres opérations">{autres}<a class="link-arrow" href="/operations/#en-projet">Toutes nos opérations</a></nav>
      </article>
      <aside class="article-aside op-aside" aria-labelledby="en-bref">
        <h2 id="en-bref">L’opération en bref</h2>
        <dl class="op-facts">
{faits(o["fiche"], "          ")}
        </dl>
        <a class="btn btn-solid" href="/operations/#avant-premiere">Recevoir la présentation</a>
        <div class="article-links">
          <p class="article-links-title">Pour aller plus loin</p>
          <ul>
{liens}
          </ul>
        </div>
      </aside>
    </div>
  </section>'''
    donnees_structurees = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': o['titre_seo'], 'description': o['description'],
         'inLanguage': 'fr-FR', 'isPartOf': {'@id': SITE + '/#site'}, 'about': {'@id': url + '#operation'},
         'publisher': {'@id': SITE + '/#organisation'}},
        {'@type': 'ApartmentComplex', '@id': url + '#operation', 'name': o['nom'], 'url': url,
         'description': o['description'],
         'numberOfAccommodationUnits': {'@type': 'QuantitativeValue', 'value': o['logements']},
         'address': {'@type': 'PostalAddress', 'addressLocality': o['ville'], 'postalCode': o['code_postal'],
                     'addressRegion': o['departement'], 'addressCountry': 'FR'}},
        fil(('Accueil', SITE + '/'), ('Opérations', SITE + '/operations/'), (o['nom'], url))]}
    ecrire(os.path.join(OUT, o['slug'], 'index.html'),
           PAGE.format(titre=attr(o['titre_seo']), description=attr(o['description']), url=url, og_image=OG_IMAGE,
                       css=css, js=js, jsonld=jsonld(donnees_structurees), sprite=sprite, entete=entete,
                       pied=pied, main=main))

# --- Bloc « En projet » de la page Opérations ------------------------------------------

page_ops = lire(OUT, 'index.html')
debut, fin = '<!-- operations:debut -->', '<!-- operations:fin -->'
if debut not in page_ops or fin not in page_ops:
    print('operations/index.html : repères <!-- operations:debut --> / <!-- operations:fin --> introuvables')
    sys.exit(1)
cartes = '\n'.join(f'''        <li class="op-card">
          <p class="op-meta"><span class="op-tag">{visible(o["etiquette"])}</span><span>{visible(o["lieu"])}</span></p>
          <h3><a href="/operations/{o["slug"]}/">{visible(o["nom"])}</a></h3>
          <p>{visible(o["carte"])}</p>
          <dl class="op-facts">
{faits(o["resume"], "            ")}
          </dl>
          <a class="link-arrow" href="/operations/{o["slug"]}/" aria-label="{attr("Découvrir l’opération : " + o["nom"])}">Découvrir l’opération</a>
        </li>''' for o in operations)
liste = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Opérations en projet · URBAIN V',
         'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': f'{SITE}/operations/{o["slug"]}/',
                              'name': f'{o["nom"]}, {o["ville"]}'} for i, o in enumerate(operations)]}
n = len(operations)
titre_bloc = f'{NOMBRES[n] if n < len(NOMBRES) else n} adresse{"s" if n > 1 else ""} en préparation.'
bloc = f'''{debut}
  <section class="band band-paper2" id="en-projet" data-anchor="en-projet">
    <div class="wrap">
      <div class="sec-head"><p class="eyebrow">En projet</p><h2>{titre_bloc}</h2><p class="lede">{visible(donnees["intro"])}</p></div>
      <ul class="op-list">
{cartes}
      </ul>
      <p class="news-foot">Informations indicatives sur des opérations en projet, susceptibles d’évoluer et non contractuelles&nbsp;; elles ne constituent pas une offre de vente.</p>
    </div>
    <script type="application/ld+json">{jsonld(liste)}</script>
  </section>
  {fin}'''
page_ops = re.sub(re.escape(debut) + r'.*?' + re.escape(fin), lambda m: bloc, page_ops, flags=re.S)
ecrire(os.path.join(OUT, 'index.html'), page_ops)

# --- Sitemap ----------------------------------------------------------------------

plan = lire(ROOT, 'sitemap.xml')
plan = re.sub(r'\n\s*<url><loc>' + re.escape(SITE) + r'/operations/[^<]+/</loc>.*?</url>', '', plan)
derniere = max(o['maj'] for o in operations)
plan = re.sub(r'(<url><loc>' + re.escape(SITE) + r'/operations/</loc><lastmod>)[^<]*(</lastmod></url>)',
              lambda m: m.group(1) + max(derniere, re.search(r'/operations/</loc><lastmod>([^<]*)', plan).group(1)) + m.group(2),
              plan)
entrees = ''.join(f'\n  <url><loc>{SITE}/operations/{o["slug"]}/</loc><lastmod>{o["maj"]}</lastmod></url>'
                  for o in operations)
plan = re.sub(r'(<url><loc>' + re.escape(SITE) + r'/operations/</loc>.*?</url>)', lambda m: m.group(1) + entrees, plan)
ecrire(os.path.join(ROOT, 'sitemap.xml'), plan)

print(f'Opérations : {n} pages, bloc « En projet » et sitemap générés.')
