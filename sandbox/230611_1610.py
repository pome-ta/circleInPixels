# 円を作る カクカクさせる: 整理
import math
import ui


class View(ui.View):

  def __init__(self, r: int = 2):
    # todo: 初期定義
    self.cell_rad: int
    self.cell_dia: int
    self.cell_size: float
    self.grid_size: float
    self.cells: list

    self.cell_rad = r
    self.bg_color = 1

  def draw(self):
    _, _, w, h = self.frame
    self.cell_dia = int(self.cell_rad * 2) + 1
    self.grid_size = min(w, h)
    self.cell_size = self.grid_size / self.cell_dia

    dia_range = range(self.cell_dia)

    create_rect = lambda _x, _y: ui.Path.rect(
      self.cell_size * _x, self.cell_size * _y, self.cell_size, self.cell_size)

    self.cells = [[create_rect(x, y) for y in dia_range] for x in dia_range]

  def layout(self):
    pass


if __name__ == '__main__':
  cell_radius: int = 8
  view = View(cell_radius)
  #view.present()
  #view.present(hide_title_bar=True)
  view.present(style='fullscreen', orientations=['portrait'])

