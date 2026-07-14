# 来源登记

> 本项目是独立、非官方项目。链接和摘要只用于规则追溯，不替代目标 SDK 文档。

## 1. 来源等级

| 等级 | 含义 | 使用边界 |
| --- | --- | --- |
| H1 | 华为官方 HarmonyOS 设计/开发文档 | 版本与范围明确时可称官方要求或建议 |
| H2 | OpenHarmony 官方 UX、ArkUI、性能文档 | 称 OpenHarmony 官方；不可自动等同所有商业 HarmonyOS 版本 |
| H3 | 官方样例、系统应用或公开演讲观察 | 只能称观察模式或惯例 |
| H4 | 跨平台设计工程经验或项目 House Style | 只能称项目建议，不冒充官方 |

## 2. HarmonyOS / OpenHarmony 官方来源

| ID | 等级 | 标题 | 主要用途 |
| --- | --- | --- | --- |
| `HW-DESIGN-PORTAL` | H1 | 华为开发者联盟设计门户 | HarmonyOS 官方设计入口与后续核验 |
| `OH-UX-INDEX` | H2 | OpenHarmony 应用 UX 设计规范目录 | 设计知识结构 |
| `OH-UX-PRINCIPLES` | H2 | 应用 UX 设计原则 | 差异性、一致性、灵活性、兼容性 |
| `OH-NAV-STRUCTURE` | H2 | 应用导航结构设计要求 | 平级、层级、混合导航与层级深度 |
| `OH-ADAPTIVE-LAYOUT` | H2 | 自适应布局 | 拉伸、均分、缩放、延伸、隐藏、折行 |
| `OH-RESPONSIVE-LAYOUT` | H2 | 响应式布局 | 断点、缩进、挪移、重复 |
| `OH-GRID-SYSTEM` | H2 | 栅格系统 | Margin、Gutter、Column |
| `OH-HMI-BASIS` | H2 | 交互基础 | 输入方式与交互距离 |
| `OH-INPUT-MODES` | H2 | 常见输入方式 | 触摸、鼠标、键盘、手写笔、隔空手势 |
| `OH-VISUAL-BASIS` | H2 | 视觉基础 | vp、fp、8vp、分层参数 |
| `OH-VISUAL-COLORS` | H2 | 色彩 | 语义色彩与多端主题 |
| `OH-VISUAL-FONTS` | H2 | 字体 | 多设备字号层级 |
| `OH-MULTIMODAL-COMPONENTS` | H2 | 多态控件概述 | 正常、禁用、按下、焦点、激活、悬停 |
| `OH-DESIGN-CHECKLIST` | H2 | 设计自检表 | 必须/推荐的适配、单位、字体和状态要求 |
| `OH-MOTION-OVERVIEW` | H2 | 动效概述 | 生长动效与目的 |
| `OH-MOTION-PRINCIPLES` | H2 | 动效设计原则 | 自然流畅、简洁高效、快速响应、运动一致 |
| `OH-MOTION-ATTRIBUTES` | H2 | 动效属性 | 时长、曲线、弹簧、帧率 |
| `OH-TRANSITION` | H2 | 转场动效 | 层级、一镜到底、共享元素/容器/动势 |
| `OH-GESTURE-MOTION` | H2 | 手势动效 | 点击、滑动、翻动、捏合、拖拽 |
| `OH-ARKUI-SMOOTHING` | H2 | 动画衔接 | 动画打断、跟手与离手速度继承 |
| `OH-ARKUI-CURVES` | H2 | ArkUI curves API | Curve、springMotion、responsiveSpringMotion 等 |
| `OH-NAV-ANIMATION` | H2 | Navigation 转场动画 | 默认、自定义、共享转场 |
| `OH-ARKUI-ACCESSIBILITY` | H2 | ArkUI 无障碍 | 文本、说明、分组、状态、虚拟节点 |
| `OH-PERF-ANIMATION` | H2 | 合理使用动画 | 系统 API、Tabs、动效时延和帧率 |
| `OH-ANIMATION-PRACTICE` | H2 | 应用程序动效能力实践 | transition、图形变换、合并 animateTo |

## 3. 项目自有来源

| ID | 等级 | 内容 | 使用边界 |
| --- | --- | --- | --- |
| `HD-PROJECT-METHOD` | H4 | HarmonyOS-Design 项目方法与设计经验 | 项目基于跨平台设计工程经验形成的状态真实性、反同质化、知识分层与可执行原型方法；只能称项目建议或 House Style，不冒充官方 |

## 4. 完整链接

### H1

- `HW-DESIGN-PORTAL`  
  https://developer.huawei.com/consumer/cn/design/

### H2：UX

- `OH-UX-INDEX`  
  https://github.com/openharmony/docs/blob/master/zh-cn/design/ux-design/Readme-CN.md
- `OH-UX-PRINCIPLES`  
  https://github.com/openharmony/docs/blob/master/zh-cn/design/ux-design/app-ux-design.md
- `OH-NAV-STRUCTURE`  
  https://github.com/openharmony/docs/blob/master/zh-cn/design/ux-design/app-navigation-structure-design.md
- `OH-ADAPTIVE-LAYOUT`  
  https://github.com/openharmony/docs/blob/master/zh-cn/design/ux-design/adaptive-layout.md
- `OH-RESPONSIVE-LAYOUT`  
  https://github.com/openharmony/docs/blob/master/zh-cn/design/ux-design/responsive-layout.md
- `OH-GRID-SYSTEM`  
  https://github.com/openharmony/docs/blob/master/zh-cn/design/ux-design/grid-system.md
- `OH-HMI-BASIS`  
  https://github.com/openharmony/docs/blob/master/zh-cn/design/ux-design/human-machine-interaction-basis.md
- `OH-INPUT-MODES`  
  https://github.com/openharmony/docs/blob/master/zh-cn/design/ux-design/typical-input-modes.md
- `OH-VISUAL-BASIS`  
  https://github.com/openharmony/docs/blob/master/zh-cn/design/ux-design/visual-basis.md
- `OH-VISUAL-COLORS`  
  https://github.com/openharmony/docs/blob/master/zh-cn/design/ux-design/visual-colors.md
- `OH-VISUAL-FONTS`  
  https://github.com/openharmony/docs/blob/master/zh-cn/design/ux-design/visual-fonts.md
- `OH-MULTIMODAL-COMPONENTS`  
  https://github.com/openharmony/docs/blob/master/zh-cn/design/ux-design/multimodal-component-overview.md
- `OH-DESIGN-CHECKLIST`  
  https://github.com/openharmony/docs/blob/master/zh-cn/design/ux-design/design-checklist.md

### H2：动效与 ArkUI

- `OH-MOTION-OVERVIEW`  
  https://github.com/openharmony/docs/blob/master/zh-cn/design/ux-design/animation-overview.md
- `OH-MOTION-PRINCIPLES`  
  https://github.com/openharmony/docs/blob/master/zh-cn/design/ux-design/animation-design-principles.md
- `OH-MOTION-ATTRIBUTES`  
  https://github.com/openharmony/docs/blob/master/zh-cn/design/ux-design/animation-attributes.md
- `OH-TRANSITION`  
  https://github.com/openharmony/docs/blob/master/zh-cn/design/ux-design/transition-animation.md
- `OH-GESTURE-MOTION`  
  https://github.com/openharmony/docs/blob/master/zh-cn/design/ux-design/gesture-animation.md
- `OH-ARKUI-SMOOTHING`  
  https://github.com/openharmony/docs/blob/master/zh-cn/application-dev/ui/arkts-animation-smoothing.md
- `OH-ARKUI-CURVES`  
  https://github.com/openharmony/docs/blob/master/zh-cn/application-dev/reference/apis-arkui/js-apis-curve.md
- `OH-NAV-ANIMATION`  
  https://github.com/openharmony/docs/blob/master/zh-cn/application-dev/ui/arkts-navigation-animation.md
- `OH-ARKUI-ACCESSIBILITY`  
  https://github.com/openharmony/docs/blob/master/zh-cn/application-dev/ui/arkts-universal-attributes-accessibility.md
- `OH-PERF-ANIMATION`  
  https://github.com/openharmony/docs/blob/master/zh-cn/application-dev/performance/reasonable-using-animation.md
- `OH-ANIMATION-PRACTICE`  
  https://github.com/openharmony/docs/blob/master/zh-cn/application-dev/performance/animation_practice.md

## 5. 更新政策

每个版本发布前：

1. 判断来源属于永恒基础、版本化平台还是项目覆盖层；
2. 检查链接；
3. 核验 API 默认参数；
4. 核验 API Level；
5. 核验设备范围；
6. 更新核验日期；
7. 运行规则和 Eval；
8. 对已变化内容生成迁移说明。

若 H1 与 H2 发生冲突，目标商业 HarmonyOS 项目优先以适用版本的 H1 和本地 SDK 为准，并记录差异。
