# PigletC

import sys
from parse import parse
from tools import *
from trans import trans
from gen import gen

class Compiler:
  def __init__(self, path, src):
    self.path = path
    self.src = src
    self.table = {}
    self.data_cnt = 0
    self.label_cnt = 0
    self.ir = []
    self.asm = ""
    self.curr_func = ""

def compile(c):
  ast = parse(src, lambda p: error("syntax error", c.path, c.src, p))
  apply_rule(trans, ast, c=c)
  c.asm = "\n".join(apply_rule(gen, c.ir, c=c) + ["DONE", ""])

if len(sys.argv) == 2:
  path = sys.argv[1]
  with open(path) as f:
    src = f.read()
  c = Compiler(path, src)
  compile(c)
  with open("%s.pvm" % path, "w") as f:
    f.write(c.asm)
