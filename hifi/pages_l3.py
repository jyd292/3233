# -*- coding: utf-8 -*-
"""L3 页面 · 认识 MC 频道 + 通用文章页"""
from ds import *
from blocks import (cover_card, detail_title, filter_row, page_head, pager, related,
                    section_banner, side_download, body_paras, cover_panel, feature_grid,
                    spec_table, steps_list, tag_pill)


def article_page(cfg):
    code, name, active = cfg["code"], cfg["name"], cfg["active"]
    crumb, kicker, title, lead = cfg["crumb"], cfg["kicker"], cfg["title"], cfg["lead"]
    sections, toc = cfg["sections"], cfg.get("toc", [])
    stat_right = cfg.get("stats")
    p = [page_strip(code, name, cfg.get("level", "L3"), cfg.get("strip", "")), topbar(active, 30)]
    p.append(breadcrumb(118, crumb, "面包屑回溯 R2"))
    hy, hh = 170, 246
    p.append(r(0, hy, W, hh, PAPER))
    p.append(ln(0, hy + hh, W, hy + hh, LINE))
    p.append(t(CX, hy + 50, kicker, 11, GRASS_D, 700, family=MONO, ls=1.6))
    p.append(t(CX, hy + 106, title, 40, INK, 800, ls=0.5))
    p.append(t(CX, hy + 140, lead, 14, MUT))
    p.append(t(CX, hy + 208, cfg.get("meta", ""), 11, MUT2, 400))
    if stat_right:
        sx = CX + CW
        for i, (n, l) in enumerate(reversed(stat_right)):
            p.append(stat(sx - 150, hy + 120, n, l, INK, 26))
            sx -= 160
    # 正文
    by = hy + hh + 44
    LX, LW = CX, 780
    RX, RW = CX + 820, 380
    # TOC
    p.append(r(RX, by, RW, 52 + len(toc) * 34, CARD, LINE, 1))
    p.append(r(RX, by, RW, 4, GRASS))
    p.append(t(RX + 20, by + 32, "本页目录", 13, INK, 800))
    for i, it in enumerate(toc):
        yy = by + 56 + i * 34
        p.append(t(RX + 20, yy + 20, str(i + 1).zfill(2), 10, GRASS_D if i == 0 else MUT2, 700, family=MONO))
        p.append(t(RX + 46, yy + 20, it, 12, INK if i == 0 else MUT, 700 if i == 0 else 400))
        if i == 0:
            p.append(r(RX + 12, yy + 10, 2, 12, GRASS))
    ys = by
    for sec in sections:
        kind = sec[0]
        if kind == "h2":
            ys += 24
            p.append(t(LX, ys, sec[1], 22, INK, 800))
            p.append(ln(LX, ys + 14, LX + LW, ys + 14, LINE2))
            ys += 42
        elif kind == "p":
            p.append(para(LX, ys, sec[1], 14, MUT, 26, LW))
            ys += 26 * len(wrap(sec[1], 14, LW)) + 14
        elif kind == "img":
            p.append(cover_panel(LX, ys, LW, 340, sec[1], sec[2], sec[3] if len(sec) > 3 else ""))
            ys += 372
        elif kind == "list":
            for it in sec[1]:
                p.append(r(LX, ys + 6, 8, 8, GRASS))
                p.append(t(LX + 20, ys + 16, it, 13, INK, 600))
                p.append(t(LX + 20, ys + 36, "", 10, MUT))
                ys += 34
            ys += 10
        elif kind == "quote":
            p.append(r(LX, ys, LW, 62, GRASS_SOFT))
            p.append(r(LX, ys, 4, 62, GRASS))
            p.append(t(LX + 24, ys + 38, sec[1], 14, GRASS_D, 700))
            ys += 82
        elif kind == "table":
            p.append(spec_table(LX, ys, LW, sec[2], sec[1], sec[3] if len(sec) > 3 else (180, 380, 220))[0])
            ys += 40 + len(sec[2]) * 44 + 18
        elif kind == "steps":
            p.append(steps_list(LX, ys, LW, sec[1])[0])
            ys += len(sec[1]) * 66 + 10
        elif kind == "note":
            p.append(r(LX, ys, LW, 54, PAPER2))
            p.append(icon(LX + 18, ys + 17, "check", GRASS_D, 18))
            p.append(t(LX + 46, ys + 33, sec[1], 12, MUT))
            ys += 70
    # 右侧底部提示
    p.append(r(RX, by + 90 + len(toc) * 34, RW, 118, INK))
    p.append(t(RX + 20, by + 126 + len(toc) * 34, "还没解决？", 14, "#F2F7E8", 800))
    p.append(t(RX + 20, by + 150 + len(toc) * 34, "把日志与截图发到论坛或联系我们", 11, "#A9B9A2"))
    p.append(link("P0502", r(RX + 20, by + 166 + len(toc) * 34, 150, 34, GRASS) +
                  t(RX + 95, by + 188 + len(toc) * 34, "联系与反馈", 12, WHITE, 700, "middle")))
    yend = max(ys, by + 400)
    p.append(footer(yend + 40, f"{code} / {cfg.get('level','L3')}"))
    return W, yend + 360, "".join(p), lead


# ---------------- P0101 游戏简介 ----------------
def p_intro():
    return article_page(dict(
        code="P0101", name="游戏简介", active="认识 MC", level="L3",
        strip="GUIDE / INTRO · SANDBOX · MODES",
        crumb=["首页", "认识 MC", "游戏简介"],
        kicker="GUIDE / GAME INTRO",
        title="Minecraft 是什么？",
        lead="一个由方块构成的世界：采集、建造、探索、联机，四种玩法从同一套规则长出来。",
        meta="更新于 2024-06-12 · 阅读约 6 分钟 · 作者 MC HUB 编辑部",
        stats=[("2009", "首次发布"), ("300M+", "全球销量")],
        toc=["它是什么", "四种玩法", "为什么值得玩", "下一步"],
        sections=[
            ("h2", "一、它是什么"),
            ("p", "Minecraft 是一款沙盒建造游戏。世界由 1 米见方的方块组成，地形、植被、矿物、生物都按同一套规则生成，玩家可以破坏、放置、组合这些方块，把世界改造成任何样子。"),
            ("p", "它没有固定的主线剧情。你可以把目标定成「活过第一夜」、造一座城堡、写完一个自动化模组，或者只是和朋友在服务器里聊天。规则简单，但组合空间极大，这是它能持续十五年的原因。"),
            ("img", "village", "主世界 · 村庄与草原", "SURVIVAL / OVERWORLD"),
            ("h2", "二、四种玩法"),
            ("list", ["生存模式：采集资源、合成工具、建造庇护所，并在夜晚对抗怪物。",
                      "创造模式：无限方块与飞行，适合建筑、红石与场景创作。",
                      "多人联机：局域网、服务器或联机工具，一起建造、冒险或对抗。",
                      "模组扩展：通过 MOD 与整合包，加入机械、魔法、任务与全新维度。"]),
            ("h2", "三、为什么值得玩"),
            ("p", "它同时是一个游戏、一个创作工具和一个社交空间。你可以在单人世界里安静建造，也可以在服务器里和几十个人协作完成一个项目；可以用原版规则，也可以装上百个模组把它变成另一款游戏。"),
            ("quote", "「先活过第一夜，再谈建筑与红石。」—— 新手路线第一课"),
            ("h2", "四、下一步"),
            ("p", "如果还没安装，先看「版本与玩法」确认设备与版本；如果已经装好，直接进入「新手入门教程」，按难度逐级跟做。"),
            ("note", "下载类页面必须出现版本与兼容性信息；本站在每个资源详情页固定展示（R5）。"),
        ]))


# ---------------- P0102 版本与玩法 ----------------
def p_versions():
    p = [page_strip("P0102", "版本与玩法", "L3", "GUIDE / JAVA · BEDROCK · SNAPSHOT"), topbar("认识 MC", 30)]
    p.append(breadcrumb(118, ["首页", "认识 MC", "版本与玩法"], "面包屑回溯 R2"))
    p.append(page_head(170, "GUIDE / VERSIONS", "版本与玩法",
                       "Java 版、基岩版与快照版本的核心差异：模组、跨平台、服务器与性能。",
                       right=[("3", "版本分支"), ("1.20.1", "推荐版本")]))
    y = 384
    p.append(filter_row(y, [("类型", ["全部", "Java", "基岩", "快照"]),
                            ("用途", ["全部", "生存", "模组", "跨平台"])], "共 18 个版本记录"))
    y = 500
    p.append(sec_head(CX, y, "01", "版本对照表", "VERSION MATRIX", "按发布时间倒序 · 点击行进入版本详情"))
    y += 56
    rows = [("1.21", "Java", "2024-06-13", "试炼厅 / 新怪物", "尝鲜玩家", "详情 →"),
            ("1.20.6", "Java", "2024-04-29", "稳定性与修复", "模组玩家", "详情 →"),
            ("1.20.1", "Java", "2023-06-12", "模组生态最完整", "推荐 · 模组 / 服务器", "详情 →"),
            ("1.20.0", "基岩", "2023-06-07", "跨平台联机", "手机 / 主机玩家", "详情 →"),
            ("1.19.2", "Java", "2022-08-05", "大量整合包兼容", "整合包玩家", "详情 →"),
            ("1.18.2", "Java", "2022-02-28", "洞穴与山崖", "低配设备", "详情 →")]
    p.append(r(CX, y, CW, 44, INK))
    heads = [("版本", 0), ("类型", 200), ("发布时间", 320), ("核心特性", 500), ("适合人群", 860), ("", 1120)]
    for hd, off in heads:
        p.append(t(CX + 20 + off, y + 28, hd, 11, "#C9D6BE", 700))
    for i, row in enumerate(rows):
        yy = y + 44 + i * 76
        seg = [r(CX, yy, CW, 76, CARD if i % 2 == 0 else PAPER)]
        seg.append(ln(CX, yy + 76, CX + CW, yy + 76, LINE))
        seg.append(t(CX + 20, yy + 40, row[0], 20, INK, 800, family=MONO))
        seg.append(r(CX + 20, yy + 50, 42, 2, GRASS if i == 2 else LINE2))
        seg.append(t(CX + 220, yy + 42, row[1], 12, GRASS_D, 700))
        seg.append(t(CX + 340, yy + 42, row[2], 11, MUT, 400, family=MONO))
        seg.append(t(CX + 520, yy + 42, row[3], 13, INK))
        seg.append(t(CX + 880, yy + 42, row[4], 12, MUT))
        seg.append(t(CX + CW - 20, yy + 58, row[5], 12, GRASS_D, 700, "end"))
        p.append(link("P010201" if i in (0, 2) else "P0102", "".join(seg)))
    y = y + 44 + len(rows) * 76 + 28
    p.append(r(CX, y, CW, 86, GRASS_SOFT))
    p.append(icon(CX + 20, y + 32, "check", GRASS_D, 20))
    p.append(t(CX + 50, y + 40, "推荐：第一次玩选 1.20.1（Java）", 14, GRASS_D, 700))
    p.append(t(CX + 50, y + 62, "模组与整合包生态最完整；基岩版适合手机与主机跨平台联机。", 12, MUT))
    y += 86
    # 三卡片
    p.append(sec_head(CX, y + 50, "02", "三条路线", "PATHS", "按你的设备与目标选择"))
    cw3 = (CW - 2 * 24) / 3
    items = [("Java 版", "模组 / 服务器", "模组与整合包最多，适合长期游玩", "forest", "P010201"),
             ("基岩版", "手机 / 主机", "跨平台联机方便，性能稳定", "village", "P0102"),
             ("快照版", "尝鲜", "提前体验新内容，稳定性较低", "night", "P0102")]
    for i, (nm, cat, meta, var, tg) in enumerate(items):
        p.append(cover_card(CX + i * (cw3 + 24), y + 106, cw3, 330, nm, cat, meta, var, tg))
    y = y + 106 + 330
    p.append(footer(y + 60, "P0102 / L3"))
    return W, y + 380, "".join(p), "Java / 基岩 / 快照版本对照表"


# ---------------- P0103 新手入门教程 ----------------
def p_tutorials():
    p = [page_strip("P0103", "新手入门教程", "L3", "GUIDE / TUTORIAL SERIES"), topbar("认识 MC", 30)]
    p.append(breadcrumb(118, ["首页", "认识 MC", "新手入门教程"], "面包屑回溯 R2"))
    p.append(page_head(170, "GUIDE / TUTORIAL", "新手入门教程",
                       "从第一夜到第一次联机：12 篇教程按难度分级，建议按顺序跟做。",
                       right=[("12", "篇教程"), ("3", "难度等级")]))
    y = 314
    p.append(filter_row(y, [("难度", ["全部", "入门", "进阶", "挑战"]),
                            ("主题", ["全部", "生存", "建筑", "红石", "联机"])], "共 12 篇 · 学习进度 0%"))
    y = 374
    p.append(sec_head(CX, y, "01", "教程目录", "CURRICULUM", "建议从 01 开始，按顺序解锁"))
    y += 56
    cards = [("第一夜生存清单", "入门", "难度 1 · 30 分钟 · 1.20.1", "forest", "P010301", "01"),
             ("第一座庇护所", "入门", "难度 1 · 25 分钟 · 任意版本", "village", "P010301", "02"),
             ("工具与矿物入门", "入门", "难度 2 · 35 分钟 · 1.20.1", "night", "P010301", "03"),
             ("农田与食物", "入门", "难度 2 · 20 分钟 · 1.20.1", "forest", "P010301", "04"),
             ("下界通行证", "进阶", "难度 3 · 40 分钟 · 1.20.1", "nether", "P010301", "05"),
             ("红石入门：门与灯", "进阶", "难度 3 · 45 分钟 · 1.20.1", "village", "P010301", "06"),
             ("建筑配色基础", "进阶", "难度 3 · 30 分钟 · 任意版本", "ocean", "P010301", "07"),
             ("第一次联机", "进阶", "难度 3 · 25 分钟 · 1.20.1", "night", "P010301", "08"),
             ("整合包安装", "挑战", "难度 4 · 30 分钟 · 1.20.1", "forest", "P010301", "09")]
    cw3 = (CW - 2 * 24) / 3
    for i, (nm, diff, meta, var, tg, idx) in enumerate(cards):
        row, col = divmod(i, 3)
        x = CX + col * (cw3 + 24)
        yy = y + row * 386
        p.append(cover_card(x, yy, cw3, 366, nm, diff, meta, var, tg, tag=diff, idx=idx, footer_left="教程"))
    y = y + 3 * 386
    p.append(section_banner(y + 40, "学完基础，去装一个整合包", "从下载中心开始：启动器 → 整合包 → MOD 与光影。",
                            "进入下载中心", "P02", 160))
    y += 200
    p.append(footer(y + 40, "P0103 / L3"))
    return W, y + 340, "".join(p), "教程目录 / 难度分级"


# ---------------- P0104 常见问题 ----------------
def p_faq():
    p = [page_strip("P0104", "常见问题", "L3", "GUIDE / FAQ"), topbar("认识 MC", 30)]
    p.append(breadcrumb(118, ["首页", "认识 MC", "常见问题"], "面包屑回溯 R2"))
    p.append(page_head(170, "GUIDE / FAQ", "常见问题",
                       "启动失败、联机超时、模组冲突……先在这里找答案，已解决 92%。",
                       right=[("186", "个问题"), ("92%", "解决率")]))
    y = 314
    # 搜索条
    p.append(r(CX, y, 760, 56, CARD, LINE2, 1))
    p.append(icon(CX + 20, y + 18, "search", MUT2, 20))
    p.append(t(CX + 50, y + 34, "搜索问题关键词，如「崩溃」「联机」「Java」", 13, MUT2))
    p.append(link("G02", r(CX + 772, y, 120, 56, GRASS) + t(CX + 832, y + 34, "搜索", 14, WHITE, 700, "middle")))
    p.append(t(CX + CW, y + 34, "热门搜索：崩溃 / 联机超时 / 前置 MOD", 11, MUT2, 400, "end"))
    y = 386
    # 分类
    cats = ["全部", "启动与安装", "账号与登录", "联机与服务器", "性能与报错", "下载与资源"]
    cx = CX
    for i, c in enumerate(cats):
        on = i == 0
        w = len(c) * 13 + 30
        p.append(r(cx, y, w, 34, INK if on else CARD, None if on else LINE, 1))
        p.append(t(cx + w / 2, y + 22, c, 12, GRASS_L if on else MUT, 700 if on else 400, "middle"))
        cx += w + 10
    # 左问题列表
    y = 444
    p.append(sec_head(CX, y, "01", "热门问题", "TOP QUESTIONS", "按浏览量排序 · 共 186 条"))
    y += 56
    qs = [("游戏启动崩溃，日志提示 Java 版本不匹配怎么办？", "启动与安装", "12,860 浏览 · 解决率 91%", "P010401"),
          ("HMCL 打开后一直停在「正在检查更新」", "启动与安装", "9,420 浏览 · 解决率 88%", "P010401"),
          ("整合包导入后提示缺少前置 MOD，无法启动", "下载与资源", "8,760 浏览 · 解决率 84%", "P010401"),
          ("联机提示「连接超时」，但局域网可以进入", "联机与服务器", "7,180 浏览 · 解决率 79%", "P010401"),
          ("帧数很低，光影包一开就掉到 20 FPS", "性能与报错", "6,540 浏览 · 解决率 76%", "P010401"),
          ("正版账号登录失败 / 一直要求验证邮箱", "账号与登录", "5,320 浏览 · 解决率 82%", "P010401"),
          ("资源包放进文件夹后，游戏里看不到", "下载与资源", "4,180 浏览 · 解决率 90%", "P010401"),
          ("服务器显示「版本不兼容」，无法加入", "联机与服务器", "3,960 浏览 · 解决率 87%", "P010401")]
    for i, (q, cat, meta, tg) in enumerate(qs):
        yy = y + i * 74
        seg = [r(CX, yy, 780, 64, CARD, LINE, 1)]
        seg.append(r(CX, yy, 3, 64, GRASS if i < 3 else LINE2))
        seg.append(t(CX + 20, yy + 24, f"Q{i+1}", 10, GRASS_D, 700, family=MONO))
        seg.append(t(CX + 56, yy + 26, q, 14, INK, 700))
        seg.append(t(CX + 56, yy + 48, cat, 11, GRASS_D))
        seg.append(t(CX + 260, yy + 48, meta, 10, MUT2, 400, family=MONO))
        seg.append(t(CX + 760, yy + 38, "查看解答 →", 12, GRASS_D, 700, "end"))
        p.append(link(tg, "".join(seg)))
    yend = y + len(qs) * 74
    # 右侧
    RX, RW = CX + 820, 380
    p.append(r(RX, y, RW, 176, GRASS_SOFT))
    p.append(r(RX, y, RW, 4, GRASS))
    p.append(t(RX + 24, y + 40, "仍然没有解决？", 16, GRASS_D, 800))
    p.append(t(RX + 24, y + 68, "把日志和截图发到论坛，或直接联系我们。", 11, MUT))
    p.append(link("P0502", r(RX + 24, y + 92, RW - 48, 40, GRASS) +
                  t(RX + 24 + (RW - 48) / 2, y + 117, "联系与反馈", 12, WHITE, 700, "middle")))
    p.append(link("P0301", r(RX + 24, y + 138, RW - 48, 30, "none", LINE2, 1) +
                  t(RX + 24 + (RW - 48) / 2, y + 158, "去论坛发帖求助", 11, MUT, 600, "middle")))
    p.append(t(RX, y + 218, "相关问题", 13, INK, 800))
    for i, (tt, mm, tg) in enumerate([("Java 版本怎么选", "启动与安装", "P010401"),
                                     ("前置 MOD 怎么装", "下载与资源", "P010401"),
                                     ("服务器版本对齐", "联机与服务器", "P010401")]):
        yy = y + 240 + i * 60
        seg = [r(RX, yy, RW, 52, CARD, LINE, 1)]
        seg.append(t(RX + 16, yy + 22, tt, 12, INK, 700))
        seg.append(t(RX + 16, yy + 40, mm, 10, MUT2))
        seg.append(t(RX + RW - 16, yy + 30, "→", 12, GRASS_D, 700, "end"))
        p.append(link(tg, "".join(seg)))
    y2 = max(yend, y + 432)
    p.append(section_banner(y2 + 40, "没找到答案？", "论坛里已有 2,318 个主题，发帖前先搜一遍。", "进入论坛板块", "P0301", 152))
    y2 += 192
    p.append(footer(y2 + 40, "P0104 / L3"))
    return W, y2 + 340, "".join(p), "分类 FAQ / 关键词检索"


BUILDERS = {
    "P0101": p_intro,
    "P0102": p_versions,
    "P0103": p_tutorials,
    "P0104": p_faq,
}
