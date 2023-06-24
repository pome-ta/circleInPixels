import ui

def set_color(radius, x, y, cell):
  ui.set_color('red') if x == radius or y == radius else ui.set_color(0.25)
  cell.fill()
  
  ui.set_color(0.75)
  cell.stroke()


class View(ui.View):

  def __init__(self):
    self.bg_color = 1

  def did_load(self):
    pass

  def will_close(self):
    pass

  def draw(self):
    _, _, w, h = self.frame
    r = 6
    n = int(r * 2 + 1)
    l = min(w, h)
    cell_size = l / n

    self.cells = [[
      ui.Path.rect(cell_size * x, cell_size * y, cell_size, cell_size)
      for x in range(n)
    ] for y in range(n)]

    for x in range(n):
      for y in range(n):
        set_color(r, x, y, self.cells[x][y])
        #rect = self.cells[x][y]
        #ui.set_color(0.75)
        #rect.stroke()

    #for x_cell in self.
    '''
    for x in range(n):
      for y in range(n):
        ui.set_color('red') if x == r or y == r else ui.set_color(0.25)

        rect = ui.Path.rect(cell_size * x, cell_size * y, cell_size, cell_size)
        rect.fill()
        ui.set_color(0.75)
        rect.stroke()
    '''

  def layout(self):
    pass


if __name__ == '__main__':
  view = View()
  #view.present()
  #view.present(hide_title_bar=True)
  view.present(style='fullscreen', orientations=['portrait'])

