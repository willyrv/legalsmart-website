# Site vitrine Legal Smart — Choix techniques

*Octobre 2026. Les offres d'hébergement et leurs tarifs sont à revérifier au moment de la mise en ligne.*

## 1. Ce qu'on attend du site

| Besoin | Conséquence |
|---|---|
| Présenter l'offre, la méthode, les tarifs et le fondateur ; convertir vers l'atelier découverte | Peu de pages, un appel à l'action clair sur chacune |
| Publier régulièrement (reprise des posts LinkedIn, articles de fond) | Rubrique « Ressources » alimentée en Markdown, flux RSS |
| **Facile à maintenir par une seule personne**, sans être développeur web | Textes et tarifs séparés de la mise en page ; aucune dépendance à mettre à jour |
| **Cohérent avec le discours** : confidentialité, souveraineté, sobriété | Aucun cookie, aucun traceur, aucune ressource externe ; hébergement en France |
| Rapide, accessible, bien référencé | Pages statiques, HTML sémantique, sitemap, métadonnées de partage |
| Coût minimal | Hébergement statique : quelques euros par mois, voire gratuit |

Un site statique répond à tout cela. Il n'y a rien à pirater côté serveur, rien à mettre à jour en urgence, et il peut être hébergé partout.

## 2. Quel générateur ?

| Option | Points forts | Points faibles | Verdict |
|---|---|---|---|
| **Hugo** | Un seul exécutable : **aucune dépendance** (pas de `node_modules`), construction en moins d'une seconde, Markdown + fichiers de données YAML, sitemap, RSS et traitement d'images intégrés, très stable dans le temps | Les gabarits (syntaxe Go) sont moins agréables à écrire, mais on y touche rarement | **Retenu** |
| Astro | Le plus moderne, composants, excellente expérience de développement | Chaîne Node à maintenir, versions majeures fréquentes avec migrations, Node récent requis | Excellent pour un site plus interactif ; sur-dimensionné ici |
| Eleventy (11ty) | Simple, gabarits proches de Jinja | Dépend de Node et de paquets npm à suivre | Bonne alternative |
| Jekyll | Historique de GitHub Pages | Écosystème Ruby vieillissant | Écarté |
| Pelican, MkDocs (Python) | Langage familier | Pelican vise le blog, MkDocs la documentation : peu adaptés à une vitrine commerciale | Écartés |
| HTML écrit à la main | Zéro outil | En-tête, pied de page et menus à dupliquer sur chaque page ; pas de blog | Écarté |
| WordPress, Wix, Squarespace | Édition visuelle | WordPress : mises à jour de sécurité et extensions à surveiller. Wix et Squarespace : hébergement hors UE, cookies, dépendance à l'éditeur | Contradictoires avec le discours Legal Smart |

**Ce qui rend Hugo « facile à maintenir » ici :**

- **Les textes** sont en Markdown dans `content/`.
- **Les données qui changent** sont dans `data/` :
  - `offres.yaml` : tarifs ;
  - `etapes.yaml` : méthode ;
  - `enjeux.yaml` et `solutions.yaml` : blocs de la page d'accueil.
- **Les coordonnées** sont regroupées dans `hugo.toml`.
- **La version de Hugo est épinglée** (`.hugo-version` et intégration continue) : le site se construit de la même façon dans cinq ans.
- **Aucune chaîne CSS** (Sass, Tailwind…) : un seul fichier `assets/css/main.css`, minifié et versionné par Hugo.
- **Presque aucun JavaScript**, menu mobile compris. Seule exception : quelques lignes, écrites dans la page, qui affichent le numéro de téléphone au clic (`layouts/_partials/tel-script.html`). Le numéro n'est pas en clair dans les pages, pour le protéger des robots qui collectent les numéros. Il n'est pas non plus dans les données structurées pour Google. Sans JavaScript, le bouton reste masqué et le reste du site fonctionne.

**Option d'édition sans code :** un CMS « Git » léger peut se brancher plus tard, par exemple [Pages CMS](https://pagescms.org) ou Decap CMS. Il offre un formulaire web pour modifier textes et tarifs, qui enregistre directement dans le dépôt GitHub. Il n'est pas nécessaire au démarrage.

## 3. Confidentialité et conformité du site

- **Aucun cookie, aucun traceur.** Il n'y a donc pas de bandeau de consentement à afficher : c'est en soi un message envoyé aux prospects.
- **Polices système**, sans Google Fonts : rien n'est chargé depuis un tiers, donc aucune adresse IP de visiteur ne leur est transmise.
- **Pas de formulaire hébergé chez un tiers** : contact par e-mail, téléphone et LinkedIn. Un lien de prise de rendez-vous peut être ajouté dans `hugo.toml` (paramètre `booking_url`). Choisir alors un outil européen ou auto-hébergé, par exemple Cal.com en auto-hébergement.
- **Mesure d'audience** (facultative, plus tard) : Matomo ou Umami auto-hébergés, configurés sans cookie selon les conditions d'exemption de la CNIL.
- **Pages obligatoires** : mentions légales (LCEN) et politique de confidentialité sont fournies. Les informations manquantes (SIRET, adresse, hébergeur) sont signalées par un avertissement à chaque construction tant qu'elles ne sont pas renseignées.

## 4. Hébergement

Le site est un dossier de fichiers (`public/`). Tout hébergeur convient. Pour rester cohérent avec le discours « souveraineté », on privilégie un acteur français :

| Option | Mise en ligne | Pour |
|---|---|---|
| **OVHcloud — hébergement web** | `rsync`/SFTP depuis GitHub Actions (workflow fourni) | Le plus simple ; certificat TLS inclus ; nom de domaine au même endroit |
| Scaleway — Object Storage + Edge Services | `aws s3 sync` (API compatible S3) | Très bon marché, certificat via Edge Services |
| alwaysdata, Clever Cloud | SSH/rsync ou Git | Hébergeurs français simples |
| GitHub Pages, Netlify, Cloudflare Pages | Automatique | Gratuits et pratiques, mais hébergés par des sociétés américaines : moins cohérent avec le message |

Le workflow `.github/workflows/deploy.yml` fonctionne ainsi :

- **à chaque push** sur `main`, il construit le site avec la version épinglée de Hugo et vérifie les liens internes ;
- **la publication par rsync** sur l'hébergeur ne s'active que lorsque ses secrets sont configurés (`DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_PATH`, `DEPLOY_SSH_KEY`).

**Choix actuel (octobre 2026) :** une première version est publiée sur Cloudflare Pages, à l'adresse `legalsmart.willyrv.com`, car le DNS de `willyrv.com` est déjà chez Cloudflare. C'est gratuit et immédiat. Cette version de prévisualisation n'est pas indexée par les moteurs de recherche. Le choix d'un hébergeur français reste ouvert pour le site définitif sur `legalsmart.ai`. Le mode d'emploi est dans le README, section « Mettre en ligne ».

## 5. Choix éditoriaux

- **Contenus repris des livrables validés** : plaquette commerciale finale (enjeux, solutions, méthode, tarifs, biographie), plan LinkedIn (articles), note de cohérence (formulations prudentes).
- **Aucune promesse chiffrée non mesurée** (« les gains de temps sont mesurés pendant le prototype »), aucune promesse de « conformité garantie ».
- **Le mot « RAG » est toujours expliqué.** Le jargon est évité, comme le recommandait le coaching.
- **Un appel à l'action unique**, l'atelier découverte offert, sur chaque page.
- **Visuels** : compositions graphiques originales (motif d'arches de la charte) et une illustration fidèle de l'assistant, avec un document fictif. Pas de photographies de banque d'images.
