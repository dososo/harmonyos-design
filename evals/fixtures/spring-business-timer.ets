import { curves } from '@kit.ArkUI'

@Entry
@Component
struct SpringBusinessTimer {
  @State scaleValue: number = 1
  @State committed: boolean = false

  build() {
    Button('提交')
      .scale({ x: this.scaleValue, y: this.scaleValue })
      .onClick(() => {
        this.getUIContext()?.animateTo({
          duration: 550,
          curve: curves.springMotion()
        }, () => {
          this.scaleValue = 1.1
        })
        // 问题：假定弹簧 550ms 后完成，并提交业务。
        setTimeout(() => {
          this.committed = true
        }, 550)
      })
  }
}
