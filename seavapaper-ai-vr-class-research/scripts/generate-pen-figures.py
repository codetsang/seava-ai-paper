#!/usr/bin/env python3
"""Generate Visio-style flowcharts as Pencil .pen JSON (design/report-figures.pen)."""

import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "design" / "design.pen"

W = 1000
MARGIN_L = 35
CONTENT_W = W - 70

C_BLUE_LIGHT = "#DEEBF3"
C_BORDER = "#2F5597"
C_LINE = "#595959"
C_FILL = "#FFFFFF"
FONT = "Songti SC"


def nid(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:6]}"


def stroke(color: str = C_BORDER, thickness: int = 1) -> dict:
    return {"align": "inside", "thickness": thickness, "fill": color}


def text_node(
    x: float,
    y: float,
    w: float,
    content: str,
    *,
    size: float = 14,
    color: str = "#000000",
    weight: str = "normal",
) -> dict:
    lines = content.count("\n") + 1
    line_h = size * 1.35
    ty = y + max(4, (48 - lines * line_h) / 2) if lines <= 3 else y + 8
    return {
        "type": "text",
        "id": nid("t"),
        "x": x,
        "y": ty,
        "width": w,
        "content": content,
        "fontFamily": FONT,
        "fontSize": size,
        "fontWeight": weight,
        "fill": color,
        "textAlign": "center",
        "textGrowth": "fixed-width",
        "lineHeight": 1.35,
    }


def box_node(
    x: float,
    y: float,
    w: float,
    h: float,
    label: str,
    *,
    fc: str = C_FILL,
    ec: str = C_BORDER,
    size: float = 14,
    weight: str = "normal",
) -> list[dict]:
    bid = nid("b")
    return [
        {
            "type": "rectangle",
            "id": bid,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "fill": fc,
            "cornerRadius": 2,
            "stroke": stroke(ec),
        },
        text_node(x, y, w, label, size=size, weight=weight),
    ]


def path_line(points: list[tuple[float, float]], *, arrow: bool = True) -> dict:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    d = " ".join(f"{'M' if i == 0 else 'L'} {x} {y}" for i, (x, y) in enumerate(points))
    node = {
        "type": "path",
        "id": nid("p"),
        "x": min(xs),
        "y": min(ys),
        "width": max(max(xs) - min(xs), 1),
        "height": max(max(ys) - min(ys), 1),
        "geometry": d,
        "stroke": stroke(C_LINE),
    }
    if arrow and len(points) >= 2:
        x1, y1 = points[-2]
        x2, y2 = points[-1]
        dx, dy = x2 - x1, y2 - y1
        length = (dx * dx + dy * dy) ** 0.5 or 1
        ux, uy = dx / length, dy / length
        px, py = -uy, ux
        tip = 7
        wing = 4
        ax, ay = x2, y2
        p1 = (ax - ux * tip + px * wing, ay - uy * tip + py * wing)
        p2 = (ax - ux * tip - px * wing, ay - uy * tip - py * wing)
        node["geometry"] += f" M {p1[0]} {p1[1]} L {ax} {ay} L {p2[0]} {p2[1]}"
    return node


def row_boxes(
    y: float,
    h: float,
    labels: list[str],
    *,
    gap: float = 18,
    fc: str = C_BLUE_LIGHT,
    size: float = 14,
) -> tuple[list[dict], list[tuple[float, float, float, float]]]:
    n = len(labels)
    gap_total = gap * (n - 1)
    bw = (CONTENT_W - gap_total) / n
    nodes: list[dict] = []
    rects: list[tuple[float, float, float, float]] = []
    x = MARGIN_L
    for label in labels:
        nodes.extend(box_node(x, y, bw, h, label, fc=fc, size=size))
        rects.append((x, y, bw, h))
        x += bw + gap
    return nodes, rects


def link_row(rects: list[tuple[float, float, float, float]], cy: float) -> list[dict]:
    lines = []
    for a, b in zip(rects, rects[1:]):
        x1 = a[0] + a[2]
        x2 = b[0]
        lines.append(path_line([(x1 + 2, cy), (x2 - 2, cy)]))
    return lines


def frame(name: str, fid: str, y_offset: float, height: float, children: list[dict]) -> dict:
    return {
        "type": "frame",
        "id": fid,
        "name": name,
        "x": 0,
        "y": y_offset,
        "width": W,
        "height": height,
        "fill": "#FFFFFF",
        "layout": "none",
        "clip": False,
        "children": children,
    }


def build_fig4_experiment() -> dict:
    nodes: list[dict] = []

    r1_nodes, r1 = row_boxes(
        19,
        66,
        ["学生参与\n外语实验室教学", "AIGC情景实验环境"],
        gap=120,
        fc=C_FILL,
        size=13,
    )
    nodes.extend(r1_nodes)
    nodes.extend(link_row(r1, 52))

    c_x, c_y, c_w, c_h = MARGIN_L, 135, CONTENT_W, 90
    nodes.append({
        "type": "rectangle",
        "id": nid("b"),
        "x": c_x,
        "y": c_y,
        "width": c_w,
        "height": c_h,
        "fill": "#FFFFFF",
        "cornerRadius": 2,
        "stroke": stroke("#A6A6A6"),
    })
    nodes.append(text_node(c_x, c_y - 14, c_w, "三次口语训练", size=11, color="#444444"))
    t_gap, t_bw = 50, (c_w - 40 - 100) / 3
    t_y, t_h = 175, 52
    t_rects = []
    x = c_x + 20
    for label in ("第一次\n口语训练", "第二次\n口语训练", "第三次\n口语训练"):
        nodes.extend(box_node(x, t_y, t_bw, t_h, label, fc=C_BLUE_LIGHT, size=12))
        t_rects.append((x, t_y, t_bw, t_h))
        x += t_bw + t_gap
    nodes.extend(link_row(t_rects, t_y + t_h / 2))

    src_cx = r1[1][0] + r1[1][2] / 2
    nodes.append(path_line([(src_cx, 85), (src_cx, c_y + c_h)]))

    f_w, f_h = 540, 62
    f_x = MARGIN_L + (CONTENT_W - f_w) / 2
    f_y = 288
    nodes.extend(box_node(f_x, f_y, f_w, f_h, "观察记录：投入程度、表达欲望、参与兴趣度", fc=C_FILL, size=13))
    nodes.append(path_line([(c_x + c_w / 2, c_y + c_h), (c_x + c_w / 2, f_y)]))

    return frame("图2 实验教学流程", "fig4Experiment", 0, 380, nodes)


def build_fig5_teaching() -> dict:
    nodes: list[dict] = []
    labels = [
        "课前准备\n熟悉系统、领取任务",
        "课中训练\nAIGC情景口语训练",
        "课后复盘\n回看录像、自评互评",
        "教师讲评\n现场点评、教师评分",
    ]
    gap = 50
    n = len(labels)
    bw = (CONTENT_W - gap * (n - 1)) / n
    rects: list[tuple[float, float, float, float]] = []
    x = MARGIN_L
    y, bh = 30, 100
    for label in labels:
        nodes.extend(box_node(x, y, bw, bh, label, fc=C_BLUE_LIGHT, size=13))
        rects.append((x, y, bw, bh))
        x += bw + gap
    nodes.extend(link_row(rects, y + bh / 2))
    return frame("图1 实验教学四环节流程", "fig5Teaching", 520, 160, nodes)


def main() -> None:
    doc = {
        "version": "2.8",
        "children": [
            build_fig4_experiment(),
            build_fig5_teaching(),
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
