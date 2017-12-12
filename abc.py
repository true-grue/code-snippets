from dsl_parse import *

equal_size = lambda s: len(set(map(len, s.out.pop()))) == 1
L = lambda x: quote(some(a(x)))
abc = seq(group(L("a"), L("b"), L("c"), L("d")), equal_size)

s = Stream("aabbccdd")
print abc(s)
print s.out
