# 新项目启动计划

对应规则：`HD-FOUNDATION-001`、`HD-FOUNDATION-006`、`HD-FOUNDATION-007`。

## 1. Product Context Card

```yaml
核心任务: 快速记录收支并确认保存状态
设备: 手机、平板
窗口: 全屏、分屏
输入: 触摸；平板键鼠
API_Level: 待确认
数据: 本地优先，远端同步
风险: 重复提交、同步失败、误删
```

## 2. Evergreen Baseline

- 保存状态真实；
- 输入即时反馈；
- 错误可恢复；
- 导航清晰；
- 手势可打断；
- 大字体和读屏可用。

## 3. Platform Version Profile

- 固定目标 SDK；
- 记录 Button、Tabs、Navigation 默认行为；
- 核验 `springMotion`、`transition` 与无障碍 API；
- 记录手机和平板差异。

## 4. Project Overlay

- 人格：平静、可信、轻量；
- 高频记账路径减少装饰动效；
- 统计和首次成功可以适度强调；
- 所有自定义参数标为 House Style。

## 5. 首个可交互原型

只实现：

```text
首页 → 新增支出 → Pending → Confirmed / Failed → 返回首页
```

验证：快速双击、慢后端、失败、取消、反向返回、大字体、读屏和平板分屏。

## 6. 编码门禁

完成上下文、平台版本、状态模型、原型与验收矩阵后，再批量生成其他页面。
