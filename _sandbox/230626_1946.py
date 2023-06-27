# 円座標上の点から、取得点の数でプロット
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

  def set_guide_oval(self, dot_size: float = 2.0, interval: int = 1):
    # xxx: ガイドのドットがズレるけど、いまはOK
    pos_offset = self.radius_length + self.offset_length

    self.guide_oval_indexs = []
    for i in range(0, 360, interval):
      if i > 361:  # xxx: テスト確認用
        break
      r = math.radians(i)
      x = pos_offset + (self.radius_length * math.cos(r))
      y = pos_offset + (self.radius_length * math.sin(r))

      pos_xy = self.get_position_to_index(x, y)
      #self.set_cell(pos_xy, c3, g_stroke)
      self.guide_oval_indexs.append(pos_xy)

      ui.set_color('magenta')
      dot = ui.Path.oval(x, y, dot_size, dot_size)
      dot.fill()
    self.set_index = list(map(list, set(map(tuple, self.guide_oval_indexs))))

    self.index_counter_dics = []
    self.index_total_count = []
    for xy in self.set_index:
      count = self.guide_oval_indexs.count(xy)
      index_count = {'index': xy, 'count': count}
      self.index_counter_dics.append(index_count)
      self.index_total_count.append(count)

    set_all = list(set(self.index_total_count))
    mean_all = statistics.mean(self.index_total_count)
    mean_set = statistics.mean(set_all)
    print(f'mean_all:{mean_all}')
    print(f'mean_set: {mean_set}')
    stdev_all = statistics.stdev(self.index_total_count)
    stdev_set = statistics.stdev(set_all)
    print(f'stdev_all: {stdev_all}')
    print(f'stdev_set: {stdev_set}')
    variance_all = statistics.variance(self.index_total_count)
    print(f'{variance_all=}')

  def draw(self):
    # todo: view 確定後に、画面位置サイズ情報を取得
    _, _, w, h = self.frame
    self.init_grid_cells(w, h)
    self.init_grid_colors()
    self.set_guide_oval(4, 1)

  def layout(self):
    pass


if __name__ == '__main__':
  cell_radius: int = 9
  view = View(cell_radius)
  #view.present(style='fullscreen', orientations=['portrait'])
  view.present(style='panel', orientations=['portrait'])

