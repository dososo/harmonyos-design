@Entry
@Component
struct LongPressOnly {
  build() {
    ListItem() {
      Text('项目')
    }
    .gesture(
      LongPressGesture()
        .onAction(() => {
          // 唯一删除入口
          this.deleteItem()
        })
    )
  }

  deleteItem(): void {}
}
