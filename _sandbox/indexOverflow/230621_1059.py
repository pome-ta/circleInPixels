def ovflw(_o: int) -> int:
  o = _o % d
  return o


def pos2nor(_p: int) -> int:
  p = ovflw(_p)
  return ri[p]


def nor2pos(_n: int) -> int:
  pass


d = 5
r = 2

# [ 0,  1, 2, 3, 4]
# [-2, -1, 0, 1, 2]
# list(range(-r, r+1))

di = list(range(d))
ri = list(range(-r, r + 1))

aa = list(map(pos2nor, range(7)))

