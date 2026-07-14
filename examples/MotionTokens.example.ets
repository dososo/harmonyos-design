// 概念示例：需按目标 SDK 与项目资源系统核验后使用。
// 该文件展示“语义、来源、范围”建模方式，不声明这些值是 HarmonyOS 官方统一参数。

import { curves } from '@kit.ArkUI'

export enum ValueKind {
  OfficialReference = 'OFFICIAL_REFERENCE',
  ArkUIDefault = 'ARKUI_DEFAULT',
  HouseStyle = 'HOUSE_STYLE'
}

export class MotionTokens {
  // OpenHarmony 公开参考：很短动作约 150ms 内。
  static readonly shortMs: number = 150
  static readonly shortMsKind: ValueKind = ValueKind.OfficialReference

  // 项目偏好：仅用于自定义、需要额外按压反馈的控件。
  // 系统 Button 应优先保留默认反馈；该值需要真机调校。
  static readonly customPressScale: number = 0.98
  static readonly customPressScaleKind: ValueKind = ValueKind.HouseStyle

  static followCurve() {
    return curves.responsiveSpringMotion()
  }

  static settleCurve() {
    return curves.springMotion()
  }
}

export enum RemoteActionState {
  Idle,
  Pending,
  Confirmed,
  Failed
}

// Pressed 只表达输入已接收；成功 UI 必须由 Confirmed 驱动。
