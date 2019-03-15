# Forth Wizard for Z3

from z3 import *


DEPTH = 10


INS = [1, 4, 2, 3, 4]
OUTS = [1, 2, 1, 2, 1, 2, 2, 1, 1]


class State:
    def __init__(self, step):
        self.st = [Int("st_%d_%d" % (step, r)) for r in range(DEPTH)]
        self.sp = Int("sp_%d" % step)


def idx(i):
    return min(max(i, 0), DEPTH - 1)


def drop(states, pc):
    expr = []
    expr.append(states[pc].sp == states[pc - 1].sp - 1)
    for i in range(DEPTH):
        expr.append(states[pc].st[i] == states[pc - 1].st[i])
    return And(expr)


def dup(states, pc):
    expr = []
    expr.append(states[pc].sp == states[pc - 1].sp + 1)
    expr.append(states[pc - 1].sp > 0)
    for i in range(DEPTH):
        expr.append(
            If(i == states[pc].sp - 1, states[pc].st[i] == states[pc - 1].st[idx(i - 1)],
            states[pc].st[i] == states[pc - 1].st[i])
        )
    return And(expr)


def over(states, pc):
    expr = []
    expr.append(states[pc].sp == states[pc - 1].sp + 1)
    expr.append(states[pc - 1].sp > 1)
    for i in range(DEPTH):
        expr.append(
            If(i == states[pc].sp - 1, states[pc].st[i] == states[pc - 1].st[idx(i - 2)],
            states[pc].st[i] == states[pc - 1].st[i])
        )
    return And(expr)


def swap(states, pc):
    expr = []
    expr.append(states[pc].sp == states[pc - 1].sp)
    expr.append(states[pc - 1].sp > 1)
    for i in range(DEPTH):
        expr.append(
            If(i == states[pc].sp - 2, states[pc].st[i] == states[pc - 1].st[idx(i + 1)],
            If(i == states[pc].sp - 1, states[pc].st[i] == states[pc - 1].st[idx(i - 1)],
            states[pc].st[i] == states[pc - 1].st[i]))
        )
    return And(expr)


def rot(states, pc):
    expr = []
    expr.append(states[pc].sp == states[pc - 1].sp)
    expr.append(states[pc - 1].sp > 2)
    for i in range(DEPTH):
        expr.append(
            If(i == states[pc].sp - 3, states[pc].st[i] == states[pc - 1].st[idx(i + 1)],
            If(i == states[pc].sp - 2, states[pc].st[i] == states[pc - 1].st[idx(i + 1)],
            If(i == states[pc].sp - 1, states[pc].st[i] == states[pc - 1].st[idx(i - 2)],
            states[pc].st[i] == states[pc - 1].st[i])))
        )
    return And(expr)


OPS = [dup, drop, swap, over, rot]


def instr(states, op, pc):
    expr = OPS[-1](states, pc)
    for i in reversed(range(len(OPS) - 1)):
        expr = If(op == i, OPS[i](states, pc), expr)
    return expr


def opt(steps):
    def fill_stack(state, data):
        for i in range(len(data)):
            s.add(state.st[i] == data[i])
        s.add(state.sp == len(data))


    s = Solver()
    states = [State(i) for i in range(steps)]
    for i in range(steps):
        s.add(states[i].sp >= 0, states[i].sp < DEPTH)
    code = IntVector("code", steps - 1)
    for x in code:
        s.add(x >= 0, x < len(OPS))

    fill_stack(states[0], INS)
    fill_stack(states[-1], OUTS)

    for i in range(steps - 1):
        s.add(instr(states, code[i], i + 1))
    return s, states, code


steps = 2
while True:
    print(".")
    s, states, code = opt(steps)
    if s.check() == sat:
        break
    steps += 1

m = s.model()


def dump_stack(states, pc):
    sp = m.eval(states[pc].sp).as_long()
    for i in range(sp):
        print(m.eval(states[pc].st[i]), end=" ")


for i in range(steps):
    dump_stack(states, i)
    print()

names = [f.__name__ for f in OPS]
for x in code:
    print(names[m.eval(x).as_long()], end=" ")
