# Toy Term Rewriting System (TTRS)
# Author: Peter Sovietov

def match(scope, pat, term):
  if isinstance(pat, tuple):
    if pat[0] in MATCH:
      return MATCH[pat[0]](scope, pat, term)
    if not isinstance(term, tuple) or len(pat) != len(term):
      return False
    for i in range(len(pat)):
      if not match(scope, pat[i], term[i]):
        return False
    return True
  return pat == term

def build(scope, term):
  if not isinstance(term, tuple):
    return term
  lst = []
  for x in term:
    lst.append(build(scope, x))
  term = tuple(lst)
  if term[0] in BUILD:
    return BUILD[term[0]](scope, term)
  return term

M = lambda x: ("M", x)
App = lambda *x: ("App",) + x

def match_m(scope, pat, term):
  if pat[1] in scope:
    return match(scope, scope[pat[1]], term)
  scope[pat[1]] = term
  return True

def build_m(scope, term):
  return scope[term[1]]

def build_app(scope, term):
  op, left, right = term[1:]
  if op == "+":
    return left + right
  if op == "-":
    return left - right
  if op == "*":
    return left * right
  if op == "/":
    return left / right
  if op == "^":
    return left ** right

MATCH = dict(M=match_m)
BUILD = dict(M=build_m, App=build_app)

def rewrite(rules, term):
  for rule in rules:
    left, right = rule
    scope = {}
    if match(scope, left, term):
      return True, build(scope, right)
  return False, term

def innermost(rules, term):
  while isinstance(term, tuple):
    lst = []
    for x in term:
      lst.append(innermost(rules, x))
    m, term = rewrite(rules, tuple(lst))
    if not m:
      break
  return term

Var = lambda x: ("Var", x)
Num = lambda x: ("Num", x)
Add = lambda x, y: ("+", x, y)
Sub = lambda x, y: ("-", x, y)
Mul = lambda x, y: ("*", x, y)
Div = lambda x, y: ("/", x, y)
Pow = lambda x, y: ("Pow", x, y)
Deriv = lambda x, y: ("Deriv", x, y)

eval_rules = [
  [Add(Num(M("x")), Num(M("y"))), Num(App("+", M("x"), M("y")))],
  [Sub(Num(M("x")), Num(M("y"))), Num(App("-", M("x"), M("y")))],
  [Mul(Num(M("x")), Num(M("y"))), Num(App("*", M("x"), M("y")))],
  [Div(Num(M("x")), Num(M("y"))), Num(App("/", M("x"), M("y")))],
  [Add(M("x"), Num(0)), M("x")],
  [Add(Num(0), M("x")), M("x")],
  [Add(M("x"), Num(M("y"))), Add(Num(M("y")), M("x"))],
  [Add(Num(M("x")), Add(Num(M("y")), M("z"))),
    Add(Add(Num(M("x")), Num(M("y"))), M("z"))],
  [Sub(M("x"), Num(0)), M("x")],
  [Sub(M("x"), M("x")), Num(0)],
  [Mul(M("x"), Num(1)), M("x")],
  [Mul(Num(1), M("x")), M("x")],
  [Mul(M("x"), Num(0)), Num(0)],
  [Mul(Num(0), M("x")), Num(0)],
  [Mul(M("x"), Num(M("y"))), Mul(Num(M("y")), M("x"))],
  [Mul(Num(M("x")), Mul(Num(M("y")), M("z"))),
    Mul(Mul(Num(M("x")), Num(M("y"))), M("z"))],
  [Div(M("x"), Num(1)), M("x")],
  [Div(M("x"), M("x")), Num(1)],
  [Div(Num(0), M("x")), Num(0)],
  [Pow(M("x"), Num(1)), M("x")],
  [Pow(M("x"), Num(0)), Num(1)]
]

deriv_rules = [
  [Deriv(M("x"), Num(M("y"))), Num(0)],
  [Deriv(M("x"), M("x")), Num(1)],
  [Deriv(M("x"), Pow(M("u"), M("v"))),
    Mul(Mul(M("v"), Pow(M("u"), Sub(M("v"), Num(1)))), Deriv(M("x"), M("u")))],
  [Deriv(M("x"), Add(M("u"), M("v"))),
    Add(Deriv(M("x"), M("u")), Deriv(M("x"), M("v")))],
  [Deriv(M("x"), Mul(M("u"), M("v"))),
    Add(Mul(M("u"), Deriv(M("x"), M("v"))), Mul(M("v"), Deriv(M("x"), M("u"))))]
]

expr = Pow(Add(Mul(Num(2), Var("x")), Num(7)), Num(3))
expr = innermost(deriv_rules, Deriv(Var("x"), expr))
expr = innermost(eval_rules, expr)
print(expr)
