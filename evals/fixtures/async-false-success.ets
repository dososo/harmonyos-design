enum SaveState { Idle, Pending, Confirmed, Failed }

@Entry
@Component
struct AsyncFalseSuccess {
  @State state: SaveState = SaveState.Idle

  async save(): Promise<void> {
    // 问题：请求开始前就进入成功状态。
    this.state = SaveState.Confirmed
    try {
      await new Promise<void>((resolve) => setTimeout(resolve, 3000))
    } catch (_) {
      this.state = SaveState.Failed
    }
  }

  build() {
    Button(this.state === SaveState.Confirmed ? '保存成功' : '保存')
      .onClick(() => this.save())
      .accessibilityText(this.state === SaveState.Confirmed ? '保存成功' : '保存')
  }
}
