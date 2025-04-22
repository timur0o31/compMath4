from math import sqrt
def factorial(k):
    if k==1:
        return 1
    else:
        return k*factorial(k-1)
def determinant(triangle_matrix, sign):
    ans = 1
    for i in range(len(triangle_matrix)):
        ans*=triangle_matrix[i][i]
    return ans*(-1)**sign
def forw_gauss(m,b):
    n=len(m)
    matrix = [[x for x in m[i]] for i in range(n)]
    new_b = [x for x in b]
    sign = 0
    for i in range(n-1):
        while matrix[i][i] == 0:
            matrix = matrix[:i] + matrix[i + 1:] + [matrix[i]]
            new_b = new_b[:i] + new_b[i + 1:] + [new_b[i]]
            sign += 1
            if sign > factorial(n):
                print("Матрица СЛАУ не соответствует теореме Кронекера-Капелли.")
                exit(0)
        for k in range(i+1,n):
            t = matrix[k][i]/matrix[i][i]
            matrix[k][i] = 0
            for j in range(i+1,n):
                matrix[k][j] = matrix[k][j]-t*matrix[i][j]
            new_b[k] = new_b[k] - t*new_b[i]
    ans = []
    for i in range(n):
        k=[]
        for j in range(n):
            k.append(matrix[i][j])
        k.append(new_b[i])
        ans.append(k)
    return ans, sign


def back_gauss(matrix, det):
    n = len(matrix)
    x1 = [0 for x in range(n)]
    if det==0:
        return 0
    for i in range(n-1,-1,-1):
        k=0
        for j in range(i+1,n):
            k+=matrix[i][j]*x1[j]
        x1[i]=(matrix[i][n]-k)/matrix[i][i]
    return x1
def solve_equation(matrix,b):
    n_matrix, sign = forw_gauss(matrix,b)
    det = determinant(n_matrix,sign)
    x1 = back_gauss(n_matrix,det)
    return x1

def arr_exp(arr, n1):
    res = []
    for n in range(1, n1 + 1):
        l = []
        for a in arr:
            l.append(a ** n)
        res.append(l)
    return res

def sum_of_y(arr1, arr2, n1):
    res = []
    for n in range(n1 + 1):
        sm = 0
        for x,y in zip(arr1, arr2):
            sm += x**n*y
        res.append(sm)
    return res

def calc_deviation(x_p, y_p, phi):
    sm = 0
    t=[]
    for x,y in zip(x_p, y_p):
        t.append(phi(x)-y)
    for i in t:
        sm += i ** 2
    return sm
def stand_deviation(x_p, y_p, phi, n):
    s1 = 0
    for x,y in zip(x_p, y_p):
        s1 += (phi(x) - y) ** 2
    return sqrt(s1/n)

def pearson_corr_coeff(x_p, y_p, n):
    sr_x = sum(x_p) / n
    sr_y = sum(y_p) / n
    s1 = 0
    s2 = 0
    s3 = 0
    for x,y in zip(x_p, y_p):
        s1 += (x - sr_x) * (y - sr_y)
        s2 +=  (x - sr_x) ** 2
        s3 += (y - sr_y) ** 2
    if (s2==0):
        print("дисперсия по x, равна 0, невозможно рассчитать коэффициент Пирсона")
        return 0
    elif (s3==0):
        print("дисперсия по y, равна 0, невозможно рассчитать коэффициент Пирсона")
        return 0
    s23 = sqrt(s2 * s3)
    return s1/s23

def coeff_of_determination(x_p, y_p, phi, n):
    s1 = 0
    s2 = 0
    s3 = 0
    for x,y in zip(x_p, y_p):
        s1 += (y - phi(x)) ** 2
        s2 += phi(x) ** 2
        s3 += phi(x)
    s23 = (s2 - s3 ** 2 / n)
    if s23 == 0:
        print("Невозможно вычислить коэффициент детерминации, так как знаменатель равен 0")
        return None
    return 1 - s1 / s23


