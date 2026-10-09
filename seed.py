# -*- coding: utf-8 -*-
"""Contenido de demostración para El Mañanero Deportes.

- `enrich(store)`: agrega noticias/videos de ejemplo y redes sociales si el
  store está vacío (lo usa el primer arranque y se puede correr a mano:
  `python seed.py`).

Todo el contenido es dummy: se puede editar o eliminar desde el panel
(/admin → Noticias / Multimedia) como cualquier otra nota.
"""
import os
from datetime import date, timedelta

DEMO_TAGLINE = "Tu Guía Local: Noticias, Deportes y Comunidad en Oregón"

SOCIAL_DEFAULTS = {
    "facebook": "https://www.facebook.com/elsolmananero",
    "x": "",
    "instagram": "https://www.instagram.com/elsolmananero",
    "youtube": "",
}


def _dates_ago(n):
    return (date.today() - timedelta(days=n)).isoformat()


def _post(slug, title, cat, cover, excerpt, author, days, blocks, featured=False, video=False):
    return {
        "id": "demo" + slug[:6].replace("-", ""),
        "slug": slug,
        "title": title,
        "excerpt": excerpt,
        "category": cat,
        "author": author,
        "date": _dates_ago(days),
        "status": "published",
        "featured": featured,
        "kind": "video" if video else "post",
        "cover": "/img/covers/" + cover + ".webp",
        "tags": [],
        "inNav": False,
        "navOrder": 90,
        "blocks": blocks,
    }


def content():
    V = "/media/demo-video.mp4"
    posts = [
        # ---------------- Deportes (4) ----------------
        _post("timbers-victoria-providence-park",
              "Los Timbers abren la temporada con victoria en el Providence Park",
              "Deportes", "deportes",
              "Golazo al 78' y portería a cero: Portland arrancó con pie derecho "
              "ante 25 mil aficionados que pintaron de verde y amarillo la ciudad.",
              "Redacción El Mañanero", 0,
              [{"t": "p", "text": "El Portland Timbers comenzó la temporada por todo lo alto con una "
                                 "victoria que se cocinó en la media hora final. Tras un primer tiempo de "
                                 "estudio, el equipo ajustó líneas y encontró el gol al minuto 78 con un "
                                 "zapatazo desde fuera del área que se incrustó en el ángulo."},
               {"t": "h", "text": "El partido, minuto a minuto"},
               {"t": "p", "text": "Los primeros 45 minutos fueron de estudio a la defensiva, con el visitante "
                                  "sosteniendo la pelota. La reestructuración del mediocampo en el descanso "
                                  "cambió la cara del encuentro: la presión alta llegó y con ella las ocasiones "
                                  "más claras.\nLa afición, que llenó el estadio pese al frío, empujó en el "
                                  "tramo final y celebró la primera victoria de la campaña."},
               {"t": "q", "text": "Este equipo nunca deja de correr. Eso es lo que queremos ver cada fin de semana.",
                "by": "Director técnico de los Timbers"},
               {"t": "p", "text": "La próxima jornada será de visita. El Mañanero estará ahí con la previa, "
                                  "el minuto a minuto y la reacción del vestidor."}],
              featured=True),
        _post("lidom-cartas-winter-ball",
              "LIDOM: las cartas del winter ball que verán acción esta semana",
              "Deportes", "deportes-alt",
              "Repasamos el calendario de la pelota dominicana y a los bateadores que "
              "llegan calientes al plato, con horarios convertidos al horario del Pacífico.",
              "Redacción El Mañanero", 1,
              [{"t": "p", "text": "El round robin de la Liga de Béisbol Profesional de la República Dominicana "
                                 "entra en su tramo decisivo y varios compatriotas que viven en Oregón ya "
                                 "preparan sus madrugadas para seguir la acción."},
               {"t": "h", "text": "Horarios para el Pacífico"},
               {"t": "p", "text": "Los juegos de la noche dominicana comienzan entre las 4:00 y las 6:00 PM "
                                  "hora de Oregón. El Mañanero publicará cada mañana la guía completa con "
                                  "los lanzadores probables."}],
              featured=True),
        _post("dominicanos-ncaa-temporada",
              "Los dominicanos a seguir en la NCAA esta temporada",
              "Deportes", "deportes",
              "De Portland State a University of Oregon: la lista de la juventud quisqueyana "
              "que está dejando el nombre alto en el deporte universitario.",
              "Enrique Caizero", 3,
              [{"t": "p", "text": "La diáspora dominicana en Oregón tiene nuevo motivo de orgullo: una camada "
                                 "de atletas universitarios que suma minutos, puntos y récords en la NCAA."},
               {"t": "p", "text": "Seguiremos de cerca sus estadísticas cada semana, con entrevistas a sus "
                                  "entrenadores y familias."}]),
        _post("clasico-mundial-horarios-oregon",
              "Clásico Mundial: calendario y horarios para verlo desde Oregón",
              "Deportes", "deportes-alt",
              "Fechas, sedes y la tabla de conversión de horarios para no perderse ningún "
              "lanzamiento del torneo que une a toda la comunidad.",
              "Redacción El Mañanero", 5,
              [{"t": "p", "text": "El torneo que cada cuatro años detiene a la nación beisbolera ya tiene "
                                 "calendario. Para quienes madrugan o trasnochan en Oregón, esta es la guía "
                                 "de horarios del Pacífico."},
               {"t": "h", "text": "Dónde ver los partidos"},
               {"t": "p", "text": "La mayoría de los encuentros se transmiten por televisión abierta y "
                                  "plataformas de streaming. En El Mañanero los analizaremos cada mañana "
                                  "con la pelota ya enfriada."}]),
        # ---------------- Noticias (2) ----------------
        _post("crece-comunidad-dominicana-portland",
              "Crece la comunidad dominicana en el área metropolitana de Portland",
              "Noticias", "noticia",
              "Los datos del censo y la calle coinciden: más familias quisqueyanas eligen "
              "el noroeste para poner raíces, negocio y béisbol.",
              "Redacción El Mañanero", 1,
              [{"t": "p", "text": "Entre inscripciones escolares, licencias de negocio y ligas deportivas, la "
                                 "huella dominicana en el metro de Portland crece año con año."},
               {"t": "h", "text": "Números que suman"},
               {"t": "p", "text": "Organizaciones comunitarias calculan que la población se ha multiplicado en la "
                                  "última década, con núcleos fuertes en Beaverton, Hillsboro y Gresham."},
               {"t": "q", "text": "Aquí encontramos trabajo, seguridad y espacio para crecer. No nos vamos.",
                "by": "Vecina de Beaverton"}],
              featured=True),
        _post("centro-comunitario-latino-beaverton",
              "Nuevo centro comunitario latino abre sus puertas en Beaverton",
              "Noticias", "noticia-alt",
              "El espacio ofrecerá clases de inglés, tutorías deportivas y orientación "
              "legal gratuita los sábados por la mañana.",
              "Redacción El Mañanero", 4,
              [{"t": "p", "text": "Después de dos años de gestión, el centro abrió con una jornada de puertas "
                                 "abiertas que reunió a cientos de familias."},
               {"t": "p", "text": "El calendario incluye torneos de dominó, clínicas de béisbol para niños y "
                                  "un club de lectura en español."}]),
        # ---------------- Salud y Belleza (2) ----------------
        _post("estiramientos-madrugadores",
              "Rutinas de estiramiento para madrugadores deportistas",
              "Salud y Belleza", "salud",
              "Diez minutos antes de salir de casa que protegen tu espalda y mejoran tu "
              "rendimiento, explicados paso a paso por fisioterapeutas locales.",
              "Redacción El Mañanero", 2,
              [{"t": "p", "text": "Levantarse antes del amanecer para entrenar o trabajar exige prepararle el "
                                 "terreno al cuerpo. Esta rutina de diez minutos activa articulaciones y "
                                 "despierta la circulación."},
               {"t": "h", "text": "La rutina, en orden"},
               {"t": "p", "text": "Cuello, hombros, cadera y tobillos: cuatro bloques de dos minutos con "
                                  "respiración guiada. Ideal antes de correr o de una jornada frente al mostrador."}]),
        _post("desayuno-del-atleta-expertos",
              "El desayuno del atleta, según nutricionistas de Oregón",
              "Salud y Belleza", "salud-alt",
              "Qué comer a las 5 de la mañana para rendir a las 10: proteínas, hidratación "
              "y el error más común que cometemos todos.",
              "Redacción El Mañanero", 6,
              [{"t": "p", "text": "Consultamos a tres nutricionistas deportivas del área de Portland sobre el "
                                 "desayuno ideal para quienes entrenan o trabajan de madrugada."},
               {"t": "p", "text": "La regla de oro: hidratar antes que cafeinar. El café llega después del primer "
                                  "vaso de agua y de una porción de proteína."}]),
        # ---------------- Personalidades Locales (2) ----------------
        _post("el-profesor-voz-madrugada-oregon",
              "La historia de 'El Profesor': la voz que despierta a Oregón",
              "Personalidades Locales", "personalidades",
              "Maestro de escuela de día, locutor de madrugada siempre. Recorremos la vida "
              "del hombre detrás del micrófono que acompaña las mañanas de la comunidad.",
              "Enrique Caizero", 2,
              [{"t": "p", "text": "Su alarma suena a las 3:30 AM. A las 5:00 ya está al aire, repasando la "
                                 "noche deportiva con el mismo entusiasmo de hace veinte años."},
               {"t": "h", "text": "Del aula al estudio"},
               {"t": "p", "text": "Llegó desde San Pedro de Macorís con una maleta y una colección de "
                                  "estadísticas de béisbol anotadas a mano. Hoy esas libretas son leyenda "
                                  "entre los oyentes."},
               {"t": "q", "text": "La mañana no empieza hasta que el oyente se ríe. Ese es mi marcador.",
                "by": "'El Profesor'"}],
              featured=True),
        _post("entrenadora-hillsboro-beisbol-ninos",
              "La entrenadora de Hillsboro que lleva el béisbol a mil niños latinos",
              "Personalidades Locales", "personalidades-alt",
              "Sin campo propio y con donaciones de guantes, armó una liga que este año "
              "celebra su quinta temporada con lista de espera.",
              "Redacción El Mañanero", 7,
              [{"t": "p", "text": "Empezó con doce niños en un parque público. Hoy son mil inscritos y una "
                                 "lista de espera que no deja de crecer."},
               {"t": "p", "text": "Su fórmula: horarios compatibles con los turnos de los padres, uniformes "
                                  "donados y un trofeo simbólico que todos recuerdan."}]),
        # ---------------- Comunidad (2) ----------------
        _post("liga-beisbol-latina-busca-voluntarios",
              "La liga de béisbol latina busca voluntarios para la nueva temporada",
              "Comunidad", "comunidad",
              "Umpires, anotadores y coordinadores de merienda: la liga necesita veinte "
              "voluntarios para arrancar en primavera.",
              "Redacción El Mañanero", 3,
              [{"t": "p", "text": "No hace falta experiencia: la liga capacita a sus voluntarios en una jornada "
                                 "de sábado con comida incluida."},
               {"t": "p", "text": "Las inscripciones para coach asistente siguen abiertas en las categorías "
                                  "infantiles de 6 a 12 años."}]),
        _post("kermes-dominicana-hillsboro",
              "Kermés dominicana en Hillsboro: fecha, lugar y actividades",
              "Comunidad", "comunidad-alt",
              "Dominó, empanadas y merengue en vivo: la cita que ya es tradición regresa "
              "al parque central con entrada gratuita.",
              "Redacción El Mañanero", 8,
              [{"t": "p", "text": "El comité organizador confirmó la fecha de la kermés anual, con torneo de "
                                 "dominó parejas, comida casera y presentaciones en vivo hasta las 8 de la noche."},
               {"t": "h", "text": "Qué llevar"},
               {"t": "p", "text": "Silla plegable, efectivo para los stands y, si puedes, un juguete nuevo para "
                                  "la colecta infantil."}]),
        # ---------------- Eventos (2) ----------------
        _post("cinco-partidos-octubre-oregon",
              "Calendario: los cinco partidos que no te puedes perder este mes",
              "Eventos", "eventos",
              "Del derby universitario al clásico de la liga urbana: la agenda deportiva "
              "de octubre en Oregón, con fechas y precios.",
              "Redacción El Mañanero", 0,
              [{"t": "p", "text": "Octubre llega cargado: cinco citas que van del fútbol profesional al "
                                  "béisbol de la liga latina, todas con entrada accesible para la familia."},
               {"t": "h", "text": "La agenda"},
               {"t": "p", "text": "Viernes de fútbol en Providence Park, sábado doble de la liga latina en "
                                  "Hillsboro y el derby universitario que cierra el mes."}],
              featured=True),
        _post("festival-alegria-latina-portland",
              "El festival de la alegría latina regresa a Portland este fin de semana",
              "Eventos", "eventos-alt",
              "Dos escenarios, veinte propuestas gastronómicas y una zona deportiva con "
              "clínicas gratuitas de béisbol y fútbol para niños.",
              "Redacción El Mañanero", 9,
              [{"t": "p", "text": "El festival espera más de quince mil asistentes entre sábado y domingo en el "
                                  "parque del río."},
               {"t": "p", "text": "El Mañanero transmitirá en vivo desde su stand: pasa a saludar y a grabar tu "
                                  "saludo para el programa."}]),
        # ---------------- Videos (4) ----------------
        _post("video-previa-timbers",
              "Video: la previa de los Timbers desde el Providence Park",
              "Deportes", "video",
              "Ambiente, cánticos y el pronóstico de nuestra mesa de análisis antes del "
              "pitazo inicial.",
              "Redacción El Mañanero", 1,
              [{"t": "video", "src": V, "cap": "La previa de El Mañanero, desde las afueras del estadio."}],
              video=True),
        _post("video-resumen-lidom-jornada",
              "Video: resumen de la jornada en la pelota dominicana",
              "Deportes", "video-alt",
              "Los mejores swings, las atrapadas imposibles y la tabla actualizada del round robin.",
              "Redacción El Mañanero", 2,
              [{"t": "video", "src": V, "cap": "Resumen semanal de la pelota dominicana."}],
              video=True),
        _post("video-entrevista-el-profesor",
              "Video: entrevista completa con 'El Profesor'",
              "Personalidades Locales", "video",
              "Cuarenta años de béisbol contados en veinte minutos, sin prisas y sin filtros.",
              "Enrique Caizero", 4,
              [{"t": "video", "src": V, "cap": "Sentado a conversar, como cada mañana."}],
              video=True),
        _post("video-clinica-beisbol-hillsboro",
              "Video: así fue la clínica de béisbol en Hillsboro",
              "Comunidad", "video-alt",
              "Ciento cincuenta niños, doce coaches voluntarios y una mañana de esos que "
              "hacen la liga grande.",
              "Redacción El Mañanero", 6,
              [{"t": "video", "src": V, "cap": "Clinicazo en Hillsboro, con resumen y entrevistas."}],
              video=True),
    ]
    about = {
        "id": "demopageabout",
        "slug": "nosotros",
        "title": "Nosotros",
        "status": "published",
        "kind": "page",
        "date": _dates_ago(30),
        "inNav": True,
        "navOrder": 40,
        "blocks": [
            {"t": "p", "text": "El Mañanero Deportes es el espacio donde la comunidad latina de Oregón "
                               "empieza el día: análisis deportivo, noticias de la comunidad y la mejor "
                               "música para arrancar la mañana."},
            {"t": "h", "text": "Nuestra misión"},
            {"t": "p", "text": "Informar, acompañar y celebrar a la comunidad hispana del noroeste con "
                               "contenido cercano, honesto y con la pasión que nos caracteriza."},
            {"t": "q", "text": "La mañana no empieza hasta que tú nos escuchas.", "by": "Equipo El Mañanero"},
        ],
    }
    return posts, [about]


def enrich(store):
    """Agrega el contenido dummy al store si aún no existe (idempotente)."""
    posts, pages = content()
    slugs = {p.get("slug") for p in store.get("posts", [])}
    added = 0
    for p in posts:
        if p["slug"] not in slugs:
            store.setdefault("posts", []).append(p)
            added += 1
    pslugs = {p.get("slug") for p in store.get("pages", [])}
    for pg in pages:
        if pg["slug"] not in pslugs:
            store.setdefault("pages", []).append(pg)
            added += 1
    s = store.setdefault("settings", {})
    social = s.setdefault("social", {})
    for k, v in SOCIAL_DEFAULTS.items():
        if not social.get(k):
            social[k] = v
    if not s.get("tagline"):
        s["tagline"] = DEMO_TAGLINE
    if not s.get("contactEmail"):
        s["contactEmail"] = "hola@elsolmananero.com"
    return added


if __name__ == "__main__":
    import json
    import server

    def fn(d):
        return enrich(d)

    n = server.mut(fn)
    print(f"seed: {n} elementos agregados al store")
