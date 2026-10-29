# -*- coding: utf-8 -*-
"""L4 / L5 页面 · 详情与内容"""
from ds import *
from blocks import (cover_card, detail_title, filter_row, page_head, pager, related,
                    row_card, section_banner, side_download, spec_table, tag_pill,
                    cover_panel, feature_grid, steps_list)
from pages_l3 import article_page


def detail(cfg):
    code, name, active = cfg["code"], cfg["name"], cfg["active"]
    p = [page_strip(code, name, cfg.get("level", "L4"), cfg.get("strip", "")), topbar(active, 30)]
    p.append(breadcrumb(118, cfg["crumb"], "面包屑回溯 R2 · 返回列表保持上下文"))
    p.append(detail_title(170, cfg["kicker"], cfg["title"], cfg["meta"], cfg.get("chips", ()), cfg.get("rating")))
    y = 420
    LX, LW = CX, 780
    RX = CX + 820
    p.append(cover_panel(LX, y, LW, 360, cfg.get("var", "forest"), cfg.get("cover_label", ""), cfg.get("cover_meta", ""), cfg.get("cover_tag", "")))
    # 简介
    iy = y + 400
    p.append(t(LX, iy, "简介", 20, INK, 800))
    p.append(ln(LX, iy + 14, LX + LW, iy + 14, LINE2))
    paras = cfg.get("paras", [])
    yy = iy + 44
    for s in paras:
        p.append(para(LX, yy, s, 14, MUT, 26, LW))
        yy += 26 * len(wrap(s, 14, LW)) + 12
    # 模块
    for m in cfg.get("modules", []):
        yy += 20
        if m[0] == "features":
            p.append(t(LX, yy, m[1], 20, INK, 800))
            p.append(ln(LX, yy + 14, LX + LW, yy + 14, LINE2))
            block, yend = feature_grid(LX, yy + 30, LW, m[2], m[3] if len(m) > 3 else 2)
            p.append(block)
            yy = yend
        elif m[0] == "steps":
            p.append(t(LX, yy, m[1], 20, INK, 800))
            p.append(ln(LX, yy + 14, LX + LW, yy + 14, LINE2))
            block, yend = steps_list(LX, yy + 34, LW, m[2])
            p.append(block)
            yy = yend
        elif m[0] == "table":
            p.append(t(LX, yy, m[1], 20, INK, 800))
            p.append(ln(LX, yy + 14, LX + LW, yy + 14, LINE2))
            block, yend = spec_table(LX, yy + 30, LW, m[3], m[2], m[4] if len(m) > 4 else (180, 380, 200))
            p.append(block)
            yy = yend
        elif m[0] == "note":
            p.append(r(LX, yy, LW, 54, GRASS_SOFT))
            p.append(r(LX, yy, 4, 54, GRASS))
            p.append(t(LX + 24, yy + 32, m[1], 12, GRASS_D, 700))
            yy += 70
    # 右侧下载
    p.append(side_download(y, cfg.get("side", {})))
    yend = max(yy, y + 470)
    block, ry = related(yend + 50, cfg.get("related", []))
    p.append(block)
    p.append(footer(ry + 40, f"{code} / L4"))
    return W, ry + 340, "".join(p), cfg["meta"]


# ---------- 版本详情 ----------
def version_detail():
    return detail(dict(
        code="P010201", name="版本详情", active="认识 MC", level="L4",
        strip="GUIDE / VERSION 1.20.1",
        crumb=["首页", "认识 MC", "版本与玩法", "版本详情"],
        kicker="VERSION / 1.20.1 · RELEASE",
        title="Minecraft 1.20.1",
        meta="正式版 · 发布于 2023-06-12 · Java Edition · 支持 Windows / macOS / Linux",
        chips=("Java 版", "正式版", "模组生态最完整"),
        rating=("4.8", "1,286 次下载"),
        var="village",
        cover_label="1.20.1 · 村庄与掠夺更新", cover_meta="RELEASE / 2023-06-12", cover_tag="推荐版本",
        paras=["1.20.1 是目前模组与整合包生态最完整的正式版本。绝大多数整合包、光影与服务器都以此版本为基准，适合作为长期游玩与开服的首选。",
               "该版本以「村庄与掠夺」为主题，新增樱花生物群系、嗅探兽与考古系统，同时保留了 1.20 的内容更新。"],
        modules=[
            ("features", "版本特性", [("cube", "樱花生物群系", "新增樱花木与粉色花海"), ("book", "考古系统", "可疑沙砾与陶片"),
                                      ("shield", "村庄与掠夺", "村民交易与袭击机制"), ("grid", "性能优化", "区块加载与光照修复")], 2),
            ("table", "版本信息", ("项目", "说明", "备注"),
             [("版本号", "1.20.1", "正式版"), ("发布时间", "2023-06-12", "Mojang"), ("Java 要求", "Java 17", "必须"),
              ("模组加载器", "Forge / Fabric", "推荐 Forge 47.x"), ("推荐内存", "4–6 GB", "大型整合包 8 GB")],
             (180, 380, 180)),
            ("steps", "安装步骤", [("安装 Java 17", "从 Adoptium 下载并安装，确认 java -version"), ("安装启动器", "HMCL 或 PCL2，选择 1.20.1 版本"),
                                  ("分配内存", "在启动器设置中分配 4–6 GB"), ("安装模组", "按需安装 Forge / Fabric 与 MOD")]),
            ("note", "版本详情页固定提供启动器下载与整合包详情出口，形成「看 → 拿 → 装」闭环（R5）。"),
        ],
        side=dict(title="获取此版本", en="GET VERSION 1.20.1", version="1.20.1 · Java Edition",
                  rows=[("支持平台", "Win / macOS / Linux"), ("安装包大小", "1.2 GB"), ("Java", "17"),
                        ("来源", "官方启动器")],
                  btn="下载服务端", btn2="查看安装说明", target="P020101",
                  note="已校验官方签名 · 更新于 2023-06-12"),
        related=[("HMCL 启动器", "启动器", "支持 1.20.1 · 开源免费", "village", "P020101"),
                 ("Better MC 整合包", "整合包", "1.20.1 · 120+ MOD", "forest", "P020201"),
                 ("新手入门教程", "教程", "从第一夜开始", "night", "P0103"),
                 ("Java 版本指南", "FAQ", "启动崩溃排查", "ocean", "P010401")],
    ))


# ---------- 启动器详情 ----------
def launcher_detail():
    return detail(dict(
        code="P020101", name="启动器详情", active="下载中心", level="L4",
        strip="DOWNLOAD / LAUNCHER · HMCL",
        crumb=["首页", "下载中心", "启动器下载", "启动器详情"],
        kicker="LAUNCHER / HMCL 3.5.3",
        title="HMCL 启动器",
        meta="开源免费 · 支持 Windows / macOS / Linux · 更新于 2024-06-12",
        chips=("开源", "离线登录", "模组管理"),
        rating=("4.8", "286,400 次下载"),
        var="forest",
        cover_label="HMCL · 跨平台启动器", cover_meta="OPEN SOURCE / v3.5.3", cover_tag="编辑推荐",
        paras=["HMCL 是目前中文社区使用最广的开源启动器：自动检测 Java、支持离线登录、内置整合包导入与模组管理，Windows / macOS / Linux 都能用。",
               "它不绑定正版账号，适合离线游玩与整合包测试；如需联机到正版服务器，仍建议使用正版登录。"],
        modules=[
            ("features", "核心能力", [("download", "整合包导入", "拖入压缩包即可安装"), ("grid", "版本隔离", "每个实例独立配置"),
                                      ("shield", "离线登录", "无需正版账号即可启动"), ("link", "下载源切换", "国内镜像加速")], 2),
            ("table", "配置要求", ("项目", "最低", "推荐"),
             [("系统", "Windows 7 / macOS 10.13", "Windows 10 / macOS 12+"), ("Java", "Java 8", "Java 17"),
              ("内存", "2 GB", "4–8 GB"), ("磁盘", "200 MB", "1 GB / 每个实例")],
             (180, 300, 300)),
            ("steps", "安装与首次启动", [("下载 HMCL", "选择对应平台的安装包"), ("安装 Java 17", "HMCL 可自动下载"),
                                         ("登录账号", "正版或离线模式"), ("导入整合包", "拖入 .zip 自动安装")]),
            ("note", "下载页固定展示版本、兼容性与来源；本页为启动器详情的统一模板。"),
        ],
        side=dict(title="下载 HMCL", en="GET LAUNCHER", version="v3.5.3 · 全平台",
                  rows=[("支持平台", "Win / macOS / Linux"), ("安装包大小", "32 MB"), ("Java", "8 / 17"),
                        ("来源", "GitHub Releases")],
                  btn="立即下载", btn2="查看安装说明", target="P020101",
                  note="开源项目 · 已校验 SHA256"),
        related=[("PCL2 启动器", "启动器", "Windows · 自动下载 Java", "night", "P020101"),
                 ("Better MC 整合包", "整合包", "1.20.1 · 120+ MOD", "forest", "P020201"),
                 ("版本详情 1.20.1", "版本", "Java 17 · 正式版", "village", "P010201"),
                 ("启动失败 FAQ", "FAQ", "Java 版本不匹配", "ocean", "P010401")],
    ))


# ---------- 整合包详情 ----------
def modpack_detail():
    return detail(dict(
        code="P020201", name="整合包详情", active="下载中心", level="L4",
        strip="DOWNLOAD / MODPACK · BETTER MC",
        crumb=["首页", "下载中心", "整合包获取", "整合包详情"],
        kicker="MODPACK / BETTER MC [FORGE]",
        title="Better MC [FORGE]",
        meta="1.20.1 · Forge · 120+ MOD · 更新于 2024-06-12",
        chips=("冒险", "Forge", "120+ MOD"),
        rating=("4.4", "86,200 次下载"),
        var="village",
        cover_label="Better MC · 冒险整合包", cover_meta="FORGE / 1.20.1", cover_tag="本周热门",
        paras=["Better MC 是面向冒险与探索的整合包：在保留原版节奏的前提下，加入新的生物群系、地牢、任务线与装饰方块，适合第一次接触整合包的玩家。",
               "整合包已预配置光影与优化模组，开箱即可游玩；低配设备建议关闭光影并分配 6 GB 内存。"],
        modules=[
            ("features", "整合包特性", [("cube", "新生物群系", "30+ 地形与结构"), ("book", "任务线", "轻量引导，不强制"),
                                      ("shield", "优化预配置", "Sodium / Iris 已调优"), ("grid", "120+ MOD", "冒险 / 装饰 / 优化")], 2),
            ("table", "MOD 清单（部分）", ("MOD", "版本", "作用"),
             [("Create 机械动力", "0.5.1", "机械与自动化"), ("Farmer's Delight", "1.2.3", "农业与食物"),
              ("JourneyMap", "5.9.7", "小地图"), ("JEI", "15.2.0", "物品查询")],
             (300, 220, 220)),
            ("steps", "安装步骤", [("安装启动器", "HMCL / PCL2 任选"), ("导入整合包", "启动器内选择 .zip 导入"),
                                  ("分配内存", "建议 6 GB 以上"), ("首次启动", "等待 3–5 分钟加载")]),
            ("note", "整合包详情必须提供启动器下载、MOD 详情与视频攻略出口（R4 / R5）。"),
        ],
        side=dict(title="下载整合包", en="GET MODPACK", version="1.20.1 · Forge 47.2.0",
                  rows=[("整合包大小", "268 MB"), ("MOD 数量", "120+"), ("内存建议", "6 GB"),
                        ("来源", "CurseForge")],
                  btn="立即下载", btn2="查看 MOD 清单", target="P020201",
                  note="已通过病毒扫描 · 更新于 2024-06-12"),
        related=[("HMCL 启动器", "启动器", "导入整合包 · 全平台", "forest", "P020101"),
                 ("Create 机械动力", "MOD", "前置 Flywheel", "night", "P020301"),
                 ("机械动力全流程", "视频", "18 集 · 7.2 万播放", "ocean", "P040101"),
                 ("Complementary 光影", "光影", "中配可跑", "village", "P020401")],
    ))


# ---------- MOD 详情 ----------
def mod_detail():
    return detail(dict(
        code="P020301", name="MOD 详情", active="下载中心", level="L4",
        strip="DOWNLOAD / MOD · CREATE",
        crumb=["首页", "下载中心", "MOD 下载", "MOD 详情"],
        kicker="MOD / CREATE 0.5.1",
        title="Create 机械动力",
        meta="1.20.1 · Forge · 前置 Flywheel · 更新于 2024-06-12",
        chips=("科技", "Forge", "前置 1"),
        rating=("4.9", "142,800 次下载"),
        var="night",
        cover_label="Create · 机械动力", cover_meta="FORGE / 1.20.1", cover_tag="必装",
        paras=["Create 把机械与工程带进 Minecraft：齿轮、传动轴、机械臂与传送带可以组合成完整的自动化产线，同时保持原版的视觉风格。",
               "本 MOD 需要前置 Flywheel 提供渲染支持；与 OptiFine 存在兼容问题，建议改用 Iris + Sodium。"],
        modules=[
            ("features", "核心玩法", [("grid", "动力系统", "齿轮 / 传动轴 / 马达"), ("download", "自动化产线", "传送带与机械臂"),
                                      ("cube", "列车系统", "轨道与车厢"), ("shield", "兼容提示", "需 Flywheel 前置")], 2),
            ("table", "版本与依赖", ("项目", "要求", "说明"),
             [("游戏版本", "1.20.1", "Forge 47.x"), ("前置 MOD", "Flywheel 0.6.11", "必装"),
              ("不兼容", "OptiFine", "改用 Iris"), ("推荐内存", "4 GB", "大型产线 6 GB")],
             (180, 320, 260)),
            ("steps", "安装步骤", [("安装 Forge", "1.20.1 · 47.2.0"), ("安装前置", "Flywheel 放入 mods"),
                                  ("安装本体", "Create 放入 mods"), ("启动验证", "创造模式测试齿轮")]),
            ("note", "MOD 详情必须列出前置依赖并可继续跳转（R5）；前置缺失是最常见的崩溃原因。"),
        ],
        side=dict(title="下载 MOD", en="GET MOD", version="0.5.1 · Forge",
                  rows=[("文件大小", "38 MB"), ("前置", "Flywheel"), ("游戏版本", "1.20.1"),
                        ("来源", "CurseForge")],
                  btn="立即下载", btn2="下载前置 Flywheel", target="P020301",
                  note="已校验文件哈希 · 更新于 2024-06-12"),
        related=[("Flywheel 前置", "前置 MOD", "渲染支持 · 必装", "village", "P020301"),
                 ("Better MC 整合包", "整合包", "已内置 Create", "forest", "P020201"),
                 ("机械动力全流程", "视频", "18 集 · 7.2 万播放", "ocean", "P040101"),
                 ("MOD 冲突排查", "FAQ", "崩溃日志解读", "night", "P010401")],
    ))


# ---------- 资源详情 ----------
def resource_detail():
    return detail(dict(
        code="P020401", name="资源详情", active="下载中心", level="L4",
        strip="DOWNLOAD / SHADER · COMPLEMENTARY",
        crumb=["首页", "下载中心", "资源包与光影", "资源详情"],
        kicker="SHADER / COMPLEMENTARY r5.2",
        title="Complementary 光影",
        meta="需 Iris / OptiFine · 中配可跑 · 更新于 2024-06-12",
        chips=("光影", "均衡", "中配"),
        rating=("4.8", "128,600 次下载"),
        var="ocean",
        cover_label="Complementary · 均衡光影", cover_meta="IRIS / r5.2", cover_tag="编辑推荐",
        paras=["Complementary 是兼顾画面与性能的均衡型光影：默认配置下保留清晰的水面反射与柔和阴影，中端显卡即可稳定 60 FPS。",
               "提供五个预设（Potato / Low / Medium / High / Ultra），可在游戏内直接切换，不需要手动改配置文件。"],
        modules=[
            ("features", "画面特性", [("cube", "水体反射", "屏幕空间反射"), ("star", "体积光", "日出与日落"),
                                      ("shield", "性能预设", "五档一键切换"), ("grid", "天气效果", "雨雪与雾")], 2),
            ("table", "配置要求", ("档位", "显卡", "预期帧率"),
             [("Potato", "GTX 1050", "60 FPS"), ("Medium", "GTX 1660", "60 FPS"),
              ("High", "RTX 3060", "60 FPS"), ("Ultra", "RTX 4070+", "60 FPS")],
             (180, 300, 260)),
            ("steps", "安装步骤", [("安装 Iris", "Fabric 环境推荐 Iris"), ("放入光影包", "shaderpacks 文件夹"),
                                  ("选择光影", "视频设置 → 光影"), ("调整预设", "按显卡选择档位")]),
            ("note", "光影与资源包可叠加；32× 以上材质会明显增加显存占用。"),
        ],
        side=dict(title="下载光影", en="GET SHADER", version="r5.2 · Iris / OptiFine",
                  rows=[("文件大小", "12 MB"), ("推荐显卡", "GTX 1660+"), ("游戏版本", "1.20.1"),
                        ("来源", "GitHub Releases")],
                  btn="立即下载", btn2="查看配置说明", target="P020401",
                  note="已校验文件哈希 · 更新于 2024-06-12"),
        related=[("BSL Shaders", "光影", "风格化 · 中高配", "village", "P020401"),
                 ("资源包 Stay True", "资源包", "16× · 写实", "forest", "P0204"),
                 ("光影配置 FAQ", "FAQ", "帧数优化", "night", "P010401"),
                 ("整合包推荐", "整合包", "已预配置光影", "ocean", "P0202")],
    ))


# ---------- 工具详情 ----------
def tool_detail():
    return detail(dict(
        code="P020501", name="工具详情", active="下载中心", level="L4",
        strip="DOWNLOAD / VOICE · KOOK",
        crumb=["首页", "下载中心", "联机与语音工具", "工具详情"],
        kicker="TOOL / KOOK VOICE",
        title="KOOK 语音",
        meta="频道制 · 全平台 · 免费 · 更新于 2024-06-12",
        chips=("语音", "频道", "全平台"),
        rating=("4.6", "96,400 次下载"),
        var="forest",
        cover_label="KOOK · 频道语音", cover_meta="VOICE / ALL PLATFORM", cover_tag="开黑必备",
        paras=["KOOK 采用频道制结构：一个服务器下可分多个语音频道，适合固定车队与大型社区；支持文字、语音与屏幕分享。",
               "免费版即可满足日常联机需求；国内网络直连，延迟通常低于 60ms。"],
        modules=[
            ("features", "功能说明", [("video", "频道语音", "多人同时在线"), ("link", "房间码", "一键加入"),
                                      ("shield", "权限管理", "频道角色"), ("grid", "全平台", "Win / macOS / 手机")], 2),
            ("table", "平台支持", ("平台", "支持", "说明"),
             [("Windows", "✓", "客户端"), ("macOS", "✓", "客户端"), ("iOS / Android", "✓", "移动端"),
              ("网页版", "✓", "无需安装")],
             (200, 200, 320)),
            ("steps", "配置流程", [("创建服务器", "命名并选择模板"), ("创建语音频道", "设置人数与权限"),
                                  ("邀请队友", "分享房间码"), ("开始联机", "与游戏同步启动")]),
            ("note", "工具详情页固定提供服务器与整合包出口，方便「聊天 → 开服 → 进服」链路。"),
        ],
        side=dict(title="下载 KOOK", en="GET VOICE TOOL", version="全平台 · 免费",
                  rows=[("支持平台", "Win / macOS / 手机"), ("房间人数", "不限"), ("延迟", "30–60 ms"),
                        ("来源", "官方网站")],
                  btn="立即下载", btn2="查看联机教程", target="P020501",
                  note="官方源 · 无捆绑安装"),
        related=[("SakuraFrp", "联机工具", "内网穿透 · 免费", "village", "P020501"),
                 ("服务器与联机", "服务器", "86 个在线服", "ocean", "P0302"),
                 ("联机延迟优化", "文章", "6 分钟阅读", "forest", "P040201"),
                 ("联机工具配置", "视频", "9 集 · 4.6 万播放", "night", "P040101")],
    ))


# ---------- 教程详情 ----------
def tutorial_detail():
    return article_page(dict(
        code="P010301", name="教程详情", active="认识 MC", level="L4",
        strip="GUIDE / TUTORIAL · FIRST NIGHT",
        crumb=["首页", "认识 MC", "新手入门教程", "教程详情"],
        kicker="TUTORIAL 01 / FIRST NIGHT",
        title="第一夜生存清单",
        lead="难度 1 · 约 30 分钟 · 适用于 1.20.1 · 学完即可安全度过第一个夜晚。",
        meta="更新于 2024-06-12 · 作者 MC HUB 编辑部 · 已完成 12,860 次",
        stats=[("30", "分钟"), ("1", "难度等级")],
        toc=["出生点判断", "采集与合成", "庇护所", "第一夜清单"],
        sections=[
            ("h2", "一、出生点判断"),
            ("p", "进入世界后先环顾四周：优先选择靠近树林与水源的平地。按 F3 查看坐标，记下出生点，避免迷路。"),
            ("list", ["树林：提供原木与苹果，是第一夜的资源核心。",
                      "水源：方便后续耕种与躲避怪物。",
                      "避免沙漠与雪原：缺少木材，夜间温度与视野都不利。"]),
            ("h2", "二、采集与合成"),
            ("p", "徒手打 4–6 个原木，合成工作台、木镐与木剑；用木镐采集 12 个石头，升级为石镐、石剑与石斧。"),
            ("table", ("资源", "数量", "用途"),
             [("原木", "6", "工作台 / 工具"), ("石头", "12", "石制工具"), ("煤炭", "4", "火把"),
              ("生肉", "3", "食物")],
             (200, 160, 320)),
            ("h2", "三、庇护所"),
            ("p", "在天黑前挖一个 3×3 的洞穴或用泥土围出小屋，封顶并留一个进出口。放置工作台、箱子与床（需要 3 羊毛 + 3 木板）。"),
            ("steps", [("挖洞或围屋", "3×3 空间，高度 3 格"), ("封顶留门", "防止怪物生成"),
                       ("放置床", "3 羊毛 + 3 木板"), ("插火把", "照亮入口与内部")]),
            ("h2", "四、第一夜清单"),
            ("list", ["石制工具一套（镐 / 剑 / 斧）", "火把 ≥ 8 个", "食物 ≥ 3 份",
                      "床 1 张", "箱子 1 个（存放多余资源）"]),
            ("quote", "活过第一夜不需要战斗，只需要一盏灯和一个封顶的房间。"),
            ("note", "完成本教程后，建议继续「第一座庇护所」与「工具与矿物入门」。"),
        ]))


# ---------- 问题详情 ----------
def faq_detail():
    return article_page(dict(
        code="P010401", name="问题详情", active="认识 MC", level="L4",
        strip="GUIDE / FAQ · JAVA VERSION",
        crumb=["首页", "认识 MC", "常见问题", "问题详情"],
        kicker="FAQ / LAUNCH CRASH",
        title="游戏启动崩溃，日志提示 Java 版本不匹配怎么办？",
        lead="启动与安装 · 浏览 12,860 · 解决率 91% · 更新于 2024-06-12",
        meta="分类 启动与安装  ·  标签 Java / 崩溃 / 日志",
        stats=[("91%", "解决率"), ("12,860", "浏览")],
        toc=["确认报错", "检查 Java", "切换版本", "仍然崩溃"],
        sections=[
            ("h2", "一、确认报错"),
            ("p", "在崩溃日志（crash-reports 文件夹）中搜索「UnsupportedClassVersionError」或「Java version」。若出现 1.20.1 需要 Java 17 的提示，说明版本不匹配。"),
            ("h2", "二、检查 Java"),
            ("p", "打开终端执行 java -version，确认输出为 17.x。若为 8.x 或 11.x，需要安装 Java 17 并在启动器中指定路径。"),
            ("table", ("游戏版本", "最低 Java", "推荐"),
             [("1.20.x", "Java 17", "Java 17"), ("1.18–1.19", "Java 17", "Java 17"),
              ("1.16.5", "Java 8", "Java 8"), ("1.12.2", "Java 8", "Java 8")],
             (240, 200, 200)),
            ("h2", "三、切换版本"),
            ("steps", [("下载 Java 17", "Adoptium Temurin 17"), ("安装并记录路径", "例如 C:\\Program Files\\Java\\jdk-17"),
                       ("启动器指定 Java", "HMCL：设置 → Java → 手动选择"), ("重启启动器", "重新启动游戏验证")]),
            ("h2", "四、仍然崩溃"),
            ("p", "若 Java 版本正确仍崩溃，检查内存分配（建议 4–6 GB）、MOD 前置是否缺失，以及是否混用了 Forge 与 Fabric。"),
            ("note", "仍未解决？把 crash-reports 最新日志发到「帮助与反馈」板块，附上版本与 MOD 列表。"),
        ]))


# ---------- 文章详情 ----------
def article_detail():
    return article_page(dict(
        code="P040201", name="文章详情", active="攻略视频", level="L4",
        strip="GUIDES / ARTICLE · REDSTONE",
        crumb=["首页", "攻略视频", "图文攻略", "文章详情"],
        kicker="ARTICLE / REDSTONE 101",
        title="红石从零开始：门、灯与时钟",
        lead="红石 · 12 分钟阅读 · 更新于 2024-06-12 · 作者 Steve_Builder",
        meta="分类 红石  ·  标签 红石 / 逻辑门 / 时钟  ·  收藏 1,286",
        stats=[("3,286", "阅读"), ("4.8", "评分")],
        toc=["红石基础", "红石门", "红石灯", "时钟电路"],
        sections=[
            ("h2", "一、红石基础"),
            ("p", "红石粉传递信号，信号强度从 15 开始逐格衰减。红石火把、拉杆与按钮是最基础的信号源；中继器用于放大与延时。"),
            ("img", "night", "红石电路 · 夜间测试", "REDSTONE / NIGHT TEST"),
            ("h2", "二、红石门"),
            ("p", "用粘性活塞推动方块即可做门。把压力板接红石粉，再接到活塞，踩下即开门；中继器用于控制延时，避免门关得太快。"),
            ("steps", [("放置活塞", "门洞两侧各一个"), ("铺设红石", "压力板 → 红石粉 → 活塞"),
                       ("加中继器", "设置 2 档延时"), ("测试", "踩下压力板验证")]),
            ("h2", "三、红石灯"),
            ("p", "红石灯需要持续信号。用红石火把 + 拉杆做手动开关，或用侦测器做自动照明；注意红石灯不导能，需要方块中转。"),
            ("h2", "四、时钟电路"),
            ("p", "时钟电路用于周期性输出：两个中继器首尾相接形成循环，调整档位即可改变频率。常见用途是自动农场与闪烁灯。"),
            ("quote", "红石的本质是「信号 + 延时 + 逻辑」，先把这三件事拆开，再谈自动化。"),
            ("note", "下一篇：红石逻辑 20 讲 —— 从与门、或门到全自动农场。"),
        ]))


# ---------- 板块帖子列表 ----------
def board():
    p = [page_strip("P030101", "板块帖子列表", "L4", "COMMUNITY / BOARD · GENERAL"), topbar("社区交流", 30)]
    p.append(breadcrumb(118, ["首页", "社区交流", "论坛板块", "板块帖子列表"], "面包屑回溯 R2"))
    hy, hh = 170, 190
    p.append(r(0, hy, W, hh, INK))
    p.append(t(CX, hy + 62, "综合讨论区", 38, "#F4F8EC", 800))
    p.append(t(CX, hy + 100, "版本更新、整合包、服务器与技术话题", 13, "#A9B9A2"))
    p.append(t(CX, hy + 136, "主题 1,286  ·  帖 12,860  ·  今日 42", 11, GRASS_L, 400))
    p.append(link("P03010101", r(CX + CW - 150, hy + 74, 130, 44, GRASS) +
                  icon(CX + CW - 132, hy + 88, "plus", WHITE, 16) +
                  t(CX + CW - 106, hy + 102, "发布主题", 12, WHITE, 700)))
    y = 360
    p.append(r(CX, y, CW, 56, CARD, LINE, 1))
    p.append(t(CX + 20, y + 34, "置顶", 12, GRASS_D, 700))
    p.append(t(CX + 90, y + 34, "排序：最新回复 ∨", 12, MUT))
    p.append(t(CX + 240, y + 34, "筛选：全部 ∨", 12, MUT))
    p.append(t(CX + CW - 20, y + 34, "共 1,286 个主题", 11, MUT2, 400, "end"))
    y = 436
    p.append(t(CX, y + 20, "置顶主题", 14, INK, 800))
    pinned = [("【置顶】板块规则与发帖指南", "版主 · 置顶 · 12,860 浏览 · 236 回复"),
              ("【置顶】求助模板：日志、版本与截图", "版主 · 置顶 · 8,420 浏览 · 128 回复")]
    for i, (ti, meta) in enumerate(pinned):
        yy = y + 36 + i * 72
        seg = [r(CX, yy, CW, 62, GRASS_SOFT)]
        seg.append(r(CX, yy, 3, 62, GRASS))
        seg.append(t(CX + 20, yy + 26, ti, 14, INK, 800))
        seg.append(t(CX + 20, yy + 46, meta, 10, MUT))
        seg.append(t(CX + CW - 20, yy + 36, "置顶", 10, GRASS_D, 700, "end"))
        p.append(link("P03010101", "".join(seg)))
    y = y + 36 + 2 * 72 + 16
    p.append(t(CX, y + 16, "全部主题", 14, INK, 800))
    threads = [("【求助】1.20.1 整合包启动崩溃，日志如下", "Steve_Builder", "42", "1,286", "8 分钟前"),
               ("【分享】用 12000 个方块复刻主城", "Builder_A", "128", "3,420", "15 分钟前"),
               ("【教程】从零写一个数据包（附源码）", "Data_Pack", "36", "2,180", "22 分钟前"),
               ("【讨论】1.20.1 与 1.21 模组兼容性", "Modder", "64", "1,960", "31 分钟前"),
               ("【招募】周末生存服招新（1.20.1）", "Server_Owner", "18", "860", "45 分钟前"),
               ("【作品】樱花村庄建筑存档分享", "Architect", "96", "2,860", "1 小时前")]
    for i, (ti, author, rep, view, last) in enumerate(threads):
        yy = y + 40 + i * 72
        seg = [r(CX, yy, CW, 62, CARD, LINE, 1)]
        seg.append(avatar(CX + 18, yy + 14, 34, i))
        seg.append(t(CX + 68, yy + 26, ti, 13, INK, 700))
        seg.append(t(CX + 68, yy + 46, f"{author}  ·  {rep} 回复  ·  {view} 浏览", 10, MUT2))
        seg.append(t(CX + CW - 20, yy + 26, last, 10, MUT2, 400, "end"))
        seg.append(t(CX + CW - 20, yy + 46, "最后回复", 9, GRASS_D, 400, "end"))
        p.append(link("P03010101", "".join(seg)))
    y = y + 40 + 6 * 72
    p.append(pager(y + 10, 8, 1))
    y += 66
    p.append(footer(y, "P030101 / L4"))
    return W, y + 320, "".join(p), "置顶 / 排序 / 发帖入口"


# ---------- 帖子详情 ----------
def post():
    p = [page_strip("P03010101", "帖子详情", "L5", "COMMUNITY / POST · DEEPEST LEVEL"), topbar("社区交流", 30)]
    p.append(breadcrumb(118, ["首页", "社区交流", "论坛板块", "板块帖子列表", "帖子详情"], "第 5 层 · 面包屑完整回溯"))
    y = 170
    p.append(r(0, y, W, 210, PAPER))
    p.append(t(CX, y + 56, "综合讨论区 / 求助", 11, GRASS_D, 700, ls=1.0))
    p.append(t(CX, y + 108, "求助：1.20.1 整合包启动崩溃，日志如下", 34, INK, 800))
    p.append(t(CX, y + 144, "楼主 Steve_Builder  ·  2024-06-12 20:14  ·  128 浏览  ·  12 回复", 11, MUT))
    p.append(t(CX + CW, y + 144, "5 层最深处：首页 → 频道 → 栏目 → 列表 → 帖子", 10, MUT2, 400, "end"))
    y = 400
    LX, LW = CX, 800
    RX, RW = CX + 840, 360
    floors = [(0, "Steve_Builder", "楼主", "2024-06-12 20:14", ["HMCL 启动 1.20.1 整合包时直接崩溃，日志见下。已确认 Java 17，内存分配 6 GB。",
                                                              "整合包是 Better MC [FORGE]，没有额外装 MOD。"]),
              (1, "Modder", "2 楼", "2024-06-12 20:26", ["日志里有 Flywheel 版本冲突，Better MC 自带的 Create 需要 Flywheel 0.6.11。",
                                                          "先把 mods 里的 Flywheel 删掉，让整合包自己校验版本。"]),
              (2, "Helper", "3 楼", "2024-06-12 20:41", ["补充：如果是 HMCL，建议在「版本设置 → 高级」里把 Forge 版本固定为 47.2.0。",
                                                          "还不行就把 crash-reports 完整日志发出来。"])]
    fh = [352, 280, 280]
    fy = y
    for i, (idx, author, role, tm, lines) in enumerate(floors):
        yy = fy
        hh = fh[i]
        p.append(r(LX, yy, LW, hh, CARD, LINE, 1))
        p.append(avatar(LX + 20, yy + 22, 44, i))
        p.append(t(LX + 78, yy + 40, author, 14, INK, 800))
        p.append(t(LX + 78, yy + 60, f"{role}  ·  {tm}", 10, MUT2))
        p.append(t(LX + LW - 20, yy + 40, f"#{idx+1}", 10, GRASS_D, 700, "end", MONO))
        ly = yy + 92
        for s in lines:
            p.append(para(LX + 20, ly, s, 13, INK, 24, LW - 40))
            ly += 24 * len(wrap(s, 13, LW - 40)) + 6
        if idx == 0:
            p.append(r(LX + 20, ly + 4, LW - 40, 92, INK2))
            p.append(t(LX + 34, ly + 26, "[20:14:02] [main/ERROR] Unsupported class file major version 61", 10, "#93C94A", 400, family=MONO))
            p.append(t(LX + 34, ly + 46, "[20:14:02] [main/ERROR] java.lang.NoClassDefFoundError: net/createmod/flywheel", 10, "#C9A0A0", 400, family=MONO))
            p.append(t(LX + 34, ly + 66, "[20:14:02] [main/ERROR] Missing dependency: flywheel >= 0.6.11", 10, "#C9A0A0", 400, family=MONO))
        p.append(ln(LX + 20, yy + hh - 54, LX + LW - 20, yy + hh - 54, LINE))
        p.append(t(LX + 20, yy + hh - 28, "点赞 12   ·   回复   ·   举报", 10, MUT2))
        p.append(t(LX + LW - 20, yy + hh - 28, "引用 →", 10, GRASS_D, 700, "end"))
        fy += hh + 20
    yend = fy - 20
    # 回复框
    p.append(r(LX, yend + 16, LW, 150, CARD, LINE, 1))
    p.append(t(LX + 20, yend + 46, "回复：支持图文 / 代码块 / 附件", 11, MUT2))
    p.append(r(LX + 20, yend + 62, LW - 40, 46, PAPER))
    p.append(link("P03010101", r(LX + LW - 130, yend + 118, 110, 38, GRASS) +
                  t(LX + LW - 75, yend + 143, "发布回复", 11, WHITE, 700, "middle")))
    # 右侧
    p.append(r(RX, y, RW, 200, CARD, LINE, 1))
    p.append(t(RX + 20, y + 34, "关于作者", 12, INK, 800))
    p.append(avatar(RX + 20, y + 56, 56, 0))
    p.append(t(RX + 88, y + 76, "Steve_Builder", 14, INK, 800))
    p.append(t(RX + 88, y + 98, "Lv.12 · 128 发帖 · 1,286 获赞", 10, MUT2))
    p.append(link("P0303", t(RX + 20, y + 156, "查看个人中心 →", 11, GRASS_D, 700)))
    p.append(r(RX, y + 220, RW, 180, INK))
    p.append(t(RX + 20, y + 254, "相关资源", 13, "#F2F7E8", 800))
    for i, (nm, tg) in enumerate([("Better MC 整合包", "P020201"), ("Flywheel 前置", "P020301"), ("启动失败 FAQ", "P010401")]):
        yy = y + 276 + i * 36
        p.append(link(tg, t(RX + 20, yy + 20, nm, 11, "#D6E0CC") + t(RX + RW - 20, yy + 20, "→", 11, GRASS_L, 700, "end")))
    p.append(r(RX, y + 420, RW, 120, GRASS_SOFT))
    p.append(t(RX + 20, y + 452, "举报与规范", 12, GRASS_D, 800))
    p.append(t(RX + 20, y + 476, "广告 / 引战 / 盗版资源将被封禁", 10, MUT))
    p.append(link("P0504", t(RX + 20, y + 510, "查看社区规范 →", 11, GRASS_D, 700)))
    p.append(footer(max(yend + 200, y + 560) + 30, "P03010101 / L5"))
    return W, max(yend + 200, y + 560) + 340, "".join(p), "楼层 / 图文 / 点赞回复"


# ---------- 服务器详情 ----------
def server_detail():
    p = [page_strip("P030201", "服务器详情", "L4", "COMMUNITY / SERVER · OAK TOWN"), topbar("社区交流", 30)]
    p.append(breadcrumb(118, ["首页", "社区交流", "服务器与联机", "服务器详情"], "面包屑回溯 R2"))
    p.append(detail_title(170, "SERVER / OAK TOWN · SURVIVAL", "橡木镇 · 原版生存",
                          "1.20.1 · 原版生存 · 在线 86 / 200 · 延迟 32 ms",
                          ("原版", "生存", "长期", "白名单"), ("4.7", "286 人收藏")))
    y = 420
    LX, LW = CX, 780
    RX = CX + 820
    p.append(cover_panel(LX, y, LW, 360, "forest", "橡木镇 · 主城全景", "SURVIVAL / SEASON 3", "长期开放"))
    p.append(t(LX, y + 400, "服务器介绍", 20, INK, 800))
    p.append(ln(LX, y + 414, LX + LW, y + 414, LINE2))
    yy = y + 444
    for s in ["橡木镇是一个以长期生存为核心的服务器：不删档、不换周目，主城由玩家共同建设，经济完全由玩家驱动。",
              "服务器采用白名单制，需在论坛提交申请；禁止外挂、刷物品与恶意破坏，违规一次即永久封禁。"]:
        p.append(para(LX, yy, s, 14, MUT, 26, LW))
        yy += 26 * len(wrap(s, 14, LW)) + 12
    yy += 20
    p.append(t(LX, yy, "服务器规则", 20, INK, 800))
    p.append(ln(LX, yy + 14, LX + LW, yy + 14, LINE2))
    block, yend = feature_grid(LX, yy + 30, LW, [("shield", "禁止外挂", "包括自动点击与透视"), ("grid", "禁止刷物品", "利用漏洞获利"),
                                                  ("like", "尊重玩家", "恶意破坏直接封禁"), ("book", "白名单制", "论坛申请后进入")], 2)
    p.append(block)
    yy = yend + 20
    p.append(t(LX, yy, "配置信息", 20, INK, 800))
    p.append(ln(LX, yy + 14, LX + LW, yy + 14, LINE2))
    block, yend = spec_table(LX, yy + 30, LW, [("版本", "1.20.1 · 原版", "无需模组"), ("人数上限", "200", "当前 86"),
                                                ("服务器位置", "华东 · 杭州", "延迟 32ms"), ("开服时间", "2023-06-12", "不删档")],
                             ("项目", "说明", "备注"), (200, 360, 200))
    p.append(block)
    yy = yend
    # 右侧加入面板
    p.append(r(RX, y, 380, 420, INK))
    p.append(r(RX, y, 4, 420, GRASS))
    p.append(t(RX + 24, y + 38, "加入服务器", 16, "#F2F7E8", 800))
    p.append(t(RX + 24, y + 58, "JOIN THE SERVER", 9, "#7C8B77", 700, family=MONO, ls=1.5))
    p.append(r(RX + 24, y + 82, 332, 48, INK3, "#2C3C2F", 1))
    p.append(t(RX + 38, y + 112, "oak.example.com", 13, "#EAF2E0", 700, family=MONO))
    p.append(t(RX + 340, y + 112, "复制", 10, GRASS_L, 700, "end"))
    p.append(t(RX + 24, y + 158, "在线 86 / 200", 11, MUT2))
    p.append(r(RX + 24, y + 168, 332, 8, "#223126"))
    p.append(r(RX + 24, y + 168, 332 * 86 / 200, 8, GRASS))
    p.append(link("P0201", r(RX + 24, y + 196, 332, 50, GRASS) +
                  t(RX + 24 + 166, y + 227, "用启动器加入", 14, WHITE, 800, "middle")))
    p.append(link("P0205", r(RX + 24, y + 258, 332, 40, "none", "#3A4C3C", 1) +
                  t(RX + 24 + 166, y + 283, "下载联机工具", 12, "#D6E0CC", 600, "middle")))
    p.append(t(RX + 24, y + 330, "白名单申请：论坛「服务器招募」板块", 10, "#A9B9A2"))
    p.append(t(RX + 24, y + 352, "开服时间 2023-06-12 · 不删档", 10, "#7C8B77"))
    p.append(block_icon(RX + 276, y + 318, 60, 60, top=GRASS, soil="#8A6A46", seed=2))
    # 在线玩家
    p.append(r(RX, y + 440, 380, 200, CARD, LINE, 1))
    p.append(t(RX + 20, y + 476, "在线玩家（部分）", 12, INK, 800))
    for i, nm in enumerate(["Steve_Builder", "Builder_A", "Architect", "Modder"]):
        xx = RX + 20 + i * 86
        p.append(avatar(xx, y + 496, 40, i))
        p.append(t(xx + 20, y + 552, nm.split("_")[0], 9, MUT, 400, "middle"))
    # 相关
    block, ry = related(max(yend, y + 650) + 50, [("服务器与联机", "全部服务器", "86 个在线服", "ocean", "P0302"),
                                                    ("联机工具", "工具", "延迟 30–60ms", "village", "P0205"),
                                                    ("服务器招募", "论坛", "白名单申请", "night", "P030101"),
                                                    ("Better MC 整合包", "整合包", "1.20.1 · 120+ MOD", "forest", "P020201")])
    p.append(block)
    p.append(footer(ry + 40, "P030201 / L4"))
    return W, ry + 340, "".join(p), "规则 / 版本 / 加入方式"


# ---------- 我的内容 ----------
def my_content():
    p = [page_strip("P030301", "我的内容", "L4", "COMMUNITY / MY CONTENT"), topbar("社区交流", 30)]
    p.append(breadcrumb(118, ["首页", "社区交流", "个人中心", "我的内容"], "面包屑回溯 R2"))
    p.append(page_head(170, "PROFILE / MY CONTENT", "我的内容",
                       "发帖、收藏、消息与设置；所有内容按最近更新时间排序。",
                       right=[("128", "我的帖子"), ("46", "我的收藏")]))
    y = 384
    tabs = [("我的帖子", True), ("我的收藏", False), ("我的消息", False), ("账号设置", False)]
    x = CX
    for i, (lb, on) in enumerate(tabs):
        w = len(lb) * 13 + 34
        p.append(r(x, y, w, 42, INK if on else CARD, None if on else LINE, 1))
        p.append(t(x + w / 2, y + 27, lb, 12, GRASS_L if on else MUT, 700 if on else 400, "middle"))
        x += w + 8
    p.append(t(CX + CW, y + 27, "共 128 条", 11, MUT2, 400, "end"))
    y = 456
    items = [("【教程】从零写一个数据包", "技术讨论 · 36 回复 · 3 天前", "已发布", "P03010101"),
             ("【作品】用 12000 个方块复刻主城", "创作展示 · 128 回复 · 5 天前", "已发布", "P03010101"),
             ("【求助】整合包启动崩溃，日志如下", "帮助与反馈 · 42 回复 · 8 天前", "已解决", "P03010101"),
             ("【整合包】1.20.1 机械动力服推荐", "整合包与 MOD · 86 回复 · 12 天前", "已发布", "P03010101"),
             ("草稿：建筑配色手册", "未发布 · 最后编辑 2 天前", "草稿", "P030301")]
    for i, (ti, meta, status, tg) in enumerate(items):
        yy = y + i * 92
        seg = [r(CX, yy, CW, 78, CARD, LINE, 1)]
        seg.append(r(CX, yy, 3, 78, GRASS if status == "已发布" else (AMBER if status == "草稿" else LINE2)))
        seg.append(t(CX + 20, yy + 30, ti, 14, INK, 700))
        seg.append(t(CX + 20, yy + 52, meta, 10, MUT2))
        seg.append(t(CX + CW - 20, yy + 30, status, 10, GRASS_D if status == "已发布" else "#8A6416", 700, "end"))
        seg.append(t(CX + CW - 20, yy + 52, "编辑 →", 10, MUT2, 400, "end"))
        p.append(link(tg, "".join(seg)))
    y = y + 5 * 92
    p.append(link("P0303", r(CX, y + 20, 150, 40, "none", LINE2, 1) +
                  t(CX + 75, y + 45, "返回个人中心", 11, MUT, 600, "middle")))
    p.append(footer(y + 100, "P030301 / L4"))
    return W, y + 420, "".join(p), "发帖 / 收藏 / 消息 / 设置"


# ---------- 视频播放页 ----------
def watch():
    p = [page_strip("P040101", "视频播放页", "L4", "GUIDES / WATCH"), topbar("攻略视频", 30)]
    p.append(breadcrumb(118, ["首页", "攻略视频", "视频攻略", "视频播放页"], "面包屑回溯 R2"))
    y = 170
    p.append(r(0, y, W, 700, INK))
    p.append(r(CX, y + 40, 800, 450, "#080C09", "#2C3C2F", 2))
    p.append(r(CX + 368, y + 232, 64, 64, GRASS, op=0.92))
    p.append(icon(CX + 386, y + 250, "play", INK, 28))
    p.append(t(CX + 400, y + 344, "新手 30 分钟入门路线（第 1 集）", 14, "#7C8B77", 400, "middle"))
    # 播放进度
    p.append(r(CX, y + 506, 800, 4, "#2C3C2F"))
    p.append(r(CX, y + 506, 272, 4, GRASS))
    p.append(r(CX + 272, y + 502, 12, 12, GRASS_L))
    p.append(t(CX, y + 534, "12:20 / 42:00", 10, "#7C8B77", 400, family=MONO))
    p.append(t(CX + 800, y + 534, "1080P · 1.0×", 10, "#7C8B77", 400, "end", MONO))
    # 标题区
    p.append(t(CX, y + 592, "新手 30 分钟入门路线（第 1 集）", 28, "#F4F8EC", 800))
    p.append(t(CX, y + 626, "UP 主 木鱼 · 12.8 万播放 · 2024-06-12 · 42 分钟", 11, "#A9B9A2"))
    p.append(t(CX + 800, y + 592, "点赞 2,860", 11, "#A9B9A2", 400, "end"))
    p.append(t(CX + 800, y + 620, "收藏 1,286", 11, "#A9B9A2", 400, "end"))
    # 右侧播放列表
    RX = CX + 840
    p.append(t(RX, y + 40, "播放列表 / 12 集", 13, "#F2F7E8", 800))
    eps = [("01", "新手 30 分钟入门", True), ("02", "第一座庇护所", False), ("03", "工具与矿物", False),
           ("04", "农田与食物", False), ("05", "下界通行证", False)]
    for i, (no, tt, on) in enumerate(eps):
        yy = y + 66 + i * 82
        p.append(r(RX, yy, 360, 70, "#1B2A1E" if not on else "#26331F"))
        if on:
            p.append(r(RX, yy, 3, 70, GRASS_L))
        p.append(r(RX + 12, yy + 10, 96, 50, "#0A100B"))
        p.append(icon(RX + 46, yy + 24, "play", GRASS_L if on else "#5E6E5A", 20))
        p.append(t(RX + 122, yy + 30, tt, 12, "#EAF2E0" if on else "#B9C6B1", 700 if on else 400))
        p.append(t(RX + 122, yy + 50, f"{no} · 42 分钟", 10, "#7C8B77"))
    y = 170 + 700 + 56
    p.append(sec_head(CX, y, "01", "剧情简介", "ABOUT THIS EPISODE", "配套资源在简介下方"))
    y += 56
    p.append(r(CX, y, 780, 180, CARD, LINE, 1))
    p.append(para(CX + 24, y + 40, "本期从出生点开始，带你完成第一夜的全部准备：采集、合成、庇护所与食物。视频中使用的整合包与光影可在下方直接获取。", 13, MUT, 24, 730))
    p.append(t(CX + 24, y + 90, "相关资源", 12, INK, 800))
    for i, (nm, tg) in enumerate([("Better MC 整合包", "P020201"), ("Complementary 光影", "P020401"), ("第一夜教程", "P010301")]):
        xx = CX + 24 + i * 240
        p.append(link(tg, r(xx, y + 106, 220, 52, PAPER) +
                      t(xx + 14, y + 128, nm, 11, INK, 700) + t(xx + 14, y + 146, "查看 →", 9, GRASS_D, 400)))
    y += 220
    block, ry = related(y, [("机械动力全流程", "视频", "18 集 · 7.2 万播放", "village", "P040101"),
                             ("红石逻辑 20 讲", "视频", "20 集 · 6.4 万播放", "night", "P040101"),
                             ("建筑配色手册", "文章", "8 分钟阅读", "forest", "P040201"),
                             ("Better MC 整合包", "整合包", "视频同款", "ocean", "P020201")], "配套内容", "看完 → 拿资源（R4）")
    p.append(block)
    p.append(footer(ry + 40, "P040101 / L4"))
    return W, ry + 340, "".join(p), "播放器 / 分 P / 相关推荐"


BUILDERS = {
    "P010201": version_detail,
    "P010301": tutorial_detail,
    "P010401": faq_detail,
    "P020101": launcher_detail,
    "P020201": modpack_detail,
    "P020301": mod_detail,
    "P020401": resource_detail,
    "P020501": tool_detail,
    "P030101": board,
    "P030201": server_detail,
    "P030301": my_content,
    "P040101": watch,
    "P040201": article_detail,
    "P03010101": post,
}
