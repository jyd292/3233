# -*- coding: utf-8 -*-
"""可复用的高保真页面骨架 / 区块"""
from ds import *


def page_head(y, kicker, title, lead, right=None, h=214, en=""):
    """浅色页头：栏目 kicker + 大标题 + 导语 + 右侧统计。"""
    p = [r(0, y, W, h, PAPER)]
    p.append(ln(0, y + h, W, y + h, LINE))
    p.append(r(CX, y + 44, 8, 8, GRASS))
    p.append(t(CX + 18, y + 53, kicker, 11, GRASS_D, 700, family=MONO, ls=1.5))
    p.append(t(CX, y + 106, title, 40, INK, 800, ls=0.5))
    if lead:
        p.append(t(CX, y + 142, lead, 15, MUT))
    if en:
        p.append(t(CX + CW, y + 60, en.upper(), 11, MUT2, 700, "end", MONO, 2))
    if right:
        for i, (n, l) in enumerate(right):
            xx = CX + CW - (len(right) - i) * 150
            p.append(stat(xx, y + 110, n, l, INK, 30))
    return "".join(p)


def filter_row(y, groups, right="", active_first=True, x=CX, width=CW):
    p = [r(x, y, width, 60, CARD, LINE, 1)]
    cx = x + 20
    for gi, (label, opts) in enumerate(groups):
        if label:
            p.append(t(cx, y + 37, label, 11, MUT2, 700, ls=0.5))
            cx += len(label) * 11 + 20
        for i, o in enumerate(opts):
            w = len(o) * 13 + 26
            on = active_first and i == 0
            if on:
                p.append(r(cx, y + 15, w, 30, INK))
                p.append(t(cx + w / 2, y + 35, o, 12, GRASS_L, 700, "middle"))
            else:
                p.append(r(cx, y + 15, w, 30, PAPER))
                p.append(t(cx + w / 2, y + 35, o, 12, MUT, 400, "middle"))
            cx += w + 8
        cx += 22
    if right:
        p.append(t(x + width, y - 12, right, 11, MUT2, 400, "end"))
    return "".join(p)


def pager(y, n=6, active=1, x=CX):
    p = []
    total = n * 40 + (n - 1) * 8 + 60
    cx = W / 2 - total / 2
    p.append(r(cx, y, 40, 40, CARD, LINE, 1))
    p.append(icon(cx + 12, y + 13, "chevron", MUT2, 14))
    cx += 48
    for i in range(n):
        on = (i + 1 == active)
        p.append(r(cx, y, 40, 40, INK if on else CARD, None if on else LINE, 1))
        p.append(t(cx + 20, y + 26, str(i + 1), 13, GRASS_L if on else MUT, 700 if on else 400, "middle"))
        cx += 48
    p.append(r(cx, y, 40, 40, CARD, LINE, 1))
    p.append(icon(cx + 12, y + 13, "chevron", INK, 14))
    return "".join(p)


def cover_card(x, y, w, h, title, cat, meta, var, target, tag=None, footer_left="", idx=""):
    """资源卡片：方块封面 + 分类 + 标题 + 元信息 + 底部动作。"""
    p = [card_frame(x, y, w, h, CARD, LINE)]
    art_h = int(h * 0.44)
    p.append(voxel(x + 1, y + 1, w - 2, art_h, var, hash(title) % 97 + 1))
    p.append(r(x + 1, y + 1, w - 2, art_h, "none", LINE))
    if idx:
        p.append(r(x + 12, y + 12, 30, 22, INK, op=0.82))
        p.append(t(x + 27, y + 27, idx, 10, GRASS_L, 700, "middle", MONO))
    if tag:
        p.append(r(x + w - 12 - len(tag) * 10 - 14, y + 12, len(tag) * 10 + 14, 22, INK, op=0.82))
        p.append(t(x + w - 19, y + 27, tag, 10, "#EAF2E0", 700, "end"))
    yy = y + art_h + 32
    p.append(t(x + 18, yy, cat, 11, GRASS_D, 700, ls=1.2))
    p.append(t(x + 18, yy + 26, title, 17, INK, 800))
    p.append(t(x + 18, yy + 50, meta, 12, MUT))
    p.append(ln(x + 18, y + h - 50, x + w - 18, y + h - 50, LINE))
    p.append(t(x + 18, y + h - 24, footer_left, 11, MUT2, 400, family=MONO))
    p.append(t(x + w - 18, y + h - 24, "查看 →", 12, GRASS_D, 700, "end"))
    return link(target, "".join(p))


def row_card(x, y, w, h, title, meta, tags, target, right="", thumb=None, var="forest", idx=""):
    p = [card_frame(x, y, w, h, CARD, LINE)]
    if thumb:
        p.append(voxel(x + 1, y + 1, thumb, h - 2, var, hash(title) % 91 + 2))
        p.append(r(x + 1, y + 1, thumb, h - 2, "none", LINE))
        tx = x + thumb + 20
    else:
        tx = x + 20
    if idx:
        p.append(t(x + 16, y + 26, idx, 10, GRASS_D, 700, family=MONO, ls=1))
        p.append(t(tx, y + 30, title, 16, INK, 800))
        p.append(t(tx, y + 54, meta, 12, MUT))
    else:
        p.append(t(tx, y + 32, title, 16, INK, 800))
        p.append(t(tx, y + 56, meta, 12, MUT))
    xx = tx
    for tg in tags[:3]:
        tp, nx = tag_pill(xx, y + h - 34, tg, GRASS_D, GRASS_SOFT)
        p.append(tp)
        xx = nx + 8
    if right:
        p.append(t(x + w - 20, y + h - 22, right, 11, MUT2, 400, "end"))
    else:
        p.append(t(x + w - 20, y + 32, "→", 14, GRASS_D, 700, "end"))
    return link(target, "".join(p))


def side_download(y, cfg):
    """右侧深色下载面板。"""
    x, w = CX + 820, 380
    h = cfg.get("h", 402)
    p = [r(x, y, w, h, INK)]
    p.append(r(x, y, 4, h, GRASS))
    p.append(t(x + 24, y + 38, cfg.get("title", "下载与安装"), 16, "#F2F7E8", 800))
    p.append(t(x + 24, y + 58, cfg.get("en", "GET IT NOW"), 9, "#7C8B77", 700, family=MONO, ls=1.5))
    if cfg.get("version"):
        p.append(r(x + 24, y + 76, w - 48, 44, INK3, "#2C3C2F", 1))
        p.append(t(x + 38, y + 103, "版本", 11, MUT2))
        p.append(t(x + w - 24, y + 103, cfg["version"], 13, "#EAF2E0", 700, "end", MONO))
        p.append(icon(x + w - 40, y + 91, "chevron", GRASS_L, 12))
    rows = cfg.get("rows", [])
    for i, (k, v) in enumerate(rows):
        yy = y + 142 + i * 26
        p.append(t(x + 24, yy, k, 11, MUT2))
        p.append(t(x + w - 24, yy, v, 11, "#D6E0CC", 600, "end"))
    by = y + h - 138
    p.append(link(cfg.get("target", ""), r(x + 24, by, w - 48, 52, GRASS) + r(x + 28, by, w - 56, 3, GRASS_L) +
                  t(x + 24 + (w - 48) / 2 - 30, by + 32, cfg.get("btn", "立即下载"), 15, WHITE, 800) +
                  icon(x + w - 56, by + 18, "download", WHITE, 18)))
    p.append(r(x + 24, by + 60, w - 48, 40, "none", "#3A4C3C", 1))
    p.append(t(x + 24 + (w - 48) / 2, by + 85, cfg.get("btn2", "查看安装说明"), 12, "#D6E0CC", 600, "middle"))
    p.append(t(x + 24, y + h - 16, cfg.get("note", "已通过安全扫描 · 官方源"), 10, GRASS_L))
    return "".join(p)


def related(y, items, title="相关推荐", desc="跨频道打通：下载 / 攻略 / 社区（R4）"):
    p = [sec_head(CX, y, "04", title, "RELATED", desc)]
    cy = y + 56
    cw = (CW - 3 * 24) / 4
    for i, (nm, cat, meta, var, tg) in enumerate(items[:4]):
        p.append(cover_card(CX + i * (cw + 24), cy, cw, 320, nm, cat, meta, var, tg))
    return "".join(p), cy + 320


def section_banner(y, title, desc, btn_label, target, h=180):
    p = [r(CX, y, CW, h, INK)]
    p.append(r(CX, y, 6, h, GRASS))
    p.append(t(CX + 40, y + 60, title, 28, "#F4F8EC", 800))
    p.append(t(CX + 40, y + 92, desc, 14, "#A9B9A2"))
    p.append(link(target, r(CX + CW - 214, y + h / 2 - 24, 174, 48, GRASS) +
                  t(CX + CW - 214 + 87 - 14, y + h / 2 + 8, btn_label, 14, WHITE, 800, "middle") +
                  icon(CX + CW - 42, y + h / 2 - 6, "arrow", WHITE, 12)))
    return "".join(p)


def detail_title(y, kicker, title, meta, chips=(), rating=None, h=250, bg=PAPER):
    p = [r(0, y, W, h, bg)]
    p.append(ln(0, y + h, W, y + h, LINE))
    p.append(t(CX, y + 48, kicker, 11, GRASS_D, 700, family=MONO, ls=1.6))
    p.append(t(CX, y + 106, title, 44, INK, 800, ls=0.5))
    p.append(t(CX, y + 140, meta, 13, MUT))
    cx = CX
    for i, c in enumerate(chips):
        tp, nx = tag_pill(cx, y + 166, c, INK, PAPER2)
        p.append(tp)
        cx = nx + 10
    if rating:
        p.append(t(CX + CW, y + 92, rating[0], 34, INK, 800, "end", MONO))
        p.append(t(CX + CW, y + 118, rating[1], 10, MUT, 400, "end"))
        for i in range(5):
            full = i < int(float(rating[0]))
            p.append(icon(CX + CW - 20 - (5 - i) * 18, y + 136, "star", AMBER if full else LINE2, 14))
    return "".join(p)


def cover_panel(x, y, w, h, var="forest", label="", meta="", tag=""):
    p = [voxel(x, y, w, h, var, hash(label) % 83 + 5)]
    p.append(r(x, y, w, h, "none", LINE, 1))
    if tag:
        p.append(r(x + 16, y + 16, len(tag) * 11 + 20, 24, INK, op=0.85))
        p.append(t(x + 26, y + 32, tag, 11, GRASS_L, 700))
    if label:
        p.append(r(x, y + h - 56, w, 56, INK, op=0.72))
        p.append(t(x + 20, y + h - 26, label, 14, "#F2F7E8", 700))
        p.append(t(x + w - 20, y + h - 26, meta, 11, "#A9B9A2", 400, "end", MONO))
    return "".join(p)


def body_paras(x, y, w, title, paras, size=14, lh=26):
    p = [t(x, y, title, 20, INK, 800)]
    p.append(ln(x, y + 14, x + w, y + 14, LINE2))
    yy = y + 44
    for s in paras:
        p.append(para(x, yy, s, size, MUT, lh, w))
        yy += lh * (1 + len(s) // max(1, int(w / size)))
    return "".join(p), yy + 16


def feature_grid(x, y, w, items, cols=2):
    p = []
    cw = (w - 20 * (cols - 1)) / cols
    for i, (ic, tt, ds) in enumerate(items):
        row, col = divmod(i, cols)
        xx = x + col * (cw + 20)
        yy = y + row * 104
        p.append(r(xx, yy, cw, 92, PAPER, LINE, 1))
        p.append(r(xx, yy, 3, 92, GRASS))
        p.append(icon(xx + 20, yy + 22, ic, GRASS_D, 18))
        p.append(t(xx + 52, yy + 38, tt, 14, INK, 700))
        p.append(t(xx + 52, yy + 60, ds, 11, MUT))
    rows = (len(items) + cols - 1) // cols
    return "".join(p), y + rows * 104


def steps_list(x, y, w, steps):
    p = []
    for i, (tt, ds) in enumerate(steps):
        yy = y + i * 66
        p.append(r(x, yy, 32, 32, INK))
        p.append(t(x + 16, yy + 21, str(i + 1).zfill(2), 11, GRASS_L, 700, "middle", MONO))
        p.append(t(x + 48, yy + 15, tt, 14, INK, 700))
        p.append(t(x + 48, yy + 36, ds, 12, MUT))
        if i < len(steps) - 1:
            p.append(ln(x + 16, yy + 36, x + 16, yy + 64, LINE2, 1, "2 3"))
    return "".join(p), y + len(steps) * 66


def spec_table(x, y, w, rows, head=("项目", "说明", "适用"), widths=(180, 420, 120)):
    p = [r(x, y, w, 40, INK)]
    cx = x + 16
    for i, hd in enumerate(head):
        p.append(t(cx, y + 25, hd, 11, "#C9D6BE", 700, family=MONO, ls=1))
        cx += widths[i]
    for j, row in enumerate(rows):
        yy = y + 40 + j * 44
        p.append(r(x, yy, w, 44, CARD if j % 2 == 0 else PAPER))
        cx = x + 16
        for i, cell in enumerate(row):
            p.append(t(cx, yy + 28, cell, 12 if i == 0 else 12, MUT if i == 0 else INK, 700 if i == 0 else 400))
            cx += widths[i]
        p.append(ln(x, yy + 44, x + w, yy + 44, LINE))
    return "".join(p), y + 40 + len(rows) * 44
