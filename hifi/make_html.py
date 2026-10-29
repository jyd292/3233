# -*- coding: utf-8 -*-
"""生成可点击的 HTML 高保真预览站 + 目录页"""
import os, json, html
import cairosvg
from meta import PAGES, GROUPS

BASE = os.path.dirname(__file__)
OUT = os.path.join(BASE, "out")
SITE = os.path.join(BASE, "site")
PAGES_DIR = os.path.join(SITE, "pages")
THUMBS = os.path.join(SITE, "thumbs")
os.makedirs(PAGES_DIR, exist_ok=True)
os.makedirs(THUMBS, exist_ok=True)

PAGE_W = {p[0]: p for p in PAGES}
codes = [p[0] for p in PAGES]

PAGE_TPL = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{code} · {name} · MC HUB 高保真</title>
<style>
  html,body{{margin:0;padding:0;background:#0C130D;}}
  .stage{{width:100%;max-width:1920px;margin:0 auto;}}
  .stage svg{{display:block;width:100%;height:auto;}}
  .bar{{position:fixed;right:18px;bottom:18px;z-index:99;display:flex;gap:8px;align-items:center;
        background:rgba(12,19,13,.92);border:1px solid #3A4C3C;padding:8px 10px;font:12px/1.4 "Microsoft YaHei","Noto Sans CJK SC",sans-serif;color:#DAE4D5;
        backdrop-filter:blur(6px);}}
  .bar b{{font-family:Consolas,monospace;color:#93C94A;font-weight:700;margin-right:6px}}
  .bar a{{color:#DAE4D5;text-decoration:none;padding:4px 8px;border:1px solid #3A4C3C}}
  .bar a:hover{{border-color:#6EA832;color:#93C94A}}
  .tip{{position:fixed;left:18px;bottom:18px;z-index:99;background:rgba(12,19,13,.9);border:1px solid #2C3C2F;
        color:#7C8B77;font:11px/1.5 "Microsoft YaHei",sans-serif;padding:6px 10px}}
</style></head>
<body>
<div class="tip">点击画板中的导航 / 卡片 / 按钮可直接跳转；也可用右下角目录切换</div>
<div class="stage">{svg}</div>
<div class="bar"><b>{code}</b><a href="../index.html">目录</a><a href="{prev}.html">← 上一页</a><a href="{next_}.html">下一页 →</a></div>
</body></html>
"""


def build_pages():
    for i, code in enumerate(codes):
        svg = open(os.path.join(OUT, code + ".svg"), encoding="utf-8").read()
        prev = codes[i - 1] if i > 0 else code
        nxt = codes[i + 1] if i < len(codes) - 1 else code
        html_text = PAGE_TPL.format(code=code, name=PAGE_W[code][1], svg=svg, prev=prev, next_=nxt)
        with open(os.path.join(PAGES_DIR, code + ".html"), "w", encoding="utf-8") as f:
            f.write(html_text)
        cairosvg.svg2png(url=os.path.join(OUT, code + ".svg"),
                         write_to=os.path.join(THUMBS, code + ".png"), output_width=560)


def build_index():
    groups = []
    for g in GROUPS:
        items = [p for p in PAGES if p[3] == g]
        groups.append((g, items))
    cards = []
    for g, items in groups:
        cards.append(f'<div class="grp" data-g="{g}"><div class="gh"><h2>{g}</h2><span>{len(items)} 页</span></div><div class="grid">')
        for code, name, lv, _, desc in items:
            cards.append(f'''<a class="card" href="pages/{code}.html" data-g="{g}">
  <div class="thumb"><img loading="lazy" src="thumbs/{code}.png" alt="{name}"></div>
  <div class="meta"><span class="code">{code}</span><span class="lv">{lv}</span></div>
  <h3>{name}</h3><p>{desc}</p><span class="go">打开画板 →</span></a>''')
        cards.append('</div></div>')
    body = "\n".join(cards)
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MC HUB · 高保真原型 V1.0 · 41 页</title>
<style>
:root{{--ink:#0C130D;--paper:#F4F5EE;--line:#D7DEC9;--grass:#6EA832;--grassl:#93C94A;--mut:#6D7A66}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--paper);color:var(--ink);
font-family:"Microsoft YaHei","Noto Sans CJK SC",sans-serif}}
header{{background:var(--ink);color:#F4F8EC;padding:64px 0 56px}}
.wrap{{max-width:1320px;margin:0 auto;padding:0 40px}}
.kick{{font:11px/1 Consolas,monospace;letter-spacing:2px;color:var(--grassl)}}
h1{{margin:16px 0 10px;font-size:44px;letter-spacing:1px}}
.sub{{color:#A9B9A2;font-size:15px;max-width:760px}}
.stats{{display:flex;gap:48px;margin-top:32px}}
.stats b{{display:block;font:800 30px/1.2 Consolas,monospace;color:#F4F8EC}}
.stats span{{font-size:11px;color:#7C8B77}}
.filters{{display:flex;gap:8px;flex-wrap:wrap;padding:28px 0 10px}}
.filters button{{font:12px "Microsoft YaHei",sans-serif;padding:8px 14px;border:1px solid var(--line);background:#fff;cursor:pointer}}
.filters button.on{{background:var(--ink);color:var(--grassl);border-color:var(--ink)}}
.grp{{padding:26px 0 6px}}
.gh{{display:flex;align-items:baseline;gap:14px;border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:18px}}
.gh h2{{margin:0;font-size:21px}} .gh span{{font:11px Consolas,monospace;color:var(--mut)}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}}
.card{{background:#fff;border:1px solid var(--line);text-decoration:none;color:var(--ink);padding:0 0 16px;transition:.16s}}
.card:hover{{border-color:var(--grass);transform:translateY(-2px)}}
.thumb{{height:132px;overflow:hidden;border-bottom:1px solid var(--line);background:#E9ECDF}}
.thumb img{{width:100%;display:block}}
.meta{{display:flex;gap:8px;align-items:center;padding:12px 14px 0}}
.code{{font:10px Consolas,monospace;color:var(--grass);border:1px solid #DCE8C8;background:#EAF3DB;padding:2px 6px}}
.lv{{font:10px Consolas,monospace;color:var(--mut);border:1px solid var(--line);padding:2px 6px}}
h3{{margin:10px 14px 4px;font-size:16px}} p{{margin:0 14px;font-size:12px;color:var(--mut);min-height:34px}}
.go{{display:block;margin:10px 14px 0;font-size:11px;color:var(--grass)}}
footer{{margin-top:48px;padding:26px 0;border-top:1px solid var(--line);font:11px Consolas,monospace;color:var(--mut)}}
</style></head><body>
<header><div class="wrap">
  <div class="kick">MC HUB / HIGH-FIDELITY PROTOTYPE V1.0</div>
  <h1>高保真原型 · 41 页</h1>
  <p class="sub">信息架构 V1.0 的视觉落地：1920 画布 / 1200 安全宽 / 12 列栅格 / 方块视觉语言。点击任意画板进入可交互页面，页面内导航、卡片、面包屑均可点击。</p>
  <div class="stats"><div><b>41</b><span>页面画板</b></span></div><div><b>5</b><span>一级频道</b></span></div>
  <div><b>1,141</b><span>交互连线</b></span></div><div><b>1200</b><span>安全宽度</b></span></div></div>
</div></header>
<div class="wrap">
  <div class="filters"><button class="on" data-f="all">全部 41</button>
  {"".join(f'<button data-f="{g}">{g}</button>' for g in GROUPS)}
  </div>
  {body}
  <footer>MC HUB · 界面交互应用综合训练 · 高保真 V1.0 · 2024-06</footer>
</div>
<script>
const btns=[...document.querySelectorAll('.filters button')];
btns.forEach(b=>b.onclick=()=>{{
  btns.forEach(x=>x.classList.remove('on')); b.classList.add('on');
  const f=b.dataset.f;
  document.querySelectorAll('.grp').forEach(g=>{{
    g.style.display=(f==='all'||g.dataset.g===f)?'':'none';
  }});
}});
</script></body></html>"""


if __name__ == "__main__":
    build_pages()
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_index())
    print("site built:", len(codes), "pages")
