PROF = {}

def prof(name):
  def prof1(f):
    def prof2(*args, **kwargs):
      PROF[name] = PROF.get(name, 0) + 1
      return f(*args, **kwargs)
    return prof2
  return prof1

@prof("factorial")
def fact(n):
  if n < 2:
    return 1
  else:
    return n * fact(n - 1)

@prof("fibonacci number")
def fib(n):
  if n > 1:
    return fib(n - 1) + fib(n - 2)
  return n

@prof("ackermann")
def ack(m, n):
  if m == 0:
    return n + 1
  elif n == 0:
    return ack(m - 1, 1)
  else:
    return ack(m - 1, ack(m, n - 1))

fact(10)
fib(10)
ack(3, 3)

print(PROF)
