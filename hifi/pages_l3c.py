# -*- coding: utf-8 -*-
"""L3 页面 · 社区 / 攻略 / 关于与支持"""
from ds import *
from blocks import (cover_card, detail_title, filter_row, page_head, pager, related,
                    row_card, section_banner, side_download, spec_table, tag_pill)
from pages_l3 import article_page


def forum():
    p = [page_strip("P0301", "论坛板块", "L3", "COMMUNITY / FORUM BOARDS"), topbar("社区交流", 30)]
    p.append(breadcrumb(118, ["首页", "社区交流", "论坛板块"], "面包屑回溯 R2"))
    p.append(page_head(170, "COMMUNITY / FORUM", "论坛板块",
                       "五个分区覆盖版本、整合包、建筑、红石与技术；发帖前请先读板块规则。",
                       right=[("2,318", "论坛主题"), ("236", "今日新帖")]))
    y = 384
    p.append(r(CX, y, CW, 64, CARD, LINE, 1))
    p.append(t(CX + 20, y + 38, "全部分区", 15, INK, 800))
    p.append(t(CX + 140, y + 38, "主题 2,318  ·  帖 24,760  ·  今日 236", 11, MUT, 400))
    p.append(link("P030101", r(CX + CW - 150, y + 12, 130, 40, GRASS) +
                  icon(CX + CW - 132, y + 23, "plus", WHITE, 16) +
                  t(CX + CW - 106, y + 37, "发布主题", 12, WHITE, 700)))
    y = 464
    boards = [("综合讨论区", "版本更新、整合包、服务器与技术话题", "1,286", "12,860", "3 分钟前", "forest", "P030101"),
              ("建筑与红石", "作品展示、建筑教程、红石电路", "428", "4,320", "8 分钟前", "village", "P030101"),
              ("整合包与 MOD", "整合包推荐、MOD 兼容与安装求助", "316", "3,180", "12 分钟前", "night", "P030101"),
              ("服务器招募", "服务器宣传、招募与联机约战", "186", "2,460", "22 分钟前", "ocean", "P030101"),
              ("帮助与反馈", "启动失败、报错、站点问题", "102", "1,940", "31 分钟前", "nether", "P030101")]
    for i, (nm, desc, topics, posts, last, var, tg) in enumerate(boards):
        yy = y + i * 132
        seg = [r(CX, yy, CW, 118, CARD, LINE, 1)]
        seg.append(r(CX, yy, 3, 118, GRASS if i == 0 else LINE2))
        seg.append(block_icon(CX + 20, yy + 27, 64, 64, top=[GRASS, "#6E9455", "#7E9BAA", "#B4522A", "#8C3B2A"][i],
                              soil=["#8A6A46", "#5A4A3A", "#A88F68", "#552017", "#3F160F"][i], seed=i))
        seg.append(t(CX + 104, yy + 38, nm, 19, INK, 800))
        seg.append(t(CX + 104, yy + 60, desc, 12, MUT))
        seg.append(t(CX + 104, yy + 92, f"主题 {topics}  ·  帖 {posts}  ·  最后回复 {last}", 10, MUT2, 400))
        seg.append(t(CX + CW - 24, yy + 62, "进入 →", 12, GRASS_D, 700, "end"))
        p.append(link(tg, "".join(seg)))
    y = y + 5 * 132
    # 公告 + 版主
    p.append(r(CX, y + 10, 780, 150, INK))
    p.append(r(CX, y + 10, 4, 150, GRASS))
    p.append(t(CX + 24, y + 46, "板块公告", 14, "#F2F7E8", 800))
    p.append(t(CX + 24, y + 74, "发帖前请搜索历史主题；求助请附日志、截图与版本信息。", 12, "#A9B9A2"))
    p.append(t(CX + 24, y + 98, "禁止发布服务器广告以外的推广内容，违者封禁 7 天。", 11, "#7C8B77"))
    p.append(link("P0504", t(CX + 24, y + 130, "查看完整社区规范 →", 11, GRASS_L, 700)))
    p.append(r(CX + 820, y + 10, 380, 150, GRASS_SOFT))
    p.append(t(CX + 844, y + 44, "还没账号？", 14, GRASS_D, 800))
    p.append(t(CX + 844, y + 70, "登录后可发帖、收藏与接收回复提醒。", 11, MUT))
    p.append(link("G01", r(CX + 844, y + 92, 200, 38, GRASS) +
                  t(CX + 944, y + 116, "登录 / 注册", 12, WHITE, 700, "middle")))
    y += 170
    p.append(footer(y + 20, "P0301 / L3"))
    return W, y + 320, "".join(p), "分区列表 / 最新主题 / 发帖入口"


def servers():
    p = [page_strip("P0302", "服务器与联机", "L3", "COMMUNITY / SERVERS"), topbar("社区交流", 30)]
    p.append(breadcrumb(118, ["首页", "社区交流", "服务器与联机"], "面包屑回溯 R2"))
    p.append(page_head(170, "COMMUNITY / SERVERS", "服务器与联机",
                       "按版本、玩法与人数筛选服务器；在线人数与延迟每 5 分钟刷新一次。",
                       right=[("86", "个在线服"), ("12,480", "总在线")]))
    y = 384
    p.append(filter_row(y, [("版本", ["全部", "1.20.1", "1.19.2", "1.18.2"]),
                            ("玩法", ["全部", "生存", "建筑", "PVP", "模组"])], "共 86 个服务器 · 按在线人数排序"))
    y = 464
    sv = [("橡木镇 · 原版生存", "1.20.1", ["原版", "生存", "长期"], "86/200", 32, "forest", "P030201"),
          ("深岩堡 · 模组生存", "1.20.1", ["模组", "生存", "经济"], "142/300", 46, "night", "P030201"),
          ("潮汐湾 · 建筑服", "1.19.2", ["建筑", "创造", "休闲"], "58/120", 28, "ocean", "P030201"),
          ("熔炉城 · PVP", "1.20.1", ["PVP", "竞技", "赛季"], "96/150", 61, "nether", "P030201"),
          ("天空岛 · 空岛生存", "1.20.1", ["空岛", "生存", "任务"], "74/160", 39, "village", "P030201"),
          ("红石工坊 · 技术服", "1.20.1", ["红石", "技术", "创造"], "42/100", 35, "forest", "P030201")]
    for i, (nm, ver, tags, online, ping, var, tg) in enumerate(sv):
        yy = y + i * 118
        seg = [r(CX, yy, CW, 104, CARD, LINE, 1)]
        seg.append(block_icon(CX + 20, yy + 20, 64, 64, top=[GRASS, "#6E9455", "#7E9BAA", "#B4522A", "#C4A06A", "#6E9455"][i],
                              soil="#8A6A46", seed=i))
        seg.append(t(CX + 104, yy + 34, nm, 17, INK, 800))
        xx = CX + 104
        for tgx in tags:
            tp, nx = tag_pill(xx, yy + 48, tgx, INK, PAPER2)
            seg.append(tp)
            xx = nx + 8
        seg.append(t(CX + 104, yy + 84, f"版本 {ver}  ·  在线 {online}  ·  延迟 {ping}ms", 10, MUT2, 400))
        seg.append(r(CX + 700, yy + 44, 220, 8, LINE))
        seg.append(r(CX + 700, yy + 44, 220 * int(online.split('/')[0]) / int(online.split('/')[1]), 8, GRASS))
        seg.append(t(CX + 820, yy + 76, "在线率", 9, MUT2, 400, "middle"))
        seg.append(r(CX + CW - 130, yy + 32, 110, 40, "none", LINE2, 1))
        seg.append(t(CX + CW - 75, yy + 57, "加入 →", 11, INK, 700, "middle"))
        p.append(link(tg, "".join(seg)))
    y = y + 6 * 118
    p.append(pager(y + 10, 8, 1))
    y += 66
    p.append(section_banner(y + 20, "想自己开服？", "服务器基础配置、端口映射与联机工具，一页看完。", "查看联机工具", "P0205", 150))
    y += 170
    p.append(footer(y + 40, "P0302 / L3"))
    return W, y + 340, "".join(p), "服务器列表 / 版本筛选"


def profile():
    p = [page_strip("P0303", "个人中心", "L3", "COMMUNITY / PROFILE"), topbar("社区交流", 30)]
    p.append(breadcrumb(118, ["首页", "社区交流", "个人中心"], "需登录 · 面包屑回溯 R2"))
    # 头部
    hy, hh = 170, 260
    p.append(r(0, hy, W, hh, INK))
    for i in range(1, 40):
        p.append(r(i * 48, hy, 1, hh, "#16231A"))
    p.append(r(CX, hy + 50, 96, 96, "#1B2A1E", GRASS, 2))
    p.append(avatar(CX + 8, hy + 58, 80, 0, GRASS))
    p.append(t(CX + 120, hy + 86, "Steve_Builder", 28, "#F4F8EC", 800))
    p.append(t(CX + 120, hy + 116, "Lv.12 · 注册 2023-04 · 综合讨论区", 12, "#A9B9A2"))
    p.append(t(CX + 120, hy + 150, "128 发帖  ·  46 收藏  ·  1,286 获赞", 11, GRASS_L, 400))
    p.append(link("P030301", r(CX + CW - 144, hy + 66, 124, 40, "none", "#3A4C3C", 1) +
                  t(CX + CW - 82, hy + 91, "编辑资料", 12, "#DAE4D5", 600, "middle")))
    # 侧栏
    y = 430
    p.append(r(CX, y, 260, 300, CARD, LINE, 1))
    for i, s in enumerate(["我的帖子", "我的收藏", "我的消息", "账号设置"]):
        yy = y + i * 66
        if i == 0:
            p.append(r(CX, yy, 260, 66, PAPER2))
            p.append(r(CX, yy, 3, 66, GRASS))
        p.append(t(CX + 24, yy + 40, s, 14, INK if i == 0 else MUT, 700 if i == 0 else 400))
        p.append(t(CX + 236, yy + 40, ["128", "46", "3", ""][i], 10, MUT2, 400, "end", MONO))
    p.append(r(CX, y + 300, 260, 120, GRASS_SOFT))
    p.append(t(CX + 20, y + 332, "发帖规范", 13, GRASS_D, 800))
    p.append(t(CX + 20, y + 356, "求助附日志，作品附存档", 10, MUT))
    p.append(link("P0301", t(CX + 20, y + 392, "进入论坛 →", 11, GRASS_D, 700)))
    # 内容
    LX = CX + 300
    p.append(t(LX, y + 20, "我的帖子", 22, INK, 800))
    p.append(link("P0301", r(LX + 640, y + 6, 120, 40, GRASS) +
                  t(LX + 700, y + 30, "发帖", 12, WHITE, 700, "middle")))
    posts = [("【教程】从零写一个数据包", "技术讨论 · 36 回复 · 3 天前", "P03010101"),
             ("【作品】用 12000 个方块复刻主城", "创作展示 · 128 回复 · 5 天前", "P03010101"),
             ("【求助】整合包启动崩溃，日志如下", "帮助与反馈 · 42 回复 · 8 天前", "P03010101"),
             ("【整合包】1.20.1 机械动力服推荐", "整合包与 MOD · 86 回复 · 12 天前", "P03010101")]
    for i, (ti, meta, tg) in enumerate(posts):
        p.append(row_card(LX, y + 44 + i * 92, 760, 78, ti, meta, [], tg, right="查看 →"))
    p.append(footer(y + 450, "P0303 / L3"))
    return W, y + 770, "".join(p), "资料 / 我的帖子 / 收藏入口"


def video_list():
    p = [page_strip("P0401", "视频攻略", "L3", "GUIDES / VIDEO SERIES"), topbar("攻略视频", 30)]
    p.append(breadcrumb(118, ["首页", "攻略视频", "视频攻略"], "面包屑回溯 R2"))
    p.append(page_head(170, "GUIDES / VIDEO", "视频攻略",
                       "按合集、UP 主与难度分区；从第一夜到红石与建筑，按顺序跟做即可。",
                       right=[("86", "个合集"), ("4.8", "平均评分")]))
    y = 384
    # 精选
    p.append(r(CX, y, 780, 340, INK))
    p.append(voxel(CX + 400, y, 380, 340, "village", 9))
    p.append(r(CX, y, 4, 340, GRASS))
    p.append(t(CX + 32, y + 40, "本周精选", 10, GRASS_L, 700, ls=1.2))
    p.append(t(CX + 92, y + 40, "/ FEATURED", 10, "#7C8B77", 700, family=MONO, ls=1.4))
    p.append(t(CX + 32, y + 100, "新手 30 分钟", 30, "#F4F8EC", 800))
    p.append(t(CX + 32, y + 134, "入门路线（第 1 集）", 30, "#F4F8EC", 800))
    p.append(t(CX + 32, y + 174, "从第一夜到第一次联机，边看边装。", 13, "#A9B9A2"))
    p.append(t(CX + 32, y + 208, "12.8 万播放  ·  42 分钟  ·  2024-06-12", 10, "#7C8B77", 400))
    p.append(link("P040101", r(CX + 32, y + 244, 190, 50, GRASS) +
                  icon(CX + 56, y + 259, "play", WHITE, 18) +
                  t(CX + 126, y + 275, "立即播放", 14, WHITE, 800, "middle")))
    # 右侧榜单
    RX, RW = CX + 820, 380
    p.append(r(RX, y, RW, 340, CARD, LINE, 1))
    p.append(t(RX + 20, y + 34, "热度榜 / TOP 5", 12, INK, 800))
    hot = [("01", "第一夜生存清单", "86K"),
           ("02", "Create 机械动力入门", "72K"),
           ("03", "红石从零开始", "64K"),
           ("04", "建筑配色手册", "58K"),
           ("05", "联机工具配置", "46K")]
    for i, (no, tt, vv) in enumerate(hot):
        yy = y + 56 + i * 54
        p.append(t(RX + 20, yy + 22, no, 10, GRASS_D if i < 3 else MUT2, 700, family=MONO))
        p.append(t(RX + 52, yy + 22, tt, 12, INK, 600))
        p.append(t(RX + RW - 20, yy + 22, vv, 10, MUT2, 400, "end", MONO))
        p.append(ln(RX + 20, yy + 36, RX + RW - 20, yy + 36, LINE))
    y = 384 + 340 + 60
    p.append(sec_head(CX, y, "01", "全部合集", "ALL SERIES", "按难度分级 · 更新于 2024-06-12"))
    y += 56
    vids = [("新手 30 分钟入门", "入门 / 生存", "42 分钟 · 12.8 万播放", "forest", "P040101", "入门"),
            ("创世神建筑课", "进阶 / 建筑", "12 集 · 8.6 万播放", "village", "P040101", "建筑"),
            ("红石逻辑 20 讲", "进阶 / 红石", "20 集 · 6.4 万播放", "night", "P040101", "红石"),
            ("机械动力全流程", "挑战 / 模组", "18 集 · 7.2 万播放", "ocean", "P040101", "模组"),
            ("服务器开服指南", "进阶 / 联机", "9 集 · 4.6 万播放", "nether", "P040101", "联机"),
            ("数据包开发入门", "挑战 / 技术", "6 集 · 3.8 万播放", "forest", "P040101", "技术")]
    cw3 = (CW - 2 * 24) / 3
    for i, (nm, cat, meta, var, tg, tag) in enumerate(vids):
        row, col = divmod(i, 3)
        p.append(cover_card(CX + col * (cw3 + 24), y + row * 366, cw3, 340, nm, cat, meta, var, tg,
                            tag=tag, footer_left="播放列表"))
    y = y + 2 * 366
    p.append(pager(y, 4, 1))
    y += 66
    p.append(footer(y, "P0401 / L3"))
    return W, y + 320, "".join(p), "合集 / UP 主 / 难度分区"


def articles():
    p = [page_strip("P0402", "图文攻略", "L3", "GUIDES / ARTICLES"), topbar("攻略视频", 30)]
    p.append(breadcrumb(118, ["首页", "攻略视频", "图文攻略"], "面包屑回溯 R2"))
    p.append(page_head(170, "GUIDES / ARTICLE", "图文攻略",
                       "适合查阅与精读：分类文章列表，覆盖生存、建筑、红石、模组与联机。",
                       right=[("240", "篇文章"), ("12", "本周更新")]))
    y = 384
    p.append(filter_row(y, [("分类", ["全部", "生存", "建筑", "红石", "模组"]),
                            ("排序", ["最新", "热门", "收藏"])], "共 240 篇文章"))
    y = 464
    arts = [("红石从零开始：门、灯与时钟", "红石 / REDSTONE", "12 分钟 · 3,286 阅读 · 4.8 分", "P040201", "forest"),
            ("建筑配色手册：五种不出错的搭配", "建筑 / BUILD", "8 分钟 · 2,860 阅读 · 4.7 分", "P040201", "village"),
            ("从零写一个数据包", "技术 / DATAPACK", "15 分钟 · 2,180 阅读 · 4.9 分", "P040201", "night"),
            ("整合包冲突排查流程", "模组 / MODPACK", "10 分钟 · 1,960 阅读 · 4.5 分", "P040201", "ocean"),
            ("联机延迟优化清单", "联机 / NETWORK", "6 分钟 · 1,720 阅读 · 4.4 分", "P040201", "nether"),
            ("第一夜生存的 12 个细节", "生存 / SURVIVAL", "7 分钟 · 1,580 阅读 · 4.6 分", "P040201", "forest")]
    for i, (nm, cat, meta, tg, var) in enumerate(arts):
        row, col = divmod(i, 2)
        x = CX + col * 612
        yy = y + row * 148
        seg = [r(x, yy, 588, 132, CARD, LINE, 1)]
        seg.append(voxel(x + 1, yy + 1, 200, 130, var, i + 4))
        seg.append(r(x + 1, yy + 1, 200, 130, "none", LINE))
        seg.append(t(x + 224, yy + 34, cat, 10, GRASS_D, 700, ls=0.8))
        seg.append(t(x + 224, yy + 62, nm, 16, INK, 800))
        seg.append(t(x + 224, yy + 88, meta, 11, MUT))
        seg.append(t(x + 568, yy + 112, "阅读 →", 11, GRASS_D, 700, "end"))
        p.append(link(tg, "".join(seg)))
    y = y + 3 * 148
    p.append(pager(y + 10, 8, 1))
    y += 66
    p.append(section_banner(y + 20, "更喜欢看视频？", "视频攻略按合集顺序更新，适合跟做。", "切换到视频攻略", "P0401", 150))
    y += 170
    p.append(footer(y + 40, "P0402 / L3"))
    return W, y + 340, "".join(p), "分类文章列表"


# ---------- 关于与支持 ----------
def about():
    return article_page(dict(
        code="P0501", name="关于我们", active="关于与支持", level="L3",
        strip="ABOUT / TEAM · MISSION",
        crumb=["首页", "关于与支持", "关于我们"],
        kicker="ABOUT / MC HUB",
        title="我们为什么做 MC HUB",
        lead="一个给中文玩家用的 Minecraft 资源与社区索引：找得到、装得上、有人问。",
        meta="最后更新 2024-06-12 · 3 人团队 · 所在城市 杭州",
        stats=[("41", "页面模板"), ("1,860", "资源收录")],
        toc=["起点", "我们坚持的三件事", "团队", "联系方式"],
        sections=[
            ("h2", "一、起点"),
            ("p", "2019 年，我们三个人在同一个服务器里搭了一座城。那时候找整合包要翻五个论坛、下载链接一半失效、版本对不上导致游戏崩溃——我们想做一个「把版本、兼容性和安装说明写清楚」的地方。"),
            ("p", "MC HUB 不是下载站，也不是论坛。它更像一张索引：把散落在各处的启动器、整合包、MOD、光影与攻略收拢到同一套结构里，让新手能在三次点击内找到下一步。"),
            ("img", "forest", "主世界 · 橡木镇", "THE FIRST WORLD / 2019"),
            ("h2", "二、我们坚持的三件事"),
            ("list", ["版本与兼容性前置：每个下载详情页必须写清楚版本、加载器与依赖。",
                      "内容可回溯：攻略标注更新时间与适用版本，过期内容会被标记。",
                      "社区优先：求助帖 24 小时内有人回复；广告与引战内容零容忍。"]),
            ("h2", "三、团队"),
            ("p", "三个人：一名前端与交互、一名内容编辑、一名社区运营。白天各自上班，晚上维护站点；服务器费用由社区赞助覆盖。"),
            ("h2", "四、联系方式"),
            ("p", "内容纠错、合作与赞助请联系 support@mchub.example；社区问题请优先发到「帮助与反馈」板块。"),
            ("note", "本页信息每季度复核一次；团队与联系方式变更会在更新日志同步。"),
        ]))


def contact():
    p = [page_strip("P0502", "联系与反馈", "L3", "ABOUT / CONTACT"), topbar("关于与支持", 30)]
    p.append(breadcrumb(118, ["首页", "关于与支持", "联系与反馈"], "面包屑回溯 R2"))
    p.append(page_head(170, "ABOUT / CONTACT", "联系与反馈",
                       "问题反馈、内容纠错、合作洽谈，都会在 2 个工作日内回复。",
                       right=[("2", "工作日"), ("100%", "回复率")]))
    y = 384
    LX, LW = CX, 780
    RX, RW = CX + 820, 380
    p.append(t(LX, y, "问题反馈表单", 20, INK, 800))
    p.append(ln(LX, y + 14, LX + LW, y + 14, LINE2))
    fields = [("反馈类型", "问题反馈 / 内容纠错 / 合作 / 其他", 44),
              ("联系方式", "邮箱或 QQ（便于回复）", 44),
              ("相关页面", "粘贴出现问题的页面链接", 44),
              ("问题描述", "描述现象、复现步骤与期望结果", 120)]
    fy = y + 44
    for k, ph, h in fields:
        p.append(t(LX, fy, k, 12, INK, 700))
        p.append(r(LX, fy + 12, LW, h, CARD, LINE2, 1))
        p.append(t(LX + 16, fy + (40 if h < 60 else 40), ph, 12, MUT2))
        fy += h + 40
    p.append(r(LX, fy + 6, LW, 90, PAPER2, LINE2, 1))
    p.append(icon(LX + 20, fy + 34, "download", MUT2, 20))
    p.append(t(LX + 52, fy + 50, "上传截图 / 日志文件（≤ 10 MB）", 12, MUT))
    p.append(t(LX + 52, fy + 72, "支持 .png / .jpg / .log / .txt", 10, MUT2))
    p.append(link("P0502", r(LX, fy + 118, 190, 48, GRASS) + t(LX + 95, fy + 148, "提交反馈", 14, WHITE, 800, "middle")))
    p.append(t(LX + 210, fy + 148, "提交即视为同意《用户协议与隐私》", 10, MUT2))
    # 右侧
    p.append(r(RX, y + 20, RW, 320, CARD, LINE, 1))
    p.append(t(RX + 20, y + 56, "其他联系方式", 16, INK, 800))
    contacts = [("反馈邮箱", "support@mchub.example"), ("合作邮箱", "bd@mchub.example"),
                ("QQ 群", "1234 5678"), ("工作时间", "工作日 10:00–19:00")]
    for i, (k, v) in enumerate(contacts):
        yy = y + 96 + i * 34
        p.append(t(RX + 20, yy, k, 11, MUT))
        p.append(t(RX + RW - 20, yy, v, 11, INK, 600, "end"))
        p.append(ln(RX + 20, yy + 12, RX + RW - 20, yy + 12, LINE))
    p.append(r(RX, y + 360, RW, 110, GRASS_SOFT))
    p.append(t(RX + 20, y + 392, "紧急问题？", 13, GRASS_D, 800))
    p.append(t(RX + 20, y + 416, "先查「常见问题」，92% 的问题已有答案。", 10, MUT))
    p.append(link("P0104", t(RX + 20, y + 448, "打开常见问题 →", 11, GRASS_D, 700)))
    yend = max(fy + 190, y + 480)
    p.append(footer(yend + 40, "P0502 / L3"))
    return W, yend + 340, "".join(p), "联系方式 / 问题反馈表单"


def changelog():
    p = [page_strip("P0503", "更新日志", "L3", "ABOUT / CHANGELOG"), topbar("关于与支持", 30)]
    p.append(breadcrumb(118, ["首页", "关于与支持", "更新日志"], "面包屑回溯 R2"))
    p.append(page_head(170, "ABOUT / CHANGELOG", "更新日志",
                       "站点功能、资源库与社区规则的版本记录，按时间倒序。",
                       right=[("24", "次更新"), ("V1.0", "当前版本")]))
    y = 384
    p.append(filter_row(y, [("范围", ["全部", "站点", "资源库", "社区"]),
                            ("时间", ["近 3 个月", "今年", "全部"])], "共 24 条记录"))
    y = 482
    p.append(sec_head(CX, y, "01", "版本记录", "RELEASES", "从 V1.0 开始归档"))
    y += 56
    logs = [("v1.4.0", "2024-06-12", "高保真视觉系统上线", "全新方块视觉语言、12 列栅格与 41 页高保真模板", "站点"),
            ("v1.3.0", "2024-05-20", "联机与语音工具分组", "下载中心新增联机 / 语音工具分组与人数对比", "资源库"),
            ("v1.2.0", "2024-04-18", "整合包筛选与详情重构", "新增版本 / 加载器筛选，详情页补 MOD 清单", "资源库"),
            ("v1.1.0", "2024-03-06", "社区规则 2.0", "新增求助模板与广告判定细则", "社区"),
            ("v1.0.0", "2024-02-12", "信息架构 V1.0", "5 频道 / 18 栏目 / 41 页面正式定稿", "站点")]
    for i, (ver, date, title, desc, scope) in enumerate(logs):
        yy = y + i * 170
        p.append(r(CX, yy, CW, 150, CARD, LINE, 1))
        p.append(r(CX, yy, 4, 150, GRASS if i == 0 else LINE2))
        p.append(t(CX + 24, yy + 38, ver, 20, INK, 800, family=MONO))
        p.append(t(CX + 24, yy + 62, date, 10, MUT2, 400, family=MONO))
        tp, nx = tag_pill(CX + 110, yy + 22, scope, GRASS_D, GRASS_SOFT)
        p.append(tp)
        p.append(t(CX + 110, yy + 68, title, 16, INK, 800))
        p.append(t(CX + 24, yy + 102, desc, 12, MUT))
        p.append(t(CX + CW - 24, yy + 38, "→", 14, MUT2, 400, "end"))
    y = y + 5 * 170
    p.append(footer(y + 20, "P0503 / L3"))
    return W, y + 320, "".join(p), "版本更新记录"


def legal():
    return article_page(dict(
        code="P0504", name="用户协议与隐私", active="关于与支持", level="L3",
        strip="ABOUT / LEGAL · PRIVACY",
        crumb=["首页", "关于与支持", "用户协议与隐私"],
        kicker="ABOUT / LEGAL",
        title="用户协议与隐私",
        lead="使用本站前请阅读：账号规则、内容规范与个人信息处理说明。",
        meta="最近更新 2024-06-12 · 生效日期 2024-06-20 · 阅读约 8 分钟",
        stats=[("5", "章节"), ("8", "分钟阅读")],
        toc=["协议范围", "账号与注册", "内容发布规范", "个人信息与隐私", "免责声明"],
        sections=[
            ("h2", "一、协议范围"),
            ("p", "本协议适用于你对 MC HUB（以下称「本站」）的访问与使用。访问本站即表示你同意本协议；如不同意，请停止使用。"),
            ("h2", "二、账号与注册"),
            ("p", "注册需提供有效邮箱或手机号。账号仅限本人使用，不得转让、出租或用于商业推广。因账号外借导致的封禁与损失由账号持有人承担。"),
            ("p", "我们不会要求你提供游戏正版凭证、身份证照片或支付密码；如遇此类要求，请立即通过「联系与反馈」举报。"),
            ("h2", "三、内容发布规范"),
            ("list", ["禁止发布盗版资源、外挂、破解补丁与绕过正版验证的教程。",
                      "禁止人身攻击、引战、刷屏与未经许可的服务器广告。",
                      "转载内容需注明来源与作者；教程类内容建议标注适用版本。",
                      "违规内容将被删除，情节严重者封禁 7 天至永久。"]),
            ("h2", "四、个人信息与隐私"),
            ("p", "我们仅收集提供服务所必需的信息：账号标识、邮箱、发帖内容与访问日志。访问日志保留 90 天，用于安全审计与故障排查。"),
            ("table", ("信息类型", "用途", "保留期"),
             [("账号与邮箱", "登录、找回密码、通知", "账号存续期"),
              ("发帖与回复", "内容展示、社区管理", "直至删除"),
              ("访问日志", "安全审计、故障排查", "90 天"),
              ("Cookies", "登录状态、偏好设置", "会话 / 1 年")],
             (220, 380, 180)),
            ("h2", "五、免责声明"),
            ("p", "本站资源均来自公开渠道或作者授权，下载后请在 24 小时内自行删除。因使用第三方资源造成的设备损坏、存档丢失或账号风险，本站不承担责任。"),
            ("note", "如对本协议有疑问，请通过「联系与反馈」提交；我们会在 2 个工作日内回复。"),
        ]))


BUILDERS = {
    "P0301": forum,
    "P0302": servers,
    "P0303": profile,
    "P0401": video_list,
    "P0402": articles,
    "P0501": about,
    "P0502": contact,
    "P0503": changelog,
    "P0504": legal,
}
