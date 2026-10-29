# -*- coding: utf-8 -*-
"""L3 页面 · 下载中心（P0201–P0205）"""
from ds import *
from blocks import (cover_card, filter_row, page_head, pager, row_card, section_banner,
                    side_download, spec_table, tag_pill)


def launchers():
    p = [page_strip("P0201", "启动器下载", "L3", "DOWNLOAD / LAUNCHER COMPARE"), topbar("下载中心", 30)]
    p.append(breadcrumb(118, ["首页", "下载中心", "启动器下载"], "面包屑回溯 R2"))
    p.append(page_head(170, "DOWNLOAD / LAUNCHER", "启动器下载",
                       "官方启动器、HMCL、PCL2 横向对比：支持平台、Java 依赖、模组管理与更新频率。",
                       right=[("3", "款启动器"), ("4.6", "平均评分")]))
    y = 384
    p.append(sec_head(CX, y, "01", "横向对比", "COMPARE", "数据更新于 2024-06-12"))
    y += 56
    heads = ["启动器", "支持平台", "Java", "模组管理", "适合人群", "评分"]
    offs = [0, 200, 360, 470, 690, 930]
    p.append(r(CX, y, CW, 44, INK))
    for hd, off in zip(heads, offs):
        p.append(t(CX + 20 + off, y + 28, hd, 11, "#C9D6BE", 700))
    rows = [("官方启动器", "Win / macOS", "内置", "基础", "正版玩家", "4.2"),
            ("HMCL", "Win / macOS / Linux", "自动检测", "完整", "模组 / 整合包玩家", "4.8"),
            ("PCL2", "Windows", "自动下载", "完整", "低配 / 中文用户", "4.7")]
    for i, row in enumerate(rows):
        yy = y + 44 + i * 80
        seg = [r(CX, yy, CW, 80, CARD if i % 2 == 0 else PAPER)]
        seg.append(ln(CX, yy + 80, CX + CW, yy + 80, LINE))
        seg.append(t(CX + 20, yy + 34, row[0], 20, INK, 800))
        seg.append(t(CX + 20, yy + 56, ["launcher-detail.html?name=official", "launcher-detail.html?name=hmcl", "launcher-detail.html?name=pcl2"][i], 10, MUT2, 400, family=MONO))
        seg.append(t(CX + 220, yy + 44, row[1], 12, MUT))
        seg.append(t(CX + 380, yy + 44, row[2], 12, MUT))
        seg.append(t(CX + 490, yy + 44, row[3], 12, GREEN_TEXT if False else INK, 700))
        seg.append(t(CX + 710, yy + 44, row[4], 12, MUT))
        seg.append(t(CX + 950, yy + 44, row[5], 20, GRASS_D, 800, family=MONO))
        seg.append(t(CX + CW - 20, yy + 52, "详情 →", 12, GRASS_D, 700, "end"))
        p.append(link("P020101", "".join(seg)))
    y = y + 44 + 3 * 80
    p.append(r(CX, y, CW, 60, GRASS_SOFT))
    p.append(icon(CX + 20, y + 20, "check", GRASS_D, 18))
    p.append(t(CX + 48, y + 26, "推荐：第一次装模组选 HMCL；只有 Windows 且偏好中文界面可选 PCL2。", 12, GRASS_D, 700))
    p.append(t(CX + 48, y + 46, "三款启动器都需要单独安装 Java 17（1.20.1 模组环境）。", 11, MUT))
    y += 60
    # 下载卡片
    p.append(sec_head(CX, y + 56, "02", "下载入口", "DOWNLOADS", "官方源 · 已校验签名"))
    cw3 = (CW - 2 * 24) / 3
    items = [("官方启动器", "官方 / OFFICIAL", "Win / macOS · 需正版账号", "forest", "P020101", "4.2"),
             ("HMCL 启动器", "开源 / OPEN SOURCE", "Win / macOS / Linux · 离线可玩", "village", "P020101", "4.8"),
             ("PCL2 启动器", "中文 / WINDOWS", "Windows · 自动下载 Java", "night", "P020101", "4.7")]
    for i, (nm, cat, meta, var, tg, sc) in enumerate(items):
        p.append(cover_card(CX + i * (cw3 + 24), y + 112, cw3, 360, nm, cat, meta, var, tg,
                            tag="★ " + sc, footer_left="v 3.5.3"))
    y = y + 112 + 360
    p.append(footer(y + 60, "P0201 / L3"))
    return W, y + 380, "".join(p), "官方 / HMCL / PCL2 横向对比"


def modpacks():
    p = [page_strip("P0202", "整合包获取", "L3", "DOWNLOAD / MODPACK"), topbar("下载中心", 30)]
    p.append(breadcrumb(118, ["首页", "下载中心", "整合包获取"], "面包屑回溯 R2"))
    p.append(page_head(170, "DOWNLOAD / MODPACK", "整合包获取",
                       "按分类、热度与版本筛选整合包；详情页给出完整 MOD 清单与安装步骤。",
                       right=[("428", "个整合包"), ("120+", "MOD 规模")]))
    y = 384
    p.append(filter_row(y, [("分类", ["全部", "冒险", "科技", "生活", "硬核"]),
                            ("版本", ["全部", "1.20.1", "1.19.2", "1.18.2"])], "共 428 个整合包 · 按热度排序"))
    y = 464
    packs = [("Better MC [FORGE]", "冒险 / ADVENTURE", "1.20.1 · 120+ MOD · 4.4 分", "forest", "P020201", "热门", "120+ MOD"),
             ("Create: Astral", "科技 / TECH", "1.18.2 · 200+ MOD · 4.7 分", "village", "P020201", "硬核", "200+ MOD"),
             ("DawnCraft", "冒险 / RPG", "1.18.2 · 350+ MOD · 4.6 分", "night", "P020201", "大型", "350+ MOD"),
             ("All the Mods 9", "综合 / KITCHEN SINK", "1.20.1 · 400+ MOD · 4.5 分", "ocean", "P020201", "综合", "400+ MOD"),
             ("FTB Skies", "空岛 / SKYBLOCK", "1.20.1 · 180+ MOD · 4.3 分", "forest", "P020201", "空岛", "180+ MOD"),
             ("RLCraft", "硬核 / HARDCORE", "1.12.2 · 160+ MOD · 4.2 分", "nether", "P020201", "高难", "160+ MOD"),
             ("Better MC [FABRIC]", "冒险 / ADVENTURE", "1.20.1 · 90+ MOD · 4.3 分", "village", "P020201", "轻量", "90+ MOD"),
             ("Medieval MC", "生活 / BUILD", "1.20.1 · 110+ MOD · 4.4 分", "forest", "P020201", "建筑", "110+ MOD"),
             ("Prominence II", "冒险 / RPG", "1.20.1 · 200+ MOD · 4.8 分", "ocean", "P020201", "评分最高", "200+ MOD")]
    cw3 = (CW - 2 * 24) / 3
    for i, (nm, cat, meta, var, tg, tag, foot) in enumerate(packs):
        row, col = divmod(i, 3)
        p.append(cover_card(CX + col * (cw3 + 24), y + row * 366, cw3, 340, nm, cat, meta, var, tg,
                            tag=tag, footer_left=foot))
    y = y + 3 * 366
    p.append(pager(y + 10, 6, 1))
    y += 66
    p.append(section_banner(y + 20, "不会装整合包？", "启动器导入 + 选择 Java + 分配内存，三步完成；详情页有完整步骤。",
                            "查看安装教程", "P0103", 150))
    y += 170
    p.append(footer(y + 40, "P0202 / L3"))
    return W, y + 340, "".join(p), "分类 / 热度 / 版本筛选"


def mods():
    p = [page_strip("P0203", "MOD 下载", "L3", "DOWNLOAD / MOD LIBRARY"), topbar("下载中心", 30)]
    p.append(breadcrumb(118, ["首页", "下载中心", "MOD 下载"], "面包屑回溯 R2"))
    p.append(page_head(170, "DOWNLOAD / MOD", "MOD 下载",
                       "按分类与版本筛选；涉及前置依赖的 MOD 会在卡片与详情页双重标注。",
                       right=[("1,286", "个 MOD"), ("12", "今日更新")]))
    y = 384
    p.append(filter_row(y, [("分类", ["全部", "科技", "冒险", "装饰", "优化"]),
                            ("加载器", ["全部", "Forge", "Fabric", "NeoForge"])], "共 1,286 个 MOD · 前置校验已开启"))
    y = 464
    mods_list = [("Create 机械动力", "科技 / TECH", "1.20.1 · Forge · 前置 Flywheel", "village", "P020301", "前置 1"),
                 ("JEI 物品管理器", "优化 / UTILITY", "1.20.1 · Forge / Fabric · 无前置", "ocean", "P020301", "必装"),
                 ("Farmer's Delight", "生活 / FOOD", "1.20.1 · Forge · 无前置", "forest", "P020301", "美食"),
                 ("JourneyMap", "优化 / MAP", "1.20.1 · Forge / Fabric · 无前置", "night", "P020301", "地图"),
                 ("Twilight Forest", "冒险 / DIMENSION", "1.20.1 · Forge · 无前置", "forest", "P020301", "维度"),
                 ("Iris Shaders", "优化 / RENDER", "1.20.1 · Fabric · 需 Sodium", "ocean", "P020301", "光影"),
                 ("Sodium", "优化 / PERF", "1.20.1 · Fabric · 无前置", "village", "P020301", "帧率"),
                 ("AE2 应用能源", "科技 / STORAGE", "1.20.1 · Forge · 前置 GuideME", "night", "P020301", "前置 1"),
                 ("Mekanism", "科技 / TECH", "1.20.1 · Forge · 无前置", "village", "P020301", "能源"),
                 ("Biomes O' Plenty", "世界 / WORLDGEN", "1.20.1 · Forge · 无前置", "forest", "P020301", "地形"),
                 ("Waystones", "生活 / TRAVEL", "1.20.1 · Forge · 无前置", "ocean", "P020301", "传送"),
                 ("AppleSkin", "优化 / HUD", "1.20.1 · Forge / Fabric · 无前置", "night", "P020301", "HUD")]
    cw4 = (CW - 3 * 24) / 4
    for i, (nm, cat, meta, var, tg, tag) in enumerate(mods_list):
        row, col = divmod(i, 4)
        p.append(cover_card(CX + col * (cw4 + 24), y + row * 352, cw4, 326, nm, cat, meta, var, tg,
                            tag=tag, footer_left="1.20.1"))
    y = y + 3 * 352
    p.append(r(CX, y + 6, CW, 70, AMBER_SOFT))
    p.append(r(CX, y + 6, 4, 70, AMBER))
    p.append(icon(CX + 20, y + 30, "link", "#8A6416", 20))
    p.append(t(CX + 50, y + 36, "前置依赖提示：带「前置」标签的 MOD 需先安装依赖，详情页可一键跳转。", 12, "#8A6416", 700))
    p.append(t(CX + 50, y + 56, "版本不匹配是最常见的崩溃原因，下载前请确认游戏版本与加载器。", 11, MUT))
    y += 90
    p.append(pager(y, 6, 1))
    y += 60
    p.append(footer(y + 20, "P0203 / L3"))
    return W, y + 320, "".join(p), "分类 / 版本筛选 / 前置提示"


def resources():
    p = [page_strip("P0204", "资源包与光影", "L3", "DOWNLOAD / RESOURCE PACK · SHADER"), topbar("下载中心", 30)]
    p.append(breadcrumb(118, ["首页", "下载中心", "资源包与光影"], "面包屑回溯 R2"))
    p.append(page_head(170, "DOWNLOAD / RESOURCE", "资源包与光影",
                       "资源包改变材质，光影改变光照；两者叠加前先确认配置是否撑得住。",
                       right=[("246", "个资源"), ("中配", "推荐配置")]))
    y = 384
    tabs = [("资源包 / RESOURCE PACK", True), ("光影 / SHADER", False), ("整合预设", False)]
    x = CX
    for i, (lb, on) in enumerate(tabs):
        w = len(lb) * 11 + 36
        p.append(r(x, y, w, 42, INK if on else CARD, None if on else LINE, 1))
        p.append(t(x + w / 2, y + 27, lb, 12, GRASS_L if on else MUT, 700 if on else 400, "middle"))
        x += w + 10
    y = 452
    p.append(sec_head(CX, y, "01", "热门资源包", "RESOURCE PACKS", "16× 与 32× 混合 · 适配 1.20.1"))
    y += 56
    packs = [("Stay True", "写实 / REALISTIC", "16× · 1.20.1 · 4.7 分", "forest", "P020401", "16×"),
             ("Better Leaves", "自然 / NATURE", "16× · 树叶优化 · 4.5 分", "village", "P020401", "16×"),
             ("Mizuno's 16", "清新 / CLEAN", "16× · 低配友好 · 4.6 分", "ocean", "P020401", "低配"),
             ("Pixel Perfection", "像素 / PIXEL", "16× · 原版风 · 4.4 分", "night", "P020401", "像素")]
    cw4 = (CW - 3 * 24) / 4
    for i, (nm, cat, meta, var, tg, tag) in enumerate(packs):
        p.append(cover_card(CX + i * (cw4 + 24), y, cw4, 320, nm, cat, meta, var, tg, tag=tag, footer_left="16×"))
    y += 320
    p.append(sec_head(CX, y + 60, "02", "热门光影", "SHADERS", "需 Iris / OptiFine · 按配置选择"))
    y += 116
    shaders = [("Complementary", "光影 / BALANCED", "中配可跑 · 4.8 分", "ocean", "P020401", "均衡"),
               ("BSL Shaders", "光影 / STYLIZED", "中高配 · 4.6 分", "village", "P020401", "风格化"),
               ("Photon", "光影 / REALISTIC", "高配 · 4.5 分", "night", "P020401", "写实"),
               ("Solas", "光影 / LIGHT", "低配可跑 · 4.2 分", "forest", "P020401", "轻量")]
    for i, (nm, cat, meta, var, tg, tag) in enumerate(shaders):
        p.append(cover_card(CX + i * (cw4 + 24), y, cw4, 320, nm, cat, meta, var, tg, tag=tag, footer_left="Iris"))
    y += 340
    p.append(r(CX, y + 10, CW, 64, PAPER2))
    p.append(t(CX + 24, y + 34, "配置提示：光影对显卡要求高，集显建议先用「Solas」或关闭阴影。", 12, MUT))
    p.append(t(CX + 24, y + 54, "资源包与光影可叠加，但 32× 以上材质会明显增加显存占用。", 11, MUT2))
    y += 94
    p.append(footer(y, "P0204 / L3"))
    return W, y + 320, "".join(p), "资源包 / 光影分区"


def nettools():
    p = [page_strip("P0205", "联机与语音工具下载", "L3", "DOWNLOAD / NETWORK & VOICE"), topbar("下载中心", 30)]
    p.append(breadcrumb(118, ["首页", "下载中心", "联机与语音工具"], "面包屑回溯 R2"))
    p.append(page_head(170, "DOWNLOAD / NET TOOLS", "联机与语音工具",
                       "联机工具负责连得上，语音工具负责聊得清；按平台、人数与延迟选择。",
                       right=[("6", "款工具"), ("全平台", "覆盖")]))
    y = 384
    p.append(sec_head(CX, y, "01", "联机工具", "NETWORK", "房间码 / 直连 / 服务器列表"))
    y += 56
    nets = [("SakuraFrp", "内网穿透 / TUNNEL", "全平台 · 免费额度 · 延迟 30–80ms", "village", "P020501", "免费"),
            ("Radmin LAN", "虚拟局域网 / LAN", "Windows · 最多 10 人 · 延迟 20ms", "forest", "P020501", "低延迟"),
            ("Playit.gg", "隧道 / TUNNEL", "全平台 · 免配置 · 支持基岩版", "ocean", "P020501", "免配置")]
    cw3 = (CW - 2 * 24) / 3
    for i, (nm, cat, meta, var, tg, tag) in enumerate(nets):
        p.append(cover_card(CX + i * (cw3 + 24), y, cw3, 330, nm, cat, meta, var, tg, tag=tag, footer_left="NET"))
    y += 330
    p.append(sec_head(CX, y + 60, "02", "语音工具", "VOICE", "频道制 / 房间码 / 权限管理"))
    y += 116
    voices = [("KOOK", "语音 / CHANNELS", "全平台 · 频道制 · 免费", "night", "P020501", "频道"),
              ("YY 语音", "语音 / ROOMS", "Windows / 手机 · 房间制", "village", "P020501", "房间"),
              ("Discord", "语音 / COMMUNITY", "全平台 · 社区服务器 · 免费", "forest", "P020501", "社区")]
    for i, (nm, cat, meta, var, tg, tag) in enumerate(voices):
        p.append(cover_card(CX + i * (cw3 + 24), y, cw3, 330, nm, cat, meta, var, tg, tag=tag, footer_left="VOICE"))
    y += 350
    # 对比表
    p.append(sec_head(CX, y + 10, "03", "平台与人数对比", "MATRIX", "选择前先看这一张表"))
    y += 66
    p.append(spec_table(CX, y, CW,
                        [("SakuraFrp", "全平台 · 免费隧道", "不限人数"),
                         ("Radmin LAN", "Windows · 虚拟局域网", "10 人"),
                         ("Playit.gg", "全平台 · 免配置隧道", "不限人数"),
                         ("KOOK", "全平台 · 频道语音", "不限人数"),
                         ("YY 语音", "Windows / 手机 · 房间", "8 人 / 房间"),
                         ("Discord", "全平台 · 社区语音", "不限人数")],
                        ("工具", "形态", "人数"), (220, 480, 240))[0])
    y += 40 + 6 * 44 + 20
    p.append(footer(y, "P0205 / L3"))
    return W, y + 320, "".join(p), "联机工具 / 语音工具分组 + 平台与人数对比"


BUILDERS = {
    "P0201": launchers,
    "P0202": modpacks,
    "P0203": mods,
    "P0204": resources,
    "P0205": nettools,
}
