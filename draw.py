#!/usr/bin/env python3
"""Thursday 26 November 2026 front page — fresh build for news-image-20261126.

Deterministic Pillow drawing: fixed content, no clock, no network.
Renders a 1024x1024 cream newspaper page with 13 illustrated main cards,
16 briefs, region chips, UTC timeline, numbers column, world map and a
DATE CHECK box, following the 22 Nov winner blueprint.
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

W = H = 1024
OUT = os.environ.get("ENTRY_OUT", "entry.png")

PAPER = (250, 246, 235)
INK = (18, 18, 18)
NAVY = (13, 33, 82)
RED = (190, 22, 22)
GREY = (105, 105, 105)
LIGHT = (235, 230, 216)
GREEN = (22, 122, 54)
BLUE = (28, 95, 184)
ORANGE = (214, 110, 12)
PURPLE = (106, 54, 148)
TEAL = (12, 125, 125)
YELLOW = (250, 199, 44)
SKY = (196, 225, 250)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_I = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def draw_wrap(draw, xy, text, font, fill, max_w, leading=None, max_lines=4):
    x, y = xy
    leading = leading or int(font.size * 1.18)
    for line in wrap(draw, text, font, max_w)[:max_lines]:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def badge(draw, x, y, label, colour):
    f = F(SANS_B, 11)
    w = int(draw.textlength(label, font=f)) + 12
    draw.rounded_rectangle([x, y, x + w, y + 19], radius=4, fill=colour)
    draw.text((x + 6, y + 3), label, font=f, fill=(255, 255, 255))
    return w


def illo_flame(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 40, 60))
    d.polygon([(x + w * .5, y + 4), (x + w * .72, y + h * .62), (x + w * .28, y + h * .62)], fill=(255, 120, 20))
    d.polygon([(x + w * .5, y + h * .30), (x + w * .62, y + h * .62), (x + w * .38, y + h * .62)], fill=(255, 205, 40))
    d.rectangle([x + 8, y + h * .68, x + w - 8, y + h * .78], fill=(120, 120, 130))
    for cx in (0.25, 0.5, 0.75):
        d.rectangle([x + w * cx - 9, y + h * .60, x + w * cx + 9, y + h * .70], fill=(30, 30, 30))


def illo_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h * .68, x + w, y + h], fill=(60, 130, 200))
    d.polygon([(x + 10, y + h * .68), (x + w - 10, y + h * .68), (x + w - 26, y + h * .85), (x + 26, y + h * .85)], fill=(150, 30, 30))
    for i, col in enumerate([(220, 80, 40), (40, 140, 80), (240, 180, 30), (60, 90, 200)]):
        d.rectangle([x + 16 + i * (w - 32) / 4, y + h * .38, x + 16 + (i + 1) * (w - 32) / 4 - 3, y + h * .66], fill=col)
    d.rectangle([x + w * .78, y + h * .22, x + w * .92, y + h * .40], fill=(240, 240, 240))


def illo_refinery(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 225, 190))
    d.ellipse([x + w * .72, y + 4, x + w * .95, y + h * .34], fill=(255, 190, 40))
    for fx in (0.18, 0.45, 0.72):
        d.rectangle([x + w * fx, y + h * .30, x + w * fx + 12, y + h * .88], fill=(90, 90, 100))
        d.ellipse([x + w * fx - 4, y + h * .10, x + w * fx + 18, y + h * .34], fill=(150, 150, 160))
    d.rectangle([x + 6, y + h * .80, x + w - 6, y + h * .92], fill=(70, 70, 80))
    d.polygon([(x + w * .45, y + h * .55), (x + w * .58, y + h * .82), (x + w * .32, y + h * .82)], fill=(255, 110, 20))


def illo_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(170, 210, 235))
    d.rectangle([x, y + h * .62, x + w, y + h], fill=(35, 100, 170))
    d.ellipse([x + w * .08, y + h * .42, x + w * .92, y + h * .72], fill=(200, 40, 40))
    d.rectangle([x + w * .70, y + h * .26, x + w * .88, y + h * .46], fill=(245, 245, 245))
    d.polygon([(x + w * .38, y + h * .60), (x + w * .52, y + h * .30), (x + w * .64, y + h * .60)], fill=(255, 140, 30))
    d.polygon([(x + w * .30, y + h * .62), (x + w * .44, y + h * .44), (x + w * .56, y + h * .62)], fill=(255, 200, 60))


def illo_factory(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 240, 220))
    d.rectangle([x + 10, y + h * .45, x + w - 10, y + h * .90], fill=(180, 90, 60))
    d.polygon([(x + 6, y + h * .48), (x + w * .35, y + h * .28), (x + w * .35, y + h * .48)], fill=(120, 60, 40))
    d.polygon([(x + w * .35, y + h * .48), (x + w * .62, y + h * .28), (x + w * .62, y + h * .48)], fill=(120, 60, 40))
    for wx in (0.22, 0.48, 0.74):
        d.rectangle([x + w * wx, y + h * .58, x + w * wx + 16, y + h * .74], fill=(255, 240, 170))
    d.rectangle([x + w * .78, y + h * .18, x + w * .88, y + h * .48], fill=(100, 100, 110))


def illo_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 64))
    for sx, sy in ((.15, .2), (.8, .15), (.65, .4), (.25, .55), (.9, .6)):
        d.ellipse([x + w * sx, y + h * sy, x + w * sx + 4, y + h * sy + 4], fill=(255, 255, 220))
    cx = x + w * .5
    d.polygon([(cx, y + 4), (cx + 13, y + h * .45), (cx - 13, y + h * .45)], fill=(240, 240, 245))
    d.rectangle([cx - 13, y + h * .45, cx + 13, y + h * .72], fill=(200, 205, 215))
    d.ellipse([cx - 6, y + h * .48, cx + 6, y + h * .60], fill=(70, 140, 220))
    d.polygon([(cx - 13, y + h * .72), (cx, y + h * .95), (cx + 13, y + h * .72)], fill=(255, 150, 30))


def illo_chess(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 238, 220))
    n = 4
    cw = (w - 20) / n
    ch = (h - 12) / n
    for r in range(n):
        for c in range(n):
            col = (60, 60, 60) if (r + c) % 2 else (250, 250, 250)
            d.rectangle([x + 10 + c * cw, y + 6 + r * ch, x + 10 + (c + 1) * cw, y + 6 + (r + 1) * ch], fill=col)
    d.ellipse([x + w * .38, y + h * .18, x + w * .62, y + h * .52], fill=(255, 255, 255), outline=(20, 20, 20), width=2)
    d.rectangle([x + w * .42, y + h * .48, x + w * .58, y + h * .62], fill=(255, 255, 255), outline=(20, 20, 20), width=2)


def illo_war(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(90, 100, 120))
    d.rectangle([x + 8, y + h * .55, x + w * .45, y + h * .92], fill=(60, 65, 75))
    d.rectangle([x + w * .55, y + h * .45, x + w - 8, y + h * .92], fill=(60, 65, 75))
    d.polygon([(x + w * .28, y + h * .30), (x + w * .42, y + h * .58), (x + w * .14, y + h * .58)], fill=(255, 120, 25))
    d.polygon([(x + w * .72, y + h * .22), (x + w * .86, y + h * .48), (x + w * .58, y + h * .48)], fill=(255, 165, 35))
    d.line([(x + w * .05, y + h * .12), (x + w * .30, y + h * .30)], fill=(255, 255, 255), width=3)
    d.line([(x + w * .95, y + h * .08), (x + w * .72, y + h * .22)], fill=(255, 255, 255), width=3)


def illo_shop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 235, 200))
    d.rectangle([x + 8, y + h * .30, x + w - 8, y + h * .92], fill=(240, 240, 245), outline=(90, 90, 90), width=2)
    d.polygon([(x + 4, y + h * .32), (x + w * .5, y + h * .12), (x + w - 4, y + h * .32)], fill=(200, 50, 50))
    d.rectangle([x + w * .38, y + h * .55, x + w * .62, y + h * .92], fill=(120, 80, 50))
    d.ellipse([x + w * .18, y + h * .42, x + w * .32, y + h * .60], fill=(255, 210, 60))
    d.ellipse([x + w * .68, y + h * .42, x + w * .82, y + h * .60], fill=(80, 180, 120))


def illo_mine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 215, 190))
    d.polygon([(x + 4, y + h * .92), (x + w * .5, y + h * .18), (x + w - 4, y + h * .92)], fill=(130, 105, 80))
    d.polygon([(x + w * .38, y + h * .92), (x + w * .5, y + h * .55), (x + w * .62, y + h * .92)], fill=(40, 35, 30))
    d.rectangle([x, y + h * .78, x + w, y + h * .92], fill=(70, 140, 200))
    d.ellipse([x + w * .78, y + 4, x + w * .96, y + h * .30], fill=(255, 195, 50))


def illo_parliament(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 240, 210))
    d.rectangle([x + 10, y + h * .55, x + w - 10, y + h * .90], fill=(235, 220, 185), outline=(140, 120, 80), width=2)
    d.ellipse([x + w * .36, y + h * .12, x + w * .64, y + h * .56], fill=(210, 190, 150), outline=(140, 120, 80), width=2)
    d.rectangle([x + w * .47, y + h * .02, x + w * .53, y + h * .14], fill=(160, 130, 80))
    for px in (0.20, 0.38, 0.56, 0.74):
        d.rectangle([x + w * px, y + h * .62, x + w * px + 8, y + h * .88], fill=(255, 255, 255))
    d.rectangle([x + 8, y + h * .88, x + w - 8, y + h * .94], fill=(160, 130, 80))


def illo_flags(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.line([(x + w * .30, y + h * .92), (x + w * .30, y + h * .12)], fill=(60, 60, 60), width=3)
    d.line([(x + w * .70, y + h * .92), (x + w * .70, y + h * .12)], fill=(60, 60, 60), width=3)
    d.rectangle([x + w * .30, y + h * .12, x + w * .52, y + h * .42], fill=(30, 110, 200))
    d.rectangle([x + w * .30, y + h * .27, x + w * .52, y + h * .42], fill=(240, 240, 240))
    d.rectangle([x + w * .48, y + h * .12, x + w * .70, y + h * .42], fill=(200, 40, 40))
    d.rectangle([x + w * .48, y + h * .27, x + w * .70, y + h * .42], fill=(255, 200, 40))
    d.rectangle([x, y + h * .88, x + w, y + h], fill=(90, 170, 90))


def illo_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 26, 48))
    pts = [(0.06, 0.30), (0.28, 0.42), (0.48, 0.38), (0.68, 0.62), (0.92, 0.82)]
    xy = [(x + w * px, y + h * py) for px, py in pts]
    d.line(xy, fill=(255, 90, 90), width=4)
    for px, py in xy:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 200, 60))
    d.polygon([(x + w * .92, y + h * .82), (x + w * .80, y + h * .76), (x + w * .88, y + h * .66)], fill=(255, 90, 90))
    for gy in (0.25, 0.5, 0.75):
        d.line([(x + 6, y + h * gy), (x + w - 6, y + h * gy)], fill=(70, 85, 130), width=1)


ILLOS = [illo_flame, illo_ship, illo_refinery, illo_tanker, illo_factory,
         illo_rocket, illo_chess, illo_war, illo_shop, illo_mine,
         illo_parliament, illo_flags, illo_chart]

MAINS = [
    ("1 CAIRO, EGYPT", "AFRICA · DISASTER", RED, "REPORTED", GREEN,
     "Tanker fire kills 30+",
     "Ring Road blaze; 25 hurt, cars charred.", "AP · 26 NOV"),
    ("2 WASHINGTON, USA", "AMERICAS · TRADE", PURPLE, "REPORTED", GREEN,
     "Tariffs proposed on 14",
     "China +20% after capacity probe.", "REUTERS · 25 NOV"),
    ("3 RAS TANURA, SAUDI", "MIDDLE EAST · ENERGY", RED, "CLAIM", ORANGE,
     "Houthis claim refinery hit",
     "Group says plant hit; flights cut.", "WIRES · 26 NOV"),
    ("4 STRAIT OF HORMUZ", "MIDDLE EAST · ENERGY", RED, "CLAIM", ORANGE,
     "IRGC: two tankers mined",
     "Ships hit mines, burned.", "IRGC VIA WIRES"),
    ("5 DHAKA, BANGLADESH", "ASIA · LABOUR", ORANGE, "REPORTED", GREEN,
     "Garment wage up 36%",
     "Vote 4-2: 12,500 to 17,000 taka.", "AP · 25 NOV"),
    ("6 TIANGONG ORBIT", "WORLD · SPACE", GREY, "REPORTED", GREEN,
     "First foreigner in orbit",
     "Zeeshan Ali on Shenzhou-24.", "WIRES · 26 NOV"),
    ("7 GENEVA, SWITZERLAND", "EUROPE · CHESS", BLUE, "REPORTED", GREEN,
     "Game 2 drawn, 20 moves",
     "Gukesh held; match level 1-1.", "CHESSBASE · 25 NOV"),
    ("8 KYIV / MOSCOW", "EUROPE · WAR", BLUE, "REPORTED", GREEN,
     "Refineries hit; 490k dead",
     "Two plants struck overnight.", "BBC / WIRES"),
    ("9 CARTAGENA, COLOMBIA", "AMERICAS · CRIME", PURPLE, "REPORTED", GREEN,
     "20 hostages freed",
     "Police storm shop after 17 hours.", "AP · 25 NOV"),
    ("10 INDONESIA", "ASIA · DISASTER", ORANGE, "ONGOING", BLUE,
     "Mine flood: 9 dead",
     "17 trapped in flooded gold mine.", "AP · 25 NOV"),
    ("11 NEW DELHI, INDIA", "ASIA · NATION", ORANGE, "REPORTED", GREEN,
     "Constitution Day tributes",
     "77 years on; 18 years since 26/11.", "WIRES · 26 NOV"),
    ("12 HONIARA, SOLOMON IS.", "OCEANIA · SECURITY", TEAL, "REPORTED", GREEN,
     "No-base treaty signed",
     "Solomons-Australia pact agreed.", "WIRES · 26 NOV"),
    ("13 GLOBAL MARKETS", "WORLD · MARKETS", GREY, "REPORTED", GREEN,
     "Nasdaq falls 2%",
     "VIX +60% in Nov; chips halve.", "REUTERS · 25 NOV"),
]

BRIEFS = [
    ("14", "Niger: Saudi national kidnapped, IS suspected", "Reuters"),
    ("15", "South Africa: Biovac vaccine plant, EU loan", "AP"),
    ("16", "Brazil: Wolbachia cuts viral infections 68%", "Wires"),
    ("17", "Iowa: Army blows up lead-azide stockpile", "AP"),
    ("18", "Washington: Vance says Huang needs no pardon", "AP / BBC"),
    ("19", "China: Xi graft probe hits Shanghai star", "BBC"),
    ("20", "North Korea: Swiss office ordered closed", "BBC"),
    ("21", "Beijing: fair climate urged in Nexperia row", "Reuters"),
    ("22", "India: Delhi court hears Das passport plea", "Reuters"),
    ("23", "India: IITs add 6,000 AI, space seats", "Jagran"),
    ("24", "Gaza: medics warn meningitis spreading", "Wires"),
    ("25", "Qatar: Doha F1 goes ahead despite war", "Reuters"),
    ("26", "Serbia: Vucic media ally detained", "AP"),
    ("27", "UK: two charged over royal home break-in", "AP"),
    ("28", "India: 1,220 register for IPL 2027 auction", "SelfStudys"),
    ("29", "India: Flipkart chief to step down in Dec", "Jagran"),
]

NUMBERS = [
    ("30+", "dead, Cairo tanker fire"),
    ("20%", "extra US tariff on China"),
    ("36%", "wage rise to 17,000 taka"),
    ("490,000+", "Russian dead, BBC tally"),
]

TIMELINE = [
    ("00:00", "Constitution Day, India"),
    ("Morning", "Delhi court: Das plea"),
    ("14:00", "Chess Game 3, Geneva"),
    ("All day", "US markets shut: Thanksgiving"),
    ("Evening", "Qatar F1 weekend opens"),
]

# map pin positions as fractions of map box (x, y)
PINS = [(0.50, 0.42), (0.12, 0.28), (0.58, 0.44), (0.63, 0.50), (0.75, 0.46),
        (0.80, 0.24), (0.47, 0.22), (0.55, 0.20), (0.20, 0.60), (0.82, 0.66),
        (0.70, 0.50), (0.94, 0.74), (0.08, 0.36)]


def panel(draw, x, y, w, h, idx, big=False):
    banner, label, lab_col, status, st_col, head, body, src = MAINS[idx]
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=(40, 40, 40), width=2)
    bf = F(SANS_B, 11 if not big else 12)
    draw.rectangle([x, y, x + w, y + 20], fill=NAVY)
    draw.text((x + 6, y + 4), banner, font=bf, fill=(255, 255, 255))
    ih = int(h * 0.30)
    ILLOS[idx](draw, x + 4, y + 24, w - 8, ih)
    badge(draw, x + w - 86, y + 24 + ih - 23, status, st_col)
    cy = y + 24 + ih + 3
    draw.text((x + 6, cy), label, font=F(SANS_B, 9), fill=lab_col)
    cy += 13
    hf = F(SANS_B, 19 if big else 16)
    cy = draw_wrap(draw, (x + 6, cy), head, hf, INK, w - 12, max_lines=2)
    cy += 1
    cy = draw_wrap(draw, (x + 6, cy), body, F(SANS, 10), (50, 50, 50), w - 12, max_lines=2)
    draw.text((x + 6, y + h - 16), src, font=F(SANS_B, 9), fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 14

    # masthead strip
    d.rectangle([0, 0, W, 30], fill=NAVY)
    d.text((M, 7), "THE WORLD IN ONE DAY", font=F(SANS_B, 14), fill=(255, 255, 255))
    right = "29 STORIES · 7 REGIONS · ALL FROM THIS ONE DAY"
    rf = F(SANS_B, 13)
    d.text((W - M - d.textlength(right, font=rf), 8), right, font=rf, fill=YELLOW)

    # giant date title + red deck
    tf = F(SERIF_B, 62)
    title = "Thursday 26 November 2026"
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 34), title, font=tf, fill=INK)
    deck = "Cairo fire kills 30+ · US tariffs on 14 partners · Chess match level 1-1"
    df = F(SANS_I, 17)
    dw = d.textlength(deck, font=df)
    d.text(((W - dw) / 2, 108), deck, font=df, fill=RED)

    # region chips (sum = 29)
    chips = [("EUROPE 4", BLUE), ("MIDDLE EAST 4", RED), ("AFRICA 3", GREEN),
             ("ASIA 10", ORANGE), ("AMERICAS 5", PURPLE), ("OCEANIA 1", TEAL),
             ("WORLD 2", (60, 60, 60))]
    cx = M
    cf = F(SANS_B, 12)
    for name, col in chips:
        cw = int(d.textlength(name, font=cf)) + 16
        d.rounded_rectangle([cx, 132, cx + cw, 154], radius=5, fill=col)
        d.text((cx + 8, 137), name, font=cf, fill=(255, 255, 255))
        cx += cw + 6

    # UTC timeline ruler
    d.rectangle([M, 160, W - M, 198], fill=NAVY)
    d.rectangle([M, 160, M + 52, 198], fill=RED)
    d.text((M + 9, 170), "UTC", font=F(SANS_B, 16), fill=(255, 255, 255))
    tx = M + 62
    seg = (W - 2 * M - 62) / len(TIMELINE)
    for tm, ev in TIMELINE:
        d.text((tx + 4, 164), tm, font=F(SANS_B, 13), fill=YELLOW)
        draw_wrap(d, (tx + 4, 180), ev, F(SANS, 10), (255, 255, 255), seg - 10, max_lines=2)
        tx += seg

    # main grid: row1 = 3 big panels + numbers column; rows 2-3 = 5 each
    gy = 204
    gap = 6
    num_w = 168
    big_w = (W - 2 * M - num_w - 3 * gap) // 3
    row1_h = 188
    for i in range(3):
        panel(d, M + i * (big_w + gap), gy, big_w, row1_h, i, big=True)
    nx = M + 3 * (big_w + gap)
    d.rectangle([nx, gy, nx + num_w, gy + row1_h], fill=NAVY)
    d.text((nx + 8, gy + 6), "THE DAY IN", font=F(SANS_B, 14), fill=(255, 255, 255))
    d.text((nx + 8, gy + 24), "NUMBERS", font=F(SANS_B, 14), fill=YELLOW)
    ny = gy + 46
    for val, lab in NUMBERS:
        d.text((nx + 8, ny), val, font=F(SANS_B, 18), fill=(140, 205, 255))
        ny += 21
        ny = draw_wrap(d, (nx + 8, ny), lab, F(SANS, 9), (255, 255, 255), num_w - 16, max_lines=1)
        ny += 2

    small_w = (W - 2 * M - 4 * gap) // 5
    row_h = 148
    y2 = gy + row1_h + gap
    for i in range(5):
        panel(d, M + i * (small_w + gap), y2, small_w, row_h, 3 + i)
    y3 = y2 + row_h + gap
    for i in range(5):
        panel(d, M + i * (small_w + gap), y3, small_w, row_h, 8 + i)

    # briefs (left 3 cols) + map (right)
    by = y3 + row_h + 8
    d.text((M, by), "ALSO ON THURSDAY 26 NOVEMBER", font=F(SANS_B, 15), fill=NAVY)
    by += 22
    map_w = 300
    brief_w = W - 2 * M - map_w - 10
    col_w = brief_w // 3
    col_counts = [6, 5, 5]
    pos = 0
    for c in range(3):
        cy = by
        for _ in range(col_counts[c]):
            num, head, src = BRIEFS[pos]
            pos += 1
            d.ellipse([M + c * col_w, cy, M + c * col_w + 20, cy + 20], fill=RED)
            nf = F(SANS_B, 10)
            nw = d.textlength(num, font=nf)
            d.text((M + c * col_w + 10 - nw / 2, cy + 4), num, font=nf, fill=(255, 255, 255))
            hy = draw_wrap(d, (M + c * col_w + 24, cy), head, F(SANS_B, 10), INK, col_w - 28, max_lines=2)
            d.text((M + c * col_w + 24, hy + 1), src, font=F(SANS, 8), fill=GREY)
            cy = hy + 13

    mx = M + brief_w + 10
    my = by - 22
    mh = 168
    d.rectangle([mx, my, mx + map_w, my + mh], fill=(230, 242, 252), outline=(40, 40, 40), width=2)
    d.text((mx + 8, my + 5), "WHERE IT HAPPENED", font=F(SANS_B, 13), fill=NAVY)
    d.text((mx + 8, my + 22), "pins = story numbers 1-13", font=F(SANS, 10), fill=GREY)
    # dot-matrix continents (rough blobs of dots)
    blobs = [(0.16, 0.45, 0.13, 0.16), (0.24, 0.68, 0.07, 0.14), (0.51, 0.36, 0.09, 0.10),
             (0.53, 0.58, 0.09, 0.16), (0.72, 0.40, 0.16, 0.18), (0.88, 0.72, 0.08, 0.09)]
    for bx, byy, brx, bry in blobs:
        for gx in range(28):
            for gy2 in range(16):
                px = mx + 8 + gx * (map_w - 16) / 27
                py = my + 40 + gy2 * (mh - 48) / 15
                nx2 = (px - (mx + bx * map_w)) / (brx * map_w)
                ny2 = (py - (my + 40 + byy * (mh - 48))) / (bry * (mh - 48))
                if nx2 * nx2 + ny2 * ny2 <= 1.0:
                    d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(165, 185, 205))
    for i, (fx, fy) in enumerate(PINS):
        px = mx + fx * map_w
        py = my + 40 + fy * (mh - 52)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255), width=2)
        pf = F(SANS_B, 10)
        t = str(i + 1)
        d.text((px - d.textlength(t, font=pf) / 2, py - 6), t, font=pf, fill=(255, 255, 255))

    # DATE CHECK box
    dy = by + 172
    d.rectangle([M, dy, W - M, dy + 72], fill=(255, 252, 245), outline=RED, width=4)
    d.rectangle([M, dy, M + 128, dy + 24], fill=RED)
    d.text((M + 8, dy + 5), "DATE CHECK", font=F(SANS_B, 13), fill=(255, 255, 255))
    d.text((M + 138, dy + 5), "Every story happened or was first reported on Thursday 26 November 2026 (UTC).",
           font=F(SANS_B, 12), fill=INK)
    excl = ("Left out as earlier news: Sooryavanshi 204 (Tue 24 Nov) · PIF Tower hit (24 Nov) · "
            "Huawei verdict (24 Nov) · England T20 win (24 Nov) · Senegal CAS (24 Nov) · "
            "Chess Game 1 (24 Nov) · Zaporizhzhia strike (25 Nov) · Australia apology (25 Nov)")
    draw_wrap(d, (M + 10, dy + 30), excl, F(SANS, 10.5), RED, W - 2 * M - 20, max_lines=3)

    legend = ("HOW SURE: REPORTED = carried by the day's wires or officials · CLAIM = one side's account, "
              "labelled as such · ONGOING = still unfolding · Scenes are drawn illustrations, not photographs.")
    draw_wrap(d, (M, dy + 78), legend, F(SANS, 9), GREY, W - 2 * M, max_lines=2)

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
