# 円のアルゴリズム [計算機科学の分野で、直感に反する法則などはありますか? - Quora](https://jp.quora.com/%E8%A8%88%E7%AE%97%E6%A9%9F%E7%A7%91%E5%AD%A6%E3%81%AE%E5%88%86%E9%87%8E%E3%81%A7-%E7%9B%B4%E6%84%9F%E3%81%AB%E5%8F%8D%E3%81%99%E3%82%8B%E6%B3%95%E5%89%87%E3%81%AA%E3%81%A9%E3%81%AF%E3%81%82%E3%82%8A%E3%81%BE)

import functools

import ui

# --- color 定義
g_stroke: str | float | int = 0.75
g_fill: str | float | int = 0.25
c0: str | float = 0.88
c1: str | float = 'maroon'
c2: str | float = 'blue'
c3: str | float = 'green'
c4: str | float = 'yellow'


def release_normalize(xy_index: list[int, int],
                      radius_length: int) -> list[int, int]:
  _x, _y = xy_index
  _x += radius_length
  _y += radius_length
  return [_x, _y]


def get_normalize_oval_indexs(radius_length: int) -> list:
  x = 0
  y = radius_length
  a = radius_length
  oval_list = []

  set_index = lambda _x, _y: [[_x, _y], [-_x, _y], [-_x, -_y], [_x, -_y],
                              [_y, _x], [-_y, _x], [-_y, -_x], [_y, -_x]]

  while x < y:
    [oval_list.append(items) for items in set_index(x, y)]
    a = a - (x * 2) - 1
    x += 1
    if a < 0:
      a = a + (y * 2) - 1
      y -= 1

  return oval_list


class DrawCanvas(ui.View):

  def __init__(self, r: int = 2, *args, **kwargs):
    # --- 初期定義
    self.cell_rad: int  # cell の半径
    self.cells: list[list[ui.Path]]
    self.oval_indexs: list

    # --- 変数反映
    self.bg_color = 0
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

  def draw(self):
    # todo: view 確定後に、画面位置サイズ情報を取得
    _, _, w, h = self.frame
    self.init_grid_cells(w, h)
    self.init_grid_colors()

    normalize_oval_indexs: list = get_normalize_oval_indexs(self.cell_rad)

    self.oval_indexs = list(
      map(functools.partial(release_normalize, radius_length=self.cell_rad),
          normalize_oval_indexs))

    for xy_index in self.oval_indexs:
      self.set_cell(xy_index, c3, g_stroke)

  def layout(self):
    pass


class ControlView(ui.View):

  def __init__(self, *args, **kwargs):
    self.bg_color = 'red'

    self.wrap_view = ui.View()
    self.wrap_view.bg_color = 'blue'

    self.add_subview(self.wrap_view)
    self.setup_buttons()

  def setup_buttons(self):
    self.down_button = self.create_button_item('iob:arrow_down_b_32', -1)
    self.up_button = self.create_button_item('iob:arrow_up_b_32', 1)

    # xxx: いい感じに調整

    self.wrap_view.add_subview(self.down_button)
    self.wrap_view.add_subview(self.up_button)

  def create_button_item(self, img_path: str, rate: int):
    img = ui.Image.named(img_path)
    btn = ui.Button(image=img)
    btn.rate = rate
    wrap = ui.View()
    wrap.bg_color = 'green'
    wrap.add_subview(btn)
    return wrap

  def layout(self):
    _, _, w, h = self.frame
    min_size = min(w, h)
    margin = min_size - (min_size * 0.88)

    width_size = w - margin
    height_size = h - margin

    position_x = (w / 2) - (width_size / 2)
    position_y = (h / 2) - (height_size / 2)

    self.wrap_view.width = width_size
    self.wrap_view.height = height_size

    self.wrap_view.x = position_x
    self.wrap_view.y = position_y

    #for btn in self.


class View(ui.View):

  def __init__(self, r: int = 2, *args, **kwargs):
    # --- 変数反映
    self.bg_color = 1
    self.canvas = DrawCanvas(r)
    self.add_subview(self.canvas)

    self.img = ui.Image.named('iob:arrow_down_b_32')
    self.btn = ui.Button(image=self.img)

    self.add_subview(self.btn)
    self.control_view = ControlView()

    self.add_subview(self.control_view)

  def layout(self):
    _, _, w, h = self.frame

    min_size = min(w, h)
    self.canvas.width = min_size
    self.canvas.height = min_size

    canvas_x = (w / 2) - (min_size / 2)
    self.canvas.x = canvas_x

    self.control_view.width = min_size
    self.control_view.y = min_size


if __name__ == '__main__':
  cell_radius: int = 8

  view = View(cell_radius)

  view.present(style='fullscreen')

  #view.present(style='fullscreen', orientations=['portrait'])

  #view.present(style='panel', orientations=['portrait'])

