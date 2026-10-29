# -*- coding: utf-8 -*-
"""MC HUB 高保真设计系统 · 方块像素语言
画布 1920 / 安全宽 1200 / 12 列栅格；仅使用 rect / line / text，保证可回写 Adobe XD。
"""
import html
import random

W = 1920
CX, CW = 360, 1200
GUT = 24

# ---------- 色板（主题 / 背景 / 辅助 / 强调，≤4 主色 + 中性） ----------
INK = "#0C130D"
INK2 = "#141F17"
INK3 = "#1D2B21"
PAPER = "#F4F5EE"
PAPER2 = "#E9ECDF"
CARD = "#FFFFFF"
LINE = "#D7DEC9"
LINE2 = "#B7C2A6"
MUT = "#6D7A66"
MUT2 = "#98A38F"
GRASS = "#6EA832"
GRASS_L = "#93C94A"
GRASS_D = "#4A781B"
GRASS_SOFT = "#EAF3DB"
AMBER = "#D9A13B"
AMBER_SOFT = "#FBF0D6"
BLUE = "#3D7FA6"
BLUE_SOFT = "#E2EFF4"
PURPLE = "#7A67AE"
PINK = "#C4699A"
PINK_SOFT = "#F8E7EF"
WHITE = "#FFFFFF"

FONT = "Noto Sans CJK SC, Microsoft YaHei, sans-serif"
MONO = "DejaVu Sans Mono, Consolas, monospace"

# ---------- 基础绘制 ----------
def esc(s):
    return html.escape(str(s), quote=True)


def r(x, y, w, h, fill="none", stroke=None, sw=1, rx=0, dash=None, op=None):
    a = f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" fill="{fill}"'
    if rx:
        a += f' rx="{rx:g}"'
    if stroke:
        a += f' stroke="{stroke}" stroke-width="{sw:g}"'
    if dash:
        a += f' stroke-dasharray="{dash}"'
    if op is not None:
        a += f' opacity="{op:g}"'
    return a + "/>"


def ln(x1, y1, x2, y2, color=LINE, sw=1, dash=None, op=None):
    a = f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{color}" stroke-width="{sw:g}"'
    if dash:
        a += f' stroke-dasharray="{dash}"'
    if op is not None:
        a += f' opacity="{op:g}"'
    return a + "/>"


def t(x, y, s, size=15, color=INK, weight=400, anchor="start", family=None, ls=0, op=None):
    fam = family or FONT
    extra = f' letter-spacing="{ls:g}"' if ls else ""
    if op is not None:
        extra += f' opacity="{op:g}"'
    return (f'<text x="{x:g}" y="{y:g}" font-family="{fam}" font-size="{size:g}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}"{extra}>{esc(s)}</text>')


def wrap(s, size, width):
    """按像素宽度折行（中文全角 / 英文半角估算）。返回行列表。"""
    lines, cur, curw = [], "", 0.0
    for ch in s:
        cw = size if ord(ch) >= 0x2E80 else size * 0.56
        if curw + cw > width:
            lines.append(cur)
            cur, curw = "", 0.0
        cur += ch
        curw += cw
    if cur:
        lines.append(cur)
    return lines


def para(x, y, s, size=15, color=MUT, lh=26, width=None, weight=400):
    if width is None:
        return t(x, y, s, size, color, weight)
    out = []
    for i, line in enumerate(wrap(s, size, width)):
        out.append(t(x, y + i * lh, line, size, color, weight))
    return "".join(out)


# ---------- 像素图标（12×12 点阵，按 size 缩放） ----------
_ICONS = {
    "search": ["000000000000", "011111111000", "110000000110", "100000000010",
               "100000000010", "100000000010", "100000000010", "110000000110",
               "011111111000", "000000111100", "000001110000", "000011000000"],
    "download": ["000111100000", "000100100000", "000100100000", "000100100000",
                 "001111110000", "011000011000", "010000001000", "000000001000",
                 "000111111100", "000000000100", "000000000100", "000111111100"],
    "play": ["000000000000", "000110000000", "000111000000", "000111100000",
             "000111110000", "000111111000", "000111111100", "000111111110",
             "000111111110", "000111111000", "000110000000", "000000000000"],
    "user": ["000011000000", "000111100000", "000111100000", "000011000000",
             "001111110000", "011111111000", "011111111000", "011111111000",
             "011111111000", "011111111000", "011111111000", "000000000000"],
    "arrow": ["000000000000", "000000000000", "000000000000", "000000000000",
              "011111111110", "000000000010", "000000000010", "000000000000",
              "000000000000", "000000000000", "000000000000", "000000000000"],
    "chevron": ["000000000000", "000000000000", "001100000000", "000110000000",
                "000011000000", "000001100000", "000000110000", "000000000000",
                "000000000000", "000000000000", "000000000000", "000000000000"],
    "forum": ["001111111100", "011000000110", "010000000010", "010000000010",
              "010000000010", "010000000010", "011111111110", "000000000110",
              "000000001100", "000000011000", "000000010000", "000000000000"],
    "server": ["000111111000", "001100001100", "011000000110", "001111111100",
               "000111111000", "000000000000", "000111111000", "001100001100",
               "011000000110", "001111111100", "000111111000", "000000000000"],
    "video": ["000000000000", "001111111100", "011000000110", "010011001010",
              "010011001010", "010011001010", "010011001010", "011000000110",
              "001111111100", "000000000000", "000000000000", "000000000000"],
    "book": ["000111111100", "001000000010", "001000000010", "001111111110",
             "001000000010", "001000000010", "001111111110", "001000000010",
             "001000000010", "001111111110", "000000000000", "000000000000"],
    "cube": ["000011110000", "000111111000", "001100001100", "011000000110",
             "010000000010", "010000000010", "011000000110", "001100001100",
             "000111111000", "000011110000", "000000000000", "000000000000"],
    "star": ["000001000000", "000011100000", "001111111000", "011111111100",
             "111111111110", "111111111110", "011111111100", "001111111000",
             "000011100000", "000001000000", "000000000000", "000000000000"],
    "fire": ["000010000000", "000111000000", "001111100000", "011111110000",
             "011111111000", "111111111100", "111111111100", "111111111000",
             "011111110000", "001111000000", "000100000000", "000000000000"],
    "check": ["000000000000", "000000000010", "000000000110", "000000001100",
              "000000011000", "000000110000", "000001100000", "000011000000",
              "000110000000", "001100000000", "000000000000", "000000000000"],
    "clock": ["000111111000", "001100001100", "011000000110", "011000000110",
              "011001100110", "011001100110", "011001111110", "011000000110",
              "001100001100", "000111111000", "000000000000", "000000000000"],
    "mail": ["000000000000", "011111111110", "011000000010", "011000000010",
             "011100001110", "011011011010", "011001110010", "011000000010",
             "011000000010", "011111111110", "000000000000", "000000000000"],
    "shield": ["001111111100", "011000000110", "011000000110", "011000000110",
               "011000000110", "011000000110", "001100001100", "000110011000",
               "000011110000", "000001100000", "000000000000", "000000000000"],
    "filter": ["000000000000", "001111111100", "000000000000", "000111111000",
               "000000000000", "000011110000", "000000000000", "000001100000",
               "000000000000", "000000000000", "000000000000", "000000000000"],
    "like": ["000110011000", "001111111100", "011111111110", "011111111110",
             "011111111110", "001111111100", "000110011000", "000000000000",
             "000000000000", "000000000000", "000000000000", "000000000000"],
    "reply": ["001111111100", "011000000110", "010000000010", "010000000010",
              "010000000010", "011000000110", "001111111100", "000000000110",
              "000000001100", "000000011000", "000000000000", "000000000000"],
    "eye": ["000011110000", "001100001100", "011000000110", "110011110011",
            "110011110011", "011000000110", "001100001100", "000011110000",
            "000000000000", "000000000000", "000000000000", "000000000000"],
    "grid": ["000000000000", "011111111110", "010000000010", "010000000010",
             "011111111110", "010000000010", "010000000010", "011111111110",
             "010000000010", "010000000010", "011111111110", "000000000000"],
    "plus": ["000001100000", "000001100000", "000001100000", "000111111000",
             "000111111000", "000001100000", "000001100000", "000001100000",
             "000000000000", "000000000000", "000000000000", "000000000000"],
    "link": ["000000000000", "001111000000", "011001100000", "011001100000",
             "001111000000", "000111100000", "000000111100", "000000011000",
             "000000011000", "000000000000", "000000000000", "000000000000"],
}


def icon(x, y, name, color=INK, size=20, op=None):
    m = _ICONS.get(name)
    if not m:
        return ""
    cell = size / 12.0
    out = []
    for row, bits in enumerate(m):
        run = 0
        for col, b in enumerate(bits + "0"):
            if b == "1":
                run += 1
                continue
            if run:
                out.append(r(x + (col - run) * cell, y + row * cell, run * cell, cell, color, op=op))
                run = 0
    return "".join(out)


# ---------- 像素方块场景 ----------
_PAL = {
    "forest": dict(sky1="#BBDDEA", sky2="#E4F0D8", sun="#F3CE72", hill1="#8FB373",
                   hill2="#6E9455", ground="#77AE35", ground2="#5C8A25", dirt="#8A6A46",
                   dirt2="#6F5336", trunk="#6B4A2C", leaf1="#4F8B2F", leaf2="#3E7024",
                   water="#5C9FB8", water2="#8CC7D8"),
    "village": dict(sky1="#C6E2E8", sky2="#F3EFD2", sun="#EFC463", hill1="#9CB77A",
                    hill2="#7C9A5D", ground="#7FB63C", ground2="#609026", dirt="#93734B",
                    dirt2="#745737", trunk="#7A5632", leaf1="#5A9636", leaf2="#457428",
                    water="#5FA5BB", water2="#93CBD9"),
    "night": dict(sky1="#182519", sky2="#2A3B27", sun="#D9D08A", hill1="#2C4029",
                  hill2="#22331F", ground="#3E5E2A", ground2="#314A20", dirt="#4A3D2A",
                  dirt2="#382D1F", trunk="#4A3521", leaf1="#2E5426", leaf2="#24431D",
                  water="#264B54", water2="#3B6E7A"),
    "nether": dict(sky1="#3A1D18", sky2="#5A2A1E", sun="#F0A05A", hill1="#7A3324",
                   hill2="#5C2418", ground="#8C3B2A", ground2="#6E2A1D", dirt="#552017",
                   dirt2="#3F160F", trunk="#4A2018", leaf1="#9A4A2A", leaf2="#7A341E",
                   water="#B4522A", water2="#D97A3E"),
    "ocean": dict(sky1="#A9D6E5", sky2="#E7F4EC", sun="#F2D07E", hill1="#7FAE8B",
                  hill2="#639471", ground="#DEC9A0", ground2="#C4AC82", dirt="#A88F68",
                  dirt2="#8A7252", trunk="#6B4A2C", leaf1="#4F8B2F", leaf2="#3E7024",
                  water="#4B93B0", water2="#7FBCCF"),
}


def _blocks(x, y, w, h, color, step=16, seed=0):
    """在矩形内铺像素块（轻微色差），形成方块质感。"""
    rnd = random.Random(seed)
    out = [r(x, y, w, h, color)]
    base = color.lstrip("#")
    br, bg, bb = int(base[0:2], 16), int(base[2:4], 16), int(base[4:6], 16)
    cols = max(1, int(w // step))
    rows = max(1, int(h // step))
    for i in range(cols):
        for j in range(rows):
            if rnd.random() < 0.22:
                d = rnd.choice([-8, -4, 4, 8])
                c = "#%02X%02X%02X" % (max(0, min(255, br + d)), max(0, min(255, bg + d)), max(0, min(255, bb + d)))
                out.append(r(x + i * step, y + j * step, min(step, w - i * step), min(step, h - j * step), c))
    return "".join(out)


def _emblem(x, y, w, h, p, seed):
    """小尺寸方块徽记：3×3 方块矩阵 + 高光/阴影。"""
    rnd = random.Random(seed)
    out = [r(x, y, w, h, p["sky1"])]
    cols, rows = 3, 3
    bw, bh = w / cols, h / rows
    pal = [p["ground"], p["hill2"], p["leaf1"], p["water"], p["dirt"], p["ground2"]]
    for i in range(cols):
        for j in range(rows):
            c = pal[(i * 2 + j * 3 + rnd.randint(0, 2)) % len(pal)]
            out.append(r(x + i * bw, y + j * bh, bw, bh, c))
            out.append(r(x + i * bw, y + j * bh, bw, 2, "#FFFFFF", op=0.14))
            out.append(r(x + i * bw, y + (j + 1) * bh - 2, bw, 2, "#000000", op=0.12))
    out.append(r(x, y, w, h, "none", INK, 2))
    return "".join(out)


def block_icon(x, y, w, h, top=GRASS, soil="#8A6A46", accent=None, seed=0):
    """单块「草方块」图标：顶面草色 + 泥土 + 像素颗粒，用于服务器/资源缩略。"""
    out = [r(x, y, w, h, soil)]
    out.append(r(x, y, w, h * 0.30, top))
    out.append(r(x, y, w, h * 0.06, GRASS_L if top == GRASS else "#FFFFFF", op=0.45))
    rnd = random.Random(seed)
    cell = max(4, h / 8)
    for i in range(4):
        for j in range(2, 7):
            if rnd.random() < 0.35:
                out.append(r(x + i * cell * 1.6 + 2, y + j * cell, cell * 0.9, cell * 0.7, "#000000", op=0.12))
    if accent:
        out.append(r(x + w * 0.62, y + h * 0.58, w * 0.26, h * 0.26, accent))
    out.append(r(x, y, w, h, "none", INK, 2))
    return "".join(out)


def voxel(x, y, w, h, variant="forest", seed=1):
    """方块风景：天空分层 + 像素太阳 + 云 + 阶梯山体 + 树 + 水塘（严格裁在框内）。"""
    p = _PAL.get(variant, _PAL["forest"])
    rnd = random.Random(seed)
    if w < 120 or h < 90:
        return _emblem(x, y, w, h, p, seed)
    right, bottom = x + w, y + h
    out = []
    bands = 10
    for i in range(bands):
        f = i / (bands - 1)
        c1, c2 = p["sky1"].lstrip("#"), p["sky2"].lstrip("#")
        c = "#%02X%02X%02X" % tuple(int(int(c1[k:k + 2], 16) * (1 - f) + int(c2[k:k + 2], 16) * f) for k in (0, 2, 4))
        out.append(r(x, y + i * h / bands, w, h / bands + 1, c))
    # 像素太阳
    ss = max(22, min(40, h * 0.10))
    sx, sy = x + w * 0.74, y + h * 0.17
    out.append(r(sx - ss / 2, sy - ss / 2, ss, ss, p["sun"]))
    for dx, dy in [(-ss * 1.5, 0), (ss * 1.5, 0), (0, -ss * 1.5), (0, ss * 1.5)]:
        out.append(r(sx + dx - ss * 0.14, sy + dy - ss * 0.14, ss * 0.28, ss * 0.28, p["sun"], op=0.45))
    # 方块云
    for i in range(3):
        cw = min(rnd.randint(60, 150), int(w * 0.30))
        cx = rnd.randint(int(x + 8), int(right - cw - 8))
        cy = rnd.randint(int(y + h * 0.08), int(y + h * 0.30))
        for k in range(3):
            out.append(r(cx + k * cw / 4.2, cy + (k % 2) * h * 0.028, cw / 2.4, max(10, h * 0.075), WHITE, op=0.8))
    # 阶梯远山
    for layer, (col, amp) in enumerate([(p["hill1"], 0.17), (p["hill2"], 0.11)]):
        cx = x
        yy = y + h * 0.60 + layer * h * 0.045
        while cx < right:
            seg = rnd.randint(int(w / 9), int(w / 5))
            hh = rnd.randint(max(8, int(h * amp * 0.55)), max(10, int(h * amp)))
            out.append(r(cx, yy - hh, min(seg, right - cx), hh, col))
            cx += seg
    # 草地 + 泥土
    gy = y + h * 0.72
    out.append(_blocks(x, gy, w, bottom - gy, p["ground"], max(12, min(24, int(w / 14))), seed))
    out.append(r(x, gy, w, max(6, h * 0.022), p["ground2"]))
    out.append(r(x, bottom - max(6, h * 0.05), w, max(6, h * 0.05), p["dirt"], op=0.9))
    # 水塘（限制在画面内）
    if h >= 200:
        wx = x + w * 0.10
        wy = gy + h * 0.10
        wh = min(h * 0.15, bottom - wy - 4)
        if wh > 16:
            out.append(_blocks(wx, wy, w * 0.32, wh, p["water"], 22, seed + 7))
            for i in range(3):
                out.append(r(wx + 14 + i * (w * 0.09), wy + wh * 0.35 + (i % 2) * wh * 0.3, w * 0.09, 5, p["water2"], op=0.85))
    # 村庄小屋（village 变体）
    if variant == "village":
        hw = min(150, w * 0.24)
        hh = hw * 0.55
        hx = x + w * 0.60
        hb = gy + h * 0.06
        out.append(r(hx, hb - hh, hw, hh, "#B08A5C"))
        for i in range(int(hw // 12)):
            out.append(r(hx + i * 12, hb - hh, 1, hh, "#8A6A46", op=0.7))
        out.append(r(hx, hb - hh * 0.42, hw, 5, "#8A6A46"))
        # 阶梯屋顶
        for k in range(3):
            rw = hw + 26 - k * 26
            out.append(r(hx - 13 + k * 13, hb - hh - 16 - k * 14, rw, 14, "#4A3A2A" if k % 2 == 0 else "#5C4630"))
        out.append(r(hx + hw / 2 - 14, hb - hh * 0.46, 28, hh * 0.46, "#4A3A2A"))
        out.append(r(hx + hw * 0.16, hb - hh * 0.78, 22, 20, "#BFD8DE", "#4A3A2A", 2))
        out.append(r(hx + hw - 40, hb - hh * 0.78, 22, 20, "#BFD8DE", "#4A3A2A", 2))
        out.append(r(hx + hw - 28, hb - hh - 34, 6, 20, "#6B4A2C"))
        out.append(r(hx + hw - 32, hb - hh - 38, 14, 10, "#D9A13B"))
    # 树（阶梯状像素树冠）
    n_tree = 2 if w < 420 else 3
    for i in range(n_tree):
        tw = max(8, min(14, w * 0.022))
        tx = x + w * (0.20 + i * 0.30) + rnd.randint(-18, 18)
        tx = max(x + 20, min(tx, right - 60))
        th = h * (0.13 + 0.02 * i)
        ty = gy + h * 0.01
        out.append(r(tx, ty - th, tw, th, p["trunk"]))
        out.append(r(tx, ty - th, tw, 4, "#000000", op=0.18))
        cw = min(66, w * 0.11)
        ch = h * 0.19
        rows = 5
        for k in range(rows):
            bw = cw * (0.44 + 0.56 * (1 - abs(k - 2) / 2.6))
            out.append(r(tx + tw / 2 - bw / 2, ty - th - ch + k * ch / rows, bw, ch / rows + 1,
                         p["leaf1"] if k % 2 == 0 else p["leaf2"]))
    # 前景草丛（像素点）
    for i in range(8):
        bx = x + i * w / 8 + 4
        out.append(r(bx, gy - h * 0.028, max(10, w * 0.022), h * 0.028, p["ground"] if i % 2 == 0 else p["ground2"]))
    out.append(r(x, y, w, h, "none", INK, 2))
    return "".join(out)


def link(target, content):
    """可点击热区：SVG 内 <a> 在浏览器直接跳转，同时携带 data-target 供 XD 连线使用。"""
    return f'<a href="{target}.html" data-target="{target}">{content}</a>'


# ---------- 组件 ----------
def btn(x, y, w, h, label, kind="primary", size=15, arrow=False):
    if kind == "primary":
        base = r(x, y, w, h, GRASS) + r(x, y, w, 3, GRASS_L)
        base += r(x + 4, y + h - 4, w - 4, 4, GRASS_D)
        col, txtc = GRASS, WHITE
    elif kind == "dark":
        base = r(x, y, w, h, INK2, "#3A4C3C", 2) + r(x, y, w, 3, "#2A3A2C")
        col, txtc = INK2, "#EAF2E0"
    elif kind == "ghost":
        base = r(x, y, w, h, "none", LINE2, 2)
        col, txtc = "none", INK
    else:
        base = r(x, y, w, h, WHITE, LINE2, 2)
        col, txtc = WHITE, INK
    tx = x + w / 2 - (10 if arrow else 0)
    base += t(tx, y + h / 2 + size * 0.36, label, size, txtc, 700, "middle")
    if arrow:
        base += icon(x + w - 26, y + h / 2 - 6, "arrow", txtc, 12)
    return base


def badge(x, y, label, color=GRASS, bg=GRASS_SOFT, size=11):
    w = len(label) * size * 0.95 + 14
    return r(x, y, w, 22, bg) + r(x, y, 3, 22, color) + t(x + 10, y + 15, label, size, color, 700), x + w


def chip(x, y, label, active=False, size=13):
    w = len(label) * size + 26
    if active:
        return r(x, y, w, 34, INK) + t(x + w / 2, y + 22, label, size, "#F2F7E8", 700, "middle"), x + w
    return r(x, y, w, 34, WHITE, LINE2, 1) + t(x + w / 2, y + 22, label, size, MUT, 400, "middle"), x + w


def sec_head(x, y, no, cn, en="", desc="", width=CW, color=INK):
    out = [t(x, y, no, 12, GRASS, 700, family=MONO, ls=1)]
    out.append(t(x + 46, y + 2, cn, 30, color, 800))
    if en:
        out.append(t(x + 46 + len(cn) * 30 + 16, y - 2, en.upper(), 11, MUT2, 700, family=MONO, ls=2))
    if desc:
        out.append(t(x + width, y, desc, 13, MUT, 400, "end"))
    out.append(ln(x, y + 24, x + width, y + 24, LINE2))
    out.append(r(x, y + 24, 64, 3, GRASS))
    return "".join(out)


def stat(x, y, num, label, color=INK, size=34):
    return (t(x, y, num, size, color, 800, family=MONO) +
            t(x, y + 22, label, 12, MUT))


def card_frame(x, y, w, h, fill=CARD, stroke=LINE, accent=None):
    out = [r(x, y, w, h, fill, stroke, 1)]
    out.append(r(x, y, 10, 2, stroke or LINE))
    out.append(r(x, y, 2, 10, stroke or LINE))
    out.append(r(x + w - 10, y + h - 2, 10, 2, stroke or LINE))
    out.append(r(x + w - 2, y + h - 10, 2, 10, stroke or LINE))
    if accent:
        out.append(r(x, y, 4, h, accent))
    return "".join(out)


def meta_row(x, y, items, size=12, color=MUT, gap=18):
    out = []
    cx = x
    for i, it in enumerate(items):
        if i:
            out.append(r(cx - gap / 2 - 1, y - 4, 2, 2, MUT2))
        out.append(t(cx, y, it, size, color))
        cx += len(it) * size * 0.62 + gap
    return "".join(out)


def avatar(x, y, s, kind=0, ring=LINE2):
    pal = [("#8FB373", "#4E7A2F"), ("#6E9455", "#3E6027"), ("#C4A06A", "#86643A"), ("#7E9BAA", "#4C6C7C")]
    a, b = pal[kind % len(pal)]
    out = [r(x, y, s, s, b), r(x + 2, y + 2, s - 4, s - 4, a)]
    out.append(r(x + s * 0.28, y + s * 0.42, s * 0.44, s * 0.16, b))
    out.append(r(x + s * 0.3, y + s * 0.66, s * 0.4, s * 0.1, b))
    out.append(r(x, y, s, s, "none", ring, 2))
    return "".join(out)


def topbar(active=None, y=0, dark=True):
    p = [r(0, y, W, 88, INK)]
    p.append(ln(0, y + 88, W, y + 88, INK3, 2))
    # logo：方块叠加
    p.append(r(CX, y + 24, 40, 40, GRASS))
    p.append(r(CX, y + 24, 40, 8, GRASS_L))
    p.append(r(CX + 8, y + 33, 24, 24, INK))
    p.append(r(CX + 13, y + 38, 14, 14, GRASS_L))
    logo = (t(CX + 54, y + 46, "MC HUB", 22, "#F3F8E9", 800, ls=1) +
            t(CX + 54, y + 66, "APPLICATIONS & COMMUNITY", 9, MUT2, 700, family=MONO, ls=1.6))
    p.append(link("P00", logo))
    x = CX + 236
    nav_targets = {"认识 MC": "P01", "下载中心": "P02", "社区交流": "P03",
                   "攻略视频": "P04", "关于与支持": "P05"}
    for n in ("认识 MC", "下载中心", "社区交流", "攻略视频", "关于与支持"):
        w = len(n) * 15 + 26
        seg = []
        if n == active:
            seg.append(t(x, y + 52, n, 15, GRASS_L, 700))
            seg.append(r(x, y + 62, len(n) * 15, 3, GRASS_L))
        else:
            seg.append(t(x, y + 52, n, 15, "#C6D2C2", 400))
        p.append(link(nav_targets[n], "".join(seg)))
        x += w + 6
    # 搜索
    p.append(link("G02", r(1236, y + 24, 244, 40, INK3, "#2C3C2F", 1) +
                  icon(1250, y + 34, "search", MUT2, 20) +
                  t(1278, y + 49, "搜索 MOD / 整合包 / 帖子", 12, MUT2) +
                  r(1488, y + 24, 30, 40, GRASS) + icon(1493, y + 34, "arrow", WHITE, 20)))
    # 登录
    p.append(link("G01", r(1536, y + 24, 156, 40, "none", "#3A4C3C", 1) +
                  icon(1550, y + 33, "user", "#C6D2C2", 22) +
                  t(1580, y + 49, "登录 / 注册", 13, "#DAE4D5", 600)))
    return "".join(p)


def footer(y, page_no=""):
    p = [r(0, y, W, 320, INK)]
    p.append(r(0, y, W, 4, GRASS))
    p.append(r(CX, y + 54, 34, 34, GRASS))
    p.append(r(CX + 7, y + 61, 20, 20, INK))
    p.append(t(CX + 46, y + 72, "MC HUB", 20, "#F3F8E9", 800))
    p.append(t(CX + 46, y + 92, "把 Minecraft 玩明白", 11, MUT2, 400, ls=0.5))
    cols = [("频道", [("认识 MC", "P01"), ("下载中心", "P02"), ("社区交流", "P03"),
                     ("攻略视频", "P04"), ("关于与支持", "P05")]),
            ("资源", [("启动器下载", "P0201"), ("整合包获取", "P0202"), ("MOD 下载", "P0203"),
                     ("资源包与光影", "P0204"), ("联机与语音工具", "P0205")]),
            ("社区", [("论坛板块", "P0301"), ("服务器与联机", "P0302"), ("个人中心", "P0303"),
                     ("我的内容", "P030301"), ("更新日志", "P0503")]),
            ("支持", [("关于我们", "P0501"), ("联系与反馈", "P0502"), ("用户协议与隐私", "P0504"),
                     ("常见问题", "P0104"), ("搜索结果", "G02")])]
    x = CX + 300
    for title, items in cols:
        p.append(t(x, y + 66, title, 13, GRASS_L, 700, ls=1))
        for i, (it, tg) in enumerate(items):
            p.append(link(tg, t(x, y + 96 + i * 30, it, 13, "#AFBDA9")))
        x += 226
    p.append(ln(CX, y + 246, CX + CW, y + 246, "#2A3A2C"))
    p.append(t(CX, y + 278, "© 2024 MC HUB · 界面交互应用综合实训 · 信息架构 V1.0 / 高保真 V1.0", 11, "#7C8B77"))
    p.append(t(CX + CW, y + 278, page_no, 11, "#7C8B77", 400, "end", MONO))
    return "".join(p)


def breadcrumb(y, items, note=""):
    p = [r(0, y, W, 52, PAPER2)]
    p.append(ln(0, y + 52, W, y + 52, LINE, 1))
    x = CX
    for i, it in enumerate(items):
        if i:
            p.append(icon(x - 14, y + 21, "chevron", MUT2, 12))
        color = INK if i == len(items) - 1 else MUT
        p.append(t(x, y + 32, it, 12, color, 700 if i == len(items) - 1 else 400))
        x += len(it) * 12 + 28
    if note:
        p.append(t(CX + CW, y + 32, note, 11, MUT2, 400, "end"))
    return "".join(p)


def page_strip(code, name, level, desc=""):
    """顶部细信息条：编号 / 页面 / 层级 / 画布"""
    p = [r(0, 0, W, 30, INK2)]
    p.append(t(24, 20, code, 10, "#93C94A", 700, family=MONO, ls=1))
    p.append(t(24 + len(code) * 7 + 10, 20, f"·  {name}  ·  {level}", 10, "#B9C8AE", 600))
    p.append(t(W - 24, 20, "1920 CANVAS · 1200 SAFE · 12 COL / 70+30", 9, "#7C8B77", 400, "end", MONO))
    if desc:
        p.append(t(W / 2, 20, desc, 9, "#7C8B77", 400, "middle", MONO))
    return "".join(p)


def tag_pill(x, y, label, color=INK, bg=PAPER2):
    w = len(label) * 11 * 0.95 + 16
    return r(x, y, w, 20, bg) + t(x + 8, y + 14, label, 11, color, 700), x + w
