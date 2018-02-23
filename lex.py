import re

class Lex:
  def __init__(self, source, rules):
    self.source = source
    self.rules = rules
    self.pos = 0

def scan(lex):
  while True:
    pos = lex.pos
    for pat, func in lex.rules:
      matched = re.match(pat, lex.source[lex.pos:])
      if matched:
        pos = lex.pos + len(matched.group())
        token = func(lex, lex.pos, pos)
        if token is not None:
          yield token
        break
    if lex.pos == pos:
      return
    lex.pos = pos

# Example

def skip_token(lex, i, j):
  return None

def number_token(base):
  def func(lex, i, j):
    return ("number", int(lex.source[i:j], base), i)
  return func

def string_token(lex, i, j):
  return ("string", lex.source[i + 1:j - 1], i)

def token(tag):
  def func(lex, i, j):
    return (tag, lex.source[i:j], i)
  return func

rules = (
  (r"\s+", skip_token),
  (r"\\[^\n]*", skip_token),
  (r"0[xX][a-fA-F0-9]+", number_token(16)),
  (r"\d+", number_token(10)),
  (r'".*"', string_token),
  (r"[+\-*/=;()]", token("op")),
  (r"\w+", token("name"))
)

source = """
a = 0xff;
b = 42 + 1;
print("hello");
"""

s = Lex(source, rules)

for l in scan(s):
  print(l)

print(s.pos == len(s.source))
