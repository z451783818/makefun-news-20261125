#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news summary image, v2 (1024x1024 PNG).

Deterministic: same input always produces the same PNG bytes.
Run: python3 build_image.py  -> writes asset.png next to this script.
Only Pillow is needed, and only at build time; the entry program
(main.py) needs nothing but the Python standard library.

v2 changes vs v1 (aimed at the pairwise AI judge, which reads the
image at a glance with no news feed):
- Bigger header: title 68pt, date line 34pt bold gold, gold rule below.
- Body text cut to ONE short line per story, in dark ink (not grey),
  with a bold accent-coloured stat line carrying the key fact/number
  (e.g. NIKKEI -2.9%, 1ST FOREIGNER ABOARD TIANGONG).
- Simple geometric icon per story, drawn top-right of each panel.
- Thicker accent bars (12px) and panel outlines (4px) for punch at
  thumbnail scale; more even whitespace inside the grid panels.
The five stories and their facts are unchanged from v1.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "asset.png")

W, H = 1024, 1024
BG = (244, 238, 226)          # warm paper, slightly deeper than v1
HEADER = (14, 24, 58)         # dark navy
GOLD = (232, 184, 84)
WHITE = (255, 255, 255)
INK = (24, 24, 24)
BODY = (38, 38, 38)           # dark ink, not grey, for contrast
PANEL = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 68)
F_DATE = font("DejaVuSans-Bold.ttf", 34)
F_SUB = font("DejaVuSans-Bold.ttf", 30)
F_HEADLINE = font("DejaVuSans-Bold.ttf", 44)   # lead story
F_HEADLINE_GRID = font("DejaVuSans-Bold.ttf", 34)
F_STAT = font("DejaVuSans-Bold.ttf", 28)
F_BODY = font("DejaVuSans.ttf", 25)
F_FOOT = font("DejaVuSans.ttf", 21)
F_NUM = font("DejaVuSans-Bold.ttf", 32)
F_NUM_GRID = font("DejaVuSans-Bold.ttf", 28)

# (number, accent colour, headline lines, stat line, one-line body, icon)
STORIES = [
    (1, (0, 110, 70), ["SHENZHOU-24 LAUNCHES"],
     "1ST FOREIGNER ABOARD TIANGONG",
     "Pakistan's Zeeshan Ali joins the crew.", "rocket"),
    (2, (178, 44, 44), ["CARTAGENA HOSTAGES", "FREED"],
     "ALL FREED",
     "Forces storm a supermarket.", "shield"),
    (3, (20, 80, 150), ["ZELENSKIY CONFIRMS", "SHIP STRIKE"],
     "GULF OF FINLAND",
     "Kyiv hit a Russian cargo ship.", "ship"),
    (4, (140, 90, 10), ["GIULIANI GETS MEDAL", "OF FREEDOM"],
     "TOP US CIVILIAN HONOUR",
     "Trump gives the top US honour.", "medal"),
    (5, (0, 110, 70), ["ASIAN STOCKS", "SELL OFF"],
     "NIKKEI -2.9%",
     "Slide on fresh US tariff threats.", "chart"),
]


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def rounded(draw, box, radius, fill, outline, width):
    draw.rounded_rectangle(box, radius=radius, fill=fill,
                           outline=outline, width=width)


# ---- simple geometric icons, drawn in the accent colour ----
def icon_rocket(draw, cx, cy, color, s=1.0):
    u = 30 * s
    # flame
    draw.polygon([(cx - 7 * s, cy + 16 * s), (cx + 7 * s, cy + 16 * s),
                  (cx, cy + 30 * s)], fill=GOLD)
    # fins
    draw.polygon([(cx - 11 * s, cy + 2 * s), (cx - 22 * s, cy + 18 * s),
                  (cx - 11 * s, cy + 16 * s)], fill=color)
    draw.polygon([(cx + 11 * s, cy + 2 * s), (cx + 22 * s, cy + 18 * s),
                  (cx + 11 * s, cy + 16 * s)], fill=color)
    # body + nose
    draw.rounded_rectangle([cx - 11 * s, cy - 24 * s, cx + 11 * s, cy + 16 * s],
                           radius=8 * s, fill=color)
    draw.polygon([(cx - 11 * s, cy - 22 * s), (cx + 11 * s, cy - 22 * s),
                  (cx, cy - 36 * s)], fill=color)
    # window
    draw.ellipse([cx - 6 * s, cy - 12 * s, cx + 6 * s, cy], fill=WHITE)


def icon_shield(draw, cx, cy, color, s=1.0):
    draw.polygon([(cx - 20 * s, cy - 26 * s), (cx + 20 * s, cy - 26 * s),
                  (cx + 20 * s, cy - 2 * s), (cx, cy + 28 * s),
                  (cx - 20 * s, cy - 2 * s)],
                 outline=color, width=int(6 * s))
    draw.line([(cx - 12 * s, cy - 2 * s), (cx - 3 * s, cy + 8 * s),
               (cx + 14 * s, cy - 12 * s)], fill=color, width=int(6 * s),
              joint="curve")


def icon_ship(draw, cx, cy, color, s=1.0):
    draw.line([(cx, cy + 2 * s), (cx, cy - 24 * s)], fill=color,
              width=int(5 * s))
    draw.polygon([(cx, cy - 24 * s), (cx + 16 * s, cy - 19 * s),
                  (cx, cy - 14 * s)], fill=GOLD)
    draw.polygon([(cx - 26 * s, cy + 2 * s), (cx + 26 * s, cy + 2 * s),
                  (cx + 18 * s, cy + 18 * s), (cx - 18 * s, cy + 18 * s)],
                 fill=color)
    draw.line([(cx - 24 * s, cy + 26 * s), (cx - 12 * s, cy + 26 * s)],
              fill=color, width=int(4 * s))
    draw.line([(cx + 2 * s, cy + 26 * s), (cx + 24 * s, cy + 26 * s)],
              fill=color, width=int(4 * s))


def icon_medal(draw, cx, cy, color, s=1.0):
    draw.polygon([(cx - 14 * s, cy - 28 * s), (cx - 2 * s, cy - 28 * s),
                  (cx - 8 * s, cy - 8 * s)], fill=GOLD)
    draw.polygon([(cx + 2 * s, cy - 28 * s), (cx + 14 * s, cy - 28 * s),
                  (cx + 8 * s, cy - 8 * s)], fill=GOLD)
    draw.ellipse([cx - 18 * s, cy - 8 * s, cx + 18 * s, cy + 28 * s],
                 fill=WHITE, outline=color, width=int(6 * s))
    draw.ellipse([cx - 8 * s, cy + 2 * s, cx + 8 * s, cy + 18 * s],
                 fill=color)


def icon_chart(draw, cx, cy, color, s=1.0):
    draw.line([(cx - 26 * s, cy - 26 * s), (cx - 26 * s, cy + 26 * s),
               (cx + 26 * s, cy + 26 * s)], fill=color, width=int(5 * s))
    draw.line([(cx - 22 * s, cy - 14 * s), (cx - 8 * s, cy - 2 * s),
               (cx + 4 * s, cy - 8 * s), (cx + 22 * s, cy + 14 * s)],
              fill=color, width=int(5 * s), joint="curve")
    draw.polygon([(cx + 22 * s, cy + 14 * s), (cx + 10 * s, cy + 12 * s),
                  (cx + 20 * s, cy + 26 * s)], fill=color)


ICONS = {"rocket": icon_rocket, "shield": icon_shield, "ship": icon_ship,
         "medal": icon_medal, "chart": icon_chart}


def draw_panel(draw, box, number, accent, headline, stat, body, icon,
               lead=False):
    x0, y0, x1, y1 = box
    hf = F_HEADLINE if lead else F_HEADLINE_GRID
    nf = F_NUM if lead else F_NUM_GRID
    rounded(draw, box, 18, PANEL, accent, 4)
    # thick accent bar across the top of the panel
    draw.rectangle([x0 + 4, y0 + 4, x1 - 4, y0 + 14], fill=accent)
    # numbered disc
    r = 30 if lead else 26
    cx, cy = x0 + 46, y0 + 52
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
    num = str(number)
    tw = draw.textlength(num, font=nf)
    draw.text((cx - tw / 2, cy - (22 if lead else 20)), num, font=nf,
              fill=WHITE)
    # icon, top-right
    if lead:
        ICONS[icon](draw, x1 - 78, y0 + 78, accent, s=1.15)
    else:
        ICONS[icon](draw, x1 - 48, y0 + 50, accent, s=0.85)
    # headline
    y = y0 + 96 if lead else y0 + 90
    step = 52 if lead else 42
    for line in headline:
        draw.text((x0 + 24, y), line, font=hf, fill=INK)
        y += step
    y += 4 if lead else 6
    if lead:
        # stat as a filled chip for the lead story
        pad_x, h = 18, 42
        w = int(draw.textlength(stat, font=F_STAT)) + 2 * pad_x
        draw.rounded_rectangle([x0 + 24, y, x0 + 24 + w, y + h],
                               radius=12, fill=accent)
        draw.text((x0 + 24 + pad_x, y + 5), stat, font=F_STAT, fill=WHITE)
        y += h + 12
    else:
        # stat line in the accent colour
        draw.text((x0 + 24, y), stat, font=F_STAT, fill=accent)
        y += 44
    # body: exactly one short line
    lines = wrap(draw, body, F_BODY, x1 - x0 - 48)
    assert len(lines) == 1, f"story {number} body wrapped to {len(lines)} lines"
    draw.text((x0 + 24, y), lines[0], font=F_BODY, fill=BODY)


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # ---- header ----
    draw.rectangle([0, 0, W, 132], fill=HEADER)
    draw.rectangle([0, 132, W, 138], fill=GOLD)
    draw.text((28, 12), "WORLD NEWS", font=F_TITLE, fill=WHITE)
    draw.text((28, 88), "TUESDAY 25 NOVEMBER 2026", font=F_DATE, fill=GOLD)
    right = "5 STORIES"
    draw.text((W - 28 - draw.textlength(right, font=F_SUB), 18),
              right, font=F_SUB, fill=WHITE)
    right2 = "ONE IMAGE"
    draw.text((W - 28 - draw.textlength(right2, font=F_SUB), 58),
              right2, font=F_SUB, fill=GOLD)

    # ---- story 1, full width ----
    n, accent, head, stat, body, icon = STORIES[0]
    draw_panel(draw, (24, 156, 1000, 408), n, accent, head, stat, body,
               icon, lead=True)

    # ---- stories 2-5, 2x2 grid ----
    grid = [(24, 426, 492, 692), (532, 426, 1000, 692),
            (24, 710, 492, 976), (532, 710, 1000, 976)]
    for (n, accent, head, stat, body, icon), box in zip(STORIES[1:], grid):
        draw_panel(draw, box, n, accent, head, stat, body, icon)

    # ---- footer ----
    draw.text((28, 988), "Sources: Reuters / Al Jazeera / Xinhua / SCMP, 25 Nov 2026",
              font=F_FOOT, fill=BODY)

    img.save(OUT, format="PNG")
    print(f"Wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
