# リファクタリング

#import itertools

r = 5

pick_list = []
l = (r * 2) + 1
a = r
x = 0
y = r


def set_indexs(ab):
  _a, _b = ab
  _a += r
  _b += r
  return [_a, _b]


def set_index(
  x_index: int, y_index: int
) -> list[list[int, int], list[int, int], list[int, int], list[int, int], list[
    int, int], list[int, int], list[int, int], list[int, int]]:

  indexs = [
    [x_index, y_index],
    [-x_index, y_index],
    [-x_index, -y_index],
    [x_index, -y_index],
    [y_index, x_index],
    [-y_index, x_index],
    [-y_index, -x_index],
    [y_index, -x_index],
  ]
  return indexs


while x < y:
  print(x)
  [pick_list.append(items) for items in set_index(x, y)]

  a = a - (x * 2) - 1
  #a -= (x * 2) - 1
  x += 1
  if a < 0:
    a = a + (y * 2) - 1
    y -= 1

grid_indexs = [[[x, y] for y in range(l)] for x in range(l)]

oval_indexs = list(map(set_indexs, pick_list))

v = '\n'

for rows in grid_indexs:
  for column in rows:
    _x, _y = column
    if column in oval_indexs:
      #v += '▫︎ '
      v += '🌝 '
    else:
      #v += '◾︎ '
      v += '🌚 '
    if _y == l - 1:
      v += '\n'

print(v)



