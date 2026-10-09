# -*- coding: utf-8 -*-
"""Genera portadas de marca para el contenido dummy + un video demo corto.
Uso: python make_media.py   (idempotente, regenera img/covers y media/)"""
import math
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
COVERS = os.path.join(ROOT, "img", "covers")
MEDIA = os.path.join(ROOT, "media")
os.makedirs(COVERS, exist_ok=True)
os.makedirs(MEDIA, exist_ok=True)

W, H = 1600, 900
NAVY = (13, 27, 40)
DEEP = (21, 58, 91)
BLUE = (43, 138, 199)
SKY = (63, 169, 220)
GOLD = (232, 179, 44)
SLATE = (30, 42, 56)

VARIANTS = {
    # nombre: (tope, fondo, acento de anillo)
    "noticia": (DEEP, NAVY, SKY),
    "deportes": (BLUE, NAVY, GOLD),
    "salud": (SKY, DEEP, (255, 255, 255)),
    "personalidades": (SLATE, NAVY, GOLD),
    "comunidad": (DEEP, SLATE, GOLD),
    "eventos": (GOLD, NAVY, SKY),
    "video": ((18, 34, 50), (8, 15, 23), SKY),
}


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def base_gradient(top, bottom):
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        c = lerp(top, bottom, y / (H - 1))
        for x in range(W):
            px[x, y] = c
    return img


def rings(draw, cx, cy, radii, color, width=3, alpha=28):
    for r in radii:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color + (alpha,), width=width)


def glow(img, cx, cy, radius, color, peak=70):
    layer = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=peak)
    layer = layer.filter(ImageFilter.GaussianBlur(radius / 2.2))
    tint = Image.new("RGB", (W, H), color)
    return Image.composite(tint, img, layer.point(lambda v: min(v, 90)))


def make_cover(name, top, bottom, accent):
    img = base_gradient(top, bottom).convert("RGB")
    img = glow(img, int(W * 0.78), int(H * 0.30), 460, accent, peak=80)
    img = glow(img, int(W * 0.12), int(H * 0.88), 380, bottom, peak=60)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    # motivo del logo: ondas de radio concéntricas
    rings(d, int(W * 0.80), int(H * 0.32), [90, 150, 215, 285, 360], accent)
    # líneas diagonales finas
    for i in range(-2, 12):
        x0 = i * 180
        d.line([x0, H, x0 + 420, 0], fill=(255, 255, 255, 10), width=2)
    # viñeta suave
    vig = Image.new("L", (W, H), 0)
    dv = ImageDraw.Draw(vig)
    dv.rectangle([0, 0, W, H], fill=0)
    dv.ellipse([-W * 0.25, -H * 0.35, W * 1.25, H * 1.35], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(120))
    dark = Image.new("RGB", (W, H), (5, 10, 16))
    img = Image.composite(img, dark, vig)
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    # marca del logo, discreta, abajo a la izquierda
    mark_path = os.path.join(ROOT, "img", "mark.png")
    if os.path.isfile(mark_path):
        mark = Image.open(mark_path).convert("RGBA")
        mh = 150
        mw = int(mark.width * mh / mark.height)
        mark = mark.resize((mw, mh), Image.LANCZOS)
        mark.putalpha(mark.split()[3].point(lambda a: int(a * 0.55)))
        # zona segura: los recortes 16:10 y 3:2 de object-fit:cover quitan ~80-125px
        # por lado; el sello va en x=220 para que siempre se vea completo.
        img.alpha_composite(mark, (220, H - mh - 55))
    img.convert("RGB").save(os.path.join(COVERS, name + ".webp"), "WEBP", quality=78, method=5)
    print("cover:", name)


def wordmark_frame(t, w=1280, h=720):
    """Fondo animado + logotipo para el video demo. t en 0..1 (se compone a W,H y se reduce)."""
    top, bottom, accent = VARIANTS["video"]
    img = base_gradient(top, bottom)
    img = glow(img, int(W * (0.75 - 0.1 * math.sin(t * math.pi))), int(H * 0.35), 420, accent, peak=85)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    cx = int(W * 0.78)
    rings(d, cx, int(H * 0.34), [int(60 + t * 90) + k * 70 for k in range(5)], accent, alpha=36)
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    d2 = ImageDraw.Draw(img)
    # texto
    try:
        f_big = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 120)
        f_sm = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 44)
    except OSError:
        f_big = f_sm = ImageFont.load_default()
    title = "EL MAÑANERO"
    sub = "DEPORTES  ·  OREGÓN"
    fade = min(1.0, t / 0.35) if t < 0.35 else (max(0.0, 1 - (t - 0.85) / 0.15) if t > 0.85 else 1.0)
    a = int(255 * fade)
    tw = d2.textlength(title, font=f_big)
    d2.text(((W - tw) / 2, H * 0.40), title, font=f_big, fill=(255, 255, 255, a),
            stroke_width=3, stroke_fill=(13, 27, 40, a))
    sw = d2.textlength(sub, font=f_sm)
    d2.text(((W - sw) / 2, H * 0.40 + 150), sub, font=f_sm, fill=GOLD + (a,))
    # barra inferior estilo transmisión
    d2.rectangle([0, H - 10, int(W * min(1, t * 1.15)) if t < 0.87 else W, H], fill=GOLD)
    return img.convert("RGB").resize((w, h), Image.LANCZOS)


def make_demo_video():
    out = os.path.join(MEDIA, "demo-video.mp4")
    try:
        import imageio_ffmpeg
    except ImportError:
        print("imageio_ffmpeg no disponible; se omite el video demo")
        return
    fps, dur = 12, 8
    writer = imageio_ffmpeg.write_frames(out, (1280, 720), fps=fps, quality=7, macro_block_size=8)
    writer.send(None)
    import numpy as np
    for i in range(fps * dur):
        frame = wordmark_frame(i / (fps * dur))
        writer.send(np.asarray(frame))
    writer.close()
    print("video demo listo:", out)


if __name__ == "__main__":
    for name, (top, bottom, accent) in VARIANTS.items():
        make_cover(name, top, bottom, accent)
        # segunda variante (alt) por si se necesitan más
        make_cover(name + "-alt", bottom, top, accent)
    make_demo_video()
