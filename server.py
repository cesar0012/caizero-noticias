#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EL MAÑANERO DEPORTES — servidor del sitio + CMS
Un solo contenedor, cero dependencias externas (solo stdlib de Python 3.12).
- Base de datos NoSQL embebida: documento JSON en data/store.json (escritura atómica)
- Admin en /admin con login (PBKDF2-SHA256), sesiones firmadas HMAC, CSRF, rate-limit
- Formularios de contacto guardados en el inbox del admin (+ relay opcional FormSubmit)
- SEO: render del servidor, canonical/OG por página, sitemap.xml, robots.txt, rss.xml
"""
import base64
import hashlib
import hmac
import html
import json
import mimetypes
import os
import re
import secrets
import threading
import time
import uuid
from datetime import datetime, timedelta, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import ui

# ----------------------------------------------------------------------------
# Configuración
# ----------------------------------------------------------------------------
PORT = int(os.environ.get("PORT", "8080"))
BASE_URL = os.environ.get("BASE_URL", "").rstrip("/")
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "").strip()  # relay FormSubmit opcional
DATA_DIR = os.environ.get("DATA_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"))
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads"))
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

STORE_PATH = os.path.join(DATA_DIR, "store.json")
SECRET_PATH = os.path.join(DATA_DIR, "secret.key")
SESSION_TTL = 60 * 60 * 12          # 12 h
CATEGORIES = ["Noticias", "Deportes", "Salud y Belleza", "Personalidades Locales", "Comunidad", "Eventos"]
MAX_UPLOAD = 220 * 1024 * 1024      # 220 MB
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".mp4", ".webm", ".m4a", ".mp3"}

_lock = threading.Lock()
_login_fails = {}   # ip -> [fails, lock_until]


# ----------------------------------------------------------------------------
# Secret + store
# ----------------------------------------------------------------------------
def load_secret() -> bytes:
    if os.path.exists(SECRET_PATH):
        return bytes.fromhex(open(SECRET_PATH, encoding="utf-8").read().strip())
    key = secrets.token_hex(64)
    fd = open(SECRET_PATH, "x", encoding="utf-8")
    fd.write(key)
    fd.close()
    os.chmod(SECRET_PATH, 0o600)
    return key.encode()


SECRET = load_secret()

DEFAULT_SETTINGS = {
    "siteTitle": "El Mañanero con Caizero",
    "ad1Media": "/img/pub-filler-top.png",
    "ad1Link": "",
    "ad2Media": "/img/pub-filler-rail.png",
    "ad2Link": "",
    "tagline": "El análisis deportivo que despierta contigo.",
    "heroTitle": "Deportes sin filtro, todas las mañanas",
    "heroSubtitle": "Noticias, opinión y video del deporte dominicano y del mundo. Directo, sin rodeos y con la pasión que el juego merece.",
    "heroImage": "",
    "contactEmail": CONTACT_EMAIL,
    "social": {"facebook": "https://www.facebook.com/elsolmananero", "x": "",
              "instagram": "https://www.instagram.com/elsolmananero", "youtube": ""},
}


def first_run_store():
    """Store inicial: ajustes, usuario admin y contenido de bienvenida."""
    password = os.environ.get("ADMIN_PASSWORD") or (
        "Mnr-" + secrets.token_urlsafe(9))
    users = [{
        "id": uuid.uuid4().hex[:10],
        "username": "admin",
        "hash": hash_password(password),
    }]
    if not os.environ.get("ADMIN_PASSWORD"):
        with open(os.path.join(DATA_DIR, "first_password.txt"), "w", encoding="utf-8") as fh:
            fh.write(password + "\n")
        print("=" * 62)
        print("PRIMER INICIO — contraseña del admin:", password)
        print("(guardada también en data/first_password.txt — cámbiala en Ajustes)")
        print("=" * 62)
    else:
        print("Admin creado con la contraseña de ADMIN_PASSWORD.")
    return {
        "posts": [
            {
                "id": uuid.uuid4().hex[:10], "kind": "post",
                "title": "Bienvenidos a El Mañanero",
                "slug": "bienvenidos-a-el-mananero-deportes",
                "excerpt": "Arrancamos con todo: noticias, opinión y video del deporte dominicano y del mundo, todas las mañanas.",
                "cover": "", "category": "Noticias", "author": "Redacción El Mañanero", "tags": ["El Mañanero"], "status": "published",
                "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "featured": False,
                "blocks": [
                    {"t": "p", "text": "Arranca El Mañanero Deportes: el espacio donde el deporte dominicano se analiza sin filtros, con datos, opinión y la pasión que el juego merece."},
                    {"t": "h", "text": "¿Qué vas a encontrar aquí?"},
                    {"t": "p", "text": "Coberturas, análisis, video y reacciones de béisbol, baloncesto, fútbol y todo lo que mueva la pizarra. Publicamos todas las mañanas y también en nuestras redes."},
                    {"t": "q", "text": "El deporte se vive mejor cuando se conversa.", "by": "Equipo El Mañanero"},
                ],
            },
            {
                "id": uuid.uuid4().hex[:10], "kind": "post",
                "title": "Ejemplo: nota deportiva (editar o eliminar)",
                "slug": "ejemplo-nota-deportiva",
                "excerpt": "Ejemplo de nota para que veas la estructura: título, resumen, portada y bloques de contenido.",
                "cover": "", "category": "Deportes", "author": "Redacción El Mañanero", "tags": ["Ejemplo"], "status": "draft",
                "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "featured": False,
                "blocks": [
                    {"t": "p", "text": "Esta es una nota de ejemplo. Edítala o elimínala desde el panel: Noticias → Editar."},
                    {"t": "img", "src": "", "alt": "", "cap": ""},
                    {"t": "p", "text": "Los bloques se pueden arrastrar para reordenar y se pueden mezclar textos, imágenes y videos."},
                ],
            },
        ],
        "pages": [
            {
                "id": uuid.uuid4().hex[:10], "title": "Nosotros", "slug": "nosotros",
                "status": "published", "inNav": True, "navOrder": 90,
                "blocks": [
                    {"t": "h", "text": "El Mañanero Deportes"},
                    {"t": "p", "text": "Somos el programa deportivo que acompaña tus mañanas: análisis, entrevista y la conversación del deporte dominicano e internacional. Esta página la puedes editar desde el panel en Páginas → Nosotros."},
                ],
            },
        ],
        "inbox": [],
        "settings": dict(DEFAULT_SETTINGS),
        "users": users,
    }


_store = None
_store_lock = threading.RLock()


def store():
    global _store
    with _store_lock:
        if _store is None:
            if os.path.exists(STORE_PATH):
                with open(STORE_PATH, encoding="utf-8") as fh:
                    _store = json.load(fh)
                for k, v in DEFAULT_SETTINGS.items():
                    _store["settings"].setdefault(k, v)
                # sanear: eliminar entradas dañadas por crashes previos
                for key in ("posts", "pages"):
                    clean = []
                    for item in _store.get(key, []):
                        if not isinstance(item, dict) or not item.get("id") or not item.get("title"):
                            continue
                        if not item.get("slug"):
                            item["slug"] = slugify(item["title"]) + "-" + item["id"][:4]
                        item.setdefault("blocks", [])
                        item.setdefault("status", "draft")
                        item.setdefault("date", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
                        item.setdefault("category", "Noticias")
                        item.setdefault("author", "Redacción El Mañanero")
                        clean.append(item)
                    _store[key] = clean
                _store.setdefault("inbox", [])
                _store.setdefault("users", [])
            else:
                _store = first_run_store()
                try:
                    import seed
                    seed.enrich(_store)
                except Exception as e:
                    print("[seed] contenido demo no disponible:", e)
                save_store(_store)
        return _store


def save_store(data):
    tmp = STORE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, STORE_PATH)


def mut(fn):
    """Mutación atómica del store bajo lock."""
    with _store_lock:
        data = store()
        result = fn(data)
        save_store(data)
        return result


# ----------------------------------------------------------------------------
# Passwords + sesiones + CSRF
# ----------------------------------------------------------------------------
def hash_password(pw: str, salt: str = None) -> str:
    salt = salt or secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt.encode(), 200_000)
    return f"pbkdf2${salt}${dk.hex()}"


def check_password(pw: str, stored: str) -> bool:
    try:
        _, salt, dk = stored.split("$")
        return hmac.compare_digest(hash_password(pw, salt), stored)
    except Exception:
        return False


def sign(payload: str) -> str:
    key = SECRET if isinstance(SECRET, bytes) else str(SECRET).encode()
    return hmac.new(key, payload.encode(), hashlib.sha256).hexdigest()[:32]


def make_session(username: str) -> str:
    payload = json.dumps({"u": username, "exp": int(time.time()) + SESSION_TTL,
                          "t": secrets.token_hex(8)})
    b64 = base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
    return b64 + "." + sign(b64)


def read_session(token: str):
    try:
        b64, sig = token.split(".")
        if not hmac.compare_digest(sign(b64), sig):
            return None
        pad = "=" * (-len(b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(b64 + pad))
        if payload.get("exp", 0) < time.time():
            return None
        return payload
    except Exception:
        return None


def csrf_token(token: str) -> str:
    return sign("csrf:" + token)[:32]


def verify_csrf(token: str, supplied: str) -> bool:
    return hmac.compare_digest(csrf_token(token), supplied or "")


def current_user(headers) -> str | None:
    raw = headers.get("Cookie", "")
    m = re.search(r"mnr_s=([^;]+)", raw)
    if not m:
        return None
    sess = read_session(m.group(1))
    return sess.get("u") if sess else None


def current_session(headers):
    raw = headers.get("Cookie", "")
    m = re.search(r"mnr_s=([^;]+)", raw)
    return m.group(1) if m else None


# ----------------------------------------------------------------------------
# Utilidades de contenido
# ----------------------------------------------------------------------------
def slugify(text: str) -> str:
    text = text.lower()
    repl = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ü": "u", "ñ": "n"}
    text = "".join(repl.get(c, c) for c in text)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:70] or "post"


def unique_slug(kind: str, slug: str, exclude_id: str = "") -> str:
    base, n = slug, 2
    items = store()["posts" if kind == "post" else "pages"]
    while any(p.get("slug") == slug and p["id"] != exclude_id for p in items):
        slug = f"{base}-{n}"
        n += 1
    return slug


def published_posts():
    return [p for p in store()["posts"] if p.get("status") == "published"]


def sorted_posts():
    return sorted(published_posts(), key=lambda p: p.get("date", ""), reverse=True)


def published_pages():
    return sorted([p for p in store()["pages"] if p.get("status") == "published"],
                  key=lambda p: p.get("navOrder", 99))


def base_url(host: str) -> str:
    return BASE_URL or f"http://{host}"


# ----------------------------------------------------------------------------
# Servidor HTTP
# ----------------------------------------------------------------------------
class Handler(SimpleHTTPRequestHandler):
    server_version = "MananeroServer/1.0"

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=os.path.dirname(os.path.abspath(__file__)), **kw)

    def log_message(self, fmt, *args):
        print("[http]", self.command, self.path)

    # ---------------- helpers ----------------
    def cookie(self, name, value, max_age):
        return f"Set-Cookie: {name}={value}; Path=/; Max-Age={max_age}; HttpOnly; SameSite=Lax"

    def send_html(self, body, status=200, extra=""):
        body_b = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body_b)))
        # el panel admin nunca se cachea; el sitio público revalida
        self.send_header("Cache-Control", "no-store" if self.path.startswith("/admin") else "no-cache")
        for h, v in self._sec_headers():
            self.send_header(h, v)
        if extra:
            for h, v in [extra] if isinstance(extra, tuple) else extra:
                self.send_header(h, v)
        self.end_headers()
        self.wfile.write(body_b)

    def send_json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def redirect(self, location, cookie=None):
        self.send_response(303)
        self.send_header("Location", location)
        if cookie:
            self.send_header(*cookie)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _sec_headers(self):
        headers = [
            ("X-Content-Type-Options", "nosniff"),
            ("X-Frame-Options", "SAMEORIGIN"),
            ("Referrer-Policy", "strict-origin-when-cross-origin"),
        ]
        if os.environ.get("DEMO") == "1":
            # preview/demo: fuera de índice y sin caché (LINEAMIENTOS 3.2/5)
            headers.append(("X-Robots-Tag", "noindex, nofollow"))
            headers.append(("Cache-Control", "no-store"))
        return headers

    def read_body(self) -> bytes:
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_UPLOAD:
            raise ValueError("Body demasiado grande")
        return self.rfile.read(length)

    def body_form(self, body: bytes) -> dict:
        return {k: v[0] for k, v in parse_qs(body.decode("utf-8"), keep_blank_values=True).items()}

    def admin_guard(self):
        """Devuelve (user, session, csrf) o None si no hay sesión válida."""
        sess = current_session(self.headers)
        if not sess:
            return None
        s = read_session(sess)
        if not s:
            return None
        return s.get("u"), sess, csrf_token(sess)

    # ---------------- GET ----------------
    def do_GET(self):
        path = urlparse(self.path).path
        qs = parse_qs(urlparse(self.path).query)

        if path == "/healthz":
            return self.send_json({"ok": True})

        if path.startswith("/uploads/"):
            return self.serve_upload(path)

        if path == "/sitemap.xml":
            return self.send_html(ui.sitemap(base_url(self.headers.get("Host", "localhost")), store()), 200,
                                  ("Content-Type", "application/xml; charset=utf-8"))
        if path == "/robots.txt":
            host = self.headers.get("Host", "localhost")
            body = f"User-agent: *\nAllow: /\nDisallow: /admin\n\nSitemap: {base_url(host)}/sitemap.xml\n"
            return self.send_html(body, 200, ("Content-Type", "text/plain; charset=utf-8"))
        if path == "/rss.xml":
            return self.send_html(ui.rss(base_url(self.headers.get("Host", "localhost")), sorted_posts()), 200,
                                  ("Content-Type", "application/rss+xml; charset=utf-8"))

        if path == "/admin/login":
            return self.send_html(ui.admin_login())
        if path == "/admin/logout":
            tok = current_session(self.headers)
            return self.redirect("/admin/login",
                                 ("Set-Cookie", f"mnr_s=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax"))
        if path == "/admin" or path.startswith("/admin/"):
            if path == "/admin/login":
                return None
            guard = self.admin_guard()
            if not guard:
                return self.redirect("/admin/login")
            return self.admin_get(path, qs, guard)

        if path == "/":
            posts = sorted_posts()
            s = store()["settings"]
            return self.send_html(ui.home(base_url(self.headers.get("Host", "localhost")), s, posts))

        if path == "/noticias":
            page = int(qs.get("page", ["1"])[0] or 1)
            return self.send_html(ui.noticias(base_url(self.headers.get("Host", "localhost")), sorted_posts(), page))

        m = re.match(r"^/noticias/([\w-]+)$", path)
        if m:
            post = next((p for p in published_posts() if p["slug"] == m.group(1)), None)
            if not post:
                return self.send_html(ui.not_found(), 404)
            return self.send_html(ui.post_detail(base_url(self.headers.get("Host", "localhost")), post,
                                                 sorted_posts()))

        if path == "/videos":
            vids = [p for p in sorted_posts() if p.get("kind") == "video" or
                    any(b.get("t") == "video" for b in p.get("blocks", []))]
            return self.send_html(ui.videos(base_url(self.headers.get("Host", "localhost")), vids))

        m = re.match(r"^/categoria/([\w-]+)$", path)
        if m:
            cat = next((c for c in CATEGORIES if slugify(c) == m.group(1)), None)
            if not cat:
                return self.send_html(ui.not_found(), 404)
            posts = [p for p in sorted_posts() if p.get("category") == cat]
            return self.send_html(ui.noticias(base_url(self.headers.get("Host", "localhost")),
                                              posts, cat=cat, cat_slug=m.group(1)))

        if path == "/contacto":
            return self.send_html(ui.contacto(base_url(self.headers.get("Host", "localhost")),
                                              store()["settings"], ok=("ok" in qs)))

        if path == "/contactar" or path == "/contacto/":
            return self.redirect("/contacto")

        # página personalizada publicada
        m = re.match(r"^/([\w-]+)$", path)
        if m and m.group(1) not in {"noticias", "videos", "contacto", "admin", "uploads", "css", "js", "img", "favicon.ico"}:
            page = next((p for p in published_pages() if p["slug"] == m.group(1)), None)
            if page:
                return self.send_html(ui.custom_page(base_url(self.headers.get("Host", "localhost")), page,
                                                     published_pages()))

        # estáticos (css/js/img/favicon)
        if "." in os.path.basename(path):
            return super().do_GET()

        return self.send_html(ui.not_found(), 404)

    def serve_upload(self, path):
        fname = os.path.basename(path)
        safe = os.path.normpath(os.path.join(UPLOAD_DIR, fname))
        if not safe.startswith(UPLOAD_DIR) or not os.path.isfile(safe):
            return self.send_html(ui.not_found(), 404)
        ctype = mimetypes.guess_type(safe)[0] or "application/octet-stream"
        size = os.path.getsize(safe)
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(size))
        self.send_header("Cache-Control", "public, max-age=31536000, immutable")
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()
        if self.command == "HEAD":
            return
        with open(safe, "rb") as fh:
            while True:
                chunk = fh.read(1 << 18)
                if not chunk:
                    break
                self.wfile.write(chunk)

    # ---------------- POST público ----------------
    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/contacto":
            try:
                body = self.read_body()
            except ValueError:
                return self.send_html(ui.not_found(), 413)
            form = self.body_form(body)
            if (form.get("_honey") or "").strip():
                return self.redirect("/contacto?ok=1")
            msg = {
                "id": uuid.uuid4().hex[:10],
                "name": (form.get("name") or "").strip()[:120],
                "email": (form.get("email") or "").strip()[:160],
                "message": (form.get("message") or "").strip()[:4000],
                "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "read": False,
            }
            if msg["name"] and msg["email"] and msg["message"]:
                mut(lambda d: d["inbox"].insert(0, msg))
                relay_contact(msg)
            return self.redirect("/contacto?ok=1")

        if path.startswith("/admin"):
            if path == "/admin/login":
                return self.admin_login_post()
            guard = self.admin_guard()
            if not guard:
                return self.redirect("/admin/login")
            try:
                body = self.read_body()
            except ValueError:
                return self.send_json({"error": "body demasiado grande"}, 413)
            return self.admin_post(path, body, guard)

        return self.send_html(ui.not_found(), 404)

    def admin_login_post(self):
        body = self.read_body()
        form = self.body_form(body)
        ip = self.client_address[0]
        fails, lock = _login_fails.get(ip, [0, 0])
        if lock > time.time():
            return self.send_html(ui.admin_login(error="Demasiados intentos. Espera unos minutos."), 429)
        user = next((u for u in store()["users"] if u["username"] == (form.get("u") or "").strip()), None)
        if not user or not check_password(form.get("p") or "", user["hash"]):
            fails += 1
            _login_fails[ip] = [fails, time.time() + 900 if fails >= 5 else 0]
            return self.send_html(ui.admin_login(error="Usuario o contraseña incorrectos."), 401)
        _login_fails.pop(ip, None)
        tok = make_session(user["username"])
        return self.redirect("/admin", ("Set-Cookie", f"mnr_s={tok}; Path=/; Max-Age={SESSION_TTL}; HttpOnly; SameSite=Lax"))

    # ---------------- Admin GET ----------------
    def admin_get(self, path, qs, guard):
        user, sess, csrf = guard
        data = store()
        if path == "/admin":
            return self.send_html(ui.admin_home(user, csrf, data))
        if path == "/admin/posts":
            return self.send_html(ui.admin_posts(user, csrf, data))
        m = re.match(r"^/admin/editor/(new|([\w-]+))$", path)
        if m:
            kind = "post"
            item = next((p for p in data["posts"] if p["id"] == m.group(2)), None) if m.group(2) else None
            return self.send_html(ui.admin_editor(user, csrf, "post", item))
        m = re.match(r"^/admin/pages/editor/(new|([\w-]+))$", path)
        if m:
            item = next((p for p in data["pages"] if p["id"] == m.group(2)), None) if m.group(2) else None
            return self.send_html(ui.admin_editor(user, csrf, "page", item))
        if path == "/admin/pages":
            return self.send_html(ui.admin_pages(user, csrf, data))
        if path == "/admin/media":
            files = sorted(os.listdir(UPLOAD_DIR), reverse=True)
            return self.send_html(ui.admin_media(user, csrf, files))
        if path == "/admin/inbox":
            return self.send_html(ui.admin_inbox(user, csrf, data))
        if path == "/admin/settings":
            return self.send_html(ui.admin_settings(user, csrf, data))
        return self.send_html(ui.not_found(), 404)

    # ---------------- Admin POST (API) ----------------
    def admin_post(self, path, body: bytes, guard):
        user, sess, csrf = guard
        ctype = self.headers.get("Content-Type", "")

        if ctype.startswith("application/json"):
            try:
                payload = json.loads(body.decode("utf-8"))
            except Exception:
                return self.send_json({"error": "JSON inválido"}, 400)
            if not verify_csrf(sess, self.headers.get("X-CSRF", "")):
                return self.send_json({"error": "CSRF inválido"}, 403)
            return self.admin_api(path, payload, user)

        form = self.body_form(body)
        if not verify_csrf(sess, form.get("_csrf", "")):
            return self.send_html(ui.admin_login(error="Sesión expirada. Vuelve a entrar."), 403)

        if path == "/admin/login2fa":  # reservado
            return self.redirect("/admin")

        if path == "/admin/inbox/delete":
            mid = form.get("id", "")
            mut(lambda d: d.__setitem__("inbox", [m for m in d["inbox"] if m["id"] != mid]))
            return self.redirect("/admin/inbox")
        if path == "/admin/inbox/read":
            mid = form.get("id", "")
            mut(lambda d: [m.__setitem__("read", True) for m in d["inbox"] if m["id"] == mid])
            return self.redirect("/admin/inbox")

        if path == "/admin/settings/site":
            def fn(d):
                s = d["settings"]
                for k in ("siteTitle", "tagline", "heroTitle", "heroSubtitle", "contactEmail"):
                    s[k] = (form.get(k) or "").strip()[:400]
                for k in ("ad1Media", "ad2Media"):
                    s[k] = (form.get(k) or "").strip()[:300]
                for k in ("ad1Link", "ad2Link"):
                    s[k] = (form.get(k) or "").strip()[:300]
                for k in ("facebook", "x", "instagram", "youtube"):
                    s["social"][k] = (form.get("social_" + k) or "").strip()[:200]
                if form.get("heroImage"):
                    s["heroImage"] = form["heroImage"][:300]
            mut(fn)
            return self.redirect("/admin/settings")

        if path == "/admin/settings/password":
            u = next((u for u in store()["users"] if u["username"] == user), None)
            if not u or not check_password(form.get("current", ""), u["hash"]):
                return self.send_html(ui.admin_settings(user, csrf, store(), error="Contraseña actual incorrecta."), 400)
            newp = form.get("new") or ""
            if len(newp) < 10 or not re.search(r"[A-Za-z]", newp) or not re.search(r"\d", newp):
                return self.send_html(ui.admin_settings(user, csrf, store(),
                                        error="La nueva contraseña necesita 10+ caracteres con letras y números."), 400)
            mut(lambda d: [u2.__setitem__("hash", hash_password(newp)) for u2 in d["users"] if u2["username"] == user])
            return self.redirect("/admin/settings")

        if path == "/admin/media/delete":
            fname = os.path.basename(form.get("file", ""))
            safe = os.path.join(UPLOAD_DIR, fname)
            if os.path.isfile(safe):
                os.remove(safe)
            return self.redirect("/admin/media")

        return self.send_json({"error": "ruta no encontrada"}, 404)

    def admin_api(self, path, payload, user):
        if path == "/admin/api/save":
            kind = "page" if payload.get("kind") == "page" else "post"
            title = (payload.get("title") or "").strip()[:200] or "Sin título"
            blocks = payload.get("blocks") if isinstance(payload.get("blocks"), list) else []
            clean_blocks = []
            for b in blocks[:80]:
                if not isinstance(b, dict) or b.get("t") not in {"h", "p", "img", "video", "q"}:
                    continue
                clean = {"t": b["t"]}
                for k, limit in (("text", 20000), ("src", 400), ("alt", 300), ("cap", 400), ("by", 160), ("yt", 60)):
                    if b.get(k):
                        clean[k] = str(b[k]).strip()[:limit]
                if clean.get("t") in {"h", "p"} and not clean.get("text"):
                    continue
                clean_blocks.append(clean)

            def fn(d):
                target = d["posts"] if kind == "post" else d["pages"]
                pid = payload.get("id") or ""
                item = next((p for p in target if p["id"] == pid), None)
                if item is None:
                    item = {"id": uuid.uuid4().hex[:10],
                            "date": payload.get("date") or datetime.now(timezone.utc).strftime("%Y-%m-%d")}
                    item["slug"] = unique_slug(kind, slugify(payload.get("slug") or title), item["id"])
                    target.append(item)
                item["title"] = title
                item["slug"] = unique_slug(kind, slugify(payload.get("slug") or title), item["id"])
                if kind == "post":
                    item["excerpt"] = (payload.get("excerpt") or "").strip()[:400]
                    item["cover"] = (payload.get("cover") or "").strip()[:300]
                    tags = payload.get("tags") or ""
                    if isinstance(tags, list):
                        tags = ", ".join(str(t) for t in tags)
                    cat_in = payload.get("category") or ""
                    item["category"] = cat_in if cat_in in CATEGORIES else "Noticias"
                    item["author"] = (payload.get("author") or "Redacción El Mañanero").strip()[:120]
                    item["tags"] = [t.strip()[:40] for t in tags.split(",") if t.strip()][:8]
                    item["featured"] = bool(payload.get("featured"))
                    item.setdefault("blocks", [])
                    item["blocks"] = clean_blocks
                    item["kind"] = "video" if payload.get("isVideo") else "post"
                else:
                    item["blocks"] = clean_blocks
                    item["inNav"] = bool(payload.get("inNav"))
                    item["navOrder"] = int(payload.get("navOrder") or 99)
                item["status"] = "published" if payload.get("status") == "published" else "draft"
                if kind == "page" and not item.get("date"):
                    item["date"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            mut(fn)
            items = store()["posts"] if kind == "post" else store()["pages"]
            item = next((p for p in items if p["title"] == title), items[-1])
            return self.send_json({"ok": True, "id": item["id"], "slug": item["slug"],
                                   "url": ("/noticias/" + item["slug"]) if kind == "post" else ("/" + item["slug"])})

        if path == "/admin/api/delete":
            kind = "page" if payload.get("kind") == "page" else "post"
            pid = payload.get("id", "")

            def fn(d):
                target = d["posts"] if kind == "post" else d["pages"]
                d["posts" if kind == "post" else "pages"] = [p for p in target if p["id"] != pid]
            mut(fn)
            return self.send_json({"ok": True})

        if path == "/admin/api/status":
            kind = "page" if payload.get("kind") == "page" else "post"
            pid = payload.get("id", "")
            status = payload.get("status")

            def fn(d):
                target = d["posts"] if kind == "post" else d["pages"]
                for p in target:
                    if p["id"] == pid:
                        p["status"] = "published" if status == "published" else "draft"
            mut(fn)
            return self.send_json({"ok": True})

        if path == "/admin/api/upload":
            raise ValueError("usa multipart")

        return self.send_json({"error": "ruta no encontrada"}, 404)


# multipart para /admin/api/upload (sobrecargado aparte por claridad)
def _admin_upload(self, guard):
    user, sess, csrf = guard
    if not verify_csrf(sess, self.headers.get("X-CSRF", "")):
        return self.send_json({"error": "CSRF inválido"}, 403)
    ctype = self.headers.get("Content-Type", "")
    if "boundary=" not in ctype:
        return self.send_json({"error": "multipart requerido"}, 400)
    try:
        body = self.read_body()
    except ValueError:
        return self.send_json({"error": "archivo demasiado grande"}, 413)
    import email
    msg = email.message_from_bytes(
        b"Content-Type: " + ctype.encode("latin-1") + b"\r\nMIME-Version: 1.0\r\n\r\n" + body)
    saved = []
    for part in msg.walk():
        fname = part.get_filename()
        if not fname:
            continue
        ext = os.path.splitext(fname)[1].lower()
        if ext not in ALLOWED_EXT:
            return self.send_json({"error": f"formato no permitido: {ext}"}, 400)
        data = part.get_payload(decode=True) or b""
        if not data or len(data) > MAX_UPLOAD:
            return self.send_json({"error": "archivo vacío o demasiado grande"}, 400)
        safe = uuid.uuid4().hex[:12] + ext
        with open(os.path.join(UPLOAD_DIR, safe), "wb") as fh:
            fh.write(data)
        saved.append({"name": fname, "file": safe, "url": "/uploads/" + safe,
                      "size": len(data), "isVideo": ext in {".mp4", ".webm"}})
    if not saved:
        return self.send_json({"error": "sin archivo"}, 400)
    return self.send_json({"ok": True, "files": saved})


# parche: enrutar el upload multipart
def _do_POST_with_upload(self):
    path = urlparse(self.path).path
    if path == "/admin/api/upload":
        guard = self.admin_guard()
        if not guard:
            return self.send_json({"error": "no autenticado"}, 401)
        return _admin_upload(self, guard)
    return Handler_doPOST_original(self)


Handler_doPOST_original = Handler.do_POST
Handler.do_POST = _do_POST_with_upload


# ----------------------------------------------------------------------------
# Relay opcional de contacto vía FormSubmit (si CONTACT_EMAIL está definido)
# ----------------------------------------------------------------------------
def relay_contact(msg: dict):
    email = store()["settings"].get("contactEmail") or CONTACT_EMAIL
    if not email:
        return

    def _task():
        try:
            import urllib.request
            payload = json.dumps({
                "name": msg["name"], "email": msg["email"],
                "message": msg["message"][:2000],
                "_subject": "Contacto web — El Mañanero",
                "_template": "table", "_captcha": "false",
            }).encode()
            req = urllib.request.Request(
                f"https://formsubmit.co/ajax/{email}", data=payload,
                headers={"Content-Type": "application/json", "Accept": "application/json"})
            urllib.request.urlopen(req, timeout=15)
        except Exception as e:
            print("[contact] relay falló (el mensaje sigue en el inbox del admin):", e)
    threading.Thread(target=_task, daemon=True).start()


# ----------------------------------------------------------------------------
def main():
    # ADMIN_PASSWORD manda: si la variable está definida y no coincide con la
    # guardada, se sincroniza al arrancar (método de recuperación sin sesión).
    pw_env = os.environ.get("ADMIN_PASSWORD", "").strip()
    if pw_env:
        admin = next((u for u in store()["users"] if u.get("username") == "admin"), None)
        if admin and not check_password(pw_env, admin["hash"]):
            admin["hash"] = hash_password(pw_env)
            save_store(store())
            print("[admin] contraseña sincronizada con la variable ADMIN_PASSWORD.")
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"El Mañanero — sirviendo en http://0.0.0.0:{PORT}")
    print(f"Admin: http://0.0.0.0:{PORT}/admin  (usuario: admin)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
