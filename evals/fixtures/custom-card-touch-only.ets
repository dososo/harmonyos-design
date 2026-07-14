@Entry
@Component
struct CustomCardTouchOnly {
  @State pressed: boolean = false

  build() {
    Column() {
      Text('打开详情')
    }
    .backgroundColor(this.pressed ? '#EEEEEE' : '#FFFFFF')
    .onTouch((event?: TouchEvent) => {
      if (event?.type === TouchType.Down) this.pressed = true
      if (event?.type === TouchType.Up) this.pressed = false
    })
    .onClick(() => {})
    // 问题：面向平板和 PC，但无焦点、悬停和可访问角色。
  }
}
