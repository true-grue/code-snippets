import operator
from functools import reduce

def lisp(s):
  if isinstance(s, list) and s and callable(s[0]):
    return s[0](s[1:])
  return s

def define(f):
  return lambda s: lisp(f(*map(lisp, s)))

def ifelse(s):
  cond, a, b = s
  return lisp(a if lisp(cond) else b)

def make_unop(op):
  return lambda s: op(lisp(s[0]))

def make_binop(op):
  return lambda s: reduce(lambda x, y: op(lisp(x), lisp(y)), s)

neg = make_unop(operator.neg)
add = make_binop(operator.add)
sub = make_binop(operator.sub)
mul = make_binop(operator.mul)
eq = make_binop(operator.eq)
lt = make_binop(operator.lt)

fact = define(lambda n: [ifelse, [lt, n, 2],
  1,
  [mul, n, [fact, [sub, n, 1]]]
])

print(lisp([fact, 5]))
