# -*- coding: utf-8 -*-
"""
MC 社区平台 · Web 低保真线框生成器
依据：MC社区平台-信息架构图 V1.0 + 《破译Web UI》规范（1920 画布 / 1200 安全宽 / 12列 70+30）
输出：SVG（每页一张）+ index.html 预览
"""
import os, html

OUT = r"c:\Users\Administrator\Desktop\金方涵 240802181040（界面交互应用综合实训）\MC社区平台-低保真原型"
SVG_DIR = os.path.join(OUT, "svg")
os.makedirs(SVG_DIR, exist_ok=True)

# ---------- 设计变量 ----------
W = 1920
CX, CW = 360, 1200           # 安全宽 1200，左右留白 360（1920 画布）
HEADER_H = 84
COL_W, GUTTER = 70, 30       # 12 列栅格（1170）→ 在 1200 内均分使用
BG = "#FFFFFF"
SOFT = "#F5F5F7"
SOFT2 = "#ECECF0"
LINE = "#D9D9DF"
LINE2 = "#C3C3CB"
TXT = "#2E2E33"
MUT = "#8A8A93"
DARK = "#3A3A40"
ACC = "#6EA832"
ACC_SOFT = "#EDF4E4"
FONT = "Microsoft YaHei, PingFang SC, sans-serif"
MONO = "Consolas, monospace"

def esc(t):
    return html.escape(str(t), quote=True)

def rect(x, y, w, h, fill="none", stroke=None, sw=1, rx=0, dash=None, opacity=None):
    a = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'
    if rx: a += f' rx="{rx}"'
    if stroke: a += f' stroke="{stroke}" stroke-width="{sw}"'
    if dash: a += f' stroke-dasharray="{dash}"'
    if opacity is not None: a += f' opacity="{opacity}"'
    return a + '/>'

def line(x1, y1, x2, y2, color=LINE, sw=1, dash=None):
    a = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"'
    if dash: a += f' stroke-dasharray="{dash}"'
    return a + '/>'

def text(x, y, s, size=16, color=TXT, weight=400, anchor="start", family=None, ls=0):
    fam = family or FONT
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}" letter-spacing="{ls}">{esc(s)}</text>')

def img_ph(x, y, w, h, label="图片", rx=4):
    """图片占位：浅底 + 对角线 + 标签"""
    parts = [rect(x, y, w, h, SOFT2, LINE, 1, rx),
             line(x, y, x + w, y + h, LINE, 1),
             line(x + w, y, x, y + h, LINE, 1),
             text(x + w / 2, y + h / 2 + 5, label, 13, MUT, 400, "middle")]
    return "".join(parts)

def btn(x, y, w, h, label, kind="primary", size=15):
    if kind == "primary":
        return rect(x, y, w, h, ACC, None, 0, 4) + text(x + w/2, y + h/2 + 5, label, size, "#FFFFFF", 600, "middle")
    if kind == "ghost":
        return rect(x, y, w, h, "#FFFFFF", LINE2, 1, 4) + text(x + w/2, y + h/2 + 5, label, size, TXT, 500, "middle")
    return rect(x, y, w, h, SOFT, LINE, 1, 4) + text(x + w/2, y + h/2 + 5, label, size, MUT, 400, "middle")

def tag(x, y, s, color=MUT, bg=None):
    w = 12 + len(s) * 7.2
    out = rect(x, y, w, 22, bg or "#FFFFFF", LINE, 1, 3)
    out += text(x + 6, y + 15, s, 12, color, 400, "start", MONO)
    return out, x + w

# ---------- 通用区块 ----------
NAV = ["认识 MC", "下载中心", "社区交流", "攻略视频", "关于与支持"]

def header(active=None):
    p = [rect(0, 0, W, HEADER_H, "#FFFFFF"), line(0, HEADER_H, W, HEADER_H, LINE)]
    p.append(rect(CX, 26, 32, 32, ACC, None, 0, 4))
    p.append(rect(CX + 8, 34, 16, 16, "#FFFFFF", None, 0, 2, opacity=0.55))
    p.append(text(CX + 44, 52, "MC HUB", 20, TXT, 800, ls=0.5))
    x = CX + 300
    for i, n in enumerate(NAV):
        w = len(n) * 16 + 28
        if n == active:
            p.append(text(x + 6, 52, n, 16, TXT, 700))
            p.append(rect(x + 6, 62, len(n) * 16, 3, ACC))
        else:
            p.append(text(x + 6, 52, n, 16, MUT, 400))
        x += w
    # 搜索
    p.append(rect(1240, 22, 240, 40, SOFT, LINE, 1, 20))
    p.append(text(1262, 48, "搜索 MOD / 整合包 / 帖子…", 13, MUT))
    p.append(text(1448, 48, "搜索", 13, TXT, 500, "end"))
    # 登录
    p.append(rect(1500, 22, 96, 40, "#FFFFFF", LINE2, 1, 20))
    p.append(text(1548, 48, "登录 / 注册", 14, TXT, 500, "middle"))
    return "".join(p)

def breadcrumb(items, y):
    p = [rect(0, y, W, 48, SOFT), line(0, y + 48, W, y + 48, LINE)]
    s = "  ›  ".join(items)
    p.append(text(CX, y + 30, s, 13, MUT))
    p.append(text(W - CX, y + 30, "面包屑：每一级可点击返回（R2）", 12, "#B0B0B8", 400, "end"))
    return "".join(p)

def section_title(y, no, title, desc=""):
    p = [text(CX, y, no, 14, ACC, 700, family=MONO),
         text(CX + 48, y + 1, title, 30, TXT, 700)]
    if desc:
        p.append(text(CX + CW, y, desc, 14, MUT, 400, "end"))
    p.append(line(CX, y + 22, CX + CW, y + 22, LINE))
    return "".join(p), y + 22

def footer(y):
    p = [rect(0, y, W, 300, DARK)]
    cols = [("产品", ["认识 MC", "版本与玩法", "启动器", "整合包"]),
            ("资源", ["MOD 下载", "资源包与光影", "联机与语音", "更新日志"]),
            ("社区", ["论坛板块", "服务器与联机", "攻略视频", "个人中心"]),
            ("支持", ["关于我们", "联系与反馈", "用户协议与隐私", "404"])]
    x = CX
    for title, items in cols:
        p.append(text(x, y + 56, title, 15, "#FFFFFF", 700))
        for i, it in enumerate(items):
            p.append(text(x, y + 92 + i * 30, it, 13, "#B9B9C0"))
        x += 300
    p.append(line(CX, y + 236, CX + CW, y + 236, "#55555C"))
    p.append(text(CX, y + 266, "MC HUB · Minecraft 应用与社区交流平台   |   信息架构 V1.0   |   页面清单 41 个", 12, "#9C9CA4"))
    p.append(text(CX + CW, y + 266, "顶部导航常驻 6 入口 · 页脚四列兜底（R1 / R6）", 12, "#9C9CA4", 400, "end"))
    return "".join(p)

def page_tag(code, name, level, h=None):
    """页面标识改由 add() 顶部规范条统一绘制"""
    return ""

def canvas(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'{rect(0, 0, w, h, BG)}{body}</svg>')

def card(x, y, w, h, title, lines=2, img_h=150, tag_s=None, cta="查看详情"):
    p = [rect(x, y, w, h, "#FFFFFF", LINE, 1, 6)]
    p.append(img_ph(x + 1, y + 1, w - 2, img_h, "图片", 6))
    yy = y + img_h + 28
    if tag_s:
        t, _ = tag(x + 16, yy - 16, tag_s)
        p.append(t)
        yy += 18
    p.append(text(x + 16, yy, title, 17, TXT, 700))
    for i in range(lines):
        p.append(rect(x + 16, yy + 14 + i * 20, w - 32 - (i * 40), 8, SOFT2, None, 0, 4))
    p.append(text(x + 16, y + h - 18, cta, 13, ACC, 600))
    p.append(text(x + w - 16, y + h - 18, "→", 14, ACC, 600, "end"))
    return "".join(p)

def list_row(x, y, w, h, title, meta, right="→"):
    p = [rect(x, y, w, h, "#FFFFFF", LINE, 1, 6)]
    p.append(rect(x + 16, y + h/2 - 22, 44, 44, SOFT2, None, 0, 4))
    p.append(text(x + 76, y + h/2 - 2, title, 16, TXT, 600))
    p.append(text(x + 76, y + h/2 + 20, meta, 13, MUT))
    p.append(text(x + w - 24, y + h/2 + 6, right, 16, MUT, 400, "end"))
    return "".join(p)

def filter_bar(y, groups):
    p = [rect(CX, y, CW, 56, SOFT, LINE, 1, 6)]
    x = CX + 20
    for label, opts in groups:
        p.append(text(x, y + 34, label, 13, MUT, 600))
        x += len(label) * 14 + 12
        for i, o in enumerate(opts):
            w = len(o) * 14 + 26
            if i == 0:
                p.append(rect(x, y + 15, w, 26, ACC_SOFT, ACC, 1, 3))
                p.append(text(x + w/2, y + 33, o, 13, ACC, 600, "middle"))
            else:
                p.append(rect(x, y + 15, w, 26, "#FFFFFF", LINE, 1, 3))
                p.append(text(x + w/2, y + 33, o, 13, MUT, 400, "middle"))
            x += w + 10
        x += 24
    return "".join(p)

def pagination(y, n=5):
    p = []
    total = n * 44 + (n - 1) * 8
    x = W / 2 - total / 2
    for i in range(n):
        on = (i == 0)
        p.append(rect(x, y, 44, 40, ACC if on else "#FFFFFF", None if on else LINE, 1, 4))
        p.append(text(x + 22, y + 26, str(i + 1), 14, "#FFFFFF" if on else MUT, 600 if on else 400, "middle"))
        x += 52
    return "".join(p)

# ---------- 页面 ----------
pages = []

def add(code, name, level, w, h, body, desc):
    strip = (rect(0, 0, w, 40, "#EFEFF3") + line(0, 40, w, 40, LINE)
             + text(24, 26, f"{code}  {name}   ·   {level}   ·   {desc}", 13, TXT, 700, family=MONO)
             + text(w - 24, 26, f"{w} × {h}   |   安全宽 1200   |   12 列栅格", 12, MUT, 400, "end", MONO))
    svg = canvas(w, h + 40, strip + f'<g transform="translate(0,40)">{body}</g>')
    fn = f"{code}_{name.replace('/', '-')}.svg"
    with open(os.path.join(SVG_DIR, fn), "w", encoding="utf-8") as f:
        f.write(svg)
    pages.append((code, name, level, fn, w, h + 40, desc))

# ===== P00 首页 =====
def p_home():
    H = 2780
    b = [header()]
    b.append(page_tag("P00", "首页", "L1"))
    # Hero
    b.append(rect(0, HEADER_H, W, 620, SOFT))
    b.append(img_ph(CX, HEADER_H + 70, 560, 480, "主视觉 / 游戏场景 16:9", 8))
    b.append(text(CX + 620, HEADER_H + 150, "认识 → 获取 → 交流 → 学习", 14, ACC, 700, family=MONO, ls=1))
    b.append(text(CX + 620, HEADER_H + 226, "从第一夜到服务器联机，", 48, TXT, 800))
    b.append(text(CX + 620, HEADER_H + 292, "把 Minecraft 玩明白。", 48, TXT, 800))
    b.append(text(CX + 620, HEADER_H + 344, "版本 / 启动器 / 整合包 / MOD / 光影，一站式获取；论坛、服务器、视频攻略，一站式交流。", 17, MUT))
    b.append(btn(CX + 620, HEADER_H + 392, 190, 52, "开始入门"))
    b.append(btn(CX + 830, HEADER_H + 392, 190, 52, "前往下载中心", "ghost"))
    b.append(text(CX + 620, HEADER_H + 500, "当前在线 12,480 人   ·   今日新帖 236   ·   资源总量 1,860", 13, MUT))
    # 六入口
    y = 780
    t, y2 = section_title(y, "01", "六个入口，三次点击内到达", "结构原则：层级 ≤ 5，任意页 3 次点击可达")
    b.append(t)
    ent = [("认识 MC", "guide.html", "L2"), ("下载中心", "download.html", "L2"), ("社区交流", "community.html", "L2"),
           ("攻略视频", "video.html", "L2"), ("关于与支持", "about.html", "L2"), ("全局搜索", "search.html", "G")]
    gap = 20
    cw = (CW - gap * 2) // 3
    for i, (nm, url, lv) in enumerate(ent):
        r, c = divmod(i, 3)
        x = CX + c * (cw + gap)
        yy = y2 + 24 + r * 176
        b.append(rect(x, yy, cw, 156, "#FFFFFF", LINE, 1, 8))
        b.append(rect(x + 20, yy + 20, 44, 44, ACC_SOFT, ACC, 1, 6))
        b.append(text(x + 60, yy + 70, nm, 20, TXT, 700))
        b.append(text(x + 20, yy + 108, f"{url}   ·   {lv}", 12, MUT, 400, family=MONO))
        b.append(text(x + cw - 20, yy + 132, "进入 →", 13, ACC, 600, "end"))
    # 热门资源
    y = 1330
    t, y2 = section_title(y, "02", "热门资源轮播", "启动器 / 整合包 / MOD / 资源包")
    b.append(t)
    cw2 = (CW - 3 * 20) // 4
    data = [("HMCL 启动器", "支持 Win / macOS / Linux", "启动器"), ("Better MC 整合包", "1.20.1 · 120+ MOD", "整合包"),
            ("Create 机械动力", "前置：Flywheel", "MOD"), ("Complementary 光影", "需 Iris / OptiFine", "光影")]
    for i, (tt, mt, tg) in enumerate(data):
        b.append(card(CX + i * (cw2 + 20), y2 + 24, cw2, 330, tt, 2, 150, tg))
    # 社区动态
    y = 1760
    t, y2 = section_title(y, "03", "社区动态", "最新主题 / 服务器 / 视频")
    b.append(t)
    b.append(rect(CX, y2 + 24, 760, 420, "#FFFFFF", LINE, 1, 8))
    b.append(text(CX + 24, y2 + 64, "最新主题", 18, TXT, 700))
    for i in range(6):
        yy = y2 + 92 + i * 52
        b.append(rect(CX + 24, yy, 712, 40, SOFT, None, 0, 4))
        b.append(text(CX + 38, yy + 26, f"[板块] 主题标题占位 —— 回复 {18 + i * 7} · {2 + i} 分钟前", 13, MUT))
    b.append(rect(CX + 780, y2 + 24, 420, 420, "#FFFFFF", LINE, 1, 8))
    b.append(text(CX + 804, y2 + 64, "在线服务器", 18, TXT, 700))
    for i in range(4):
        yy = y2 + 88 + i * 78
        b.append(rect(CX + 804, yy, 372, 62, SOFT, None, 0, 6))
        b.append(text(CX + 820, yy + 26, f"服务器名称占位 {i+1}", 14, TXT, 600))
        b.append(text(CX + 820, yy + 48, "1.20.1 · 原版生存 · 在线 86/200", 12, MUT))
    # 底部 CTA
    b.append(rect(0, 2260, W, 220, SOFT))
    b.append(text(W/2, 2330, "第一次进入 MC？先看 30 分钟新手路线", 30, TXT, 700, "middle"))
    b.append(text(W/2, 2364, "认识 MC → 版本与玩法 → 新手教程 → 启动器下载", 15, MUT, 400, "middle"))
    b.append(btn(W/2 - 100, 2388, 200, 48, "开始新手路径"))
    b.append(footer(2480))
    add("P00", "首页", "L1", W, H, "".join(b), "品牌区 / 六入口 / 热门资源轮播 / 社区动态 / 新手路径")

# ===== 频道页模板 =====
def channel_page(code, name, active, lead, entries, extra=""):
    h0 = 980
    b = [header(active), breadcrumb(["首页", name], HEADER_H), page_tag(code, name, "L2")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 300, SOFT))
    b.append(text(CX, y + 96, name, 44, TXT, 800))
    b.append(text(CX, y + 140, lead, 17, MUT))
    b.append(text(CX, y + 214, "频道导语 + 栏目入口：本页所有卡片均为二级栏目，点击进入 L3", 13, MUT))
    y2 = y + 300
    t, y3 = section_title(y2 + 60, "01", "栏目入口", f"{len(entries)} 个二级栏目")
    b.append(t)
    cols = 2
    gap = 24
    cw = (CW - gap) // cols
    for i, (nm, url, desc_, tag_s) in enumerate(entries):
        r, c = divmod(i, cols)
        x = CX + c * (cw + gap)
        yy = y3 + 20 + r * 190
        b.append(rect(x, yy, cw, 170, "#FFFFFF", LINE, 1, 8))
        b.append(rect(x + 20, yy + 20, 56, 56, SOFT2, LINE, 1, 6))
        b.append(text(x + 92, yy + 46, nm, 21, TXT, 700))
        b.append(text(x + 92, yy + 74, url, 12, MUT, 400, family=MONO))
        b.append(text(x + 20, yy + 116, desc_, 14, MUT))
        if tag_s:
            tg, _ = tag(x + 20, yy + 132, tag_s, ACC, ACC_SOFT)
            b.append(tg)
        b.append(text(x + cw - 20, yy + 148, "进入 →", 13, ACC, 600, "end"))
    yend = y3 + 20 + ((len(entries) + 1) // 2) * 190
    if extra:
        b.append(extra(yend + 40))
        yend += 300
    b.append(footer(yend + 120))
    H = yend + 420
    add(code, name, "L2", W, H, "".join(b), lead)

# ===== 列表页模板 =====
def list_page(code, name, active, crumbs, title, desc, cols=3, rows=2, with_filter=True, right_panel=False):
    b = [header(active), breadcrumb(crumbs, HEADER_H), page_tag(code, name, "L3")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 240, SOFT))
    b.append(text(CX, y + 80, title, 40, TXT, 800))
    b.append(text(CX, y + 120, desc, 16, MUT))
    b.append(text(CX, y + 186, "列表 → 详情单向下钻；面包屑保持上下文（R3）", 13, MUT))
    y += 240
    if with_filter:
        b.append(filter_bar(y + 32, [("分类", ["全部", "官方", "HMCL", "PCL2"]),
                                     ("版本", ["全部", "1.20", "1.19", "1.18"]),
                                     ("排序", ["热度", "最新", "评分"])]))
        y += 120
    t, y2 = section_title(y + 24, "01", "内容列表", f"{cols * rows} 条 / 页")
    b.append(t)
    gap = 20
    cw = (CW - gap * (cols - 1)) // cols
    for i in range(cols * rows):
        r, c = divmod(i, cols)
        x = CX + c * (cw + gap)
        yy = y2 + 24 + r * 360
        b.append(card(x, yy, cw, 340, f"资源标题占位 {i+1}", 2, 160, "标签"))
    yend = y2 + 24 + rows * 360
    b.append(pagination(yend + 20))
    b.append(footer(yend + 120))
    add(code, name, "L3", W, yend + 420, "".join(b), desc)

# ===== 详情页模板 =====
def detail_page(code, name, active, crumbs, title, meta, modules, recommend, side=None):
    side = side or {}
    side_title = side.get("title", "下载 / 操作")
    side_btns = side.get("btns", [("立即下载", "primary"), ("查看安装说明", "ghost")])
    side_rows = side.get("rows", [("版本", "1.20.1"), ("兼容", "Win / macOS"), ("大小", "268 MB")])
    side_note = side.get("note", "下载页必须出现版本 / 兼容性信息")
    b = [header(active), breadcrumb(crumbs, HEADER_H), page_tag(code, name, "L4")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 120, "#FFFFFF"))
    b.append(text(CX, y + 64, title, 38, TXT, 800))
    b.append(text(CX, y + 96, meta, 14, MUT))
    y += 120
    # 左正文 820 / 右侧栏 340
    LX, LW = CX, 820
    RX, RW = CX + 860, 340
    b.append(img_ph(LX, y + 20, LW, 420, "主图 / 预览 16:9", 8))
    yy = y + 470
    for m in modules:
        b.append(text(LX, yy, m[0], 22, TXT, 700))
        yy += 16
        b.append(line(LX, yy, LX + LW, yy, LINE))
        yy += 26
        if m[1] == "table":
            rows = m[2]
            for j, (k, v) in enumerate(rows):
                b.append(rect(LX, yy + j * 48, LW, 48, "#FFFFFF" if j % 2 == 0 else SOFT))
                b.append(text(LX + 16, yy + j * 48 + 30, k, 14, MUT, 600))
                b.append(text(LX + 220, yy + j * 48 + 30, v, 14, TXT))
            yy += len(rows) * 48 + 20
        elif m[1] == "steps":
            for j, s in enumerate(m[2]):
                b.append(rect(LX, yy + j * 56, 28, 28, ACC_SOFT, ACC, 1, 14))
                b.append(text(LX + 14, yy + j * 56 + 19, str(j + 1), 12, ACC, 700, "middle"))
                b.append(text(LX + 44, yy + j * 56 + 19, s, 15, TXT))
            yy += len(m[2]) * 56 + 16
        else:
            for j in range(3):
                b.append(rect(LX, yy + j * 22, LW - j * 60, 9, SOFT2, None, 0, 4))
            yy += 90
    # 右侧栏
    b.append(rect(RX, y + 20, RW, 320, "#FFFFFF", LINE, 1, 8))
    b.append(text(RX + 20, y + 60, side_title, 18, TXT, 700))
    for j, (label, kind) in enumerate(side_btns):
        b.append(btn(RX + 20, y + 84 + j * 58, RW - 40, 48 if kind == "primary" else 44, label, "primary" if kind == "primary" else "ghost"))
    for j, (k, v) in enumerate(side_rows):
        b.append(text(RX + 20, y + 216 + j * 26, k, 13, MUT))
        b.append(text(RX + RW - 20, y + 216 + j * 26, v, 13, TXT, 600, "end"))
    b.append(text(RX + 20, y + 314, side_note, 11, ACC))
    # 相关推荐
    yy = max(yy, y + 760) + 40
    t, y2 = section_title(yy, "02", "相关推荐", "跨频道打通：下载 / 攻略 / 社区（R4）")
    b.append(t)
    gap = 20
    cw = (CW - 3 * gap) // 4
    for i, r in enumerate(recommend[:4]):
        b.append(card(CX + i * (cw + gap), y2 + 24, cw, 300, r, 1, 140, "相关"))
    yend = y2 + 24 + 300
    b.append(footer(yend + 80))
    add(code, name, "L4", W, yend + 380, "".join(b), meta)

# ===== 生成各页 =====
p_home()

channel_page("P01", "认识 MC", "认识 MC",
             "从「这是什么」到「怎么开始」：简介、版本与玩法、新手教程、常见问题四条主线。",
             [("游戏简介", "guide-intro.html", "是什么 / 玩法概览 / 图集", "新手主路径"),
              ("版本与玩法", "guide-versions.html", "Java / 基岩 / 快照版本对照", "含版本详情"),
              ("新手入门教程", "guide-tutorial.html", "教程目录 / 难度分级", "新手主路径"),
              ("常见问题", "guide-faq.html", "分类 FAQ / 关键词检索", "含问题详情")])

channel_page("P02", "下载中心", "下载中心",
             "核心转化页：启动器、整合包、MOD、资源包与光影、联机与语音工具。",
             [("启动器下载", "launcher.html", "官方 / HMCL / PCL2 横向对比", "核心转化页"),
              ("整合包获取", "modpack.html", "分类 + 热度 + 版本筛选", "强关联"),
              ("MOD 下载", "mod.html", "分类 / 版本筛选 / 前置提示", "前置依赖"),
              ("资源包与光影", "resource.html", "资源包 / 光影分区", ""),
              ("联机与语音工具", "net-tools.html", "联机工具 / 语音工具分组 + 对比", "联机场景")])

channel_page("P03", "社区交流", "社区交流",
             "热门帖、公告、在线人数；论坛、服务器、个人中心三个入口。",
             [("论坛板块", "forum.html", "分区列表 / 最新主题", "5 层最深处"),
              ("服务器与联机", "servers.html", "服务器列表 / 版本筛选", "含详情"),
              ("个人中心", "profile.html", "资料 / 我的帖子 / 收藏入口", "需登录")])

channel_page("P04", "攻略视频", "攻略视频",
             "视频与图文双入口：合集、UP 主、难度分区，看完即可跳转资源。",
             [("视频攻略", "video-guide.html", "合集 / UP 主 / 难度分区", "含播放页"),
              ("图文攻略", "article.html", "分类文章列表", "含文章详情")])

channel_page("P05", "关于与支持", "关于与支持",
             "团队、联系与反馈、更新日志、用户协议与隐私。",
             [("关于我们", "about-us.html", "平台介绍 / 团队", ""),
              ("联系与反馈", "contact.html", "联系方式 / 问题反馈表单", ""),
              ("更新日志", "changelog.html", "版本更新记录", ""),
              ("用户协议与隐私", "legal.html", "用户协议 / 隐私说明", "")])

# 游戏简介（内容页，L3）
def p_intro():
    b = [header("认识 MC"), breadcrumb(["首页", "认识 MC", "游戏简介"], HEADER_H), page_tag("P0101", "游戏简介", "L3")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 300, SOFT))
    b.append(text(CX, y + 90, "游戏简介", 42, TXT, 800))
    b.append(text(CX, y + 132, "Minecraft 是什么、能玩什么、为什么值得玩。", 17, MUT))
    b.append(text(CX, y + 200, "本页为 L3 内容页模板：导语 + 正文分栏 + 图集 + 出口", 13, MUT))
    y += 300
    LX, LW = CX, 820
    RX, RW = CX + 860, 340
    b.append(text(LX, y + 60, "一、它是什么", 24, TXT, 700))
    for i in range(4):
        b.append(rect(LX, y + 82 + i * 26, LW - i * 50, 9, SOFT2, None, 0, 4))
    b.append(img_ph(LX, y + 200, LW, 360, "游戏图集 16:9", 8))
    b.append(text(LX, y + 620, "二、玩法概览", 24, TXT, 700))
    for i, s in enumerate(["生存：采集、建造、探索、对抗", "创造：无限资源与自由建造", "多人：局域网 / 服务器 / 联机工具", "模组：MOD 与整合包扩展玩法"]):
        b.append(rect(LX, y + 648 + i * 54, LW, 44, SOFT, None, 0, 6))
        b.append(text(LX + 16, y + 676 + i * 54, s, 15, TXT))
    b.append(rect(RX, y + 40, RW, 300, "#FFFFFF", LINE, 1, 8))
    b.append(text(RX + 20, y + 78, "下一步", 18, TXT, 700))
    b.append(btn(RX + 20, y + 100, RW - 40, 44, "查看版本与玩法", "ghost"))
    b.append(btn(RX + 20, y + 154, RW - 40, 44, "新手入门教程", "ghost"))
    b.append(text(RX + 20, y + 232, "本页出口：版本与玩法 / 新手教程", 12, MUT))
    b.append(text(RX + 20, y + 258, "避免死链：至少 1 个主出口 + 返回路径", 12, ACC))
    yend = y + 880
    t, y2 = section_title(yend, "02", "相关推荐", "跨频道")
    b.append(t)
    gap = 20
    cw = (CW - 3 * gap) // 4
    for i in range(4):
        b.append(card(CX + i * (cw + gap), y2 + 24, cw, 300, f"相关内容 {i+1}", 1, 140, "推荐"))
    b.append(footer(y2 + 24 + 300 + 80))
    add("P0101", "游戏简介", "L3", W, y2 + 24 + 300 + 380, "".join(b), "是什么 / 玩法概览 / 图集")

# 版本与玩法（表格页）
def p_versions():
    b = [header("认识 MC"), breadcrumb(["首页", "认识 MC", "版本与玩法"], HEADER_H), page_tag("P0102", "版本与玩法", "L3")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 240, SOFT))
    b.append(text(CX, y + 84, "版本与玩法", 40, TXT, 800))
    b.append(text(CX, y + 124, "Java 版 / 基岩版 / 快照版本对照，选择适合你的版本。", 16, MUT))
    y += 240
    b.append(filter_bar(y + 24, [("版本类型", ["全部", "Java", "基岩", "快照"]), ("排序", ["最新", "稳定"])]))
    y += 100
    # 表格
    tw = CW
    b.append(rect(CX, y + 20, tw, 64, SOFT))
    heads = ["版本", "类型", "发布时间", "核心特性", "适合人群", "操作"]
    xs = [CX + 20, CX + 200, CX + 360, CX + 540, CX + 900, CX + 1100]
    for h, x in zip(heads, xs):
        b.append(text(x, y + 60, h, 14, MUT, 700))
    for i in range(6):
        yy = y + 84 + i * 72
        b.append(rect(CX, yy, tw, 72, "#FFFFFF" if i % 2 == 0 else SOFT))
        b.append(text(xs[0], yy + 44, f"1.20.{5-i}", 15, TXT, 700))
        b.append(text(xs[1], yy + 44, "Java" if i % 2 == 0 else "基岩", 14, MUT))
        b.append(text(xs[2], yy + 44, f"2024-0{6-i}-12", 13, MUT))
        b.append(rect(xs[3], yy + 34, 300, 8, SOFT2, None, 0, 4))
        b.append(text(xs[4], yy + 44, "新玩家" if i % 2 == 0 else "跨平台", 13, MUT))
        b.append(text(xs[5], yy + 44, "版本详情 →", 13, ACC, 600))
    yend = y + 84 + 6 * 72 + 20
    b.append(text(CX, yend + 20, "版本详情页（L4）承接：特性 / 更新内容 / 安装说明 → 启动器下载、整合包详情", 13, MUT))
    b.append(footer(yend + 90))
    add("P0102", "版本与玩法", "L3", W, yend + 390, "".join(b), "Java / 基岩 / 快照版本对照表")

list_page("P0103", "新手入门教程", "认识 MC", ["首页", "认识 MC", "新手入门教程"],
          "新手入门教程", "从第一夜到第一次联机：按难度分级的图文教程目录。", cols=3, rows=2, with_filter=False)

list_page("P0201", "启动器下载", "下载中心", ["首页", "下载中心", "启动器下载"],
          "启动器下载", "官方 / HMCL / PCL2 横向对比：支持平台、配置要求、下载入口。", cols=3, rows=2)

list_page("P0202", "整合包获取", "下载中心", ["首页", "下载中心", "整合包获取"],
          "整合包获取", "按分类、热度、版本筛选整合包；详情页给出 MOD 清单与安装步骤。", cols=3, rows=2)

detail_page("P020201", "整合包详情", "下载中心",
            ["首页", "下载中心", "整合包获取", "整合包详情"],
            "Better MC [FORGE] 整合包",
            "整合包 · 1.20.1 · 120+ MOD · 更新于 2024-06-12",
            [("整合包说明", "paras", None),
             ("MOD 清单", "table", [("Create 机械动力", "1.20.1-0.5.1"), ("Farmer's Delight", "1.20.1-1.2.3"), ("JourneyMap", "1.20.1-5.9.7"), ("JEI", "1.20.1-15.2.0")]),
             ("安装步骤", "steps", ["下载并安装启动器（HMCL / PCL2）", "在启动器中导入整合包压缩包", "选择对应 Java 版本并分配内存", "启动游戏，首次加载约 3–5 分钟"])],
            ["配套视频攻略", "启动器下载", "前置 MOD 说明", "同类整合包"])

channel_page("P03b", "社区交流（含热帖）", "社区交流",
             "热门帖、公告、在线人数；论坛、服务器、个人中心三个入口。",
             [("论坛板块", "forum.html", "分区列表 / 最新主题", "5 层最深处"),
              ("服务器与联机", "servers.html", "服务器列表 / 版本筛选", "含详情"),
              ("个人中心", "profile.html", "资料 / 我的帖子 / 收藏入口", "需登录")])
pages.pop()  # 去掉重复的 P03b（仅保留一个社区页）
os.remove(os.path.join(SVG_DIR, "P03b_社区交流（含热帖）.svg"))

# 论坛板块（分区列表）
def p_forum():
    b = [header("社区交流"), breadcrumb(["首页", "社区交流", "论坛板块"], HEADER_H), page_tag("P0301", "论坛板块", "L3")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 220, SOFT))
    b.append(text(CX, y + 80, "论坛板块", 40, TXT, 800))
    b.append(text(CX, y + 120, "分区 + 最新主题；每个板块进入帖子列表。", 16, MUT))
    y += 220
    b.append(rect(CX, y + 24, CW, 64, "#FFFFFF", LINE, 1, 6))
    b.append(text(CX + 20, y + 62, "全部分区", 15, TXT, 700))
    b.append(text(CX + 200, y + 62, "主题 2,318   ·   帖 24,760   ·   今日 236", 13, MUT))
    b.append(btn(CX + CW - 140, y + 36, 120, 40, "发帖"))
    y += 104
    for i in range(5):
        yy = y + i * 128
        b.append(rect(CX, yy, CW, 112, "#FFFFFF", LINE, 1, 8))
        b.append(rect(CX + 20, yy + 24, 64, 64, SOFT2, LINE, 1, 8))
        b.append(text(CX + 104, yy + 44, f"板块名称占位 {i+1}", 19, TXT, 700))
        b.append(text(CX + 104, yy + 72, "板块简介：讨论版本、整合包、建筑、红石等技术话题。", 13, MUT))
        b.append(text(CX + 104, yy + 96, "主题 126 · 帖 1,860 · 最后回复 3 分钟前", 12, "#A0A0A8"))
        b.append(text(CX + CW - 24, yy + 62, "进入 →", 14, ACC, 600, "end"))
    yend = y + 5 * 128
    b.append(footer(yend + 20))
    add("P0301", "论坛板块", "L3", W, yend + 320, "".join(b), "分区列表 / 最新主题 / 发帖入口")

# 板块帖子列表
def p_board():
    b = [header("社区交流"), breadcrumb(["首页", "社区交流", "论坛板块", "板块帖子列表"], HEADER_H), page_tag("P030101", "板块帖子列表", "L4")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 200, SOFT))
    b.append(text(CX, y + 76, "综合讨论区", 38, TXT, 800))
    b.append(text(CX, y + 116, "置顶 4 · 主题 1,286 · 今日 42", 15, MUT))
    y += 200
    b.append(rect(CX, y + 24, CW, 56, SOFT, LINE, 1, 6))
    b.append(text(CX + 20, y + 58, "置顶", 13, ACC, 700))
    b.append(text(CX + 90, y + 58, "排序：最新回复 ∨     筛选：全部 ∨", 13, MUT))
    b.append(btn(CX + CW - 140, y + 32, 120, 40, "发帖"))
    y += 104
    b.append(text(CX, y + 24, "置顶主题", 16, TXT, 700))
    for i in range(2):
        b.append(list_row(CX, y + 40 + i * 76, CW, 64, f"【置顶】板块规则与发帖指南 {i+1}", "版主 · 置顶 · 12,860 浏览 · 236 回复"))
    y = y + 40 + 2 * 76 + 24
    b.append(text(CX, y, "全部主题", 16, TXT, 700))
    for i in range(6):
        b.append(list_row(CX, y + 16 + i * 76, CW, 64, f"主题标题占位：求助 / 分享 / 教程 {i+1}", f"作者 · {i+2} 分钟前 · 回复 {18+i*3} · 查看 {420+i*37}"))
    yend = y + 16 + 6 * 76
    b.append(pagination(yend + 16))
    b.append(footer(yend + 100))
    add("P030101", "板块帖子列表", "L4", W, yend + 400, "".join(b), "置顶 / 排序 / 发帖入口 → 帖子详情")

# 帖子详情（L5）
def p_post():
    b = [header("社区交流"), breadcrumb(["首页", "社区交流", "论坛板块", "板块帖子列表", "帖子详情"], HEADER_H), page_tag("P03010101", "帖子详情", "L5")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 200, SOFT))
    b.append(text(CX, y + 70, "求助：1.20.1 整合包启动崩溃，日志如下", 34, TXT, 800))
    b.append(text(CX, y + 112, "楼主 · 2024-06-12 20:14 · 综合讨论区 · 128 浏览", 13, MUT))
    b.append(text(CX + CW, y + 112, "5 层最深处：首页 → 频道 → 栏目 → 列表 → 帖子", 12, MUT, 400, "end"))
    y += 200
    # 楼层
    for i in range(3):
        yy = y + 24 + i * 260
        b.append(rect(CX, yy, CW, 240, "#FFFFFF", LINE, 1, 8))
        b.append(rect(CX + 20, yy + 20, 44, 44, SOFT2, None, 0, 22))
        b.append(text(CX + 84, yy + 40, f"楼层作者 {i+1}", 15, TXT, 700))
        b.append(text(CX + 84, yy + 62, f"{i+1} 楼 · 2024-06-12 20:{14+i*6}", 12, MUT))
        for j in range(3):
            b.append(rect(CX + 20, yy + 92 + j * 26, CW - 40 - j * 80, 9, SOFT2, None, 0, 4))
        if i == 0:
            b.append(rect(CX + 20, yy + 172, CW - 40, 40, SOFT, LINE, 1, 4))
            b.append(text(CX + 32, yy + 198, "崩溃日志代码块占位 ……", 12, MUT, family=MONO))
        b.append(text(CX + CW - 24, yy + 224, "点赞 12   ·   回复   ·   举报", 12, MUT, 400, "end"))
    yend = y + 24 + 3 * 260
    b.append(rect(CX, yend, CW, 120, "#FFFFFF", LINE, 1, 8))
    b.append(text(CX + 20, yend + 34, "回复框：支持图文 / 代码块 / 附件", 13, MUT))
    b.append(btn(CX + CW - 120, yend + 60, 100, 40, "发布"))
    b.append(footer(yend + 180))
    add("P03010101", "帖子详情", "L5", W, yend + 480, "".join(b), "楼层 / 图文 / 点赞回复 → 个人中心、相关资源")

# 视频播放页（L4）
def p_watch():
    b = [header("攻略视频"), breadcrumb(["首页", "攻略视频", "视频攻略", "视频播放页"], HEADER_H), page_tag("P040101", "视频播放页", "L4")]
    y = HEADER_H + 48
    b.append(rect(CX, y + 24, 820, 460, "#1F1F23", None, 0, 8))
    b.append(text(CX + 410, y + 254, "▶", 48, "#FFFFFF", 400, "middle"))
    b.append(text(CX + 410, y + 300, "视频播放器占位 16:9", 14, "#B9B9C0", 400, "middle"))
    b.append(text(CX, y + 520, "视频标题：新手 30 分钟入门路线（第 1 集）", 24, TXT, 700))
    b.append(text(CX, y + 552, "UP 主 · 12.8 万播放 · 2024-06-12", 13, MUT))
    for i in range(6):
        b.append(rect(CX, y + 584 + i * 22, 820 - i * 50, 9, SOFT2, None, 0, 4))
    # 右侧推荐
    RX = CX + 860
    b.append(text(RX, y + 40, "相关推荐", 18, TXT, 700))
    for i in range(5):
        yy = y + 60 + i * 96
        b.append(rect(RX, yy, 340, 84, "#FFFFFF", LINE, 1, 6))
        b.append(rect(RX + 10, yy + 10, 110, 64, SOFT2, None, 0, 4))
        b.append(text(RX + 132, yy + 34, f"视频标题 {i+1}", 13, TXT, 600))
        b.append(text(RX + 132, yy + 58, "UP 主 · 播放量", 11, MUT))
    b.append(rect(RX, y + 560, 340, 140, ACC_SOFT, ACC, 1, 8))
    b.append(text(RX + 16, y + 592, "看完 → 拿资源", 15, ACC, 700))
    b.append(text(RX + 16, y + 622, "整合包详情 / 图文攻略", 13, MUT))
    b.append(btn(RX + 16, y + 640, 150, 38, "前往整合包", "ghost", 13))
    yend = y + 700
    t, y2 = section_title(yend, "02", "相关推荐", "视频 → 资源 → 下载")
    b.append(t)
    gap = 20
    cw = (CW - 3 * gap) // 4
    for i in range(4):
        b.append(card(CX + i * (cw + gap), y2 + 24, cw, 300, f"推荐 {i+1}", 1, 140, "推荐"))
    b.append(footer(y2 + 24 + 300 + 80))
    add("P040101", "视频播放页", "L4", W, y2 + 24 + 300 + 380, "".join(b), "播放器 / 分 P / 相关推荐")

# 个人中心
def p_profile():
    b = [header("社区交流"), breadcrumb(["首页", "社区交流", "个人中心"], HEADER_H), page_tag("P0303", "个人中心", "L3")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 260, SOFT))
    b.append(rect(CX, y + 40, 96, 96, SOFT2, LINE, 1, 48))
    b.append(text(CX + 120, y + 76, "用户名占位", 30, TXT, 800))
    b.append(text(CX + 120, y + 110, "Lv.12 · 注册 2023-04 · 发帖 128 · 收藏 46", 14, MUT))
    b.append(btn(CX + CW - 130, y + 60, 110, 40, "编辑资料", "ghost"))
    y += 260
    # 侧边导航
    b.append(rect(CX, y + 24, 260, 360, "#FFFFFF", LINE, 1, 8))
    for i, s in enumerate(["我的帖子", "我的收藏", "我的消息", "账号设置"]):
        yy = y + 24 + i * 64
        if i == 0:
            b.append(rect(CX, yy, 260, 64, ACC_SOFT, None, 0, 0))
            b.append(rect(CX, yy, 4, 64, ACC))
        b.append(text(CX + 24, yy + 40, s, 15, TXT if i == 0 else MUT, 600 if i == 0 else 400))
    # 内容
    LX = CX + 300
    b.append(text(LX, y + 56, "我的帖子", 22, TXT, 700))
    b.append(btn(LX + 560, y + 32, 120, 40, "发帖"))
    for i in range(5):
        b.append(list_row(LX, y + 80 + i * 76, 900, 64, f"我发布的主题 {i+1}", "综合讨论区 · 12 回复 · 3 天前"))
    b.append(footer(y + 520))
    add("P0303", "个人中心", "L3", W, y + 820, "".join(b), "资料 / 我的帖子 / 收藏入口")

# 搜索
def p_search():
    b = [header(), page_tag("G02", "搜索结果", "G")]
    y = HEADER_H
    b.append(rect(0, y, W, 200, SOFT))
    b.append(rect(CX, y + 52, 700, 56, "#FFFFFF", LINE2, 1, 28))
    b.append(text(CX + 24, y + 88, "搜索：整合包 1.20.1", 16, TXT))
    b.append(btn(CX + 716, y + 56, 100, 48, "搜索"))
    b.append(text(CX, y + 150, "结果约 236 条 · 用时 0.12 秒", 13, MUT))
    y += 200
    tabs = ["全部", "页面", "MOD", "整合包", "帖子", "视频"]
    x = CX
    for i, t in enumerate(tabs):
        w = len(t) * 16 + 36
        if i == 0:
            b.append(rect(x, y + 20, w, 36, ACC_SOFT, ACC, 1, 4))
            b.append(text(x + w/2, y + 44, t, 14, ACC, 700, "middle"))
        else:
            b.append(text(x + w/2, y + 44, t, 14, MUT, 400, "middle"))
        x += w + 8
    y += 80
    for i in range(5):
        yy = y + i * 128
        b.append(rect(CX, yy, CW, 112, "#FFFFFF", LINE, 1, 6))
        b.append(text(CX + 20, yy + 32, f"[类型] 结果标题占位 {i+1}", 17, TXT, 700))
        b.append(text(CX + 20, yy + 58, "摘要文字占位：说明该结果与关键词的匹配片段……", 13, MUT))
        b.append(text(CX + 20, yy + 88, "modpack-detail.html?id=1024", 11, "#A0A0A8", family=MONO))
        b.append(text(CX + CW - 20, yy + 58, "进入 →", 13, ACC, 600, "end"))
    b.append(pagination(y + 5 * 128 + 20))
    b.append(footer(y + 5 * 128 + 100))
    add("G02", "搜索结果", "G", W, y + 5 * 128 + 400, "".join(b), "页面 / MOD / 整合包 / 帖子 / 视频分组结果")

# 登录
def p_login():
    b = [header(), page_tag("G01", "登录 / 注册", "G")]
    b.append(rect(0, HEADER_H, W, 900, SOFT))
    b.append(rect(W/2 - 260, HEADER_H + 110, 520, 560, "#FFFFFF", LINE, 1, 10))
    b.append(text(W/2, HEADER_H + 180, "登录 MC HUB", 28, TXT, 800, "middle"))
    b.append(text(W/2, HEADER_H + 212, "登录后可发帖、收藏、加入服务器", 14, MUT, 400, "middle"))
    b.append(rect(W/2 - 200, HEADER_H + 250, 400, 52, SOFT, LINE, 1, 6))
    b.append(text(W/2 - 184, HEADER_H + 282, "邮箱 / 手机号", 14, MUT))
    b.append(rect(W/2 - 200, HEADER_H + 318, 400, 52, SOFT, LINE, 1, 6))
    b.append(text(W/2 - 184, HEADER_H + 350, "密码", 14, MUT))
    b.append(rect(W/2 - 200, HEADER_H + 392, 400, 52, ACC, None, 0, 6))
    b.append(text(W/2, HEADER_H + 424, "登录", 16, "#FFFFFF", 700, "middle"))
    b.append(text(W/2 - 200, HEADER_H + 484, "忘记密码", 13, MUT))
    b.append(text(W/2 + 200, HEADER_H + 484, "注册新账号 →", 13, ACC, 600, "end"))
    b.append(text(W/2, HEADER_H + 620, "第三方登录：微信 / QQ / GitHub（占位）", 12, MUT, 400, "middle"))
    b.append(footer(HEADER_H + 960))
    add("G01", "登录/注册", "G", W, HEADER_H + 1260, "".join(b), "登录 / 注册 / 找回密码")

# 404
def p_404():
    b = [header(), page_tag("G03", "404 / 空状态", "G")]
    b.append(rect(0, HEADER_H, W, 760, SOFT))
    b.append(text(W/2, HEADER_H + 280, "404", 120, LINE2, 800, "middle", family=MONO))
    b.append(text(W/2, HEADER_H + 360, "这个区块还没有被探索过", 30, TXT, 700, "middle"))
    b.append(text(W/2, HEADER_H + 400, "页面可能已移动或删除；试试搜索，或回到首页重新开始。", 15, MUT, 400, "middle"))
    b.append(rect(W/2 - 260, HEADER_H + 450, 420, 52, "#FFFFFF", LINE2, 1, 26))
    b.append(text(W/2 - 240, HEADER_H + 482, "搜索关键词…", 14, MUT))
    b.append(btn(W/2 + 180, HEADER_H + 450, 90, 52, "搜索"))
    b.append(btn(W/2 - 100, HEADER_H + 540, 200, 48, "回到首页", "ghost"))
    b.append(footer(HEADER_H + 800))
    add("G03", "404/空状态", "G", W, HEADER_H + 1100, "".join(b), "错误提示 + 搜索建议 → 首页")

p_intro()
p_versions()
p_forum()
p_board()
p_post()
p_watch()
p_profile()
p_search()
p_login()
p_404()

# ===== 补充页（依据 IA V1.0 补全至 41 页） =====

# ---------- P0104 常见问题（L3） ----------
def p_faq():
    b = [header("认识 MC"), breadcrumb(["首页", "认识 MC", "常见问题"], HEADER_H), page_tag("P0104", "常见问题", "L3")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 300, SOFT))
    b.append(text(CX, y + 84, "常见问题", 42, TXT, 800))
    b.append(text(CX, y + 126, "启动失败、联机超时、模组冲突……先在这里找答案。", 17, MUT))
    b.append(rect(CX, y + 168, 620, 56, "#FFFFFF", LINE2, 1, 28))
    b.append(text(CX + 24, y + 203, "搜索问题关键词，如「崩溃」「联机」", 14, MUT))
    b.append(btn(CX + 636, y + 168, 110, 56, "搜索"))
    b.append(text(CX + 780, y + 203, "共 186 个问题 · 已解决 92%", 13, MUT))
    y += 300
    b.append(text(CX, y + 52, "问题分类", 16, TXT, 700))
    x = CX + 120
    for i, c in enumerate(["全部", "启动与安装", "账号与登录", "联机与服务器", "性能与报错", "下载与资源"]):
        w = len(c) * 14 + 30
        if i == 0:
            b.append(rect(x, y + 30, w, 32, ACC_SOFT, ACC, 1, 4))
            b.append(text(x + w / 2, y + 51, c, 13, ACC, 700, "middle"))
        else:
            b.append(rect(x, y + 30, w, 32, "#FFFFFF", LINE, 1, 4))
            b.append(text(x + w / 2, y + 51, c, 13, MUT, 400, "middle"))
        x += w + 10
    y += 96
    LW = 820
    b.append(text(CX, y + 24, "热门问题", 20, TXT, 700))
    b.append(text(CX + LW, y + 24, "按浏览量排序", 12, MUT, 400, "end"))
    qs = [("游戏启动崩溃，日志提示 Java 版本不匹配怎么办？", "启动与安装 · 浏览 12,860"),
          ("HMCL 打开后一直停在「正在检查更新」", "启动与安装 · 浏览 9,420"),
          ("整合包导入后提示缺少前置 MOD，无法启动", "下载与资源 · 浏览 8,760"),
          ("联机提示「连接超时」，但局域网可以进入", "联机与服务器 · 浏览 7,180"),
          ("帧数很低，光影包一开就掉到 20 FPS", "性能与报错 · 浏览 6,540"),
          ("正版账号登录失败 / 一直要求验证邮箱", "账号与登录 · 浏览 5,320"),
          ("资源包放进文件夹后，游戏里看不到", "下载与资源 · 浏览 4,180"),
          ("服务器显示「版本不兼容」，无法加入", "联机与服务器 · 浏览 3,960")]
    for i, (q, m) in enumerate(qs):
        yy = y + 48 + i * 72
        b.append(rect(CX, yy, LW, 60, "#FFFFFF", LINE, 1, 6))
        b.append(text(CX + 20, yy + 27, "Q%d  %s" % (i + 1, q), 14, TXT, 600))
        b.append(text(CX + 20, yy + 47, m + " · 更新 2024-06-12", 11, MUT))
        b.append(text(CX + LW - 20, yy + 38, "查看详情 →", 12, ACC, 600, "end"))
    yend = y + 48 + len(qs) * 72
    # 右侧：仍未解决 / 相关教程
    RX, RW = CX + 860, 340
    b.append(rect(RX, y + 48, RW, 240, ACC_SOFT, ACC, 1, 8))
    b.append(text(RX + 20, y + 84, "仍然没有解决？", 17, TXT, 700))
    b.append(text(RX + 20, y + 114, "把日志和截图发到论坛，或直接联系我们。", 12.5, MUT))
    b.append(btn(RX + 20, y + 134, RW - 40, 44, "联系与反馈"))
    b.append(btn(RX + 20, y + 188, RW - 40, 44, "去论坛发帖求助", "ghost"))
    b.append(text(RX, y + 330, "相关教程", 17, TXT, 700))
    for i, (s, m) in enumerate([("新手上路：第一夜生存", "教程 · 约 30 分钟"),
                                ("Java 版本与内存分配", "教程 · 约 8 分钟"),
                                ("联机工具配置说明", "教程 · 约 12 分钟")]):
        b.append(list_row(RX, y + 350 + i * 84, RW, 72, s, m))
    b.append(footer(yend + 80))
    add("P0104", "常见问题", "L3", W, yend + 380, "".join(b), "分类 FAQ / 关键词检索 → 问题详情、联系与反馈")


# ---------- 关于与支持子页（L3） ----------
def info_page(code, name, crumbs, title, lead, sections, side_title="本页信息", side_items=None):
    b = [header("关于与支持"), breadcrumb(crumbs, HEADER_H), page_tag(code, name, "L3")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 260, SOFT))
    b.append(text(CX, y + 84, title, 40, TXT, 800))
    b.append(text(CX, y + 126, lead, 17, MUT))
    b.append(text(W - CX, y + 214, "关于与支持 · L3 内容页：正文 + 侧栏出口 + 页脚兜底", 12, MUT, 400, "end"))
    y += 260
    LX, LW = CX, 820
    RX, RW = CX + 860, 340
    yy = y + 40
    for head, lines in sections:
        b.append(text(LX, yy + 30, head, 22, TXT, 700))
        b.append(line(LX, yy + 46, LX + LW, yy + 46, LINE))
        yy += 74
        for s in lines:
            b.append(text(LX, yy, s, 14, MUT))
            yy += 30
        yy += 26
    b.append(rect(RX, y + 40, RW, 300, "#FFFFFF", LINE, 1, 8))
    b.append(text(RX + 20, y + 78, side_title, 17, TXT, 700))
    for i, (k, v) in enumerate(side_items or []):
        b.append(text(RX + 20, y + 118 + i * 30, k, 13, MUT))
        b.append(text(RX + RW - 20, y + 118 + i * 30, v, 13, TXT, 600, "end"))
    b.append(text(RX + 20, y + 304, "页脚四列兜底，避免死链（R6）", 11, ACC))
    yend = max(yy, y + 380)
    t, y2 = section_title(yend + 10, "02", "相关内容", "关于与支持频道内跳转")
    b.append(t)
    gap = 20
    cw = (CW - 3 * gap) // 4
    for i, s in enumerate(["关于我们", "联系与反馈", "更新日志", "用户协议与隐私"]):
        b.append(card(CX + i * (cw + gap), y2 + 24, cw, 300, s, 1, 140, "频道内"))
    b.append(footer(y2 + 24 + 300 + 80))
    add(code, name, "L3", W, y2 + 24 + 300 + 380, "".join(b), lead)


def p_contact():
    b = [header("关于与支持"), breadcrumb(["首页", "关于与支持", "联系与反馈"], HEADER_H), page_tag("P0502", "联系与反馈", "L3")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 260, SOFT))
    b.append(text(CX, y + 84, "联系与反馈", 40, TXT, 800))
    b.append(text(CX, y + 126, "问题反馈、内容纠错、合作洽谈，都会在 2 个工作日内回复。", 17, MUT))
    y += 260
    LX, LW = CX, 820
    RX, RW = CX + 860, 340
    b.append(text(LX, y + 60, "问题反馈表单", 22, TXT, 700))
    b.append(line(LX, y + 76, LX + LW, y + 76, LINE))
    fields = [("反馈类型", "问题反馈 / 内容纠错 / 合作 / 其他"), ("联系方式", "邮箱或 QQ（便于回复）"),
              ("相关页面", "粘贴出现问题的页面链接"), ("问题描述", "描述现象、复现步骤与期望结果")]
    fy = y + 110
    for i, (k, ph) in enumerate(fields):
        h = 44 if i < 3 else 120
        b.append(text(LX, fy, k, 14, TXT, 600))
        b.append(rect(LX, fy + 12, LW, h, "#FFFFFF", LINE, 1, 6))
        b.append(text(LX + 16, fy + 40, ph, 13, MUT))
        fy += h + 40
    b.append(rect(LX, fy + 6, LW, 96, SOFT, LINE, 1, 6))
    b.append(text(LX + 16, fy + 40, "上传截图 / 日志文件（≤ 10 MB）", 13, MUT))
    b.append(text(LX + 16, fy + 72, "支持 .png / .jpg / .log / .txt", 11, "#A0A0A8"))
    b.append(btn(LX, fy + 130, 200, 48, "提交反馈"))
    b.append(text(LX + 224, fy + 160, "提交即视为同意《用户协议与隐私》", 11, MUT))
    b.append(rect(RX, y + 40, RW, 320, "#FFFFFF", LINE, 1, 8))
    b.append(text(RX + 20, y + 78, "其他联系方式", 17, TXT, 700))
    for i, (k, v) in enumerate([("反馈邮箱", "support@mchub.example"), ("合作邮箱", "bd@mchub.example"),
                                ("QQ 群", "1234 5678"), ("工作时间", "工作日 10:00–19:00")]):
        b.append(text(RX + 20, y + 118 + i * 32, k, 13, MUT))
        b.append(text(RX + RW - 20, y + 118 + i * 32, v, 12, TXT, 600, "end"))
    b.append(text(RX + 20, y + 300, "紧急问题请先查「常见问题」", 11, ACC))
    yend = fy + 210
    b.append(footer(yend + 40))
    add("P0502", "联系与反馈", "L3", W, yend + 340, "".join(b), "联系方式 / 问题反馈表单 → 常见问题、用户协议")


def p_changelog():
    b = [header("关于与支持"), breadcrumb(["首页", "关于与支持", "更新日志"], HEADER_H), page_tag("P0503", "更新日志", "L3")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 260, SOFT))
    b.append(text(CX, y + 84, "更新日志", 40, TXT, 800))
    b.append(text(CX, y + 126, "站点功能、资源库与社区规则的版本记录。", 17, MUT))
    y += 260
    b.append(filter_bar(y + 24, [("范围", ["全部", "站点", "资源库", "社区"]), ("时间", ["近 3 个月", "今年", "全部"])]))
    y += 120
    LX = CX
    b.append(line(LX + 8, y + 30, LX + 8, y + 30 + 5 * 190, LINE))
    for i in range(5):
        yy = y + 30 + i * 190
        b.append(rect(LX, yy - 6, 28, 28, ACC if i == 0 else "#FFFFFF", ACC, 1, 14))
        b.append(text(LX + 132, yy + 4, "v2.%d.0" % (4 - i), 18, TXT, 700, family=MONO))
        b.append(text(LX + 240, yy + 4, "2024-0%d-12" % (6 - i), 13, MUT))
        b.append(text(LX + 132, yy + 34, ["新增：联机与语音工具分组页", "优化：整合包筛选与详情结构", "新增：图文攻略分类与文章详情", "修复：搜索结果的类型标签错误", "上线：信息架构 V1.0 与全站导航"][i], 14, TXT, 600))
        for j in range(2):
            b.append(rect(LX + 132, yy + 54 + j * 22, 820 - j * 120, 9, SOFT2, None, 0, 4))
        b.append(text(LX + 980, yy + 4, "站点", 12, MUT, 600, "end"))
    yend = y + 30 + 5 * 190
    b.append(footer(yend + 40))
    add("P0503", "更新日志", "L3", W, yend + 340, "".join(b), "版本更新记录 → 首页、关于我们")


def p_legal():
    b = [header("关于与支持"), breadcrumb(["首页", "关于与支持", "用户协议与隐私"], HEADER_H), page_tag("P0504", "用户协议与隐私", "L3")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 260, SOFT))
    b.append(text(CX, y + 84, "用户协议与隐私", 40, TXT, 800))
    b.append(text(CX, y + 126, "使用本站前请阅读：账号规则、内容规范与个人信息处理说明。", 17, MUT))
    b.append(text(CX, y + 214, "最近更新：2024-06-12   ·   生效日期：2024-06-20", 12, MUT))
    y += 260
    LX, LW = CX, 820
    RX, RW = CX + 860, 340
    yy = y + 40
    for head, paras in [("一、协议范围", 3), ("二、账号与注册", 4), ("三、内容发布规范", 4), ("四、个人信息与隐私", 5), ("五、免责声明", 3)]:
        b.append(text(LX, yy + 28, head, 22, TXT, 700))
        yy += 56
        for j in range(paras):
            b.append(rect(LX, yy + j * 24, LW - j * 60, 9, SOFT2, None, 0, 4))
        yy += paras * 24 + 30
    b.append(rect(RX, y + 40, RW, 260, "#FFFFFF", LINE, 1, 8))
    b.append(text(RX + 20, y + 78, "本页目录", 17, TXT, 700))
    for i, s in enumerate(["一、协议范围", "二、账号与注册", "三、内容发布规范", "四、个人信息与隐私", "五、免责声明"]):
        b.append(text(RX + 20, y + 116 + i * 28, s, 13, MUT if i else ACC, 600 if i == 0 else 400))
    b.append(text(RX + 20, y + 276, "点击目录锚点跳转（R2）", 11, ACC))
    yend = max(yy, y + 380)
    b.append(footer(yend + 40))
    add("P0504", "用户协议与隐私", "L3", W, yend + 340, "".join(b), "用户协议 / 隐私说明 → 联系与反馈")


# ---------- 下载中心补充（L3） ----------
def p_mod_list():
    b = [header("下载中心"), breadcrumb(["首页", "下载中心", "MOD 下载"], HEADER_H), page_tag("P0203", "MOD 下载", "L3")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 240, SOFT))
    b.append(text(CX, y + 80, "MOD 下载", 40, TXT, 800))
    b.append(text(CX, y + 120, "按分类与版本筛选；涉及前置依赖的 MOD 会明确标注。", 16, MUT))
    b.append(text(CX, y + 186, "下载类页面必须出现「版本 / 兼容性」信息", 13, ACC))
    y += 240
    b.append(filter_bar(y + 32, [("分类", ["全部", "科技", "冒险", "装饰", "优化"]),
                                 ("版本", ["全部", "1.20.1", "1.19.2", "1.18.2"]),
                                 ("前置", ["全部", "无前置", "需 Forge", "需 Fabric"])]))
    y += 120
    t, y2 = section_title(y + 24, "01", "MOD 列表", "6 条 / 页 · 前置依赖单独标注")
    b.append(t)
    gap = 20
    cw = (CW - gap * 2) // 3
    mods = [("Create 机械动力", "前置：Flywheel · Forge"), ("JEI 物品管理器", "无前置 · Forge / Fabric"),
            ("Farmer's Delight", "前置：无 · Forge"), ("JourneyMap 地图", "无前置 · Forge"),
            ("Sophisticated Backpacks", "前置：无 · Forge"), ("Sodium 优化", "无前置 · Fabric")]
    for i, (nm, meta) in enumerate(mods):
        r, c = divmod(i, 3)
        x = CX + c * (cw + gap)
        yy = y2 + 24 + r * 360
        b.append(card(x, yy, cw, 340, nm, 2, 160, "1.20.1"))
        b.append(text(x + 16, yy + 286, meta, 12, MUT))
    yend = y2 + 24 + 2 * 360
    b.append(pagination(yend + 20))
    b.append(footer(yend + 120))
    add("P0203", "MOD 下载", "L3", W, yend + 420, "".join(b), "分类 / 版本筛选 / 前置提示 → MOD 详情")


def p_resource():
    b = [header("下载中心"), breadcrumb(["首页", "下载中心", "资源包与光影"], HEADER_H), page_tag("P0204", "资源包与光影", "L3")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 240, SOFT))
    b.append(text(CX, y + 80, "资源包与光影", 40, TXT, 800))
    b.append(text(CX, y + 120, "先选资源包改画面风格，再加光影提升光照与反射。", 16, MUT))
    b.append(text(CX, y + 186, "光影需要 Iris / OptiFine 支持，注意显卡配置", 13, ACC))
    y += 240
    b.append(filter_bar(y + 24, [("分区", ["全部", "资源包", "光影"]), ("分辨率", ["全部", "16x", "64x", "128x+"]), ("排序", ["热门", "最新"])]))
    y += 116
    gap = 20
    cw = (CW - gap * 2) // 3
    yend = y
    for si, (sec_no, sec_name, desc_, items) in enumerate([
            ("01", "资源包", "改变方块与界面贴图风格，对性能影响较小。",
             [("Faithful 32x", "32x · 原版写实"), ("Bare Bones", "16x · 极简扁平"), ("Stay True", "32x · 温柔原版")]),
            ("02", "光影", "改变光照、水面与反射，需要较好的显卡。",
             [("Complementary", "需 Iris · 中配可跑"), ("BSL Shaders", "需 OptiFine · 中高配"), ("SEUS PTGI", "需光追 · 高配")])]):
        t, y2 = section_title(y + 24, sec_no, sec_name, desc_)
        b.append(t)
        for i, (nm, meta) in enumerate(items):
            b.append(card(CX + i * (cw + gap), y2 + 24, cw, 330, nm, 2, 150, "资源" if si == 0 else "光影"))
            b.append(text(CX + i * (cw + gap) + 16, y2 + 24 + 276, meta, 12, MUT))
        y += 24 + 22 + 24 + 330 + 60
        yend = y
    b.append(pagination(yend - 20))
    b.append(footer(yend + 60))
    add("P0204", "资源包与光影", "L3", W, yend + 360, "".join(b), "资源包 / 光影分区 → 资源详情")


def p_net_tools():
    b = [header("下载中心"), breadcrumb(["首页", "下载中心", "联机与语音工具"], HEADER_H), page_tag("P0205", "联机与语音工具下载", "L3")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 240, SOFT))
    b.append(text(CX, y + 80, "联机与语音工具", 40, TXT, 800))
    b.append(text(CX, y + 120, "联机工具负责「进得去」，语音工具负责「聊得顺」。", 16, MUT))
    b.append(text(CX, y + 186, "联机失败时可从「服务器与联机」回流到本页（跨频道）", 13, ACC))
    y += 240
    gap = 20
    cw = (CW - gap * 2) // 3
    for si, (sec_no, sec_name, desc_, items) in enumerate([
            ("01", "联机工具", "把局域网或远程好友连到同一个世界。",
             [("SakuraFrp 内网穿透", "免费 · 需实名"), ("Radmin VPN", "免费 · Win"), ("HMCL 联机", "内置 · 需启动器")]),
            ("02", "语音工具", "开黑语音，支持房间码 / 频道。",
             [("KOOK", "频道制 · 全平台"), ("Discord", "频道制 · 需加速"), ("QQ 语音", "群语音 · 免安装")])]):
        t, y2 = section_title(y + 24, sec_no, sec_name, desc_)
        b.append(t)
        for i, (nm, meta) in enumerate(items):
            b.append(card(CX + i * (cw + gap), y2 + 24, cw, 330, nm, 2, 150, "联机" if si == 0 else "语音"))
            b.append(text(CX + i * (cw + gap) + 16, y2 + 24 + 276, meta, 12, MUT))
        y += 24 + 22 + 24 + 330 + 50
    # 对比表
    t, y2 = section_title(y + 10, "03", "工具对比", "支持平台 / 房间人数 / 是否需实名")
    b.append(t)
    heads = ["工具", "类型", "支持平台", "房间人数", "实名 / 账号", "操作"]
    xs = [CX + 20, CX + 260, CX + 400, CX + 620, CX + 800, CX + 1080]
    b.append(rect(CX, y2 + 20, CW, 56, SOFT))
    for h, xx in zip(heads, xs):
        b.append(text(xx, y2 + 56, h, 13, MUT, 700))
    rows = [("SakuraFrp", "联机", "Win / Linux", "不限", "需实名"), ("Radmin VPN", "联机", "Win", "≤ 100 人", "需账号"),
            ("KOOK", "语音", "Win / macOS / 移动", "≤ 200 人", "需账号"), ("Discord", "语音", "全平台", "≤ 500 人", "需账号")]
    for i, r in enumerate(rows):
        yy = y2 + 76 + i * 60
        b.append(rect(CX, yy, CW, 60, "#FFFFFF" if i % 2 == 0 else SOFT))
        b.append(text(xs[0], yy + 38, r[0], 14, TXT, 700))
        b.append(text(xs[1], yy + 38, r[1], 13, MUT))
        b.append(text(xs[2], yy + 38, r[2], 13, MUT))
        b.append(text(xs[3], yy + 38, r[3], 13, MUT))
        b.append(text(xs[4], yy + 38, r[4], 13, MUT))
        b.append(text(xs[5], yy + 38, "工具详情 →", 12, ACC, 600))
    yend = y2 + 76 + 4 * 60 + 20
    b.append(footer(yend + 40))
    add("P0205", "联机与语音工具下载", "L3", W, yend + 340, "".join(b), "联机工具 / 语音工具分组 + 平台与人数对比")


# ---------- 社区补充（L3 / L4） ----------
def p_servers():
    b = [header("社区交流"), breadcrumb(["首页", "社区交流", "服务器与联机"], HEADER_H), page_tag("P0302", "服务器与联机", "L3")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 240, SOFT))
    b.append(text(CX, y + 80, "服务器与联机", 40, TXT, 800))
    b.append(text(CX, y + 120, "按版本、玩法、人数筛选服务器，看清规则再加入。", 16, MUT))
    b.append(text(CX, y + 186, "加入前先备好客户端版本与语音工具（R5）", 13, ACC))
    y += 240
    b.append(filter_bar(y + 32, [("版本", ["全部", "1.20.1", "1.19.2", "基岩"]),
                                 ("玩法", ["全部", "原版生存", "模组", "小游戏"]),
                                 ("人数", ["全部", "≤ 50", "50–200", "200+"])]))
    y += 120
    t, y2 = section_title(y + 24, "01", "服务器列表", "按在线人数排序 · 6 条 / 页")
    b.append(t)
    rows = [("方块大陆 · 原版生存", "1.20.1 · 原版生存 · 白名单", "86 / 200"),
            ("机械纪元 · Create 模组服", "1.20.1 · 模组 · 需整合包", "64 / 100"),
            ("像素竞技场 · 小游戏", "1.20.1 · 小游戏 · 免白名单", "128 / 300"),
            ("红石工坊 · 创造建筑", "1.19.2 · 创造 · 需申请", "32 / 80"),
            ("基岩互通服", "基岩 1.20 · 原版生存", "58 / 100"),
            ("空岛生存 · SkyBlock", "1.20.1 · 模组 · 需整合包", "42 / 100")]
    for i, (nm, meta, online) in enumerate(rows):
        yy = y2 + 24 + i * 96
        b.append(rect(CX, yy, CW, 84, "#FFFFFF", LINE, 1, 8))
        b.append(rect(CX + 18, yy + 14, 56, 56, SOFT2, LINE, 1, 6))
        b.append(text(CX + 92, yy + 34, nm, 17, TXT, 700))
        b.append(text(CX + 92, yy + 60, meta, 12.5, MUT))
        b.append(text(CX + CW - 220, yy + 42, "在线 " + online, 13, ACC, 600))
        b.append(text(CX + CW - 24, yy + 42, "查看详情 →", 13, MUT, 600, "end"))
    yend = y2 + 24 + len(rows) * 96
    b.append(pagination(yend + 16))
    b.append(footer(yend + 100))
    add("P0302", "服务器与联机", "L3", W, yend + 400, "".join(b), "服务器列表 / 版本筛选 → 服务器详情")


def p_profile_content():
    b = [header("社区交流"), breadcrumb(["首页", "社区交流", "个人中心", "我的内容"], HEADER_H), page_tag("P030301", "我的内容", "L4")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 180, SOFT))
    b.append(text(CX, y + 76, "我的内容", 36, TXT, 800))
    b.append(text(CX, y + 116, "发帖 / 收藏 / 消息 / 设置，四个分页管理你的社区资产。", 15, MUT))
    y += 180
    tabs = ["我的发帖", "我的收藏", "我的消息", "账号设置"]
    x = CX
    for i, t in enumerate(tabs):
        w = len(t) * 16 + 40
        if i == 0:
            b.append(rect(x, y + 20, w, 40, ACC_SOFT, ACC, 1, 4))
            b.append(text(x + w / 2, y + 46, t, 14, ACC, 700, "middle"))
        else:
            b.append(text(x + w / 2, y + 46, t, 14, MUT, 400, "middle"))
        x += w + 8
    y += 90
    b.append(text(CX, y + 20, "我的发帖（128）", 20, TXT, 700))
    b.append(btn(CX + CW - 120, y + 2, 120, 40, "发帖"))
    for i in range(6):
        b.append(list_row(CX, y + 44 + i * 76, CW, 64, "我发布的主题 %d" % (i + 1),
                          "综合讨论区 · 12 回复 · %d 天前 · 状态：正常" % (i + 1)))
    yend = y + 44 + 6 * 76
    b.append(pagination(yend + 16))
    b.append(footer(yend + 100))
    add("P030301", "我的内容", "L4", W, yend + 400, "".join(b), "发帖 / 收藏 / 消息 / 设置 → 帖子详情、首页")


# ---------- 攻略视频补充（L3 / L4） ----------
def p_articles():
    b = [header("攻略视频"), breadcrumb(["首页", "攻略视频", "图文攻略"], HEADER_H), page_tag("P0402", "图文攻略", "L3")]
    y = HEADER_H + 48
    b.append(rect(0, y, W, 240, SOFT))
    b.append(text(CX, y + 80, "图文攻略", 40, TXT, 800))
    b.append(text(CX, y + 120, "适合边做边看的步骤型内容：红石、建筑、生存技巧。", 16, MUT))
    b.append(text(CX, y + 186, "文章详情与视频攻略互为补充（R4）", 13, ACC))
    y += 240
    b.append(filter_bar(y + 32, [("分类", ["全部", "生存", "红石", "建筑", "模组"]), ("排序", ["最新", "最热", "收藏"])]))
    y += 120
    t, y2 = section_title(y + 24, "01", "文章列表", "左列表 + 右侧热门")
    b.append(t)
    LW = 780
    for i in range(6):
        yy = y2 + 24 + i * 120
        b.append(rect(CX, yy, LW, 108, "#FFFFFF", LINE, 1, 8))
        b.append(rect(CX + 16, yy + 14, 140, 80, SOFT2, LINE, 1, 6))
        b.append(text(CX + 172, yy + 34, "文章标题占位 %d：从零开始的红石基础" % (i + 1), 16, TXT, 700))
        b.append(text(CX + 172, yy + 60, "摘要：用三步搭出可循环的自动农场……", 12.5, MUT))
        b.append(text(CX + 172, yy + 88, "红石 · 12 分钟阅读 · 2024-06-%02d" % (12 - i), 11, MUT))
        b.append(text(CX + LW - 16, yy + 88, "阅读 →", 12, ACC, 600, "end"))
    RX = CX + 820
    b.append(rect(RX, y2 + 24, 380, 320, "#FFFFFF", LINE, 1, 8))
    b.append(text(RX + 20, y2 + 62, "热门文章", 17, TXT, 700))
    for i in range(4):
        b.append(text(RX + 20, y2 + 104 + i * 52, "%d. 热门文章标题占位" % (i + 1), 13, TXT, 600))
        b.append(text(RX + 20, y2 + 124 + i * 52, "阅读 8,6%02d · 收藏 1,2%02d" % (40 - i * 7, 30 - i * 4), 11, MUT))
    b.append(rect(RX, y2 + 370, 380, 180, ACC_SOFT, ACC, 1, 8))
    b.append(text(RX + 20, y2 + 404, "看视频更直观？", 15, TXT, 700))
    b.append(text(RX + 20, y2 + 430, "切换到视频攻略，按合集跟做。", 12, MUT))
    b.append(btn(RX + 20, y2 + 452, 160, 40, "视频攻略", "ghost"))
    yend = y2 + 24 + 6 * 120
    b.append(pagination(yend + 16))
    b.append(footer(yend + 100))
    add("P0402", "图文攻略", "L3", W, yend + 400, "".join(b), "分类文章列表 → 文章详情")


# ---------- 下载详情补充（L4） ----------
def p_launcher_detail():
    detail_page("P020101", "启动器详情", "下载中心",
                ["首页", "下载中心", "启动器下载", "启动器详情"],
                "HMCL 启动器",
                "启动器 · 开源免费 · 支持离线登录 · 更新于 2024-06-12",
                [("支持平台", "table", [("Windows", "Win 7 及以上 · 64 位"), ("macOS", "10.15 及以上"),
                                         ("Linux", "主流发行版 · 需 Java"), ("Android", "HMCL-PE 独立版本")]),
                 ("配置要求", "table", [("Java", "Java 8 / 17 / 21"), ("内存", "建议 4 GB 以上"),
                                        ("磁盘", "≥ 2 GB（含整合包）"), ("显卡", "无特殊要求")]),
                 ("安装步骤", "steps", ["下载对应平台安装包", "安装并选择 Java 路径", "登录账号（正版 / 离线）",
                                        "选择版本并启动游戏"])],
                ["整合包获取", "版本与玩法", "MOD 下载", "启动器横向对比"],
                side={"title": "下载 / 操作", "btns": [("立即下载", "primary"), ("查看安装说明", "ghost")],
                      "rows": [("版本", "3.5.5"), ("平台", "Win / macOS / Linux"), ("大小", "38 MB")],
                      "note": "启动器详情 → 版本详情 / 整合包获取（R5）"})


def p_version_detail():
    detail_page("P010201", "版本详情", "认识 MC",
                ["首页", "认识 MC", "版本与玩法", "版本详情"],
                "Java 版 1.20.1",
                "版本详情 · 正式版 · 发布于 2023-06-12 · 收录 MOD 2,860 个",
                [("版本特性", "paras", None),
                 ("更新内容", "table", [("方块", "新增樱花木系列"), ("生物", "骆驼 / 嗅探兽"),
                                        ("机制", "考古系统与陶片"), ("性能", "区块加载优化")]),
                 ("安装说明", "steps", ["下载对应启动器（HMCL / PCL2）", "在启动器中选择 1.20.1",
                                        "分配 4 GB 以上内存", "首次启动自动补全运行库"])],
                ["启动器下载", "整合包详情", "MOD 下载", "新手入门教程"],
                side={"title": "版本信息", "btns": [("下载该版本", "primary"), ("查看启动器", "ghost")],
                      "rows": [("版本号", "1.20.1"), ("类型", "Java 正式版"), ("发布", "2023-06-12")],
                      "note": "版本详情 → 启动器下载 / 整合包详情（R5）"})


def p_mod_detail():
    detail_page("P020301", "MOD 详情", "下载中心",
                ["首页", "下载中心", "MOD 下载", "MOD 详情"],
                "Create 机械动力",
                "MOD · 1.20.1 · Forge · 前置：Flywheel · 更新于 2024-06-12",
                [("MOD 说明", "paras", None),
                 ("前置依赖", "table", [("Flywheel", "必需 · 0.6.10 及以上"), ("Forge", "必需 · 47.1.0"),
                                        ("JEI", "可选 · 推荐安装"), ("Create Crafts & Additions", "可选 · 联动")]),
                 ("安装方式", "steps", ["先安装 Flywheel 前置 MOD", "把 jar 放入 mods 文件夹",
                                        "在启动器中确认 Forge 版本", "启动游戏并在模组列表核对"])],
                ["整合包详情", "MOD 下载", "视频攻略", "相关资源包"],
                side={"title": "下载 / 依赖", "btns": [("下载 MOD", "primary"), ("查看前置 MOD", "ghost")],
                      "rows": [("版本", "1.20.1"), ("加载器", "Forge"), ("大小", "2.4 MB")],
                      "note": "MOD 详情必须列出前置依赖（R5）"})


def p_resource_detail():
    detail_page("P020401", "资源详情", "下载中心",
                ["首页", "下载中心", "资源包与光影", "资源详情"],
                "Complementary Shaders",
                "光影 · 需 Iris / OptiFine · 中配可跑 · 更新于 2024-06-12",
                [("资源说明", "paras", None),
                 ("配置要求", "table", [("显卡", "GTX 1060 及以上"), ("显存", "≥ 4 GB"),
                                        ("加载器", "Iris / OptiFine"), ("建议", "关闭体积云以提升帧数")]),
                 ("使用步骤", "steps", ["安装 Iris 或 OptiFine", "把压缩包放入 shaderpacks 文件夹",
                                        "在视频设置中启用光影", "按配置调整阴影与水面质量"])],
                ["资源包与光影", "整合包详情", "版本与玩法", "视频攻略"],
                side={"title": "下载 / 操作", "btns": [("下载资源", "primary"), ("查看安装说明", "ghost")],
                      "rows": [("分辨率", "—"), ("兼容", "1.20.1 / 1.19.2"), ("大小", "12 MB")],
                      "note": "资源详情 → 整合包详情（R4）"})


def p_tool_detail():
    detail_page("P020501", "工具详情", "下载中心",
                ["首页", "下载中心", "联机与语音工具", "工具详情"],
                "KOOK 语音",
                "语音工具 · 频道制 · 全平台 · 免费",
                [("功能说明", "paras", None),
                 ("支持平台", "table", [("Windows", "桌面客户端"), ("macOS", "桌面客户端"),
                                        ("Android / iOS", "移动端"), ("网页", "免安装")]),
                 ("房间码与语音频道设置", "steps", ["创建服务器并生成邀请码", "把邀请码发给联机好友",
                                              "为不同小队建立独立语音频道", "设置按键说话与降噪"])],
                ["服务器与联机", "联机工具下载", "整合包详情", "常见问题"],
                side={"title": "下载 / 操作", "btns": [("下载客户端", "primary"), ("查看使用说明", "ghost")],
                      "rows": [("平台", "全平台"), ("人数", "≤ 200 人"), ("大小", "86 MB")],
                      "note": "工具详情 → 服务器详情 / 整合包详情（R5）"})


def p_server_detail():
    detail_page("P030201", "服务器详情", "社区交流",
                ["首页", "社区交流", "服务器与联机", "服务器详情"],
                "方块大陆 · 原版生存",
                "服务器 · 1.20.1 · 原版生存 · 在线 86 / 200 · 延迟 32 ms",
                [("服务器规则", "paras", None),
                 ("版本与玩法", "table", [("版本", "Java 1.20.1"), ("模式", "原版生存 · 白名单"),
                                          ("周期", "长期不删档"), ("插件", "领地 / 商店 / 反作弊")]),
                 ("加入方式", "steps", ["确认客户端版本为 1.20.1", "准备启动器并登录账号",
                                        "在多人游戏中添加服务器地址", "申请白名单后进入大厅"])],
                ["论坛板块", "启动器下载", "联机与语音工具", "服务器与联机"],
                side={"title": "加入服务器", "btns": [("复制服务器地址", "primary"), ("联机工具下载", "ghost")],
                      "rows": [("版本", "1.20.1"), ("人数", "86 / 200"), ("延迟", "32 ms")],
                      "note": "加入前先备好客户端与语音工具（R5）"})


def p_article_detail():
    detail_page("P040201", "文章详情", "攻略视频",
                ["首页", "攻略视频", "图文攻略", "文章详情"],
                "从零开始的红石基础：三步搭出自动农场",
                "图文攻略 · 红石 · 12 分钟阅读 · 更新于 2024-06-12",
                [("正文", "paras", None),
                 ("本章目录", "table", [("一、红石元件", "中继器 / 比较器 / 红石火把"), ("二、时钟电路", "循环与延时"),
                                        ("三、自动农场", "收割与收集"), ("四、常见问题", "不工作怎么排查")]),
                 ("步骤", "steps", ["准备红石粉、中继器与活塞", "搭出 4 刻时钟电路",
                                    "连接观察者与收割活塞", "接入漏斗与箱子收集"])],
                ["视频攻略", "教程详情", "整合包详情", "常见问题"],
                side={"title": "文章信息", "btns": [("收藏文章", "primary"), ("分享链接", "ghost")],
                      "rows": [("分类", "红石"), ("阅读", "12 分钟"), ("更新", "2024-06-12")],
                      "note": "文章详情 ↔ 视频攻略 / 教程详情（R4）"})


def p_tutorial_detail():
    detail_page("P010301", "教程详情", "认识 MC",
                ["首页", "认识 MC", "新手入门教程", "教程详情"],
                "第一夜生存：从砍树到床",
                "教程详情 · 入门 · 约 30 分钟 · 适用于 1.20.1",
                [("你将学会", "paras", None),
                 ("准备工作", "table", [("游戏版本", "Java 1.20.1"), ("难度", "普通 / 和平"),
                                        ("种子", "任意"), ("所需时间", "约 30 分钟")]),
                 ("步骤", "steps", ["徒手砍树，制作工作台与木镐", "挖石头，升级石质工具", "找羊做床并设置重生点",
                                    "建简易庇护所，度过第一夜"])],
                ["教程详情", "版本详情", "常见问题", "启动器下载"],
                side={"title": "教程信息", "btns": [("收藏教程", "primary"), ("导出 / 打印", "ghost")],
                      "rows": [("难度", "入门"), ("时长", "约 30 分钟"), ("更新", "2024-06-12")],
                      "note": "教程详情出口：常见问题 / 版本与玩法（R4）"})


def p_faq_detail():
    detail_page("P010401", "问题详情", "认识 MC",
                ["首页", "认识 MC", "常见问题", "问题详情"],
                "游戏启动崩溃，日志提示 Java 版本不匹配",
                "常见问题 · 启动与安装 · 浏览 12,860 · 解决率 86%",
                [("问题现象", "paras", None),
                 ("可能原因", "table", [("Java 版本", "游戏所需 17，实际为 8"), ("内存分配", "过低导致加载失败"),
                                        ("启动器配置", "未指定正确的 Java 路径"), ("模组冲突", "前置缺失")]),
                 ("解决步骤", "steps", ["在启动器中查看当前 Java 路径", "安装 Java 17 并重新指定路径",
                                        "把内存调整为 4 GB 以上", "逐个禁用模组定位冲突"])],
                ["教程详情", "版本详情", "联系与反馈", "常见问题"],
                side={"title": "问题信息", "btns": [("问题已解决", "primary"), ("联系与反馈", "ghost")],
                      "rows": [("分类", "启动与安装"), ("提问", "128"), ("解决率", "86%")],
                      "note": "仍未解决 → 联系与反馈 / 论坛发帖（R4）"})


# 注册补充页
p_faq()
info_page("P0501", "关于我们", ["首页", "关于与支持", "关于我们"],
          "关于我们", "MC HUB 是谁做的、为什么做，以及我们坚持的三件事。",
          [("平台定位", ["把「认识 → 获取 → 交流 → 学习」四件事收进一个站点。",
                         "不做资源搬运的堆砌，而是让每个入口都有明确的下一步。"]),
           ("团队与协作", ["内容组：维护版本、教程与常见问题。",
                           "资源组：审核启动器、整合包与 MOD 的可用性与安全性。",
                           "社区组：运营论坛、服务器与视频攻略。"]),
           ("内容原则", ["所有下载页标注版本与兼容性。",
                         "所有详情页保留面包屑与相关推荐。",
                         "所有纠错都有反馈入口，2 个工作日内回复。"])],
          side_title="平台信息", side_items=[("上线时间", "2024-06"), ("页面总量", "41"), ("信息架构", "IA V1.0"), ("联系邮箱", "hi@mchub.example")])
p_contact()
p_changelog()
p_legal()

p_mod_list()
p_resource()
p_net_tools()
p_servers()
p_profile_content()
list_page("P0401", "视频攻略", "攻略视频", ["首页", "攻略视频", "视频攻略"],
          "视频攻略", "合集 / UP 主 / 难度分区：按顺序跟做，看完即可跳转资源。", cols=3, rows=2)
p_articles()
p_launcher_detail()
p_version_detail()
p_mod_detail()
p_resource_detail()
p_tool_detail()
p_server_detail()
p_article_detail()
p_tutorial_detail()
p_faq_detail()

# ---------- 索引页 ----------
rows = []
for code, name, level, fn, w, h, desc in sorted(pages, key=lambda p: (0 if p[0].startswith("P") else 1, p[0])):
    rows.append(f'''<article class="card">
      <div class="meta"><span class="code">{esc(code)}</span><span class="lv">{esc(level)}</span>
      <span class="dim">{w}×{h}</span></div>
      <h3>{esc(name)}</h3>
      <p>{esc(desc)}</p>
      <a href="svg/{esc(fn)}" target="_blank"><img src="svg/{esc(fn)}" alt="{esc(name)}" loading="lazy"></a>
    </article>''')

index = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MC 社区平台 · Web 低保真原型</title>
<style>
:root{{--bg:#f3f4f6;--card:#fff;--line:#e2e4e8;--txt:#23262b;--mut:#7b818a;--acc:#6ea832;}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--txt);font-family:"Microsoft YaHei",system-ui,sans-serif}}
header.top{{position:sticky;top:0;z-index:9;background:rgba(255,255,255,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:18px 32px}}
h1{{margin:0;font-size:20px;letter-spacing:.3px}}
.top p{{margin:6px 0 0;font-size:13px;color:var(--mut)}}
.wrap{{max-width:1560px;margin:0 auto;padding:28px 32px 80px;display:grid;grid-template-columns:repeat(auto-fill,minmax(460px,1fr));gap:24px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 16px 14px;display:flex;flex-direction:column}}
.meta{{display:flex;align-items:center;gap:8px;font-size:11px;color:var(--mut)}}
.code{{font-family:Consolas,monospace;background:#eef5e6;color:#4d7a22;border:1px solid #d7e7c5;border-radius:3px;padding:1px 6px}}
.lv{{font-family:Consolas,monospace;border:1px solid var(--line);border-radius:3px;padding:1px 6px}}
.dim{{margin-left:auto}}
h3{{margin:10px 0 4px;font-size:16px}}
.card p{{margin:0 0 12px;font-size:12.5px;color:var(--mut);min-height:32px}}
.card img{{width:100%;border:1px solid var(--line);border-radius:6px;display:block;background:#fff}}
</style></head>
<body>
<header class="top">
  <h1>MC 应用与社区交流平台 · Web 低保真原型</h1>
  <p>依据《MC社区平台-信息架构图 V1.0》 · 画布 1920 · 安全宽 1200 · 12 列栅格 · 共 {len(pages)} 个页面模板 · L1–L5 与全局工具全覆盖</p>
</header>
<main class="wrap">
{''.join(rows)}
</main></body></html>'''
with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(index)

print("pages:", len(pages))
for p in pages:
    print(p[0], p[1], p[4], "x", p[5])
