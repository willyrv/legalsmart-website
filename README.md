# Site vitrine Legal Smart

Site statique de présentation de Legal Smart, construit avec [Hugo](https://gohugo.io). Il est :

- **sans cookie, sans traceur, sans ressource externe** ;
- **sans JavaScript**, à une exception : le bouton qui affiche le numéro de téléphone au clic, pour le cacher aux robots ;
- **rapide**, et hébergeable n'importe où.

Les choix techniques sont expliqués dans [docs/CHOIX-TECHNIQUES.md](docs/CHOIX-TECHNIQUES.md).

## Modifier le site : où se trouve quoi

| Je veux modifier… | Fichier |
|---|---|
| E-mail, téléphone, LinkedIn, lien de rendez-vous | `hugo.toml`, section `[params.contact]` |
| Mentions légales (SIRET, adresse, hébergeur) | `hugo.toml`, section `[params.legal]` |
| Les tarifs et les offres | `data/offres.yaml` |
| Les six étapes de la méthode | `data/etapes.yaml` |
| Les blocs de l'accueil (enjeux, solutions, bénéfices) | `data/accueil.yaml` |
| Le titre et le texte du bandeau d'accueil | `content/_index.md` |
| Une page (Offres, Méthode, Confidentialité, À propos, Contact…) | `content/<page>.md` |
| Les articles | `content/ressources/*.md` |
| Le menu | `hugo.toml`, section `[menus]` |
| Couleurs et mise en page | `assets/css/main.css` (variables en haut du fichier) |

Les textes sont en **Markdown** : `**gras**`, `## Titre`, `- liste`, `[lien](/offres/)`.

**Typographie française.** Mettez une espace insécable avant `? : ! ;` et à l'intérieur des guillemets `« »`, pour éviter qu'un signe se retrouve seul en début de ligne. Sous Linux, l'espace insécable se tape avec AltGr + Maj + Espace.

## Prévisualiser

Installez Hugo, de préférence en version **0.168.0** (`.hugo-version`) :

```bash
sudo snap install hugo
```

Puis lancez la prévisualisation :

```bash
hugo server
```

Ouvrez http://localhost:1313 : chaque modification enregistrée s'affiche immédiatement.

## Publier un article

```bash
hugo new content ressources/titre-de-mon-article.md
```

Le fichier créé contient un modèle à remplir. L'article reste invisible tant que `draft: true`.

- Pour le publier, passez à `draft: false`.
- **Pour programmer une publication**, mettez une date future dans `date:`. Le site est reconstruit chaque matin et l'article apparaîtra le jour venu.

Un article LinkedIn peut être repris tel quel, puis enrichi. Retirez les émojis et les hashtags, et ajoutez des intertitres.

## Vérifier avant de publier

```bash
hugo --gc --minify && python3 scripts/check_site.py
```

Le script signale les liens cassés, toute ressource chargée depuis un autre site et les mentions légales encore « à compléter ».

## Mettre en ligne

### Version actuelle : Cloudflare Pages (legalsmart.willyrv.com)

Cloudflare Pages construit et publie le site lui-même à chaque `git push` sur `main`. Réglages du projet Pages :

- Build command : `hugo --gc --minify` ; output directory : `public` ;
- variables d'environnement :
  - `HUGO_VERSION` = la version de `.hugo-version` ;
  - `HUGO_BASEURL` = `https://legalsmart.willyrv.com/` (remplace `baseURL` de `hugo.toml`) ;
  - `HUGO_PARAMS_NOINDEX` = `true`, tant que ce n'est qu'une prévisualisation (les moteurs de recherche n'indexent pas le site).

Pour publier les articles programmés le jour venu, créer un *deploy hook* dans Cloudflare (Settings → Builds → Deploy hooks) et enregistrer son URL dans le secret GitHub `CLOUDFLARE_DEPLOY_HOOK`. Le workflow l'appelle chaque matin.

### Hébergeur français par rsync

À chaque `git push` sur `main`, GitHub Actions construit le site et le vérifie (`.github/workflows/deploy.yml`). Pour qu'il le **publie** aussi chez l'hébergeur :

1. **Créer un hébergement** chez un acteur français acceptant SSH/rsync, par exemple OVHcloud (hébergement web avec accès SSH), alwaysdata, ou un petit serveur. Faire pointer le nom de domaine `legalsmart.ai` vers cet hébergement et activer le certificat HTTPS.
2. **Créer une clé SSH dédiée** au déploiement et ajouter sa partie publique sur l'hébergement :

   ```bash
   ssh-keygen -t ed25519 -f deploy_key -N ""
   ```

3. **Dans GitHub, ajouter les secrets** (Settings → Secrets and variables → Actions) :
   - `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_PATH` (dossier web, par exemple `www`) ;
   - `DEPLOY_SSH_KEY` : contenu du fichier `deploy_key` ;
   - `DEPLOY_KNOWN_HOSTS` : résultat de `ssh-keyscan <hôte>`, à vérifier.
4. **Ajouter la variable** `DEPLOY_ENABLED` = `true`.
5. **Supprimer** le fichier `deploy_key` de votre poste une fois enregistré.

*Alternative S3 (Scaleway Object Storage) :* remplacer l'étape rsync par `aws s3 sync public/ s3://<bucket> --delete --endpoint-url https://s3.fr-par.scw.cloud`.

## Avant la mise en ligne

- [ ] Compléter `[params.legal]` dans `hugo.toml` (adresse, SIRET, TVA). La construction affiche un avertissement tant que c'est vide. L'hébergeur y est renseigné : le mettre à jour en cas de changement d'hébergeur.
- [ ] Vérifier les coordonnées dans `[params.contact]`, et ajouter si souhaité un lien de prise de rendez-vous (`booking_url`).
- [ ] Vérifier la disponibilité et la réservation du nom de domaine.
- [ ] Relire les articles de `content/ressources/` : ils reprennent le plan LinkedIn et méritent des exemples vécus.
- [ ] Facultatif : une photo professionnelle pour la page « À propos ». Le monogramme « WR » est utilisé en attendant.

## Image de partage

`static/images/og-legal-smart.png` est l'aperçu affiché par LinkedIn quand un lien du site est partagé. Pour le modifier, éditez `scripts/og-image.html`, puis régénérez l'image (Chrome ou Chromium nécessaire) :

```bash
./scripts/og-image.sh
```

## Organisation

```
hugo.toml            configuration, coordonnées, mentions légales, menus
content/             pages et articles (Markdown)
data/                offres, méthode, blocs de l'accueil (YAML)
layouts/             gabarits HTML (rarement modifiés)
assets/css/main.css  feuille de style unique
static/              favicon, images
scripts/             vérification du site, image de partage
archetypes/          modèle de nouvel article
.github/workflows/   construction, vérification et publication automatiques
```
