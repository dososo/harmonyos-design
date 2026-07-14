@Entry
@Component
struct MultipleAnimateTo {
  @State x: number = 0
  @State opacityValue: number = 1

  build() {
    Row()
      .translate({ x: this.x })
      .opacity(this.opacityValue)
      .onClick(() => {
        this.getUIContext()?.animateTo({ duration: 200, curve: Curve.Smooth }, () => {
          this.x = 100
        })
        this.getUIContext()?.animateTo({ duration: 200, curve: Curve.Smooth }, () => {
          this.opacityValue = 0.5
        })
      })
  }
}
