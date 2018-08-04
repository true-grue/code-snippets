# simple lexer

import re

class Lex:
  def __init__(self, source):
    self.source = source
    self.pos = 0

def scan(lex, rules):
  while True:
    next_pos = lex.pos
    for pat, func in rules:
      matched = re.match(pat, lex.source[lex.pos:])
      if matched:
        next_pos = lex.pos + len(matched.group())
        token = func(lex, lex.pos, next_pos)
        if token is not None:
          yield token
        break
    if lex.pos == next_pos:
      return
    lex.pos = next_pos

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

lex_rules = (
  (r"\s+", skip_token),
  (r"#[^\n]*", skip_token),
  (r"0[xX][a-fA-F0-9]+", number_token(16)),
  (r"\d+", number_token(10)),
  (r'".*"', string_token),
  (r"[+\-*/=;()]", token("op")),
  (r"\w+", token("name"))
)

source = """
# comment
a = 0xff;
b = 42 + 1;
print("hello");
"""

s = Lex(source)

for l in scan(s, lex_rules):
  print(l)

print(s.pos == len(s.source))
