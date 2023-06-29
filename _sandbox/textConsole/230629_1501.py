import itertools

r = 9

pick_list = []
l = (r * 2) + 1
a = r
x = 0
y = r


def set_indexs(ab):
  a, b = ab
  a += r
  b += r
  return [a, b]


while x < y:
  #x += 1
  a = a - (x * 2) - 1
  x += 1
  if a < 0:
    #y -= 1
    a = a + (y * 2) - 1
    y -= 1
  pick_list.append([
    [x, y],
    [-x, y],
    [-x, -y],
    [x, -y],
    [y, x],
    [-y, x],
    [-y, -x],
    [y, -x],
  ])

pick_flat = list(itertools.chain.from_iterable(pick_list))

grid_indexs = [[[x, y] for y in range(l)] for x in range(l)]

oval_indexs = list(map(set_indexs, pick_flat))

v = '\n'

for rows in grid_indexs:
  for column in rows:
    _x, _y = column
    if column in oval_indexs:
      v += '▫︎ '
    else:
      v += '◾︎ '
    if _y == l - 1:
      v += '\n'

print(v)

