import { curves } from '@kit.ArkUI'

@Entry
@Component
struct GestureVelocityHandoff {
  @State offsetX: number = 0
  private startOffsetX: number = 0

  build() {
    Row()
      .width(120)
      .height(80)
      .translate({ x: this.offsetX })
      .gesture(
        PanGesture({ direction: PanDirection.Horizontal, distance: 5 })
          .onActionStart(() => {
            this.startOffsetX = this.offsetX
          })
          .onActionUpdate((event?: GestureEvent) => {
            if (!event) return
            this.getUIContext()?.animateTo({
              curve: curves.responsiveSpringMotion()
            }, () => {
              this.offsetX = this.startOffsetX + event.offsetX
            })
          })
          .onActionEnd(() => {
            this.getUIContext()?.animateTo({
              curve: curves.springMotion()
            }, () => {
              this.offsetX = 0
            })
          })
      )
  }
}
