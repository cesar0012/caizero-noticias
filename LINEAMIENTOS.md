# Lineamientos y Buenas Prácticas del Proyecto

Guía de referencia que documenta los lineamientos de SEO, la estrategia de
URLs amigables, la preparación para despliegue en Coolify y las buenas
prácticas generales aplicadas en este sitio. Es genérica: sirve como
checklist para futuros sitios del mismo tipo.

> **VERSÍON CANÓNICA (raíz del workspace).** Este archivo en `paginas/LINEAMIENTOS.md`
> es el documento base para todos los proyectos nuevos. Las copias dentro de cada
> subproyecto quedan obsoletas: no se actualizan ni se consultan.

---

## 1. Lineamientos de SEO

### 1.1 Metadatos por página (en el `<head>`)

- **`<title>` único por página**, de 50–60 caracteres: palabra clave +
  nombre del negocio. Nada de títulos duplicados o genéricos.
- **`meta description` única** (150–160 caracteres) con propuesta de valor
  y llamada a la acción; incluir datos de contacto relevantes solo si
  aportan (teléfono en la página de contacto).
- **`canonical`** absoluto en cada página: una sola versión canónica,
  siempre con el dominio de producción y sin parámetros ni extensiones.
- `meta name="robots" content="index, follow, max-image-preview:large"`
  para permitir vista previa grande de imágenes en resultados.
- **Open Graph completo** (`og:type`, `og:title`, `og:description`,
  `og:url`, `og:image` con dimensiones, `og:locale`) y **Twitter Cards**
  (`twitter:card` summary_large_image + título/descripción/imagen).
- **SEO local**: `geo.region`, `geo.placename`, área de servicio y
  licencia del negocio visibles tanto en contenido como en metadatos.
- `theme-color`, favicon PNG, `apple-touch-icon` y `lang` correcto en
  `<html>`.

### 1.2 Datos estructurados (JSON-LD)

- Grafo `@graph` con la entidad central del negocio:
  `HomeAndConstructionBusiness` + `LocalBusiness` (nombre, teléfono
  en formato internacional, email, dirección, `areaServed`,
  `priceRange`, licencia/identificador, fundador).
- `WebSite` y `WebPage` enlazados por `@id` absolutos.
- `OfferCatalog` con los servicios agrupados por categorías (cada uno
  como `Offer` → `Service` con nombre).
- `BreadcrumbList` coherente con el breadcrumb visible.
- Validar siempre en el Rich Results Test / Schema.org validator.

### 1.3 Contenido y semántica

- **Un solo `<h1>` por página**; jerarquía `h2/h3` sin saltos; los
  encabezados describen la sección (palabras clave naturales, sin
  keyword stuffing).
- Texto alternativo **descriptivo y específico** en cada imagen
  (no "foto de jardín" sino qué se hace en esa imagen).
- Navegación consistente entre páginas, breadcrumb visible, enlaces de
  pie con las rutas canónicas.
- Idioma único y consistente; entidades HTML correctas (`&amp;`).

### 1.4 Rendimiento y experiencia (Core Web Vitals)

- Imágenes: compresión razonable, `loading="lazy"` debajo del pliegue y
  **`width`/`height` explícitos** para reservar el espacio (evita CLS).
- JS con `defer`; CSS en un solo archivo; `preconnect` a orígenes de
  fuentes; fuentes con `display=swap`.
- Evitar desplazamiento horizontal en cualquier viewport (guardas de
  overflow a nivel del contenedor de contenido, no del `html/body`
  cuando haya `position:sticky`, porque los guards en ancestros del
  sticky lo rompen en navegadores móviles).
- Móvil primero: objetivos táctiles ≥ 44px, `prefers-reduced-motion`
  respetado (animaciones y video de fondo se desactivan).
- Cache-busting de assets estáticos con query versionada (`?v=n`) para
  invalidar caché de navegadores al publicar cambios.

### 1.5 Indexabilidad

- `sitemap.xml` con todas las URLs canónicas, `lastmod` real y
  prioridades razonables; `robots.txt` apuntando al sitemap.
- Cabecera `X-Robots-Tag: noindex` **solo en ambientes de preview/demo**,
  nunca en producción.
- Redirecciones **301** de URLs antiguas (p. ej. con extensión) a las
  canónicas para no duplicar contenido.

---

## 2. URLs amigables (friendly routes)

### 2.1 Principios

- Rutas semánticas, en minúsculas, planas (un solo nivel):
  `/servicio`, `/nosotros` — sin extensiones, sin guiones bajos, sin
  parámetros innecesarios, sin mayúsculas.
- La URL limpia es la **única canónica**: enlaces internos, canonical,
  `og:url`, datos estructurados (`@id`/`url`) y sitemap deben usarla.
- Un solo formato de slash final y redirección coherente si llega con
  variante.

### 2.2 Elementos técnicos necesarios

1. **Mapa de rutas**: tabla `{ruta → archivo}` en el servidor que
   traduce `/about` → `about.html` (o su equivalente en el stack:
   rewrites de nginx/Caddy/vercel.json, routing del framework, etc.).
2. **Redirección 301** de las versiones con extensión (`.html`) a la
   limpia — evita contenido duplicado y consolida señales SEO.
3. **Enlaces internos** actualizados a las rutas limpias en todo el
   sitio (navegación, footer, CTAs, anclas tipo `/seccion#ancla`).
4. **Metadatos y schemas** regenerados con las URLs limpias y el dominio
   de producción.
5. **404 controlado** para rutas desconocidas y **sin listado de
   directorios** en carpetas de assets.
6. Repetir la verificación en cada cambio: ningún enlace interno debe
   quedar apuntando a la versión vieja.

---

## 3. Despliegue en Coolify (desde GitHub)

### 3.1 Requisitos del repositorio

- **`Dockerfile`** en la raíz: imagen base ligera (p. ej. Python
  Alpine), copiar los archivos del sitio, `EXPOSE` del puerto y `CMD`
  arrancando el servidor.
- **Puerto por variable de entorno** (`PORT`): Coolify la inyecta según
  la configuración del recurso; el proceso debe escuchar en `0.0.0.0`
  (no en localhost).
- **`.dockerignore`**: excluir `.git`, herramientas locales y artefactos
  de desarrollo para imágenes más livianas.
- **Assets binarios necesarios deben vivir en el repositorio**
  (imágenes, videos, fuentes) porque el build se hace desde GitHub;
  usar `.gitignore` solo para binarios que no necesita el deploy
  (ejecutables de herramientas locales, archivos temporales).

### 3.2 El servidor web dentro del contenedor

- Un servidor estático con rewrites es suficiente para un sitio sin
  backend; las rutas amigables las resuelve el propio servidor (ver
  sección 2.2).
- **Cabeceras según ambiente por variables de entorno**: producción con
  caché normal e indexable; modo demo con `Cache-Control: no-store` y
  `X-Robots-Tag: noindex`.
- **No bloquear user-agents de monitoreo** (curl/wget) si se usan
  health checks — mantener el bloqueo solo para herramientas de
  espejado (HTTrack y similares).

### 3.3 Pasos de despliegue

1. Crear el repositorio en GitHub y subir el proyecto completo.
2. En Coolify: nuevo recurso → vincular el repo → Coolify detecta el
   Dockerfile → construir y desplegar.
3. Asignar el **dominio** al recurso (Coolify genera HTTPS con su
   reverse proxy).
4. Verificar en producción: rutas limpias, redirecciones 301, formulario,
   sitemap accesible y `robots.txt`.

### 3.4 Formularios sin backend — MÉTODO OBLIGATORIO

**Método obligatorio para el envío de correos: FormSubmit por AJAX.** Es el
servicio gratuito que se usa en producción (probado en Roque General
Construction); sin cuenta, sin tarjeta y sin backend propio:

1. **Endpoint AJAX**: `https://formsubmit.co/ajax/<correo-del-cliente>`
   como `action` del formulario; el JS hace `fetch(POST, FormData)` con
   cabecera `Accept: application/json`.
2. **Campos ocultos de configuración**: `_subject` (asunto identificable,
   p. ej. "Free Estimate Request — <negocio> website"), `_template` con
   valor `table` (el correo llega como tabla legible) y `_captcha` en
   `false` cuando existe validación propia.
3. **Activación única**: el primer envío real genera un correo de
   confirmación al destinatario; hay que hacer clic en "Activate" una sola
   vez para habilitar la entrega de todos los siguientes.
4. **Honeypot** `_honey` (campo oculto fuera de pantalla) contra spam,
   validación en cliente con estados de error accesibles (`aria-invalid`,
   mensajes por campo), botón deshabilitado durante el envío y estado de
   éxito/error anunciado con `role="status"`.
5. **Fallback a `mailto:`** pre-llenado si el servicio falla o no hay red:
   el JS abre el cliente de correo del visitante con los datos del
   formulario ya escritos.
6. Documentar en el README del proyecto el correo destino y el paso de
   activación (es el pendiente número uno antes de producción).

---

## 4. Buenas prácticas generales (checklist)

### Accesibilidad
- `skip-link` al contenido principal; landmark roles; `aria-current`
  en el ítem activo de navegación; `aria-expanded` en toggles.
- Contraste suficiente en todos los textos, incluidos los que van
  sobre fotos/video (capa de overlay controlada).
- Focus visible y navegación completa por teclado (menús, lightbox,
  formularios); cerrar overlays con `Escape`.

### Responsive
- Breakpoints por contenido, no por dispositivos; probar en el ancho
  real más chico esperado (≈320–390px) buscando overflow horizontal.
- Menú móvil como drawer lateral a nivel de `<body>`: elementos fixed
  dentro de headers con `backdrop-filter`/`transform` heredan el
  containing block y se cortan — el drawer debe vivir fuera.
- Bloqueo de scroll al abrir overlays fijando el `body` con
  `position: fixed` y restaurando la posición al cerrar (el simple
  `overflow: hidden` no detiene el scroll chaining táctil).
- Iconos/controles táctiles con área generosa y separación.

### Calidad de código y mantenimiento
- Commits descriptivos por versión; respaldos antes de cambios grandes.
- Validar balance de etiquetas HTML y sintaxis de JS en cada cambio.
- Repetibles: fotos sustituibles por archivo, galerías que se extienden
  agregando items sin tocar lógica.
- Cache-busting (`?v=n`) en cada publicación de CSS/JS.

---

## 5. Demo para cliente con Cloudflare Tunnel

### 5.1 Objetivo
Poder enviar al cliente un enlace público HTTPS para revisar el sitio antes
de publicar a producción, sin cuenta ni dominio propio, sirviendo el sitio
en **modo demo** (cabeceras `X-Robots-Tag: noindex` y `Cache-Control:
no-store`, ver sección 3.2) para que Google no indexe la versión de
previsualización.

### 5.2 Archivos que deben existir en la raíz del proyecto
- **`tools/cloudflared.exe`** — binario de Cloudflare Tunnel (no se sube a
  GitHub ni al Docker image: `tools/` está en `.gitignore` y
  `.dockerignore`).
- **`demo.py`** — lanzador: levanta `server.py` con `DEMO=1` en un puerto
  libre (evitar puertos ocupados por otros proyectos; configurable con la
  variable `PORT`), abre el quick tunnel con
  `cloudflared.exe tunnel --url http://localhost:PUERTO`, escribe la URL
  pública en `demo-url.txt` y la imprime en consola. Si el túnel se cae, lo
  reinicia automáticamente (los quick tunnels generan una URL aleatoria
  nueva en cada arranque).
- **`demo-server.bat`** — punto de entrada de doble clic para Windows:
  sitúa la raíz del proyecto (`cd /d "%~dp0"`), ejecuta `python demo.py` y
  mantiene la ventana abierta al detenerse. Es el único archivo que el
  usuario final necesita ejecutar.

### 5.3 Flujo de uso
1. Doble clic en `demo-server.bat`.
2. Copiar la URL `https://*.trycloudflare.com` que muestra la ventana (o de
   `demo-url.txt`) y enviarla al cliente.
3. El enlace funciona mientras la ventana esté abierta y la máquina
   encendida; al reiniciar el bat hay que enviar la URL nueva.
4. Para detener: cerrar la ventana o Ctrl+C.

### 5.4 Notas
- El túnel expone **solo** el sitio local por HTTPS; no abre puertos del
  equipo a internet.
- No bloquear el user-agent de curl/wget (health checks de Cloudflare),
  siguiendo la sección 3.2.
- Recordar al cliente que es una previsualización temporal; la versión
  definitiva vive en producción (sección 3).


---

## 6. Reglas obligatorias de diseño

### 6.1 El header no puede tener información duplicada

El header se compone de **dos capas**: la barra superior (topbar) y la barra
de navegación principal con sus CTAs. **Ningún dato puede aparecer en ambas
capas a la vez.** Cada pieza de información de contacto tiene un único
lugar asignado; si se necesita en la otra capa, se mueve, no se copia.

- Caso ocurrido (Roque GC): el teléfono estaba en la topbar y también junto
  al botón "Free Estimate" de la barra principal. Corrección aplicada: el
  teléfono vive solo en la barra principal, junto al CTA.
- Regla práctica por defecto: **topbar** = ubicación/área de servicio y
  credenciales cortas (licencia, "licensed & insured"); **barra principal** =
  teléfono (click-to-call) y CTA principal.
- **Esta regla aplica solo al header.** El footer queda exento: ahí sí es
  correcto (y deseable) repetir teléfono, correo y ubicación completos.
- Al terminar un sitio, verificar: ningún texto de la topbar aparece
  también en la barra de navegación de la misma página.

### 6.2 Iconografía: nunca emojis — usar Lucide (SVG inline)

**Prohibido usar emojis como iconos de UI** (📍 📞 ✅ 🗑 etc.). Se ven
distintos en cada sistema operativo, no escalan como iconografía de marca,
no heredan la paleta y baratizan el resultado.

- Usar siempre **SVG inline estilo Lucide**: `viewBox="0 0 24 24"`,
  `fill="none"`, `stroke="currentColor"`, `stroke-width="2"`, con
  `aria-hidden="true"` y tamaño explícito. Así los iconos heredan el color
  del texto y el grosor es consistente en todo el sitio.
- Aplica a todos los iconos: ubicación, teléfono, correo, checks, escudos,
  flechas de botones, etc.
- Excepciones tipográficas aceptables (no son emojis): flechas de texto
  (→), estrellas de calificación (★) y símbolos decorativos estilizados
  (✦) cuando forman parte del diseño.
- Los elementos decorativos de marca que son CSS puro (p. ej. los
  "remaches" de la placa) no son iconos y no se sustituyen.
- Al cerrar un sitio, buscar emojis con un rango Unicode (U+1F000–U+1FAFF)
  y confirmar que quedan cero.

### 6.3 Tener cuidado (behavior): "scroll fantasma" al cerrar overlays con scroll bloqueado

**Escenario a vigilar en todos los sitios**: los overlays que bloquean el
scroll (menú móvil drawer, lightbox) fijan el `body` con
`position: fixed` y al cerrarse restauran la posición con
`window.scrollTo(0, y)`. Si el sitio define `html { scroll-behavior: smooth }`,
ese `scrollTo` de restauración se vuelve **animado**: el usuario ve un
scroll repentino hacia abajo justo antes de que la página cambie (típico al
elegir otra sección desde el menú móvil). Ocurrió en Roque GC y puede ocurrir
en cualquier proyecto con drawer + smooth scroll global.

**Solución obligatoria**: restaurar la posición de forma **instantánea** —
`window.scrollTo({ top: y, behavior: "instant" })`, o forzar
`document.documentElement.style.scrollBehavior = "auto"` justo antes del
`scrollTo` y restaurar su valor previo después. El smooth global queda
intacto para anclas y botones back-to-top.
