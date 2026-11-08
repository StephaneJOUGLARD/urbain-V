# URBAIN V — site internet

Site vitrine d'URBAIN V, rénovation immobilière de prestige à Grenoble : <https://urbain-v.fr>

*Restaurer · Sublimer · Transmettre*

## Fonctionnement

- Site statique : pages HTML, une feuille de style et un script communs, sans base de données ni CMS.
- Hébergement web OVH relié à ce dépôt (intégration Git) : chaque modification publiée sur la branche `main` est déployée automatiquement sur urbain-v.fr grâce au webhook GitHub.
- Certificat SSL Let's Encrypt de l'hébergement OVH : les adresses en `http://` et en `www.` sont redirigées vers `https://urbain-v.fr` (`.htaccess`).
- Les évolutions se demandent à Claude dans une session reliée à ce dépôt : Claude modifie les fichiers, contrôle le site, puis publie sur `main`.

## Pages

| Page | Adresse | Fichier |
| --- | --- | --- |
| Accueil | `/` | `index.html` |
| La Maison | `/la-maison/` | `la-maison/index.html` |
| Savoir-faire | `/savoir-faire/` | `savoir-faire/index.html` |
| Investir | `/investir/` | `investir/index.html` |
| Opérations | `/operations/` | `operations/index.html` |
| Contact | `/contact/` | `contact/index.html` |
| Mentions légales | `/mentions-legales/` | `mentions-legales/index.html` |
| Page introuvable | — | `404.html` |

Ressources communes : `assets/css/site.css`, `assets/js/site.js`, photos dans `assets/img/`, logo dans `assets/img/logo/`.
Documents à télécharger : `documents/` (plaquette de présentation, guide de la fiscalité 2026), avec leurs sources dans `tools/documents/`.
Référencement : `sitemap.xml`, `robots.txt`, titres et descriptions propres à chaque page.

## À compléter avant la mise en ligne

- Créer la boîte contact@urbain-v.fr dans l'espace client OVH ; elle recevra les messages une fois le domaine basculé sur les serveurs DNS d'OVH.
- Formulaires : ils affichent pour l'instant un message de démonstration ; ils pourront envoyer un e-mail à contact@urbain-v.fr via l'hébergement OVH.

## Photographies

Photographies d'illustration publiées sur Unsplash (licence Unsplash). Elles ne représentent pas des réalisations d'URBAIN V et seront remplacées par les photos des opérations.
