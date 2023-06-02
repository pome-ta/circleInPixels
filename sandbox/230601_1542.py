import ui


class View(ui.View):

  def __init__(self):
    self.bg_color = 1

  def did_load(self):
    pass

  def will_close(self):
    pass

  def draw(self):
    _, _, w, h = self.frame
    #red = ui.set_color('red')
    #grey = ui.set_color(0.25)
    r = 4
    n = int(r * 2 + 1)
    l = min(w, h)
    cell_size = l / n

    for x in range(n):
      for y in range(n):
        ui.set_color('red') if x == r and y == r else ui.set_color(0.25)

        rect = ui.Path.rect(cell_size * x, cell_size * y, cell_size, cell_size)
        rect.fill()
        ui.set_color(0.75)
        rect.stroke()

  def layout(self):
    pass


if __name__ == '__main__':
  view = View()
  #view.present()
  #view.present(hide_title_bar=True)
  view.present(style='fullscreen', orientations=['portrait'])

