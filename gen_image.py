#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news summary image (1024x1024 PNG).

Original drawn/text layout, PIL only, fully deterministic: no timestamps,
no randomness, fixed fonts. Run: python3 gen_image.py -> writes entry.png
beside this file. The graded entrypoint (main.py) only copies entry.png.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (20, 33, 61)
PAPER = (247, 243, 234)
INK = (24, 24, 24)
RED = (155, 34, 38)
TEAL = (14, 110, 110)
GOLD = (176, 132, 24)
GREY = (90, 90, 90)
CARD = (255, 255, 255)
LINE = (200, 196, 186)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to pixel width; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 134, 186),
              outline=NAVY, width=4)
    d.ellipse([cx - r + 14, cy - r + 18, cx - r + 62, cy - r + 52],
              fill=(76, 175, 80))
    d.ellipse([cx + 8, cy + 6, cx + 58, cy + 44], fill=(76, 175, 80))
    d.ellipse([cx - 52, cy + 30, cx - 8, cy + 62], fill=(46, 160, 120))
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255),
          width=3)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=3)


def draw_missile(d, cx, cy):
    d.polygon([(cx - 52, cy + 18), (cx + 30, cy + 18), (cx + 58, cy),
               (cx + 30, cy - 18), (cx - 52, cy - 18)], fill=(120, 124, 130),
              outline=NAVY)
    d.polygon([(cx - 52, cy - 18), (cx - 38, cy - 34), (cx - 22, cy - 18)],
              fill=RED)
    d.polygon([(cx - 52, cy + 18), (cx - 38, cy + 34), (cx - 22, cy + 18)],
              fill=RED)
    d.polygon([(cx + 30, cy - 18), (cx + 58, cy), (cx + 30, cy + 18)],
              fill=RED)


def draw_rubble(d, cx, cy):
    d.rectangle([cx - 52, cy - 10, cx - 6, cy + 42], fill=(150, 148, 140),
                outline=NAVY, width=3)
    d.rectangle([cx + 6, cy - 34, cx + 52, cy + 42], fill=(178, 175, 165),
                outline=NAVY, width=3)
    d.line([cx + 6, cy - 34, cx + 28, cy - 8, cx + 14, cy + 12],
           fill=NAVY, width=3)
    for y in (-2, 14, 30):
        d.line([cx - 52, cy + y, cx - 6, cy + y], fill=NAVY, width=2)
    d.ellipse([cx + 22, cy - 22, cx + 38, cy - 6], fill=(255, 214, 64),
              outline=NAVY, width=2)


def draw_capitol(d, cx, cy):
    d.pieslice([cx - 30, cy - 44, cx + 30, cy + 4], 180, 360,
               fill=(236, 236, 236), outline=NAVY, width=3)
    d.ellipse([cx - 4, cy - 52, cx + 4, cy - 44], fill=NAVY)
    d.rectangle([cx - 52, cy + 4, cx + 52, cy + 12], fill=NAVY)
    for x in (cx - 40, cx - 14, cx + 12, cx + 38):
        d.rectangle([x - 5, cy + 12, x + 5, cy + 42], fill=(236, 236, 236),
                    outline=NAVY, width=2)
    d.rectangle([cx - 56, cy + 42, cx + 56, cy + 50], fill=NAVY)


def draw_ball(d, cx, cy, r=44):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
              outline=NAVY, width=4)
    pts = [(cx, cy - 18), (cx + 17, cy - 6), (cx + 11, cy + 14),
           (cx - 11, cy + 14), (cx - 17, cy - 6)]
    d.polygon(pts, fill=NAVY)
    for (x1, y1) in [(cx, cy - 18), (cx + 17, cy - 6), (cx + 11, cy + 14),
                     (cx - 11, cy + 14), (cx - 17, cy - 6)]:
        d.line([cx, cy, x1, y1], fill=NAVY, width=2)


def draw_quake(d, cx, cy):
    pts = [(cx - 54, cy + 10), (cx - 34, cy + 10), (cx - 24, cy - 26),
           (cx - 10, cy + 30), (cx + 4, cy - 14), (cx + 16, cy + 10),
           (cx + 54, cy + 10)]
    d.line(pts, fill=RED, width=5, joint="curve")
    d.line([cx - 54, cy + 38, cx + 54, cy + 38], fill=NAVY, width=3)


def card(d, x, y, w, h, kicker, kcolor, headline, body, icon):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                        outline=LINE, width=2)
    d.rounded_rectangle([x, y, x + 118, y + h], radius=10, fill=(238, 240, 244))
    d.rounded_rectangle([x + 60, y, x + 118, y + h], radius=10,
                        fill=(238, 240, 244))
    icon(d, x + 59, y + h // 2)
    tx = x + 134
    tw = w - 150
    d.text((tx, y + 14), kicker, font=font(BOLD, 22), fill=kcolor)
    lines = wrap(d, headline, font(BOLD, 28), tw)
    yy = y + 44
    for ln in lines[:2]:
        d.text((tx, yy), ln, font=font(BOLD, 28), fill=INK)
        yy += 34
    blines = wrap(d, body, font(REG, 22), tw)
    for ln in blines[:3]:
        d.text((tx, yy + 4), ln, font=font(REG, 22), fill=(60, 60, 60))
        yy += 27


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 168], fill=NAVY)
    d.text((W // 2, 16), "THE WORLD IN ONE DAY", font=font(BOLD, 28),
           fill=(255, 214, 64), anchor="ma")
    d.text((W // 2, 50), "23 NOVEMBER 2026", font=font(BOLD, 76),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 132), "MONDAY  •  WORLD NEWS IN ONE IMAGE",
           font=font(BOLD, 24), fill=(180, 200, 230), anchor="ma")

    # Lead story: COP31
    d.rounded_rectangle([16, 184, 1008, 392], radius=12, fill=(255, 255, 255),
                        outline=LINE, width=2)
    d.rectangle([16, 184, 1008, 226], fill=RED)
    d.text((36, 192), "LEAD STORY  —  CLIMATE", font=font(BOLD, 26),
           fill=(255, 255, 255))
    draw_globe(d, 130, 312, 62)
    d.text((216, 240), "COP31 COLLAPSES", font=font(BOLD, 62), fill=RED)
    d.text((216, 312), "Climate talks end with no deal:",
           font=font(BOLD, 29), fill=INK)
    d.text((216, 348), "fossil-fuel wording kills the pact.",
           font=font(REG, 29), fill=(60, 60, 60))

    # Grid of four stories
    gx, gy, cw, ch, gap = 16, 408, 480, 212, 12
    card(d, gx, gy, cw, ch, "POLAND  •  NATO", RED,
         "3 RUSSIAN MISSILES",
         "All three were Russian Kh-101s, prosecutors say. NATO meets today.",         draw_missile)
    card(d, gx + cw + gap, gy, cw, ch, "UKRAINE  •  WAR", RED,
         "KYIV STRIKES KILL 6",
         "At least six killed in the Kyiv region. A boy, 7, is pulled alive from the rubble.",
         draw_rubble)
    card(d, gx, gy + ch + gap, cw, ch, "USA  •  POLITICS", TEAL,
         "DEMOCRATS WIN",
         "Largest House majority since 1992 after a North Carolina seat flips.",
         draw_capitol)
    card(d, gx + cw + gap, gy + ch + gap, cw, ch, "SPORT  •  FOOTBALL",
         TEAL, "UK TO HOST 2035",
         "FIFA confirms the UK as host of the 2035 Women's World Cup.",
         draw_ball)

    # Bottom band: quake + also-today ticker
    d.rounded_rectangle([16, 856, 496, 968], radius=10, fill=CARD,
                        outline=LINE, width=2)
    draw_quake(d, 76, 906)
    d.text((140, 858), "PACIFIC  •  QUAKE", font=font(BOLD, 22), fill=GOLD)
    d.text((140, 886), "M6.5 QUAKE HITS", font=font(BOLD, 30), fill=INK)
    d.text((140, 922), "VANUATU", font=font(BOLD, 30), fill=INK)
    d.rounded_rectangle([512, 856, 1008, 968], radius=10, fill=NAVY)
    d.text((536, 858), "ALSO TODAY", font=font(BOLD, 22),
           fill=(255, 214, 64))
    also = ("Houthis claim Saudi strikes  •  Paolo Bulgari dies at 89  •  "
            "Markets on edge after Friday's sell-off")
    yy = 890
    for ln in wrap(d, also, font(REG, 23), 448):
        d.text((536, yy), ln, font=font(REG, 23), fill=(255, 255, 255))
        yy += 28

    # Footer
    d.text((W // 2, 984), "Sources: BBC, Reuters, CNN, AFP  •  23 November 2026",
           font=font(REG, 20), fill=GREY, anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
