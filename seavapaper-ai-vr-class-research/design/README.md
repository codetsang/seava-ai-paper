# 流程图工作流（Pencil）

源文件：`design/design.pen`（在 Pencil 画布中打开编辑）

## 导出到报告

1. 在 Pencil 中修改 `design.pen`
2. 让 Agent 执行 `export_nodes` 导出 PNG
3. 覆盖到：
   - `src/assets/figures/fig5-teaching-flow.png`（图1）
   - `src/assets/figures/fig4-experiment-flow.png`（图2）
4. `npm run dev` 预览报告

当前帧 ID（导出用）：

| 帧名 | 节点 ID | 输出文件 |
|------|---------|----------|
| 图1 实验教学四环节流程 | `GUUBI` | `fig5-teaching-flow.png` |
| 图2 实验教学流程 | `bX1US` | `fig4-experiment-flow.png` |

## 命令

```bash
npm run dev                 # 预览 HTML 报告
npm run build               # 构建（使用已导出的 PNG）
npm run generate:figures    # 生成图1、图2 PNG
```
