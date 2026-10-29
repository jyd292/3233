# -*- coding: utf-8 -*-
"""MC HUB 高保真页面 · 首页打样"""
from ds import *


def page_home():
    H = 2760
    p = [page_strip("P00", "首页", "L1", "INDEX / BRAND · ENTRY · CURATION")]
    p.append(topbar(None, 30))
    # ---------- HERO ----------
    hy, hh = 118, 600
    p.append(r(0, hy, W, hh, INK))
    # 像素网格底纹
    for i in range(1, 40):
        p.append(r(i * 48, hy, 1, hh, "#16231A"))
    for j in range(1, 12):
        p.append(r(0, hy + j * 52, W, 1, "#16231A"))
    # 左侧文案
    lx = CX
    p.append(r(lx, hy + 92, 10, 10, GRASS_L))
    p.append(t(lx + 20, hy + 102, "MINECRAFT", 12, "#A9BE9A", 700, family=MONO, ls=2))
    p.append(t(lx + 20 + 92, hy + 102, "· 应用与社区交流平台", 12, "#A9BE9A", 600))
    p.append(t(lx, hy + 190, "从第一夜，", 56, "#F4F8EC", 800, ls=1))
    p.append(t(lx, hy + 258, "到属于你的服务器。", 56, "#F4F8EC", 800, ls=1))
    p.append(t(lx, hy + 314, "版本、启动器、整合包、MOD 与光影，一次找齐；", 16, "#A9B9A2"))
    p.append(t(lx, hy + 344, "论坛、联机、视频攻略与图文教程，一路陪你从萌新到老玩家。", 16, "#A9B9A2"))
    # 按钮
    p.append(btn(lx, hy + 392, 210, 54, "开始新手路线", "primary", 16, True))
    p.append(btn(lx + 230, hy + 392, 200, 54, "进入下载中心", "outline_dark" if False else "dark", 16))
    # 数据
    stats = [("1,860", "资源收录"), ("12,480", "当前在线"), ("2,318", "论坛主题"), ("41", "页面模板")]
    sx = lx
    for i, (n, l) in enumerate(stats):
        p.append(stat(sx, hy + 536, n, l, "#F4F8EC", 30))
        p.append(t(sx + 22, hy + 536, "", 1, "#F4F8EC"))
        sx += 150
    # 右侧方块场景
    ax, ay, aw, ah = 1040, hy + 66, 640, 440
    p.append(r(ax - 10, ay - 10, aw + 20, ah + 20, "#0A100B", "#26332A", 2))
    p.append(voxel(ax, ay, aw, ah, "village", 3))
    p.append(r(ax, ay + ah - 4, aw, 4, GRASS))
    p.append(t(ax, ay + ah + 34, "FIG.01", 10, "#7C8B77", 400, family=MONO, ls=1))
    p.append(t(ax + 52, ay + ah + 34, "— 主世界 / 生存模式", 10, "#7C8B77", 400))
    p.append(t(ax + aw, ay + ah + 34, "1920 × 1200 SAFE AREA", 10, "#7C8B77", 400, "end", MONO))

    # ---------- 六入口 ----------
    y = 790
    p.append(sec_head(CX, y, "01", "六个入口，三次点击内到达", "ENTRY POINTS", "层级 ≤ 5 · 任意页面 3 次点击可达"))
    entries = [
        ("认识 MC", "guide.html", "游戏简介 / 版本与玩法 / 教程 / FAQ", "book", GRASS),
        ("下载中心", "download.html", "启动器 / 整合包 / MOD / 资源包 / 联机", "download", AMBER),
        ("社区交流", "community.html", "论坛 / 服务器 / 个人中心", "forum", PINK),
        ("攻略视频", "video.html", "视频合集 / 图文攻略", "video", BLUE),
        ("关于与支持", "about.html", "团队 / 反馈 / 协议 / 更新日志", "shield", PURPLE),
        ("全局搜索", "search.html", "页面 / MOD / 整合包 / 帖子 / 视频", "search", MUT),
    ]
    cy = y + 56
    cwid = (CW - 2 * 24) / 3
    entry_targets = {"guide.html": "P01", "download.html": "P02", "community.html": "P03",
                     "video.html": "P04", "about.html": "P05", "search.html": "G02"}
    for i, (nm, url, desc, ic, col) in enumerate(entries):
        row, col_i = divmod(i, 3)
        x = CX + col_i * (cwid + 24)
        yy = cy + row * 176
        seg = [card_frame(x, yy, cwid, 160, CARD, LINE)]
        seg.append(r(x + 20, yy + 22, 46, 46, PAPER2))
        seg.append(icon(x + 33, yy + 35, ic, col, 20))
        seg.append(t(x + 82, yy + 48, nm, 20, INK, 800))
        seg.append(t(x + 82, yy + 70, url, 10, MUT2, 400, family=MONO))
        seg.append(para(x + 20, yy + 106, desc, 12, MUT, 20, cwid - 40))
        seg.append(icon(x + cwid - 30, yy + 120, "arrow", GRASS, 14))
        seg.append(r(x, yy, 46, 3, col))
        p.append(link(entry_targets[url], "".join(seg)))

    # ---------- 热门资源 ----------
    y = 1200
    p.append(sec_head(CX, y, "02", "本周热门资源", "TRENDING DOWNLOADS", "按下载量与评分排序 · 每日更新"))
    items = [("HMCL 启动器", "启动器", "支持 Win / macOS / Linux", "3.5.3", "forest"),
             ("Better MC 整合包", "整合包", "1.20.1 · 120+ MOD", "120+", "village"),
             ("Create 机械动力", "MOD", "前置 Flywheel · Forge", "0.5.1", "night"),
             ("Complementary 光影", "光影", "需 Iris / OptiFine", "r5.2", "ocean")]
    cy = y + 56
    cwid = (CW - 3 * 24) / 4
    hot_targets = ["P020101", "P020201", "P020301", "P020401"]
    for i, (nm, cat, meta, ver, var) in enumerate(items):
        x = CX + i * (cwid + 24)
        seg = [card_frame(x, cy, cwid, 386, CARD, LINE)]
        seg.append(voxel(x + 1, cy + 1, cwid - 2, 158, var, i + 5))
        seg.append(r(x + 1, cy + 1, cwid - 2, 158, "none", LINE))
        seg.append(t(x + 16, cy + 196, cat.upper(), 10, GRASS, 700, family=MONO, ls=1.6))
        seg.append(t(x + 16, cy + 224, nm, 18, INK, 800))
        seg.append(t(x + 16, cy + 250, meta, 12, MUT))
        seg.append(r(x + 16, cy + 274, cwid - 32, 1, LINE))
        seg.append(t(x + 16, cy + 304, "v " + ver, 10, MUT2, 400, family=MONO))
        seg.append(t(x + cwid - 16, cy + 304, "查看详情 →", 12, GRASS, 700, "end"))
        seg.append(r(x, cy, 3, 60, GRASS if i == 0 else LINE2))
        p.append(link(hot_targets[i], "".join(seg)))

    # ---------- 社区动态 ----------
    y = 1700
    p.append(sec_head(CX, y, "03", "社区此刻", "LIVE COMMUNITY", "12,480 人在线 · 今日 236 条新帖"))
    cy = y + 56
    # 左：最新主题
    p.append(card_frame(CX, cy, 780, 400, CARD, LINE))
    p.append(r(CX, cy, 780, 44, INK))
    p.append(t(CX + 20, cy + 28, "最新主题", 14, "#F2F7E8", 700))
    p.append(link("P0301", t(CX + 760, cy + 28, "全部 →", 11, GRASS_L, 600, "end")))
    rows = [("[整合包] 1.20.1 机械动力服务器推荐", "建筑与红石", "86 回复 · 2 分钟前"),
            ("[求助] 启动器卡在检查更新怎么办", "帮助与反馈", "42 回复 · 8 分钟前"),
            ("[作品] 用 12000 个方块复刻主城", "创作展示", "128 回复 · 15 分钟前"),
            ("[教程] 从零写一个数据包", "技术讨论", "36 回复 · 22 分钟前"),
            ("[联机] 周末生存服招新（1.20.1）", "服务器招募", "64 回复 · 31 分钟前")]
    for i, (ti, board, meta) in enumerate(rows):
        ry = cy + 58 + i * 66
        seg = [avatar(CX + 20, ry + 6, 34, i)]
        seg.append(t(CX + 68, ry + 26, ti, 14, INK, 700))
        seg.append(t(CX + 68, ry + 46, board, 11, GRASS, 700))
        seg.append(t(CX + 760, ry + 30, meta, 11, MUT2, 400, "end"))
        if i < 4:
            seg.append(ln(CX + 20, ry + 58, CX + 760, ry + 58, LINE, 1))
        p.append(link("P03010101", "".join(seg)))
    # 右：在线服务器
    p.append(card_frame(CX + 804, cy, 396, 400, INK, INK))
    p.append(t(CX + 824, cy + 30, "在线服务器", 14, "#F2F7E8", 700))
    p.append(r(CX + 1090, cy + 18, 86, 22, "#20301F"))
    p.append(r(CX + 1096, cy + 24, 6, 6, GRASS_L))
    p.append(t(CX + 1108, cy + 34, "LIVE", 9, GRASS_L, 700, family=MONO, ls=1))
    sv = [("橡木镇 · 原版生存", "1.20.1 · 86/200", "forest"), ("深岩堡 · 模组生存", "1.20.1 · 142/300", "night"),
          ("潮汐湾 · 建筑服", "1.19.2 · 58/120", "ocean"), ("熔炉城 · PVP", "1.20.1 · 96/150", "nether")]
    for i, (nm, meta, var) in enumerate(sv):
        yy = cy + 56 + i * 82
        seg = [block_icon(CX + 820, yy, 64, 64, top=[GRASS, "#6E9455", "#7E9BAA", "#B4522A"][i],
                          soil=["#8A6A46", "#5A4A3A", "#A88F68", "#552017"][i],
                          accent=[GRASS_L, GRASS_L, BLUE, AMBER][i], seed=i + 3)]
        seg.append(t(CX + 898, yy + 26, nm, 13, "#EAF2E0", 700))
        seg.append(t(CX + 898, yy + 46, meta, 10, MUT2, 400))
        p.append(link("P030201", "".join(seg)))

    # ---------- 新手 CTA ----------
    y = 2180
    p.append(r(CX, y, CW, 200, INK))
    p.append(r(CX, y, 6, 200, GRASS))
    p.append(t(CX + 44, y + 62, "第一次进入 MC？", 30, "#F4F8EC", 800))
    p.append(t(CX + 44, y + 96, "认识 MC → 版本与玩法 → 新手教程 → 启动器下载，四步进入游戏。", 14, "#A9B9A2"))
    steps = ["认识 MC", "版本与玩法", "新手教程", "启动器下载"]
    sx = CX + 44
    for i, s in enumerate(steps):
        w = len(s) * 13 + 24
        p.append(r(sx, y + 122, w, 34, "#1B2A1E"))
        p.append(t(sx + 12, y + 144, s, 12, "#DAE4D5"))
        if i < len(steps) - 1:
            p.append(icon(sx + w + 10, y + 133, "chevron", GRASS, 12))
        sx += w + 34
    p.append(link("P0103", btn(CX + CW - 224, y + 118, 184, 48, "开始新手路线", "primary", 14, True)))

    # 页脚
    p.append(footer(2480, "P00 / INDEX"))
    H = 2800
    return W, H, "".join(p), "品牌区 / 六入口 / 热门资源 / 社区动态 / 新手路径"


BUILDERS = {"P00": page_home}
