#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news summary image (1024x1024 PNG).

Deterministic: same input always produces the same PNG bytes.
Run: python3 build_image.py  -> writes asset.png next to this script.
Only Pillow is needed, and only at build time; the entry program
(main.py) needs nothing but the Python standard library.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "asset.png")

W, H = 1024, 1024
BG = (250, 246, 236)          # warm paper
HEADER = (18, 28, 66)         # dark navy
GOLD = (232, 184, 84)
WHITE = (255, 255, 255)
INK = (24, 24, 24)
GREY = (84, 84, 84)
PANEL = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 56)
F_SUB = font("DejaVuSans-Bold.ttf", 30)
F_HEADLINE = font("DejaVuSans-Bold.ttf", 34)
F_HEADLINE_GRID = font("DejaVuSans-Bold.ttf", 29)
F_BODY = font("DejaVuSans.ttf", 26)
F_FOOT = font("DejaVuSans.ttf", 22)
F_NUM = font("DejaVuSans-Bold.ttf", 30)

# (number, accent colour, headline lines, body) for the five stories.
STORIES = [
    (1, (0, 110, 70), ["SHENZHOU-24 LAUNCHES"],
     "China launches Shenzhou-24 with Pakistan's Muhammad "
     "Zeeshan Ali, the first foreigner aboard Tiangong."),
    (2, (178, 44, 44), ["CARTAGENA HOSTAGES", "FREED"],
     "All hostages freed as forces storm a Cartagena supermarket."),
    (3, (20, 80, 150), ["ZELENSKIY CONFIRMS", "SHIP STRIKE"],
     "Ukraine's president confirms Kyiv hit a Russian cargo "
     "ship in the Gulf of Finland."),
    (4, (140, 90, 10), ["GIULIANI GETS MEDAL", "OF FREEDOM"],
     "Trump awards the top US civilian honour to Rudy Giuliani."),
    (5, (0, 110, 70), ["ASIAN STOCKS", "SELL OFF"],
     "Nikkei falls 2.9% as Asian markets slide on fresh US "
     "tariff threats."),
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


def draw_panel(draw, box, number, accent, headline, body, headline_font=None):
    x0, y0, x1, y1 = box
    hf = headline_font or F_HEADLINE
    rounded(draw, box, 18, PANEL, accent, 3)
    # accent bar across the top of the panel
    draw.rectangle([x0 + 4, y0 + 4, x1 - 4, y0 + 12], fill=accent)
    # numbered disc
    cx, cy, r = x0 + 46, y0 + 56, 26
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
    num = str(number)
    tw = draw.textlength(num, font=F_NUM)
    draw.text((cx - tw / 2, cy - 21), num, font=F_NUM, fill=WHITE)
    # headline
    y = y0 + 96
    for line in headline:
        draw.text((x0 + 24, y), line, font=hf, fill=INK)
        y += 40
    y += 6
    # body, wrapped to the panel width
    for line in wrap(draw, body, F_BODY, x1 - x0 - 48):
        draw.text((x0 + 24, y), line, font=F_BODY, fill=GREY)
        y += 34


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # ---- header ----
    draw.rectangle([0, 0, W, 118], fill=HEADER)
    draw.text((28, 14), "WORLD NEWS", font=F_TITLE, fill=WHITE)
    draw.text((28, 74), "TUESDAY 25 NOVEMBER 2026", font=F_SUB, fill=GOLD)
    right = "5 STORIES"
    draw.text((W - 28 - draw.textlength(right, font=F_SUB), 22),
              right, font=F_SUB, fill=WHITE)
    right2 = "ONE IMAGE"
    draw.text((W - 28 - draw.textlength(right2, font=F_SUB), 60),
              right2, font=F_SUB, fill=GOLD)

    # ---- story 1, full width ----
    n, accent, head, body = STORIES[0]
    draw_panel(draw, (24, 140, 1000, 360), n, accent, head, body)

    # ---- stories 2-5, 2x2 grid ----
    grid = [(24, 380, 492, 670), (532, 380, 1000, 670),
            (24, 690, 492, 970), (532, 690, 1000, 970)]
    for (n, accent, head, body), box in zip(STORIES[1:], grid):
        draw_panel(draw, box, n, accent, head, body,
                   headline_font=F_HEADLINE_GRID)

    # ---- footer ----
    draw.text((28, 986), "Sources: Reuters / Al Jazeera / Xinhua / SCMP, 25 Nov 2026",
              font=F_FOOT, fill=GREY)

    img.save(OUT, format="PNG")
    print(f"Wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
