# 中心から、セルごとに線を引く
import math
import colorsys
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

  def setup_rect_edge_index(self):
    # xxx: `filter` やら、あとでやる
    for x in range(self.cell_dia):
      for y in range(self.cell_dia):
        if (0 < y < self.cell_dia - 1) and (0 < x < self.cell_dia - 1):
          continue
        self.rect_edge_index.append([x, y])

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

  def create_line_cells_index(self,
                              s_cell: ui.Path,
                              e_cell: ui.Path,
                              stroke: str | float,
                              line_width: int = 1):
    sx, sy, ex, ey = self.get_cells_position(s_cell, e_cell)

    line = ui.Path()
    line.line_width = line_width
    line.move_to(sx, sy)
    line.line_to(ex, ey)
    ui.set_color(stroke)
    line.stroke()

  def get_oblique_length(self, base_length: float,
                         height_length: float) -> float:

    oblique = math.sqrt(pow((base_length), 2) + pow((height_length), 2))

    return oblique

  def plot_radius_index(self, s_cell: ui.Path, e_cell: ui.Path):
    ax, ay, bx, by = self.get_cells_position(s_cell, e_cell)
    base_length = ax - bx
    height_length = ay - by

    oblique = self.get_oblique_length(base_length, height_length)

    cx = ax + (self.radius_length / oblique) * (bx - ax)
    cy = ay + (self.radius_length / oblique) * (by - ay)

    line = ui.Path()
    line.line_width = 1
    line.move_to(ax, ay)
    line.line_to(cx, cy)
    ui.set_color('cyan')
    line.stroke()

    px = cx - self.offset_length
    py = cy - self.offset_length

    ix, iy = self.get_position_to_index(px, py)
    return [ix, iy]

  def test_line(self, s, e):
    #self.create_line_cells_index(s, e, g_stroke)
    self.create_line_cells_index(s, e, 'magenta')
    self.plot_radius_index(s, e)

  def draw(self):
    # todo: view 確定後に、画面位置サイズ情報を取得
    _, _, w, h = self.frame
    self.init_grid_cells(w, h)
    self.init_grid_colors()
    self.setup_rect_edge_index()

    s_cell = self.set_cell([self.cell_rad, self.cell_rad], c3, g_stroke)

    cache = []
    for n, adrs in enumerate(self.rect_edge_index):
      h = n / self.cell_dia
      hsv_color = colorsys.hsv_to_rgb(h, 1.0, 1.0)
      #e_cell = self.set_cell(adrs, hsv_color, g_stroke)
      #self.test_line(s_cell, e_cell)
      e_cell = self.cell_cell(adrs)

      o_cell_index = self.plot_radius_index(s_cell, e_cell)
      if o_cell_index in cache:
        print(o_cell_index)
        continue
      cache.append(o_cell_index)
      o_cell = self.set_cell(o_cell_index, c0, g_stroke)
      self.test_line(s_cell, e_cell)

  def layout(self):
    pass


if __name__ == '__main__':
  cell_radius: int = 9
  view = View(cell_radius)
  #view.present(style='fullscreen', orientations=['portrait'])
  view.present(style='panel', orientations=['portrait'])

