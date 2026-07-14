@Entry
@Component
struct ImageButtonNoA11y {
  build() {
    Image($r('app.media.delete'))
      .width(48)
      .height(48)
      .onClick(() => {
        // 删除逻辑
      })
  }
}
