# 円を作る カクカクさせる
import math
import ui

c1 = 0.25
c2 = 'red'
c3 = 'yellow'
c4 = 'blue'


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
      for y in range(n)
    ] for x in range(n)]

    [[setup_cells(r, x, y, cells[x][y]) for y in range(n)] for x in range(n)]

    return [cells, cell_size, grid_size]

  def draw(self):
    _, _, w, h = self.frame

    box_len = 5

    self.cells, self.cell_size, self.grid_size = self.create_grid_cells(
      box_len, w, h)

    self.indexs = len(self.cells)

    ov = 2
    r = (self.grid_size / 2) - (self.cell_size / 2)
    pos_x = r - (ov / 2)
    pos_y = r - (ov / 2)

    self.pi_r = [[
      pos_x + (r * math.sin(math.radians(i))) + (self.cell_size / 2),
      pos_y + (r * math.cos(math.radians(i))) + (self.cell_size / 2)
    ] for i in range(0, 360, 36)]

    self.cell_pi = set(
      map(tuple, [[int(x / self.cell_size),
                   int(y / self.cell_size)] for x, y in self.pi_r]))

    ui.set_color(c4)
    for idx in self.cell_pi:
      i_x, i_y = idx
      cell = self.cells[i_x][i_y]
      cell.fill()

    ui.set_color(c3)
    for idx in self.pi_r:
      r_x, r_y = idx
      oval = ui.Path.oval(r_x, r_y, ov, ov)
      oval.fill()
    '''
    for i in range(0, 360, 120):
      rad = math.radians(i)

      r_x = pos_x + (r * math.sin(rad)) + (self.cell_size / 2)
      i_x = int(r_x / self.cell_size)

      r_y = pos_y + (r * math.cos(rad)) + (self.cell_size / 2)
      i_y = int(r_y / self.cell_size)

      #ui.set_color(c4)
      cell = self.cells[i_x][i_y]
      cell.fill()

      oval = ui.Path.oval(r_x, r_y, ov, ov)
      oval.fill()
    '''

  def layout(self):
    pass


if __name__ == '__main__':
  view = View()
  #view.present()
  #view.present(hide_title_bar=True)
  view.present(style='fullscreen', orientations=['portrait'])

