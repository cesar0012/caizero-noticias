# -*- coding: utf-8 -*-
"""Logo 'El Mañanero con Caizero' + renombrar rellenos publicitarios."""
from PIL import Image, ImageDraw, ImageFont

logo = Image.open("img/logo.png")
alpha = logo.split()[3]

# --- linea 1: EL MANANERO (y 2380..2660) ---
l1 = alpha.crop((0, 2390, logo.width, 2660))
bb = l1.getbbox()
word = logo.crop((bb[0], 2390 + bb[1], bb[2], 2390 + bb[3]))

# --- color azul de marca, muestreado de las letras ---
band = logo.crop((bb[0], 2700, bb[2], 3050)).convert("RGB")
colors = band.getcolors(band.width * band.height)
colors.sort(reverse=True)
brand_blue = None
for count, col in colors:
    if count > 5000 and col[2] > col[0] and col[2] > 120:  # dominante azul
        brand_blue = col
        break
print("azul de marca:", brand_blue)

# --- emblema desde el original ---
top = alpha.crop((0, 0, logo.width, 2350))
eb = top.getbbox()
emblem = logo.crop(eb)
pad = int(emblem.height * 0.12)
emb_pad = Image.new("RGBA", (emblem.width + pad * 2, emblem.height + pad * 2), (0, 0, 0, 0))
emb_pad.alpha_composite(emblem, (pad, pad))

# --- composicion: emblema + EL MANANERO + CON CAIZERO debajo ---
H = 570
emb_r = emb_pad.resize((int(emb_pad.width * 500 / emb_pad.height), 500), Image.LANCZOS)
W1 = 1850
w1r = word.resize((W1, int(word.height * W1 / word.width)), Image.LANCZOS)

# linea 2 dibujada con tracking para igualar el ancho de la linea 1
line2 = "CON CAIZERO"
font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 96)
no_sp = ImageDraw.Draw(Image.new("RGB", (10, 10))).textlength(line2, font=font)
n = len(line2) - 1
TARGET = W1 - 10
track = (TARGET - no_sp) / n
l2_h = int(font.size * 1.25)
l2 = Image.new("RGBA", (TARGET + 60, l2_h), (0, 0, 0, 0))
d2 = ImageDraw.Draw(l2)
x = 0
for ch in line2:
    d2.text((x, 6), ch, font=font, fill=brand_blue + (255,))
    x += d2.textlength(ch, font=font) + track

col_h = w1r.height + 26 + l2_h
col = Image.new("RGBA", (W1, col_h), (0, 0, 0, 0))
col.alpha_composite(w1r, (0, 0))
col.alpha_composite(l2, (0, w1r.height + 26))

GAP = 70
PAD_R = 28
W = emb_r.width + GAP + W1 + PAD_R
canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
canvas.alpha_composite(emb_r, (0, 35))
canvas.alpha_composite(col, (emb_r.width + GAP, (H - col_h) // 2))
canvas.save("img/logo-h.png")
print("logo-h.png:", canvas.size)

# --- renombrar rellenos publicitarios (nombres neutros anti-bloqueador) ---
import os
if os.path.exists("img/ad-header.png"):
    os.replace("img/ad-header.png", "img/pub-filler-top.png")
if os.path.exists("img/ad-rail.png"):
    os.replace("img/ad-rail.png", "img/pub-filler-rail.png")
print("rellenos renombrados")
