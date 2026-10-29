# -*- coding: utf-8 -*-
"""全局工具页 G01–G03"""
from ds import *
from blocks import cover_card, page_head, tag_pill


def login():
    p = [page_strip("G01", "登录 / 注册", "G", "GLOBAL / AUTH"), topbar(None, 30)]
    y = 118
    p.append(r(0, y, W, 940, INK))
    for i in range(1, 40):
        p.append(r(i * 48, y, 1, 940, "#16231A"))
    # 左侧
    p.append(r(CX + 20, y + 90, 40, 40, GRASS))
    p.append(r(CX + 27, y + 97, 26, 26, INK))
    p.append(t(CX + 74, y + 118, "MC HUB", 22, "#F3F8E9", 800, ls=1))
    p.append(t(CX + 74, y + 138, "APPLICATIONS & COMMUNITY", 9, MUT2, 700, family=MONO, ls=1.6))
    p.append(t(CX + 20, y + 236, "回到你的世界。", 44, "#F4F8EC", 800, ls=1))
    p.append(t(CX + 20, y + 276, "登录后可发帖、收藏资源、加入服务器。", 14, "#A9B9A2"))
    p.append(voxel(CX + 20, y + 340, 560, 380, "village", 12))
    p.append(t(CX + 20, y + 756, "FIG.02", 10, "#7C8B77", 400, family=MONO, ls=0.8))
    p.append(t(CX + 72, y + 756, "— 橡木镇 · 服务器主城", 10, "#7C8B77", 400))
    stats = [("12,480", "在线玩家"), ("2,318", "论坛主题"), ("1,860", "资源收录")]
    sx = CX + 20
    for i, (n, l) in enumerate(stats):
        p.append(stat(sx, y + 840, n, l, "#F4F8EC", 26))
        sx += 200
    # 右侧表单
    fx = CX + 680
    fw = 520
    p.append(r(fx, y + 120, fw, 700, CARD, LINE, 1))
    p.append(r(fx, y + 120, fw, 4, GRASS))
    p.append(t(fx + 40, y + 184, "登录 MC HUB", 26, INK, 800))
    p.append(t(fx + 40, y + 212, "使用邮箱或手机号登录，未注册将自动创建账号。", 12, MUT))
    # tabs
    p.append(r(fx + 40, y + 244, 200, 42, PAPER2))
    p.append(r(fx + 40, y + 244, 100, 42, INK))
    p.append(t(fx + 90, y + 271, "登录", 13, GRASS_L, 700, "middle"))
    p.append(t(fx + 190, y + 271, "注册", 13, MUT, 400, "middle"))
    # fields
    p.append(t(fx + 40, y + 320, "邮箱 / 手机号", 11, INK, 700))
    p.append(r(fx + 40, y + 334, fw - 80, 48, PAPER, LINE2, 1))
    p.append(t(fx + 56, y + 364, "you@example.com", 12, MUT2))
    p.append(t(fx + 40, y + 408, "密码", 11, INK, 700))
    p.append(r(fx + 40, y + 422, fw - 80, 48, PAPER, LINE2, 1))
    p.append(t(fx + 56, y + 452, "••••••••", 12, MUT2))
    p.append(icon(fx + fw - 72, y + 436, "eye", MUT2, 18))
    p.append(r(fx + 40, y + 486, 18, 18, CARD, LINE2, 1))
    p.append(t(fx + 66, y + 500, "记住登录状态（30 天）", 11, MUT))
    p.append(link("P0303", r(fx + 40, y + 522, fw - 80, 52, GRASS) +
                  r(fx + 44, y + 522, fw - 88, 3, GRASS_L) +
                  t(fx + 40 + (fw - 80) / 2, y + 555, "登录", 15, WHITE, 800, "middle")))
    p.append(link("P0502", t(fx + 40, y + 602, "忘记密码？", 11, MUT)))
    p.append(t(fx + 40, y + 630, "第三方登录", 10, MUT2, 700, ls=0.8))
    p.append(t(fx + 92, y + 630, "/ SSO", 10, MUT2, 700, family=MONO, ls=1))
    p.append(ln(fx + 148, y + 626, fx + fw - 40, y + 626, LINE))
    for i, (nm, ic) in enumerate([("微信", "forum"), ("QQ", "user"), ("GitHub", "link")]):
        xx = fx + 40 + i * 148
        p.append(r(xx, y + 646, 136, 44, PAPER, LINE2, 1))
        p.append(icon(xx + 18, y + 656, ic, MUT, 18))
        p.append(t(xx + 46, y + 674, nm, 11, MUT, 600))
    p.append(t(fx + 40, y + 724, "登录即视为同意《用户协议与隐私》", 10, MUT2))
    p.append(link("P00", t(fx + fw - 40, y + 724, "返回首页 →", 10, GRASS_D, 700, "end")))
    p.append(footer(1100, "G01 / GLOBAL"))
    return W, 1440, "".join(p), "登录 / 注册 / 找回密码"


def search():
    p = [page_strip("G02", "搜索结果", "G", "GLOBAL / SEARCH"), topbar(None, 30)]
    y = 118
    p.append(r(0, y, W, 300, INK))
    for i in range(1, 40):
        p.append(r(i * 48, y, 1, 300, "#16231A"))
    p.append(t(CX, y + 56, "SEARCH", 11, GRASS_L, 700, family=MONO, ls=1.6))
    p.append(t(CX + 58, y + 56, "/ 全站搜索", 11, "#A9B9A2", 600))
    p.append(r(CX, y + 84, 860, 60, "#0A100B", "#2C3C2F", 1))
    p.append(icon(CX + 20, y + 102, "search", GRASS_L, 22))
    p.append(t(CX + 56, y + 122, "整合包 1.20.1", 16, "#F4F8EC", 600))
    p.append(link("G02", r(CX + 870, y + 84, 124, 60, GRASS) +
                  t(CX + 932, y + 122, "搜索", 14, WHITE, 800, "middle")))
    p.append(t(CX, y + 178, "结果约 236 条  ·  用时 0.12 秒  ·  已按相关度排序", 11, "#7C8B77", 400))
    p.append(t(CX + CW, y + 178, "搜索覆盖：页面 / MOD / 整合包 / 帖子 / 视频", 10, "#7C8B77", 400, "end"))
    y = 418
    # tabs
    tabs = [("全部", "236", True), ("页面", "12", False), ("MOD", "86", False),
            ("整合包", "42", False), ("帖子", "64", False), ("视频", "32", False)]
    x = CX
    for lb, cnt, on in tabs:
        w = len(lb) * 14 + 62
        p.append(r(x, y, w, 44, INK if on else CARD, None if on else LINE, 1))
        p.append(t(x + 16, y + 28, lb, 12, GRASS_L if on else INK, 700 if on else 400))
        p.append(t(x + w - 14, y + 28, cnt, 9, GRASS_L if on else MUT2, 400, "end", MONO))
        x += w + 8
    p.append(link("P0102", t(CX + CW, y + 28, "切换为「最新」排序 →", 10, MUT2, 400, "end")))
    y = 486
    # 结果
    results = [("整合包", "Better MC [FORGE] 整合包", "1.20.1 · 120+ MOD · 4.4 分 · 86,200 次下载", "modpack-detail.html?id=1024", "P020201", "village"),
               ("整合包", "Create: Astral 整合包", "1.18.2 · 200+ MOD · 4.7 分 · 42,600 次下载", "modpack-detail.html?id=2048", "P020201", "forest"),
               ("MOD", "Create 机械动力 0.5.1", "1.20.1 · Forge · 前置 Flywheel · 142,800 次下载", "mod-detail.html?id=301", "P020301", "night"),
               ("帖子", "1.20.1 机械动力服务器推荐", "综合讨论区 · 86 回复 · 2 分钟前", "post.html?id=1024", "P03010101", "ocean"),
               ("页面", "版本与玩法 · 1.20.1 说明", "认识 MC · 版本对照 · 发布于 2023-06-12", "guide-versions.html", "P0102", "forest"),
               ("视频", "机械动力全流程（第 1 集）", "视频攻略 · 7.2 万播放 · 18 集", "watch.html?id=2048", "P040101", "village")]
    for i, (typ, ti, ds_, path, tg, var) in enumerate(results):
        yy = y + i * 116
        seg = [r(CX, yy, 800, 100, CARD, LINE, 1)]
        seg.append(voxel(CX + 1, yy + 1, 140, 98, var, i + 7))
        seg.append(r(CX + 1, yy + 1, 140, 98, "none", LINE))
        seg.append(r(CX + 156, yy + 16, len(typ) * 10 + 18, 22, PAPER2))
        seg.append(t(CX + 166, yy + 32, typ, 10, GRASS_D, 700))
        seg.append(t(CX + 156, yy + 62, ti, 16, INK, 800))
        seg.append(t(CX + 156, yy + 84, ds_, 11, MUT))
        seg.append(t(CX + 780, yy + 32, path, 9, MUT2, 400, "end", MONO))
        seg.append(t(CX + 780, yy + 62, "进入 →", 11, GRASS_D, 700, "end"))
        p.append(link(tg, "".join(seg)))
    y = y + 6 * 116
    p.append(r(CX, y + 10, 800, 40, CARD, LINE, 1))
    p.append(t(CX + 380, y + 36, "1  /  8  ·  下一页 →", 11, MUT, 400, "middle"))
    y += 60
    # 右侧筛选
    RX, RW = CX + 840, 360
    p.append(r(RX, 486, RW, 430, CARD, LINE, 1))
    p.append(t(RX + 20, 522, "筛选结果", 14, INK, 800))
    groups = [("类型", ["整合包 42", "MOD 86", "帖子 64", "页面 12", "视频 32"]),
              ("版本", ["1.20.1 126", "1.19.2 42", "1.18.2 36", "其他 32"]),
              ("排序", ["相关度", "最新", "下载量"])]
    yy = 546
    for gi, (lb, opts) in enumerate(groups):
        p.append(t(RX + 20, yy + 20, lb, 11, MUT2, 700))
        for oi, o in enumerate(opts):
            on = oi == 0
            p.append(r(RX + 20, yy + 32 + oi * 34, RW - 40, 28, INK if on else PAPER))
            p.append(t(RX + 32, yy + 51 + oi * 34, o, 10, GRASS_L if on else MUT, 700 if on else 400))
        yy += 32 + len(opts) * 34 + 14
    p.append(r(RX, 936, RW, 180, GRASS_SOFT))
    p.append(t(RX + 20, 972, "没有找到？", 14, GRASS_D, 800))
    p.append(t(RX + 20, 998, "试试更短的关键词，或按类型筛选。", 11, MUT))
    p.append(link("P0104", t(RX + 20, 1030, "去常见问题找答案 →", 11, GRASS_D, 700)))
    p.append(link("P0301", t(RX + 20, 1058, "去论坛发帖求助 →", 11, GRASS_D, 700)))
    p.append(footer(y + 40, "G02 / GLOBAL"))
    return W, y + 360, "".join(p), "页面 / MOD / 整合包 / 帖子 / 视频分组结果"


def nf404():
    p = [page_strip("G03", "404 / 空状态", "G", "GLOBAL / NOT FOUND"), topbar(None, 30)]
    y = 118
    p.append(r(0, y, W, 660, PAPER))
    p.append(r(CX + 40, y + 60, 420, 360, INK))
    p.append(voxel(CX + 40, y + 60, 420, 360, "nether", 21))
    p.append(t(CX + 40, y + 452, "SECTOR NOT GENERATED", 9, MUT2, 700, family=MONO, ls=2))
    p.append(t(CX + 540, y + 140, "404", 120, INK, 800, family=MONO, ls=4))
    p.append(r(CX + 540, y + 168, 240, 6, GRASS))
    p.append(t(CX + 542, y + 232, "这个区块还没有被生成", 34, INK, 800))
    p.append(t(CX + 542, y + 270, "页面可能已移动、删除，或者链接拼错了。", 14, MUT))
    p.append(t(CX + 542, y + 296, "试试搜索，或者回到首页重新开始。", 14, MUT))
    p.append(r(CX + 542, y + 336, 440, 56, CARD, LINE2, 1))
    p.append(icon(CX + 562, y + 353, "search", MUT2, 20))
    p.append(t(CX + 592, y + 369, "搜索关键词…", 13, MUT2))
    p.append(link("G02", r(CX + 990, y + 336, 110, 56, GRASS) +
                  t(CX + 1045, y + 369, "搜索", 13, WHITE, 800, "middle")))
    p.append(link("P00", r(CX + 542, y + 416, 180, 48, INK) +
                  t(CX + 632, y + 446, "回到首页", 13, "#F2F7E8", 800, "middle")))
    p.append(link("P0301", r(CX + 738, y + 416, 180, 48, "none", LINE2, 2) +
                  t(CX + 828, y + 446, "去论坛求助", 13, INK, 700, "middle")))
    # 推荐
    y2 = 118 + 660 + 40
    p.append(sec_head(CX, y2, "01", "也许你在找", "MAYBE YOU NEED", "按访问量推荐"))
    cw3 = (CW - 2 * 24) / 3
    items = [("下载中心", "5 类资源 · 1,860 个条目", "village", "P02"),
             ("新手入门教程", "12 篇 · 30 分钟入门", "forest", "P0103"),
             ("论坛板块", "2,318 个主题 · 12,480 在线", "night", "P0301")]
    for i, (nm, ds_, var, tg) in enumerate(items):
        p.append(cover_card(CX + i * (cw3 + 24), y2 + 56, cw3, 320, nm, "推荐入口", ds_, var, tg))
    p.append(footer(y2 + 430, "G03 / GLOBAL"))
    return W, y2 + 750, "".join(p), "错误提示 + 搜索建议"


BUILDERS = {"G01": login, "G02": search, "G03": nf404}
