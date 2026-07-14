enum SaveState { Idle, Pending, Confirmed, Failed }

@Entry
@Component
struct TruthfulAsyncSave {
  @State state: SaveState = SaveState.Idle
  @State errorMessage: string = ''
  private latestRequestId: number = 0

  async save(): Promise<void> {
    if (this.state === SaveState.Pending) {
      return
    }

    const requestId = ++this.latestRequestId
    this.state = SaveState.Pending
    this.errorMessage = ''

    try {
      await this.saveRemote()
      if (requestId !== this.latestRequestId) {
        return
      }
      // 只有真实请求确认后才进入成功状态。
      this.state = SaveState.Confirmed
    } catch (_) {
      if (requestId !== this.latestRequestId) {
        return
      }
      this.state = SaveState.Failed
      this.errorMessage = '保存失败，请重试'
    }
  }

  build() {
    Column({ space: 12 }) {
      Button(this.buttonLabel())
        .enabled(this.state !== SaveState.Pending)
        .accessibilityText(this.accessibilityLabel())
        .onClick(() => this.save())

      if (this.state === SaveState.Failed) {
        Text(this.errorMessage)
          .accessibilityText(this.errorMessage)
      }
    }
  }

  buttonLabel(): string {
    if (this.state === SaveState.Pending) return '保存中'
    if (this.state === SaveState.Confirmed) return '已保存'
    return '保存'
  }

  accessibilityLabel(): string {
    if (this.state === SaveState.Pending) return '正在保存'
    if (this.state === SaveState.Confirmed) return '保存成功'
    if (this.state === SaveState.Failed) return '保存失败，可重试'
    return '保存'
  }

  async saveRemote(): Promise<void> {
    // 由真实业务实现替换。
  }
}
