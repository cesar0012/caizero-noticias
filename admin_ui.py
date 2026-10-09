#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vistas del panel de administración (CMS)."""
import json

from ui import icon, esc, BRAND
from datetime import datetime


def _fmt_date(iso):
    try:
        return (iso or "")[:10]
    except Exception:
        return ""


# Guía paso a paso por sección (lenguaje llano, para cualquier persona)
TOURS = {
    "dashboard": [
        {"t": "Bienvenido a su panel", "d": "Desde esta pantalla usted controla toda su página web. Nada se rompe: todo lo que escriba se puede editar o borrar después con calma.", "demo": "welcome"},
        {"t": "Para escribir una noticia", "d": "Pulse este botón. Se abre una página para escribir: título, texto, fotos y video.", "demo": "nueva"},
        {"t": "Para editar o borrar", "d": "En el menú de la izquierda pulse «Noticias». Ahí está la lista de todo, con los botones Editar y Eliminar.", "demo": "lista"},
        {"t": "Los mensajes de sus lectores", "d": "Cuando alguien escribe en su página, el mensaje le llega a «Bandeja», en el menú de la izquierda.", "demo": "bandeja"},
        {"t": "Esta guía, siempre a la mano", "d": "Este botón de interrogación abre la guía en cualquier momento. Pulse «Entendido» para empezar.", "demo": "ayuda"},
    ],
    "editor": [
        {"t": "Escriba el título aquí", "d": "Es la casilla grande de arriba. Ejemplo: «Los Timbers ganan su primer partido».", "demo": "titulo"},
        {"t": "Agregue el contenido", "d": "Pulse un botón para agregar un cuadro: +Texto para escribir, +Imagen para una foto, +Video para YouTube. Agrege todos los que quiera.", "demo": "bloques"},
        {"t": "Para cambiar el orden", "d": "Cada cuadro tiene un asa que dice MOVER. Tómela con el mouse y arrastre el cuadro hacia arriba o hacia abajo.", "demo": "mover"},
        {"t": "La categoría y el autor", "d": "Más abajo elija la categoría (Noticias, Deportes…) y escriba quién firma la nota.", "demo": "campos"},
        {"t": "No olvide Guardar", "d": "El botón Guardar está arriba, a la derecha. Púlselo cuando termine. ¡Eso es todo!", "demo": "guardar"},
    ],
    "posts": [
        {"t": "Esta es la lista de sus noticias", "d": "Cada línea es una noticia de su página. Verde significa publicada; gris, borrador (nadie la ve todavía).", "demo": "lista"},
        {"t": "Editar, ver o borrar", "d": "«Editar» abre la noticia para cambiarla. «Ver» la muestra en su página. «Eliminar» la borra: siempre le pediremos confirmar.", "demo": "acciones"},
        {"t": "Para escribir una nueva", "d": "Pulse el botón Nuevo de arriba, a la derecha.", "demo": "nueva"},
    ],
    "pages": [
        {"t": "Páginas fijas del menú", "d": "Las páginas son secciones que siempre aparecen en el menú, como «Nosotros». Se editan igual que las noticias.", "demo": "lista"},
    ],
    "media": [
        {"t": "Subir fotos o videos", "d": "Arrastre el archivo a este recuadro, o pulse «Elegir archivos». Puede subir varios a la vez.", "demo": "media"},
        {"t": "Usar una foto en una noticia", "d": "Pulse «Copiar enlace» y pegue ese enlace en el cuadro Imagen de su noticia. Así de simple.", "demo": "copy"},
    ],
    "inbox": [
        {"t": "Aquí llegan los mensajes", "d": "Todo lo que la gente escriba en la página de Contacto aparece en esta lista, con el nombre y el correo de quien escribió.", "demo": "bandeja"},
        {"t": "Después de leer", "d": "Pulse «Marcar leído» para dejarlo en paz, o «Eliminar» si no quiere guardarlo.", "demo": "acciones"},
    ],
    "settings": [
        {"t": "Su correo de contacto", "d": "Los mensajes del formulario llegarán a este correo. Nota: el primer mensaje pide una activación — abra su correo y pulse el enlace que le llega (solo se hace una vez).", "demo": "campos"},
        {"t": "Sus redes sociales", "d": "Pegue los enlaces de Facebook o Instagram para que aparezcan en su página, arriba y en el pie.", "demo": "campos"},
        {"t": "Cambiar la contraseña", "d": "Más abajo puede poner una contraseña fácil de recordar: 10 o más caracteres, con letras y números.", "demo": "pass"},
    ],
}


def admin_shell(user, csrf, title, body, active="", tour=None):
    nav = [
        ("layout-dashboard", "/admin", "Dashboard", "dashboard"),
        ("file-text", "/admin/posts", "Noticias", "posts"),
        ("file-text", "/admin/pages", "Páginas", "pages"),
        ("image", "/admin/media", "Multimedia", "media"),
        ("inbox", "/admin/inbox", "Bandeja", "inbox"),
        ("settings", "/admin/settings", "Ajustes", "settings"),
    ]
    nav_html = "".join(
        f'<a href="{u}" class="anav{" on" if a == active else ""}">{icon(ic, 18)}<span>{t}</span></a>'
        for ic, u, t, a in [(ic, u, t, active) for ic, u, t, a in nav])
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — Admin {BRAND}</title>
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/admin.css?v=4">
<script>window.CSRF = {json.dumps(csrf) if False else repr(csrf)};</script>
<script>window.__TOUR = {json.dumps(TOURS.get(tour or active, []), ensure_ascii=False)};</script>
</head>
<body class="admin">
<div class="admin-shell">
  <aside class="aside">
    <a class="abrand" href="/admin"><img src="/img/mark.png" alt="" width="34" height="34"><span><b>El Mañanero</b><i>Deportes</i></span></a>
    <nav class="anav-list">{nav_html}</nav>
    <div class="aside-foot">
      <a href="/" target="_blank" rel="noopener noreferrer" class="anav">{icon("eye", 18)}<span>Ver sitio</span></a>
      <a href="/admin/logout" class="anav out">{icon("log-out", 18)}<span>Salir</span></a>
      <div class="auser">{icon("user", 16)}<span>{esc(user)}</span></div>
    </div>
  </aside>
  <main class="amain">{body}</main>
</div>
<button class="help-fab" id="helpBtn" aria-label="Ayuda: guía paso a paso" title="Guía paso a paso">{icon("help-circle", 26)}<span class="help-fab-txt">Ayuda</span></button>
<div class="tour" id="tour" hidden>
  <div class="tour-scrim" data-tour-close></div>
  <div class="tour-card" role="dialog" aria-modal="true" aria-label="Guía paso a paso">
    <div class="tour-head">
      <span class="tour-step-num" data-tour-num></span>
      <button class="icon-btn" data-tour-close aria-label="Cerrar la guía">{icon("x", 20)}</button>
    </div>
    <div class="tour-demo" data-tour-demo hidden></div>
    <h2 class="tour-title" data-tour-title></h2>
    <p class="tour-text" data-tour-text></p>
    <div class="tour-dots" data-tour-dots aria-hidden="true"></div>
    <div class="tour-actions">
      <button class="btn ghost" data-tour-prev type="button">{icon("arrow-left", 16)} Atrás</button>
      <button class="btn primary" data-tour-next type="button">Siguiente {icon("arrow-right", 16)}</button>
    </div>
  </div>
</div>
<script src="/js/admin.js?v=6" defer></script>
</body>
</html>'''


def admin_login(error=""):
    err = f'<div class="alert err">{icon("x", 18)}<span>{esc(error)}</span></div>' if error else ""
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Entrar — Admin {BRAND}</title><meta name="robots" content="noindex, nofollow">
<link rel="icon" href="/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/admin.css?v=3">
</head>
<body class="admin login-page">
<main class="login-card">
  <div class="login-brand"><img src="/img/mark.png" alt="" width="72" height="72"><span><b>El Mañanero</b><i>Deportes</i></span></div>
  <h1>Panel de administración</h1>
  <p class="login-hint">Escriba su usuario y su contraseña para entrar.</p>
  {err}
  <form method="post" action="/admin/login">
    <label>Usuario
      <div class="inwrap">{icon("user", 17)}<input name="u" type="text" required autocomplete="username" autofocus></div>
    </label>
    <label>Contraseña
      <div class="inwrap">{icon("key", 17)}<input name="p" type="password" required autocomplete="current-password"></div>
    </label>
    <button class="btn primary w100" type="submit">Entrar {icon("chevron-right", 16)}</button>
  </form>
  <a class="back" href="/">{icon("arrow-left", 14)} Volver al sitio</a>
</main>
</body></html>'''


def stat_card(icon_name, value, label):
    return (f'<div class="stat">{icon(icon_name, 22)}<b>{value}</b><span>{label}</span></div>')


def admin_home(user, csrf, data):
    posts = data["posts"]
    pub = [p for p in posts if p.get("status") == "published"]
    drafts = [p for p in posts if p.get("status") != "published"]
    unread = [m for m in data["inbox"] if not m.get("read")]
    recent = sorted(posts, key=lambda p: p.get("date", ""), reverse=True)[:5]
    rows = "".join(
        f'''<tr><td>{esc(p["title"])}</td>
        <td><span class="badge {"pub" if p.get("status") == "published" else "draft"}">{"Publicado" if p.get("status") == "published" else "Borrador"}</span></td>
        <td class="row-actions"><a class="mini" href="/admin/editor/{p["id"]}">{icon("pencil", 15)} Editar</a></td></tr>'''
        for p in recent)
    body = f'''
    <header class="ahead"><h1>Hola, {esc(user)}</h1>
      <div class="ahead-actions"><a class="btn ghost" href="/admin/pages/editor/new">{icon("plus", 16)} Nueva página</a></div></header>

    <a class="start-hero" href="/admin/editor/new">
      <span class="start-hero-ic">{icon("pencil", 30)}</span>
      <span class="start-hero-txt"><b>Escribir una noticia nueva</b>
      <small>Título, texto, fotos y video. Al final, pulse Guardar y aparecerá en su página.</small></span>
      {icon("arrow-right", 22)}
    </a>

    <div class="start-grid">
      <a class="start-card" href="/admin/posts">
        {icon("file-text", 24)}<b>Mis noticias</b>
        <p>{len(pub)} publicadas · {len(drafts)} borradores<br>Editar, ver o borrar</p>
      </a>
      <a class="start-card" href="/admin/inbox">
        {icon("message", 24)}<b>Mensajes</b>
        <p>{"Tiene " + str(len(unread)) + " sin leer" if unread else "No tiene mensajes nuevos"}<br>De quienes escriben en Contacto</p>
        {('<span class="bubble">' + str(len(unread)) + "</span>") if unread else ""}
      </a>
      <a class="start-card" href="/admin/settings">
        {icon("settings", 24)}<b>Mi contraseña y redes</b>
        <p>Cambiar la clave<br>Poner mis redes sociales</p>
      </a>
    </div>

    <section class="panel">
      <h2>{icon("lightbulb", 18)} Toda noticia tiene 3 partes</h2>
      <div class="steps3">
        <div class="step3"><span>1</span><b>Escriba el título</b><p>En la casilla grande de arriba.</p></div>
        <div class="step3"><span>2</span><b>Agregue lo que quiera contar</b><p>Con los botones +Texto, +Imagen y +Video.</p></div>
        <div class="step3"><span>3</span><b>Pulse Guardar</b><p>Arriba, a la derecha. ¡Y listo!</p></div>
      </div>
    </section>

    <section class="panel">
      <h2>Sus últimas noticias</h2>
      <table class="tbl"><thead><tr><th>Título</th><th>Estado</th><th></th></tr></thead>
      <tbody>{rows or '<tr><td colspan="3" class="muted">Aún no hay noticias. La primera puede ser hoy.</td></tr>'}</tbody></table>
      <p class="panel-foot"><a class="btn ghost" href="/admin/posts">{icon("arrow-right", 15)} Ver todas</a></p>
    </section>'''
    return admin_shell(user, csrf, "Inicio", body, "dashboard")


def admin_posts(user, csrf, data):
    rows = "".join(
        f'''<tr data-title="{esc(p["title"]).lower()}">
        <td>{esc(p["title"])}{' ' + icon("video", 15) if p.get("kind") == "video" else ''}</td>
        <td><span class="badge {"pub" if p.get("status") == "published" else "draft"}">{'Publicado' if p.get('status') == 'published' else 'Borrador'}</span></td>
        <td>{_fmt_date(p.get('date'))}</td>
        <td class="row-actions">
          <a class="mini" href="/admin/editor/{p['id']}">{icon('pencil', 15)} Editar</a>
          <a class="mini" href="/noticias/{p['slug']}" target="_blank" rel="noopener">{icon('eye', 15)} Ver</a>
          <button class="mini danger" data-del data-id="{p['id']}" data-kind="post">{icon('trash-2', 15)} Eliminar</button>
        </td></tr>'''
        for p in sorted(data["posts"], key=lambda p: p.get("date", ""), reverse=True))
    body = f'''
    <header class="ahead"><h1>Noticias</h1>
      <div class="ahead-actions"><input id="qa-filter" class="in" type="search" placeholder="Buscar por título…" aria-label="Buscar">
      <a class="btn primary" href="/admin/editor/new">{icon("plus", 16)} Nueva</a></div></header>
    <p class="page-sub">Aquí están todas sus noticias. Con <b>Editar</b> las cambia; con <b>Eliminar</b> las borra (le pediremos confirmar).</p>
    <section class="panel"><table class="tbl"><thead><tr><th>Título</th><th>Estado</th><th>Fecha</th><th>Acciones</th></tr></thead>
    <tbody id="qa-rows">{rows or '<tr><td colspan="4" class="muted">Sin noticias todavía.</td></tr>'}</tbody></table></section>'''
    return admin_shell(user, csrf, "Noticias", body, "posts")


def admin_pages(user, csrf, data):
    rows = "".join(
        f'''<tr><td>{esc(p["title"])}</td>
        <td>/{esc(p["slug"])}</td>
        <td><span class="badge {"pub" if p.get("status") == "published" else "draft"}">{'Publicado' if p.get('status') == 'published' else 'Borrador'}</span></td>
        <td class="row-actions">
          <a class="mini" href="/admin/pages/editor/{p['id']}">{icon('pencil', 15)} Editar</a>
          <a class="mini" href="/{p['slug']}" target="_blank" rel="noopener">{icon('eye', 15)} Ver</a>
          <button class="mini danger" data-del data-id="{p['id']}" data-kind="page">{icon('trash-2', 15)} Eliminar</button>
        </td></tr>'''
        for p in sorted(data["pages"], key=lambda p: p.get("title", "")))
    body = f'''
    <header class="ahead"><h1>Páginas</h1>
      <div class="ahead-actions"><a class="btn primary" href="/admin/pages/editor/new">{icon("plus", 16)} Nueva página</a></div></header>
    <section class="panel"><table class="tbl"><thead><tr><th>Título</th><th>URL</th><th>Estado</th><th>Acciones</th></tr></thead>
    <tbody>{rows or '<tr><td colspan="4" class="muted">Sin páginas.</td></tr>'}</tbody></table></section>'''
    return admin_shell(user, csrf, "Páginas", body, "pages")


BLOCK_TYPES = [
    ("h", "Subtítulo", "heading"),
    ("p", "Texto", "align-left"),
    ("img", "Imagen", "image"),
    ("video", "Video", "video"),
    ("q", "Cita", "quote"),
]


def admin_editor(user, csrf, kind, item):
    is_post = kind == "post"
    item = item or {}
    title = item.get("title", "")
    back = "/admin/posts" if is_post else "/admin/pages"
    back_label = "Noticias" if is_post else "Páginas"
    cat_opts = "".join(
        f'<option{" selected" if c == item.get("category", "Noticias") else ""}>{c}</option>'
        for c in ["Noticias", "Deportes", "Salud y Belleza", "Personalidades Locales", "Comunidad", "Eventos"])
    meta_rows = ""
    if is_post:
        meta_rows = f'''
      <label>Resumen <span class="hint">(una o dos frases; aparece bajo el título en su página)</span>
        <textarea name="excerpt" rows="2" maxlength="400" placeholder="Escriba aquí un resumen corto…">{esc(item.get("excerpt", ""))}</textarea></label>
      <label>Foto principal <span class="hint">(suba una foto o pegue su enlace)</span>
        <div class="cover-row"><input name="cover" type="text" value="{esc(item.get("cover", ""))}" placeholder="https://… o sube una imagen">
        <label class="btn ghost upl">{icon("upload", 15)} Subir<input type="file" data-upload hidden accept="image/*"></div></label>
        <div class="cover-preview">{'<img src="' + esc(item.get("cover", "")) + '" alt="">' if item.get("cover") else ''}</div>
      <label>Categoría
        <select name="category">{cat_opts}</select></label>
      <label>¿Quién lo escribe? <span class="hint">(su nombre o el del programa)</span>
        <input name="author" type="text" value="{esc(item.get("author", "Redacción El Mañanero"))}" placeholder="Redacción El Mañanero"></label>
      <label>Etiquetas (separadas por coma)
        <input name="tags" type="text" value="{esc(', '.join(item.get("tags", [])))}" placeholder="LIDOM, Béisbol, Selección"></label>
      <label class="chk"><input type="checkbox" name="featured" {'checked' if item.get('featured') else ''}> Destacar en el inicio</label>
      <label class="chk"><input type="checkbox" name="isVideo" {'checked' if item.get('kind') == 'video' else ''}> Es un video (aparece en la sección Videos)</label>'''
    else:
        meta_rows = f'''
      <label class="chk"><input type="checkbox" name="inNav" {'checked' if item.get('inNav', True) else ''}> Mostrar en el menú del sitio</label>
      <label>Orden en el menú<input name="navOrder" type="number" value="{item.get('navOrder', 90)}" min="1" max="99"></label>'''
    body = f'''
    <header class="ahead"><a class="mini" href="{back}">{icon("arrow-left", 15)} {back_label}</a>
      <div class="ahead-actions">
        <span class="save-state" data-savestate></span>
        <button class="mini danger" data-del data-id="{item.get('id', '')}" data-kind="{kind}" {'hidden' if not item else ''}>{icon("trash-2", 15)} Eliminar</button>
        <button class="btn primary" data-save>{icon("save", 16)} Guardar</button>
      </div></header>
    <div class="editor" data-kind="{kind}">
      <input type="hidden" name="id" value="{item.get('id', '')}">
      <section class="panel">
        <input class="title-in" name="title" type="text" placeholder="Título de la {'nota' if is_post else 'página'}"
               value="{esc(title)}" required maxlength="200">
        <div class="meta-grid">
          <label>Enlace web <span class="hint">(se llena solo — no necesita tocarlo)</span><input name="slug" type="text" value="{esc(item.get('slug', ''))}" placeholder="se-genera-del-titulo"></label>
          {meta_rows}
          <label>Estado
            <select name="status">
              <option value="published" {'selected' if item.get('status') == 'published' else ''}>Publicado</option>
              <option value="draft" {'selected' if item.get('status') != 'published' else ''}>Borrador</option>
            </select></label>
        </div>
      </section>
      <section class="panel blocks-panel">
        <div class="blk-head"><h2>Contenido</h2>
          <div class="add-bar">{"".join(f'<button type="button" class="mini" data-add="{t}">{icon(ic2, 15)} {lbl}</button>' for t, lbl, ic2 in BLOCK_TYPES)}</div>
        </div>
        <p class="panel-help">{icon("lightbulb", 16)} Para agregar un cuadro nuevo, pulse uno de los botones de arriba. Para cambiar el orden, tome el asa <b>MOVER</b> y arrastre. Al terminar, pulse <b>Guardar</b>.</p>
        <div class="blocks" data-blocks></div>
      </section>
    </div>
    <script>window.__ITEM = {json.dumps(item, ensure_ascii=False)}; window.__KIND = {kind!r};</script>'''
    return admin_shell(user, csrf, ("Editar " if item else "Nueva ") + ("noticia" if is_post else "página"), body,
                       "posts" if is_post else "pages", tour="editor")


def admin_media(user, csrf, files):
    cards = ""
    for f in files:
        url = "/uploads/" + f
        is_vid = f.lower().endswith((".mp4", ".webm"))
        thumb = (f'<video src="{url}" muted preload="metadata"></video>' if is_vid
                 else f'<img src="{url}" alt="" loading="lazy">')
        cards += f'''<div class="media-card">{thumb}
        <div class="media-meta"><span>{f[:22]}</span>
        <div class="row-actions"><button class="mini" data-copy="{url}">{icon("copy", 14)} Copiar enlace</button>
        <form method="post" action="/admin/media/delete"><input type="hidden" name="_csrf" value="{esc(csrf)}">
        <input type="hidden" name="file" value="{esc(f)}"><button class="mini danger" type="submit">{icon("trash-2", 14)}</button></form></div></div></div>'''
    body = f'''
    <header class="ahead"><h1>Multimedia</h1></header>
    <section class="panel">
      <div class="dropzone" data-drop>{icon("upload", 30)}
        <p><b>Arrastra imágenes o videos aquí</b> o</p>
        <label class="btn primary">{icon("upload", 16)} Elegir archivos<input type="file" multiple hidden accept="image/*,video/mp4,video/webm"></label>
        <p class="muted small">JPG, PNG, WebP, GIF, MP4, WebM · hasta 220 MB por archivo</p>
      </div>
      <div class="media-grid">{cards or '<p class="muted">Todavía no hay archivos. Sube el primero.</p>'}</div>
    </section>'''
    return admin_shell(user, csrf, "Multimedia", body, "media")


def admin_inbox(user, csrf, data):
    msgs = data["inbox"]
    items = "".join(
        f'''<div class="msg{" unread" if not m.get("read") else ""}">
        <div class="msg-head"><b>{esc(m.get("name", ""))}</b>
          <a href="mailto:{esc(m.get("email", ""))}">{esc(m.get("email", ""))}</a>
          <span class="muted">{esc((m.get("date") or "")[:16].replace("T", " "))}</span></div>
        <p>{esc(m.get("message", ""))}</p>
        <div class="row-actions">
          {'<form method="post" action="/admin/inbox/read"><input type="hidden" name="_csrf" value="' + esc(csrf) + '"><input type="hidden" name="id" value="' + m["id"] + '"><button class="mini" type="submit">' + icon("check", 14) + ' Marcar leído</button></form>' if not m.get("read") else '<span class="mini ok">' + icon("check", 14) + ' Leído</span>'}
          <form method="post" action="/admin/inbox/delete"><input type="hidden" name="_csrf" value="{esc(csrf)}"><input type="hidden" name="id" value="{m["id"]}"><button class="mini danger" type="submit">{icon("trash-2", 14)} Eliminar</button></form>
        </div></div>'''
        for m in msgs)
    body = f'''
    <header class="ahead"><h1>Mensajes</h1><span class="badge pub">{len(msgs)} en total</span></header>
    <p class="page-sub">Todos los mensajes que la gente envía en la página de Contacto llegan aquí. Nada se pierde.</p>
    <section class="panel">{items or '<p class="muted">Sin mensajes por ahora. Los del formulario de contacto llegan aquí.</p>'}</section>'''
    return admin_shell(user, csrf, "Bandeja", body, "inbox")


def admin_settings(user, csrf, data, error=None):
    s = data["settings"]
    social = s.get("social", {})
    banner = f'<div class="alert err">{icon("x", 18)}<span>{esc(error)}</span></div>' if error else ""
    body = f'''
    <header class="ahead"><h1>Ajustes</h1></header>
    <p class="page-sub">Cambie lo que quiera y pulse Guardar al final de cada sección.</p>
    {banner}
    <section class="panel">
      <h2>Inicio y marca</h2>
      <form method="post" action="/admin/settings/site" class="settings-form">
        <input type="hidden" name="_csrf" value="{esc(csrf)}">
        <label>Nombre del sitio<input name="siteTitle" type="text" value="{esc(s.get('siteTitle', ''))}" required></label>
        <label>Frase corta (bajo el logo y en el pie)<input name="tagline" type="text" value="{esc(s.get('tagline', ''))}"></label>
        <label>Título grande del inicio<input name="heroTitle" type="text" value="{esc(s.get('heroTitle', ''))}"></label>
        <label>Subtítulo del inicio<textarea name="heroSubtitle" rows="2">{esc(s.get('heroSubtitle', ''))}</textarea></label>
        <label>Imagen de fondo del inicio (URL o subir en Multimedia)<input name="heroImage" type="text" value="{esc(s.get('heroImage', ''))}" placeholder="/uploads/…"></label>
        <h2 class="mt">Correo de contacto</h2>
        <label>Los mensajes del formulario también se reenvían a este correo<input name="contactEmail" type="email" value="{esc(s.get('contactEmail', ''))}" placeholder="contacto@tudominio.com"></label>
        <h2 class="mt">Redes sociales</h2>
        <div class="meta-grid">
          <label>Facebook<input name="social_facebook" type="url" value="{esc(social.get('facebook', ''))}" placeholder="https://facebook.com/…"></label>
          <label>X (Twitter)<input name="social_x" type="url" value="{esc(social.get('x', ''))}" placeholder="https://x.com/…"></label>
          <label>Instagram<input name="social_instagram" type="url" value="{esc(social.get('instagram', ''))}" placeholder="https://instagram.com/…"></label>
          <label>YouTube<input name="social_youtube" type="url" value="{esc(social.get('youtube', ''))}" placeholder="https://youtube.com/@…"></label>
        </div>
        <button class="btn primary" type="submit">{icon("save", 16)} Guardar ajustes</button>
      </form>
    </section>
    <section class="panel">
      <h2>Cambiar contraseña</h2>
      <form method="post" action="/admin/settings/password" class="settings-form">
        <input type="hidden" name="_csrf" value="{esc(csrf)}">
        <label>Contraseña actual<div class="inwrap">{icon("key", 16)}<input name="current" type="password" required autocomplete="current-password"></div></label>
        <label>Nueva contraseña (10+ caracteres, letras y números)<div class="inwrap">{icon("key", 16)}<input name="new" type="password" required minlength="10" autocomplete="new-password"></div></label>
        <button class="btn primary" type="submit">{icon("key", 16)} Actualizar contraseña</button>
      </form>
    </section>'''
    return admin_shell(user, csrf, "Ajustes", body, "settings")
