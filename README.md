# El Mañanero Deportes — sitio + CMS en un solo contenedor

Sitio web público (inicio, noticias, videos, páginas, contacto) con un panel
de administración integrado para que una persona no técnica publique
contenido: noticias tipo blog con texto, imágenes, videos (YouTube o subidos),
citas, categorías, autor y página de portada.

- **Sin SQL**: la base de datos es una tienda de documentos JSON
  (`data/store.json`) con escritura atómica. No requiere ningún servicio
  externo.
- **Sin dependencias**: solo la librería estándar de Python 3.12.
- **Todo en un contenedor**: sitio público + CMS + base de datos + uploads.

## Estructura

```
server.py    HTTP + rutas limpias + tienda JSON + sesiones + seguridad
ui.py        Plantillas del sitio público (render en servidor, SEO por página)
admin_ui.py  Panel de administración (login, editor de bloques, media, bandeja)
css/ js/     Estilos y comportamiento (vanilla, iconos Lucide inline, sin emojis)
img/         Logo, favicon, og-image
data/        (volumen) store.json + clave de sesiones + contraseña inicial
uploads/     (volumen) imágenes y videos subidos desde el panel
```

## Primer arranque

Al arrancar sin `data/store.json` se crea automáticamente:

- usuario **admin** con contraseña aleatoria impresa en consola y guardada en
  `data/first_password.txt` (o la que indique la variable `ADMIN_PASSWORD`);
- una noticia de bienvenida publicada, un borrador de ejemplo y la página
  "Nosotros".

Entra en `/admin`, inicia sesión y **cambia la contraseña en Ajustes**.

## Variables de entorno

| Variable         | Para qué                                                                 |
|------------------|--------------------------------------------------------------------------|
| `PORT`           | Puerto de escucha (Coolify lo inyecta; por defecto 8080).                 |
| `BASE_URL`       | URL canónica de producción, p. ej. `https://elsolmananero.com`. Genera canonicals, OG, sitemap y RSS absolutos. Si se omite, se deduce del header `Host`. |
| `CONTACT_EMAIL`  | Correo del cliente. Si se define, el formulario de contacto además de guardarse en la bandeja del panel se envía por FormSubmit (AJAX server-side). |
| `ADMIN_PASSWORD` | Contraseña inicial del admin en el primer arranque (opcional).            |

## Despliegue en Coolify

1. Sube este repositorio a GitHub y crea el recurso en Coolify apuntando al
   repo: detecta el `Dockerfile` y construye.
2. Monta/volumena **`/app/data`** y **`/app/uploads`** (el Dockerfile ya los
   declara) para que el contenido sobreviva a los redeploy.
3. Asigna el dominio y define `BASE_URL` con la URL final.
4. Define `CONTACT_EMAIL` con el correo del cliente.
5. Verifica en producción: `/`, `/noticias`, `/categoria/deportes`,
   `/sitemap.xml`, `/robots.txt`, `/rss.xml` y el formulario de contacto.

## Formulario de contacto (método FormSubmit)

El envío usa **FormSubmit AJAX** (`https://formsubmit.co/ajax/<correo>`), sin
registro ni límites, con honeypot anti-spam. **Activación única**: el primer
envío genera un correo de confirmación hacia el destinatario; hay que hacer
clic una sola vez en ese correo para habilitar la entrega. Todos los mensajes
quedan además guardados en la bandeja del panel (`/admin/inbox`), así que
aunque el correo no llegue, el cliente los ve en su panel.

## SEO

- Render en servidor, `title`/`description`/`canonical` absolutos por página,
  Open Graph + Twitter Cards, `robots` con `max-image-preview:large`.
- JSON-LD: `Organization`/`WebSite` en el sitio y `BlogPosting` (con autor y
  `articleSection`) en cada nota.
- `sitemap.xml` (incluye páginas de categoría), `robots.txt` y `rss.xml`
  generados automáticamente.
- URLs limpias sin extensión, 404 controlado, cache-busting `?v=n` en CSS/JS.

## Demo para cliente (Cloudflare Tunnel)

1. Doble clic en `demo-server.bat` (requiere `tools/cloudflared.exe`, que no
   se versiona: cópialo desde otro proyecto).
2. Comparte la URL `https://*.trycloudflare.com` que imprime (queda también
   en `demo-url.txt`).
3. El sitio demo arranca en modo **noindex** (`X-Robots-Tag`) para que Google
   no indexe la previsualización.

## Desarrollo local

```
python server.py
# http://localhost:8080  — panel: http://localhost:8080/admin
```

Contraseña inicial: `data/first_password.txt` (solo existe tras el primer
arranque; no se versiona).

## Seguridad incluida

- Contraseñas con PBKDF2-SHA256 (200k iteraciones), sesiones firmadas HMAC
  (cookie HttpOnly), tokens CSRF en todas las mutaciones del panel,
  bloqueo temporal tras intentos de login fallidos.
- Subidas con lista blanca de extensiones y nombres de archivo uuid; el panel
  no se cachea (`Cache-Control: no-store`).
