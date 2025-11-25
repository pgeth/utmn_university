#------------------------------------------
# 1. Вывод матрицы, транспанирование квадратной матрицы
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

def print_matrix(matrix):
  for row in matrix:
    for item in row:
      print(item, end=" ")
    print()

def transpose_matrix(matrix):
  for i in range(0, len(matrix)):
    for j in range(0 + 1, len(matrix)):
      matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

transpose_matrix(matrix)
print_matrix(matrix)

#------------------------------------------
# 2. lambda-функции. map.
# Чистая функция - ведет себя одинаково при одних и тех же входных данных
def my_apply(a, b, func):
  print(func(a, b))
my_apply(1, 2, lambda x, y: x + y)

#------------------------------------------
# 3. Аргументы args и kwargs
def api_request(*params):
    """
    Документация функции api_request
    Аргументы:
    *params - список параметров (картеж)
    """
    print(params) #список параметров (картеж)

def api_request2(**params):
  print(params) #словарь

api_request(1, 2)
api_request2(a=1, b=2, c=3)

#------------------------------------------
# 4. Рекурсия. mult(a ,b) = mult(a, b-1) + a
# Простое определение: Такая функция, которая внутри себя вызывает саму себя.
def mult(a, b):
    if b == 1: #базовый случай всегда есть в рекурсии
        return a
    first = mult(a, b-1)
    result = first + a
    return result

print(mult(2, 3))

#------------------------------------------
# 5. Рекурсия. Собака, кактус и человек.
# Собака может бежать только влево и вверх. * - кактусы, Ч - человек, С - собака
field = [
    ['Ч', '-', '-', '*'],
    ['*', '*', '-', '-'],
    ['-', '-', 'С', '-'],
    ['-', '-', '-', '-'],
]

def can_reach(field, row, col):
    if field[row][col] == 'Ч':
        return True
    can_go_left = col > 0 and field[row][col-1] != '*'
    if can_go_left and can_reach(field, row, col-1):
        return True
    can_go_up = row > 0 and field[row-1][col] != '*'
    if can_go_up and can_reach(field, row-1, col):
        return True
    return False

#------------------------------------------
# 6.Рекурсия и динамическое программирование. Собака, кактус и человек
# Простое определение: Динамическое программирование - это запоминание результатов вычислений и использование их для ускорения рекурсии.
field2 = [
    ['Ч', '-', '-', '-', '*', '-'],
    ['*', '*', '*', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-'],
    ['-', '*', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', 'С', '-'],
]

def can_reach2(field, row, col):
    memory = []
    for line in field:
        memory.append([None] * len(line))

    def helper(field, row, col):
        if memory[row][col] is not None:
            return memory[row][col]
        if field[row][col] == 'Ч':
            memory[row][col] = True
            return True
        can_go_left = col > 0 and field[row][col-1] != '*'
        if can_go_left and helper(field, row, col-1):
            memory[row][col] = True
            field[row][col] = '+'
            return True
        can_go_up = row > 0 and field[row-1][col] != '*'
        if can_go_up and helper(field, row-1, col):
            memory[row][col] = True
            field[row][col] = '+'
            return True
        memory[row][col] = False
        return False
    return helper(field, row, col)

print(can_reach2(field2, 6, 4))
for row in field2:
    for cell in row:
        print(cell, end=" ")
    print()

#------------------------------------------
# 7. Рекурсия. Список полетов. Обход в глубину и поиск кратчайшего пути.
# Будем использовать обход в ширину. (max_flights)
flights = {
    'Paris': {'London', 'Rome', 'Madrid'},
    'London': {'LA'},
    'Rome': {'Paris', 'Istanbul'},
    'Istanbul': {'Moscow', 'SPb'},
}

def can_fly(city_from, city_to, flights, max_flights=None):
    visited = set()
    def helper(city_from, city_to, flights, max_flights):
        visited.add(city_from)
        if max_flights == 0:
            return False
        next_max_flights = max_flights-1 if max_flights is not None else None
        if city_from not in flights:
            return False
        if city_to in flights[city_from]:
            return True
        for near_city in flights[city_from]:
            if near_city not in visited and helper(near_city, city_to, flights, next_max_flights):
                return True
        return False
    return helper(city_from, city_to, flights, max_flights)


print(can_fly('Paris', 'Moscow', flights, 3)) # True
print(can_fly('Paris', 'Moscow', flights, 2)) # False
print(can_fly('London', 'Moscow', flights)) # False

#Алгоритм Дейкстры — более мощный для поиска кратчайшего пути в графе.
