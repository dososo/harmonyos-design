// 场景四：无障碍图标按钮（HD-A11Y-001、HD-INTERACTION-001）
// 正确实现：用 Button 承载点击（自带按压反馈），并提供 accessibilityText 可访问名称与后果说明。

@Component
export struct A11yButtonDemo {
  @State count: number = 0

  build() {
    Column({ space: 12 }) {
      Text(`已删除 ${this.count} 项`)
        .fontSize(16)

      Button() {
        Image($r('app.media.startIcon'))
          .width(24)
          .height(24)
      }
      .width(48)
      .height(48)
      .accessibilityText('删除')
      .accessibilityDescription('删除当前项，操作不可撤销')
      .onClick(() => {
        this.count++
      })

      Text('图标按钮具备可访问名称与后果说明，读屏可识别')
        .fontSize(12)
        .fontColor(Color.Gray)
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
  }
}
