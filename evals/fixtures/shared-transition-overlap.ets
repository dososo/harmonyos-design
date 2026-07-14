@Entry
@Component
struct SharedTransitionOverlap {
  stack: NavPathStack = new NavPathStack()

  build() {
    Navigation(this.stack) {
      Image($r('app.media.cover'))
        .geometryTransition('cover')
        .onClick(() => {
          // 问题：共享转场存在，但仍使用默认动画 push。
          this.getUIContext()?.animateTo({ duration: 300 }, () => {
            this.stack.pushPath({ name: 'Detail' })
          })
        })
    }
  }
}
