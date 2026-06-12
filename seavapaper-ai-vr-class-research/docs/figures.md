# 插图说明

## 流程图（2 张）

| 图号 | 文件 | 内容 | 源文件 |
|------|------|------|--------|
| 图1 | `fig5-teaching-flow.png` | 实验教学四环节流程 | `design/design.pen` |
| 图2 | `fig4-experiment-flow.png` | 实验教学流程 | `design/design.pen` |

在 Pencil 中编辑 `design/design.pen` 后导出 PNG 到 `src/assets/figures/`。

流程图无外层标题栏、脚注框及页面边框，标题仅出现在图注中。

图3 为 ECharts 动态图表，见 `src/components/MultiRoundEffectChart.jsx`。

## 命令

```bash
npm run dev
npm run build
```

备用：`npm run generate:figures`（Matplotlib，会覆盖 Pencil 导出的 PNG）
