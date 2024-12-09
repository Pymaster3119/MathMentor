from sympy import symbols, Eq, solve

t = symbols('t')
equation = Eq(75*t, 60*(t + 2))
solution = solve(equation, t)
solution[0]

