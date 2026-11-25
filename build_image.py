#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news front page (v3).

A newspaper front page: masthead, KPI strip, hero lead story, a
schematic world map with one pin per story, four briefs, and a
date-check footer. Deterministic: no time, no randomness, no network.
Run:  python3 build_image.py   ->  writes asset.png (1024x1024)
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "asset.png"

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"

# Palette
PAPER = (247, 243, 232)
NAVY = (20, 33, 61)
NAVY_D = (13, 22, 42)
GOLD = (201, 162, 39)
GOLD_L = (232, 197, 92)
INK = (24, 24, 24)
MUTED = (90, 86, 76)
CARD = (255, 255, 255)
GREEN = (16, 120, 70)
RED = (178, 44, 36)
BLUE = (24, 84, 160)
BROWN = (140, 96, 32)
TEAL = (14, 110, 105)
OCEAN = (207, 227, 238)
LAND = (217, 201, 163)
LAND_LINE = (170, 150, 110)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def text_size(s, f):
    box = d.textbbox((0, 0), s, font=f)
    return box[2] - box[0], box[3] - box[1]


def draw_text(x, y, s, f, fill=INK, anchor="la"):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)


def wrap(s, f, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_size(trial, f)[0] <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(s, f, max_w, max_lines):
    lines = wrap(s, f, max_w)
    assert len(lines) <= max_lines, f"overflow: {s!r} -> {lines}"
    return lines


def card(x, y, w, h, accent, radius=10, lw=3):
    d.rounded_rectangle([x, y, x + w, y + h], radius=radius,
                        fill=CARD, outline=accent, width=lw)
    d.rounded_rectangle([x, y, x + w, y + 10], radius=5, fill=accent)


def num_badge(x, y, n, color, r=22):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=color)
    s = str(n)
    f = font(SANS_B, 26)
    tw, th = text_size(s, f)
    d.text((x + r - tw / 2, y + r - th / 2 - 2), s, font=f, fill=(255, 255, 255))


def stat_chip(x, y, s, fill, fg=(255, 255, 255), size=20, pad_x=12, pad_y=6):
    f = font(SANS_B, size)
    tw, th = text_size(s, f)
    d.rounded_rectangle([x, y, x + tw + 2 * pad_x, y + th + 2 * pad_y],
                        radius=8, fill=fill)
    d.text((x + pad_x, y + pad_y - 1), s, font=f, fill=fg)
    return tw + 2 * pad_x


def stat_line(x, y, s, color, size=21):
    f = font(SANS_B, size)
    d.text((x, y), s, font=f, fill=color)
    return text_size(s, f)[0]


# ---------------- icons (simple geometric marks) ----------------

def icon_rocket(x, y, s, color):
    # body
    d.polygon([(x + 0.5 * s, y), (x + 0.72 * s, y + 0.45 * s),
               (x + 0.72 * s, y + 0.72 * s), (x + 0.28 * s, y + 0.72 * s),
               (x + 0.28 * s, y + 0.45 * s)], fill=color)
    # window
    d.ellipse([x + 0.40 * s, y + 0.28 * s, x + 0.60 * s, y + 0.48 * s],
              fill=(255, 255, 255))
    # fins
    d.polygon([(x + 0.28 * s, y + 0.55 * s), (x + 0.10 * s, y + 0.85 * s),
               (x + 0.28 * s, y + 0.78 * s)], fill=color)
    d.polygon([(x + 0.72 * s, y + 0.55 * s), (x + 0.90 * s, y + 0.85 * s),
               (x + 0.72 * s, y + 0.78 * s)], fill=color)
    # flame
    d.polygon([(x + 0.38 * s, y + 0.74 * s), (x + 0.62 * s, y + 0.74 * s),
               (x + 0.50 * s, y + 1.00 * s)], fill=(242, 140, 40))


def icon_shield(x, y, s, color):
    d.polygon([(x + 0.5 * s, y), (x + 0.95 * s, y + 0.18 * s),
               (x + 0.95 * s, y + 0.55 * s), (x + 0.5 * s, y + s),
               (x + 0.05 * s, y + 0.55 * s), (x + 0.05 * s, y + 0.18 * s)],
              fill=color)
    d.line([(x + 0.28 * s, y + 0.50 * s), (x + 0.45 * s, y + 0.68 * s),
            (x + 0.75 * s, y + 0.32 * s)], fill=(255, 255, 255), width=5)


def icon_ship(x, y, s, color):
    d.polygon([(x + 0.05 * s, y + 0.55 * s), (x + 0.95 * s, y + 0.55 * s),
               (x + 0.80 * s, y + 0.85 * s), (x + 0.20 * s, y + 0.85 * s)],
              fill=color)
    d.rectangle([x + 0.48 * s, y + 0.08 * s, x + 0.54 * s, y + 0.55 * s],
                fill=color)
    d.polygon([(x + 0.54 * s, y + 0.08 * s), (x + 0.85 * s, y + 0.20 * s),
               (x + 0.54 * s, y + 0.32 * s)], fill=GOLD)
    d.line([(x + 0.05 * s, y + 0.95 * s), (x + 0.95 * s, y + 0.95 * s)],
           fill=color, width=3)


def icon_medal(x, y, s, color):
    d.polygon([(x + 0.30 * s, y), (x + 0.45 * s, y),
               (x + 0.55 * s, y + 0.30 * s), (x + 0.40 * s, y + 0.30 * s)],
              fill=(242, 140, 40))
    d.polygon([(x + 0.55 * s, y), (x + 0.70 * s, y),
               (x + 0.60 * s, y + 0.30 * s), (x + 0.45 * s, y + 0.30 * s)],
              fill=(201, 162, 39))
    d.ellipse([x + 0.18 * s, y + 0.28 * s, x + 0.82 * s, y + 0.92 * s],
              fill=color, outline=(120, 80, 20), width=3)
    d.ellipse([x + 0.38 * s, y + 0.48 * s, x + 0.62 * s, y + 0.72 * s],
              fill=(255, 255, 255))


def icon_chart(x, y, s, color):
    d.line([(x, y + 0.90 * s), (x, y + 0.10 * s)], fill=color, width=4)
    d.line([(x, y + 0.90 * s), (x + 0.95 * s, y + 0.90 * s)],
           fill=color, width=4)
    d.line([(x + 0.10 * s, y + 0.25 * s), (x + 0.38 * s, y + 0.45 * s),
            (x + 0.58 * s, y + 0.38 * s), (x + 0.88 * s, y + 0.72 * s)],
           fill=color, width=5)
    d.polygon([(x + 0.88 * s, y + 0.72 * s), (x + 0.70 * s, y + 0.66 * s),
               (x + 0.86 * s, y + 0.86 * s)], fill=color)


# ---------------- masthead ----------------
d.rectangle([0, 0, W, 100], fill=NAVY)
d.rectangle([0, 100, W, 106], fill=GOLD)
draw_text(24, 12, "THE WORLD TODAY", font(SERIF_B, 54), fill=(255, 255, 255))
draw_text(24, 68, "WEDNESDAY 25 NOVEMBER 2026", font(SANS_B, 24), fill=GOLD_L)
draw_text(1000, 16, "5 STORIES", font(SANS_B, 26), fill=(255, 255, 255),
          anchor="ra")
draw_text(1000, 48, "4 CONTINENTS", font(SANS_B, 26), fill=GOLD_L,
          anchor="ra")
draw_text(1000, 76, "ONE FRONT PAGE", font(SANS_B, 20), fill=(255, 255, 255),
          anchor="ra")

# ---------------- KPI strip ----------------
kpis = [("5", "STORIES"), ("4", "CONTINENTS"), ("3", "REGIONS"),
        ("4", "SOURCES")]
kx, ky, kw, kh, gap = 24, 118, 232, 44, 8
for i, (num, label) in enumerate(kpis):
    x = kx + i * (kw + gap)
    d.rounded_rectangle([x, ky, x + kw, ky + kh], radius=8,
                        fill=(255, 255, 255), outline=(200, 190, 165), width=2)
    draw_text(x + 14, ky + 6, num, font(SANS_B, 28), fill=NAVY)
    draw_text(x + 52, ky + 13, label, font(SANS_B, 20), fill=MUTED)

# ---------------- hero: lead story ----------------
HX, HY, HW, HH = 24, 174, 560, 296
card(HX, HY, HW, HH, GREEN)
draw_text(HX + 18, HY + 24, "LEAD STORY", font(SANS_B, 18), fill=GREEN)
draw_text(HX + 18, HY + 46, "ASIA  ·  SPACE", font(SANS_B, 18), fill=MUTED)
icon_rocket(HX + HW - 108, HY + 26, 84, GREEN)
hero_head = fit_lines("SHENZHOU-24 LAUNCHES", font(SANS_B, 38), HW - 36, 2)
hy = HY + 76
for line in hero_head:
    draw_text(HX + 18, hy, line, font(SANS_B, 38), fill=INK)
    hy += 40
chip_w = stat_chip(HX + 18, HY + 158, "1ST FOREIGNER ABOARD TIANGONG",
                   GREEN, size=19)
hero_body = fit_lines(
    "China launches Shenzhou-24 with Pakistan's Muhammad Zeeshan Ali "
    "aboard.", font(SANS, 19), HW - 36, 2)
by = HY + 196
for line in hero_body:
    draw_text(HX + 18, by, line, font(SANS, 19), fill=INK)
    by += 25
draw_text(HX + 18, HY + HH - 34,
          "Crew docks with the Tiangong station.",
          font(SANS, 19), fill=MUTED)

# ---------------- world map panel ----------------
MX, MY, MW, MH = 600, 174, 400, 296
card(MX, MY, MW, MH, BLUE)
draw_text(MX + 18, MY + 24, "WHERE THE DAY HAPPENED",
          font(SANS_B, 18), fill=BLUE)
draw_text(MX + MW - 18, MY + 24, "5 PINS", font(SANS_B, 18),
          fill=MUTED, anchor="ra")

map_x0, map_y0 = MX + 14, MY + 56
map_w, map_h = MW - 28, 196
d.rounded_rectangle([map_x0, map_y0, map_x0 + map_w, map_y0 + map_h],
                    radius=8, fill=OCEAN)

LON_MIN, LON_MAX = -170.0, 190.0
LAT_MIN, LAT_MAX = -55.0, 78.0


def project(lon, lat):
    px = map_x0 + (lon - LON_MIN) / (LON_MAX - LON_MIN) * map_w
    py = map_y0 + (LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * map_h
    return px, py


# light graticule
for lon in range(-150, 181, 30):
    x, _ = project(lon, 0)
    d.line([(x, map_y0), (x, map_y0 + map_h)], fill=(190, 210, 222), width=1)
for lat in range(-30, 61, 30):
    _, y = project(0, lat)
    d.line([(map_x0, y), (map_x0 + map_w, y)], fill=(190, 210, 222), width=1)

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-55, 60),
     (-65, 45), (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-105, 20),
     (-115, 30), (-125, 40), (-125, 49), (-145, 60)],
    # South America
    [(-80, 10), (-60, 10), (-50, 0), (-40, -5), (-35, -10), (-40, -20),
     (-50, -30), (-60, -35), (-70, -40), (-70, -55), (-75, -30), (-80, -15)],
    # Europe
    [(-10, 36), (0, 44), (10, 45), (20, 55), (30, 60), (30, 70),
     (20, 70), (10, 60), (0, 55), (-5, 50), (-10, 45)],
    # Africa
    [(-17, 15), (-10, 30), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 15), (50, 10), (40, 0), (35, -15), (30, -25), (20, -35),
     (15, -30), (10, -15), (5, 0), (-10, 5)],
    # Asia
    [(40, 70), (60, 70), (80, 73), (110, 76), (140, 72), (160, 66),
     (170, 60), (160, 55), (140, 40), (130, 35), (120, 30), (110, 20),
     (105, 10), (100, 5), (95, 15), (90, 22), (80, 25), (75, 20),
     (70, 25), (60, 25), (50, 30), (45, 35), (40, 45), (35, 55)],
    # Australia
    [(113, -22), (125, -15), (135, -12), (142, -11), (150, -22),
     (150, -37), (140, -38), (130, -32), (120, -34), (113, -30)],
]
for poly in CONTINENTS:
    pts = [project(lon, lat) for lon, lat in poly]
    d.polygon(pts, fill=LAND, outline=LAND_LINE)

PINS = [
    (1, 98.5, 39.7, GREEN),
    (2, -75.5, 10.4, RED),
    (3, 24.0, 59.8, BLUE),
    (4, -77.0, 38.9, BROWN),
    (5, 139.7, 35.7, TEAL),
]
for n, lon, lat, color in PINS:
    px, py = project(lon, lat)
    d.ellipse([px - 11, py - 11, px + 11, py + 11], fill=color,
              outline=(255, 255, 255), width=2)
    f = font(SANS_B, 15)
    tw, th = text_size(str(n), f)
    d.text((px - tw / 2, py - th / 2 - 1), str(n), font=f,
           fill=(255, 255, 255))

legend = ["1 Jiuquan, China", "2 Cartagena", "3 Finland Gulf"]
legend2 = ["4 Washington", "5 Tokyo"]
ly = MY + 258
lx = MX + 18
for item in legend:
    draw_text(lx, ly, item, font(SANS_B, 14), fill=MUTED)
    lx += text_size(item, font(SANS_B, 14))[0] + 12
ly = MY + 278
lx = MX + 18
for item in legend2:
    draw_text(lx, ly, item, font(SANS_B, 14), fill=MUTED)
    lx += text_size(item, font(SANS_B, 14))[0] + 12

# ---------------- briefs 2x2 ----------------
BRIEFS = [
    (2, "CARTAGENA HOSTAGES FREED", "ALL FREED",
     "Forces storm a supermarket.", "AMERICAS", RED, icon_shield),
    (3, "ZELENSKIY CONFIRMS SHIP STRIKE", "GULF OF FINLAND",
     "Kyiv hit a Russian cargo ship.", "EUROPE", BLUE, icon_ship),
    (4, "GIULIANI GETS MEDAL OF FREEDOM", "TOP US CIVILIAN HONOUR",
     "Trump gives the top US honour.", "N. AMERICA", BROWN, icon_medal),
    (5, "ASIAN STOCKS SELL OFF", "NIKKEI -2.9%",
     "Slide on fresh US tariff threats.", "ASIA", TEAL, icon_chart),
]
BW, BH = 476, 200
BX0, BY0 = 24, 486
for i, (n, head, stat, body, region, color, icon) in enumerate(BRIEFS):
    bx = BX0 + (i % 2) * (BW + 24)
    by = BY0 + (i // 2) * (BH + 16)
    card(bx, by, BW, BH, color)
    num_badge(bx + 16, by + 20, n, color)
    icon(bx + BW - 62, by + 20, 44, color)
    draw_text(bx + 70, by + 24, region, font(SANS_B, 16), fill=color)
    head_lines = fit_lines(head, font(SANS_B, 27), BW - 36, 2)
    hy = by + 72
    for line in head_lines:
        draw_text(bx + 18, hy, line, font(SANS_B, 27), fill=INK)
        hy += 33
    stat_line(bx + 18, hy + 4, stat, color, size=20)
    draw_text(bx + 18, hy + 36, body, font(SANS, 19), fill=INK)

# ---------------- footer: date check + sources ----------------
FY = 918
d.rectangle([0, FY, W, H], fill=NAVY_D)
draw_text(24, FY + 14, "DATE CHECK  ✓  Wednesday 25 November 2026 — verified",
          font(SANS_B, 21), fill=GOLD_L)
draw_text(24, FY + 46, "Sources: Reuters / Al Jazeera / Xinhua / SCMP, 25 Nov 2026",
          font(SANS, 18), fill=(220, 220, 220))
draw_text(1000, FY + 14, "THE WORLD TODAY", font(SERIF_B, 22),
          fill=(255, 255, 255), anchor="ra")
draw_text(1000, FY + 46, "One day. One page.", font(SANS, 18),
          fill=(200, 200, 200), anchor="ra")

img.save(OUT)
print(f"Wrote {OUT} ({img.size[0]}x{img.size[1]})")
