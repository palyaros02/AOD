task = """
20(1). Посчитать число последовательностей нулей и единиц длины n, в которых не встречаются две идущие подряд единицы.
Динамическое программирование
"""

import time


def timeit(f):  # декоратор для замера времени
    def wrap(*args):
        time_start = time.time()
        ret = f(*args)
        time_end = time.time()
        print('Время работы функции "%s" : %0.3f нс' % (f.__name__, (time_end - time_start) * 10000.0))
        return ret

    return wrap


def check(s):
    a = s % 0b10
    s //= 0b10
    while s != 0:
        b = s % 0b10
        s //= 0b10
        if a * b == 1:
            return False
        a = b
    return True


@timeit
def bruteforce(n):  # простой перебор
    steps = 0
    ans = 0
    num = 0b0
    for i in range(2 ** n - 1):
        steps += 1
        if check(num):
            # print(bin(num))
            ans += 1
        num += 1
    print("Шагов:", steps)
    print("Ответ:", ans)


@timeit
def dynamic(n):  # выведенная формула
    f = [2, 3]  # массив рассчитанных значений
    steps = 1
    for i in range(3, n + 1):
        f.append(f[i - 2] + f[i - 3])
        steps += 1
    print("Шагов:", steps)
    print("Ответ:", f[n - 1])


if __name__ == '__main__':
    print(task)
    nodes = int(input("Введите n (длина последовательности): "))
    print("\nПростой перебор:")
    bruteforce(nodes)
    print("\nДинамическое программирование:")
    dynamic(nodes)
