# 中心から、セルごとに線を引く
import math
import colorsys
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

import ui


def round_halfup(f: float) -> int:
  return Decimal(str(f)).quantize(Decimal('0'), rounding=ROUND_HALF_UP)


class View(ui.View):

  def __init__(self, r: int = 2):
    # --- 初期定義
    self.cell_rad: int  # cell の半径
    self.cell_dia: int  # cell の全径
    self.cell_size: float
    self.grid_size: float
    self.cells: list
    self.indexs: list

    # --- color 定義
    self.g_stroke: str | float | int = 0.75
    self.g_fill: str | float | int = 0.25
    self.c0: str | float = 0.88
    self.c1: str | float = 'maroon'
    self.c2: str | float = 'blue'
    self.c3: str | float = 'green'
    self.c4: str | float = 'yellow'

    # --- 変数反映
    self.cell_rad = r
    self.bg_color = 1

  def set_fill_stroke(self,
                      cell: ui.Path,
                      fill: str | float,
                      stroke: str | float | None = None):
    stroke = fill if stroke == None else stroke
    ui.set_color(fill)
    cell.fill()
    ui.set_color(stroke)
    cell.stroke()

  def init_grid_colors(self):
    # --- 中心線塗り
    _r = self.cell_rad
    is_center = lambda _x, _y: True if _x == _r or _y == _r else False

    for x, rows in enumerate(self.cells):
      for y, cell in enumerate(rows):
        self.set_fill_stroke(cell, self.c1 if is_center(x, y) else self.g_fill,
                             self.g_stroke)
        #ui.set_color(self.c1) if is_center(x, y) else ui.set_color(self.g_fill)
        #cell.fill()
        #ui.set_color(self.g_stroke)
        #cell.stroke()

  def setup_grid_cells(self, width: float, height: float):
    gs = min(width, height)
    cd = int(self.cell_rad * 2) + 1
    cs = gs / cd

    rd = range(cd)
    create_rect = lambda _x, _y: ui.Path.rect(cs * _x, cs * _y, cs, cs)

    self.cells = [[create_rect(x, y) for y in rd] for x in rd]

    self.grid_size = gs
    self.cell_dia = cd
    self.cell_size = cs

  def _normalize_to_position(self, nx: int, ny: int) -> list[int, int]:
    px = self.cell_rad + nx
    py = self.cell_rad + ny
    return [px, py]

  def _position_to_normalize(self, px: int, py: int) -> list[int, int]:
    nx = px - self.cell_rad - 1
    ny = py - self.cell_rad - 1
    return [nx, ny]

  def normalize_cell(self, cx: int, cy: int) -> ui.Path:
    nx, ny = self._position_to_normalize(cx, cy)
    return self.cells[nx][ny]

  def get_index_to_position(self,
                            ix: int,
                            iy: int,
                            is_normalized: bool = True) -> list[float, float]:
    x, y = self._normalize_to_position(ix, iy) if is_normalized else [ix, iy]

    offset = self.cell_size / 2
    gpx = x * self.cell_size + offset
    gpy = y * self.cell_size + offset
    return [gpx, gpy]

  def get_position_to_index(self, px: float, py: float) -> list[int, int]:
    offset = self.cell_size / 2
    _x = (px - offset) / self.cell_size
    _y = (py - offset) / self.cell_size
    ix = round_halfup(_x)
    iy = round_halfup(_y)
    return [int(ix), int(iy)]

  def get_bounds_to_index(self, cell: ui.Path) -> list[int, int]:
    cx, cy, _, _ = cell.bounds
    ix = round_halfup(cx / self.cell_size)
    iy = round_halfup(cy / self.cell_size)
    return [int(ix), int(iy)]

  def draw(self):
    # todo: view 確定後に、画面位置サイズ情報を取得
    _, _, w, h = self.frame
    self.setup_grid_cells(w, h)
    self.init_grid_colors()

    s_cell = self.normalize_cell(0, 0)
    ui.set_color(self.c0)
    s_cell.fill()
    for i in range(self.cell_dia):
      cell = self.cells[i][0]

      ui.set_color(self.c0)
      cell.fill()
      ui.set_color(self.g_stroke)
      cell.stroke()

      h = i / self.cell_dia
      hsv_color = colorsys.hsv_to_rgb(h, 1.0, 1.0)

  def layout(self):
    pass


if __name__ == '__main__':
  cell_radius: int = 8
  view = View(cell_radius)
  view.present(style='fullscreen', orientations=['portrait'])

