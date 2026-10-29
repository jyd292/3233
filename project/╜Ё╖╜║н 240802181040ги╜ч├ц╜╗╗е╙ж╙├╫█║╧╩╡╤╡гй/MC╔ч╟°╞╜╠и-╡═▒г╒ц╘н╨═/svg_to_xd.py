# -*- coding: utf-8 -*-
"""
把 svg/ 下的低保真页面重新打包为 Adobe XD 工程（.xd）。

XD 工程本质是一个 zip：manifest + 每个画板一份 graphicContent.agc（JSON 场景图）。
本脚本按现有工程的同一套节点结构重建画板，保证：
  1. 画板数量、名称、尺寸与 svg/ 页面一一对应；
  2. 画板按 4 列网格排布，互不重叠；
  3. manifest 与 resources 中的画板登记表同步更新。
"""
import json
import os
import re
import shutil
import tempfile
import uuid
import zipfile
import xml.etree.ElementTree as ET

OUT = r"c:\Users\Administrator\Desktop\金方涵 240802181040（界面交互应用综合实训）\MC社区平台-低保真原型"
SVG_DIR = os.path.join(OUT, "svg")
XD_PATH = os.path.join(OUT, "MC社区平台-低保真原型.xd")
BACKUP_DIR = os.path.join(os.path.dirname(OUT), ".backup")

NS = "{http://www.w3.org/2000/svg}"
COLS = 4
GAP_X, GAP_Y = 400, 280

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
    alpha = round(opacity, 4)
    return {"mode": "RGB", "value": {"r": r, "g": g, "b": b}, "alpha": alpha}


def fill_style(color, opacity=None):
    if not color or color == "none":
        return {"type": "none"}
    c = hex_rgb(color, 1.0 if opacity is None else opacity)
    if c["alpha"] >= 1:
        c.pop("alpha")
    return {"type": "solid", "color": c}


def stroke_style(color, width=1.0, opacity=None):
    if not color or color == "none":
        return {"type": "none", "color": {"mode": "RGB", "value": {"r": 0, "g": 0, "b": 0}, "alpha": 0}, "width": 1}
    c = hex_rgb(color, 1.0 if opacity is None else opacity)
    if c["alpha"] >= 1:
        c.pop("alpha")
    return {"type": "solid", "color": c, "width": float(width or 1)}


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


class NodeFactory(object):
    def __init__(self):
        self.rect_no = 0

    def rect_node(self, x, y, w, h, fill, stroke, sw, opacity):
        if w <= 0 or h <= 0:
            return None
        self.rect_no += 1
        return {
            "type": "shape",
            "name": "矩形 %d" % self.rect_no,
            "meta": {"ux": {"nameL10N": "SHAPE_RECTANGLE"}},
            "id": str(uuid.uuid4()),
            "transform": {"a": 1, "b": 0, "c": 0, "d": 1, "tx": round(x, 2), "ty": round(y, 2)},
            "style": {"fill": fill_style(fill, opacity), "stroke": stroke_style(stroke, sw, opacity)},
            "shape": {"type": "rect", "x": 0, "y": 0, "width": round(w, 2), "height": round(h, 2)},
        }

    def text_node(self, el):
        raw = "".join(el.itertext())
        if not raw:
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
        x, y = num(el, "x"), num(el, "y")
        anchor = el.get("text-anchor", "start")
        w = text_width(raw, size, ls)
        if anchor == "middle":
            x -= w / 2
        elif anchor == "end":
            x -= w
        rgb = hex_rgb(color)["value"]
        argb = (255 << 24) | (rgb["r"] << 16) | (rgb["g"] << 8) | rgb["b"]
        return {
            "type": "text",
            "name": raw,
            "meta": {"ux": {
                "nameL10N": "SHAPE_GROUP",
                "singleTextObject": True,
                "rangedStyles": [{
                    "length": len(raw), "linkId": "", "fontFamily": family, "fontStyle": style_name,
                    "fontSize": size, "charSpacing": ls, "underline": False, "textTransform": "none",
                    "textScript": "none", "fill": {"value": argb}, "strikethrough": False, "hyperlinkUrl": "",
                }],
            }},
            "id": str(uuid.uuid4()),
            "transform": {"a": 1, "b": 0, "c": 0, "d": 1, "tx": round(x, 2), "ty": round(y, 2)},
            "style": {
                "fill": fill_style(color, opacity),
                "stroke": stroke_style(None),
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
    factory = NodeFactory()
    nodes = []

    def walk(el, tx=0.0, ty=0.0):
        for child in el:
            tag = child.tag.replace(NS, "")
            if tag == "g":
                t = child.get("transform", "")
                m = re.search(r"translate\(\s*([-\d.]+)[ ,]+([-\d.]+)", t)
                walk(child, tx + (float(m.group(1)) if m else 0), ty + (float(m.group(2)) if m else 0))
            elif tag == "rect":
                opacity = float(child.get("opacity", 1) or 1)
                node = factory.rect_node(
                    tx + num(child, "x"), ty + num(child, "y"),
                    num(child, "width"), num(child, "height"),
                    child.get("fill", "none"), child.get("stroke"), num(child, "stroke-width", 1), opacity)
                if node:
                    nodes.append(node)
            elif tag == "line":
                sw = num(child, "stroke-width", 1)
                x1, y1 = tx + num(child, "x1"), ty + num(child, "y1")
                x2, y2 = tx + num(child, "x2"), ty + num(child, "y2")
                if abs(y2 - y1) <= abs(x2 - x1):
                    node = factory.rect_node(min(x1, x2), y1 - sw / 2, max(abs(x2 - x1), sw), sw,
                                             child.get("stroke", "#D9D9DF"), None, 1, 1.0)
                else:
                    node = factory.rect_node(x1 - sw / 2, min(y1, y2), sw, abs(y2 - y1),
                                             child.get("stroke", "#D9D9DF"), None, 1, 1.0)
                if node:
                    nodes.append(node)
            elif tag == "text":
                node = factory.text_node(child)
                if node:
                    node["transform"]["tx"] += tx
                    node["transform"]["ty"] += ty
                    nodes.append(node)

    walk(root)
    return w, h, nodes


def artboard_doc(ab_id, name, x, y, w, h, nodes):
    group_id = str(uuid.uuid4())
    return {
        "version": "1.5.0",
        "children": [{
            "type": "artboard",
            "meta": {"ux": {"nameL10N": "SHAPE_RECTANGLE", "constraintsDisabled": True, "gridStyle": GRID_STYLE}},
            "id": ab_id,
            "style": {"fill": {"type": "solid", "color": {"mode": "RGB", "value": {"r": 255, "g": 255, "b": 255}}}},
            "artboard": {
                "children": [{
                    "type": "group",
                    "name": name,
                    "id": group_id,
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


def main():
    svgs = sorted((f for f in os.listdir(SVG_DIR) if f.lower().endswith(".svg")),
                  key=lambda f: (0 if f.startswith("P") else 1, f.split("_")[0]))
    if not svgs:
        raise SystemExit("svg/ 下没有页面，请先运行 generate_wireframes.py")

    if os.path.exists(XD_PATH):
        os.makedirs(BACKUP_DIR, exist_ok=True)
        bak = os.path.join(BACKUP_DIR, "MC社区平台-低保真原型_旧版.xd")
        if not os.path.exists(bak):
            shutil.copy2(XD_PATH, bak)

    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(XD_PATH) as z:
        z.extractall(tmp)
        keep = {n: z.read(n) for n in z.namelist()
                if not n.startswith("artwork/") and n != "manifest" and n != "resources/graphics/graphicContent.agc"}

    # 清掉旧画板，仅保留 pasteboard
    art_root = os.path.join(tmp, "artwork")
    for d in os.listdir(art_root) if os.path.isdir(art_root) else []:
        if d != "pasteboard":
            shutil.rmtree(os.path.join(art_root, d), ignore_errors=True)

    manifest = json.load(open(os.path.join(tmp, "manifest"), encoding="utf-8"))
    resources = json.load(open(os.path.join(tmp, "resources", "graphics", "graphicContent.agc"), encoding="utf-8"))

    artwork = next(c for c in manifest["children"] if c.get("name") == "artwork")
    pasteboard = next((c for c in artwork["children"] if c.get("name") == "pasteboard"), None)
    boards = []
    reg = {}
    x, y, col, row_h = 0, 0, 0, 0
    for fn in svgs:
        code, name = fn[:-4].split("_", 1)
        w, h, nodes = parse_svg(os.path.join(SVG_DIR, fn))
        if col >= COLS:
            col, x = 0, 0
            y += row_h + GAP_Y
            row_h = 0
        ab_id = str(uuid.uuid4())
        label = "%s %s" % (code, name.replace("-", "/"))
        boards.append({
            "id": ab_id,
            "path": "artboard-" + ab_id,
            "name": label,
            "children": [{
                "id": str(uuid.uuid4()), "path": "graphics", "name": "graphics",
                "components": [{"id": str(uuid.uuid4()), "state": "unmodified", "path": "graphicContent.agc",
                                "name": "", "type": "application/vnd.adobe.agc.graphicsTree+json", "rel": "primary"}],
            }],
            "uxdesign#bounds": {"x": int(x), "y": int(y), "width": int(w), "height": int(h)},
            "uxdesign#viewport": {"height": int(h)},
        })
        reg[ab_id] = {"width": int(w), "height": int(h), "name": label,
                      "x": int(x), "y": int(y), "viewportHeight": int(h)}
        doc = artboard_doc(ab_id, label, x, y, w, h, nodes)
        dest = os.path.join(tmp, "artwork", "artboard-" + ab_id, "graphics")
        os.makedirs(dest, exist_ok=True)
        with open(os.path.join(dest, "graphicContent.agc"), "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, separators=(",", ":"))
        x += w + GAP_X
        col += 1
        row_h = max(row_h, h)

    artwork["children"] = ([pasteboard] if pasteboard else []) + boards
    resources["artboards"] = reg

    with open(os.path.join(tmp, "manifest"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(tmp, "resources", "graphics", "graphicContent.agc"), "w", encoding="utf-8") as f:
        json.dump(resources, f, ensure_ascii=False, separators=(",", ":"))

    tmp_zip = XD_PATH + ".tmp"
    with zipfile.ZipFile(tmp_zip, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(zipfile.ZipInfo("mimetype"), keep["mimetype"], compress_type=zipfile.ZIP_STORED)
        for name, data in keep.items():
            if name == "mimetype":
                continue
            z.writestr(name, data)
        for root, _, files in os.walk(os.path.join(tmp, "artwork")):
            for f in files:
                full = os.path.join(root, f)
                z.write(full, os.path.relpath(full, tmp).replace("\\", "/"))
        for rel in ("manifest", os.path.join("resources", "graphics", "graphicContent.agc")):
            z.write(os.path.join(tmp, rel), rel.replace("\\", "/"))
    os.replace(tmp_zip, XD_PATH)
    shutil.rmtree(tmp, ignore_errors=True)

    print("artboards:", len(boards))
    for b in boards:
        print(" ", b["name"], b["uxdesign#bounds"]["width"], "x", b["uxdesign#bounds"]["height"])


if __name__ == "__main__":
    main()
