#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261118.

Build-time only (uses PIL). The grader never runs this file; main.py
just copies the finished entry.png. 1024x1024 newspaper infographic
summarising the world news of Wednesday 18 November 2026.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (245, 243, 238)          # paper
NAVY = (16, 32, 66)           # header
GOLD = (214, 178, 94)         # date line
INK = (24, 24, 24)            # body text
MUTED = (90, 90, 90)
RED = (158, 32, 32)
PANEL_BG = (255, 255, 255)
PANEL_EDGE = (205, 200, 190)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

f_title = ImageFont.truetype(SERIF_B, 74)
f_date = ImageFont.truetype(SANS_B, 30)
f_head = ImageFont.truetype(SANS_B, 27)
f_body = ImageFont.truetype(SANS, 19)
f_foot = ImageFont.truetype(SANS_B, 20)
f_num = ImageFont.truetype(SANS_B, 26)

# (number, accent colour, headline, summary, icon kind)
STORIES = [
    (1, (158, 32, 32), "US STRIKES IRAN'S\nQESHM ISLAND",
     "US jets hit Revolutionary Guard missile sites on Qeshm Island. "
     "Iran fires drones at Bahrain and Kuwait, targeting US Patriot systems.",
     "jet"),
    (2, (18, 90, 90), "UKRAINE HITS KERCH\nBRIDGE, DAY 2",
     "Ukraine strikes the Kerch Bridge a second day; one arch collapses "
     "into the strait.",
     "bridge"),
    (3, (30, 80, 160), "APEC OPENS\nIN SHENZHEN",
     "APEC summit opens in Shenzhen; Xi hosts Putin. Trump\u2013Xi\u2013Putin "
     "trilateral meeting set for Thursday.",
     "globe"),
    (4, (150, 100, 20), "DEMOCRATS\nWIN ALASKA",
     "Mary Peltola wins Alaska's Senate seat; Democrats now hold 56 seats "
     "in the US Senate.",
     "ballot"),
    (5, (110, 50, 140), "EBOLA SURGES\nIN CONGO",
     "Ebola in Congo more than doubles in 3 months: 11,000+ cases, 5,400 "
     "deaths. Three in four infected children under five die.",
     "virus"),
    (6, (140, 40, 40), "RUSSIAN MILITARY\nPLANE CRASHES",
     "A Russian military plane crashes in Siberia's Kemerovo region; "
     "19 killed.",
     "plane"),
]


def wrap(text, font, width):
    """Wrap text to the given pixel width; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        words, line = para.split(), ""
        for w in words:
            trial = (line + " " + w).strip()
            if font.getlength(trial) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = w
        if line:
            lines.append(line)
    return lines


def draw_icon(d, kind, x, y, s, color):
    """Simple geometric icon inside a ~s x s box at (x, y)."""
    if kind == "jet":
        # fighter jet silhouette (side view)
        d.polygon([(x + 8, y + s // 2), (x + s - 8, y + s // 2 - 14),
                   (x + s - 8, y + s // 2 + 14)], fill=color)
        d.polygon([(x + s // 2, y + s // 2 - 4), (x + s // 2 + 18, y + 4),
                   (x + s // 2 + 26, y + 4), (x + s // 2 + 8, y + s // 2)],
                  fill=color)
        d.polygon([(x + s // 2, y + s // 2 + 4), (x + s // 2 + 18, y + s - 4),
                   (x + s // 2 + 26, y + s - 4), (x + s // 2 + 8, y + s // 2)],
                  fill=color)
        for i, yy in enumerate((y + 10, y + s // 2, y + s - 14)):
            d.line([(x, yy), (x + 14, yy)], fill=(140, 160, 190), width=3)
    elif kind == "bridge":
        d.line([(x + 4, y + s - 18), (x + s - 4, y + s - 18)],
               fill=color, width=5)
        for bx in (x + 14, x + s // 2, x + s - 20):
            d.line([(bx, y + 8), (bx, y + s - 18)], fill=color, width=4)
        d.arc([x + 6, y + 2, x + s - 6, y + s - 10], 180, 360,
              fill=color, width=4)
        d.line([(x + 4, y + s - 8), (x + s - 4, y + s - 8)],
               fill=(120, 170, 210), width=3)
    elif kind == "globe":
        d.ellipse([x + 4, y + 4, x + s - 4, y + s - 4],
                  outline=color, width=5)
        d.ellipse([x + s // 2 - 10, y + 4, x + s // 2 + 10, y + s - 4],
                  outline=color, width=3)
        d.line([(x + 4, y + s // 2), (x + s - 4, y + s // 2)],
               fill=color, width=3)
        d.arc([x + 8, y + s // 4, x + s - 8, y + 3 * s // 4], 0, 180,
              fill=color, width=3)
    elif kind == "ballot":
        d.rectangle([x + 8, y + 8, x + s - 8, y + s - 8],
                    outline=color, width=5)
        d.line([(x + 16, y + s // 2 + 4), (x + s // 2 - 2, y + s - 18),
                (x + s - 14, y + 14)], fill=RED, width=6)
    elif kind == "virus":
        d.ellipse([x + s // 4, y + s // 4, x + 3 * s // 4, y + 3 * s // 4],
                  fill=color)
        for ang in range(0, 360, 45):
            import math
            r = math.radians(ang)
            x1 = x + s // 2 + int(0.28 * s * math.cos(r))
            y1 = y + s // 2 + int(0.28 * s * math.sin(r))
            x2 = x + s // 2 + int(0.48 * s * math.cos(r))
            y2 = y + s // 2 + int(0.48 * s * math.sin(r))
            d.line([(x1, y1), (x2, y2)], fill=color, width=4)
            d.ellipse([x2 - 5, y2 - 5, x2 + 5, y2 + 5], fill=color)
    elif kind == "plane":
        d.polygon([(x + 6, y + s // 2), (x + s - 6, y + s // 2 - 12),
                   (x + s - 6, y + s // 2 + 12)], fill=color)
        d.polygon([(x + s // 2 - 6, y + s // 2 - 2), (x + s // 2 + 10, y + 6),
                   (x + s // 2 + 18, y + 6), (x + s // 2 + 2, y + s // 2)],
                  fill=color)
        d.polygon([(x + s // 2 - 6, y + s // 2 + 2), (x + s // 2 + 10, y + s - 6),
                   (x + s // 2 + 18, y + s - 6), (x + s // 2 + 2, y + s // 2)],
                  fill=color)
        d.line([(x + 10, y + s - 6), (x + s - 10, y + s - 6)],
               fill=(140, 160, 190), width=3)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=RED)
    title = "WORLD NEWS"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 18), title, font=f_title, fill=(255, 255, 255))
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 102), date, font=f_date, fill=GOLD)

    # ---- 6 panels: 2 cols x 3 rows ----
    margin, gap = 24, 16
    pw = (W - 2 * margin - gap) // 2
    ph = 236
    top0 = 172
    for i, (num, accent, head, summary, icon) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (pw + gap)
        y0 = top0 + row * (ph + gap)
        d.rectangle([x0, y0, x0 + pw, y0 + ph], fill=PANEL_BG,
                    outline=PANEL_EDGE, width=2)
        d.rectangle([x0, y0, x0 + pw, y0 + 6], fill=accent)
        # number badge
        cx, cy, r = x0 + 26, y0 + 34, 17
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
        nt = str(num)
        d.text((cx - d.textlength(nt, font=f_num) / 2, cy - 14), nt,
               font=f_num, fill=(255, 255, 255))
        # headline (2 lines, left of badge is taken by badge; headline
        # starts right of it)
        hx = x0 + 52
        head_lines = wrap(head, f_head, pw - 52 - 14)
        assert len(head_lines) <= 2, f"story {num}: headline too long"
        hy = y0 + 16
        for hl in head_lines:
            d.text((hx, hy), hl, font=f_head, fill=INK)
            hy += 30
        # icon + body
        icon_box = 84
        ix, iy = x0 + 18, y0 + 96
        draw_icon(d, icon, ix, iy, icon_box, accent)
        bx = x0 + 116
        bw = pw - 116 - 14
        body_lines = wrap(summary, f_body, bw)
        assert len(body_lines) <= 5, \
            f"story {num}: {len(body_lines)} body lines, max 5"
        by = y0 + 98
        for bl in body_lines:
            d.text((bx, by), bl, font=f_body, fill=(40, 40, 40))
            by += 25

    # ---- footer ----
    foot = "SIX STORIES SHAPING THE WORLD  \u00b7  18 NOVEMBER 2026"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, H - 44), foot, font=f_foot, fill=MUTED)
    d.line([(margin, H - 56), (W - margin, H - 56)], fill=PANEL_EDGE, width=2)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
