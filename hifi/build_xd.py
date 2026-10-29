# -*- coding: utf-8 -*-
"""把高保真 SVG 打包为带完整交互连线的 Adobe XD 工程"""
import json, os, re, shutil, tempfile, uuid, zipfile
import xml.etree.ElementTree as ET
from meta import PAGES

BASE = os.path.dirname(__file__)
SVG_DIR = os.path.join(BASE, "out")
TEMPLATE = "/workspace/hifi_src/base.xd"
OUT_XD = os.path.join(BASE, "MC社区平台-高保真原型.xd")

NS = "{http://www.w3.org/2000/svg}"
COLS = 5
GAP_X, GAP_Y = 320, 260

GRID_STYLE = {
    "rowStroke": {"type": "solid", "color": {"mode": "RGB", "value": {"r": 199, "g": 199, "b": 199}, "alpha": 0.5019607843137255}},
    "columnStroke": {"type": "solid", "color": {"mode": "RGB", "value": {"r": 199, "g": 199, "b": 199}, "alpha": 0.5019607843137255}},
    "rowSpacing": 8, "columnSpacing": 8, "defaultLayoutWidth": 1920, "columns": 12, "gutter": 16,
    "marginLeft": 140, "marginTop": 0, "marginRight": 140, "marginBottom": 0,
    "layoutRowStroke": {"type": "solid", "color": {"mode": "RGB", "value": {"r": 0, "g": 255, "b": 255}, "alpha": 0.25098039215686274}},
    "layoutColumnStroke": {"type": "solid", "color": {"mode": "RGB", "value": {"r": 0, "g": 255, "b": 255}, "alpha": 0.25098039215686274}},
}


def hex_rgb(v, opacity=1.0):
    v = (v or "#000000").strip()
    if v.startswith("#"):
        h = v[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    else:
        r = g = b = 0
    c = {"mode": "RGB", "value": {"r": r, "g": g, "b": b}}
    if round(opacity, 4) < 1:
        c["alpha"] = round(opacity, 4)
    return c


def fill_style(color, opacity=None):
    if not color or color == "none":
        return {"type": "none"}
    return {"type": "solid", "color": hex_rgb(color, 1.0 if opacity is None else opacity)}


def stroke_style(color, width=1.0, opacity=None):
    if not color or color == "none":
        return {"type": "none", "color": {"mode": "RGB", "value": {"r": 0, "g": 0, "b": 0}, "alpha": 0}, "width": 1}
    return {"type": "solid", "color": hex_rgb(color, 1.0 if opacity is None else opacity), "width": float(width or 1)}


def num(el, key, default=0.0):
    try:
        return float(str(el.get(key, default)).replace("px", "").strip())
    except Exception:
        return float(default)


def text_width(s, size, ls=0.0):
    w = 0.0
    for ch in s:
        o = ord(ch)
        if o >= 0x2E80:
            w += size
        elif ch in " .,:;'|!il()[]":
            w += size * 0.32
        else:
            w += size * 0.58
    return w + max(0, len(s) - 1) * ls


def new_id():
    return str(uuid.uuid4())


def rect_node(name, x, y, w, h, fill, stroke, sw, opacity):
    if w <= 0 or h <= 0:
        return None
    return {
        "type": "shape", "name": name,
        "meta": {"ux": {"nameL10N": "SHAPE_RECTANGLE"}},
        "id": new_id(),
        "transform": {"a": 1, "b": 0, "c": 0, "d": 1, "tx": round(x, 2), "ty": round(y, 2)},
        "style": {"fill": fill_style(fill, opacity), "stroke": stroke_style(stroke, sw, opacity)},
        "shape": {"type": "rect", "x": 0, "y": 0, "width": round(w, 2), "height": round(h, 2)},
    }


def text_node(el):
    raw = "".join(el.itertext())
    if not raw.strip():
        return None
    size = num(el, "font-size", 16)
    weight = str(el.get("font-weight", "400"))
    bold = weight.isdigit() and int(weight) >= 600
    family_attr = el.get("font-family", "")
    mono = "Consolas" in family_attr or "monospace" in family_attr
    family = "Consolas" if mono else "Microsoft YaHei"
    postscript = ("Consolas-Bold" if bold else "Consolas") if mono else ("MicrosoftYaHei-Bold" if bold else "MicrosoftYaHei")
    style_name = "Bold" if bold else "Regular"
    color = el.get("fill", "#2E2E33")
    opacity = float(el.get("opacity", 1) or 1)
    ls = num(el, "letter-spacing", 0)
    x, y = num(el, "x", 0), num(el, "y", 0)
    anchor = el.get("text-anchor", "start")
    w = text_width(raw, size, ls)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    rgb = hex_rgb(color)["value"]
    argb = (255 << 24) | (rgb["r"] << 16) | (rgb["g"] << 8) | rgb["b"]
    return {
        "type": "text", "name": raw[:60],
        "meta": {"ux": {
            "nameL10N": "SHAPE_GROUP", "singleTextObject": True,
            "rangedStyles": [{
                "length": len(raw), "linkId": "", "fontFamily": family, "fontStyle": style_name,
                "fontSize": size, "charSpacing": ls, "underline": False, "textTransform": "none",
                "textScript": "none", "fill": {"value": argb}, "strikethrough": False, "hyperlinkUrl": "",
            }],
        }},
        "id": new_id(),
        "transform": {"a": 1, "b": 0, "c": 0, "d": 1, "tx": round(x, 2), "ty": round(y, 2)},
        "style": {
            "fill": fill_style(color, opacity), "stroke": stroke_style(None),
            "font": {"postscriptName": postscript, "family": family, "style": style_name, "size": size},
        },
        "text": {
            "frame": {"type": "positioned"},
            "paragraphs": [{"lines": [[{"y": 0, "from": 0, "to": len(raw), "x": 0}]]}],
            "rawText": raw,
        },
    }


def parse_svg(path):
    tree = ET.parse(path)
    root = tree.getroot()
    w = float(re.sub(r"[^0-9.]", "", root.get("width", "1920")) or 1920)
    h = float(re.sub(r"[^0-9.]", "", root.get("height", "1080")) or 1080)
    nodes, links = [], []
    rect_no = [0]

    def walk(el, tx=0.0, ty=0.0, ctx=None):
        for child in el:
            tag = child.tag.replace(NS, "")
            if tag == "a":
                ctx2 = {"target": child.get("data-target"), "nodes": []}
                walk(child, tx, ty, ctx2)
                cand = pick_link_node(ctx2)
                if cand and ctx2.get("target"):
                    links.append((cand, ctx2["target"]))
                continue
            if tag == "g":
                t = child.get("transform", "")
                m = re.search(r"translate\(\s*([-\d.]+)[ ,]+([-\d.]+)", t)
                walk(child, tx + (float(m.group(1)) if m else 0), ty + (float(m.group(2)) if m else 0), ctx)
                continue
            node = None
            if tag == "rect":
                opacity = float(child.get("opacity", 1) or 1)
                rect_no[0] += 1
                node = rect_node("矩形 %d" % rect_no[0], tx + num(child, "x"), ty + num(child, "y"),
                                 num(child, "width"), num(child, "height"),
                                 child.get("fill", "none"), child.get("stroke"), num(child, "stroke-width", 1), opacity)
            elif tag == "line":
                sw = num(child, "stroke-width", 1)
                x1, y1 = tx + num(child, "x1"), ty + num(child, "y1")
                x2, y2 = tx + num(child, "x2"), ty + num(child, "y2")
                rect_no[0] += 1
                if abs(y2 - y1) <= abs(x2 - x1):
                    node = rect_node("矩形 %d" % rect_no[0], min(x1, x2), y1 - sw / 2, max(abs(x2 - x1), sw), sw,
                                     child.get("stroke", "#D9D9DF"), None, 1, 1.0)
                else:
                    node = rect_node("矩形 %d" % rect_no[0], x1 - sw / 2, min(y1, y2), sw, abs(y2 - y1),
                                     child.get("stroke", "#D9D9DF"), None, 1, 1.0)
            elif tag == "text":
                node = text_node(child)
                if node:
                    node["transform"]["tx"] += tx
                    node["transform"]["ty"] += ty
            if node:
                nodes.append(node)
                if ctx is not None:
                    ctx["nodes"].append(node)

    walk(root)
    return w, h, nodes, links


def pick_link_node(ctx):
    """在一组热区内挑选最合适的点击目标：优先大面积矩形，其次字号最大的文本。"""
    rects, texts = [], []
    for n in ctx.get("nodes", []):
        if n["type"] == "shape":
            s = n["shape"]
            rects.append((s["width"] * s["height"], n["id"]))
        elif n["type"] == "text":
            texts.append((n["style"]["font"]["size"], n["id"]))
    if rects:
        best = max(rects)
        if best[0] >= 12000:
            return best[1]
    if texts:
        return max(texts)[1]
    if rects:
        return max(rects)[1]
    return None


def artboard_doc(ab_id, name, x, y, nodes):
    return {
        "version": "1.5.0",
        "children": [{
            "type": "artboard",
            "meta": {"ux": {"nameL10N": "SHAPE_RECTANGLE", "constraintsDisabled": True, "gridStyle": GRID_STYLE}},
            "id": ab_id,
            "style": {"fill": {"type": "solid", "color": {"mode": "RGB", "value": {"r": 255, "g": 255, "b": 255}}}},
            "artboard": {
                "children": [{
                    "type": "group", "name": name, "id": new_id(),
                    "transform": {"a": 1, "b": 0, "c": 0, "d": 1, "tx": x, "ty": y},
                    "meta": {"ux": {"hasCustomName": True, "hasNameFromExternalSource": True,
                                    "localTransform": {"a": 1, "b": 0, "c": 0, "d": 1, "tx": 0, "ty": 0}}},
                    "group": {"children": nodes},
                }],
                "meta": {"ux": {"path": ab_id}},
                "ref": ab_id,
            },
        }],
        "resources": {"href": "/resources/graphics/graphicContent.agc"},
        "artboards": {"href": "/resources/graphics/graphicContent.agc"},
    }


def build():
    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(TEMPLATE) as z:
        z.extractall(tmp)
        keep = {n: z.read(n) for n in z.namelist()
                if not n.startswith("artwork/") and n not in ("manifest", "resources/graphics/graphicContent.agc",
                                                              "interactions/interactions.json")}
    art_root = os.path.join(tmp, "artwork")
    for d in list(os.listdir(art_root)):
        if d != "pasteboard":
            shutil.rmtree(os.path.join(art_root, d), ignore_errors=True)
    manifest = json.load(open(os.path.join(tmp, "manifest"), encoding="utf-8"))
    resources = json.load(open(os.path.join(tmp, "resources", "graphics", "graphicContent.agc"), encoding="utf-8"))

    # 第一轮：登记画板 ID
    boards, reg, layout = [], {}, {}
    x, y, col, row_h = 0, 0, 0, 0
    for code, name, lv, group, desc in PAGES:
        path = os.path.join(SVG_DIR, code + ".svg")
        w, h, nodes, _ = parse_svg(path)
        if col >= COLS:
            col, x = 0, 0
            y += row_h + GAP_Y
            row_h = 0
        ab_id = new_id()
        label = f"{code} {name}"
        layout[code] = (ab_id, x, y, w, h)
        boards.append({
            "id": ab_id, "path": "artboard-" + ab_id, "name": label,
            "children": [{"id": new_id(), "path": "graphics", "name": "graphics",
                          "components": [{"id": new_id(), "state": "unmodified", "path": "graphicContent.agc",
                                          "name": "", "type": "application/vnd.adobe.agc.graphicsTree+json", "rel": "primary"}]}],
            "uxdesign#bounds": {"x": int(x), "y": int(y), "width": int(w), "height": int(h)},
            "uxdesign#viewport": {"height": int(h)},
        })
        reg[ab_id] = {"width": int(w), "height": int(h), "name": label, "x": int(x), "y": int(y), "viewportHeight": int(h)}
        x += w + GAP_X
        col += 1
        row_h = max(row_h, h)
    # 第二轮：重建节点并收集连线
    interactions = {}
    total_links = 0
    missing = []
    for code, name, lv, group, desc in PAGES:
        path = os.path.join(SVG_DIR, code + ".svg")
        w, h, nodes, links = parse_svg(path)
        ab_id, ax, ay, _, _ = layout[code]
        doc = artboard_doc(ab_id, f"{code} {name}", ax, ay, nodes)
        dest = os.path.join(tmp, "artwork", "artboard-" + ab_id, "graphics")
        os.makedirs(dest, exist_ok=True)
        with open(os.path.join(dest, "graphicContent.agc"), "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, separators=(",", ":"))
        for node_id, target in links:
            if target not in layout:
                missing.append((code, target))
                continue
            interactions[node_id] = [{
                "properties": {"transition": "dissolve", "duration": 0.3, "easing": "ease-out",
                               "preserveScrollPosition": False, "destination": layout[target][0], "voiceLocale": "zh-cn"},
                "triggerEvent": "tap", "action": "artboard-transition", "id": new_id(),
            }]
            total_links += 1

    artwork = next(c for c in manifest["children"] if c.get("name") == "artwork")
    pasteboard = next((c for c in artwork["children"] if c.get("name") == "pasteboard"), None)
    artwork["children"] = ([pasteboard] if pasteboard else []) + boards
    resources["artboards"] = reg
    with open(os.path.join(tmp, "manifest"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(tmp, "resources", "graphics", "graphicContent.agc"), "w", encoding="utf-8") as f:
        json.dump(resources, f, ensure_ascii=False, separators=(",", ":"))
    os.makedirs(os.path.join(tmp, "interactions"), exist_ok=True)
    with open(os.path.join(tmp, "interactions", "interactions.json"), "w", encoding="utf-8") as f:
        json.dump({"version": "0.24", "interactions": interactions}, f, ensure_ascii=False, separators=(",", ":"))

    # 打包
    if os.path.exists(OUT_XD):
        os.remove(OUT_XD)
    tmp_zip = OUT_XD + ".tmp"
    with zipfile.ZipFile(tmp_zip, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(zipfile.ZipInfo("mimetype"), keep["mimetype"], compress_type=zipfile.ZIP_STORED)
        for nm, data in keep.items():
            if nm == "mimetype":
                continue
            z.writestr(nm, data)
        for root, _, files in os.walk(os.path.join(tmp, "artwork")):
            for fn in files:
                full = os.path.join(root, fn)
                z.write(full, os.path.relpath(full, tmp).replace("\\", "/"))
        for rel in ("manifest", "resources/graphics/graphicContent.agc", "interactions/interactions.json"):
            z.write(os.path.join(tmp, rel), rel)
    os.replace(tmp_zip, OUT_XD)
    shutil.rmtree(tmp, ignore_errors=True)
    print("artboards:", len(boards), "interactions:", total_links, "missing:", missing[:5])
    print("size MB:", round(os.path.getsize(OUT_XD) / 1024 / 1024, 2))


if __name__ == "__main__":
    build()
