#!/usr/bin/env python3
"""结题报告流程图：Visio 风格，网格对齐，正交连接线。"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, fontManager
from matplotlib.patches import FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "src" / "assets" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

W = 10.0
MARGIN = 0.35
CONTENT_W = W - 2 * MARGIN

C_FILL = "#DEEBF3"      # 浅蓝填充
C_FILL_WHITE = "#FFFFFF"
C_BORDER = "#2F5597"    # 深蓝描边
C_LINE = "#595959"      # 连接线
C_GROUP = "#A6A6A6"     # 虚线容器
C_TEXT_SUB = "#444444"


def pick_font():
    for name in ("Microsoft YaHei", "微软雅黑", "PingFang SC", "Songti SC", "STHeiti", "Heiti SC"):
        if name in {f.name for f in fontManager.ttflist}:
            return name
    raise RuntimeError("未找到中文字体")


FAMILY = pick_font()
F_TITLE = FontProperties(family=FAMILY, weight="bold", size=10)
F_BODY = FontProperties(family=FAMILY, size=9)
F_SMALL = FontProperties(family=FAMILY, size=8)


class Diagram:
    def __init__(self, height):
        self.h = height
        self.fig, self.ax = plt.subplots(figsize=(10, height))
        self.ax.set_xlim(0, W)
        self.ax.set_ylim(0, height)
        self.ax.set_axis_off()
        self.fig.patch.set_facecolor("white")

    def box(self, x, y, w, h, text, fc=C_FILL, fp=None, tc="#000000"):
        self.ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=C_BORDER, lw=1.1, zorder=2))
        self.ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                     fontproperties=fp or F_BODY, color=tc, zorder=3, linespacing=1.5)
        return (x, y, w, h)

    def titled_box(self, x, y, w, h, title, desc):
        self.ax.add_patch(Rectangle((x, y), w, h, fc=C_FILL, ec=C_BORDER, lw=1.1, zorder=2))
        self.ax.text(x + w / 2, y + h * 0.68, title, ha="center", va="center",
                     fontproperties=F_TITLE, zorder=3)
        self.ax.text(x + w / 2, y + h * 0.30, desc, ha="center", va="center",
                     fontproperties=F_SMALL, color=C_TEXT_SUB, zorder=3, linespacing=1.5)
        return (x, y, w, h)

    def arrow(self, p1, p2, *, zorder=4):
        self.ax.add_patch(FancyArrowPatch(
            p1, p2, arrowstyle="-|>", mutation_scale=11,
            linewidth=1.2, color=C_LINE, shrinkA=0, shrinkB=0, zorder=zorder))

    def v_arrow(self, x, y_high, y_low, *, pad=0.06):
        """垂直向下箭头：y_high > y_low（matplotlib y 轴向上）。"""
        y1, y2 = y_high - pad, y_low + pad
        if y1 <= y2:
            return
        self.line((x, y1), (x, y2 + 0.10))
        self.arrow((x, y2 + 0.10), (x, y2))

    def line(self, p1, p2, *, zorder=4):
        self.ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
                     color=C_LINE, lw=1.2, zorder=zorder, solid_capstyle="butt")

    def ortho_arrow(self, points):
        """折线连接，末段带箭头。"""
        for i in range(len(points) - 2):
            self.line(points[i], points[i + 1])
        self.arrow(points[-2], points[-1])

    def link_row(self, rects, gap=0.06):
        for a, b in zip(rects, rects[1:]):
            cy = a[1] + a[3] / 2
            self.arrow((a[0] + a[2] + gap, cy), (b[0] - gap, cy))

    def group_box(self, x, y, w, h, label=None):
        self.ax.add_patch(Rectangle((x, y), w, h, fc=C_FILL_WHITE, ec=C_GROUP,
                                    lw=1.0, zorder=1))
        if label:
            self.ax.text(x + 0.08, y + h + 0.06, label, ha="left", va="bottom",
                         fontproperties=F_SMALL, color=C_TEXT_SUB, zorder=3)

    def save(self, name):
        self.fig.savefig(OUT / name, dpi=220, facecolor="white",
                         bbox_inches="tight", pad_inches=0.08)
        plt.close(self.fig)
        print(f"  saved {name}")


def fig_teaching_flow():
    """图1 实验教学四环节流程。"""
    d = Diagram(1.35)
    steps = [
        ("课前准备", "熟悉系统、领取任务"),
        ("课中训练", "AIGC情景口语训练"),
        ("课后复盘", "回看录像、自评互评"),
        ("教师讲评", "现场点评、教师评分"),
    ]
    gap = 0.28
    n = len(steps)
    bw = (CONTENT_W - gap * (n - 1)) / n
    y, bh = 0.22, 0.92
    rects = []
    x = MARGIN
    for title, desc in steps:
        rects.append(d.titled_box(x, y, bw, bh, title, desc))
        x += bw + gap
    d.link_row(rects, gap=0.05)
    d.save("fig5-teaching-flow.png")


def fig_experiment_flow():
    """图2 实验教学流程。"""
    d = Diagram(3.55)
    cx = W / 2
    v_gap = 0.30

    f_w, f_h = 6.8, 0.62
    f_x = (W - f_w) / 2
    f_y = 0.34
    f_top = f_y + f_h

    c_x, c_w = MARGIN, CONTENT_W
    c_y = f_top + v_gap
    c_h = 0.90
    c_top = c_y + c_h

    r1_h = 0.64
    r1_y = c_top + v_gap

    gap1 = 1.0
    bw1 = (CONTENT_W - gap1) / 2
    x1 = MARGIN
    x2 = MARGIN + bw1 + gap1
    r1cy = r1_y + r1_h / 2

    d.titled_box(x1, r1_y, bw1, r1_h, "学生参与", "外语实验室教学")
    d.titled_box(x2, r1_y, bw1, r1_h, "AIGC情景实验环境", "开展实验教学")
    d.arrow((x1 + bw1 + 0.05, r1cy), (x2 - 0.05, r1cy))

    d.group_box(c_x, c_y, c_w, c_h, "三次口语训练")

    pad, t_gap = 0.28, 0.42
    inner_w = c_w - 2 * pad
    t_bw = (inner_w - 2 * t_gap) / 3
    t_y, t_h = c_y + 0.20, 0.54
    tasks = []
    x = c_x + pad
    for title, desc in (
        ("第一次", "口语训练"),
        ("第二次", "口语训练"),
        ("第三次", "口语训练"),
    ):
        tasks.append(d.titled_box(x, t_y, t_bw, t_h, title, desc))
        x += t_bw + t_gap
    d.link_row(tasks, gap=0.05)

    d.box(f_x, f_y, f_w, f_h,
          "观察记录：投入程度、表达欲望、参与兴趣度",
          fc=C_FILL_WHITE, fp=F_BODY)

    d.v_arrow(cx, r1_y, c_top)
    d.v_arrow(cx, c_y, f_top)

    d.save("fig4-experiment-flow.png")


def fig_org_structure():
    """图3 项目组织与分工结构图。"""
    d = Diagram(2.55)
    cx = W / 2
    top_w, top_h = 5.8, 0.56
    top_y = 1.88
    d.box(cx - top_w / 2, top_y, top_w, top_h,
          "外语实验室 AIGC情景实验教学项目", fp=F_TITLE)

    row_y, row_h = 0.98, 0.76
    roles = [
        ("授课教师", "任务发布、过程指导、课堂讲评"),
        ("实验教辅老师", "设备联调、现场协助、录像整理"),
        ("实验室管理人员", "系统维护、情景模板、操作说明"),
    ]
    gap = 0.30
    rbw = (CONTENT_W - gap * (len(roles) - 1)) / len(roles)
    rects = []
    x = MARGIN
    for title, desc in roles:
        rects.append(d.titled_box(x, row_y, rbw, row_h, title, desc))
        x += rbw + gap

    stu_y, stu_h = 0.22, 0.50
    stu_w = 4.0
    d.box(cx - stu_w / 2, stu_y, stu_w, stu_h, "学生参与课堂训练", fp=F_BODY)

    bus_top = top_y - 0.08
    bus_mid = row_y + row_h + 0.08
    bus_bot = stu_y + stu_h + 0.08

    d.line((cx, top_y), (cx, bus_top))
    left_cx = rects[0][0] + rects[0][2] / 2
    right_cx = rects[-1][0] + rects[-1][2] / 2
    d.line((left_cx, bus_top), (right_cx, bus_top))
    for rx, ry, rw, rh in rects:
        rcx = rx + rw / 2
        d.v_arrow(rcx, bus_top, ry + rh, pad=0.04)

    d.line((left_cx, bus_mid), (right_cx, bus_mid))
    for rx, ry, rw, rh in rects:
        rcx = rx + rw / 2
        d.line((rcx, ry), (rcx, bus_mid))
    d.v_arrow(cx, bus_mid, stu_y + stu_h, pad=0.04)

    d.save("fig3-org-structure.png")


def fig_platform_ui():
    """图4 AIGC情景实验平台界面示意。"""
    d = Diagram(3.1)
    win_x, win_y = 0.55, 0.28
    win_w, win_h = 8.9, 2.55
    d.ax.add_patch(Rectangle((win_x, win_y), win_w, win_h, fc=C_FILL_WHITE,
                             ec=C_BORDER, lw=1.2, zorder=1))
    d.ax.text(win_x + win_w / 2, win_y + win_h - 0.22,
              "AIGC情景实验教学平台", ha="center", va="center",
              fontproperties=F_TITLE, zorder=3)

    bar_h = 0.34
    d.ax.add_patch(Rectangle((win_x, win_y + win_h - bar_h), win_w, bar_h,
                             fc=C_FILL, ec=C_BORDER, lw=0.8, zorder=2))

    pad = 0.18
    inner_y = win_y + pad
    inner_h = win_h - bar_h - 2 * pad
    col_gap = 0.16
    col_w = (win_w - 2 * pad - 2 * col_gap) / 3
    x = win_x + pad

    panels = [
        ("任务与情景", "选择训练轮次\n切换情景模板"),
        ("训练画面", "虚拟角色预览\n口语表达录制"),
        ("回看与控制", "录像回放\n参数与状态"),
    ]
    for title, desc in panels:
        d.group_box(x, inner_y, col_w, inner_h, label=title)
        d.ax.text(x + col_w / 2, inner_y + inner_h * 0.38, desc,
                  ha="center", va="center", fontproperties=F_SMALL,
                  color=C_TEXT_SUB, zorder=3, linespacing=1.5)
        x += col_w + col_gap

    d.ax.text(win_x + win_w / 2, win_y - 0.12,
              "界面为示意结构，实际以实验室部署版本为准",
              ha="center", va="top", fontproperties=F_SMALL,
              color=C_TEXT_SUB, zorder=3)

    d.save("fig6-platform-ui.png")


if __name__ == "__main__":
    import sys

    print(f"Using font: {FAMILY}")
    targets = set(sys.argv[1:]) if len(sys.argv) > 1 else {"fig1", "fig2"}
    if "fig1" in targets:
        fig_teaching_flow()
    if "fig2" in targets:
        fig_experiment_flow()
    if "fig3" in targets:
        fig_org_structure()
    if "fig4ui" in targets:
        fig_platform_ui()
    print(f"Done → {OUT}")
