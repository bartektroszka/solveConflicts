def silnia(n):
  wynik = 1
  for i in range(1, n + 1):
    wynik = wynik * i
  return wynik

def taylor_e(x):
  wynik = 0
  for i in range(100):
    wynik += x**i / silnia(i)
  return wynik

def catalan(n):
  pass

print(catalan(7))
print(taylor_e(2))