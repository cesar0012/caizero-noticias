#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plantillas HTML del sitio público y del panel de administración (El Mañanero Deportes)."""
import html
import json
import re
from datetime import datetime

E = html.escape

BRAND = "El Mañanero Deportes"

# ----------------------------------------------------------------------------
# Iconos (Lucide, stroke currentColor)
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
            f'aria-hidden="true">{P.get(name, P["chevron-right"])}</svg>')


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


# ----------------------------------------------------------------------------
# Shell público
# ----------------------------------------------------------------------------
def shell(base, settings, title, desc, canonical, body, jsonld="", active="", ogimage="/og-image.jpg"):
    social = settings.get("social", {})
    pages = []
    try:
        pages = published_pages()
    except Exception:
        pass
    nav = [("Inicio", "/", "home"), ("Noticias", "/noticias", "newspaper"),
           ("Videos", "/videos", "video"), ("Nosotros", "/nosotros", "users"),
           ("Contacto", "/contacto", "mail")]
    nav_html = "".join(
        f'<a href="{u}" class="nav-link{" active" if a == active else ""}">{icon(ic, 16)}<span>{t}</span></a>'
        for t, u, ic, a in [(t, u, ic, active) for t, u, ic in nav])
    nav_pages = "".join(
        f'<a href="/{esc(p["slug"])}" class="nav-link{" active" if active == p["slug"] else ""}">{esc(p["title"])}</a>'
        for p in pages)
    social_html = "".join(
        f'<a href="{esc(u)}" target="_blank" rel="noopener noreferrer" aria-label="{n}">{icon(ic, 18)}</a>'
        for n, u, ic in [
            ("Facebook", social.get("facebook"), "facebook"),
            ("X", social.get("x"), "x-social"),
            ("Instagram", social.get("instagram"), "instagram"),
            ("YouTube", social.get("youtube"), "youtube"),
        ] if u)
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
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:ital,wght@0,400;0,500;0,600;0,700;0,800;1,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/site.css?v=3">
{f'<script type="application/ld+json">{jsonld}</script>' if jsonld else ''}
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
<header class="site-header">
  <div class="wrap header-row">
    <a class="brand" href="/" aria-label="{BRAND} — Inicio">
      <img src="/img/mark.png" alt="" width="44" height="44">
      <span class="brand-txt"><b>El Mañanero</b><i>Deportes</i></span>
    </a>
    <nav class="main-nav" aria-label="Principal">{nav_html}{nav_pages}</nav>
    <button class="nav-toggle" id="navToggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="drawer">{icon("menu", 22)}</button>
  </div>
  <div class="ticker" aria-hidden="true"><div class="ticker-track">
    <span>Análisis</span><i></i><span>Béisbol</span><i></i><span>LIDOM</span><i></i><span>MLB</span><i></i><span>Clásico Mundial</span><i></i><span>NBA</span><i></i>
    <span>Análisis</span><i></i><span>Béisbol</span><i></i><span>LIDOM</span><i></i><span>MLB</span><i></i><span>Clásico Mundial</span><i></i><span>NBA</span><i></i>
  </div></div>
</header>
<div class="drawer" id="drawer" hidden>
  <div class="drawer-scrim" data-close></div>
  <nav class="drawer-panel" aria-label="Menú móvil">
    <div class="drawer-head"><span class="brand-txt"><b>El Mañanero</b><i>Deportes</i></span>
      <button class="icon-btn" data-close aria-label="Cerrar menú">{icon("x", 20)}</button></div>
    {"".join(f'<a href="{u}" class="drawer-link">{icon(ic, 18)}<span>{t}</span>{icon("chevron-right", 16)}</a>' for t, u, ic in nav)}
    {nav_pages.replace('class="nav-link"', 'class="drawer-link"')}
    <div class="drawer-social">{social_html}</div>
  </nav>
</div>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div>
      <a class="brand" href="/"><img src="/img/mark.png" alt="" width="52" height="52"><span class="brand-txt"><b>El Mañanero</b><i>Deportes</i></span></a>
      <p class="muted">{esc(settings.get("tagline", ""))}</p>
      <div class="social">{social_html}</div>
    </div>
    <div><h4>Secciones</h4><ul>
      <li><a href="/">Inicio</a></li><li><a href="/noticias">Noticias</a></li>
      <li><a href="/videos">Videos</a></li><li><a href="/nosotros">Nosotros</a></li><li><a href="/contacto">Contacto</a></li>
    </ul></div>
    <div><h4>Páginas</h4><ul>{"".join(f'<li><a href="/{esc(p["slug"])}">{esc(p["title"])}</a></li>' for p in pages) or "<li>—</li>"}</ul></div>
    <div><h4>Síguenos</h4><ul class="social-list">{"".join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener noreferrer">{n}</a></li>' for n, u, ic in [("Facebook", social.get("facebook"), 0), ("X", social.get("x"), 0), ("Instagram", social.get("instagram"), 0), ("YouTube", social.get("youtube"), 0)] if u) or "<li>—</li>"}</ul></div>
  </div>
  <div class="wrap foot-legal"><span>© {datetime.now().year} {BRAND}. Todos los derechos reservados.</span><a href="/rss.xml">RSS</a></div>
</footer>
<script src="/js/site.js?v=3" defer></script>
</body>
</html>'''


# ----------------------------------------------------------------------------
# Bloques de contenido
# ----------------------------------------------------------------------------
def video_embed(b):
    yt = b.get("yt", "")
    if yt:
        m = None
        import re as _re
        m = (_re.search(r"(?:v=|youtu\.be/|embed/)([\w-]{6,})", yt))
        if m:
            return (f'<div class="vid-embed"><iframe src="https://www.youtube-nocookie.com/embed/{m.group(1)}" '
                    f'title="Video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; '
                    f'gyroscope; picture-in-picture" allowfullscreen></iframe></div>')
    if b.get("src"):
        return (f'<figure class="vid-file"><video src="{esc(b["src"])}" controls playsinline '
                f'preload="metadata"></video></figure>')
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


def card(p, base):
    cover = p.get("cover") or ""
    tag = ("Video · " if p.get("kind") == "video" else "") + p.get("category", "Noticias")
    cover_html = (f'<img src="{esc(cover)}" alt="" loading="lazy">' if cover
                  else f'<div class="card-ph">{icon("play" if p.get("kind") == "video" else "newspaper", 40)}</div>')
    return f'''<a class="card" href="{base}/noticias/{esc(p["slug"])}">
  <div class="card-media">{cover_html}<span class="card-tag">{esc(tag)}</span></div>
  <div class="card-body"><h3>{esc(p["title"])}</h3>
  <p class="muted">{esc(p.get("excerpt", ""))[:150]}</p>
  <div class="card-meta">{icon("calendar", 14)}<span>{fmt_date(p.get("date", ""))}</span></div></div>
</a>'''


# ----------------------------------------------------------------------------
# Páginas públicas
# ----------------------------------------------------------------------------
def home(base, settings, posts):
    featured = next((p for p in posts if p.get("featured")), posts[0] if posts else None)
    latest = [p for p in posts if p is not featured][:6]
    videos = [p for p in posts if p.get("kind") == "video" or any(b.get("t") == "video" for b in p.get("blocks", []))][:3]
    hero_img = settings.get("heroImage", "")
    feat_html = ""
    if featured:
        cover = featured.get("cover", "")
        media = (f'<img src="{esc(cover)}" alt="">' if cover
                 else '<div class="hero-feat-ph">' + icon("trophy", 56) + '</div>')
        feat_html = f'''<a class="hero-feat" href="{base}/noticias/{esc(featured["slug"])}">
          <div class="hero-feat-media">{media}<span class="card-tag">Destacado</span></div>
          <div class="hero-feat-body"><h3>{esc(featured["title"])}</h3>
          <p>{esc(featured.get("excerpt", ""))[:180]}</p></div></a>'''
    news_html = "".join(card(p, base) for p in latest) or '<p class="muted">Pronto: primeras notas.</p>'
    vids_html = "".join(
        f'<a class="vid-card" href="{base}/noticias/{esc(p["slug"])}"><span class="play-badge">{icon("play", 22)}</span>'
        f'<div><b>{esc(p["title"])}</b><span class="muted">{fmt_date(p.get("date", ""))}</span></div></a>'
        for p in videos) or ""
    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "WebSite",
        "name": BRAND, "url": base + "/",
        "publisher": {"@type": "Organization", "name": BRAND, "logo": {"@type": "ImageObject", "url": base + "/img/mark.png"}},
    }, ensure_ascii=False)
    body = f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <span class="plate">{icon("mic", 15)} El programa deportivo de la mañana</span>
      <h1>{esc(settings.get("heroTitle", "Deportes sin filtro"))}</h1>
      <p class="lead">{esc(settings.get("heroSubtitle", ""))}</p>
      <div class="hero-cta">
        <a class="btn btn-primary" href="/noticias">{icon("newspaper", 18)} Ver noticias</a>
        <a class="btn btn-ghost" href="/videos">{icon("play", 18)} Ver videos</a>
      </div>
    </div>
    <div class="hero-side">{feat_html}</div>
  </div>
  <div class="hero-bg" aria-hidden="true">{f'<img src="{esc(hero_img)}" alt="">' if hero_img else ''}</div>
</section>
<section class="section">
  <div class="wrap">
    <div class="sec-head"><h2 class="sec-title">{icon("newspaper", 22)} Últimas noticias</h2><a class="sec-link" href="/noticias">Ver todas {icon("chevron-right", 15)}</a></div>
    <div class="grid-3">{news_html}</div>
  </div>
</section>
{f'<section class="section alt"><div class="wrap"><div class="sec-head"><h2 class="sec-title">{icon("video", 22)} Videos</h2><a class="sec-link" href="/videos">Ver todos {icon("chevron-right", 15)}</a></div><div class="vid-list">{vids_html}</div></div></section>' if vids_html else ''}
<section class="section alt">
  <div class="wrap about-strip">
    <div>{icon("mic", 30)}</div>
    <div><h2>{esc(settings.get("siteTitle", BRAND))}</h2><p>{esc(settings.get("tagline", ""))}</p></div>
    <a class="btn btn-ghost" href="/nosotros">Conócenos {icon("chevron-right", 15)}</a>
  </div>
</section>
<section class="section" id="contacto">
  <div class="wrap contact-grid">
    <div>
      <h2 class="sec-title">{icon("mail", 22)} Contacto</h2>
      <p class="muted">¿Tienes una historia, una pregunta o quieres colaborar? Escríbenos.</p>
      <ul class="contact-info">
        <li>{icon("mail", 18)}<span>{esc(settings.get("contactEmail") or "Disponible en redes sociales")}</span></li>
      </ul>
      <div class="social">{"".join(f'<a href="{esc(u)}" target="_blank" rel="noopener noreferrer" aria-label="{n}">{icon(ic, 20)}</a>' for n, u, ic in [("Facebook", settings.get("social", {}).get("facebook"), "facebook"), ("X", settings.get("social", {}).get("x"), "x-social"), ("Instagram", settings.get("social", {}).get("instagram"), "instagram"), ("YouTube", settings.get("social", {}).get("youtube"), "youtube")] if u)}</div>
    </div>
    <form class="card form" method="post" action="/contacto">
      <label for="cf-name">Nombre<input id="cf-name" name="name" type="text" required maxlength="120"></label>
      <label for="cf-email">Correo<input id="cf-email" name="email" type="email" required maxlength="160"></label>
      <label for="cf-msg">Mensaje<textarea id="cf-msg" name="message" rows="5" required maxlength="4000"></textarea></label>
      <input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;opacity:0">
      <button class="btn btn-primary" type="submit">Enviar mensaje {icon("send", 16)}</button>
    </form>
  </div>
</section>'''
    return shell(base, settings, f"{settings.get('siteTitle', BRAND)} — Deportes dominicano",
                 settings.get("heroSubtitle", "Deportes sin filtro"), base + "/", body, jsonld, active="")


CATS = ["Noticias", "Deportes", "Salud y Belleza", "Personalidades Locales", "Comunidad", "Eventos"]


def noticias(base, posts, page=1, cat=None, cat_slug=None):
    if cat:
        posts = [p for p in posts if p.get("category") == cat]
    per = 9
    total = (len(posts) + per - 1) // per or 1
    page = max(1, min(page, total))
    chunk = posts[(page - 1) * per: page * per]
    cards = "".join(card(p, base) for p in chunk) or '<p class="muted">Aún no hay noticias publicadas.</p>'
    pager = "".join(f'<a class="pg{" on" if n == page else ""}" href="/noticias?page={n}">{n}</a>'
                    for n in range(1, total + 1))
    chips = "".join(f'<a class="cat-chip{" on" if c == cat else ""}" href="/categoria/{catslug(c)}">{c}</a>'
                    for c in CATS)
    title = f"{cat} — Noticias" if cat else "Noticias"
    desc = "Todas las noticias y análisis de El Mañanero Deportes" + (f" en la categoría {cat}." if cat else ".")
    canon = base + ("/noticias" if not cat else "/categoria/" + (cat_slug or catslug(cat)))
    body = f'''<section class="section"><div class="wrap">
    <div class="sec-head"><h1 class="sec-title">{icon("newspaper", 24)} {esc(title)}</h1></div>
    <div class="cat-chips">{chips}</div>
    <div class="grid-3">{cards}</div>
    <nav class="pager" aria-label="Páginas">{pager}</nav>
  </div></section>'''
    return shell(base, _s(), title + " — " + BRAND, desc, canon, body, active="noticias")


def post_detail(base, post, posts):
    cover = post.get("cover", "")
    cover_html = f'<img src="{esc(cover)}" alt="">' if cover else ""
    others = [p for p in posts if p["id"] != post["id"]][:3]
    rel = "".join(card(p, base) for p in others)
    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": post["title"], "description": post.get("excerpt", ""),
        "datePublished": post.get("date", ""),
        "articleSection": post.get("category", "Noticias"),
        "author": {"@type": "Person", "name": post.get("author", "Redacción El Mañanero")},
        "publisher": {"@type": "Organization", "name": BRAND},
        "mainEntityOfPage": base + "/noticias/" + post["slug"],
    }, ensure_ascii=False)
    body = f'''<article class="section"><div class="wrap article">
    <nav class="crumbs" aria-label="Ruta"><a href="/noticias">Noticias</a>{icon("chevron-right", 14)}<span>{esc(post["title"])}</span></nav>
    <h1>{esc(post["title"])}</h1>
    <div class="art-meta">{icon("calendar", 15)}<span>{fmt_date(post.get("date", ""))}</span>
      <a class="card-tag" href="/categoria/{catslug(post.get('category', 'Noticias'))}">{esc(post.get('category', 'Noticias'))}</a>
      <span class="art-author">{icon("user", 14)} {esc(post.get('author', 'Redacción El Mañanero'))}</span>
      {"".join(f'<span class="card-tag">{esc(t)}</span>' for t in post.get("tags", []))}</div>
    {f'<div class="art-cover">{cover_html}</div>' if cover else ''}
    <div class="art-body">{render_blocks(post.get("blocks", []))}</div>
    <div class="art-cta"><a class="btn btn-ghost" href="/noticias">{icon("arrow-left", 16)} Volver a noticias</a></div>
  </div></article>
  {f'<section class="section alt"><div class="wrap"><div class="sec-head"><h2 class="sec-title">Sigue leyendo</h2></div><div class="grid-3">{rel}</div></div></section>' if rel else ''}'''
    return shell(base, _s(), f'{post["title"]} — {BRAND}', post.get("excerpt", ""),
                 base + "/noticias/" + post["slug"], body, jsonld, active="noticias")


def videos(base, vids):
    cards = "".join(
        f'''<a class="card vid" href="{base}/noticias/{esc(p["slug"])}">
        <div class="card-media">{f'<img src="{esc(p["cover"])}" alt="" loading="lazy">' if p.get("cover") else f'<div class="card-ph">{icon("play", 40)}</div>'}
        <span class="play-badge">{icon("play", 20)}</span></div>
        <div class="card-body"><h3>{esc(p["title"])}</h3><p class="muted">{esc(p.get("excerpt", ""))[:140]}</p>
        <div class="card-meta">{icon("calendar", 14)}<span>{fmt_date(p.get("date", ""))}</span></div></div></a>'''
        for p in vids) or '<p class="muted">Pronto: primeros videos.</p>'
    body = f'''<section class="section"><div class="wrap">
    <div class="sec-head"><h1 class="sec-title">{icon("video", 24)} Videos</h1></div>
    <div class="grid-3">{cards}</div></div></section>'''
    return shell(base, _s(), "Videos — " + BRAND, "Videos y análisis de El Mañanero Deportes.",
                 base + "/videos", body, active="videos")


def custom_page(base, page, pages):
    body = f'''<section class="section"><div class="wrap article">
    <h1>{esc(page["title"])}</h1>
    <div class="art-body">{render_blocks(page.get("blocks", []))}</div>
  </div></section>'''
    return shell(base, _s(), f'{page["title"]} — {BRAND}', page["title"],
                 base + "/" + page["slug"], body, active=page["slug"])


def contacto(base, settings, ok=False):
    okmsg = ('<div class="form-ok">' + icon("check", 20) +
             '<div><b>¡Mensaje enviado!</b><p>Gracias por escribirnos. Te respondemos muy pronto.</p></div></div>'
             if ok else "")
    body = f'''<section class="section"><div class="wrap contact-grid">
    <div><h1 class="sec-title">{icon("mail", 24)} Contacto</h1>
      <p class="muted">¿Tienes una historia, una pregunta o quieres colaborar con El Mañanero? Escríbenos y te leemos en el próximo programa.</p>
      <ul class="contact-info"><li>{icon("mail", 18)}<span>{esc(settings.get("contactEmail") or "También puedes escribirnos por nuestras redes sociales")}</span></li></ul>
      <div class="social">{"".join(f'<a href="{esc(u)}" target="_blank" rel="noopener noreferrer" aria-label="{n}">{icon(ic, 20)}</a>' for n, u, ic in [("Facebook", settings.get("social", {}).get("facebook"), "facebook"), ("X", settings.get("social", {}).get("x"), "x-social"), ("Instagram", settings.get("social", {}).get("instagram"), "instagram"), ("YouTube", settings.get("social", {}).get("youtube"), "youtube")] if u)}</div>
    </div>
    {okmsg}
    <form class="card form" method="post" action="/contacto">
      <label for="cf-name">Nombre<input id="cf-name" name="name" type="text" required maxlength="120"></label>
      <label for="cf-email">Correo<input id="cf-email" name="email" type="email" required maxlength="160"></label>
      <label for="cf-msg">Mensaje<textarea id="cf-msg" name="message" rows="6" required maxlength="4000"></textarea></label>
      <input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;opacity:0">
      <button class="btn btn-primary" type="submit">Enviar mensaje {icon("send", 16)}</button>
    </form>
  </div></section>'''
    return shell(base, settings, "Contacto — " + BRAND, "Contacta al equipo de El Mañanero Deportes.",
                 base + "/contacto", body, active="contacto")


def not_found():
    return f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Página no encontrada — {BRAND}</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/css/site.css?v=3"></head>
<body class="nf"><main><span class="plate">Error 404</span><h1>Esta jugada no existe</h1>
<p>La página que buscas no está. Vuelve al inicio para seguir en la jugada.</p>
<a class="btn btn-primary" href="/">Volver al inicio</a></main></body></html>'''


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
