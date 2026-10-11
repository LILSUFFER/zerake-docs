# Swimlane (cross-functional) flowcharts as SVG: one column per participant, one row per step,
# right-angle arrows, ovals for start/end, diamonds for decisions — the classic process-diagram style.
# Usage: python diagrams/swimlane.py   (writes public/diagrams/*.svg from SPECS in diagrams/specs.py)
import html, os, sys

LANE_W, HEAD_H, ROW_H, TOP = 190, 40, 84, 8
STEP_W, STEP_H = 162, 46
DEC_W, DEC_H = 176, 64
PILL_W, PILL_H = 154, 38
FONT = "Segoe UI, -apple-system, Roboto, Helvetica, Arial, sans-serif"
C = {
    "lane_bg": "#ffffff", "lane_line": "#94a3b8", "head_bg": "#f1f4f9", "head_text": "#1e293b",
    "step_fill": "#ece6ff", "step_line": "#8b5cf6", "step_text": "#3b2a7a",
    "dec_fill": "#fde2e4", "dec_line": "#e0565f", "dec_text": "#7a1f2b",
    "start_fill": "#c7f2e4", "start_line": "#12a477", "start_text": "#0b3d2c",
    "end_fill": "#e3f6c8", "end_line": "#7cb342", "end_text": "#2f4a12",
    "bad_fill": "#fff1f2", "bad_line": "#e0565f", "bad_text": "#7a1f2b",
    "ok_fill": "#12a477", "ok_line": "#0f8a63", "ok_text": "#ffffff",
    "edge": "#1f2937", "edge_label": "#334155",
}


def esc(s): return html.escape(s, quote=True)


def center(lanes, n):
    return LANE_W * lanes.index(n["lane"]) + LANE_W / 2, TOP + HEAD_H + ROW_H * n["row"] + ROW_H / 2


def size(n):
    k = n.get("kind", "step")
    return {"dec": (DEC_W, DEC_H), "start": (PILL_W, PILL_H), "end": (PILL_W, PILL_H)}.get(k, (STEP_W, STEP_H))


def text_block(x, y, txt, color, size_px=14, weight=500):
    lines = txt.split("\n"); lh = size_px * 1.25; y0 = y - lh * (len(lines) - 1) / 2
    return "".join(f'<text x="{x:.1f}" y="{y0 + i * lh:.1f}" text-anchor="middle" dominant-baseline="central" font-size="{size_px}" font-weight="{weight}" fill="{color}">{esc(l)}</text>' for i, l in enumerate(lines))


def node_svg(lanes, n):
    x, y = center(lanes, n); w, h = size(n); k = n.get("kind", "step")
    if k == "dec":
        pts = f"{x},{y - h / 2} {x + w / 2},{y} {x},{y + h / 2} {x - w / 2},{y}"
        return f'<polygon points="{pts}" fill="{C["dec_fill"]}" stroke="{C["dec_line"]}" stroke-width="1.6"/>' + text_block(x, y, n["text"], C["dec_text"], 12)
    pal = {"start": "start", "end": "end", "bad": "bad", "ok": "ok"}.get(k, "step")
    r = h / 2 if k in ("start", "end") else 4
    return (f'<rect x="{x - w / 2:.1f}" y="{y - h / 2:.1f}" width="{w}" height="{h}" rx="{r}" fill="{C[pal + "_fill"]}" stroke="{C[pal + "_line"]}" stroke-width="1.6"/>'
            + text_block(x, y, n["text"], C[pal + "_text"], 13, 600 if k == "ok" else 500))


def port(lanes, n, side):
    x, y = center(lanes, n); w, h = size(n)
    return {"top": (x, y - h / 2), "bottom": (x, y + h / 2), "left": (x - w / 2, y), "right": (x + w / 2, y)}[side]


def route(lanes, a, b, out=None):
    """Right-angle path from a to b. Same lane: vertical. Same row: horizontal. Otherwise: out of a's side, then down/up into b."""
    ax, ay = center(lanes, a); bx, by = center(lanes, b)
    la, lb = lanes.index(a["lane"]), lanes.index(b["lane"])
    if la == lb and not out:
        p, q = (port(lanes, a, "bottom"), port(lanes, b, "top")) if by > ay else (port(lanes, a, "top"), port(lanes, b, "bottom"))
        return [p, q]
    if a["row"] == b["row"] and not out:
        return [port(lanes, a, "right"), port(lanes, b, "left")] if lb > la else [port(lanes, a, "left"), port(lanes, b, "right")]
    side = out or ("right" if lb > la else "left" if lb < la else "bottom")
    p = port(lanes, a, side)
    if side in ("left", "right"):
        q = port(lanes, b, "top" if by > ay else "bottom")
        return [p, (q[0], p[1]), q]
    # out of the bottom, then sideways at the target's row, into its side
    q = port(lanes, b, "left" if bx > ax else "right")
    return [p, (p[0], q[1]), q]


def edge_svg(pts, label=None):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    s = f'<path d="{d}" fill="none" stroke="{C["edge"]}" stroke-width="1.6" marker-end="url(#arr)"/>'
    if label:
        (x1, y1), (x2, y2) = pts[0], pts[1]
        w = 9 * len(label) + 14
        if abs(x2 - x1) > abs(y2 - y1):
            if abs(x2 - x1) < w + 40: lx, ly = (x1 + x2) / 2, y1 - 14      # short segment: label above the line
            else: lx, ly = x1 + (x2 - x1) * 0.42, y1
        else:
            if abs(y2 - y1) < 50: lx, ly = x1 + w / 2 + 8, (y1 + y2) / 2    # short segment: label beside the line
            else: lx, ly = x1, y1 + (y2 - y1) * 0.45
        s += (f'<rect x="{lx - w / 2:.1f}" y="{ly - 11:.1f}" width="{w}" height="22" rx="4" fill="#ffffff"/>'
              f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" dominant-baseline="central" font-size="12" font-weight="500" fill="{C["edge_label"]}">{esc(label)}</text>')
    return s


def render(spec):
    # five or more lanes: narrower lanes and blocks so the whole diagram still fits the 760 px text column
    global LANE_W, STEP_W, DEC_W, PILL_W
    LANE_W = min(190, 760 // len(spec["lanes"]))
    STEP_W, DEC_W, PILL_W = LANE_W - 28, LANE_W - 12, LANE_W - 34
    lanes = spec["lanes"]; nodes = {n["id"]: n for n in spec["nodes"]}
    rows = max(n["row"] for n in nodes.values()) + 1
    W, H = LANE_W * len(lanes), TOP + HEAD_H + ROW_H * rows + 16
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">',
           f'<title>{esc(spec["title"])}</title>',
           '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
           f'<path d="M0,0 L10,5 L0,10 z" fill="{C["edge"]}"/></marker></defs>',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    # lanes: header strip + vertical separators
    out.append(f'<rect x="0.8" y="{TOP}" width="{W - 1.6}" height="{H - TOP - 10}" fill="{C["lane_bg"]}" stroke="{C["lane_line"]}" stroke-width="1.4"/>')
    out.append(f'<rect x="0.8" y="{TOP}" width="{W - 1.6}" height="{HEAD_H}" fill="{C["head_bg"]}" stroke="{C["lane_line"]}" stroke-width="1.4"/>')
    for i, name in enumerate(lanes):
        if i: out.append(f'<line x1="{LANE_W * i}" y1="{TOP}" x2="{LANE_W * i}" y2="{H - 10}" stroke="{C["lane_line"]}" stroke-width="1.4"/>')
        out.append(text_block(LANE_W * i + LANE_W / 2, TOP + HEAD_H / 2, name, C["head_text"], 14, 600))
    for e in spec["edges"]:
        a, b = nodes[e[0]], nodes[e[1]]
        out.append(edge_svg(route(lanes, a, b, e[3] if len(e) > 3 else None), e[2] if len(e) > 2 else None))
    for n in nodes.values():
        out.append(node_svg(lanes, n))
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    from specs import SPECS
    from specs2 import SPECS2
    SPECS = {**SPECS, **SPECS2}
    dst = os.path.join(here, "..", "public", "diagrams"); os.makedirs(dst, exist_ok=True)
    import glob, hashlib, re
    versions = {}
    for name, spec in SPECS.items():
        svg = render(spec)
        open(os.path.join(dst, name + ".svg"), "w", encoding="utf-8").write(svg)
        versions[name] = hashlib.sha1(svg.encode("utf-8")).hexdigest()[:8]
        print("wrote", name)
    # every page links its diagrams with ?v=<content hash>, so a browser never shows an old cached picture
    docs = os.path.join(here, "..", "src", "content", "docs")
    for f in glob.glob(os.path.join(docs, "**", "*.md*"), recursive=True):
        t = open(f, encoding="utf-8").read()
        n = re.sub(r"\(/diagrams/([\w-]+)\.svg(\?v=\w+)?\)", lambda m: f"(/diagrams/{m.group(1)}.svg?v={versions.get(m.group(1), 'x')})", t)
        if n != t: open(f, "w", encoding="utf-8", newline="\n").write(n)
