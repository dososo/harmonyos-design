import { curves } from '@kit.ArkUI'

@Entry
@Component
struct GestureVelocityReset {
  @State offsetX: number = 0

  build() {
    Row()
      .width(120)
      .height(80)
      .translate({ x: this.offsetX })
      .gesture(
        PanGesture()
          .onActionUpdate((event?: GestureEvent) => {
            if (event) {
              this.offsetX = event.offsetX
            }
          })
          .onActionEnd(() => {
            // 问题：离手后使用固定时长普通曲线，从零速度回到目标。
            this.getUIContext()?.animateTo({ duration: 300, curve: Curve.EaseOut }, () => {
              this.offsetX = 0
            })
          })
      )
  }
}
