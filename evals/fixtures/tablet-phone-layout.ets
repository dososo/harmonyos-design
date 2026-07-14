@Entry
@Component
struct TabletPhoneLayout {
  build() {
    Column() {
      Text('我的内容').fontSize(16)
      List() { }
        .width(360)
        .height(600)
      Tabs() { }
        .width(360)
        .height(80)
    }
    .width(360)
    .height(800)
  }
}
