# 贡献指南

感谢参与 HarmonyOS-Design。本项目的目标不是快速堆积规则，而是维护少量、可信、可执行、可验证的设计判断。

## 一、贡献类型

- 修正规则来源或适用范围；
- 新增高价值规则；
- 增加 Trigger / Review Eval；
- 提交真实 ArkUI Before/After 案例；
- 修复校验脚本；
- 改善 Skill 触发描述；
- 补充设备、输入、无障碍和性能证据。

## 二、提交规则前

必须回答：

1. 规则解决了什么真实问题？
2. 来源是 H1、H2、H3 还是 H4？
3. 适用于哪些设备、窗口、输入和 API？
4. 能否观察和复现？
5. ArkUI 落点是什么？
6. 是否可能误报？
7. 为什么不能由现有规则覆盖？
8. 数值是官方要求、官方参考、API 默认、观察还是 House Style？
9. 规则是 evergreen、versioned 还是 experimental？
10. 属于 foundation、platform 还是 project 层？

使用 `templates/rule-proposal.md`。

## 三、规则 ID

格式：

```text
HD-<CATEGORY>-<NNN>
```

已发布 ID 不得因标题调整而修改。规则含义根本变化时新增 ID，并弃用旧规则。

## 四、来源要求

优先：

1. 华为官方 HarmonyOS 文档；
2. OpenHarmony 官方 UX / ArkUI 文档；
3. 官方样例、系统应用或公开演讲；
4. 明确标注的 House Style。

禁止：

- 仅凭第三方博客声称官方参数；
- 把其他平台的数值迁移成鸿蒙官方值；
- 把社区评论当规范证据；
- 大段复制官方正文；
- 忽略版本和最后核验日期。

## 五、案例要求

使用 `templates/case-study.md`。至少包含：

- 目标设备和输入；
- 无 Skill 基线；
- 命中规则；
- Before/After；
- 代码 diff；
- 构建结果；
- 真机或录屏；
- 大字体和无障碍；
- 性能；
- 未解决问题；
- 可执行原型或真实实现；
- 平台版本档案与知识层。

## 六、验证

提交前运行：

```bash
python scripts/validate_repo.py
pytest
```

修改 description 时必须增加 near-miss Trigger Eval。

修改规则时必须增加或更新 Review Eval。

## 七、异步真实性

涉及网络、同步、付款、删除、发布、权限等场景，必须测试：

- 慢响应；
- 失败；
- 超时；
- 取消；
- 重复提交；
- 响应乱序；
- 页面离开与返回。

成功动效和无障碍播报不得早于真实确认。

## 八、评审原则

- 正确性高于规则数量；
- 系统能力优先；
- 产品人格优先于统一风格；
- 证据优先于权威语气；
- 不确定时降级为 Draft；
- 当前 Draft 不接受自动修复功能；
- 最新视觉趋势不能覆盖状态真实性、可读性和无障碍；
- 通用视频剪辑不属于主 Skill。

## 九、知识分层与平台版本

规则提案必须同时标注：

- `stability`：evergreen / versioned / experimental；
- `design_layer`：foundation / platform / project。

版本化平台规则需要：

- 目标 SDK/API；
- 设备范围；
- 当前默认行为；
- 最后核验日期；
- 迁移说明。

## 十、原型和范围

高风险动态案例不能只提交静态截图。至少提供可运行原型、真实工程或可复现 fixture。

涉及代码生成视频时，先说明它是否由可检查的状态、几何、时间和代码控制。通用剪辑、实拍和镜头叙事不纳入主 Skill 规则。
