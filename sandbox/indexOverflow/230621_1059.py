def ovflw(_o: int) -> int:
  o = _o % d
  return o


def nor2pos(_p: int) -> int:
  p = _p % d
  return p


def pos2nor(_n: int) -> int:
  n = _n % d
  return ri[n]


d = 5
r = 2

# [ 0,  1, 2, 3, 4]
# [-2, -1, 0, 1, 2]
# list(range(-r, r+1))

di = list(range(d))
ri = list(range(-r, r + 1))

aa = list(map(ovflw, ri))

