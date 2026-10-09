#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plantillas HTML del sitio público de El Mañanero Deportes.

Diseño editorial tipo noticiero: masthead con logo, barra de navegación
sólida, cintillo de titulares, portada jerárquica y secciones tipográficas.
Iconografía mínima: solo redes sociales, reproductor y menú móvil.
"""
import html
import json
import re
from datetime import datetime

E = html.escape

BRAND = "El Mañanero Deportes"
CATS = ["Noticias", "Deportes", "Salud y Belleza", "Personalidades Locales", "Comunidad", "Eventos"]
ASSET_V = "7"

MES_LARGO = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
             "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
DIA_LARGO = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


# ----------------------------------------------------------------------------
# Utilidades
# ----------------------------------------------------------------------------
def icon(name, size=18, cls=""):
    P = {
        "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
        "x": '<path d="M18 6 6 18M6 6l12 12"/>',
        "chevron-right": '<path d="m9 18 6-6-6-6"/>',
        "chevron-left": '<path d="m15 18-6-6 6-6"/>',
        "chevron-down": '<path d="m6 9 6 6 6-6"/>',
        "play": '<polygon points="6 3 20 12 6 21 6 3"/>',
        "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
        "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
        "tag": '<path d="M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z"/><circle cx="7.5" cy="7.5" r=".5" fill="currentColor"/>',
        "newspaper": '<path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"/><path d="M18 14h-8M15 18h-5M10 6h8v4h-8V6Z"/>',
        "video": '<path d="m16 13 5.223 3.482a.5.5 0 0 0 .777-.416V7.87a.5.5 0 0 0-.752-.432L16 10.5"/><rect x="2" y="6" width="14" height="12" rx="2"/>',
        "image": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>',
        "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
        "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
        "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
        "send": '<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
        "settings": '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>',
        "layout-dashboard": '<rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/>',
        "file-text": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4M10 9H8M16 13H8M16 17H8M10 21H8"/>',
        "inbox": '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
        "log-out": '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="m16 17 5-5-5-5M21 12H9"/>',
        "plus": '<path d="M5 12h14M12 5v14"/>',
        "trash-2": '<path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M10 11v6M14 11v6"/>',
        "pencil": '<path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/><path d="m15 5 4 4"/>',
        "eye": '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
        "upload": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/>',
        "grip-vertical": '<circle cx="9" cy="12" r="1"/><circle cx="9" cy="5" r="1"/><circle cx="9" cy="19" r="1"/><circle cx="15" cy="12" r="1"/><circle cx="15" cy="5" r="1"/><circle cx="15" cy="19" r="1"/>',
        "arrow-left": '<path d="m12 19-7-7 7-7M19 12H5"/>',
        "arrow-up": '<path d="m5 12 7-7 7 7M12 19V5"/>',
        "arrow-down": '<path d="M12 5v14m7-7-7 7-7-7"/>',
        "check": '<path d="M20 6 9 17l-5-5"/>',
        "facebook": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
        "x-social": '<path d="M4 4l16 16M20 4 4 20"/>',
        "instagram": '<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
        "youtube": '<path d="M2.5 17a24.12 24.12 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.56 49.56 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24.12 24.12 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.55 49.55 0 0 1-16.2 0A2 2 0 0 1 2.5 17"/><path d="m10 15 5-3-5-3z"/>',
        "mic": '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v3"/>',
        "trophy": '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6M18 9h1.5a2.5 2.5 0 0 0 0-5H18M4 22h16M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22M18 2H6v7a6 6 0 0 0 12 0V2Z"/>',
        "external-link": '<path d="M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
        "copy": '<rect x="8" y="8" width="14" height="14" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
        "shield": '<path d="M12 22s8-3.5 8-10V5l-8-3-8 3v7c0 6.5 8 10 8 10z"/>',
        "save": '<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><path d="M17 21v-8H7v8M7 3v5h8"/>',
        "key": '<circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6M15.5 7.5l3 3L22 7l-3-3"/>',
        "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
        "home": '<path d="M3 11 12 3l9 8M5 10v10h14V10"/>',
        "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    }
    return (f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{P.get(name, P["menu"])}</svg>')


def catslug(c):
    repl = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n"}
    c = "".join(repl.get(ch, ch) for ch in str(c or "").lower())
    return re.sub(r"[^a-z0-9]+", "-", c).strip("-")


def esc(s):
    return E(str(s or ""))


def fmt_date(iso):
    try:
        d = datetime.fromisoformat(iso)
        meses = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
        return f"{d.day} {meses[d.month-1]} {d.year}"
    except Exception:
        return iso


def fecha_hoy():
    n = datetime.now()
    return f"{DIA_LARGO[n.weekday()]}, {n.day} de {MES_LARGO[n.month-1]} de {n.year}"


def social_links(settings, with_icons=True, size=18):
    social = settings.get("social", {}) if isinstance(settings.get("social"), dict) else {}
    out = []
    for n, key in [("Facebook", "facebook"), ("X", "x"), ("Instagram", "instagram"), ("YouTube", "youtube")]:
        u = (social.get(key) or "").strip()
        if u:
            ic = icon(key if key != "x" else "x-social", size) if with_icons else ""
            out.append(f'<a href="{esc(u)}" target="_blank" rel="noopener noreferrer" aria-label="{n}">{ic}'
                       f'{"" if with_icons else n}</a>')
    return "".join(out)


# ----------------------------------------------------------------------------
# Shell público
# ----------------------------------------------------------------------------
def shell(base, settings, title, desc, canonical, body, jsonld="", active="",
          ogimage="/og-image.jpg", ticker=None):
    social = settings.get("social", {})
    pages = []
    try:
        pages = published_pages()
    except Exception:
        pass
    nav = [("Inicio", "/", ""), ("Noticias", "/noticias", "noticias"),
           ("Videos", "/videos", "videos"), ("Nosotros", "/nosotros", "nosotros"),
           ("Contacto", "/contacto", "contacto")]
    nav_html = "".join(
        f'<a href="{u}" class="nav-link{" active" if key == active else ""}">{t}</a>'
        for t, u, key in nav)
    nav_pages = "".join(
        f'<a href="/{esc(p["slug"])}" class="nav-link{" active" if active == p["slug"] else ""}">{esc(p["title"])}</a>'
        for p in pages)
    social_html = social_links(settings)
    social_html_sm = social_links(settings, size=15)

    # Cintillo de titulares (noticias reales; si no hay, el lema del sitio)
    items = list(ticker or [])
    if not items:
        items = [(settings.get("tagline") or BRAND, "/")]
    half = "".join(f'<span class="tick-item"><a href="{u}">{esc(t)}</a></span>'
                   f'<span class="tick-sep" aria-hidden="true">•</span>' for t, u in items)
    track = f'<div class="ticker-track">{half}{half}</div>'

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canonical)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(base + ogimage)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{esc(base + ogimage)}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/img/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/site.css?v={ASSET_V}">
{f'<script type="application/ld+json">{jsonld}</script>' if jsonld else ''}
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>

<div class="topbar">
  <div class="wrap topbar-in">
    <span class="topbar-date">{fecha_hoy()}</span>
    <span class="topbar-loc">Oregón · Edición matutina</span>
    <nav class="topbar-social" aria-label="Redes sociales">{social_html_sm}</nav>
  </div>
</div>

<header class="masthead">
  <div class="wrap masthead-in">
    <a class="brand" href="/" aria-label="{BRAND} — Inicio">
      <img src="/img/logo-h.png?v=2" alt="{BRAND}" width="218" height="53">
    </a>
    <p class="mast-tagline">{esc(settings.get("tagline", ""))}</p>
  </div>
  <nav class="mainnav" aria-label="Principal">
    <div class="wrap mainnav-in">
      {nav_html}{nav_pages}
      <button class="nav-toggle" id="navToggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="drawer">{icon("menu", 22)}</button>
    </div>
  </nav>
  <div class="ticker" role="region" aria-label="Último minuto">
    <span class="ticker-label"><i class="live-dot" aria-hidden="true"></i>Último minuto</span>
    <div class="ticker-viewport">{track}</div>
  </div>
</header>

<div class="drawer" id="drawer" hidden>
  <div class="drawer-scrim" data-close></div>
  <nav class="drawer-panel" aria-label="Menú móvil">
    <div class="drawer-head"><b>Menú</b>
      <button class="icon-btn" data-close aria-label="Cerrar menú">{icon("x", 20)}</button></div>
    {"".join(f'<a href="{u}" class="drawer-link{" on" if key == active else ""}">{t}</a>' for t, u, key in nav)}
    {nav_pages.replace('class="nav-link"', 'class="drawer-link"')}
    <div class="drawer-social">{social_html}</div>
  </nav>
</div>

<main id="main">
{body}
</main>

<footer class="footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <a href="/"><img src="/img/logo-h.png?v=2" alt="{BRAND}" width="177" height="43"></a>
      <p>{esc(settings.get("tagline", ""))}</p>
      <p class="footer-loc">Hecho en Oregón para la comunidad hispana.</p>
    </div>
    <nav aria-label="Secciones">
      <h4>Secciones</h4>
      <ul>{"".join(f'<li><a href="/categoria/{catslug(c)}">{c}</a></li>' for c in CATS)}</ul>
    </nav>
    <nav aria-label="El sitio">
      <h4>El sitio</h4>
      <ul><li><a href="/">Inicio</a></li><li><a href="/noticias">Noticias</a></li>
      <li><a href="/videos">Videos</a></li><li><a href="/contacto">Contacto</a></li>
      {"".join(f'<li><a href="/{esc(p["slug"])}">{esc(p["title"])}</a></li>' for p in pages)}</ul>
    </nav>
    <div>
      <h4>Síguenos</h4>
      <div class="footer-social">{social_html}</div>
      <h4 class="mt">Escríbenos</h4>
      <p class="footer-mail">{esc(settings.get("contactEmail") or "Vía redes sociales")}</p>
    </div>
  </div>
  <div class="footer-bar">
    <div class="wrap footer-bar-in">
      <span>© {datetime.now().year} {BRAND}. Todos los derechos reservados.</span>
      <span class="footer-links"><a href="/sitemap.xml">Sitemap</a><a href="/rss.xml">RSS</a></span>
    </div>
  </div>
</footer>
<script src="/js/site.js?v={ASSET_V}" defer></script>
</body>
</html>'''


# ----------------------------------------------------------------------------
# Bloques de contenido
# ----------------------------------------------------------------------------
def video_embed(b):
    yt = b.get("yt", "")
    if yt:
        m = re.search(r"(?:v=|youtu\.be/|embed/)([\w-]{6,})", yt)
        if m:
            return (f'<div class="vid-embed"><iframe src="https://www.youtube-nocookie.com/embed/{m.group(1)}" '
                    f'title="Video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; '
                    f'gyroscope; picture-in-picture" allowfullscreen></iframe></div>')
    if b.get("src"):
        return (f'<div class="vid-file"><video src="{esc(b["src"])}" controls playsinline '
                f'preload="metadata" width="1280" height="720"></video></div>')
    return ""


def render_blocks(blocks):
    out = []
    for b in blocks:
        t = b.get("t")
        if t == "h":
            out.append(f'<h2 class="blk-h">{esc(b.get("text", ""))}</h2>')
        elif t == "p":
            paras = esc(b.get("text", "")).split("\n")
            out.append("".join(f"<p>{p}</p>" for p in paras if p.strip()))
        elif t == "img":
            if b.get("src"):
                cap = f'<figcaption>{esc(b.get("cap", ""))}</figcaption>' if b.get("cap") else ""
                out.append(f'<figure class="blk-img"><img src="{esc(b["src"])}" alt="{esc(b.get("alt", ""))}" loading="lazy">{cap}</figure>')
        elif t == "video":
            emb = video_embed(b)
            cap = f'<figcaption>{esc(b.get("cap", ""))}</figcaption>' if b.get("cap") else ""
            if emb:
                out.append(f'<figure class="blk-video">{emb}{cap}</figure>')
        elif t == "q":
            by = f'<cite>— {esc(b.get("by", ""))}</cite>' if b.get("by") else ""
            out.append(f'<blockquote class="blk-q"><p>{esc(b.get("text", ""))}</p>{by}</blockquote>')
    return "\n".join(out)


CATEGORY_COVER = {
    "Noticias": "noticia",
    "Deportes": "deportes",
    "Salud y Belleza": "salud",
    "Personalidades Locales": "personalidades",
    "Comunidad": "comunidad",
    "Eventos": "eventos",
}


def _cover(p):
    if p.get("cover"):
        return f'<img src="{esc(p["cover"])}" alt="" loading="lazy">'
    name = CATEGORY_COVER.get(p.get("category", "Noticias"), "noticia")
    if p.get("kind") == "video":
        name = "video"
    return f'<img src="/img/covers/{name}.webp" alt="" width="800" height="450" loading="lazy">'


def chip(cat):
    return (f'<span class="chip"><a href="/categoria/{catslug(cat)}">{esc(cat)}</a></span>'
            if cat else "")


def card(p, base):
    """Tarjeta vertical de noticia (grids)."""
    return f'''<article class="card">
  <a class="card-media" href="{base}/noticias/{esc(p["slug"])}" tabindex="-1" aria-hidden="true">{_cover(p)}</a>
  <div class="card-body">
    {chip(p.get("category", "Noticias"))}
    <h3 class="card-title"><a href="{base}/noticias/{esc(p["slug"])}">{esc(p["title"])}</a></h3>
    <p class="card-excerpt">{esc(p.get("excerpt", ""))[:150]}</p>
    <span class="card-meta">{fmt_date(p.get("date", ""))}</span>
  </div>
</article>'''


def row_card(p, base, thumb=132):
    """Tarjeta horizontal compacta (listados de sección)."""
    return f'''<article class="rowcard">
  <a class="rowcard-media" href="{base}/noticias/{esc(p["slug"])}" tabindex="-1" aria-hidden="true">{_cover(p)}</a>
  <div class="rowcard-body">
    {chip(p.get("category", "Noticias"))}
    <h3><a href="{base}/noticias/{esc(p["slug"])}">{esc(p["title"])}</a></h3>
    <span class="card-meta">{fmt_date(p.get("date", ""))}</span>
  </div>
</article>'''


def sec_head(title, link=None, link_text="Ver todas"):
    a = f'<a class="sec-more" href="{link}">{link_text} <span aria-hidden="true">→</span></a>' if link else ""
    return f'<div class="sec-head"><h2 class="sec-title">{esc(title)}</h2><span class="sec-rule" aria-hidden="true"></span>{a}</div>'


def _ticker_from(posts, n=6):
    return [(p["title"], "/noticias/" + p["slug"]) for p in posts[:n]]


# ----------------------------------------------------------------------------
# Portada
# ----------------------------------------------------------------------------
def home(base, settings, posts):
    published = [p for p in posts if p.get("status") == "published"]
    featured = next((p for p in published if p.get("featured")), published[0] if published else None)
    rest = [p for p in published if p is not featured]
    latest = rest[:5]
    grid = rest[5:11] or rest[:6]
    used = {id(p) for p in (latest + grid)}
    by_cat = {c: [p for p in rest if p.get("category") == c and id(p) not in used][:2] for c in CATS}
    videos = [p for p in published if p.get("kind") == "video" or
              any(b.get("t") == "video" for b in p.get("blocks", []))][:4]

    # --- Hero ---
    if featured:
        hero = f'''<article class="hero-main">
      <a class="hero-media" href="{base}/noticias/{esc(featured["slug"])}">{_cover(featured)}
        <span class="hero-chip">{esc(featured.get("category", "Noticias"))}</span></a>
      <div class="hero-body">
        <h1><a href="{base}/noticias/{esc(featured["slug"])}">{esc(featured["title"])}</a></h1>
        <p class="hero-excerpt">{esc(featured.get("excerpt", ""))}</p>
        <span class="hero-meta">Por {esc(featured.get("author", "Redacción"))} · {fmt_date(featured.get("date", ""))}</span>
      </div>
    </article>'''
    else:
        hero = ('<article class="hero-main hero-empty"><div class="hero-body">'
                '<h1>Bienvenidos a ' + esc(settings.get("siteTitle", BRAND)) + '</h1>'
                '<p class="hero-excerpt">' + esc(settings.get("heroSubtitle", "")) + '</p></div></article>')

    rail_items = "".join(
        f'''<li><a class="rail-item" href="{base}/noticias/{esc(p["slug"])}">
        <span class="rail-num" aria-hidden="true">{i + 1:02d}</span>
        <span class="rail-thumb">{_cover(p)}</span>
        <span class="rail-txt"><b>{esc(p["title"])}</b><i>{fmt_date(p.get("date", ""))}</i></span>
      </a></li>'''
        for i, p in enumerate(latest)) or '<li class="muted">Pronto: primeras notas.</li>'

    grid_html = "".join(card(p, base) for p in grid)

    def band_cat(cat, dark=False):
        items_cat = by_cat.get(cat, [])
        if not items_cat:
            return ""
        cards = "".join(row_card(p, base) for p in items_cat)
        return f'''<div class="col-sec">
      {sec_head(cat, "/categoria/" + catslug(cat))}
      <div class="col-sec-list">{cards}</div>
    </div>'''

    sports = [p for p in published if p.get("category") == "Deportes" and p is not featured][:4]
    sports_html = "".join(
        f'''<article class="sport-card"><a class="sport-media" href="{base}/noticias/{esc(p["slug"])}">{_cover(p)}</a>
      <div class="sport-body"><h3><a href="{base}/noticias/{esc(p["slug"])}">{esc(p["title"])}</a></h3>
      <span class="card-meta">{fmt_date(p.get("date", ""))}</span></div></article>'''
        for p in sports)

    vids_html = "".join(
        f'''<article class="vid-card"><a class="vid-media" href="{base}/noticias/{esc(p["slug"])}">{_cover(p)}
        <span class="vid-play" aria-hidden="true">{icon("play", 22)}</span></a>
        <div class="vid-body"><h3><a href="{base}/noticias/{esc(p["slug"])}">{esc(p["title"])}</a></h3>
        <span class="card-meta">{fmt_date(p.get("date", ""))}</span></div></article>'''
        for p in videos)

    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "WebSite",
        "name": BRAND, "url": base + "/",
        "publisher": {"@type": "Organization", "name": BRAND,
                      "logo": {"@type": "ImageObject", "url": base + "/img/mark.png"}},
    }, ensure_ascii=False)

    row1 = (f'<div class="wrap duo">{band_cat("Salud y Belleza")}{band_cat("Comunidad")}</div>') \
        if by_cat.get("Salud y Belleza") or by_cat.get("Comunidad") else ""
    row2 = (f'<div class="wrap duo">{band_cat("Personalidades Locales")}{band_cat("Eventos")}</div>') \
        if by_cat.get("Personalidades Locales") or by_cat.get("Eventos") else ""
    sports_band = f'''<section class="band band-navy" aria-label="Deportes">
    <div class="wrap">
      {sec_head("Deportes", "/categoria/deportes")}
      <div class="sport-grid">{sports_html}</div>
    </div>
  </section>''' if sports_html else ""
    vids_band = f'''<section class="band band-dark" aria-label="Videos">
    <div class="wrap">
      {sec_head("Videos", "/videos", "Ver todos")}
      <div class="vid-grid">{vids_html}</div>
    </div>
  </section>''' if vids_html else ""

    body = f'''
<section class="hero wrap" aria-label="Portada">
  {hero}
  <aside class="hero-rail" aria-label="Últimas noticias">
    <h2 class="rail-title">Últimas noticias</h2>
    <ol class="rail-list">{rail_items}</ol>
  </aside>
</section>

{f'<section class="section"><div class="wrap">{sec_head("Últimas noticias", "/noticias")}<div class="grid-3">{grid_html}</div></div></section>' if grid_html else ''}
{sports_band}
{row1}
{row2}
{vids_band}
<section class="cta-strip" aria-label="Contacto">
  <div class="wrap cta-in">
    <div><h2>¿Tienes una historia que contar?</h2>
    <p>La comunidad quiere saber. Escríbenos y te leemos en el próximo programa.</p></div>
    <a class="btn-navy" href="/contacto">Contáctanos</a>
  </div>
</section>'''
    return shell(base, settings, f"{settings.get('siteTitle', BRAND)} — Noticias y deportes en Oregón",
                 settings.get("heroSubtitle", "Noticias, deportes y comunidad hispana en Oregón."),
                 base + "/", body, jsonld, active="",
                 ticker=_ticker_from(published))


# ----------------------------------------------------------------------------
# Noticias
# ----------------------------------------------------------------------------
def noticias(base, posts, page=1, cat=None, cat_slug=None):
    published = [p for p in posts if p.get("status") == "published"]
    if cat:
        published = [p for p in published if p.get("category") == cat]
    per = 9
    total = (len(published) + per - 1) // per or 1
    page = max(1, min(page, total))
    chunk = published[(page - 1) * per: page * per]
    cards = "".join(card(p, base) for p in chunk) or '<p class="muted">Aún no hay noticias publicadas.</p>'
    pager = "".join(f'<a class="pg{" on" if n == page else ""}" href="/noticias?page={n}">{n}</a>'
                    for n in range(1, total + 1))
    chips = "".join(f'<a class="cat-chip{" on" if c == cat else ""}" href="/categoria/{catslug(c)}">{c}</a>'
                    for c in CATS)
    title = f"{cat} — Noticias" if cat else "Noticias"
    desc = "Todas las noticias y análisis de El Mañanero Deportes" + (f" en la categoría {cat}." if cat else ".")
    canon = base + ("/noticias" if not cat else "/categoria/" + (cat_slug or catslug(cat)))
    body = f'''<section class="section"><div class="wrap">
    {sec_head(title)}
    <div class="cat-chips">{chips}</div>
    <div class="grid-3">{cards}</div>
    <nav class="pager" aria-label="Páginas">{pager}</nav>
  </div></section>'''
    return shell(base, _s(), title + " — " + BRAND, desc, canon, body, active="noticias",
                 ticker=_ticker_from(published))


def post_detail(base, post, posts):
    published = [p for p in posts if p.get("status") == "published"]
    cover_html = (f'<img src="{esc(post.get("cover"))}" alt="" width="1600" height="900">'
                  if post.get("cover") else "")
    others = [p for p in published if p["id"] != post["id"]][:3]
    rel = "".join(card(p, base) for p in others)
    cat = post.get("category", "Noticias")
    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": post["title"], "description": post.get("excerpt", ""),
        "datePublished": post.get("date", ""),
        "articleSection": cat,
        "author": {"@type": "Person", "name": post.get("author", "Redacción El Mañanero")},
        "publisher": {"@type": "Organization", "name": BRAND},
        "mainEntityOfPage": base + "/noticias/" + post["slug"],
    }, ensure_ascii=False)
    body = f'''<article class="article-wrap"><div class="wrap article">
    <nav class="crumbs" aria-label="Ruta"><a href="/noticias">Noticias</a>
      <span aria-hidden="true">/</span>
      <a href="/categoria/{catslug(cat)}">{esc(cat)}</a>
      <span aria-hidden="true">/</span></nav>
    <h1 class="art-title">{esc(post["title"])}</h1>
    <p class="art-standfirst">{esc(post.get("excerpt", ""))}</p>
    <div class="art-meta">
      <span class="art-author">Por {esc(post.get("author", "Redacción El Mañanero"))}</span>
      <span class="art-date">{fmt_date(post.get("date", ""))}</span>
      <a class="chip" href="/categoria/{catslug(cat)}">{esc(cat)}</a>
    </div>
    {f'<figure class="art-cover">{cover_html}</figure>' if cover_html else ''}
    <div class="art-body">{render_blocks(post.get("blocks", []))}</div>
    <p class="art-back"><a href="/noticias">Volver a noticias</a></p>
  </div></article>
  {f'<section class="section"><div class="wrap">{sec_head("Sigue leyendo")}<div class="grid-3">{rel}</div></div></section>' if rel else ''}'''
    return shell(base, _s(), f'{post["title"]} — {BRAND}', post.get("excerpt", ""),
                 base + "/noticias/" + post["slug"], body, jsonld, active="noticias",
                 ticker=_ticker_from(published))


def videos(base, vids):
    cards = "".join(
        f'''<article class="vid-card"><a class="vid-media" href="{base}/noticias/{esc(p["slug"])}">{_cover(p)}
        <span class="vid-play" aria-hidden="true">{icon("play", 22)}</span></a>
        <div class="vid-body"><h3><a href="{base}/noticias/{esc(p["slug"])}">{esc(p["title"])}</a></h3>
        <p class="card-excerpt">{esc(p.get("excerpt", ""))[:130]}</p>
        <span class="card-meta">{fmt_date(p.get("date", ""))}</span></div></article>'''
        for p in vids) or '<p class="muted">Pronto: primeros videos.</p>'
    body = f'''<section class="band band-dark"><div class="wrap">
    {sec_head("Videos")}
    <div class="vid-grid">{cards}</div></div></section>'''
    return shell(base, _s(), "Videos — " + BRAND, "Videos y análisis de El Mañanero Deportes.",
                 base + "/videos", body, active="videos", ticker=_ticker_from(vids))


def custom_page(base, page, pages):
    body = f'''<section class="article-wrap"><div class="wrap article">
    <h1 class="art-title">{esc(page["title"])}</h1>
    <div class="art-body">{render_blocks(page.get("blocks", []))}</div>
  </div></section>'''
    return shell(base, _s(), f'{page["title"]} — {BRAND}', page["title"],
                 base + "/" + page["slug"], body, active=page["slug"])


def contacto(base, settings, ok=False):
    okmsg = ('<div class="form-ok">' + icon("check", 20) +
             '<div><b>¡Mensaje enviado!</b><p>Gracias por escribirnos. Te respondemos muy pronto.</p></div></div>'
             if ok else "")
    email = settings.get("contactEmail") or ""
    correo_html = (('<a href="mailto:' + esc(email) + '">' + esc(email) + '</a>')
                   if email else "A través de nuestras redes sociales")
    body = f'''
<section class="contact-hero">
  <div class="wrap">
    <h1 class="contact-title">Contacto</h1>
    <p class="contact-lead">¿Tienes una historia, una pregunta o quieres colaborar con El Mañanero?
    Escríbenos y te leemos en el próximo programa.</p>
  </div>
</section>
<section class="section contact-main">
  <div class="wrap contact-grid">
    <aside class="contact-aside" aria-label="Datos de contacto">
      <div class="c-card">
        <h4>Correo</h4>
        <p class="c-big">{correo_html}</p>
      </div>
      <div class="c-card">
        <h4>Síguenos</h4>
        <div class="contact-social">{social_links(settings)}</div>
      </div>
      <div class="c-card">
        <h4>Cobertura</h4>
        <p>Área metropolitana de Portland · Oregón</p>
      </div>
      <div class="c-card">
        <h4>Horario</h4>
        <p>Lunes a domingo, desde las 6:00 AM</p>
      </div>
    </aside>
    <div class="contact-form-col">
      {okmsg}
      <form class="form-card" method="post" action="/contacto">
        <h2 class="form-title">Escríbenos</h2>
        <div class="form-row">
          <label for="cf-name">Nombre<input id="cf-name" name="name" type="text" required maxlength="120" autocomplete="name" placeholder="Tu nombre"></label>
          <label for="cf-email">Correo electrónico<input id="cf-email" name="email" type="email" required maxlength="160" autocomplete="email" placeholder="tu@correo.com"></label>
        </div>
        <label for="cf-msg">Mensaje<textarea id="cf-msg" name="message" rows="7" required maxlength="4000" placeholder="Cuéntanos tu historia o tu pregunta…"></textarea></label>
        <input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;opacity:0">
        <div class="form-foot">
          <p class="form-note">Respondemos en un máximo de 48 horas.</p>
          <button class="btn-submit" type="submit">Enviar mensaje</button>
        </div>
      </form>
    </div>
  </div>
</section>'''
    return shell(base, settings, "Contacto — " + BRAND, "Contacta al equipo de El Mañanero Deportes.",
                 base + "/contacto", body, active="contacto")


def not_found():
    return f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Página no encontrada — {BRAND}</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/css/site.css?v={ASSET_V}"></head>
<body class="nf"><main><span class="nf-code">Error 404</span><h1>Página no encontrada</h1>
<p>El contenido que buscas no existe o fue movido.</p>
<a class="btn-submit" href="/">Volver al inicio</a></main></body></html>'''


def sitemap(base, data):
    urls = ["/", "/noticias", "/videos", "/nosotros", "/contacto"]
    urls += ["/categoria/" + catslug(c) for c in CATS]
    urls += ["/noticias/" + p["slug"] for p in data["posts"] if p.get("status") == "published"]
    urls += ["/" + p["slug"] for p in data["pages"] if p.get("status") == "published"]
    items = "".join(f"<url><loc>{base}{u}</loc></url>" for u in urls)
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{items}</urlset>')


def rss(base, posts):
    items = "".join(
        f"<item><title>{esc(p['title'])}</title><link>{base}/noticias/{esc(p['slug'])}</link>"
        f"<description>{esc(p.get('excerpt', ''))}</description><pubDate>{p.get('date', '')}</pubDate>"
        f"<guid>{base}/noticias/{esc(p['slug'])}</guid></item>"
        for p in posts[:20])
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
            f'<title>{BRAND}</title><link>{base}</link><description>Deportes sin filtro</description>{items}</channel></rss>')


def _s():
    from server import store
    return store()["settings"]

# Vista del panel (definidas en admin_ui.py)
from admin_ui import (admin_login, admin_home, admin_posts, admin_editor,
                      admin_pages, admin_media, admin_inbox, admin_settings)  # noqa: E402
