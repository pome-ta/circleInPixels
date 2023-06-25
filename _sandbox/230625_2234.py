# 円座標上の点から、取得点の数でプロット
import math
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

import ui

# --- color 定義
g_stroke: str | float | int = 0.75
g_fill: str | float | int = 0.25
c0: str | float = 0.88
c1: str | float = 'maroon'
c2: str | float = 'blue'
c3: str | float = 'green'
c4: str | float = 'yellow'


def round_halfup(f: float) -> int:
  return Decimal(str(f)).quantize(Decimal('0'), rounding=ROUND_HALF_UP)


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
    x, y = _xy
    return self.cells[x][y]

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
    _r = self.cell_rad
    is_center = lambda _x, _y: True if _x == _r or _y == _r else False
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

  def set_guide_oval(self, dot_size: float = 2.0, interval: int = 1):
    pos_x = self.radius_length - (dot_size / 2)
    pos_y = self.radius_length - (dot_size / 2)

    for i in range(0, 360, interval):
      r = math.radians(i)
      x = pos_x + (self.radius_length * math.cos(r))
      y = pos_y + (self.radius_length * math.sin(r))
      ui.set_color('cyan')
      dot = ui.Path.oval(x + self.offset_length, y + self.offset_length,
                         dot_size, dot_size)
      dot.fill()

  def get_bounds_to_index(self, cell: ui.Path) -> list[int, int]:
    cx, cy, _, _ = cell.bounds
    ix, iy = self.get_position_to_index(cx, cy)
    return [ix, iy]

  def get_position_to_index(self, px: float, py: float) -> list[int, int]:
    ix = round_halfup(px / self.cell_size)
    iy = round_halfup(py / self.cell_size)

    return [int(ix), int(iy)]

  def get_index_to_position(self, ix: int, iy: int) -> list[float, float]:
    gpx = ix * self.cell_size + self.offset_length
    gpy = iy * self.cell_size + self.offset_length
    return [gpx, gpy]

  def get_cells_position(self, s_cell: ui.Path,
                         e_cell: ui.Path) -> list[float, float, float, float]:
    s_bix, s_biy = self.get_bounds_to_index(s_cell)
    e_bix, e_biy = self.get_bounds_to_index(e_cell)
    sx, sy = self.get_index_to_position(s_bix, s_biy)
    ex, ey = self.get_index_to_position(e_bix, e_biy)
    return [sx, sy, ex, ey]

  def draw(self):
    # todo: view 確定後に、画面位置サイズ情報を取得
    _, _, w, h = self.frame
    self.init_grid_cells(w, h)
    self.init_grid_colors()
    self.set_guide_oval(1, 1)

  def layout(self):
    pass


if __name__ == '__main__':
  cell_radius: int = 4
  view = View(cell_radius)
  #view.present(style='fullscreen', orientations=['portrait'])
  view.present(style='panel', orientations=['portrait'])

