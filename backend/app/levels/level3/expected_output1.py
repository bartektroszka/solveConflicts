def silnia(n):
    if n == 0:
        return 1
    return n * silnia(n - 1)


def catalan(n):
    return silnia(n + n) // silnia(n + 1) // silnia(n)


def taylor_e(x):
    wynik = 0
    for i in range(100):
        wynik += x ** i / silnia(i)
    return wynik


print(catalan(7))
print(taylor_e(2))
