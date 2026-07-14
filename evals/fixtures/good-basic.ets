import { curves } from '@kit.ArkUI'

enum SubmitState { Idle, Pending, Confirmed, Failed }

@Entry
@Component
struct GoodBasic {
  @State state: SubmitState = SubmitState.Idle
  @State offsetX: number = 0

  build() {
    Column() {
      Button(this.state === SubmitState.Pending ? '保存中' : '保存')
        .enabled(this.state !== SubmitState.Pending)
        .accessibilityText(this.state === SubmitState.Pending ? '正在保存' : '保存')
        .onClick(async () => {
          this.state = SubmitState.Pending
          try {
            await this.saveRemote()
            this.state = SubmitState.Confirmed
          } catch (_) {
            this.state = SubmitState.Failed
          }
        })
    }
  }

  async saveRemote(): Promise<void> {}
}
