// 场景一：异步状态真实性（HD-ASYNC-001/002、HD-A11Y-003）
// 正确实现：成功态只在真实 await 结果后出现；Pending 禁用防重复提交；无障碍播报绑定真实状态。

enum SaveState { Idle, Pending, Confirmed, Failed }

@Component
export struct AsyncSaveDemo {
  @State state: SaveState = SaveState.Idle

  async saveRemote(): Promise<void> {
    await new Promise<void>((resolve: () => void) => setTimeout(resolve, 1500))
  }

  private label(): string {
    switch (this.state) {
      case SaveState.Pending: return '保存中…'
      case SaveState.Confirmed: return '已保存'
      case SaveState.Failed: return '保存失败，点击重试'
      default: return '保存'
    }
  }

  private a11yText(): string {
    switch (this.state) {
      case SaveState.Pending: return '正在保存'
      case SaveState.Confirmed: return '已保存成功'
      case SaveState.Failed: return '保存失败，双击重试'
      default: return '保存'
    }
  }

  build() {
    Column({ space: 12 }) {
      Text(this.label())
        .fontSize(18)
        .fontColor(this.state === SaveState.Failed ? Color.Red : Color.Black)

      Button(this.state === SaveState.Pending ? '保存中…' : '保存')
        .enabled(this.state !== SaveState.Pending)
        .accessibilityText(this.a11yText())
        .onClick(async () => {
          this.state = SaveState.Pending
          try {
            await this.saveRemote()
            this.state = SaveState.Confirmed
          } catch (_) {
            this.state = SaveState.Failed
          }
        })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
  }
}
