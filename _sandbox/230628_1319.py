# マイクラのコマンド
import math
import statistics
import collections

import ui

# --- color 定義
g_stroke: str | float | int = 0.75
g_fill: str | float | int = 0.25
c0: str | float = 0.88
c1: str | float = 'maroon'
c2: str | float = 'blue'
c3: str | float = 'green'
c4: str | float = 'yellow'


class View(ui.View):

  def __init__(self, r: int = 2):
    # --- 初期定義
    self.cell_rad: int  # cell の半径
    self.cell_dia: int  # cell の全径
    self.cell_size: float
    self.grid_size: float
    self.radius_length: float  # 半径のサイズ
    self.offset_length: float  # cell 中心調整
    self.cells: list[list[ui.Path]]
    self.rect_edge_index: list[list[int]] = []

    # --- 変数反映
    self.bg_color = 1
    self.cell_rad = r

  def cell_cell(self, _xy: list[int, int]) -> ui.Path:
    _x, _y = _xy
    return self.cells[_x][_y]

  def set_cell_color(self,
                     cell: ui.Path,
                     fill: str | float,
                     stroke: str | float | None = None):
    stroke = fill if stroke == None else stroke
    ui.set_color(fill)
    cell.fill()
    ui.set_color(stroke)
    cell.stroke()

  def set_cell(self,
               _xy: list[int, int],
               fill: str | float,
               stroke: str | float | None = None) -> ui.Path:
    _cell = self.cell_cell(_xy)
    self.set_cell_color(_cell, fill, stroke)
    return _cell

  def init_grid_colors(self):
    # --- 中心線塗り
    is_center = lambda _x, _y: True if _x == self.cell_rad or _y == self.cell_rad else False
    [[
      self.set_cell_color(cell, c1 if is_center(x, y) else g_fill, g_stroke)
      for y, cell in enumerate(rows)
    ] for x, rows in enumerate(self.cells)]

  def init_grid_cells(self, width: float, height: float):
    gs = min(width, height)
    cd = int(self.cell_rad * 2) + 1
    cs = gs / cd

    create_rect = lambda _x, _y: ui.Path.rect(cs * _x, cs * _y, cs, cs)

    self.cells = [[create_rect(x, y) for y in range(cd)] for x in range(cd)]

    self.cell_dia = cd
    self.cell_size = cs
    self.grid_size = gs
    self.radius_length = (gs / 2.0) - (cs / 2.0)
    self.offset_length = cs / 2.0

  def get_position_to_index(self, px: float, py: float) -> list[int, int]:

    ix = int(px / self.cell_size)
    iy = int(py / self.cell_size)
    '''
    ix = round_halfup(px / self.cell_size)
    iy = round_halfup(py / self.cell_size)
    '''
    return [int(ix), int(iy)]

  def draw(self):
    # todo: view 確定後に、画面位置サイズ情報を取得
    _, _, w, h = self.frame
    self.init_grid_cells(w, h)
    self.init_grid_colors()

  def layout(self):
    pass


if __name__ == '__main__':
  cell_radius: int = 9
  view = View(cell_radius)
  #view.present(style='fullscreen', orientations=['portrait'])
  view.present(style='panel', orientations=['portrait'])

