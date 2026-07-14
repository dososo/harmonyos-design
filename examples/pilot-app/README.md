# pilot-app — HarmonyOS 设计场景示例工程

一个可运行的 ArkUI 示例工程，用 Tabs 聚合 4 类设计场景的**正确实现**，可在模拟器或真机上直接运行查看效果。

## 场景组件

| 组件 | 场景 | 规则 |
| --- | --- | --- |
| `AsyncSaveDemo.ets` | 异步状态真实性：成功只在真实结果后出现，Pending 禁用防重复提交 | HD-ASYNC-001/002、HD-A11Y-003 |
| `GestureVelocityDemo.ets` | 手势离手用 springMotion 继承速度回稳 | HD-MOTION-004/006 |
| `AdaptiveLayoutDemo.ets` | GridRow 响应式断点分栏（手机 2 列 / 平板 4–6 列） | HD-ADAPT-001/002 |
| `A11yButtonDemo.ets` | Button 承载图标 + accessibilityText 可访问名称 | HD-A11Y-001 |

## 构建与运行

```bash
# 工程路径需为英文（hvigor 不支持中文路径）
export DEVECO_SDK_HOME="/path/to/DevEco-Studio/Contents/sdk"
export PATH="$DEVECO_SDK_HOME/../tools/node/bin:$DEVECO_SDK_HOME/../tools/hvigor/bin:$DEVECO_SDK_HOME/../tools/ohpm/bin:$PATH"
ohpm install
hvigorw assembleHap --mode module -p product=default
# 产物：entry/build/default/outputs/default/*.hap
# 安装到已启动的模拟器：hdc install <hap>
```

SDK：HarmonyOS API 21（6.0.1）。`build/`、`oh_modules/`、`.hvigor/` 等为生成物，已被 `.gitignore` 忽略。四个场景的真机运行截图见仓库 README 的「真机运行示例」。
