@Entry
@Component
struct LayoutAnimationInGesture {
  @State cardWidth: number = 120
  @State cardHeight: number = 80

  build() {
    Row()
      .width(this.cardWidth)
      .height(this.cardHeight)
      .gesture(
        PinchGesture()
          .onActionUpdate((event?: GestureEvent) => {
            if (event) {
              // 问题：手势高频回调持续修改布局尺寸。
              this.cardWidth = 120 * event.scale
              this.cardHeight = 80 * event.scale
            }
          })
      )
  }
}
