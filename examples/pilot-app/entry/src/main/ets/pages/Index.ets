import { AsyncSaveDemo } from '../components/AsyncSaveDemo'
import { GestureVelocityDemo } from '../components/GestureVelocityDemo'
import { AdaptiveLayoutDemo } from '../components/AdaptiveLayoutDemo'
import { A11yButtonDemo } from '../components/A11yButtonDemo'

// HarmonyOS-Design mock 试点：Tabs 聚合 4 类 skill 主张场景
@Entry
@Component
struct Index {
  build() {
    Tabs() {
      TabContent() { AsyncSaveDemo() }.tabBar('异步真实')
      TabContent() { GestureVelocityDemo() }.tabBar('手势速度')
      TabContent() { AdaptiveLayoutDemo() }.tabBar('平板适配')
      TabContent() { A11yButtonDemo() }.tabBar('无障碍')
    }
    .width('100%')
    .height('100%')
  }
}
