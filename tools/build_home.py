#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera le due home, index.html (EN) e it/index.html (IT), da un sorgente solo.

Perche' esiste: fino all'11/11/2026 le due pagine erano file statici indipendenti,
1.243 righe l'uno, e ogni modifica andava ripetuta a mano in entrambi. In piu' la
lista degli articoli stava in due posti: in posts.json, letto dal browser, e in un
blocco statico dentro l'HTML. I due si erano disallineati: nel sorgente restava una
card tolta mesi prima e due guide puntavano ancora a LinkedIn invece che al sito.

Adesso:
- i testi stanno in tools/home_content.py, le due lingue una accanto all'altra
- gli articoli stanno in posts.json e finiscono nell'HTML al momento della build:
  il browser non scarica piu' nulla, e nel sorgente c'e' quello che si vede
- lo stile della home sta in css/home.css, la base condivisa in css/site.css

Le due pagine restano file statici distinti, uno per lingua, con canonical e
hreflang reciproci: Google le indicizza separatamente, come prima. I bottoni EN/IT
sono link fra le due pagine, senza rilevamento della lingua del browser.

La build si ferma se nell'HTML finisce un em dash, se le due lingue di posts.json
non hanno la stessa forma, o se una guida ospitata non ha la copertina.

Uso:
    python tools/build_home.py            # dice cosa cambierebbe, non scrive
    python tools/build_home.py --write    # scrive index.html e it/index.html
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from home_content import CONTENT, LINKS  # noqa: E402

BASE = "https://holtibitri.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UMAMI_ID = "4d89a1e3-8961-4b64-9579-4c118118822f"

PAGES = {
    "en": {
        "file": "index.html",
        "url": "/",
        "privacy": "/privacy/",
        "locale": "en_US",
        "og_image": "/img/og-en.png",
    },
    "it": {
        "file": os.path.join("it", "index.html"),
        "url": "/it/",
        "privacy": "/it/privacy/",
        "locale": "it_IT",
        "og_image": "/img/og-it.png",
    },
}

FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;1,9..144,300"
    "&family=DM+Sans:wght@300;400;500"
    "&family=JetBrains+Mono:wght@400;500&display=swap"
)


# ---------------------------------------------------------------- utilita'
def pick(obj, lang):
    """Risolve ogni coppia T(it, en) nella lingua chiesta."""
    if isinstance(obj, dict):
        if set(obj) == {"it", "en"}:
            return obj[lang]
        return {k: pick(v, lang) for k, v in obj.items()}
    if isinstance(obj, list):
        return [pick(v, lang) for v in obj]
    return obj


def esc(text):
    return html.escape(text, quote=False)


def attr(text):
    return html.escape(text, quote=True)


def lines(parts):
    return "<br>".join(esc(p) for p in parts)


def tags(items):
    spans = "".join(f'<span class="tag">{esc(t)}</span>' for t in items)
    return f'<div class="tags">{spans}</div>'


def icon(name):
    with open(os.path.join(ROOT, "tools", "icons", name + ".svg"), encoding="utf-8") as fh:
        return fh.read().strip()


def section_header(label, title):
    return (
        '      <div class="section-header reveal">\n'
        f'        <span class="section-label">{esc(label)}</span>\n'
        f'        <h2 class="section-title">{lines(title)}</h2>\n'
        "      </div>\n"
    )


EXT = ' target="_blank" rel="noopener noreferrer"'


# ------------------------------------------------------------------- head
def render_head(c, lang):
    page = PAGES[lang]
    other = "it" if lang == "en" else "en"
    m = c["meta"]
    url = BASE + page["url"]
    og_image = BASE + page["og_image"]
    person = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Holti Bitri",
        "jobTitle": m["job_title"],
        "description": m["og_description"],
        "url": url,
        "image": BASE + "/avatar.jpg",
        "email": "mailto:" + LINKS["email"],
        "worksFor": {"@type": "Organization", "name": "TIG Factory"},
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Milan",
            "addressCountry": "IT",
        },
        "sameAs": [LINKS["linkedin"], LINKS["github"]],
    }
    ld = json.dumps(person, ensure_ascii=False, indent=2).replace("\n", "\n  ")
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- Pagina generata da tools/build_home.py. I testi stanno in tools/home_content.py,
       gli articoli in posts.json. Non modificare questo file a mano. -->
  <title>{esc(m["title"])}</title>
  <meta name="description" content="{attr(m["description"])}">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="en" href="{BASE}/">
  <link rel="alternate" hreflang="it" href="{BASE}/it/">
  <link rel="alternate" hreflang="x-default" href="{BASE}/">

  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{attr(m["og_title"])}">
  <meta property="og:description" content="{attr(m["og_description"])}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="{page["locale"]}">
  <meta property="og:locale:alternate" content="{PAGES[other]["locale"]}">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{attr(m["og_title"])}">
  <meta name="twitter:description" content="{attr(m["og_description"])}">
  <meta name="twitter:image" content="{og_image}">

  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{attr(FONTS)}" rel="stylesheet">

  <script type="application/ld+json">
  {ld}
  </script>

  <link rel="stylesheet" href="/css/site.css">
  <link rel="stylesheet" href="/css/home.css">
  <script>document.documentElement.classList.add('js');</script>
  <script defer src="https://cloud.umami.is/script.js" data-website-id="{UMAMI_ID}"></script>
</head>
<body>
"""


# -------------------------------------------------------------------- nav
def render_nav(c, lang):
    links = "\n".join(
        f'        <li><a href="{n["href"]}">{esc(n["label"])}</a></li>' for n in c["nav"]
    )

    def lang_btn(code):
        active = ' active" aria-current="page' if code == lang else ""
        return (
            f'        <a class="lang-btn{active}" href="{PAGES[code]["url"]}" '
            f'hreflang="{code}">{code.upper()}</a>'
        )

    return f"""
  <nav id="navbar">
    <a href="#home" class="nav-logo">HB_</a>
    <div class="nav-right">
      <ul class="nav-links" id="nav-links">
{links}
      </ul>
      <div class="lang-toggle">
{lang_btn("en")}
{lang_btn("it")}
      </div>
      <button class="nav-toggle" type="button" aria-label="{attr(c["menu_label"])}" aria-expanded="false" aria-controls="nav-links">
        <span></span><span></span><span></span>
      </button>
    </div>
  </nav>
"""


# ------------------------------------------------------------------- hero
def render_hero(c):
    h = c["hero"]
    # Ogni riga e' un blocco, separato da uno spazio vero: se lo schermo e' stretto
    # e una riga va a capo, le parole non si attaccano.
    claim = " ".join(f'<span class="line">{esc(part)}</span>' for part in h["claim"])
    return f"""
  <header id="home" class="hero">
    <div class="container hero-inner">
      <h1 class="hero-h1">
        <span class="hero-eyebrow">{esc(h["eyebrow"])}</span>
        <span class="hero-claim">{claim} <em>{esc(h["claim_accent"])}</em></span>
      </h1>
      <p class="hero-sub">{esc(h["sub"])}</p>
      <div class="hero-cta">
        <a href="#method" class="btn btn-primary">{esc(h["cta_primary"])}</a>
        <a href="#contact" class="btn btn-secondary">{esc(h["cta_secondary"])}</a>
      </div>
    </div>
  </header>
"""


# ------------------------------------------------------------------ about
def render_about(c):
    a = c["about"]
    paragraphs = "\n".join(f"          <p>{esc(p)}</p>" for p in a["paragraphs"])
    stats = "\n".join(
        '            <div class="stat-card">\n'
        f'              <div class="stat-number">{esc(s["number"])}</div>\n'
        f'              <div class="stat-label">{esc(s["label"])}</div>\n'
        "            </div>"
        for s in a["stats"]
    )
    clients = "".join(f"<li>{esc(name)}</li>" for name in a["clients"])
    return f"""
  <section id="about">
    <div class="container">
      <div class="about-grid">
        <div class="about-text reveal">
          <span class="section-label">{esc(a["label"])}</span>
{paragraphs}
        </div>
        <div class="about-side reveal">
          <img src="/avatar.jpg" alt="{attr(a["avatar_alt"])}" class="about-avatar" width="900" height="1433" loading="lazy">
          <div class="about-stats">
{stats}
          </div>
        </div>
      </div>
      <div class="clients reveal">
        <span class="clients-label">{esc(a["clients_label"])}</span>
        <ul class="clients-list">{clients}</ul>
      </div>
    </div>
  </section>
"""


# ----------------------------------------------------------------- method
def render_method(c):
    m = c["method"]
    rules = []
    for i, rule in enumerate(m["rules"], start=1):
        link = ""
        if "link" in rule:
            ext = EXT if rule["link"]["external"] else ""
            link = (
                f'\n            <a class="rule-link" href="{attr(rule["link"]["href"])}"{ext}>'
                f'{esc(rule["link"]["label"])} &rarr;</a>'
            )
        rules.append(
            '        <li class="rule reveal">\n'
            f'          <span class="rule-num">{i:02d}</span>\n'
            f'          <h3 class="rule-title">{esc(rule["title"])}</h3>\n'
            '          <div class="rule-body">\n'
            f'            <p>{esc(rule["text"])}</p>{link}\n'
            "          </div>\n"
            "        </li>"
        )
    return (
        '\n  <section id="method">\n    <div class="container">\n'
        + section_header(m["label"], m["title"])
        + '      <ol class="rules">\n'
        + "\n".join(rules)
        + "\n      </ol>\n    </div>\n  </section>\n"
    )


# --------------------------------------------------------------- projects
def render_projects(c):
    p = c["projects"]
    tp, fc, tig = p["toropulse"], p["fincast"], p["tig"]

    def head(title, role, actions=""):
        return (
            '          <div class="featured-head">\n'
            "            <div>\n"
            f'              <h3 class="featured-title">{esc(title)}</h3>\n'
            f'              <p class="featured-role">{esc(role)}</p>\n'
            "            </div>\n"
            f"{actions}"
            "          </div>\n"
        )

    tp_actions = (
        '            <div class="featured-actions">\n'
        f'              <a href="{LINKS["toropulse"]}"{EXT} class="btn btn-secondary btn-small">'
        f'{esc(tp["cta"])} &rarr;</a>\n'
        "            </div>\n"
    )
    fc_buttons = "\n".join(
        f'              <a href="{LINKS[key]}"{EXT} class="btn btn-secondary btn-icon" '
        f'aria-label="AI FinCast, {label}" title="{label}">{icon(svg)}</a>'
        for key, label, svg in (
            ("spotify", "Spotify", "spotify"),
            ("apple", "Apple Podcasts", "apple-podcasts"),
            ("youtube", "YouTube", "youtube"),
        )
    )
    fc_actions = (
        '            <div class="featured-actions">\n'
        f"{fc_buttons}\n"
        f'              <a href="{LINKS["fincast"]}"{EXT} class="btn btn-secondary btn-small">'
        f'{esc(fc["site"])} &rarr;</a>\n'
        "            </div>\n"
    )
    tools = "\n".join(
        '            <div class="tool">\n'
        f'              <h4 class="tool-title">{esc(item["title"])}</h4>\n'
        f'              <p>{esc(item["text"])}</p>\n'
        "            </div>"
        for item in tig["items"]
    )

    others = []
    for o in p["others"]:
        link = ""
        if "link" in o:
            link = (
                f'\n          <a class="project-link" href="{attr(o["link"]["href"])}"{EXT}>'
                f'{esc(o["link"]["label"])} &rarr;</a>'
            )
        others.append(
            '        <article class="project-card reveal">\n'
            f'          <div class="project-type">{esc(o["type"])}</div>\n'
            f'          <h3 class="project-title">{esc(o["title"])}</h3>\n'
            f'          <p class="project-desc">{esc(o["text"])}</p>\n'
            f'          {tags(o["tags"])}{link}\n'
            "        </article>"
        )

    return (
        '\n  <section id="projects">\n    <div class="container">\n'
        + section_header(p["label"], p["title"])
        + '      <div class="featured-grid" id="featured-project">\n'
        + '        <article class="featured-card reveal">\n'
        + head(tp["title"], tp["role"], tp_actions)
        + f'          <p class="featured-text">{esc(tp["text"])}</p>\n'
        + f'          <p class="featured-proof">{esc(tp["proof"])}</p>\n'
        + f'          {tags(tp["tags"])}\n'
        + "        </article>\n"
        + '        <article class="featured-card reveal">\n'
        + head(fc["title"], fc["role"], fc_actions)
        + f'          <p class="featured-text">{esc(fc["text"])}</p>\n'
        + f'          <p class="featured-proof">{esc(fc["proof"])}</p>\n'
        + f'          {tags(fc["tags"])}\n'
        + "        </article>\n"
        + '        <article class="featured-card featured-wide reveal">\n'
        + head(tig["title"], tig["role"])
        + f'          <p class="featured-text">{esc(tig["text"])}</p>\n'
        + '          <div class="tool-grid">\n'
        + tools
        + "\n          </div>\n"
        + f'          {tags(tig["tags"])}\n'
        + "        </article>\n"
        + "      </div>\n"
        + f'      <span class="section-label sub-label">{esc(p["others_label"])}</span>\n'
        + '      <div class="projects-grid">\n'
        + "\n".join(others)
        + "\n      </div>\n    </div>\n  </section>\n"
    )


# ------------------------------------------------------------- experience
def render_experience(c):
    x = c["experience"]
    items = []
    for it in x["items"]:
        end = it["to"] or x["now"]
        items.append(
            '        <div class="timeline-item reveal">\n'
            '          <div class="timeline-left">\n'
            f'            <div class="timeline-date">{esc(it["from"])} &rarr; {esc(end)}</div>\n'
            "          </div>\n"
            '          <div class="timeline-right">\n'
            f'            <div class="timeline-role">{esc(it["role"])}</div>\n'
            f'            <div class="timeline-company">{esc(it["company"])}</div>\n'
            f'            <div class="timeline-desc">{esc(it["text"])}</div>\n'
            f'            {tags(it["tags"])}\n'
            "          </div>\n"
            "        </div>"
        )
    return (
        '\n  <section id="experience">\n    <div class="container">\n'
        + section_header(x["label"], x["title"])
        + '      <div class="timeline">\n'
        + "\n".join(items)
        + "\n      </div>\n    </div>\n  </section>\n"
    )


# ---------------------------------------------------------------- writing
def load_posts():
    with open(os.path.join(ROOT, "posts.json"), encoding="utf-8") as fh:
        posts = json.load(fh)
    en, it = posts["en"], posts["it"]
    if len(en) != len(it):
        sys.exit(f"posts.json: {len(en)} voci in inglese e {len(it)} in italiano, devono essere pari")
    for i, (a, b) in enumerate(zip(en, it), start=1):
        hosted_a, hosted_b = a["url"].startswith("/"), b["url"].startswith("/")
        if hosted_a != hosted_b:
            sys.exit(f"posts.json, voce {i}: in una lingua e' ospitata sul sito e nell'altra no")
        for entry in (a, b):
            if entry["url"].startswith("/"):
                image = entry.get("image")
                if not image:
                    sys.exit(f"posts.json, voce {i}: guida ospitata senza il campo image")
                if not os.path.exists(os.path.join(ROOT, image.lstrip("/"))):
                    sys.exit(f"posts.json, voce {i}: la copertina {image} non esiste")
    return posts


def render_writing(c, posts):
    w = c["writing"]
    guides = [p for p in posts if p["url"].startswith("/")]
    linked = [p for p in posts if not p["url"].startswith("/")]
    guide_cards = "\n".join(
        f'        <a href="{attr(g["url"])}" class="guide-card reveal">\n'
        f'          <img src="{attr(g["image"])}" alt="" class="guide-cover" loading="lazy">\n'
        '          <div class="guide-body">\n'
        f'            <h3 class="guide-title">{esc(g["title"])}</h3>\n'
        f'            <p class="guide-excerpt">{esc(g["excerpt"])}</p>\n'
        '            <div class="guide-footer">\n'
        f'              <span class="guide-meta">{esc(g["date"])} &bull; {esc(g["readTime"])}</span>\n'
        f'              <span class="guide-cta">{esc(w["read"])} &rarr;</span>\n'
        "            </div>\n"
        "          </div>\n"
        "        </a>"
        for g in guides
    )
    post_rows = "\n".join(
        f'        <a href="{attr(p["url"])}"{EXT} class="post-row">\n'
        f'          <span class="post-date">{esc(p["date"])}</span>\n'
        f'          <span class="post-title">{esc(p["title"])}</span>\n'
        '          <span class="post-arrow" aria-hidden="true">&rarr;</span>\n'
        "        </a>"
        for p in linked
    )
    return (
        '\n  <section id="writing">\n    <div class="container">\n'
        + section_header(w["label"], w["title"])
        + f'      <span class="section-label sub-label">{esc(w["guides_label"])}</span>\n'
        + '      <div class="guides-grid">\n'
        + guide_cards
        + "\n      </div>\n"
        + f'      <span class="section-label sub-label">{esc(w["posts_label"])}</span>\n'
        + '      <div class="posts-list reveal">\n'
        + post_rows
        + "\n      </div>\n    </div>\n  </section>\n"
    )


# ---------------------------------------------------------------- contact
def render_contact(c):
    k = c["contact"]

    def link(href, mark, label, value, external=True):
        ext = EXT if external else ""
        return (
            f'          <a href="{attr(href)}"{ext} class="contact-link">\n'
            f'            <div class="contact-link-icon" aria-hidden="true">{esc(mark)}</div>\n'
            '            <div class="contact-link-info">\n'
            f'              <span class="contact-link-label">{esc(label)}</span>\n'
            f'              <span class="contact-link-value">{esc(value)}</span>\n'
            "            </div>\n"
            "          </a>\n"
        )

    return (
        '\n  <section id="contact">\n    <div class="container">\n'
        + section_header(k["label"], k["title"])
        + '      <div class="contact-inner reveal">\n'
        + f'        <div class="contact-text"><p>{esc(k["text"])}</p></div>\n'
        + '        <div class="contact-links">\n'
        + link("mailto:" + LINKS["email"], "@", "Email", LINKS["email"], external=False)
        + link(LINKS["linkedin"], "in", "LinkedIn", "linkedin.com/in/holtibitri")
        + link(LINKS["github"], "</>", "GitHub", "github.com/holtibitri-arch")
        + "        </div>\n      </div>\n    </div>\n  </section>\n"
    )


# ----------------------------------------------------------------- footer
SCRIPT = """
  <script>
    (function () {
      var navbar = document.getElementById('navbar');
      var toggle = navbar.querySelector('.nav-toggle');

      window.addEventListener('scroll', function () {
        navbar.classList.toggle('scrolled', window.scrollY > 20);
      }, { passive: true });

      function closeMenu() {
        navbar.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
      toggle.addEventListener('click', function () {
        var open = navbar.classList.toggle('open');
        toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      navbar.querySelectorAll('.nav-links a').forEach(function (a) {
        a.addEventListener('click', closeMenu);
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeMenu();
      });

      var items = document.querySelectorAll('.reveal');
      if (!('IntersectionObserver' in window)) {
        items.forEach(function (el) { el.classList.add('visible'); });
        return;
      }
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.05 });
      items.forEach(function (el) { io.observe(el); });
    })();
  </script>

</body>
</html>
"""


def render_footer(c, lang):
    f = c["footer"]
    return (
        "\n  <footer>\n"
        f'    {esc(f["text"])} &middot; '
        f'<a href="{PAGES[lang]["privacy"]}">{esc(f["privacy"])}</a>\n'
        "  </footer>\n"
    )


# ------------------------------------------------------------------- main
def render(lang, posts):
    c = pick(CONTENT, lang)
    page = (
        render_head(c, lang)
        + render_nav(c, lang)
        + render_hero(c)
        + render_about(c)
        + render_method(c)
        + render_projects(c)
        + render_experience(c)
        + render_writing(c, posts[lang])
        + render_contact(c)
        + render_footer(c, lang)
        + SCRIPT
    )
    for banned in ("—", "&mdash;"):
        if banned in page:
            where = page[max(0, page.index(banned) - 60): page.index(banned) + 20]
            sys.exit(f"em dash nella pagina {lang}: ...{where}...")
    return page


def main():
    write = "--write" in sys.argv[1:]
    posts = load_posts()
    changed = 0
    for lang in ("en", "it"):
        target = os.path.join(ROOT, PAGES[lang]["file"])
        new = render(lang, posts)
        old = ""
        if os.path.exists(target):
            with open(target, encoding="utf-8", newline="") as fh:
                old = fh.read()
        if new == old:
            print(f"{PAGES[lang]['file']}: invariata")
            continue
        changed += 1
        if write:
            with open(target, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(new)
            print(f"{PAGES[lang]['file']}: scritta ({len(new.splitlines())} righe)")
        else:
            print(f"{PAGES[lang]['file']}: cambierebbe ({len(new.splitlines())} righe)")
    if changed and not write:
        print("Nessun file scritto. Per applicare: python tools/build_home.py --write")


if __name__ == "__main__":
    main()
