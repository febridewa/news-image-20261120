#!/usr/bin/env python3
"""Draw the news-image-20261120 entry: one front page summing up the world
news of Friday 20 November 2026. Renders entry.png (1024x1024) beside this
file. All art is drawn in code with PIL; all text uses DejaVu fonts.
Supersampled 2x, then downscaled for clean edges.
Run: python3 draw.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

S = 2                      # supersample factor
W, H = 1024, 1024
M = 28                     # side margin
CW = W - 2 * M             # content width

PAPER = (248, 243, 230)
INK = (22, 35, 63)
RED = (166, 30, 34)
GOLD = (154, 123, 45)
GREY = (90, 86, 76)
PANEL = (255, 255, 255)
BORDER = (201, 194, 174)
TEAL = (31, 110, 107)
SKY = (213, 227, 235)

FD = "/usr/share/fonts/truetype/dejavu"


def F(size, bold=False, serif=False):
    name = ("DejaVuSerif-Bold.ttf" if serif and bold else
            "DejaVuSerif.ttf" if serif else
            "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(os.path.join(FD, name), int(size * S))


def rr(d, x, y, w, h, **kw):
    d.rectangle([x * S, y * S, (x + w) * S, (y + h) * S], **kw)


def ee(d, box, **kw):
    d.ellipse([v * S for v in box], **kw)


def ln(d, pts, **kw):
    d.line([(a * S, b * S) for a, b in pts], **kw)


def pg(d, pts, **kw):
    d.polygon([(a * S, b * S) for a, b in pts], **kw)


def ar(d, box, a0, a1, **kw):
    d.arc([v * S for v in box], a0, a1, **kw)


def tx(d, x, y, s, f, fill, anchor="la"):
    d.text((x * S, y * S), s, font=f, fill=fill, anchor=anchor)


def wrap(d, text, font, width):
    """Greedy word wrap; width in 1024-space px."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width * S:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, font, fill, leading):
    for i, s in enumerate(lines):
        tx(d, x, y + i * leading, s, font, fill)
    return y + len(lines) * leading


# ---------------------------------------------------------------- stories
HEROES = [
    dict(n=1, place="ODISHA", topic="CYCLONE", art="cyclone",
         title="Akvan comes ashore",
         deck="The severe cyclone crosses the coast near Gopalpur around noon, "
              "winds 90-100 km/h gusting to 110. 300,000 evacuated."),
    dict(n=2, place="WASHINGTON", topic="IRAN", art="calendar",
         title="Trump puts the Iran call off to 2027",
         deck="The president says there is no rush on Iran and he will 'see what happens' "
              "after January 1, pushing the decision into next year."),
    dict(n=3, place="MARKETS", topic="ASIA", art="markets",
         title="Asia's markets slide as the AI selloff deepens",
         deck="Seoul futures fall 3.7% and Samsung 4.2% before the bell; Wall Street's "
              "S&P 500 closed 2.02% lower, its sixth straight fall."),
    dict(n=4, place="RIYADH", topic="AFTERMATH", art="tower",
         title="First photos show Riyadh tower damage",
         deck="A day after Thursday's Houthi strike, Saudi Arabia releases images of the "
              "tower's shattered floors. No injuries."),
    dict(n=5, place="DEEP SPACE", topic="VOYAGER 1", art="voyager",
         title="Voyager 1 crosses one light-day",
         deck="NASA confirms the 1977 probe is now 25.9bn km out - a signal takes a full "
              "day to reach it."),
    dict(n=6, place="TOKYO", topic="SPACE", art="hayabusa",
         title="Hayabusa2 drops asteroid landing",
         deck="Engine trouble forces Japan's probe to abandon the asteroid landing it was "
              "built for."),
    dict(n=7, place="ANTALYA", topic="CLIMATE", art="cop31",
         title="COP31: fossil fuels divide talks",
         deck="A draft deal drops every fossil-fuel phase-out pledge as the final plenary meets."),
    dict(n=8, place="SEOUL", topic="LAW", art="court",
         title="Top court clears ex-PM Han",
         deck="Top court overturns Han Duck-soo's conviction."),
    dict(n=9, place="SUVA", topic="DROUGHT", art="fiji",
         title="Fiji declares a national disaster",
         deck="Drought and water shortages put Fiji in disaster."),
    dict(n=10, place="CRIMEA", topic="WAR", art="bridge",
         title="Bridge attack halts Crimea rail",
         deck="Ukrainian attack on the Kerch Bridge halts rail."),
    dict(n=11, place="CARACAS", topic="DIPLOMACY", art="flags",
         title="US-Venezuela restore military ties",
         deck="The two sides agree to restore military cooperation."),
    dict(n=12, place="NEW DELHI", topic="JUSTICE", art="gavel",
         title="Varma: resignation is not guilt",
         deck="Varma: his resignation is not an admission of guilt."),
]

ALSO = [
    "GTA VI sales pass $1.8bn, past The Odyssey",
    "GTA VI's NPCs: NPR on the game's characters",
    "Europe ready for talks with Russia on Ukraine",
    "Russian strikes damage Austrian, Dutch embassies",
    "North Korea expands uranium enrichment at Yongbyon",
    "Fire at Yunus's ancestral home; arson feared",
    "India v NZ: first Test begins; Nicholls 113 not out",
    "Bavuma ruled out of South Africa's Bangladesh decider",
    "Carlsen's shock forfeit leaves the chess world fuming",
    "Trump's election-security pick denies Jan 6 'attack'",
    "Sensex gains 1.21% on Thursday; Nifty up 1.14%",
    "Anthropic reportedly valued at $1.5 trillion",
    "India signs Rs 1,976-crore defence deal with Israel",
    "Women's Asian Hockey Champions Trophy begins",
    "India beat Malaysia in the Hong Kong Open badminton",
    "Arabian Aces v UAE Bulls in the Abu Dhabi T10",
    "Dow falls 1,084 on Thursday, its worst day of week",
    "World Children's Day marked around the globe",
    "EU-UK summit opens in Brussels",
    "Philippines and Chile sign a trade deal",
    "Migrant boat capsizes off Senegal; dozens missing",
    "Haiti approves a Salvadoran troop deal",
    "ADNOC vessel hit in Strait of Hormuz; one missing",
    "LPG tanker that sank off Bulgaria 'hit by projectiles'",
    "India launches its first home-made H5N1 vaccine",
    "US jobless claims 203,000 in the latest week",
    "NATO assembly opens its 72nd session",
    "Bayern Munich beat Koln 3-0",
    "Argentina 0-2 Australia in the U17 World Cup",
    "COP31: India presses for climate finance",
    "Amur falcons cross the Arabian Sea",
    "EU delays its methane rules by 24 months",
    "Merz hosts Qatar's emir in Berlin",
    "Azerbaijan's Aliyev visits Vietnam",
    "Youth anti-war protests held across Europe",
    "India electronics exports jump 44%",
    "ICRM completes 100 tech transfers",
    "Harimau Shakti exercise opens in Ipoh",
]

STATS = [
    ("300,000", "EVACUATED AHEAD OF AKVAN"),
    ("$1.8bn", "GTA VI SALES REPORTED"),
    ("25.9bn km", "VOYAGER 1 FROM EARTH"),
    ("90-100 km/h", "AKVAN WINDS AT LANDFALL"),
    ("-2.02%", "S&P 500'S THURSDAY CLOSE"),
]

# ---------------------------------------------------------------- art tiles
def art_cyclone(d, x, y, w, h):
    rr(d, x, y, w, h, fill=(168, 190, 205))
    rr(d, x, y + h * 0.62, w, h * 0.38, fill=(43, 111, 122))
    pg(d, [(x, y + h), (x + w * 0.42, y + h * 0.62), (x + w * 0.55, y + h),
           (x, y + h)], fill=(214, 190, 140))
    cx, cy = x + w * 0.62, y + h * 0.42
    for r, col in ((46, (255, 255, 255)), (36, (230, 238, 242)),
                   (26, (255, 255, 255)), (16, (240, 244, 246))):
        ar(d, (cx - r, cy - r * 0.7, cx + r, cy + r * 0.7), 200, 480,
           fill=col, width=3 * S)
    ee(d, (cx - 7, cy - 5, cx + 7, cy + 5), fill=(255, 255, 255))
    for rx in range(6):
        rx0 = x + 8 + rx * 16
        ln(d, [(rx0, y + 8), (rx0 - 5, y + 26)], fill=(255, 255, 255), width=2 * S)


def art_calendar(d, x, y, w, h):
    rr(d, x, y, w, h, fill=(22, 35, 63))
    px, py, pw, ph = x + w * 0.30, y + h * 0.14, w * 0.40, h * 0.74
    rr(d, px, py, pw, ph, fill=(255, 255, 255))
    rr(d, px, py, pw, ph * 0.22, fill=RED)
    tx(d, px + pw / 2, py + ph * 0.30, "2027", F(30, bold=True, serif=True),
       INK, anchor="ma")
    tx(d, px + pw / 2, py + ph * 0.72, "JAN 1", F(12, bold=True), RED, anchor="ma")
    ln(d, [(x + 12, y + h - 18), (x + w * 0.28, y + h - 18)],
       fill=(255, 255, 255), width=2 * S)
    ln(d, [(x + w - 12, y + 16), (x + w * 0.72, y + 16)],
       fill=(255, 255, 255), width=2 * S)


def art_markets(d, x, y, w, h):
    rr(d, x, y, w, h, fill=(18, 24, 38))
    base = y + h * 0.78
    xs = [x + 18 + i * 26 for i in range(9)]
    hs = [14, 20, 12, 24, 18, 30, 22, 34, 28]
    for i, (cx, ch) in enumerate(zip(xs, hs)):
        col = (46, 160, 90) if i % 3 == 0 else (200, 60, 55)
        rr(d, cx, base - ch - i * 3, 12, ch, fill=col)
        ln(d, [(cx + 6, base - ch - i * 3 - 6), (cx + 6, base - i * 3 + 4)],
           fill=col, width=2 * S)
    ln(d, [(x + 14, y + 18), (x + w - 14, base - 30)], fill=(240, 200, 60),
       width=3 * S)
    tx(d, x + w - 10, y + 6, "-2.02%", F(15, bold=True), (255, 255, 255),
       anchor="ra")


def art_tower(d, x, y, w, h):
    rr(d, x, y, w, h, fill=(16, 22, 48))
    ee(d, (x + w - 34, y + 6, x + w - 14, y + 24), fill=(235, 230, 200))
    for bx, bw, bhf in ((0, 34, 0.55), (40, 26, 0.72), (150, 30, 0.62),
                        (186, 40, 0.86), (232, 26, 0.58)):
        bh = h * bhf
        rr(d, x + bx, y + h - bh, bw, bh, fill=(38, 52, 84))
    tw, th = 46, h * 0.94
    tx_, ty = x + w * 0.40, y + h - th
    rr(d, tx_, ty, tw, th, fill=(58, 74, 110))
    wy = ty + 8
    while wy < y + h - 8:
        for wx in (tx_ + 8, tx_ + 20, tx_ + 32):
            rr(d, wx, wy, 6, 6, fill=(250, 210, 110))
        wy += 11
    rr(d, tx_, ty + th * 0.28, tw, 9, fill=(200, 70, 40))
    rr(d, tx_ - 4, ty + th * 0.28 + 4, tw + 8, 3, fill=(160, 50, 30))


def art_voyager(d, x, y, w, h):
    rr(d, x, y, w, h, fill=(8, 10, 22))
    import random
    rnd = random.Random(7)
    for _ in range(34):
        sx, sy = x + rnd.randint(2, w - 2), y + rnd.randint(2, h - 2)
        ee(d, (sx, sy, sx + 2, sy + 2), fill=(255, 255, 255))
    cx, cy = x + w * 0.60, y + h * 0.45
    pg(d, [(cx - 26, cy - 4), (cx + 26, cy - 14), (cx + 26, cy + 6),
           (cx - 26, cy + 12)], fill=(210, 170, 60))
    rr(d, cx - 34, cy - 5, 12, 10, fill=(230, 200, 90))
    ln(d, [(cx - 34, cy), (cx - 52, cy - 16)], fill=(200, 200, 200), width=2 * S)
    ln(d, [(cx - 52, cy - 16), (cx - 58, cy - 22)], fill=(200, 200, 200),
       width=2 * S)
    for i in range(5):
        ee(d, (x + 8 + i * 9, cy + 18, x + 12 + i * 9, cy + 22),
           fill=(150, 200, 230))
    tx(d, x + 8, y + 6, "25.9bn km", F(12, bold=True), (255, 255, 255))


def art_hayabusa(d, x, y, w, h):
    rr(d, x, y, w, h, fill=(12, 14, 26))
    ee(d, (x + w * 0.55, y + h * 0.30, x + w * 0.95, y + h * 0.85),
       fill=(150, 140, 125))
    ee(d, (x + w * 0.66, y + h * 0.45, x + w * 0.74, y + h * 0.55),
       fill=(120, 110, 95))
    ee(d, (x + w * 0.78, y + h * 0.60, x + w * 0.84, y + h * 0.68),
       fill=(120, 110, 95))
    px, py = x + w * 0.22, y + h * 0.30
    rr(d, px, py, 22, 12, fill=(210, 190, 80))
    pg(d, [(px + 22, py + 2), (px + 34, py - 6), (px + 34, py + 16),
           (px + 22, py + 10)], fill=(230, 210, 100))
    for i in range(6):
        t = i / 5
        dx = px + 30 + t * 60
        dy = py + 20 + t * t * 46
        ee(d, (dx, dy, dx + 3, dy + 3), fill=(220, 90, 70))
    tx(d, x + 8, y + 6, "NO LANDING", F(11, bold=True), (255, 255, 255))


def art_cop31(d, x, y, w, h):
    rr(d, x, y, w, h, fill=(178, 208, 224))
    ee(d, (x + w - 42, y + 8, x + w - 14, y + 36), fill=(245, 200, 60))
    cx, cy, r = x + w * 0.42, y + h * 0.55, 34
    ee(d, (cx - r, cy - r, cx + r, cy + r), fill=(52, 110, 180))
    pg(d, [(cx - 22, cy - 8), (cx - 4, cy - 18), (cx + 6, cy - 2),
           (cx - 8, cy + 10)], fill=(90, 170, 90))
    pg(d, [(cx + 10, cy + 8), (cx + 24, cy + 2), (cx + 20, cy + 18),
           (cx + 6, cy + 20)], fill=(90, 170, 90))
    for fx in (8, 34, 60):
        pg(d, [(x + fx, y + h - 26), (x + fx + 14, y + h - 26),
               (x + fx + 14, y + h - 12)], fill=(RED if fx == 34 else TEAL))
        ln(d, [(x + fx, y + h - 26), (x + fx, y + h - 40)], fill=INK, width=2 * S)


def art_court(d, x, y, w, h):
    rr(d, x, y, w, h, fill=(238, 230, 210))
    rr(d, x + 10, y + 10, w - 20, 8, fill=INK)
    for cx in (x + 22, x + w / 2 - 4, x + w - 30):
        rr(d, cx, y + 20, 8, h - 34, fill=(120, 100, 70))
    rr(d, x + 10, y + h - 16, w - 20, 6, fill=INK)
    mx, my = x + w * 0.68, y + h * 0.52
    ln(d, [(mx, my - 12), (mx, my + 14)], fill=INK, width=2 * S)
    ln(d, [(mx - 14, my - 12), (mx + 14, my - 12)], fill=INK, width=2 * S)
    pg(d, [(mx - 18, my - 10), (mx - 10, my - 10), (mx - 14, my - 2)],
       fill=GOLD)
    pg(d, [(mx + 10, my - 10), (mx + 18, my - 10), (mx + 14, my - 2)],
       fill=GOLD)


def art_fiji(d, x, y, w, h):
    rr(d, x, y, w, h, fill=(240, 226, 190))
    ee(d, (x + w - 44, y + 6, x + w - 16, y + 34), fill=(245, 190, 60))
    rr(d, x, y + h * 0.58, w, h * 0.42, fill=(170, 120, 70))
    for lx, ly in ((20, 30), (60, 38), (110, 30), (150, 40)):
        ln(d, [(x + lx, y + h * 0.60), (x + lx + 14, y + h * 0.60 + 10),
               (x + lx + 30, y + h * 0.60 + 4)], fill=(120, 80, 40),
           width=2 * S)
    pg(d, [(x + 18, y + 14), (x + 26, y + 26), (x + 10, y + 26)],
       fill=(60, 130, 200))


def art_bridge(d, x, y, w, h):
    rr(d, x, y, w, h, fill=(196, 216, 230))
    rr(d, x, y + h * 0.62, w, h * 0.38, fill=(70, 120, 160))
    for bx in (x + 18, x + w - 30):
        rr(d, bx, y + 10, 8, h * 0.55, fill=(90, 90, 100))
    ln(d, [(x, y + h * 0.42), (x + w * 0.44, y + h * 0.42)], fill=(70, 70, 80),
       width=4 * S)
    ln(d, [(x + w * 0.58, y + h * 0.42), (x + w, y + h * 0.42)],
       fill=(70, 70, 80), width=4 * S)
    pg(d, [(x + w * 0.44, y + h * 0.42), (x + w * 0.50, y + h * 0.30),
           (x + w * 0.58, y + h * 0.42)], fill=(150, 150, 160))
    ee(d, (x + w * 0.46, y + h * 0.16, x + w * 0.54, y + h * 0.28),
       fill=(200, 200, 200))


def art_flags(d, x, y, w, h):
    rr(d, x, y, w, h, fill=(236, 230, 210))
    for fx, cols in ((x + 14, None), (x + w * 0.52, "ven")):
        ln(d, [(fx + 4, y + 8), (fx + 4, y + h - 8)], fill=INK, width=2 * S)
        if cols is None:
            for i in range(7):
                rr(d, fx + 6, y + 10 + i * 5, 52, 5,
                   fill=(255, 255, 255) if i % 2 == 0 else (180, 40, 50))
            rr(d, fx + 6, y + 10, 22, 18, fill=(30, 50, 110))
        else:
            rr(d, fx + 6, y + 10, 52, 12, fill=(240, 200, 40))
            rr(d, fx + 6, y + 22, 52, 12, fill=(40, 80, 180))
            rr(d, fx + 6, y + 34, 52, 11, fill=(200, 50, 50))


def art_gavel(d, x, y, w, h):
    rr(d, x, y, w, h, fill=(238, 230, 210))
    rr(d, x + 12, y + 12, w - 24, h - 34, fill=(255, 255, 255),
       outline=BORDER, width=S)
    for ly in range(4):
        ln(d, [(x + 20, y + 20 + ly * 7), (x + w - 30, y + 20 + ly * 7)],
           fill=(150, 145, 130), width=S)
    ee(d, (x + w - 46, y + h - 30, x + w - 30, y + h - 14), fill=RED)
    rr(d, x + 22, y + h - 26, 40, 8, fill=(120, 85, 50))
    ln(d, [(x + 42, y + h - 26), (x + 58, y + h - 44)], fill=(120, 85, 50),
       width=3 * S)
    rr(d, x + 52, y + h - 52, 22, 10, fill=(140, 100, 60))

ART = {"cyclone": art_cyclone, "calendar": art_calendar,
       "markets": art_markets, "tower": art_tower,
       "voyager": art_voyager, "hayabusa": art_hayabusa,
       "cop31": art_cop31, "court": art_court, "fiji": art_fiji,
       "bridge": art_bridge, "flags": art_flags, "gavel": art_gavel}

# ---------------------------------------------------------------- world map
MAP_ROWS = {
    1: [(25, 27)], 2: [(8, 11), (24, 28)],
    3: [(3, 15), (24, 28), (40, 62)], 4: [(2, 16), (33, 37), (40, 63)],
    5: [(4, 19), (30, 31), (33, 37), (40, 62)],
    6: [(5, 20), (30, 31), (31, 38), (41, 62)],
    7: [(6, 20), (31, 38), (41, 62)], 8: [(7, 20), (31, 39), (42, 62)],
    9: [(8, 19), (32, 39), (43, 60)], 10: [(9, 17), (32, 40), (44, 58)],
    11: [(10, 15), (29, 40), (44, 57)], 12: [(11, 14), (29, 40), (45, 55)],
    13: [(12, 14), (30, 40), (46, 55)], 14: [(17, 25), (31, 39), (52, 56)],
    15: [(17, 26), (31, 39), (52, 57)], 16: [(18, 26), (32, 38), (53, 58)],
    17: [(18, 25), (32, 38), (55, 59)], 18: [(19, 25), (33, 38)],
    19: [(19, 24), (33, 37)], 20: [(19, 24), (33, 37), (52, 58)],
    21: [(20, 23), (34, 36), (52, 59)], 22: [(20, 23), (34, 36), (52, 59)],
    23: [(20, 22), (53, 58)], 24: [(21, 22), (53, 57)],
    25: [(21, 22)], 26: [(21, 22)], 27: [(21, 21)],
}
# (lon, lat) of the 12 picture stories
PINS = [(85, 20), (-77, 39), (-74, 41), (47, 25), (-118, 34), (139, 36),
        (31, 37), (127, 38), (178, -18), (34, 45), (-67, 10), (77, 29)]


def draw_map(d, x, y, w):
    rr(d, x, y, w, 138, fill=(226, 234, 240))
    step = w / 64.0
    for gy, spans in MAP_ROWS.items():
        for x0, x1 in spans:
            for gx in range(x0, x1 + 1):
                cx = x + gx * step + step / 2
                cy = y + gy * (138 / 32.0) + (138 / 32.0) / 2
                ee(d, (cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6),
                   fill=(120, 130, 140))
    for i, (lon, lat) in enumerate(PINS, 1):
        gx = (lon + 180) / 5.625
        gy = (85 - lat) / 4.7
        cx = x + gx * step
        cy = y + gy * (138 / 32.0)
        ee(d, (cx - 7, cy - 7, cx + 7, cy + 7), fill=RED)
        ee(d, (cx - 7, cy - 7, cx + 7, cy + 7), outline=(255, 255, 255),
           width=S)
        tx(d, cx, cy - 5, str(i), F(9, bold=True), (255, 255, 255),
           anchor="ma")


# ---------------------------------------------------------------- build
def hero_panel(d, x, y, w, h, st, big):
    rr(d, x, y, w, h, fill=PANEL, outline=BORDER, width=S)
    if big:
        aw, ah = w, 92
        tf, tl = F(19, bold=True, serif=True), 22
        df, dl = F(12), 15
        kf = F(11, bold=True)
        pad = 10
    elif w > 200:
        aw, ah = w, 58
        tf, tl = F(15, bold=True, serif=True), 18
        df, dl = F(11), 13.5
        kf = F(10, bold=True)
        pad = 8
    else:
        aw, ah = w, 42
        tf, tl = F(13.5, bold=True, serif=True), 16
        df, dl = F(10.5), 12.5
        kf = F(9, bold=True)
        pad = 7
    ART[st["art"]](d, x, y, aw, ah)
    tx(d, x + pad, y + ah + 6, "%d · %s — %s" % (st["n"], st["place"], st["topic"]),
       kf, RED)
    ty = y + ah + 6 + 14
    lines = wrap(d, st["title"], tf, w - 2 * pad)
    ty = draw_lines(d, x + pad, ty, lines[:3], tf, INK, tl)
    dlines = wrap(d, st["deck"], df, w - 2 * pad)
    draw_lines(d, x + pad, ty + 2, dlines[:3], df, (60, 58, 52), dl)


def main():
    img = Image.new("RGB", (W * S, H * S), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    tx(d, M, 12, "THE WORLD IN ONE DAY", F(14, bold=True), RED)
    tx(d, W - M, 14, "MORNING EDITION · 50 STORIES · 7 REGIONS", F(11, bold=True),
       INK, anchor="ra")
    ln(d, [(M, 34), (W - M, 34)], fill=INK, width=2 * S)

    # headline (auto-fit)
    size = 60
    while True:
        f = F(size, bold=True, serif=True)
        if d.textlength("Friday 20 November 2026", font=f) <= CW * S or size <= 40:
            break
        size -= 2
    tx(d, M, 40, "Friday 20 November 2026", f, INK)
    tx(d, M, 106, "Akvan comes ashore · Trump puts the Iran call off to 2027 · "
                  "Asia's markets slide again", F(18, serif=True), (70, 66, 58))

    # by-the-numbers strip
    colw = CW / 5.0
    for i, (num, lab) in enumerate(STATS):
        cx = M + i * colw
        tx(d, cx, 134, num, F(24, bold=True, serif=True), RED)
        tx(d, cx, 164, lab, F(9, bold=True), GREY)
    ln(d, [(M, 182), (W - M, 182)], fill=INK, width=2 * S)

    # hero rows
    y = 190
    hw, gap = 312, 16
    for i, st in enumerate(HEROES[:3]):
        hero_panel(d, M + i * (hw + gap), y, hw, 202, st, big=True)
    y = 398
    mw = 230
    for i, st in enumerate(HEROES[3:7]):
        hero_panel(d, M + i * (mw + gap), y, mw, 154, st, big=False)
    y = 560
    sw, sgap = 184, 12
    for i, st in enumerate(HEROES[7:12]):
        hero_panel(d, M + i * (sw + sgap), y, sw, 130, st, big=False)

    # bottom: map + also-on list
    y = 698
    rr(d, M, y, 296, 240, fill=PANEL, outline=BORDER, width=S)
    tx(d, M + 10, y + 8, "WHERE IT HAPPENED", F(12, bold=True), RED)
    tx(d, M + 10, y + 26, "pins 1-12 as numbered above", F(10), GREY)
    draw_map(d, M + 6, y + 46, 284)
    tx(d, M + 10, y + 192, "Red pins mark stories 1-12.", F(10), GREY)
    tx(d, M + 10, y + 208, "Grey dots mark the briefs 13-50.", F(10), GREY)
    tx(d, M + 10, y + 224, "Map: schematic, not to scale.", F(10), GREY)

    ax, aw = 336, 660
    rr(d, ax, y, aw, 240, fill=PANEL, outline=BORDER, width=S)
    tx(d, ax + 10, y + 8, "ALSO ON FRIDAY 20 NOVEMBER — 38 MORE STORIES",
       F(12, bold=True), RED)
    cols = [ALSO[:19], ALSO[19:]]
    for ci, col in enumerate(cols):
        cx = ax + 10 + ci * 330
        for ri, item in enumerate(col):
            n = 13 + ci * 19 + ri
            tx(d, cx, y + 30 + ri * 11, "%d  %s" % (n, item), F(10),
               (50, 48, 44))

    # date check
    y = 946
    rr(d, M, y, CW, 54, outline=RED, width=2 * S)
    tx(d, M + 10, y + 5, "DATE CHECK", F(12, bold=True), RED)
    tx(d, M + 108, y + 5,
       "Every story here happened or was first reported on Friday 20 November 2026.",
       F(11, bold=True), INK)
    excl = ("Left out - they broke on Thursday 19 Nov: the ICJ's genocide ruling on "
            "Myanmar · the Trump-Xi-Putin summit · the Houthi strike on Riyadh's PIF "
            "Tower (story 4 is Friday's follow-up: the first photos) · GTA VI's launch "
            "· Anthropic's Nasdaq debut · Denmark's Greenland deal.")
    elines = wrap(d, excl, F(10), CW - 20)
    draw_lines(d, M + 10, y + 21, elines[:2], F(10), (60, 58, 52), 13)

    # footer
    tx(d, M, 1004, "Sources: Reuters, AP, AFP, BBC, The Hindu, NDTV, NASA, IMD. "
                  "Original drawings. Morning edition - stories as reported by 01:00 UTC, 20 Nov 2026.",
       F(9.5), GREY)

    img = img.resize((W, H), Image.LANCZOS)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
