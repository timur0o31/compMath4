import matplotlib.pyplot as plt
from approximation_methods import *
def parse_from_file(input_file):
    try:
        x = []
        y = []
        with open(input_file, 'r') as file:
            lines = file.readlines()
            if not lines:
                raise ValueError("Файл пустой")
            n = len(lines)
            if (n==2):
                    x = list(map(float, lines[0].split()))
                    y = list(map(float, lines[1].split()))
                    if len(x) != len(y):
                        print("В файле должно быть одинаковое количество точек и значений!")
                        exit(1)
                    if (len(x)<8) or (len(x)>12):
                        print("В файле должно быть от 8 до 12 точек!")
                        exit(1)
            elif n<8 or n>12:
                print(f"В файле не может быть {n} строк.",end = " ")
                print("В файле должно быть от 8 до 12 точек!")
                exit(1)
            else:
                for i in range(n):
                    values = list(map(float, lines[i].split()))
                    if len(values) != 2:
                        raise ValueError(f"Ошибка в строке {i+1}: ожидалось {2} чисел, получено {len(values)}")
                    x.append(values[0])
                    y.append(values[-1])
        return x, y
    except FileNotFoundError:
        print(f"Ошибка: файл '{input_file}' не найден.")
        raise
def parse_from_terminal():
    x = []
    y = []
    n = 0
    while True:
        try:
            n = int(input("Введите количество точек: "))
            if n < 8 or n>12:
                raise Exception("Количество точек должно быть от 8 до 12!")
            break
        except ValueError:
            print("Введите целое число!")
        except Exception as e:
            print(e)
    print("Введите точки для апроксимирующей функции через пробел")
    i=0
    while i < n:
            try:
                x_and_y = list(map(float,input(f"Введите {i+1} точку и значение функции в данной точке: \n").split()))
                if len(x_and_y) != 2:
                    raise Exception(f"Строка {i+1} должна содержать {2} значения")
                x.append(x_and_y[0])
                y.append(x_and_y[1])
                i += 1
            except ValueError:
                print(f"Ошибка ввода строки {i+1}. Убедитесь, что все элементы являются числами")
                continue
            except Exception as exception:
                print(f"Ошибка ввода строки {i+1}: {exception}")
                continue
    return x,y

def draw_plot(a, b, func, dx=0.1):
    x_p, y_p = [], []
    a -= dx
    b += dx
    x = a
    while x <= b:
        x_p.append(x)
        y_p.append(func(x))
        x += dx
    plt.plot(x_p, y_p, 'g')

def solve():
    x_p=[]
    y_p=[]
    print("Выберите режим: для ввода с консоли нажмите 1, для ввода с файла нажмите 2")
    while True:
        ans = input()
        if ans == '1':
            while True:
                try:
                    x_p, y_p = parse_from_terminal()
                    break
                except ValueError:
                    print("Ошибка: введите целое число.")
            break
        elif ans == '2':
            print("Введите путь к файлу")
            while True:
                file_name = input()
                try:
                    x_p, y_p  = parse_from_file(file_name)
                    break
                except FileNotFoundError:
                    print(f"Указан некорректный путь, попробуйте снова.")
                    continue
                except Exception as exception:
                    print(f"Файл задан с ошибкой: {exception}")
                    exit(1)
            break
        else:
            print("Введите 1 или 2!")
    if all(x>0 for x in x_p) and all(y>0 for y in y_p):
        approximation_funcs = {
            "Линейная апроксимация": linear_approximation,
            "Степенная апроксимация": power_approximation,
            "Экспоненциальная апроксимация" : exponential_approximation,
            "Логарифмическая апроксимация": logarithmic_approximation,
            "Квадратичная апроксимация": quad_approximation,
            "Кубическая апроксимация": cub_approximation
        }
    else:
        print("Так как для степенной, экспонициальной и логарифмической функций для апроксимации нужно их линеаризировать,")
        print("То при отрицательных входных данных, можно апроксимировать только 3 оставшиеся функции")
        print("Замените точки, если хотите увидеть все 6 апроксимирующих функции")
        print("-"*50)
        approximation_funcs = {
            "Линейная апроксимация": linear_approximation,
            "Квадратичная апроксимация": quad_approximation,
            "Кубическая апроксимация": cub_approximation,
        }

    n = len(x_p)
    mn_sigma = 10000000000000000000
    ans_func = None
    for func_name, func in approximation_funcs.items():
        print(f"{func_name}:")
        phi, phi_str, *coef = func(x_p, y_p, n)
        coef_dev = calc_deviation(x_p,y_p,phi)
        σ = stand_deviation(x_p,y_p,phi,n)
        coef_det = coeff_of_determination(x_p, y_p, phi, n)
        if σ < mn_sigma:
            mn_sigma = σ
            ans_func = func_name
        print(f'phi(x) = {phi_str}')
        coef_len = len(coef)
        lit = ["a", "b", "c", "d"]
        print('coeffs:', end = "")
        for i in range(coef_len):
            print(f" {lit[i]}: {coef[i]:.5f}", end = ",")
        print()
        if coef_det is None:
            print(f'S = {coef_dev:.5f}, σ = {σ:.5f}, R^2 = невозможно вычислить')
        else:
            print(f'S = {coef_dev:.5f}, σ = {σ:.5f}, R^2 = {coef_det:.5f}')
        if func is linear_approximation:
            print(f'r = {pearson_corr_coeff(x_p, y_p, n):.5f}')
        plt.title(func_name)
        draw_plot(x_p[0],x_p[-1],phi)
        for i in range(n):
            plt.scatter(x_p[i], y_p[i], c='r')
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()
        print('-' * 50)
    print(f'Лучшая функция: {ans_func}')
    print(f"{mn_sigma:.5f}")
solve()