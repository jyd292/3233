# -*- coding: utf-8 -*-
"""L2 频道页（P01–P05）"""
from ds import *
from blocks import cover_card, filter_row, page_head, pager, related, section_banner, side_download


def channel(cfg):
    code, name, active = cfg["code"], cfg["name"], cfg["active"]
    en, no, lead, tone = cfg["en"], cfg["no"], cfg["lead"], cfg.get("tone", "forest")
    entries, picks, stats = cfg["entries"], cfg["picks"], cfg["stats"]
    p = [page_strip(code, name, "L2", cfg.get("strip", "")), topbar(active, 30)]
    p.append(breadcrumb(118, ["首页", name], "面包屑回溯 R2 · 每一级可点击"))
    # hero
    hy, hh = 170, 330
    p.append(r(0, hy, W, hh, INK))
    for i in range(1, 40):
        p.append(r(i * 48, hy, 1, hh, "#16231A"))
    p.append(t(CX, hy + 62, f"CHANNEL {no} / 05", 11, GRASS_L, 700, family=MONO, ls=2))
    p.append(t(CX, hy + 120, name, 46, "#F4F8EC", 800, ls=1))
    p.append(t(CX, hy + 164, lead, 15, "#A9B9A2"))
    # 数据
    sx = CX
    for i, (n, l) in enumerate(stats):
        p.append(stat(sx, hy + 232, n, l, "#F2F7E8", 28))
        if i:
            p.append(ln(sx - 28, hy + 206, sx - 28, hy + 240, "#2C3C2F"))
        sx += 190
    # 右侧索引
    ix, iw = CX + 780, 420
    p.append(r(ix, hy + 46, iw, 238, "#111B13", "#2C3C2F", 1))
    p.append(t(ix + 22, hy + 74, "频道索引", 10, MUT2, 700, ls=1.2))
    p.append(t(ix + 74, hy + 74, "/ INDEX", 10, "#7C8B77", 700, family=MONO, ls=1.5))
    for i, (nm, tg, desc, _tag) in enumerate(entries):
        yy = hy + 94 + i * 30
        p.append(t(ix + 22, yy + 18, f"0{i+1}", 10, GRASS_L, 700, family=MONO))
        p.append(t(ix + 54, yy + 18, nm, 13, "#E4EDDB", 600))
        p.append(t(ix + iw - 22, yy + 18, "→", 12, "#7C8B77", 400, "end"))
        p.append(ln(ix + 22, yy + 26, ix + iw - 22, yy + 26, "#223126"))
    # 栏目入口
    y = hy + hh + 64
    p.append(sec_head(CX, y, "01", "栏目入口", "SECTIONS", f"{len(entries)} 个二级栏目 · 点击进入 L3"))
    cy = y + 58
    cw = (CW - 24) / 2
    for i, (nm, tg, desc, _tag) in enumerate(entries):
        row, col = divmod(i, 2)
        x = CX + col * (cw + 24)
        yy = cy + row * 172
        seg = [card_frame(x, yy, cw, 158, CARD, LINE)]
        seg.append(t(x + 24, yy + 34, f"0{i+1}", 10, GRASS_D, 700, family=MONO, ls=1))
        seg.append(t(x + 64, yy + 34, nm, 20, INK, 800))
        seg.append(t(x + 24, yy + 66, desc, 13, MUT))
        seg.append(ln(x + 24, yy + 92, x + cw - 24, yy + 92, LINE))
        tp, nx = tag_pill(x + 24, yy + 106, _tag, GRASS_D, GRASS_SOFT)
        seg.append(tp)
        seg.append(t(x + cw - 24, yy + 124, "进入 →", 12, GRASS_D, 700, "end"))
        seg.append(r(x, yy, 4, 158, GRASS if i == 0 else LINE2))
        p.append(link(tg, "".join(seg)))
    yend = cy + ((len(entries) + 1) // 2) * 172
    # 精选
    py = yend + 56
    p.append(sec_head(CX, py, "02", "频道精选", "HIGHLIGHTS", "编辑手工挑选 · 每周一更新"))
    cw3 = (CW - 2 * 24) / 3
    for i, (nm, cat, meta, var, tg) in enumerate(picks[:3]):
        p.append(cover_card(CX + i * (cw3 + 24), py + 56, cw3, 356, nm, cat, meta, var, tg))
    yend = py + 56 + 356
    # CTA
    p.append(section_banner(yend + 64, cfg.get("cta_title", ""), cfg.get("cta_desc", ""),
                            cfg.get("cta_btn", "查看全部"), cfg.get("cta_target", entries[0][1]), 168))
    yend = yend + 232
    p.append(footer(yend + 60, f"{code} / L2"))
    return W, yend + 380, "".join(p), lead


CHANNELS = {
    "P01": dict(code="P01", name="认识 MC", active="认识 MC", en="KNOW MC", no="01", tone="forest",
                strip="CHANNEL / KNOW · INTRO · VERSIONS · TUTORIAL · FAQ",
                lead="从「这是什么」到「怎么开始玩」，四条主线带你在 30 分钟内完成第一次启动。",
                stats=[("4", "二级栏目"), ("12", "入门教程"), ("186", "常见问题")],
                entries=[("游戏简介", "P0101", "Minecraft 是什么、能玩什么、为什么值得玩", "入门第一站"),
                         ("版本与玩法", "P0102", "Java / 基岩 / 快照版本对照与差异", "含版本详情"),
                         ("新手入门教程", "P0103", "从第一夜到第一次联机，按难度分级", "新手主路径"),
                         ("常见问题", "P0104", "启动失败、联机超时、模组冲突的答案", "已解决 92%")],
                picks=[("Minecraft 是什么", "游戏简介", "沙盒 / 生存 / 创造 · 5 分钟读完", "forest", "P0101"),
                       ("Java 还是基岩版？", "版本与玩法", "跨平台 / 模组 / 服务器兼容", "village", "P0102"),
                       ("第一夜生存清单", "新手教程", "难度 1 · 约 30 分钟", "night", "P0103")],
                cta_title="还没决定从哪个版本开始？", cta_desc="版本与玩法 → 新手教程 → 启动器下载，三步完成。",
                cta_btn="进入版本与玩法", cta_target="P0102"),

    "P02": dict(code="P02", name="下载中心", active="下载中心", en="DOWNLOAD CENTER", no="02", tone="village",
                strip="CHANNEL / LAUNCHER · MODPACK · MOD · RESOURCE · NET TOOLS",
                lead="五类资源、一条安装链路：从启动器到整合包，版本与兼容性信息全部前置。",
                stats=[("1,860", "资源收录"), ("5", "资源分类"), ("12", "今日更新")],
                entries=[("启动器下载", "P0201", "官方 / HMCL / PCL2 横向对比与下载", "核心转化页"),
                         ("整合包获取", "P0202", "按分类、热度、版本筛选整合包", "含 MOD 清单"),
                         ("MOD 下载", "P0203", "分类 / 版本筛选 / 前置依赖提示", "前置校验"),
                         ("资源包与光影", "P0204", "资源包 / 光影分区与配置要求", "含配置要求"),
                         ("联机与语音工具", "P0205", "联机工具 / 语音工具分组对比", "开黑必备")],
                picks=[("HMCL 启动器", "启动器", "Win / macOS / Linux · 开源免费", "village", "P0201"),
                       ("Better MC 整合包", "整合包", "1.20.1 · 120+ MOD · 4.4 分", "forest", "P0202"),
                       ("Complementary 光影", "光影", "需 Iris / OptiFine · 中配可跑", "ocean", "P0204")],
                cta_title="不知道先装哪个？", cta_desc="先选启动器，再挑整合包，最后按需补 MOD 与光影。",
                cta_btn="查看启动器对比", cta_target="P0201"),

    "P03": dict(code="P03", name="社区交流", active="社区交流", en="COMMUNITY", no="03", tone="night",
                strip="CHANNEL / FORUM · SERVERS · PROFILE",
                lead="12,480 人在线：论坛讨论、服务器招募、个人收藏，都在同一条内容流里。",
                stats=[("2,318", "论坛主题"), ("12,480", "当前在线"), ("236", "今日新帖")],
                entries=[("论坛板块", "P0301", "分区列表 / 最新主题 / 发帖入口", "L5 最深处"),
                         ("服务器与联机", "P0302", "服务器列表 / 版本筛选 / 延迟", "实时在线"),
                         ("个人中心", "P0303", "资料 / 我的帖子 / 收藏入口", "需登录")],
                picks=[("1.20.1 机械动力服推荐", "论坛热帖", "86 回复 · 2 分钟前", "night", "P03010101"),
                       ("橡木镇 · 原版生存", "服务器", "1.20.1 · 86/200 · 32ms", "forest", "P030201"),
                       ("周末生存服招新", "服务器招募", "64 回复 · 版本 1.20.1", "village", "P0302")],
                cta_title="第一次发帖？", cta_desc="先读板块规则，再发主题；求助请附日志与截图。",
                cta_btn="进入论坛板块", cta_target="P0301"),

    "P04": dict(code="P04", name="攻略视频", active="攻略视频", en="GUIDES & VIDEOS", no="04", tone="ocean",
                strip="CHANNEL / VIDEO · ARTICLE",
                lead="视频跟做、图文细读：从第一夜到红石与建筑，看完即可跳转对应资源。",
                stats=[("86", "视频合集"), ("240", "图文攻略"), ("4.8", "平均评分")],
                entries=[("视频攻略", "P0401", "合集 / UP 主 / 难度分区，按顺序跟做", "含播放页"),
                         ("图文攻略", "P0402", "分类文章列表，适合查阅与精读", "含文章详情")],
                picks=[("新手 30 分钟入门", "视频攻略", "12.8 万播放 · 第 1 集", "ocean", "P040101"),
                       ("红石从零开始", "图文攻略", "12 分钟阅读 · 红石", "village", "P040201"),
                       ("建筑配色手册", "图文攻略", "8 分钟阅读 · 建筑", "forest", "P0402")],
                cta_title="想边看边装？", cta_desc="视频播放页右侧固定「看完 → 拿资源」入口。",
                cta_btn="打开视频攻略", cta_target="P0401"),

    "P05": dict(code="P05", name="关于与支持", active="关于与支持", en="ABOUT & SUPPORT", no="05", tone="village",
                strip="CHANNEL / ABOUT · CONTACT · CHANGELOG · LEGAL",
                lead="谁在维护 MC HUB、如何联系我们、站点如何迭代，以及你需要知道的协议。",
                stats=[("4", "信息栏目"), ("2", "工作日回复"), ("V1.0", "信息架构")],
                entries=[("关于我们", "P0501", "平台定位、团队与三项坚持", "平台介绍"),
                         ("联系与反馈", "P0502", "问题反馈、内容纠错、合作洽谈", "2 个工作日"),
                         ("更新日志", "P0503", "站点功能、资源库与规则记录", "按版本归档"),
                         ("用户协议与隐私", "P0504", "账号规则、内容规范、信息处理", "最近更新 2024-06")],
                picks=[("我们为什么做 MC HUB", "关于我们", "3 个人 · 1 个目标", "forest", "P0501"),
                       ("内容纠错怎么提", "联系与反馈", "附页面链接与截图", "village", "P0502"),
                       ("V1.0 上线记录", "更新日志", "2024-06-12 · 41 个页面", "night", "P0503")],
                cta_title="发现内容错误或有合作意向？", cta_desc="提交反馈时附上页面链接与复现步骤，我们会在 2 个工作日内回复。",
                cta_btn="联系与反馈", cta_target="P0502"),
}


def build(code):
    return channel(CHANNELS[code])


BUILDERS = {k: (lambda c=k: build(c)) for k in CHANNELS}
