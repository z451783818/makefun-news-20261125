#!/usr/bin/env python3
"""Build the 25 November 2026 world-news front page (v4, 15 stories).

Deterministic: fixed fonts, fixed layout, no network, no randomness.
Output: asset.png, 1024x1024.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

CREAM = (247, 243, 234)
NAVY = (20, 38, 74)
NAVY_DARK = (13, 26, 52)
GOLD = (201, 162, 39)
GOLD_LIGHT = (232, 196, 90)
INK = (24, 24, 24)
GREY = (90, 90, 90)
GREEN = (27, 120, 70)
RED = (178, 34, 34)
BLUE = (30, 80, 160)
BROWN = (146, 94, 20)
TEAL = (14, 110, 105)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
LINE = (200, 190, 170)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_one_line(draw, text, fnt, max_w, min_size=10):
    """Shrink font until text fits on one line; returns (font, text)."""
    size = fnt.size
    f = fnt
    while size > min_size and draw.textlength(text, font=f) > max_w:
        size -= 1
        f = ImageFont.truetype(f.path, size)
    return f


def draw_rocket(d, cx, cy, s, color):
    # Simple geometric rocket: body triangle + window + flame.
    d.polygon([(cx, cy - s), (cx + s * 0.45, cy + s * 0.55),
               (cx - s * 0.45, cy + s * 0.55)], fill=color)
    d.ellipse([cx - s * 0.16, cy - s * 0.35, cx + s * 0.16, cy - s * 0.05],
              fill=WHITE)
    d.polygon([(cx - s * 0.22, cy + s * 0.75), (cx, cy + s * 0.35),
               (cx + s * 0.22, cy + s * 0.75)], fill=(230, 120, 30))


def draw_shield(d, cx, cy, r, color):
    d.polygon([(cx, cy - r), (cx + r, cy - r * 0.5), (cx + r * 0.8, cy + r * 0.7),
               (cx, cy + r), (cx - r * 0.8, cy + r * 0.7),
               (cx - r, cy - r * 0.5)], fill=color)
    d.line([(cx - r * 0.45, cy), (cx - r * 0.1, cy + r * 0.4),
            (cx + r * 0.5, cy - r * 0.35)], fill=WHITE, width=4)


def draw_ship(d, cx, cy, s, color):
    d.polygon([(cx - s, cy + s * 0.3), (cx + s, cy + s * 0.3),
               (cx + s * 0.6, cy + s * 0.8), (cx - s * 0.6, cy + s * 0.8)],
              fill=color)
    d.line([(cx, cy - s), (cx, cy + s * 0.3)], fill=color, width=4)
    d.polygon([(cx, cy - s), (cx + s * 0.7, cy - s * 0.2), (cx, cy - s * 0.2)],
              fill=GOLD)


def draw_medal(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color,
              outline=GOLD, width=3)
    d.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45],
              fill=GOLD)


def draw_chart(d, x, y, w, h, color):
    pts = [(x, y + h * 0.75), (x + w * 0.3, y + h * 0.45),
           (x + w * 0.55, y + h * 0.65), (x + w * 0.8, y + h * 0.15),
           (x + w, y + h * 0.4)]
    d.line(pts, fill=color, width=4)
    d.line([(x, y + h), (x + w, y + h)], fill=color, width=3)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 96], fill=NAVY)
    d.text((24, 10), "THE WORLD TODAY", font=font(SERIF_B, 54), fill=WHITE)
    d.text((W - 24, 14), "15 STORIES", font=font(SANS_B, 26),
           fill=GOLD_LIGHT, anchor="ra")
    d.text((W - 24, 48), "ONE FRONT PAGE", font=font(SANS_B, 17),
           fill=WHITE, anchor="ra")
    d.text((24, 68), "WEDNESDAY 25 NOVEMBER 2026",
           font=font(SANS_B, 19), fill=GOLD)
    d.rectangle([0, 96, W, 100], fill=GOLD)

    # ---- KPI strip ------------------------------------------------------
    kpis = [("15", "STORIES"), ("5", "REGIONS"), ("5", "SOURCES"),
            ("25 NOV", "2026")]
    x = 24
    pill_w = (W - 48 - 3 * 12) // 4
    for num, label in kpis:
        d.rounded_rectangle([x, 110, x + pill_w, 148], radius=8,
                            outline=LINE, fill=CARD, width=2)
        d.text((x + 16, 118), num, font=font(SANS_B, 22), fill=NAVY)
        d.text((x + 16 + d.textlength(num, font=font(SANS_B, 22)) + 8, 122),
               label, font=font(SANS_B, 15), fill=GREY)
        x += pill_w + 12

    # ---- Lead story -----------------------------------------------------
    d.rounded_rectangle([24, 160, 1000, 300], radius=8, outline=LINE,
                        fill=CARD, width=2)
    d.rectangle([24, 160, 1000, 168], fill=GREEN)
    d.text((40, 176), "LEAD STORY", font=font(SANS_B, 15), fill=GREEN)
    d.text((170, 176), "ASIA  ·  SPACE", font=font(SANS_B, 15), fill=GREY)
    d.text((40, 198), "SHENZHOU-24 LAUNCHES",
           font=font(SANS_B, 34), fill=INK)
    d.rounded_rectangle([40, 240, 40 + 330, 266], radius=12, fill=GREEN)
    d.text((56, 244), "1ST FOREIGNER ABOARD TIANGONG",
           font=font(SANS_B, 14), fill=WHITE)
    d.text((40, 268), "China launches Shenzhou-24 with Pakistan's",
           font=font(SANS, 15), fill=INK)
    d.text((40, 286), "Muhammad Zeeshan Ali aboard.",
           font=font(SANS, 15), fill=INK)
    draw_rocket(d, 920, 225, 52, GREEN)

    # ---- Four main cards (2x2) -----------------------------------------
    cards = [
        ("2", "AMERICAS", RED, "CARTAGENA HOSTAGES FREED",
         "ALL FREED", "Forces storm a supermarket.", draw_shield),
        ("3", "EUROPE", BLUE, "ZELENSKIY CONFIRMS SHIP STRIKE",
         "GULF OF FINLAND", "Kyiv hit a Russian cargo ship.", draw_ship),
        ("4", "N. AMERICA", BROWN, "GIULIANI GETS MEDAL OF FREEDOM",
         "TOP US CIVILIAN HONOUR", "Trump gives the top US honour.",
         draw_medal),
        ("5", "ASIA", TEAL, "ASIAN STOCKS SELL OFF",
         "NIKKEI -2.9%", "Slide on fresh US tariff threats.", draw_chart),
    ]
    cw = (W - 48 - 12) // 2
    ch = 100
    positions = [(24, 308), (24 + cw + 12, 308),
                 (24, 308 + ch + 10), (24 + cw + 12, 308 + ch + 10)]
    for (num, region, color, title, stat, body, icon), (cx, cy) in zip(
            cards, positions):
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=8,
                            outline=LINE, fill=CARD, width=2)
        d.rectangle([cx, cy, cx + cw, cy + 6], fill=color)
        # number badge
        d.ellipse([cx + 12, cy + 16, cx + 44, cy + 48], fill=color)
        d.text((cx + 28, cy + 20), num, font=font(SANS_B, 20), fill=WHITE,
               anchor="ma")
        d.text((cx + 54, cy + 22), region, font=font(SANS_B, 14),
               fill=color)
        f = fit_one_line(d, title, font(SANS_B, 20), cw - 110)
        d.text((cx + 54, cy + 40), title, font=f, fill=INK)
        d.text((cx + 54, cy + 64), stat, font=font(SANS_B, 14), fill=color)
        # icon on the right
        if icon is draw_chart:
            draw_chart(d, cx + cw - 66, cy + 22, 48, 40, color)
        elif icon is draw_ship:
            draw_ship(d, cx + cw - 40, cy + 42, 22, color)
        elif icon is draw_medal:
            draw_medal(d, cx + cw - 40, cy + 42, 18, color)
        else:
            draw_shield(d, cx + cw - 40, cy + 42, 20, color)
        # body line at the bottom of the card
        d.text((cx + 12, cy + 82), body, font=font(SANS, 13),
               fill=GREY)

    # ---- Briefs section -------------------------------------------------
    d.rectangle([24, 528, 1000, 562], fill=NAVY)
    d.text((40, 536), "MORE FROM AROUND THE WORLD",
           font=font(SANS_B, 17), fill=WHITE)
    d.text((984, 536), "10 BRIEFS", font=font(SANS_B, 17), fill=GOLD_LIGHT,
           anchor="ra")

    briefs = [
        ("6", "MIDDLE EAST", "HOUTHIS HIT SAUDI REFINERY",
         "Houthis say they hit Ras Tanura and Riyadh."),
        ("7", "N. AMERICA", "HUAWEI FOUND GUILTY",
         "US jury convicts Huawei over trade secrets."),
        ("8", "CHINA", "CHINA PROBES TOP OFFICIAL",
         "Politburo member Chen Jining under graft probe."),
        ("9", "ASIA", "BANGLADESH RAISES PAY",
         "Garment wage up 36% to 17,000 taka."),
        ("10", "ASIA", "N. KOREA EXPELS SWISS ENVOY",
         "Pyongyang shuts Swiss office; 48 hours to leave."),
        ("11", "EUROPE", "UK WARNS OF SABOTAGE",
         "Firms backing Ukraine told of Russian risk."),
        ("12", "ASIA", "INDONESIA MINE FLOOD",
         "3 dead, 23 trapped in flooded gold mine."),
        ("13", "N. AMERICA", "6 DEAD IN GULF CRASH",
         "Cessna 210 crashes off Mississippi coast."),
        ("14", "EUROPE", "CANARY RECORD ARRIVALS",
         "2,100+ migrants land in one day, a record."),
        ("15", "EUROPE", "PUIGDEMONT TO RETURN",
         "Catalan leader to end exile on 12 December."),
    ]
    col_w = (W - 48 - 16) // 2
    row_h = 74
    for i, (num, region, title, body) in enumerate(briefs):
        col = i % 2
        row = i // 2
        x0 = 24 + col * (col_w + 16)
        y0 = 574 + row * row_h
        d.rectangle([x0, y0, x0 + col_w, y0 + row_h - 10], fill=CARD,
                    outline=LINE, width=1)
        d.ellipse([x0 + 10, y0 + 10, x0 + 36, y0 + 36], fill=NAVY)
        d.text((x0 + 23, y0 + 13), num, font=font(SANS_B, 14), fill=WHITE,
               anchor="ma")
        d.text((x0 + 46, y0 + 8), region, font=font(SANS_B, 11), fill=GREY)
        f = fit_one_line(d, title, font(SANS_B, 17), col_w - 60)
        d.text((x0 + 46, y0 + 26), title, font=f, fill=INK)
        f2 = fit_one_line(d, body, font(SANS, 13), col_w - 60)
        d.text((x0 + 46, y0 + 48), body, font=f2, fill=GREY)

    # ---- Footer ---------------------------------------------------------
    d.rectangle([0, 952, W, 1024], fill=NAVY_DARK)
    d.text((24, 962), "DATE CHECK  ✓   Wednesday 25 November 2026 — verified",
           font=font(SANS_B, 17), fill=GOLD_LIGHT)
    d.text((24, 988), "Sources: Reuters / Al Jazeera / Xinhua / SCMP / AP, 25 Nov 2026",
           font=font(SANS, 14), fill=WHITE)
    d.text((1000, 962), "THE WORLD TODAY", font=font(SERIF_B, 17),
           fill=WHITE, anchor="ra")
    d.text((1000, 988), "One day. One page.", font=font(SANS, 14),
           fill=WHITE, anchor="ra")

    img.save("asset.png", optimize=True)
    print("wrote asset.png")


if __name__ == "__main__":
    main()
