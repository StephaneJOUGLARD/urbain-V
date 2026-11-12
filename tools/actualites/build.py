"""Génère la rubrique Actualités du site URBAIN V.

Entrées (à éditer) :
  tools/actualites/articles.json            métadonnées de chaque actualité
  tools/actualites/contenu/<slug>.html      corps de chaque actualité (HTML)
  tools/actualites/llms-modele.md           modèle de /llms.txt

Sorties (à ne pas modifier à la main) :
  actualites/index.html                     liste des actualités
  actualites/<slug>/index.html              une page par actualité
  actualites/flux.xml                       flux RSS
  index.html                                bloc « Actualités » de l'accueil
                                            (entre <!-- actualites:debut --> et <!-- actualites:fin -->)
  sitemap.xml                               entrées /actualites/
  llms.txt                                  résumé du site pour les assistants IA

L'en-tête, le pied de page, le sprite et les versions de site.css / site.js sont
repris de index.html : modifier d'abord l'accueil, puis relancer ce script.

Usage (depuis la racine du dépôt) : python3 tools/actualites/build.py
"""
import datetime
import email.utils
import html
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'tools', 'actualites')
SITE = 'https://urbain-v.fr'
OUT = os.path.join(ROOT, 'actualites')
try:
    from zoneinfo import ZoneInfo
    PARIS = ZoneInfo('Europe/Paris')
except Exception:  # pas de base de fuseaux : heure d'hiver par défaut
    PARIS = datetime.timezone(datetime.timedelta(hours=1))
MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août',
        'septembre', 'octobre', 'novembre', 'décembre']
LOGO = SITE + '/assets/img/logo/urbain-v-couleur.png'
OG_IMAGE = SITE + '/assets/img/og-urbain-v.jpg'


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
    """Texte visible : échappement, puis « 1er » en exposant."""
    return re.sub(r'\b1er\b', '1<sup>er</sup>', html.escape(texte, quote=False))


def date_fr(iso):
    d = datetime.date.fromisoformat(iso)
    jour = '1er' if d.day == 1 else str(d.day)
    return f'{jour} {MOIS[d.month - 1]} {d.year}'


def instant(iso):
    d = datetime.date.fromisoformat(iso)
    return datetime.datetime(d.year, d.month, d.day, 8, 0, tzinfo=PARIS)


def jsonld(objet):
    texte = json.dumps(objet, ensure_ascii=False, separators=(',', ':'))
    return texte.replace('</', '<\\/')


# --- Données -----------------------------------------------------------------

donnees = json.loads(lire(SRC, 'articles.json'))
articles = donnees['articles']
champs = ('slug', 'date_tri', 'date_affichee', 'rubrique', 'titre', 'titre_court', 'titre_seo',
          'description', 'chapo', 'a_retenir', 'mots_cles', 'publie_le', 'mis_a_jour_le', 'sources', 'liens')
erreurs = []
slugs = set()
for a in articles:
    for c in champs:
        if c not in a:
            erreurs.append(f"{a.get('slug', '?')} : champ manquant « {c} »")
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', a.get('slug', '')):
        erreurs.append(f"slug invalide : {a.get('slug')}")
    if a.get('slug') in slugs:
        erreurs.append(f"slug en double : {a.get('slug')}")
    slugs.add(a.get('slug'))
    if not os.path.isfile(os.path.join(SRC, 'contenu', a.get('slug', '') + '.html')):
        erreurs.append(f"{a.get('slug')} : contenu/{a.get('slug')}.html introuvable")
    if not a.get('sources'):
        erreurs.append(f"{a.get('slug')} : aucune source")
    if len(a.get('titre', '')) > 110:
        erreurs.append(f"{a.get('slug')} : titre trop long pour les données structurées (110 caractères max.)")
if erreurs:
    print('\n'.join(erreurs))
    sys.exit(1)

# Plus récente d'abord ; à date égale, l'ordre du fichier.
articles = [a for _, a in sorted(enumerate(articles), key=lambda p: (p[1]['date_tri'], -p[0]), reverse=True)]

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
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="URBAIN V">
<meta property="og:title" content="{titre}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">{meta_article}
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
<body data-page="actualites">
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

CTA = '''  <section class="band band-night">
    <div class="wrap cta-grid">
      <div class="stack-lg"><p class="eyebrow">Nos opérations</p><h2>Nos premières adresses.</h2><p class="lede">Découvrez nos opérations en projet et recevez en priorité leur présentation complète&nbsp;: histoire du lieu, plans, prestations, prix et calendrier.</p></div>
      <div class="cta-actions"><a class="btn btn-solid" href="/operations/#en-projet">Découvrir nos opérations</a></div>
    </div>
  </section>'''


def page(titre, description, url, main, donnees_structurees, og_type='website', meta_article=''):
    return PAGE.format(titre=attr(titre), description=attr(description), url=url, og_type=og_type,
                       og_image=OG_IMAGE, meta_article=meta_article, css=css, js=js,
                       jsonld=jsonld(donnees_structurees), sprite=sprite, entete=entete, pied=pied, main=main)


def element_liste(a, niveau):
    url = f'/actualites/{a["slug"]}/'
    return (f'<li class="news-item">'
            f'<p class="news-meta"><span class="news-tag">{visible(a["rubrique"])}</span><span>{visible(a["date_affichee"])}</span></p>'
            f'<div class="news-body"><{niveau}><a href="{url}">{visible(a["titre"])}</a></{niveau}>'
            f'<p>{visible(a["description"])}</p>'
            f'<a class="link-arrow" href="{url}" aria-label="{attr("Lire l’actualité : " + a["titre"])}">Lire l’actualité</a></div></li>')


def fil(*etapes):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': nom, 'item': lien} for i, (nom, lien) in enumerate(etapes)]}


# --- Pages des actualités ----------------------------------------------------------

if os.path.isdir(OUT):
    for nom in os.listdir(OUT):
        chemin = os.path.join(OUT, nom)
        if os.path.isdir(chemin) and nom not in slugs:
            shutil.rmtree(chemin)  # actualité retirée de articles.json

for i, a in enumerate(articles):
    url = f'{SITE}/actualites/{a["slug"]}/'
    corps = lire(SRC, 'contenu', a['slug'] + '.html').strip()
    publie, maj = date_fr(a['publie_le']), date_fr(a['mis_a_jour_le'])
    dates = f'Publié le {publie}' + (f' · mis à jour le {maj}' if a['mis_a_jour_le'] != a['publie_le'] else '')
    sources = '\n'.join(
        f'            <li><a href="{attr(s["url"])}" target="_blank" rel="noopener">{visible(s["titre"])}</a>'
        f'<span> · {visible(s["editeur"])}{(", " + visible(s["date"])) if s.get("date") else ""}</span></li>'
        for s in a['sources'])
    retenir = '\n'.join(f'          <li>{visible(t)}</li>' for t in a['a_retenir'])
    liens = '\n'.join(f'            <li><a href="{attr(l["url"])}">{visible(l["titre"])}</a></li>' for l in a['liens'])
    voisins = []
    if i > 0:
        p = articles[i - 1]
        voisins.append(f'<a href="/actualites/{p["slug"]}/"><small>Actualité plus récente</small>{visible(p["titre"])}</a>')
    if i < len(articles) - 1:
        s = articles[i + 1]
        voisins.append(f'<a href="/actualites/{s["slug"]}/"><small>Actualité précédente</small>{visible(s["titre"])}</a>')
    voisins.append('<a class="link-arrow" href="/actualites/">Toutes les actualités</a>')
    main = f'''  <section class="page-hero band-night article-hero">
    <div class="wrap">
      <nav class="crumbs" aria-label="Fil d’Ariane"><a href="/">Accueil</a><span aria-hidden="true">/</span><a href="/actualites/">Actualités</a><span aria-hidden="true">/</span><span>{visible(a["titre_court"])}</span></nav>
      <h1><span class="eyebrow">{visible(a["rubrique"])} · {visible(a["date_affichee"])}</span>{visible(a["titre"])}</h1>
      <p class="lede">{visible(a["chapo"])}</p>
      <p class="article-dates">{visible(dates)}</p>
    </div>
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
        <p class="article-note">Information générale à jour au {visible(maj)}, sous réserve de l’évolution des textes et de leur interprétation. Elle ne constitue ni un conseil juridique ou fiscal, ni un conseil en investissement.</p>
        <nav class="article-nav" aria-label="Autres actualités">{"".join(voisins)}</nav>
      </article>
      <aside class="article-aside" aria-labelledby="a-retenir">
        <h2 id="a-retenir">À retenir</h2>
        <ul>
{retenir}
        </ul>
        <div class="article-links">
          <p class="article-links-title">Pour aller plus loin</p>
          <ul>
{liens}
          </ul>
        </div>
      </aside>
    </div>
  </section>

{CTA}'''
    donnees_structurees = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'NewsArticle', '@id': url + '#actualite', 'url': url, 'mainEntityOfPage': url,
         'headline': a['titre'], 'description': a['description'], 'articleSection': a['rubrique'],
         'keywords': ', '.join(a['mots_cles']), 'inLanguage': 'fr-FR',
         'datePublished': instant(a['publie_le']).isoformat(), 'dateModified': instant(a['mis_a_jour_le']).isoformat(),
         'image': [OG_IMAGE],
         'author': {'@type': 'Organization', 'name': 'URBAIN V', 'url': SITE + '/'},
         'publisher': {'@type': 'Organization', 'name': 'URBAIN V', 'url': SITE + '/',
                       'logo': {'@type': 'ImageObject', 'url': LOGO}},
         'citation': [{'@type': 'CreativeWork', 'name': s['titre'], 'url': s['url']} for s in a['sources']]},
        fil(('Accueil', SITE + '/'), ('Actualités', SITE + '/actualites/'), (a['titre_court'], url))]}
    meta_article = (f'\n<meta property="article:published_time" content="{instant(a["publie_le"]).isoformat()}">'
                    f'\n<meta property="article:modified_time" content="{instant(a["mis_a_jour_le"]).isoformat()}">'
                    f'\n<meta property="article:section" content="{attr(a["rubrique"])}">')
    ecrire(os.path.join(OUT, a['slug'], 'index.html'),
           page(a['titre_seo'], a['description'], url, main, donnees_structurees, 'article', meta_article))

# --- Liste des actualités ----------------------------------------------------------

url_liste = SITE + '/actualites/'
description_liste = ('Loi Jeanbrun, déficit foncier, DPE, MaPrimeRénov’, copropriété\u00a0: les actualités juridiques et '
                     'techniques de la rénovation et de la réhabilitation des logements anciens, vérifiées et sourcées.')
elements = '\n'.join('        ' + element_liste(a, 'h2') for a in articles)
main = f'''  <section class="page-hero band-night">
    <div class="wrap">
      <nav class="crumbs" aria-label="Fil d’Ariane"><a href="/">Accueil</a><span aria-hidden="true">/</span><span>Actualités</span></nav>
      <h1><span class="eyebrow">Actualités · Rénovation de l’ancien</span>L’actualité de l’ancien, décryptée.</h1>
      <p class="lede">Fiscalité, performance énergétique, copropriété&nbsp;: les évolutions juridiques et techniques qui comptent pour rénover, acheter ou investir dans un logement ancien. Chaque actualité renvoie à ses sources officielles.</p>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <ul class="news-list">
{elements}
      </ul>
      <p class="news-foot">Informations générales, vérifiées à la date de publication de chaque actualité et sous réserve de l’évolution des textes. Elles ne constituent ni un conseil juridique ou fiscal, ni un conseil en investissement. <a href="/actualites/flux.xml">S’abonner au flux RSS</a></p>
    </div>
  </section>

{CTA}'''
donnees_structurees = {'@context': 'https://schema.org', '@graph': [
    {'@type': 'CollectionPage', '@id': url_liste + '#page', 'url': url_liste, 'name': 'Actualités · URBAIN V',
     'description': description_liste, 'inLanguage': 'fr-FR',
     'mainEntity': {'@type': 'ItemList', 'itemListElement': [
         {'@type': 'ListItem', 'position': i + 1, 'url': f'{SITE}/actualites/{a["slug"]}/', 'name': a['titre']}
         for i, a in enumerate(articles)]}},
    fil(('Accueil', SITE + '/'), ('Actualités', url_liste))]}
ecrire(os.path.join(OUT, 'index.html'),
       page('Actualités de la rénovation dans l’ancien\u00a0: fiscalité, DPE, copropriété · URBAIN V',
            description_liste, url_liste, main, donnees_structurees))

# --- Flux RSS --------------------------------------------------------------------

def x(texte):
    return html.escape(texte, quote=False)


items = '\n'.join(
    f'''  <item>
    <title>{x(a["titre"])}</title>
    <link>{SITE}/actualites/{a["slug"]}/</link>
    <guid isPermaLink="true">{SITE}/actualites/{a["slug"]}/</guid>
    <pubDate>{email.utils.format_datetime(instant(a["publie_le"]))}</pubDate>
    <category>{x(a["rubrique"])}</category>
    <description>{x(a["description"])}</description>
  </item>''' for a in articles)
derniere = max(a['mis_a_jour_le'] for a in articles)
ecrire(os.path.join(OUT, 'flux.xml'), f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>Actualités · URBAIN V</title>
  <link>{SITE}/actualites/</link>
  <atom:link href="{SITE}/actualites/flux.xml" rel="self" type="application/rss+xml"/>
  <description>{x(description_liste)}</description>
  <language>fr-fr</language>
  <lastBuildDate>{email.utils.format_datetime(instant(derniere))}</lastBuildDate>
{items}
</channel>
</rss>
''')

# --- Bloc de l'accueil -----------------------------------------------------------------

debut, fin = '<!-- actualites:debut -->', '<!-- actualites:fin -->'
if debut not in accueil or fin not in accueil:
    print('index.html : repères <!-- actualites:debut --> / <!-- actualites:fin --> introuvables')
    sys.exit(1)
bloc = '\n'.join('        ' + element_liste(a, 'h3') for a in articles[:3])
accueil = re.sub(re.escape(debut) + r'.*?' + re.escape(fin),
                 lambda m: f'{debut}\n      <ul class="news-list">\n{bloc}\n      </ul>\n      {fin}', accueil, flags=re.S)
ecrire(os.path.join(ROOT, 'index.html'), accueil)

# --- Sitemap ----------------------------------------------------------------------

plan = lire(ROOT, 'sitemap.xml')
plan = re.sub(r'\n\s*<url><loc>' + re.escape(SITE) + r'/actualites/[^<]*</loc>.*?</url>', '', plan)
entrees = [f'  <url><loc>{SITE}/actualites/</loc><lastmod>{derniere}</lastmod></url>'] + [
    f'  <url><loc>{SITE}/actualites/{a["slug"]}/</loc><lastmod>{a["mis_a_jour_le"]}</lastmod></url>' for a in articles]
plan = plan.replace('</urlset>', '\n'.join(entrees) + '\n</urlset>')
ecrire(os.path.join(ROOT, 'sitemap.xml'), plan)

# --- llms.txt -------------------------------------------------------------------------

liste_llms = '\n'.join(f'- [{a["titre"]}]({SITE}/actualites/{a["slug"]}/) ({a["date_affichee"]}) : {a["description"]}'
                       for a in articles)
ecrire(os.path.join(ROOT, 'llms.txt'), lire(SRC, 'llms-modele.md').replace('{{ACTUALITES}}', liste_llms))

print(f'Actualités : {len(articles)} pages, liste, flux RSS, bloc d’accueil, sitemap et llms.txt générés.')
