def silnia(n):
  if n == 0:
    return 1
  return n * silnia(n - 1)

def catalan(n):
  return silnia(n + n) // silnia(n + 1) // silnia(n)

print(catalan(7))