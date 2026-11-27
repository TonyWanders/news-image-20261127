"""Build the 27 November 2026 news image (entry.png) for make.fun.

Draws a newspaper front page, 1024x1024, with the five most
significant world stories of Friday 27 November 2026, each with a
small drawn scene, a headline and a short standfirst. All facts were
checked against BBC, Reuters, CNN, USA TODAY and The Times reporting
of 26-27 November 2026. Deterministic: fixed positions, no random
numbers, no timestamps, no network. Run: python3 build_image.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

NAVY = (16, 38, 63)
NAVY_D = (10, 26, 44)
GOLD = (232, 184, 75)
PAPER = (246, 241, 231)
INK = (24, 24, 24)
RED = (178, 28, 28)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
SKY_NIGHT = (13, 27, 48)
SKY_STORM = (58, 74, 92)
SKY_DUSK = (122, 62, 58)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, color, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    n = max(1, y1 - y0)
    for i in range(n):
        t = i / n
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def stars(draw, box, pts):
    for (x, y, r) in pts:
        draw.ellipse([box[0] + x - r, box[1] + y - r,
                      box[0] + x + r, box[1] + y + r], fill=(255, 255, 220))


def burst(draw, cx, cy, r, core=(255, 214, 90), mid=(245, 130, 32),
          outer=(214, 48, 24)):
    for rr, col in ((r, outer), (int(r * 0.66), mid), (int(r * 0.36), core)):
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
    for ang in range(0, 360, 30):
        import math
        a = math.radians(ang)
        x2, y2 = cx + int(r * 1.35 * math.cos(a)), cy + int(r * 1.35 * math.sin(a))
        x3, y3 = cx + int(r * 0.55 * math.cos(a)), cy + int(r * 0.55 * math.sin(a))
        draw.line([(x3, y3), (x2, y2)], fill=mid, width=5)


def drone(draw, cx, cy, s=1.0):
    body = (20, 20, 20)
    draw.ellipse([cx - 16 * s, cy - 7 * s, cx + 16 * s, cy + 7 * s], fill=body)
    for dx in (-26, 26):
        draw.line([(cx, cy), (cx + dx * s, cy - 12 * s)], fill=body, width=3)
        draw.line([(cx + dx * s - 12, cy - 14 * s),
                   (cx + dx * s + 12, cy - 14 * s)], fill=(120, 120, 120), width=3)
    draw.ellipse([cx - 3, cy + 8 * s, cx + 3, cy + 14 * s], fill=(255, 60, 60))


def radar_dish(draw, x, y, s=1.0):
    draw.line([(x, y), (x, y + 46 * s)], fill=(8, 8, 8), width=5)
    draw.arc([x - 34 * s, y - 30 * s, x + 34 * s, y + 30 * s],
             start=200, end=340, fill=(8, 8, 8), width=6)
    draw.line([(x, y), (x + 30 * s, y - 26 * s)], fill=(8, 8, 8), width=4)


def panel(draw, x, y, w, h, border=(30, 30, 30)):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=border, width=2)


def kicker_headline(draw, x, y, w, kick, head, stand, head_size=30,
                    stand_size=19):
    f_kick = font(SANS_B, 19)
    f_head = font(SERIF_B, head_size)
    f_stand = font(SANS, stand_size)
    draw.text((x, y), kick, font=f_kick, fill=RED)
    y += 28
    y = text_block(draw, x, y, wrap(draw, head, f_head, w), f_head, INK,
                   leading=int(head_size * 1.08))
    y += 6
    y = text_block(draw, x, y, wrap(draw, stand, f_stand, w), f_stand,
                   (60, 60, 60), leading=int(stand_size * 1.25))
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -----------------------------------------------------
    d.rectangle([24, 24, 1000, 150], fill=NAVY)
    d.rectangle([24, 24, 1000, 30], fill=NAVY_D)
    f_title = font(SERIF_B, 52)
    title = "THE WORLD IN ONE PICTURE"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 40), title, font=f_title, fill=WHITE)
    f_date = font(SANS_B, 27)
    date = "FRIDAY  27  NOVEMBER  2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 106), date, font=f_date, fill=GOLD)
    d.line([(24, 150), (1000, 150)], fill=GOLD, width=4)

    # ---- Lead story: Kuwait drone strike ------------------------------
    lx, ly, lw, lh = 24, 166, 620, 330
    panel(d, lx, ly, lw, lh)
    sx, sy, sw, sh = lx + 2, ly + 2, lw - 4, 150
    vgrad(d, (sx, sy, sx + sw, sy + sh), SKY_NIGHT, (52, 32, 54))
    stars(d, (sx, sy), [(40, 22, 2), (120, 40, 2), (210, 18, 3),
                        (300, 48, 2), (380, 24, 2), (470, 42, 2),
                        (540, 20, 3), (90, 70, 2), (250, 80, 2),
                        (430, 78, 2), (580, 60, 2), (170, 100, 2)])
    burst(d, sx + 430, sy + 92, 42)
    drone(d, sx + 130, sy + 58)
    drone(d, sx + 300, sy + 34, s=0.7)
    # ground: radar station silhouettes
    d.rectangle([sx, sy + sh - 26, sx + sw, sy + sh], fill=(8, 8, 8))
    radar_dish(d, sx + 90, sy + sh - 66, s=0.9)
    radar_dish(d, sx + 540, sy + sh - 60, s=0.75)
    d.rectangle([sx + 210, sy + sh - 52, sx + 260, sy + sh - 26], fill=(8, 8, 8))
    d.rectangle([sx + 300, sy + sh - 40, sx + 340, sy + sh - 26], fill=(8, 8, 8))
    kicker_headline(
        d, lx + 18, ly + 166, lw - 36,
        "MIDDLE EAST  -  KUWAIT",
        "Drone strike in Kuwait kills two Italians",
        "Italy and Kuwait blame Iran for the attack. "
        "Tehran denies any role.",
        head_size=30, stand_size=19)

    # ---- Right story: US Thanksgiving storm ---------------------------
    rx, ry, rw, rh = 660, 166, 340, 330
    panel(d, rx, ry, rw, rh)
    sx, sy, sw, sh = rx + 2, ry + 2, rw - 4, 150
    vgrad(d, (sx, sy, sx + sw, sy + sh), SKY_STORM, (28, 38, 52))
    for (cx, cy, cr) in [(60, 40, 42), (130, 26, 52), (210, 44, 46),
                         (280, 30, 40), (170, 62, 48), (90, 66, 36)]:
        d.ellipse([sx + cx - cr, sy + cy - cr // 2, sx + cx + cr,
                   sy + cy + cr // 2], fill=(38, 50, 64))
    for (x0, y0) in [(30, 84), (70, 92), (110, 82), (150, 96), (190, 86),
                     (230, 94), (270, 84), (310, 96), (50, 112),
                     (130, 114), (210, 112), (290, 116)]:
        d.line([(sx + x0, sy + y0), (sx + x0 - 8, sy + y0 + 22)],
               fill=(150, 180, 210), width=3)
    d.polygon([(sx + 250, sy + 62), (sx + 228, sy + 104), (sx + 244, sy + 104),
               (sx + 224, sy + 140), (sx + 262, sy + 92), (sx + 246, sy + 92),
               (sx + 268, sy + 62)], fill=(255, 214, 90))
    # small grounded plane silhouette
    d.ellipse([sx + 60, sy + 122, sx + 150, sy + 134], fill=(12, 12, 12))
    d.polygon([(sx + 150, sy + 126), (sx + 178, sy + 130), (sx + 150, sy + 134)],
              fill=(12, 12, 12))
    d.polygon([(sx + 96, sy + 122), (sx + 108, sy + 108), (sx + 118, sy + 122)],
              fill=(12, 12, 12))
    kicker_headline(
        d, rx + 16, ry + 166, rw - 32,
        "UNITED STATES",
        "Thanksgiving storm cuts power to 800,000",
        "Macy's parade postponed for the first time; "
        "1,700 flights delayed.",
        head_size=26, stand_size=18)

    # ---- Bottom row: three stories ------------------------------------
    by, bw, bh, gap = 512, 312, 330, 20
    cols = [24, 24 + bw + gap, 24 + 2 * (bw + gap)]

    # Gaza
    x = cols[0]
    panel(d, x, by, bw, bh)
    sx, sy, sw, sh = x + 2, by + 2, bw - 4, 128
    vgrad(d, (sx, sy, sx + sw, sy + sh), SKY_DUSK, (38, 30, 44))
    d.ellipse([sx + 240, sy + 18, sx + 272, sy + 50], fill=(255, 190, 110))
    for (bx, bw_, bh_) in [(10, 46, 58), (66, 34, 76), (110, 52, 48),
                           (172, 38, 66), (220, 44, 54), (274, 28, 72)]:
        d.rectangle([sx + bx, sy + sh - bh_, sx + bx + bw_, sy + sh],
                    fill=(16, 14, 16))
    for (cx, cy, cr) in [(90, 34, 16), (100, 22, 12), (190, 30, 14),
                         (200, 18, 10)]:
        d.ellipse([sx + cx - cr, sy + cy - cr, sx + cx + cr, sy + cy + cr],
                  fill=(120, 112, 108))
    kicker_headline(
        d, x + 14, by + 144, bw - 28,
        "GAZA",
        "Israeli strikes kill 10; Hamas weighs response",
        "A senior Hamas official is among the dead as the "
        "ceasefire frays.",
        head_size=26, stand_size=18)

    # Ukraine
    x = cols[1]
    panel(d, x, by, bw, bh)
    sx, sy, sw, sh = x + 2, by + 2, bw - 4, 128
    d.rectangle([sx, sy, sx + sw, sy + 64], fill=(42, 92, 170))
    d.rectangle([sx, sy + 64, sx + sw, sy + sh], fill=(232, 190, 60))
    # white dove
    d.ellipse([sx + 120, sy + 46, sx + 190, sy + 78], fill=WHITE)
    d.ellipse([sx + 176, sy + 34, sx + 198, sy + 56], fill=WHITE)
    d.polygon([(sx + 196, sy + 42), (sx + 214, sy + 48), (sx + 196, sy + 50)],
              fill=(240, 160, 40))
    d.polygon([(sx + 128, sy + 48), (sx + 96, sy + 22), (sx + 148, sy + 40)],
              fill=WHITE)
    d.polygon([(sx + 150, sy + 52), (sx + 128, sy + 26), (sx + 166, sy + 44)],
              fill=(235, 235, 235))
    kicker_headline(
        d, x + 14, by + 144, bw - 28,
        "UKRAINE",
        "Trump tells Putin to pull back",
        "Zelensky questions the 'strange' Trump-Putin friendship in a "
        "BBC interview.",
        head_size=26, stand_size=18)

    # Chess
    x = cols[2]
    panel(d, x, by, bw, bh)
    sx, sy, sw, sh = x + 2, by + 2, bw - 4, 128
    d.rectangle([sx, sy, sx + sw, sy + sh], fill=(34, 34, 40))
    bs = 13
    ox, oy = sx + (sw - 8 * bs) // 2, sy + (sh - 8 * bs) // 2
    for r in range(8):
        for c in range(8):
            col = (238, 226, 200) if (r + c) % 2 == 0 else (96, 74, 58)
            d.rectangle([ox + c * bs, oy + r * bs, ox + (c + 1) * bs,
                         oy + (r + 1) * bs], fill=col)
    f_piece = font(SANS_B, 11)
    pieces = {(0, 4): ("K", (20, 20, 20)), (0, 3): ("Q", (20, 20, 20)),
              (7, 4): ("K", (255, 255, 255)), (7, 3): ("Q", (255, 255, 255)),
              (3, 3): ("N", (20, 20, 20)), (4, 5): ("B", (255, 255, 255))}
    for (r, c), (ch, col) in pieces.items():
        d.text((ox + c * bs + 3, oy + r * bs), ch, font=f_piece, fill=col)
    kicker_headline(
        d, x + 14, by + 144, bw - 28,
        "SPORT  -  CHESS",
        "Gukesh and Sindarov draw marathon Game 3",
        "World Chess Championship level after three games.",
        head_size=26, stand_size=18)

    # ---- Footer --------------------------------------------------------
    d.rectangle([24, 862, 1000, 1000], fill=NAVY)
    f_foot = font(SERIF_B, 26)
    foot = "Five stories that defined Friday 27 November 2026"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 884), foot, font=f_foot, fill=WHITE)
    f_src = font(SANS, 18)
    src = "Sources: BBC  -  Reuters  -  CNN  -  USA TODAY  -  The Times"
    sw_ = d.textlength(src, font=f_src)
    d.text(((W - sw_) / 2, 930), src, font=f_src, fill=(200, 205, 212))
    f_note = font(SANS, 16)
    note = "Drawn from the day's reporting. No photograph, no invented fact."
    nw = d.textlength(note, font=f_note)
    d.text(((W - nw) / 2, 960), note, font=f_note, fill=GOLD)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
