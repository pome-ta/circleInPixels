# 円を作る カクカクさせる
import math
import ui


def setup_cells(radius, x, y, cell):
  ui.set_color('red') if x == radius or y == radius else ui.set_color(0.25)
  cell.fill()

  ui.set_color(0.75)
  cell.stroke()


class View(ui.View):

  def __init__(self):
    self.bg_color = 1

  def create_grid_cells(self, r: int, w: float, h: float) -> list:
    n = int(r * 2 + 1)
    grid_size = min(w, h)
    cell_size = grid_size / n

    cells = [[
      ui.Path.rect(cell_size * x, cell_size * y, cell_size, cell_size)
      for x in range(n)
    ] for y in range(n)]

    [[setup_cells(r, x, y, cells[x][y]) for y in range(n)] for x in range(n)]

    return [cells, cell_size, grid_size]

  def draw(self):
    _, _, w, h = self.frame
    box_len = 9
    self.cells, self.cell_size, self.grid_size = self.create_grid_cells(
      box_len, w, h)

    self.indexs = len(self.cells)
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
      x_r = cnt_x + int(r * math.sin(rad))
      y_r = cnt_y + int(r * math.cos(rad))
      #print(y_r)
      oval = ui.Path.oval(x_r, y_r, ov, ov)
      oval.fill()

  def layout(self):
    pass


if __name__ == '__main__':
  view = View()
  #view.present()
  #view.present(hide_title_bar=True)
  view.present(style='fullscreen', orientations=['portrait'])

