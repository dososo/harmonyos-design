// 场景二：手势速度衔接（HD-MOTION-004/006）
// 正确实现：离手用弹性曲线继承速度回稳，而非固定时长普通曲线从零速度归位。

import { curves } from '@kit.ArkUI'

@Component
export struct GestureVelocityDemo {
  @State offsetX: number = 0

  build() {
    Column({ space: 16 }) {
      Text('拖动方块，离手用 springMotion 继承速度回稳')
        .fontSize(14)
        .fontColor(Color.Gray)

      Row()
        .width(80)
        .height(80)
        .borderRadius(12)
        .backgroundColor('#3D7EFF')
        .translate({ x: this.offsetX })
        .gesture(
          PanGesture()
            .onActionUpdate((event?: GestureEvent) => {
              if (event) {
                this.offsetX = event.offsetX
              }
            })
            .onActionEnd(() => {
              // 跟手离手：弹性曲线继承速度，避免急刹车般的速度断层
              this.getUIContext()?.animateTo({ curve: curves.springMotion() }, () => {
                this.offsetX = 0
              })
            })
        )
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
  }
}
