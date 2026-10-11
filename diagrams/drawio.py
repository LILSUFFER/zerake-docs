# Swimlane diagrams through draw.io: specs (diagrams/specs*.py) -> .drawio files -> SVG rendered by the official
# draw.io viewer in headless Chrome. draw.io routes the right-angle connectors and places their labels.
# The .drawio files stay in diagrams/drawio/ and can be opened and edited at https://app.diagrams.net
# Usage: python diagrams/drawio.py [name ...]
import html, json, os, re, subprocess, sys, hashlib, glob

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from specs import SPECS as S1
from specs2 import SPECS2 as S2
SPECS = {**S1, **S2}

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
FONT = "Segoe UI"
LANE_W, HEAD_H, ROW_H, PAD_TOP = 220, 42, 84, 14
SIZE = {}
OVAL = "rounded=1;arcSize=50;html=0;fontStyle=1;"
STYLE = {
    "start": OVAL + "fillColor=#C7F2E4;strokeColor=#12A477;fontColor=#0B3D2C;",     # the event that starts it
    "step": "rounded=1;arcSize=12;html=0;fillColor=#EDE7FF;strokeColor=#8B5CF6;fontColor=#3B2A7A;",   # an action
    "dec": "rhombus;html=0;fillColor=#FFF7E0;strokeColor=#D99A00;fontColor=#5C4100;",  # a check
    "status": "rounded=1;arcSize=12;html=0;fillColor=#12A477;strokeColor=#0F8A63;fontColor=#FFFFFF;fontStyle=1;",  # record status
    "end": OVAL + "fillColor=#E3F6C8;strokeColor=#7CB342;fontColor=#2F4A12;",        # result
    "fail": OVAL + "fillColor=#FFE4E6;strokeColor=#E0565F;fontColor=#7A1F2B;",       # refusal / exception
    "skip": OVAL + "fillColor=#F1F5F9;strokeColor=#94A3B8;fontColor=#334155;",       # ignored
}
COMMON = f"fontFamily={FONT};fontSize=13;strokeWidth=1.5;"
LANE = (f"swimlane;horizontal=1;startSize={HEAD_H};fillColor=#F1F4F9;swimlaneFillColor=#FFFFFF;strokeColor=#94A3B8;"
        f"fontColor=#1E293B;fontStyle=1;fontSize=14;fontFamily={FONT};collapsible=0;strokeWidth=1.2;")
EDGE = (f"edgeStyle=orthogonalEdgeStyle;rounded=1;arcSize=10;orthogonalLoop=1;jettySize=auto;html=0;strokeColor=#1F2937;strokeWidth=1.6;"
        f"endArrow=block;endFill=1;endSize=7;fontFamily={FONT};fontSize=12;fontStyle=1;fontColor=#334155;labelBackgroundColor=#FFFFFF;")
SIDE = {"right": "exitX=1;exitY=0.5;", "left": "exitX=0;exitY=0.5;", "bottom": "exitX=0.5;exitY=1;", "top": "exitX=0.5;exitY=0;", "down": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"}


def build(name, spec):
    lanes = spec["lanes"]; nodes = spec["nodes"]; wide = spec.get("wide", {})
    global LANE_W
    cols = sum(wide.get(l, 1) for l in lanes)
    LANE_W = 190 if cols <= 4 else 160          # 4 columns = the 760 px text column; 5 a little wider
    nw = LANE_W - 26
    for k in ("step", "status"): SIZE[k] = (nw, 50)
    SIZE["dec"] = (LANE_W - 14, 62)
    for k in ("start", "end", "fail", "skip"): SIZE[k] = (nw, 42)
    lane_x, x = {}, 0
    for l in lanes: lane_x[l] = x; x += wide.get(l, 1) * LANE_W
    rows = max(n["row"] for n in nodes) + 1
    H = HEAD_H + PAD_TOP + ROW_H * rows + 10
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    for i, lane in enumerate(lanes):
        cells.append(f'<mxCell id="lane{i}" value="{html.escape(lane)}" style="{LANE}" vertex="1" parent="1">'
                     f'<mxGeometry x="{lane_x[lane]}" y="0" width="{wide.get(lane, 1) * LANE_W}" height="{H}" as="geometry"/></mxCell>')
    cx = {}
    for n in nodes:
        k = n.get("kind", "step"); w, h = SIZE[k]
        c = lane_x[n["lane"]] + n.get("col", 0) * LANE_W + LANE_W / 2; cx[n["id"]] = c
        y = HEAD_H + PAD_TOP + n["row"] * ROW_H + (ROW_H - h) / 2 - 10
        label = html.escape(n["text"]).replace("\n", "&#xa;")   # a real line break in the plain-text label
        cells.append(f'<mxCell id="n_{n["id"]}" value="{label}" style="{STYLE[k]}{COMMON}" vertex="1" parent="1">'
                     f'<mxGeometry x="{c - w / 2:.0f}" y="{y:.0f}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    for i, e in enumerate(spec["edges"]):
        a, b = e[0], e[1]; lab = e[2] if len(e) > 2 and e[2] else ""; side = e[3] if len(e) > 3 else None
        st = EDGE + (SIDE[side] if side else "")
        if side == "bottom" and cx[a] != cx[b]:      # down, then sideways into the target's near side
            st += "entryX=1;entryY=0.5;" if cx[b] < cx[a] else "entryX=0;entryY=0.5;"
        if side in ("left", "right"):                # sideways, then down into the target's top
            st += "entryX=0.5;entryY=0;"
        cells.append(f'<mxCell id="edge{i}" value="{html.escape(lab)}" style="{st}" edge="1" parent="1" source="n_{a}" target="n_{b}">'
                     f'<mxGeometry relative="1" as="geometry"/></mxCell>')
    model = f'<mxGraphModel grid="0" page="0"><root>{"".join(cells)}</root></mxGraphModel>'
    return f'<mxfile><diagram name="{html.escape(spec["title"])}">{model}</diagram></mxfile>', model


LEGEND = [("start", "Начало", "событие, с которого\nвсё начинается"), ("step", "Действие", "делает участник\nэтой колонки"),
          ("dec", "Проверка?", "Да — дальше вниз,\nНет — в сторону"), ("status", "DEP-… / WD-…", "заявка меняет\nстатус"),
          ("end", "Итог", "чем закончилось"), ("fail", "Отказ", "проверка\nне пройдена"), ("skip", "Пропуск", "не учитывается")]

def legend():
    """One row of shapes with their meaning under each: the notation every diagram uses."""
    W, cells = 108, ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    for i, (k, t, d) in enumerate(LEGEND):
        w, h = (96, 56) if k == "dec" else (96, 38)
        x = i * W + (W - w) / 2
        cells.append(f'<mxCell id="l{i}" value="{html.escape(t)}" style="{STYLE[k]}fontFamily={FONT};fontSize=11;strokeWidth=1.5;" vertex="1" parent="1">'
                     f'<mxGeometry x="{x:.0f}" y="{(56 - h) / 2:.0f}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        cells.append(f'<mxCell id="d{i}" value="{html.escape(d).replace(chr(10), "&#xa;")}" style="text;html=0;align=center;verticalAlign=top;'
                     f'fontFamily={FONT};fontSize=11;fontColor=#475569;" vertex="1" parent="1"><mxGeometry x="{i * W}" y="62" width="{W}" height="34" as="geometry"/></mxCell>')
    return f'<mxGraphModel grid="0" page="0"><root>{"".join(cells)}</root></mxGraphModel>'


def render_svg(model, out_svg, title):
    """Render with the official draw.io viewer in headless Chrome and keep the SVG it draws."""
    cfg = json.dumps({"xml": model, "toolbar": "", "lightbox": False, "nav": False, "resize": False, "zoom": 1, "border": 0})
    page = os.path.join(HERE, "_render.html")
    open(page, "w", encoding="utf-8").write(
        '<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0;background:#fff">'
        f'<div class="mxgraph" style="width:2400px" data-mxgraph="{html.escape(cfg)}"></div>'
        '<script src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>'
        # frame the drawing itself: the bounding box of every shape, connector and label, in page coordinates
        '<script>setTimeout(function(){var s=document.querySelector(".mxgraph svg");var sr=s.getBoundingClientRect();'
        'var x1=1e9,y1=1e9,x2=-1e9,y2=-1e9;s.querySelectorAll("rect,path,ellipse,text,polygon").forEach(function(e){'
        'var r=e.getBoundingClientRect();if(!r.width&&!r.height)return;if(r.width>3000||r.height>3000)return;'
        'x1=Math.min(x1,r.left);y1=Math.min(y1,r.top);x2=Math.max(x2,r.right);y2=Math.max(y2,r.bottom);});'
        'var p=6,b={x:x1-sr.left,y:y1-sr.top,width:x2-x1,height:y2-y1};'
        's.setAttribute("viewBox",(b.x-p)+" "+(b.y-p)+" "+(b.width+2*p)+" "+(b.height+2*p));'
        's.setAttribute("width",Math.round(b.width+2*p));s.setAttribute("height",Math.round(b.height+2*p));'
        's.removeAttribute("style");document.body.setAttribute("data-done","1");},4000);</script></body></html>')
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", r"--user-data-dir=C:\Users\User\AppData\Local\Temp\zdrawio",
                        "--virtual-time-budget=15000", "--dump-dom", "file:///" + page.replace("\\", "/")],
                       capture_output=True, timeout=120)
    os.remove(page)
    dom = r.stdout.decode("utf-8", "replace")
    m = re.search(r"<svg[\s\S]*?</svg>", dom)
    if not m: raise SystemExit("draw.io viewer did not render " + out_svg)
    svg = m.group(0)
    if "xmlns=" not in svg[:200]: svg = svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    svg = svg.replace("<svg", f"<svg role=\"img\" aria-label=\"{html.escape(title)}\"", 1)
    # size from the viewBox / style so <img> knows it
    vb = re.search(r'viewBox="([-\d. ]+)"', svg)
    if vb:
        _, _, w, h = [float(v) for v in vb.group(1).split()]
        svg = re.sub(r'<svg([^>]*?)\swidth="[^"]*"', r'<svg\1', svg, count=1)
        svg = re.sub(r'<svg([^>]*?)\sheight="[^"]*"', r'<svg\1', svg, count=1)
        svg = svg.replace("<svg", f'<svg width="{w:.0f}" height="{h:.0f}"', 1)
    open(out_svg, "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>' + svg)
    return svg


if __name__ == "__main__":
    names = sys.argv[1:] or list(SPECS)
    src = os.path.join(HERE, "drawio"); os.makedirs(src, exist_ok=True)
    dst = os.path.join(HERE, "..", "public", "diagrams"); os.makedirs(dst, exist_ok=True)
    versions = {}
    if not sys.argv[1:] or "legend" in names:
        names = [n for n in names if n != "legend"]
        svg = render_svg(legend(), os.path.join(dst, "legend.svg"), "Обозначения на схемах")
        versions["legend"] = hashlib.sha1(svg.encode("utf-8")).hexdigest()[:8]
    for n in names:
        f, model = build(n, SPECS[n])
        open(os.path.join(src, n + ".drawio"), "w", encoding="utf-8").write(f)
        svg = render_svg(model, os.path.join(dst, n + ".svg"), SPECS[n]["title"])
        versions[n] = hashlib.sha1(svg.encode("utf-8")).hexdigest()[:8]
        print("rendered", n)
    docs = os.path.join(HERE, "..", "src", "content", "docs")
    for f in glob.glob(os.path.join(docs, "**", "*.md*"), recursive=True):
        t = open(f, encoding="utf-8").read()
        new = re.sub(r"\(/diagrams/([\w-]+)\.svg(\?v=\w+)?\)", lambda m: f"(/diagrams/{m.group(1)}.svg?v={versions.get(m.group(1), (m.group(2) or '?v=x')[3:])})", t)
        if new != t: open(f, "w", encoding="utf-8", newline="\n").write(new)
