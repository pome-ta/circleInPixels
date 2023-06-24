# 円を作る
import math
import ui


class View(ui.View):

  def __init__(self):
    self.bg_color = 1

  def draw(self):
    _, _, w, h = self.frame
    back_size = min(w, h) / 1.25
    x_pos = (w / 2) - (back_size / 2)
    y_pos = (h / 2) - (back_size / 2)
    ui.set_color(0.25)
    back = ui.Path.rect(x_pos, y_pos, back_size, back_size)
    back.fill()

    ui.set_color('red')

    r = back_size / 2

    ov = 5
    cnt_x = x_pos + (back_size / 2) - (ov / 2)
    cnt_y = y_pos + (back_size / 2) - (ov / 2)

    for i in range(0, 360, 5):
      rad = math.radians(i)
      x_r = cnt_x + (r * math.sin(rad))
      y_r = cnt_y + (r * math.cos(rad))
      oval = ui.Path.oval(x_r, y_r, ov, ov)
      oval.fill()

  def layout(self):
    pass


if __name__ == '__main__':
  view = View()
  #view.present()
  #view.present(hide_title_bar=True)
  view.present(style='fullscreen', orientations=['portrait'])

