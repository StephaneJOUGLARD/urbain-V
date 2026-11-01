"""Contrôle du site URBAIN V avant chaque publication.

Vérifie que :
- l'en-tête, le pied de page et le sprite du logo sont identiques sur toutes les pages ;
- chaque lien interne et chaque ressource (/...) pointe vers un fichier existant ;
- chaque page a un titre, une description et une URL canonique ;
- le sitemap liste toutes les pages publiques.

Usage (depuis la racine du dépôt) : python3 tools/verifier.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages = ['index.html', '404.html'] + sorted(
    os.path.join(d, 'index.html') for d in os.listdir(ROOT)
    if os.path.isfile(os.path.join(ROOT, d, 'index.html')) and not d.startswith('.'))
errors = []
blocks = {}

for page in pages:
    html = open(os.path.join(ROOT, page), encoding='utf-8').read()
    for name, pat in (('en-tête', r'<header class="site-header".*?</header>'),
                      ('pied de page', r'<footer class="site-footer">.*?</footer>'),
                      ('sprite', r'<svg class="sprite".*?</svg>')):
        m = re.search(pat, html, re.S)
        if not m:
            errors.append(f'{page} : {name} introuvable')
        else:
            blocks.setdefault(name, {}).setdefault(m.group(0), []).append(page)
    for tag in ('<title>', '<meta name="description"', '<link rel="canonical"'):
        if tag not in html:
            errors.append(f'{page} : balise manquante {tag}')
    for url in re.findall(r'(?:href|src)="(/[^"]*)"', html):
        path = url.split('#')[0].split('?')[0]
        target = os.path.join(ROOT, path.lstrip('/'))
        if path.endswith('/'):
            target = os.path.join(target, 'index.html')
        if not os.path.isfile(target):
            errors.append(f'{page} : lien cassé {url}')

for name, variants in blocks.items():
    if len(variants) > 1:
        groups = ' | '.join(', '.join(p) for p in variants.values())
        errors.append(f'{name} différent selon les pages : {groups}')

sitemap = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
for page in pages:
    if page == '404.html':
        continue
    loc = 'https://urbain-v.fr/' + page.replace('index.html', '')
    if f'<loc>{loc}</loc>' not in sitemap:
        errors.append(f'sitemap.xml : {loc} absent')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'OK : {len(pages)} pages contrôlées, aucun problème.')
