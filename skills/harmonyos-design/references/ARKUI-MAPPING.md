# ArkUI 实现映射

> 状态：V0.2 草案  
> 目标：把设计判断映射为 ArkTS / ArkUI 能力，而不是提供未经验证的完整组件库。  
> 最后核验：2026-07-11

## 1. 总体选择顺序

```text
系统组件默认能力
→ 组件属性和状态
→ transition / animateTo
→ springMotion 等原生曲线
→ Navigation / geometryTransition
→ AttributeModifier / @Styles / @Extend
→ 自定义手势或 Animator
→ 自绘
```

越靠后，越需要证明系统能力不足，并承担性能、状态、适配和无障碍责任。

## 2. 出现和消失

优先 `transition`。

公开性能资料指出，使用 `transition` 处理条件组件出现/消失通常比通过 `animateTo` 加结束回调再删除组件更简单、更新更少。

示意：

```ts
if (this.show) {
  Text('内容')
    .id('content')
    .transition(
      TransitionEffect.OPACITY.animation({ duration: 150 })
    )
}
```

数值仅为示意 House Style；项目应从语义 Token 读取。

检查：

- id 是否稳定；
- 进入与退出是否表达同一关系；
- 快速切换是否可打断；
- 是否只为结束回调而使用复杂状态；
- 无障碍树是否及时更新。

## 3. `animateTo`

适用：

- 明确状态变化；
- 多个属性共享同一参数；
- 路由操作配合自定义动画；
- 需要完成回调但不依赖物理曲线固定时长。

推荐：

```ts
this.getUIContext()?.animateTo({
  duration: MotionTokens.duration.local,
  curve: Curve.FastOutSlowIn
}, () => {
  this.offsetX = targetX
  this.opacity = targetOpacity
})
```

要求：

- 同参数属性放入同一闭包；
- 避免多个 `animateTo` 之间插入冗余状态更新；
- 不用 `setTimeout` 手写逐帧；
- 业务完成不依赖视觉完成。

## 4. 属性动画 `.animation()`

适用：属性目标由状态变化驱动，且该组件的相关属性需要持续使用同一曲线。

```ts
.scale({ x: this.scale, y: this.scale })
.animation({ curve: curves.springMotion() })
```

注意：

- 属性动画作用范围与链式顺序需要核验；
- 避免一个组件上难以理解的多段 `.animation()`；
- 快速连续目标变化要检查衔接；
- 系统默认已有动画时避免重复叠加。

## 5. 跟手和离手

### 跟手

```ts
this.getUIContext()?.animateTo({
  curve: curves.responsiveSpringMotion()
}, () => {
  this.positionX = nextX
  this.positionY = nextY
})
```

### 离手回稳

```ts
this.getUIContext()?.animateTo({
  curve: curves.springMotion()
}, () => {
  this.positionX = targetX
  this.positionY = targetY
})
```

公开文档说明该组合可在离手阶段继承跟手阶段速度。

检查：

- Gesture Update 是否高频执行耗时任务；
- 抓取偏移是否正确；
- 多点触控是否导致跳变；
- 边界阻尼；
- 目标点和速度单位；
- 快速反向。

## 6. 自定义弹簧

```ts
curves.interpolatingSpring(velocity, mass, stiffness, damping)
```

适用：

- 需要显式物理参数；
- 默认 `springMotion` 无法满足；
- 有真机调试和测试。

注意：

- velocity 是归一化速度；
- 物理时长不由 `duration` 控制；
- 参数必须进入 Token，并标来源；
- 不用未经验证的其他平台参数直接替换。

## 7. 图形变换与布局

连续位置或大小变化优先：

- `.translate()`；
- `.scale()`；
- `.rotate()`；
- 其他图形变换。

避免在手势帧中频繁修改：

- `.width()`；
- `.height()`；
- 布局权重；
- 大范围约束。

公开性能文档指出，布局属性变化会重新测量布局，而图形变换不会重新触发布局，持续动画时性能通常更好。

例外：最终布局和可访问几何必须真实更新，不能永远用视觉变换伪装布局。

## 8. Navigation

### 默认转场

Navigation 默认转场使用弹簧，具体表现可因设备而不同。不要把默认动画时长与业务逻辑耦合。

### 关闭动画

公开接口包括：

```ts
this.pageStack.disableAnimation(true)
```

或在单次 `pushPath`、`pop`、`replacePath` 等操作中设置是否动画。

只在以下场景关闭：

- 共享转场会与默认转场叠加；
- 高频键盘路径；
- 低运动替代；
- 特定任务不需要动画。

不要全局关闭后遗漏空间关系。

### 自定义转场

公开能力包括：

- `customNavContentTransition`；
- `NavDestination.customTransition`；
- 可交互转场协议。

自定义前先说明：

- 层级关系；
- 进入、返回和中断；
- timeout；
- 焦点；
- 默认转场优先级；
- 多设备差异。

## 9. 共享元素

```ts
Image(...)
  .geometryTransition('sharedId')
```

两端 ID 保持一致，并把路由操作放入合适的动画闭包。

Gotcha：配置共享元素时通常需要关闭系统默认转场，否则可能发生叠加。

## 10. Tabs

检查：

- 默认切换动画；
- `animationDuration` 是否符合任务频率；
- 设置为 0 时目标 API 的实际行为；
- 手机底部 Tab 与宽屏侧边导航的转换；
- 选中态、焦点态和无障碍 selected；
- 键盘高频切换是否需要减弱或关闭动画。

不要把性能文档中的单一示例值直接写成统一 Token。

## 11. 语义样式封装

### `@Styles` / `@Extend`

适合无状态或轻量复用样式。

### `AttributeModifier`

适合动态视觉属性、复杂行为或列表项状态封装。

建议名称：

- `PressFeedback`；
- `RowFeedback`；
- `FocusFeedback`；
- `StaggeredEntrance`；
- `SharedContainerTransition`；
- `MotionPolicy`。

不要使用：

- `style1`；
- `niceAnimation`；
- `fastSpring`；
- 仅以具体数值命名。

## 12. 视觉资源

布局和字体：

- `vp`：布局尺寸；
- `fp`：字体尺寸；
- 8vp 基础网格，细节可用 4vp；
- 使用语义资源管理颜色、字体、圆角、间距、阴影和模糊。

避免：

- 业务页面散落裸色值；
- 字体用固定 `vp` 规避动态字号；
- 同一语义在浅/深主题使用同一不可读值；
- 所有设备共用同一具体圆角和密度。

## 13. 无障碍属性

| 需求 | ArkUI 能力 |
| --- | --- |
| 非文本功能名称 | `accessibilityText` |
| 后果或补充说明 | `accessibilityDescription` |
| 是否被辅助工具识别 | `accessibilityLevel` |
| 控件角色 | `accessibilityRole` |
| 勾选状态 | `accessibilityChecked` |
| 互斥选择状态 | `accessibilitySelected` |
| 组合内容 | `accessibilityGroup` |
| 自绘语义 | `accessibilityVirtualNode` |

API 范围以目标 SDK 文档和编译为准。

## 14. 异步状态映射

建议业务状态模型：

```ts
enum SubmissionState {
  Idle,
  Pending,
  Confirmed,
  Failed
}
```

设计要求：

- 按下反馈不修改为 Confirmed；
- Pending 有明确视觉和语义；
- Confirmed 由真实结果驱动；
- Failed 保留错误与重试信息；
- 请求 ID 防止乱序覆盖；
- 视觉动画只是状态渲染，不是状态来源。

具体状态管理实现取决于项目，不在 Skill 中强制某个框架。

## 15. 性能工具

公开文档列出的工具和方向包括：

- ArkUI Inspector；
- CPU Profiler；
- SmartPerf-Host；
- HiDumper；
- Trace；
- 长帧分析；
- 状态变量更新定位。

最低验证：

- 真实设备；
- Release 或接近发布配置；
- 快速连续输入；
- 大数据列表；
- 转场中后台任务；
- 模糊和复杂绘制场景。

## 16. API 使用前检查

1. 目标 API Level；
2. Stage 模型要求；
3. Phone/Tablet/其他设备支持；
4. 默认参数；
5. `duration` 是否生效；
6. 与默认组件行为冲突；
7. 无障碍树；
8. 真机性能；
9. 文档最后核验日期。
