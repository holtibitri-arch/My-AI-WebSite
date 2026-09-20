#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tiene sitemap.xml allineata alle pagine vere sul disco.

Perche' esiste: fino al 2026-09-20 la sitemap si modificava a mano a ogni articolo
nuovo, inserendo un blocco <url> con una sostituzione di stringa. Funziona finche' non
sbagli, e sbagliare vuol dire una pagina che Google non vede mai.

Principio di progetto: **aggiunge e aggiorna, non rimescola.** I blocchi delle URL
gia' presenti restano dove sono e come sono, salvo che gli hreflang della pagina siano
cambiati davvero. Le pagine nuove si appendono in fondo. Cosi' il diff mostra solo
quello che e' successo, e una sitemap senza modifiche produce zero righe di diff.

L'appaiamento fra lingue non e' inventato qui: viene dai tag <link rel="alternate">
che stanno gia' nelle pagine. Se una pagina ha hreflang sbagliati, la sitemap lo
riporta invece di mascherarlo, e lo script lo segnala.

Uso:
    python tools/build_sitemap.py            # mostra cosa cambierebbe, non scrive
    python tools/build_sitemap.py --write    # applica
"""
import os
import re
import sys
import subprocess

BASE = "https://holtibitri.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP = os.path.join(ROOT, "sitemap.xml")

# convenzioni per le pagine NUOVE, dedotte dal percorso. Le esistenti non si toccano.
REGOLE = [
    (lambda u: u == "/", ("monthly", "1.0")),
    (lambda u: u == "/it/", ("monthly", "0.9")),
    (lambda u: u.endswith("/privacy/"), ("yearly", "0.3")),
    (lambda u: True, ("yearly", "0.8")),
]


def convenzioni(path_url):
    for test, val in REGOLE:
        if test(path_url):
            return val


def data_git(path_file):
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%ad", "--date=short", "--", path_file],
                             cwd=ROOT, capture_output=True, text=True, timeout=20)
        return out.stdout.strip() or None
    except Exception:
        return None


def scansiona():
    """Ogni index.html sul disco, con i suoi hreflang e la data buona per lastmod."""
    trovate = {}
    for cartella, _dirs, files in os.walk(ROOT):
        parti = cartella.split(os.sep)
        if ".git" in parti or "tools" in parti:
            continue
        if "index.html" not in files:
            continue
        p = os.path.join(cartella, "index.html")
        rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
        path_url = "/" + rel[: -len("index.html")]
        with open(p, "rb") as f:
            testa = f.read(8192).decode("utf-8", "replace")
        canon = re.search(r'<link rel="canonical" href="([^"]+)"', testa)
        alts = re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', testa)
        mod = re.search(r'<meta property="article:modified_time" content="(\d{4}-\d{2}-\d{2})', testa)
        pub = re.search(r'<meta property="article:published_time" content="(\d{4}-\d{2}-\d{2})', testa)
        trovate[BASE + path_url] = {
            "path": path_url, "file": p, "alts": alts,
            "canonical": canon.group(1) if canon else None,
            "lastmod": (mod or pub).group(1) if (mod or pub) else data_git(p),
        }
    return trovate


def blocchi_esistenti(xml):
    """Spezza la sitemap nei suoi <url>...</url>, indicizzati per <loc>, mantenendo l'ordine."""
    out = []
    for m in re.finditer(r"  <url>\n(.*?)\n  </url>\n", xml, re.S):
        loc = re.search(r"<loc>([^<]+)</loc>", m.group(1))
        out.append({"loc": loc.group(1) if loc else None, "testo": m.group(0)})
    return out


def blocco(loc, alts, lastmod, cf, pr):
    r = ["  <url>", "    <loc>%s</loc>" % loc]
    for lang, href in alts:
        r.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s" />' % (lang, href))
    if lastmod:
        r.append("    <lastmod>%s</lastmod>" % lastmod)
    r.append("    <changefreq>%s</changefreq>" % cf)
    r.append("    <priority>%s</priority>" % pr)
    r.append("  </url>")
    return "\n".join(r) + "\n"


def alts_del_blocco(testo):
    """Nella sitemap il tag e' <xhtml:link>, non <link>: cercare <link> qui non matcha nulla
    e fa risultare 'cambiati' tutti i blocchi."""
    return re.findall(r'<xhtml:link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', testo)


def stesso_appaiamento(a, b):
    """Confronto per insieme: l'ordine degli hreflang dentro un <url> non ha significato,
    e ordinarlo diversamente non e' un motivo per riscrivere il blocco."""
    return sorted(a) == sorted(b)


def main():
    with open(SITEMAP, encoding="utf-8") as f:
        xml = f.read()
    originale = xml
    pagine = scansiona()
    esistenti = blocchi_esistenti(xml.replace("\r\n", "\n"))
    noti = {b["loc"] for b in esistenti}

    problemi = []
    for loc, p in sorted(pagine.items()):
        if p["canonical"] and p["canonical"] != loc:
            problemi.append("%s: canonical punta a %s" % (p["path"], p["canonical"]))
        if not p["alts"]:
            problemi.append("%s: nessun hreflang, non sara' appaiata" % p["path"])
    for b in esistenti:
        if b["loc"] not in pagine:
            problemi.append("%s: in sitemap ma la pagina non esiste sul disco" % b["loc"])

    nuove = [loc for loc in sorted(pagine) if loc not in noti]
    cambiati = []
    corpo = []
    for b in esistenti:
        p = pagine.get(b["loc"])
        if p and p["alts"] and not stesso_appaiamento(alts_del_blocco(b["testo"]), p["alts"]):
            cf = re.search(r"<changefreq>([^<]+)", b["testo"]).group(1)
            pr = re.search(r"<priority>([^<]+)", b["testo"]).group(1)
            lm = re.search(r"<lastmod>([^<]+)", b["testo"])
            corpo.append(blocco(b["loc"], p["alts"], p["lastmod"] or (lm.group(1) if lm else None), cf, pr))
            cambiati.append(b["loc"])
        else:
            corpo.append(b["testo"])
    for loc in nuove:
        p = pagine[loc]
        cf, pr = convenzioni(p["path"])
        corpo.append(blocco(loc, p["alts"], p["lastmod"], cf, pr))

    testa = xml[: xml.index("  <url>")] if "  <url>" in xml else ""
    nuovo = testa.replace("\r\n", "\n") + "".join(corpo) + "</urlset>\n"

    for msg in problemi:
        print("  ATTENZIONE  " + msg, file=sys.stderr)

    if nuovo == originale.replace("\r\n", "\n"):
        print("sitemap gia' allineata: %d URL, %d pagine sul disco, nessuna differenza"
              % (len(esistenti), len(pagine)))
        return 0

    print("da aggiungere: %s" % (", ".join(nuove) if nuove else "nessuna"))
    print("da aggiornare: %s" % (", ".join(cambiati) if cambiati else "nessuna"))

    if "--write" not in sys.argv:
        print("\nnessuna scrittura. Rilancia con --write per applicare.")
        return 1

    eol = "\r\n" if "\r\n" in originale else "\n"
    with open(SITEMAP, "wb") as f:
        f.write(nuovo.replace("\n", eol).encode("utf-8"))
    print("sitemap riscritta: %d URL" % (len(esistenti) + len(nuove)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
