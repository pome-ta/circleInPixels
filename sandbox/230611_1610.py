# 円を作る カクカクさせる: 整理
import math
import ui


class View(ui.View):

  def __init__(self, r: int = 2):
    # --- 初期定義
    self.cell_rad: int
    self.cell_dia: int
    self.cell_size: float
    self.grid_size: float
    self.cells: list

    # --- color 定義
    self.g_stroke = 0.75
    self.g_fill = 0.25
    self.c1 = 'red'

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
    # xxx: `rect` 生成と位置サイズ指定を関数化（お行儀良くないけど、長くなるので）
    create_rect = lambda _x, _y: ui.Path.rect(cs * _x, cs * _y, cs, cs)

    self.cells = [[create_rect(x, y) for y in rd] for x in rd]

    self.grid_size = gs
    self.cell_dia = cd
    self.cell_size = cs

  def draw(self):
    # todo: view 確定後に、画面位置サイズ情報を取得
    _, _, w, h = self.frame
    self.setup_grid_cells(w, h)
    self.init_grid_colors()

  def layout(self):
    pass


if __name__ == '__main__':
  cell_radius: int = 8
  view = View(cell_radius)
  #view.present()
  #view.present(hide_title_bar=True)
  view.present(style='fullscreen', orientations=['portrait'])

