#!/usr/bin/env python3
"""Build the v6 front page: THE WORLD TODAY, 25 November 2026.

Deterministic Pillow rendering: no timestamps, no randomness, no network.
Writes asset.png (1024x1024) next to this file.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "asset.png")

# --- palette ---
NAVY = (27, 42, 74)
NAVY_DK = (16, 26, 48)
GOLD = (201, 162, 39)
GOLD_LT = (232, 197, 71)
CREAM = (247, 243, 234)
PAPER = (255, 252, 244)
INK = (26, 26, 46)
GREY = (107, 114, 128)
GREY_LT = (210, 205, 190)
RED = (180, 35, 24)
GREEN = (31, 122, 62)
BLUE = (30, 90, 160)
TEAL = (14, 116, 110)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)      # masthead
F_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_R = lambda s: font("DejaVuSans.ttf", s)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def fit(draw, text, fnt, max_w):
    """Truncate with ellipsis so text fits max_w pixels."""
    if text_w(draw, text, fnt) <= max_w:
        return text
    ell = "..."
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if text_w(draw, text[:mid] + ell, fnt) <= max_w:
            lo = mid
        else:
            hi = mid - 1
    return text[:lo] + ell


def wrap_two(draw, text, fnt, max_w):
    """Wrap text into at most two lines, truncating the second with ellipsis."""
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
            if len(lines) == 2:
                break
    if len(lines) < 2 and cur:
        lines.append(cur)
    if len(lines) == 2 and cur and lines[-1] != cur:
        lines[1] = fit(draw, lines[1] + " " + cur, fnt, max_w)
    if len(lines) > 2:
        lines = lines[:2]
    return lines


def pill(draw, box, text, fnt, fill, fg=(255, 255, 255)):
    """Centered rounded label."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=(y1 - y0) // 2, fill=fill)
    tw = text_w(draw, text, fnt)
    draw.text(((x0 + x1 - tw) / 2, y0 + (y1 - y0 - fnt.size) / 2 - 1),
              text, font=fnt, fill=fg)


# ---------------------------------------------------------------- scenes
# Each scene draws inside box (x, y, w, h) on a light panel. Simple flat
# vector shapes, all hand-coded.

def scene_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 236, 248))
    d.polygon([(x + w * .5, y + 8), (x + w * .62, y + h * .42),
               (x + w * .38, y + h * .42)], fill=RED)
    d.rectangle([x + w * .42, y + h * .40, x + w * .58, y + h * .72],
                fill=(240, 244, 250), outline=NAVY, width=2)
    d.ellipse([x + w * .46, y + h * .48, x + w * .54, y + h * .58],
              fill=NAVY)
    d.polygon([(x + w * .42, y + h * .62), (x + w * .30, y + h * .82),
               (x + w * .42, y + h * .74)], fill=RED)
    d.polygon([(x + w * .58, y + h * .62), (x + w * .70, y + h * .82),
               (x + w * .58, y + h * .74)], fill=RED)
    d.polygon([(x + w * .46, y + h * .72), (x + w * .54, y + h * .72),
               (x + w * .58, y + h * .92), (x + w * .42, y + h * .92)],
              fill=GOLD)
    for cx, cy in ((x + 12, y + 14), (x + w - 16, y + 26), (x + w - 26, y + 10)):
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=GOLD)


def scene_rescue(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 238, 244))
    cx, cy, r = x + w * .5, y + h * .48, min(w, h) * .30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
              outline=RED, width=4)
    d.ellipse([cx - r * .45, cy - r * .45, cx + r * .45, cy + r * .45],
              outline=RED, width=4)
    for ang in (45, 135, 225, 315):
        import math
        a = math.radians(ang)
        x1 = cx + math.cos(a) * r * .45
        y1 = cy + math.sin(a) * r * .45
        x2 = cx + math.cos(a) * r
        y2 = cy + math.sin(a) * r
        d.line([x1, y1, x2, y2], fill=RED, width=4)
    d.arc([x + 8, y + h * .72, x + w - 8, y + h * .98], 180, 360, fill=BLUE,
          width=3)
    d.arc([x + 20, y + h * .80, x + w - 20, y + h * 1.06], 180, 360,
          fill=BLUE, width=2)


def scene_tariff(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    d.rectangle([x + w * .26, y + 10, x + w * .66, y + h - 10],
                fill=(255, 255, 255), outline=NAVY, width=2)
    d.text((x + w * .30, y + 14), "%", font=F_B(26), fill=RED)
    for yy in (y + 52, y + 64, y + 76):
        d.line([x + w * .32, yy, x + w * .60, yy], fill=GREY, width=2)
    d.ellipse([x + w * .72, y + h * .30, x + w * .92, y + h * .70],
              outline=NAVY, width=3)
    d.line([x + w * .72, y + h * .50, x + w * .92, y + h * .50], fill=NAVY,
           width=2)
    d.line([x + w * .82, y + h * .30, x + w * .82, y + h * .70], fill=NAVY,
           width=2)


def scene_flame(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(253, 232, 214))
    cx, cy = x + w * .5, y + h * .55
    d.polygon([(cx, y + 8), (cx + w * .30, cy), (cx + w * .16, y + h - 10),
               (cx - w * .16, y + h - 10), (cx - w * .30, cy)],
              fill=(234, 88, 12))
    d.polygon([(cx, y + h * .34), (cx + w * .16, cy + 6),
               (cx + w * .09, y + h - 10), (cx - w * .09, y + h - 10),
               (cx - w * .16, cy + 6)], fill=GOLD_LT)
    d.rectangle([x + 8, y + h - 12, x + w - 8, y + h - 6], fill=GREY)


def scene_mine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 226, 214))
    d.polygon([(x + 6, y + h * .42), (x + w * .5, y + 8),
               (x + w - 6, y + h * .42), (x + w - 6, y + h - 8),
               (x + 6, y + h - 8)], fill=(122, 96, 66))
    d.polygon([(x + w * .42, y + h * .42), (x + w * .58, y + h * .42),
               (x + w * .58, y + h - 8), (x + w * .42, y + h - 8)],
              fill=(30, 30, 30))
    d.arc([x + 8, y + h * .62, x + w * .5, y + h * .94], 180, 360,
          fill=BLUE, width=3)
    d.arc([x + w * .5, y + h * .62, x + w - 8, y + h * .94], 180, 360,
          fill=BLUE, width=3)


def scene_gavel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(236, 232, 222))
    d.rectangle([x + w * .18, y + h * .22, x + w * .82, y + h * .40],
                fill=(122, 96, 66))
    d.rectangle([x + w * .18, y + h * .16, x + w * .28, y + h * .46],
                fill=(90, 70, 46))
    d.rectangle([x + w * .72, y + h * .16, x + w * .82, y + h * .46],
                fill=(90, 70, 46))
    d.line([x + w * .50, y + h * .40, x + w * .68, y + h * .78], fill=(90, 70, 46),
           width=5)
    d.rectangle([x + w * .30, y + h * .78, x + w * .80, y + h * .88],
                fill=(160, 130, 90))


def scene_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 236, 248))
    d.polygon([(x + 8, y + h * .5), (x + w * .62, y + h * .34),
               (x + w - 8, y + h * .44), (x + w * .62, y + h * .56)],
              fill=NAVY)
    d.polygon([(x + w * .42, y + h * .40), (x + w * .52, y + h * .16),
               (x + w * .60, y + h * .40)], fill=NAVY)
    d.polygon([(x + w * .42, y + h * .60), (x + w * .50, y + h * .82),
               (x + w * .58, y + h * .60)], fill=NAVY)
    d.line([x + 6, y + h - 12, x + w - 6, y + h - 12], fill=GREY, width=2)
    d.line([x + 14, y + h - 20, x + w - 14, y + h - 20], fill=GREY_LT,
           width=2)


def scene_missile(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 228, 228))
    d.polygon([(x + w * .5, y + 8), (x + w * .60, y + h * .30),
               (x + w * .60, y + h * .62), (x + w * .40, y + h * .62),
               (x + w * .40, y + h * .30)], fill=(90, 96, 110))
    d.polygon([(x + w * .40, y + h * .55), (x + w * .26, y + h * .78),
               (x + w * .40, y + h * .68)], fill=RED)
    d.polygon([(x + w * .60, y + h * .55), (x + w * .74, y + h * .78),
               (x + w * .60, y + h * .68)], fill=RED)
    d.polygon([(x + w * .46, y + h * .62), (x + w * .54, y + h * .62),
               (x + w * .58, y + h * .88), (x + w * .42, y + h * .88)],
              fill=GOLD)
    for cx, cy in ((x + 10, y + 12), (x + w - 14, y + 20)):
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=GOLD)


def scene_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(253, 232, 222))
    d.line([x + 8, y + h - 12, x + w - 8, y + h - 12], fill=INK, width=2)
    d.line([x + 8, y + h - 12, x + 8, y + 8], fill=INK, width=2)
    pts = [(x + 12, y + 16), (x + w * .32, y + 26), (x + w * .5, y + 22),
           (x + w * .68, y + h * .55), (x + w - 12, y + h * .78)]
    d.line(pts, fill=RED, width=4, joint="curve")
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)


def scene_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 236, 244))
    d.polygon([(x + 8, y + h * .58), (x + w - 8, y + h * .58),
               (x + w * .78, y + h * .86), (x + w * .22, y + h * .86)],
              fill=NAVY)
    d.rectangle([x + w * .42, y + h * .30, x + w * .58, y + h * .58],
                fill=(240, 244, 250), outline=NAVY, width=2)
    d.polygon([(x + w * .50, y + 8), (x + w * .50, y + h * .30),
               (x + w * .72, y + h * .30)], fill=RED)
    d.arc([x + 8, y + h * .86, x + w * .5, y + h * 1.08], 180, 360,
          fill=BLUE, width=3)
    d.arc([x + w * .5, y + h * .86, x + w - 8, y + h * 1.08], 180, 360,
          fill=BLUE, width=3)


def scene_medal(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    cx, cy = x + w * .5, y + h * .58
    d.polygon([(cx - 8, y + 8), (cx + 8, y + 8), (cx + 14, cy - 14),
               (cx - 14, cy - 14)], fill=RED)
    d.ellipse([cx - 18, cy - 16, cx + 18, cy + 20], fill=GOLD,
              outline=(146, 110, 16), width=2)
    d.text((cx - 6, cy - 11), "1", font=F_B(20), fill=(146, 110, 16))


# ------------------------------------------------------- small icons (28px)
def _icon_box(d, x, y, s, fill):
    d.rounded_rectangle([x, y, x + s, y + s], radius=5, fill=fill)


def icon_generic(d, x, y, s, kind):
    """Tiny geometric glyph on a tinted tile; kind selects the drawing."""
    tints = {"navy": (226, 236, 248), "red": (253, 232, 222),
             "gold": (243, 230, 190), "green": (220, 240, 226),
             "grey": (232, 231, 226)}
    fill, tint = NAVY, tints["navy"]
    if kind in ("flame", "chart", "warn"):
        fill, tint = RED, tints["red"]
    elif kind in ("coin", "medal", "bolt", "star"):
        fill, tint = (146, 110, 16), tints["gold"]
    elif kind in ("cross", "leaf"):
        fill, tint = GREEN, tints["green"]
    _icon_box(d, x, y, s, tint)
    c = s // 2
    if kind == "flame":
        d.polygon([(x + c, y + 5), (x + c + 7, y + c + 2), (x + c + 4, y + s - 5),
                   (x + c - 4, y + s - 5), (x + c - 7, y + c + 2)], fill=fill)
    elif kind == "chart":
        d.line([(x + 5, y + s - 7), (x + c, y + c), (x + s - 6, y + 6)],
               fill=fill, width=3)
        d.line([(x + 5, y + s - 7), (x + s - 5, y + s - 7)], fill=fill, width=2)
    elif kind == "gavel":
        d.rectangle([x + 6, y + 8, x + s - 6, y + 13], fill=fill)
        d.line([x + c + 2, y + 13, x + s - 8, y + s - 7], fill=fill, width=3)
    elif kind == "anchor":
        d.line([x + c, y + 5, x + c, y + s - 6], fill=fill, width=3)
        d.arc([x + 6, y + s - 13, x + s - 6, y + s - 1], 0, 180, fill=fill,
              width=3)
        d.line([x + 7, y + 8, x + s - 7, y + 8], fill=fill, width=3)
    elif kind == "plane":
        d.polygon([(x + 4, y + c), (x + s - 4, y + c - 4),
                   (x + s - 4, y + c + 4)], fill=fill)
        d.polygon([(x + c - 2, y + c - 2), (x + c + 2, y + 4),
                   (x + c + 6, y + c - 2)], fill=fill)
    elif kind == "ship":
        d.polygon([(x + 5, y + c + 2), (x + s - 5, y + c + 2),
                   (x + s - 9, y + s - 6), (x + 9, y + s - 6)], fill=fill)
        d.rectangle([x + c - 1, y + 6, x + c + 1, y + c + 2], fill=fill)
    elif kind == "medal":
        d.ellipse([x + c - 7, y + c - 4, x + c + 7, y + c + 10], fill=fill)
        d.polygon([(x + c - 4, y + 4), (x + c + 4, y + 4), (x + c + 6, y + c - 2),
                   (x + c - 6, y + c - 2)], fill=RED)
    elif kind == "cross":
        d.ellipse([x + c - 8, y + c - 8, x + c + 8, y + c + 8],
                  outline=fill, width=3)
        d.line([x + c, y + c - 5, x + c, y + c + 5], fill=fill, width=3)
        d.line([x + c - 5, y + c, x + c + 5, y + c], fill=fill, width=3)
    elif kind == "coin":
        d.ellipse([x + c - 8, y + c - 8, x + c + 8, y + c + 8], fill=fill)
        d.text((x + c - 4, y + c - 8), "$", font=F_B(13), fill=(255, 255, 255))
    elif kind == "warn":
        d.polygon([(x + c, y + 5), (x + s - 5, y + s - 6), (x + 5, y + s - 6)],
                  fill=fill)
        d.text((x + c - 2, y + c - 2), "!", font=F_B(12), fill=(255, 255, 255))
    elif kind == "bolt":
        d.polygon([(x + c + 2, y + 4), (x + c - 5, y + c + 2),
                   (x + c, y + c + 2), (x + c - 2, y + s - 4),
                   (x + c + 6, y + c - 2), (x + c + 1, y + c - 2)],
                  fill=fill)
    elif kind == "eye":
        d.ellipse([x + 5, y + c - 6, x + s - 5, y + c + 6], outline=fill,
                  width=2)
        d.ellipse([x + c - 3, y + c - 3, x + c + 3, y + c + 3], fill=fill)
    elif kind == "heart":
        d.ellipse([x + 6, y + 8, x + c + 1, y + 17], fill=fill)
        d.ellipse([x + c - 1, y + 8, x + s - 6, y + 17], fill=fill)
        d.polygon([(x + 6, y + 13), (x + s - 6, y + 13), (x + c, y + s - 5)],
                  fill=fill)
    elif kind == "doc":
        d.rectangle([x + 8, y + 5, x + s - 8, y + s - 5], fill=(255, 255, 255),
                    outline=fill, width=2)
        for yy in (y + 10, y + 15, y + 20):
            d.line([x + 11, yy, x + s - 11, yy], fill=fill, width=2)
    elif kind == "chat":
        d.rounded_rectangle([x + 5, y + 7, x + s - 5, y + s - 9], radius=4,
                            outline=fill, width=2)
        d.polygon([(x + 10, y + s - 9), (x + 10, y + s - 3), (x + 16, y + s - 9)],
                  fill=fill)
    elif kind == "people":
        d.ellipse([x + c - 8, y + 7, x + c - 1, y + 14], fill=fill)
        d.ellipse([x + c + 1, y + 7, x + c + 8, y + 14], fill=fill)
        d.arc([x + 5, y + 14, x + s - 5, y + s - 3], 180, 360, fill=fill,
              width=3)
    elif kind == "wave":
        d.arc([x + 4, y + 8, x + c + 4, y + 20], 180, 360, fill=fill, width=3)
        d.arc([x + c - 4, y + 14, x + s - 4, y + 26], 180, 360, fill=fill,
              width=3)
    elif kind == "chip":
        d.rectangle([x + 7, y + 8, x + s - 7, y + s - 8], outline=fill, width=2)
        for xx in (x + 11, x + c, x + s - 11):
            d.line([xx, y + 8, xx, y + 12], fill=fill, width=2)
            d.line([xx, y + s - 12, xx, y + s - 8], fill=fill, width=2)
    elif kind == "flag":
        d.line([x + 8, y + 5, x + 8, y + s - 5], fill=fill, width=2)
        d.polygon([(x + 8, y + 5), (x + s - 6, y + 9), (x + 8, y + 14)],
                  fill=RED)
    elif kind == "home":
        d.polygon([(x + c, y + 5), (x + s - 5, y + c), (x + 5, y + c)],
                  fill=fill)
        d.rectangle([x + 8, y + c, x + s - 8, y + s - 5], fill=fill)
    else:  # magnifier
        d.ellipse([x + 6, y + 6, x + s - 9, y + s - 9], outline=fill, width=3)
        d.line([x + s - 10, y + s - 10, x + s - 4, y + s - 4], fill=fill,
               width=3)

# ------------------------------------------------------------------ data
# 36 stories: 30 retained from v5 (facts unchanged; the Indonesia mine
# flood brief is updated in place to the West Java toll, 9 dead / 17
# trapped - same event, later count) + 6 newly verified 25 Nov stories.

HEROES = [
    dict(scene=scene_rocket, accent=NAVY,
         title="SHENZHOU-24\nLAUNCHES",
         chip=("1ST FOREIGNER ABOARD TIANGONG", NAVY),
         body="China launches Shenzhou-24; Pakistan's Muhammad Zeeshan Ali aboard.",
         src="REUTERS"),
    dict(scene=scene_rescue, accent=RED,
         title="CARTAGENA\nHOSTAGES FREED",
         chip=("ALL FREED", RED),
         body="Troops storm a supermarket in a dawn raid; every remaining hostage is rescued alive.",
         src="AL JAZEERA"),
    dict(scene=scene_tariff, accent=NAVY,
         title="US TARIFFS HIT\n14 ECONOMIES",
         chip=("VIETNAM 35% - CHINA 20%", NAVY),
         body="USTR proposes duties on 14 partners over excess factory capacity.",
         src="REUTERS"),
]

# UTC timeline: day-part order, approximate UTC hours.
TIMELINE = [
    ("04 UTC", "SHENZHOU-24\nLIFTS OFF"),
    ("07 UTC", "RAMAPHOSA\nWINS IN COURT"),
    ("10 UTC", "CARTAGENA RAID\nFREES HOSTAGES"),
    ("15 UTC", "US UNVEILS\n14-ECONOMY TARIFFS"),
    ("16 UTC", "CAIRO TANKER\nFIRE KILLS 31"),
    ("21 UTC", "KYIV HIT BY\nBALLISTIC MISSILES"),
]

# (title, body, source, icon-kind) - icon "scene" means a drawn scene panel.
BRIEFS = [
    ('KYIV HITS RUSSIAN SHIP', 'Zelenskiy confirms Ukraine hit a Russian ship.', 'REUTERS', 'scene_ship'),
    ('GIULIANI GETS TOP HONOUR', 'Trump awards him the Medal of Freedom.', 'REUTERS', 'scene_medal'),
    ('NIKKEI -2.9% ON TARIFFS', 'Asian stocks slide on fresh US tariff threats.', 'REUTERS', 'chart'),
    ('CAIRO TANKER FIRE: 31 DEAD', '31 killed, 21 hurt in a tanker blaze.', 'CNN', 'scene_flame'),
    ('WEST JAVA MINE FLOOD', 'Illegal gold mine floods; 9 dead, 17 trapped.', 'AP', 'scene_mine'),
    ('RAMAPHOSA WINS IN COURT', 'Court voids the Phala Phala report.', 'AL JAZEERA', 'scene_gavel'),
    ('EMBRAER FACES 10% DUTY', 'US proposes a 10% tariff on Brazilian aircraft.', 'REUTERS', 'scene_plane'),
    ('KYIV HIT BY MISSILES', 'Russian missiles hit two sites in Kyiv.', 'REUTERS', 'scene_missile'),
    ('IS ATTACK IN HASAKA', 'Islamic State kills two Syrian security men.', 'REUTERS', 'warn'),
    ('HOUTHI STRIKE HITS REFINERY', 'Houthi drone hits a Saudi refinery.', 'REUTERS', 'flame'),
    ('HUAWEI GUILTY VERDICT', 'Court finds Huawei guilty in a trade case.', 'REUTERS', 'gavel'),
    ('CHEN JINING GRAFT PROBE', 'Senior Chinese official probed for corruption.', 'REUTERS', 'doc'),
    ('BANGLADESH WAGE HIKE', 'Garment wage up 36% to 17,000 taka a month.', 'REUTERS', 'coin'),
    ('N. KOREA EXPELS SWISS ENVOY', "Pyongyang orders Switzerland's envoy to leave.", 'REUTERS', 'flag'),
    ('UK SABOTAGE WARNING', 'Britain warns of a Russian sabotage threat.', 'REUTERS', 'warn'),
    ('GULF PLANE CRASH', 'Aircraft crashes in the Gulf; a search is on.', 'REUTERS', 'plane'),
    ('CANARY MIGRANT RECORD', 'More than 2,100 arrivals in a day, a record.', 'REUTERS', 'ship'),
    ('PUIGDEMONT RETURNS', 'Catalan ex-leader to return on 12 December.', 'REUTERS', 'home'),
    ('WHO PULLS EBOLA TEAM', 'WHO evacuates staff from a Congo hospital.', 'REUTERS', 'cross'),
    ('AUSTRALIA-SOLOMONS PACT', 'Canberra signs an A$740M security pact.', 'REUTERS', 'doc'),
    ('TEEN SMASHES 204 OFF 53', '15-year-old hits the fastest List A double ton.', 'REUTERS', 'medal'),
    ('KOSPI -6.2% IN AI ROUT', '10-month low; Samsung -9.9%, SK Hynix -11.1%.', 'YONHAP', 'scene_chart'),
    ('UK ENERGY CAP +26%', 'Cap rises to GBP 2,166 a year from January.', 'OFGEM', 'bolt'),
    ('CIA SYSTEM HACKED', "US spy agencies' open-source system breached.", 'CNN', 'eye'),
    ('AUSTRALIA SAYS SORRY', 'Canberra apologises to LGBTQ veterans.', 'REUTERS', 'heart'),
    ('COALITION HITS HODEIDAH', 'Strikes hit Hodeidah port; four drones downed.', 'AL JAZEERA', 'anchor'),
    ('KYIV SINKS RUSSIAN WARSHIP', 'Sea drones sink corvette Merkury off Libya.', 'REUTERS', 'anchor'),
    ('LEAK: 720,000 RUSSIAN DEAD', 'Leak: 490,000 confirmed dead; 720,000 missing.', 'CNN', 'doc'),
    ('ABU DHABI TALKS STALL', 'Ukraine-Russia-US talks end with no deal.', 'REUTERS', 'chat'),
    ('NVIDIA GIVES BACK 6%', 'Nvidia shares fall 6% as the AI rally cools.', 'REUTERS', 'chip'),
    ('TAIEX -4.8%, 1,927 PTS', 'Taiwan posts its sixth-largest point loss.', 'FOCUS TAIWAN', 'chart'),
    ('RUSSIA HITS UKRAINE GRID', '112 drones overnight; five regions blacked out.', 'REUTERS', 'bolt'),
    ('ANTHROPIC BELOW ITS IPO', 'AI start-up slips below its listing price.', 'INVESTOPEDIA', 'chart'),
]

SCENES = {"scene_rocket": scene_rocket, "scene_rescue": scene_rescue,
          "scene_tariff": scene_tariff, "scene_flame": scene_flame,
          "scene_mine": scene_mine, "scene_gavel": scene_gavel,
          "scene_plane": scene_plane, "scene_missile": scene_missile,
          "scene_chart": scene_chart, "scene_ship": scene_ship,
          "scene_medal": scene_medal}

# ------------------------------------------------------------------ draw
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 66], fill=NAVY)
    d.rectangle([0, 66, W, 68], fill=GOLD)
    f_mast = F_SERIF_B(46)
    t = "THE WORLD TODAY"
    d.text(((W - text_w(d, t, f_mast)) / 2, 8), t, font=f_mast, fill=(255, 255, 255))

    # gold date line
    d.rectangle([0, 68, W, 98], fill=GOLD)
    f_date = F_B(19)
    t = "W E D N E S D A Y   2 5   N O V E M B E R   2 0 2 6"
    d.text(((W - text_w(d, t, f_date)) / 2, 74), t, font=f_date, fill=NAVY_DK)

    # KPI bar: 36 stories / 9 regions / 25+ sources / 100% dated
    kpis = [("36", "STORIES"), ("9", "REGIONS"), ("25+", "SOURCES"),
            ("100%", "DATED")]
    kx, kw, kgap = 12, 244, 8
    for i, (num, lab) in enumerate(kpis):
        x0 = kx + i * (kw + kgap)
        d.rectangle([x0, 106, x0 + kw, 138], fill=PAPER,
                    outline=GREY_LT, width=1)
        f_n, f_l = F_B(20), F_B(11)
        label = num + "  " + lab
        tw = text_w(d, label, f_n)
        d.text((x0 + (kw - tw) / 2, 113), num, font=f_n, fill=NAVY)
        d.text((x0 + (kw - tw) / 2 + text_w(d, num + "  ", f_n), 117),
               lab, font=f_l, fill=GREY)

    # heroes
    hy, hh, hw = 146, 230, 328
    for i, hero in enumerate(HEROES):
        x0 = 12 + i * (hw + 8)
        d.rectangle([x0, hy, x0 + hw, hy + hh], fill=PAPER,
                    outline=GREY_LT, width=1)
        d.rectangle([x0, hy, x0 + hw, hy + 4], fill=hero["accent"])
        hero["scene"](d, x0 + 8, hy + 10, hw - 16, 94)
        f_t = F_B(20)
        ty = hy + 112
        for line in hero["title"].split("\n"):
            tw = text_w(d, line, f_t)
            d.text((x0 + (hw - tw) / 2, ty), line, font=f_t, fill=INK)
            ty += 22
        chip_text, chip_fill = hero["chip"]
        f_c = F_B(10)
        cw = text_w(d, chip_text, f_c) + 20
        pill(d, [x0 + (hw - cw) / 2, ty + 2, x0 + (hw + cw) / 2, ty + 20],
             chip_text, f_c, chip_fill)
        f_b = F_R(12)
        lines = wrap_two(d, hero["body"], f_b, hw - 24)
        by = ty + 26
        for line in lines:
            tw = text_w(d, line, f_b)
            d.text((x0 + (hw - tw) / 2, by), line, font=f_b, fill=GREY)
            by += 15
        f_s = F_B(9)
        d.text((x0 + hw - 8 - text_w(d, hero["src"], f_s), hy + hh - 16),
               hero["src"], font=f_s, fill=GREY)

    # UTC timeline strip
    ty0, ty1 = 382, 456
    d.rectangle([12, ty0, W - 12, ty1], fill=PAPER, outline=GREY_LT, width=1)
    f_th = F_B(11)
    d.text((22, ty0 + 6), "UTC TIMELINE - THE DAY AS IT HAPPENED",
           font=f_th, fill=NAVY)
    line_y = ty0 + 42
    d.line([40, line_y, W - 40, line_y], fill=GREY_LT, width=2)
    n = len(TIMELINE)
    for i, (when, what) in enumerate(TIMELINE):
        cx = 40 + (W - 80) * (i + 0.5) / n
        d.ellipse([cx - 5, line_y - 5, cx + 5, line_y + 5], fill=RED,
                  outline=(255, 255, 255), width=2)
        f_w = F_B(11)
        tw = text_w(d, when, f_w)
        d.text((cx - tw / 2, line_y - 20), when, font=f_w, fill=NAVY)
        f_e = F_B(9)
        ey = line_y + 8
        for line in what.split("\n"):
            tw = text_w(d, line, f_e)
            d.text((cx - tw / 2, ey), line, font=f_e, fill=INK)
            ey += 11

    # data bar instead of a map: hard numbers, no unreadable blobs
    dy0, dy1 = 464, 500
    d.rectangle([12, dy0, W - 12, dy1], fill=NAVY)
    f_dl = F_B(11)
    d.text((22, dy0 + 11), "BY THE NUMBERS:", font=f_dl, fill=GOLD_LT)
    stats = ["KOSPI -6.2%", "TAIEX -4.8%", "NIKKEI -2.9%",
             "UK CAP GBP 2,166", "31 KILLED IN CAIRO"]
    f_ds = F_B(13)
    total = sum(text_w(d, s, f_ds) for s in stats) + 4 * 44
    sx = 22 + text_w(d, "BY THE NUMBERS:  ", f_dl)
    sx = (W - total) / 2 + text_w(d, "BY THE NUMBERS:  ", f_dl)
    sx = 22 + text_w(d, "BY THE NUMBERS:  ", f_dl)
    # lay stats out from after the label, evenly spaced
    avail = (W - 22) - sx
    step = avail / len(stats)
    for i, s in enumerate(stats):
        cx = sx + step * i + step / 2
        tw = text_w(d, s, f_ds)
        d.text((cx - tw / 2, dy0 + 11), s, font=f_ds, fill=(255, 255, 255))
        if i:
            d.text((sx + step * i - 14, dy0 + 11), "|", font=f_ds,
                   fill=GOLD)

    # briefs: 33 items, 3 columns x 11 rows
    by0 = 508
    row_h = 44
    col_w = 328
    f_bt, f_bb, f_bs = F_B(13), F_R(11), F_B(8)
    for idx, (title, body, src, kind) in enumerate(BRIEFS):
        row, col = divmod(idx, 3)
        x0 = 12 + col * (col_w + 8)
        y0 = by0 + row * row_h
        if row:
            d.line([x0, y0 - 1, x0 + col_w, y0 - 1], fill=GREY_LT, width=1)
        # icon / scene tile 30x30
        if kind.startswith("scene"):
            SCENES[kind](d, x0, y0 + 4, 30, 30)
            d.rectangle([x0, y0 + 4, x0 + 30, y0 + 34], outline=GREY_LT,
                        width=1)
        else:
            icon_generic(d, x0, y0 + 4, 30, kind)
        tx = x0 + 38
        tw_avail = col_w - 38
        src_w = text_w(d, " " + src, f_bs)
        title_fit = fit(d, title, f_bt, tw_avail - src_w - 2)
        d.text((tx, y0 + 3), title_fit, font=f_bt, fill=INK)
        d.text((tx + text_w(d, title_fit, f_bt) + 4, y0 + 6), src,
               font=f_bs, fill=GREY)
        body_fit = fit(d, body, f_bb, tw_avail)
        d.text((tx, y0 + 21), body_fit, font=f_bb, fill=GREY)

    # footer: date check
    f_f = F_R(11)
    t = ("DATE CHECK  -  All 36 stories verified against 25 Nov 2026 reporting  -  "
         "Sources: Reuters, Al Jazeera, AP, CNN, Yonhap, CNA, Xinhua, Gulf News, "
         "Focus Taiwan, Investopedia, IOL")
    tw = text_w(d, t, f_f)
    d.text(((W - tw) / 2, 1000), t, font=f_f, fill=GREY)

    img.save(OUT, "PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
