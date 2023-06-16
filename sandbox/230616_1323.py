# 中心から、セルごとに線を引く
import math
import ui


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
    self.c1: str | float = 'red'
    self.c2: str | float = 'blue'
    self.c3: str | float = 'green'

    # --- 変数反映
    self.cell_rad = r
    self.bg_color = 1

  def init_grid_colors(self):
    # --- 中心線塗り
    _r = self.cell_rad
    is_center = lambda _x, _y: True if _x == _r or _y == _r else False

    for x, rows in enumerate(self.cells):
      for y, cell in enumerate(rows):
        ui.set_color(self.c1) if is_center(x, y) else ui.set_color(self.g_fill)
        cell.fill()
        ui.set_color(self.g_stroke)
        cell.stroke()

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

  def normalize_cell(self, px: int, py: int) -> ui.Path:
    nx, ny = self._position_to_normalize(px, py)
    return self.cells[nx][ny]

  def get_grid_to_position(self,
                           cx: int,
                           cy: int,
                           is_normalized: bool = True) -> list[float, float]:
    x, y = self._normalize_to_position(cx, cy) if is_normalized else [cx, cy]
    print(x)
    offset = self.cell_size / 2
    gpx = x * self.cell_size + offset
    gpy = y * self.cell_size + offset
    return [gpx, gpy]

  def draw(self):
    # todo: view 確定後に、画面位置サイズ情報を取得
    _, _, w, h = self.frame
    self.setup_grid_cells(w, h)
    self.init_grid_colors()

    px, py = self._normalize_to_position(0, 0)

    cell = self.cells[1][2]
    #cell = self.normalize_cell(-8,0)
    ui.set_color(self.c2)
    cell.fill()
    #self.get_cell_position(cell)

    cell = self.cells[8][8]
    ui.set_color(self.c3)
    cell.fill()
    sx, sy = self.get_grid_to_position(1, 2, False)
    ex, ey = self.get_grid_to_position(8, 8, False)
    line = ui.Path()
    line.line_width = 1
    line.move_to(sx, sy)
    line.line_to(ex, ey)
    ui.set_color(self.c1)
    line.stroke()
    #print(self.get_grid_to_position(1, 2, False))

  def layout(self):
    pass


if __name__ == '__main__':
  cell_radius: int = 8
  view = View(cell_radius)
  #view.present()
  #view.present(hide_title_bar=True)
  view.present(style='fullscreen', orientations=['portrait'])

