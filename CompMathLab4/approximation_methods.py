from utility import *
from math import log, exp
def linear_approximation(x_p, y_p, n):
    sum_of_x = [sum(x) for x in arr_exp(x_p, 2)]
    vals = sum_of_y(x_p, y_p, 1)
    matrix = [[n, sum_of_x[0]],[sum_of_x[0], sum_of_x[1]]]
    b = [vals[0], vals[1]]
    a, b = solve_equation(matrix,b)
    func_str = "a + b * x"
    return lambda x: a + b * x,func_str, a, b

def quad_approximation(x_p, y_p, n):
    sum_of_x = [sum(x) for x in arr_exp(x_p, 4)]
    vals = sum_of_y(x_p, y_p, 2)
    matrix = [[n, sum_of_x[0], sum_of_x[1]],[sum_of_x[0], sum_of_x[1], sum_of_x[2]],[sum_of_x[1], sum_of_x[2], sum_of_x[3]]]
    b = [vals[0], vals[1], vals[2]]
    a, b, c = solve_equation(matrix,b)
    func_str = "a + b * x + c * x ** 2"
    return lambda x: a + b * x + c * x ** 2, func_str, a, b, c

def cub_approximation(x_p, y_p, n):
    sum_of_x = [sum(x) for x in arr_exp(x_p, 6)]
    vals = sum_of_y(x_p, y_p, 3)
    matrix = [[n, sum_of_x[0], sum_of_x[1], sum_of_x[2]],[sum_of_x[0], sum_of_x[1], sum_of_x[2], sum_of_x[3]],
            [sum_of_x[1], sum_of_x[2], sum_of_x[3], sum_of_x[4]],[sum_of_x[2], sum_of_x[3], sum_of_x[4], sum_of_x[5]]]
    b = [vals[0], vals[1], vals[2], vals[3]]
    a, b, c, d = solve_equation(matrix,b)
    func_str = "a + b * x + c * x ** 2 + d * x ** 3"
    return lambda x: a + b * x + c * x ** 2 + d * x ** 3, func_str, a, b, c, d

def exponential_approximation(x_p, y_p, n):
    y_p1 = [log(y) for y in y_p]
    func,f_s, a, b = linear_approximation(x_p, y_p1, n)
    a = exp(a)
    func_str = "a * exp(b*x)"
    return lambda x: a * exp(b * x),func_str, a, b

def logarithmic_approximation(x_p, y_p, n):
    x_p1 = [log(x) for x in x_p]
    func,f_s, a, b = linear_approximation(x_p1, y_p, n)
    func_str = "a + b * log(x)"
    return lambda x: a + b * log(x),func_str, a, b

def power_approximation(x_p, y_p, n):
    x_p1 = [log(x) for x in x_p]
    y_p1 = [log(y) for y in y_p]
    func,f_s, a, b = linear_approximation(x_p1, y_p1, n)
    a = exp(a)
    func_str = "a * x ** b"
    return lambda x: a * x ** b,func_str, a, b