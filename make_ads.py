# -*- coding: utf-8 -*-
"""Logo 'El Mañanero' (sin DEPORTES) + placeholders de publicidad."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont

logo = Image.open("img/logo.png")
alpha = logo.split()[3]

# --- separar las dos lineas del texto (EL MANANERO / DEPORTES) por su hueco ---
band = alpha.crop((0, 2380, logo.width, logo.height))
rows = [band.crop((0, y, logo.width, y + 1)).getbbox() is not None for y in range(band.height)]
# hueco mas largo = separacion real entre EL MANANERO y DEPORTES
runs = []
start = None
for y, has in enumerate(rows):
    if not has:
        if start is None:
            start = y
    else:
        if start is not None:
            runs.append((start, y - start))
            start = None
if start is not None:
    runs.append((start, len(rows) - start))
gap_start = max(runs, key=lambda r: r[1])[0]
print("hueco entre lineas en y =", 2380 + gap_start if gap_start else None)

line1_top = 2380
line1_bottom = 2380 + (gap_start or 300)
l1 = alpha.crop((0, line1_top, logo.width, line1_bottom))
bb = l1.getbbox()
word = logo.crop((bb[0], line1_top + bb[1], bb[2], line1_top + bb[3]))
print("linea EL MANANERO:", word.size)

# emblema desde el original
top = alpha.crop((0, 0, logo.width, 2350))
bb = top.getbbox()
emblem = logo.crop(bb)
pad = int(emblem.height * 0.12)
emb_pad = Image.new("RGBA", (emblem.width + pad * 2, emblem.height + pad * 2), (0, 0, 0, 0))
emb_pad.alpha_composite(emblem, (pad, pad))

# componer: emblema + una linea de texto
H = 570
scale = 500 / emb_pad.height
emb_r = emb_pad.resize((int(emb_pad.width * scale), 500), Image.LANCZOS)
wscale = (H - 150) / word.height
word_r = word.resize((int(word.width * wscale), H - 150), Image.LANCZOS)
GAP = 70
W = emb_r.width + GAP + word_r.width
canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
canvas.alpha_composite(emb_r, (0, 35))
canvas.alpha_composite(word_r, (emb_r.width + GAP, 75))
canvas.save("img/logo-h.png")
print("logo-h.png:", canvas.size)

# --- placeholders de publicidad ---
NAVY = (13, 27, 40)
DEEP = (23, 62, 94)
GOLD = (232, 179, 44)
SKY = (63, 169, 220)


def gradient(w, h, top, bottom):
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        c = tuple(int(top[i] + (bottom[i] - top[i]) * y / (h - 1)) for i in range(3))
        for x in range(w):
            px[x, y] = c
    return img


def fnt(size, bold=True):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def ad_header():
    w, h = 1400, 180
    img = gradient(w, h, DEEP, NAVY).convert("RGBA")
    d = ImageDraw.Draw(img)
    # motivo de ondas a la derecha
    for r in (70, 120, 170):
        d.ellipse([w - 120 - r, h // 2 - r, w - 120 + r, h // 2 + r], outline=SKY + (40,), width=3)
    # marco dorado fino
    d.rectangle([3, 3, w - 4, h - 4], outline=GOLD + (200,), width=3)
    # chip PUBLICIDAD
    d.rounded_rectangle([36, 36, 250, 78], 22, fill=GOLD)
    d.text((52, 44), "PUBLICIDAD", font=fnt(26), fill=NAVY)
    # titular
    d.text((38, 88), "Su anuncio puede estar aquí", font=fnt(52), fill=(255, 255, 255))
    # contacto
    d.text((40, h - 40), "Escríbanos: hola@elsolmananero.com", font=fnt(24, bold=False), fill=(159, 180, 198))
    # sello
    mk = Image.open("img/mark.png").convert("RGBA").resize((110, 110), Image.LANCZOS)
    mk.putalpha(mk.split()[3].point(lambda a: int(a * 0.85)))
    img.alpha_composite(mk, (w - 150, h // 2 - 55))
    img.convert("RGB").save("img/pub-filler-top.png")
    print("pub-filler-top.png listo")


def ad_rail():
    w, h = 1200, 780
    img = gradient(w, h, DEEP, NAVY).convert("RGBA")
    d = ImageDraw.Draw(img)
    for r in (150, 240, 330):
        d.ellipse([w // 2 - r, 240 - r, w // 2 + r, 240 + r], outline=SKY + (36,), width=3)
    d.rectangle([3, 3, w - 4, h - 4], outline=GOLD + (200,), width=3)
    d.rounded_rectangle([w // 2 - 130, 60, w // 2 + 130, 116], 28, fill=GOLD)
    f1 = fnt(34)
    tw = d.textlength("PUBLICIDAD", font=f1)
    d.text((w // 2 - tw / 2, 72), "PUBLICIDAD", font=f1, fill=NAVY)
    f2 = fnt(64)
    t2 = "Su anuncio puede"
    t3 = "estar aquí"
    d.text((w // 2 - d.textlength(t2, font=f2) / 2, 190), t2, font=f2, fill=(255, 255, 255))
    d.text((w // 2 - d.textlength(t3, font=f2) / 2, 275), t3, font=f2, fill=(255, 255, 255))
    mk = Image.open("img/mark.png").convert("RGBA").resize((170, 170), Image.LANCZOS)
    mk.putalpha(mk.split()[3].point(lambda a: int(a * 0.9)))
    img.alpha_composite(mk, (w // 2 - 85, 400))
    f3 = fnt(30, bold=False)
    t4 = "Escríbanos: hola@elsolmananero.com"
    d.text((w // 2 - d.textlength(t4, font=f3) / 2, h - 80), t4, font=f3, fill=(159, 180, 198))
    img.convert("RGB").save("img/pub-filler-rail.png")
    print("pub-filler-rail.png listo")


ad_header()
ad_rail()
