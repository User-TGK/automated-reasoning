from z3 import *
from typing import Final

ITERATIONS: Final = 10
MAX_N: Final = 10

unknowns = [Bool(f"u{i+1}") for i in range(ITERATIONS)]
a_vars = [Int(f"a{i+1}") for i in range(ITERATIONS)]
b_vars = [Int(f"b{i+1}") for i in range(ITERATIONS)]

s = Solver()

def f(i, a, b):
    If(unknown[i], a)

for i in range(1, ITERATIONS + 1):
    last_a = None
    last_b = None

    # Initialize to 1 if we are in the first iteration
    if i == 1:
        last_a = 1
        last_b = 1
    # Take the values from the previous iteration otherwise
    else:
        last_a = a_vars[i-2]
        last_b = b_vars[i-2]

    s.add(If(unknowns[i-1],
             And(a_vars[i-1] == last_a + 2*last_b, b_vars[i-1] == last_b + i),
             And(b_vars[i-1] == last_a + last_b, a_vars[i-1] == last_a + i)))

for i in range(1, MAX_N + 1):
    s_copy = copy.deepcopy(s)
    s_copy.add(b_vars[ITERATIONS-1] == 700 + i)
    print(f"n{i}: {s_copy.check()}")
