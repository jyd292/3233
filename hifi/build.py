# -*- coding: utf-8 -*-
import os, sys, json, importlib
sys.path.insert(0, os.path.dirname(__file__))
import pages
import pages_channels
import pages_l3
import pages_l3b
import pages_l3c
import pages_l4
import pages_g

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)

def svg_doc(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">{body}</svg>')

BUILDERS = dict(pages.BUILDERS)
BUILDERS.update(pages_channels.BUILDERS)
BUILDERS.update(pages_l3.BUILDERS)
BUILDERS.update(pages_l3b.BUILDERS)
BUILDERS.update(pages_l3c.BUILDERS)
BUILDERS.update(pages_l4.BUILDERS)
BUILDERS.update(pages_g.BUILDERS)
codes = sys.argv[1:] or list(BUILDERS.keys())
for code in codes:
    w, h, body, desc = BUILDERS[code]()
    doc = svg_doc(w, h, body)
    path = os.path.join(OUT, f"{code}.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)
    print(code, w, h, len(doc))
    try:
        import cairosvg
        cairosvg.svg2png(url=path, write_to=os.path.join(OUT, f"{code}.png"), output_width=w // 2)
    except Exception as e:
        print("png fail", e)
