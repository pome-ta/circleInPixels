# 円を作る
import ui


class View(ui.View):

  def __init__(self):
    self.bg_color = 1

  def draw(self):
    _, _, w, h = self.frame
    ui.set_color(0.25)
    back = ui.Path.rect(w / 4, h / 4, w / 2, h / 2)
    back.fill()

  def layout(self):
    pass


if __name__ == '__main__':
  view = View()
  #view.present()
  #view.present(hide_title_bar=True)
  view.present(style='fullscreen', orientations=['portrait'])

