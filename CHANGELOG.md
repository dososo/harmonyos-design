# 变更日志

本项目遵循[语义化版本](https://semver.org/lang/zh-CN/)。

## 1.0.0

首个公开发布。

### Skill

- `harmonyos-design`：主 Skill，支持设计 / 实现 / 审视三模式与「新项目启动 / 现有项目审视」双入口；
- `review-harmonyos-design`：严格 Reviewer，只审不改、通过需证据、给规则 ID 与结论门槛；
- `harmonyos-motion-vocabulary`：把模糊动效感受映射为精确术语与 ArkUI 能力。

### 规则与来源

- 38 条机器可读规则，覆盖导航、适配、交互、动效、异步真实性、视觉、无障碍、性能；
- JSON Schema 校验，稳定规则 ID，来源分级 H1–H4，数值类型标注；
- 来源登记只保留 HarmonyOS / OpenHarmony 官方来源与项目自有方法，H3/H4 不冒充官方；
- 自动修复默认全部关闭。

### 评测

- 52 条触发 Eval（正 26 / 负 26）、17 条 Review Eval、13 条 Skill 路由 Eval；
- ArkTS 正反例 fixtures。

### 示例与工具

- 可运行 ArkUI 示例工程 `examples/pilot-app/`，含异步真实性、手势速度、平板适配、无障碍 4 类场景，已在 HarmonyOS 模拟器（API 21）真机运行验证；
- 离线校验工具（Skill / 规则 / 来源 / Eval / 链接 / 打包）与单元测试。

### 原则

- 异步状态真实性、反同质化、三层知识架构（永恒基础 / 版本化平台 / 项目覆盖）、系统能力优先、证据可追溯；
- 默认离线、只读、不采集，不写用户工程。
