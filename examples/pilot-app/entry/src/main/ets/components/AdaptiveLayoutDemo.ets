// 场景三：手机到平板适配（HD-ADAPT-001/002）
// 正确实现：用 GridRow 响应式断点分栏，而非固定尺寸或整页等比缩放。

@Component
export struct AdaptiveLayoutDemo {
  private cards: number[] = [1, 2, 3, 4, 5, 6]

  build() {
    Column({ space: 8 }) {
      Text('随窗口宽度改变列数（手机 2 列 / 平板 4–6 列）')
        .fontSize(14)
        .fontColor(Color.Gray)

      GridRow({ columns: { xs: 2, sm: 2, md: 4, lg: 6 }, gutter: 8 }) {
        ForEach(this.cards, (item: number) => {
          GridCol() {
            Text(`卡片 ${item}`)
              .width('100%')
              .height(56)
              .textAlign(TextAlign.Center)
              .borderRadius(8)
              .backgroundColor('#E6F0FF')
          }
        }, (item: number) => item.toString())
      }
      .width('100%')
    }
    .width('100%')
    .height('100%')
    .padding(16)
    .justifyContent(FlexAlign.Center)
  }
}
