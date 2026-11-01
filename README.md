# URBAIN V — site internet

Site vitrine d'URBAIN V, rénovation immobilière de prestige à Grenoble : <https://urbain-v.fr>

*Restaurer · Sublimer · Transmettre*

## Fonctionnement

- Site statique : pages HTML, une feuille de style et un script communs, sans base de données ni CMS.
- Hébergement web OVH relié à ce dépôt (intégration Git) : chaque modification publiée sur la branche `main` est déployée automatiquement sur urbain-v.fr grâce au webhook GitHub.
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
Référencement : `sitemap.xml`, `robots.txt`, titres et descriptions propres à chaque page.

## À compléter avant la mise en ligne

- Téléphone et e-mail de contact (page Contact).
- Mentions légales : forme sociale, capital, SIREN, directeur de la publication, hébergeur, e-mail pour les données personnelles.
- Formulaires : ils affichent pour l'instant un message de démonstration ; ils pourront envoyer un e-mail via l'hébergement OVH une fois l'adresse de réception choisie.
- Après activation du certificat SSL : activer la redirection HTTPS dans `.htaccess`.

## Photographies

Photographies d'illustration publiées sur Unsplash (licence Unsplash). Elles ne représentent pas des réalisations d'URBAIN V et seront remplacées par les photos des opérations.
