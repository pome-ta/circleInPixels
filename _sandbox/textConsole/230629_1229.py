r = 5

pick_list = []

a = r
x = 0
y = r

while x < y:
  x += 1
  a = a - (x * 2) - 1
  if a < 0:
    y -= y
    a = a + (y * 2) - 1
  pick_list.append([[x, y], [-x, y], [x, -y], [y, x], [-y, -x], y, -x])

