@Entry
@Component
struct WidgetCard {
  /*
   * The title.
   */
  readonly TITLE: string = 'Hello World';
  /*
   * The action type.
   */
  readonly ACTION_TYPE: string = 'router';
  /*
   * The ability name.
   */
  readonly ABILITY_NAME: string = 'EntryAbility';
  /*
   * The message.
   */
  readonly MESSAGE: string = 'add detail';
  /*
   * The width percentage setting.
   */
  readonly FULL_WIDTH_PERCENT: string = '100%';
  /*
   * The height percentage setting.
   */
  readonly FULL_HEIGHT_PERCENT: string = '100%';

  build() {
    FormLink({
      action: this.ACTION_TYPE,
      abilityName: this.ABILITY_NAME,
      params: {
        message: this.MESSAGE
      }
    }) {
      Row() {
        Column() {
          Text(this.TITLE)
            .fontSize($r('app.float.font_size'))
            .fontWeight(FontWeight.Medium)
            .fontColor($r('app.color.item_title_font'))
        }
        .width(this.FULL_WIDTH_PERCENT)
      }
      .height(this.FULL_HEIGHT_PERCENT)
    }
  }
}