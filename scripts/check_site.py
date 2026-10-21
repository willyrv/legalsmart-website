#!/usr/bin/env python3
"""Vérifie le site construit (dossier public/) avant mise en ligne.

- chaque lien et ressource interne pointe vers un fichier existant ;
- aucune ressource n'est chargée depuis un autre domaine (pas de traceur, pas de CDN) ;
- signale les informations légales encore « à compléter ».

Usage : python3 scripts/check_site.py [public]   (code de sortie 1 en cas d'erreur)
"""

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "public")


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.resources = [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        for key in ("src", "srcset"):
            if a.get(key):
                self.resources.append(a[key])
        if tag == "link" and a.get("rel") in ("stylesheet", "icon", "preload") and a.get("href"):
            self.resources.append(a["href"])


def target_exists(path: str) -> bool:
    path = unquote(path.split("#")[0].split("?")[0])
    if not path or path == "/":
        return (ROOT / "index.html").exists()
    p = ROOT / path.lstrip("/")
    return p.is_file() or (p / "index.html").is_file()


errors, warnings = [], []
for page in sorted(ROOT.rglob("*.html")):
    html = page.read_text(encoding="utf-8")
    c = Collector()
    c.feed(html)
    rel = page.relative_to(ROOT)
    for href in c.links:
        u = urlparse(href)
        if u.scheme in ("mailto", "tel", "http", "https") and (u.scheme not in ("http", "https") or u.netloc):
            continue
        if href.startswith("#"):
            continue
        base = "/" + str(rel.parent).strip(".") + "/"
        path = u.path if u.path.startswith("/") else base + u.path
        if not target_exists(path):
            errors.append(f"{rel} : lien cassé → {href}")
    for src in c.resources:
        u = urlparse(src)
        if u.netloc and u.netloc not in ("legalsmart.ai", "localhost:1313"):
            errors.append(f"{rel} : ressource externe chargée → {src}")
        elif not u.netloc and not target_exists(u.path):
            errors.append(f"{rel} : ressource introuvable → {src}")
    if "[à compléter]" in html:
        warnings.append(f"{rel} : informations « à compléter »")

pages = len(list(ROOT.rglob("*.html")))
for w in warnings:
    print("ATTENTION", w)
for e in errors:
    print("ERREUR", e)
print(f"{pages} pages vérifiées, {len(errors)} erreur(s), {len(warnings)} avertissement(s).")
sys.exit(1 if errors else 0)
