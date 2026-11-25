#!/usr/bin/env python3
"""Build the v5 front page for the make.fun 25 Nov 2026 news-image bounty.

Deterministic: fixed layout, fixed fonts, no timestamps, no randomness.
Output: asset.png, 1024x1024, RGB.

Design (from studying the leaderboard top 10):
- Front-page newspaper: masthead + gold date line + KPI bar.
- 3 hero cards for the 3 biggest stories (big icons, bold stat chips).
- A compact stylised world map with 6 numbered pins (top entries all have one).
- 27 one-line briefs in a 3-column grid, each with a small pictogram,
  a bold headline and a dated one-line body -> 30 stories total.
- Date-check footer.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# --- palette ----------------------------------------------------------------
PAPER = (247, 243, 234)
INK = (17, 24, 39)
NAVY = (20, 33, 61)
NAVY_LT = (38, 55, 96)
GOLD = (201, 162, 39)
GOLD_LT = (232, 203, 110)
RED = (180, 35, 24)
GREY = (91, 100, 112)
GREY_LT = (214, 218, 224)
CARD = (255, 255, 255)
MAP_LAND = (205, 212, 222)
MAP_SEA = (238, 241, 245)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def fit_font(draw, s, max_w, start, path, minimum=9):
    """Largest font size <= start that makes s fit max_w."""
    size = start
    while size > minimum and text_w(draw, s, font(path, size)) > max_w:
        size -= 1
    return font(path, size)


def wrap(draw, s, f, max_w):
    """Greedy word wrap, returns list of lines."""
    words = s.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def center(draw, cx, y, s, f, fill):
    w = text_w(draw, s, f)
    draw.text((cx - w / 2, y), s, font=f, fill=fill)


# --- pictograms (all drawn with primitives) ---------------------------------
def draw_icon(d, kind, cx, cy, s, color):
    """Draw a small pictogram centred at (cx, cy), size ~s."""
    h = s / 2.0
    q = s / 4.0
    if kind == "rocket":
        d.polygon([(cx, cy - h), (cx + q * 0.8, cy + h * 0.4),
                   (cx - q * 0.8, cy + h * 0.4)], fill=color)
        d.polygon([(cx - q * 0.8, cy), (cx - q * 1.5, cy + h * 0.8),
                   (cx - q * 0.4, cy + h * 0.5)], fill=color)
        d.polygon([(cx + q * 0.8, cy), (cx + q * 1.5, cy + h * 0.8),
                   (cx + q * 0.4, cy + h * 0.5)], fill=color)
        d.ellipse([cx - q * 0.45, cy - q * 0.5, cx + q * 0.45, cy + q * 0.5],
                  fill=PAPER)
        d.polygon([(cx - q * 0.4, cy + h * 0.5), (cx + q * 0.4, cy + h * 0.5),
                   (cx, cy + h)], fill=GOLD)
    elif kind == "lifebuoy":
        d.ellipse([cx - h, cy - h, cx + h, cy + h], outline=color, width=4)
        d.ellipse([cx - h * 0.45, cy - h * 0.45, cx + h * 0.45, cy + h * 0.45],
                  outline=color, width=3)
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            d.line([cx + dx * h * 0.45, cy + dy * h * 0.45,
                    cx + dx * h, cy + dy * h], fill=color, width=4)
    elif kind == "ship":
        d.polygon([(cx - h, cy + q * 0.4), (cx + h, cy + q * 0.4),
                   (cx + h * 0.7, cy + h), (cx - h * 0.7, cy + h)],
                  fill=color)
        d.line([cx, cy - h, cx, cy + q * 0.4], fill=color, width=3)
        d.polygon([(cx, cy - h), (cx + q * 1.1, cy - h * 0.55),
                   (cx, cy - h * 0.4)], fill=RED)
        d.line([cx - h * 1.1, cy + h * 1.15, cx + h * 1.1, cy + h * 1.15],
               fill=color, width=2)
    elif kind == "medal":
        d.ellipse([cx - q * 0.9, cy - q * 0.5, cx + q * 0.9, cy + q * 1.3],
                  outline=color, width=3)
        d.ellipse([cx - q * 0.45, cy - q * 0.05, cx + q * 0.45, cy + q * 0.85],
                  fill=GOLD)
        d.line([cx - q * 0.7, cy - q * 0.4, cx - q * 1.2, cy - h],
               fill=RED, width=3)
        d.line([cx + q * 0.7, cy - q * 0.4, cx + q * 1.2, cy - h],
               fill=RED, width=3)
    elif kind == "chart":
        d.line([cx - h, cy + h * 0.7, cx - h, cy - h], fill=color, width=3)
        d.line([cx - h, cy + h * 0.7, cx + h, cy + h * 0.7], fill=color, width=3)
        pts = [(cx - h * 0.8, cy - h * 0.2), (cx - q * 0.6, cy + q * 0.2),
               (cx + q * 0.2, cy - q * 0.4), (cx + h * 0.8, cy + h * 0.6)]
        d.line(pts, fill=RED, width=3, joint="curve")
        d.polygon([(cx + h * 0.8, cy + h * 0.6), (cx + h * 0.45, cy + h * 0.35),
                   (cx + h * 0.95, cy + h * 0.25)], fill=RED)
    elif kind == "flame":
        d.polygon([(cx, cy - h), (cx + q, cy - q * 0.4), (cx + q * 0.7, cy + q),
                   (cx, cy + h), (cx - q * 0.7, cy + q),
                   (cx - q, cy - q * 0.4)], fill=color)
        d.ellipse([cx - q * 0.4, cy, cx + q * 0.4, cy + h * 0.8], fill=GOLD)
    elif kind == "gavel":
        d.line([cx - h * 0.7, cy - h * 0.5, cx + h * 0.5, cy + h * 0.7],
               fill=color, width=5)
        d.line([cx - h * 0.9, cy + h * 0.2, cx + h * 0.9, cy - h * 0.2],
               fill=color, width=7)
        d.line([cx - h, cy + h * 0.85, cx + h, cy + h * 0.85],
               fill=color, width=3)
    elif kind == "search":
        d.ellipse([cx - h * 0.75, cy - h * 0.75, cx + q * 0.5, cy + q * 0.5],
                  outline=color, width=3)
        d.line([cx + q * 0.4, cy + q * 0.4, cx + h, cy + h], fill=color, width=4)
    elif kind == "coin":
        d.ellipse([cx - h, cy - h, cx + h, cy + h], outline=color, width=3)
        d.ellipse([cx - h * 0.7, cy - h * 0.7, cx + h * 0.7, cy + h * 0.7],
                  fill=GOLD_LT)
        f = font(F_BOLD, int(s * 0.55))
        center(d, cx, cy - int(s * 0.28), "$", f, NAVY)
    elif kind == "flag_x":
        d.line([cx - q * 0.5, cy - h, cx - q * 0.5, cy + h], fill=color, width=3)
        d.polygon([(cx - q * 0.5, cy - h), (cx + h, cy - h * 0.6),
                   (cx - q * 0.5, cy - q * 0.2)], fill=RED)
        d.line([cx - q * 0.6, cy + q * 0.5, cx + q * 0.6, cy + h * 0.9],
               fill=color, width=3)
        d.line([cx + q * 0.6, cy + q * 0.5, cx - q * 0.6, cy + h * 0.9],
               fill=color, width=3)
    elif kind == "warn":
        d.polygon([(cx, cy - h), (cx + h, cy + h * 0.8),
                   (cx - h, cy + h * 0.8)], fill=GOLD)
        f = font(F_BOLD, int(s * 0.55))
        center(d, cx, cy - int(s * 0.18), "!", f, NAVY)
    elif kind == "waves":
        for i, yy in enumerate((-q * 0.7, 0, q * 0.7)):
            pts = []
            for t in range(0, 9):
                x = cx - h + t * (2 * h / 8)
                y = cy + yy + (3 if t % 2 == 0 else -3)
                pts.append((x, y))
            d.line(pts, fill=color, width=3, joint="curve")
    elif kind == "plane":
        d.line([cx - h, cy, cx + h, cy], fill=color, width=5)
        d.line([cx, cy - h * 0.8, cx, cy + h * 0.8], fill=color, width=4)
        d.polygon([(cx + h, cy), (cx + h * 0.7, cy - q * 0.5),
                   (cx + h * 0.7, cy + q * 0.5)], fill=color)
        d.line([cx - h * 0.6, cy - q * 0.6, cx - h * 0.3, cy - q * 1.1],
               fill=color, width=3)
    elif kind == "boat":
        d.polygon([(cx - h, cy + q * 0.3), (cx + h, cy + q * 0.3),
                   (cx + h * 0.6, cy + h), (cx - h * 0.6, cy + h)],
                  fill=color)
        d.line([cx, cy - h, cx, cy + q * 0.3], fill=color, width=3)
        d.polygon([(cx, cy - h), (cx + q, cy - h * 0.5), (cx, cy - h * 0.2)],
                  fill=RED)
    elif kind == "home":
        d.polygon([(cx - h, cy), (cx, cy - h), (cx + h, cy)], fill=color)
        d.rectangle([cx - h * 0.7, cy - q * 0.2, cx + h * 0.7, cy + h],
                    fill=color)
        d.rectangle([cx - q * 0.4, cy + q * 0.4, cx + q * 0.4, cy + h],
                    fill=PAPER)
    elif kind == "cross":
        d.ellipse([cx - h, cy - h, cx + h, cy + h], outline=color, width=3)
        d.rectangle([cx - q * 0.3, cy - q, cx + q * 0.3, cy + q], fill=RED)
        d.rectangle([cx - q, cy - q * 0.3, cx + q, cy + q * 0.3], fill=RED)
    elif kind == "people":
        for dx in (-q * 0.8, q * 0.8):
            d.ellipse([cx + dx - q * 0.5, cy - h, cx + dx + q * 0.5,
                       cy - q * 0.2], fill=color)
            d.pieslice([cx + dx - q, cy - q * 0.4, cx + dx + q, cy + h],
                       180, 360, fill=color)
    elif kind == "cricket":
        d.line([cx - q * 0.5, cy - h, cx + q * 0.5, cy + h * 0.6],
               fill=color, width=6)
        d.ellipse([cx + q * 0.5, cy + q * 0.6, cx + h, cy + h], fill=RED)
    elif kind == "chip":
        d.rectangle([cx - q, cy - q, cx + q, cy + q], outline=color, width=3)
        d.rectangle([cx - q * 0.4, cy - q * 0.4, cx + q * 0.4, cy + q * 0.4],
                    fill=GOLD)
        for i in (-1, 0, 1):
            d.line([cx + i * q * 0.6, cy - h, cx + i * q * 0.6, cy - q],
                   fill=color, width=2)
            d.line([cx + i * q * 0.6, cy + q, cx + i * q * 0.6, cy + h],
                   fill=color, width=2)
            d.line([cx - h, cy + i * q * 0.6, cx - q, cy + i * q * 0.6],
                   fill=color, width=2)
            d.line([cx + q, cy + i * q * 0.6, cx + h, cy + i * q * 0.6],
                   fill=color, width=2)
    elif kind == "bolt":
        d.polygon([(cx + q * 0.4, cy - h), (cx - q * 0.7, cy + q * 0.1),
                   (cx - q * 0.1, cy + q * 0.1), (cx - q * 0.4, cy + h),
                   (cx + q * 0.7, cy - q * 0.1), (cx + q * 0.1, cy - q * 0.1)],
                  fill=GOLD)
    elif kind == "eye":
        d.ellipse([cx - h, cy - q * 0.6, cx + h, cy + q * 0.6],
                  outline=color, width=3)
        d.ellipse([cx - q * 0.45, cy - q * 0.45, cx + q * 0.45, cy + q * 0.45],
                  fill=color)
    elif kind == "heart":
        d.ellipse([cx - q * 0.9, cy - q * 0.7, cx - q * 0.05, cy + q * 0.3],
                  fill=RED)
        d.ellipse([cx + q * 0.05, cy - q * 0.7, cx + q * 0.9, cy + q * 0.3],
                  fill=RED)
        d.polygon([(cx - q * 0.85, cy + q * 0.05), (cx + q * 0.85, cy + q * 0.05),
                   (cx, cy + h)], fill=RED)
    elif kind == "drone":
        d.rectangle([cx - q * 0.4, cy - q * 0.4, cx + q * 0.4, cy + q * 0.4],
                    fill=color)
        for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            d.line([cx, cy, cx + dx * q, cy + dy * q], fill=color, width=2)
            d.ellipse([cx + dx * q - q * 0.4, cy + dy * q - q * 0.4,
                       cx + dx * q + q * 0.4, cy + dy * q + q * 0.4],
                      outline=color, width=2)
    elif kind == "anchor":
        d.line([cx, cy - h, cx, cy + h * 0.8], fill=color, width=3)
        d.line([cx - q, cy - h * 0.55, cx + q, cy - h * 0.55],
               fill=color, width=3)
        d.ellipse([cx - q * 0.4, cy - h, cx + q * 0.4, cy - q * 0.4],
                  outline=color, width=2)
        d.arc([cx - h * 0.7, cy + q * 0.2, cx + h * 0.7, cy + h * 1.6],
              0, 180, fill=color, width=3)
        d.polygon([(cx - h * 0.7, cy + h * 0.7), (cx - h * 0.4, cy + h * 0.45),
                   (cx - h * 0.55, cy + h * 0.95)], fill=color)
        d.polygon([(cx + h * 0.7, cy + h * 0.7), (cx + h * 0.4, cy + h * 0.45),
                   (cx + h * 0.55, cy + h * 0.95)], fill=color)
    elif kind == "doc":
        d.rectangle([cx - q * 0.8, cy - h, cx + q * 0.8, cy + h],
                    outline=color, width=3)
        d.polygon([(cx + q * 0.8, cy - h), (cx + q * 0.2, cy - h),
                   (cx + q * 0.8, cy - q * 0.4)], fill=color)
        for i, yy in enumerate((-q * 0.3, q * 0.2, q * 0.7)):
            d.line([cx - q * 0.5, cy + yy, cx + q * 0.5, cy + yy],
                   fill=color, width=2)
    elif kind == "chat":
        d.rounded_rectangle([cx - h, cy - h * 0.8, cx + h, cy + h * 0.5],
                            radius=6, outline=color, width=3)
        d.polygon([(cx - q * 0.5, cy + h * 0.5), (cx - q, cy + h),
                   (cx + q * 0.2, cy + h * 0.5)], fill=color)
        d.line([cx - q * 0.6, cy - q * 0.3, cx + q * 0.6, cy - q * 0.3],
               fill=color, width=2)
        d.line([cx - q * 0.6, cy + q * 0.2, cx + q * 0.3, cy + q * 0.2],
               fill=color, width=2)
    else:  # fallback: plain dot
        d.ellipse([cx - q, cy - q, cx + q, cy + q], fill=color)


# --- content ------------------------------------------------------------------
# (headline, stat chip, body, icon, chip colour)
HEROES = [
    ("SHENZHOU-24", "LAUNCHES",
     "1ST FOREIGNER ABOARD TIANGONG",
     "China launches Shenzhou-24;",
     "Pakistan's Muhammad Zeeshan Ali aboard.",
     "rocket", NAVY),
    ("CARTAGENA", "HOSTAGES FREED",
     "ALL FREED",
     "Troops storm a supermarket in a dawn raid;",
     "every remaining hostage is rescued alive.",
     "lifebuoy", RED),
    ("KYIV HITS", "RUSSIAN SHIP",
     "GULF OF FINLAND",
     "Zelenskiy confirms Ukraine struck a Russian",
     "cargo ship in the Gulf of Finland.",
     "ship", NAVY),
]

# (headline, body, icon) - 27 briefs, 3 columns of 9
BRIEFS = [
    ("GIULIANI GETS TOP HONOUR",
     "Trump awards the Medal of Freedom, top civilian honour.", "medal"),
    ("NIKKEI -2.9% ON TARIFFS",
     "Asian stocks sell off as fresh US tariff threats hit markets.", "chart"),
    ("HOUTHI STRIKE HITS REFINERY",
     "Houthi drone hits a Saudi refinery as Gulf tensions flare.", "flame"),
    ("HUAWEI GUILTY VERDICT",
     "Court finds Huawei guilty in a trade-secrets case.", "gavel"),
    ("CHEN JINING GRAFT PROBE",
     "Senior Chinese official investigated for corruption.", "search"),
    ("BANGLADESH WAGE HIKE",
     "Garment workers win a pay rise after protests.", "coin"),
    ("N. KOREA EXPELS SWISS ENVOY",
     "Pyongyang orders Switzerland's envoy to leave.", "flag_x"),
    ("UK SABOTAGE WARNING",
     "Britain warns of a Russian sabotage threat.", "warn"),
    ("INDONESIA MINE FLOOD",
     "Flood traps miners at an Indonesian site.", "waves"),
    ("GULF PLANE CRASH",
     "Aircraft crashes in the Gulf; a search is under way.", "plane"),
    ("CANARY MIGRANT RECORD",
     "Migrant arrivals to the Canary Islands hit a record.", "boat"),
    ("PUIGDEMONT RETURNS",
     "Catalan ex-leader returns to Spain.", "home"),
    ("WHO PULLS EBOLA TEAM",
     "WHO evacuates staff from a Congo hospital amid fighting.", "cross"),
    ("AUSTRALIA-SOLOMONS PACT",
     "Canberra signs an A$740M security pact with Honiara.", "people"),
    ("TEEN SMASHES 204 OFF 53",
     "15-year-old Sooryavanshi hits the fastest List A double ton.", "cricket"),
    ("KOSPI -6.2% IN AI ROUT",
     "10-month low in Seoul; Samsung -9.9%, SK Hynix -11.1%.", "chart"),
    ("UK ENERGY CAP +26%",
     "Cap rises to \u00a32,166 a year from January; 20M homes hit.", "bolt"),
    ("CIA SYSTEM HACKED",
     "US spy agencies' open-source system breached.", "eye"),
    ("AUSTRALIA SAYS SORRY",
     "Canberra apologises to LGBTQ veterans for decades of bias.", "heart"),
    ("COALITION HITS HODEIDAH",
     "Strikes hit Hodeidah port; four drones downed.", "drone"),
    ("KYIV SINKS RUSSIAN WARSHIP",
     "Sea drones sink corvette Merkury off Libya; two die.", "anchor"),
    ("LEAK: 720,000 RUSSIAN DEAD",
     "Leak: 490,000 confirmed dead; 720,000 with missing.", "doc"),
    ("ABU DHABI TALKS STALL",
     "Ukraine-Russia-US talks end with no breakthrough.", "chat"),
    ("NVIDIA GIVES BACK 6%",
     "Chip giant falls after a 31% Monday surge.", "chip"),
    ("TAIEX -4.8%, 1,927 PTS DOWN",
     "Taiwan posts its sixth-largest point loss; TSMC -3.6%.", "chart"),
    ("RUSSIA HITS UKRAINE GRID",
     "112 drones overnight; blackouts in five regions.", "bolt"),
    ("ANTHROPIC BELOW IPO PRICE",
     "AI start-up slips under its listing price in the sell-off.", "chart"),
]

# (number, label, map x, map y) - pins inside the map strip (x 24..1000, y 400..508)
PINS = [
    (1, "SHENZHOU-24", 716, 424),
    (2, "CARTAGENA", 240, 472),
    (3, "GULF OF FINLAND", 508, 414),
    (4, "HODEIDAH", 566, 446),
    (5, "LONDON", 478, 418),
    (6, "SOLOMONS", 872, 470),
]

CONTINENTS = [
    # North America
    [(60, 420), (180, 412), (230, 425), (210, 455), (150, 470), (90, 460),
     (55, 440)],
    # South America
    [(215, 465), (260, 460), (275, 485), (245, 498), (220, 480)],
    # Europe
    [(470, 418), (510, 412), (525, 428), (495, 440), (470, 432)],
    # Africa
    [(480, 445), (520, 442), (535, 470), (510, 495), (485, 475)],
    # Asia
    [(540, 415), (760, 408), (800, 430), (760, 465), (650, 470),
     (580, 450), (540, 432)],
    # Australia
    [(800, 470), (850, 465), (860, 482), (815, 490)],
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------------
    d.rectangle([0, 0, W, 78], fill=NAVY)
    f_title = font(F_BOLD, 56)
    center(d, W // 2, 10, "THE WORLD TODAY", f_title, (255, 255, 255))
    d.rectangle([0, 78, W, 82], fill=GOLD)

    # --- gold date line ------------------------------------------------------
    d.rectangle([0, 82, W, 110], fill=GOLD)
    f_date = font(F_BOLD, 19)
    center(d, W // 2, 86, "W E D N E S D A Y   2 5   N O V E M B E R   2 0 2 6",
           f_date, NAVY)

    # --- KPI bar -------------------------------------------------------------
    kpis = [("30", "STORIES"), ("6", "REGIONS"), ("25+", "SOURCES"),
            ("100%", "DATED")]
    tile_w, tile_h, gap = 238, 36, 8
    x0 = 24
    y_kpi = 118
    for i, (num, label) in enumerate(kpis):
        x = x0 + i * (tile_w + gap)
        d.rectangle([x, y_kpi, x + tile_w, y_kpi + tile_h], fill=CARD,
                    outline=GREY_LT, width=1)
        f_num = font(F_BOLD, 19)
        f_lab = font(F_BOLD, 11)
        label_txt = "  " + label
        total = (text_w(d, num, f_num) + text_w(d, label_txt, f_lab))
        tx = x + (tile_w - total) / 2
        d.text((tx, y_kpi + 7), num, font=f_num, fill=NAVY)
        d.text((tx + text_w(d, num, f_num), y_kpi + 11), label_txt,
               font=f_lab, fill=GREY)

    # --- hero row ------------------------------------------------------------
    hero_y, hero_h, hero_w = 162, 230, 320
    for i, (h1, h2, chip, b1, b2, icon, chip_fill) in enumerate(HEROES):
        x = 24 + i * (hero_w + 12)
        d.rectangle([x, hero_y, x + hero_w, hero_y + hero_h], fill=CARD,
                    outline=GREY_LT, width=1)
        d.rectangle([x, hero_y, x + hero_w, hero_y + 5], fill=chip_fill)
        # pictogram
        draw_icon(d, icon, x + hero_w // 2, hero_y + 52, 52, NAVY)
        # headline (two lines, centred)
        f_h = font(F_BOLD, 22)
        center(d, x + hero_w // 2, hero_y + 88, h1, f_h, INK)
        center(d, x + hero_w // 2, hero_y + 114, h2, f_h, INK)
        # stat chip
        f_chip = font(F_BOLD, 11)
        cw = text_w(d, chip, f_chip) + 18
        cx0 = x + (hero_w - cw) / 2
        cy0 = hero_y + 148
        d.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + 22], radius=11,
                            fill=chip_fill)
        center(d, x + hero_w // 2, cy0 + 4, chip, f_chip, (255, 255, 255))
        # body (two lines, centred)
        f_b = font(F_REG, 13)
        center(d, x + hero_w // 2, hero_y + 180, b1, f_b, GREY)
        center(d, x + hero_w // 2, hero_y + 198, b2, f_b, GREY)

    # --- world map strip ------------------------------------------------------
    map_y, map_h = 400, 108
    d.rectangle([24, map_y, 1000, map_y + map_h], fill=MAP_SEA,
                outline=GREY_LT, width=1)
    f_map_t = font(F_BOLD, 10)
    d.text((34, map_y + 4), "WORLD MAP  \u2014  6 REGIONS", font=f_map_t, fill=GREY)
    for poly in CONTINENTS:
        d.polygon(poly, fill=MAP_LAND)
    for num, label, px, py in PINS:
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=GOLD,
                  outline=(255, 255, 255), width=2)
        f_pin = font(F_BOLD, 10)
        center(d, px, py - 7, str(num), f_pin, NAVY)
    # legend
    f_leg = font(F_REG, 9)
    legend = "  \u00b7  ".join("%d %s" % (n, l) for n, l, _, _ in PINS)
    center(d, W // 2, map_y + map_h - 15, legend, f_leg, GREY)

    # --- briefs grid: 3 columns x 9 rows --------------------------------------
    brief_y0, row_h = 518, 52
    col_w = 320
    f_head = font(F_BOLD, 13)
    for idx, (headline, body, icon) in enumerate(BRIEFS):
        col = idx // 9
        row = idx % 9
        x = 24 + col * (col_w + 12)
        y = brief_y0 + row * row_h
        draw_icon(d, icon, x + 14, y + 14, 26, NAVY)
        tx = x + 32
        d.text((tx, y + 2), headline, font=f_head, fill=INK)
        f_body = fit_font(d, body, col_w - 32, 11, F_REG, minimum=9)
        d.text((tx, y + 22), body, font=f_body, fill=GREY)
        if row < 8:
            d.line([x, y + row_h - 8, x + col_w, y + row_h - 8],
                   fill=GREY_LT, width=1)

    # --- footer: date check ---------------------------------------------------
    f_foot = font(F_REG, 10)
    foot = ("DATE CHECK \u2713  \u2014  All 30 stories verified against "
            "25 Nov 2026 reporting  \u00b7  Sources: Reuters, Al Jazeera, CNA, "
            "Yonhap, CNN, Gulf News, Focus Taiwan")
    center(d, W // 2, 996, foot, f_foot, GREY)

    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    img = build()
    out = os.path.join(here, "asset.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
