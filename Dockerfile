FROM python:3.12-alpine

WORKDIR /app

COPY server.py ui.py admin_ui.py seed.py ./
COPY css ./css
COPY js ./js
COPY img ./img
COPY media ./media
COPY og-image.jpg favicon.ico ./

ENV PORT=8080
EXPOSE 8080

# Persistencia: monta volúmenes en /app/data (base de datos) y /app/uploads (media)
VOLUME ["/app/data", "/app/uploads"]

CMD ["python", "server.py"]
