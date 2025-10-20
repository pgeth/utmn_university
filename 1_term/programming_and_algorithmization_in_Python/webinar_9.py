# 1. Целочисленное деление начинаем с умножения price * 3 //100
price = 99
print(price // 100 * 3) #res: 0, 

# ----------------------------------------------
# Задачи сравнения
# 2. Тернарный условный оператор
percent = 3 if price >= 10_000 else 1

# ----------------------------------------------
# 3. Вывод всех чисел, которые есть в обоих списках
list1 = [1, 2, 3, 4, 5]
list2 = [3, 4, 5, 6, 7]

set2 = set(list2)
for num in list1:
  if num in set2:
    print(num)

# ----------------------------------------------
# 4. Все строки, которые есть ТОЛЬКО в одном из списоков
list3 = ['apple', 'banana', 'orange']
list4 = ['banana', 'grape', 'pear']
for num in set(list3) ^ set(list4):
  print(num)

# ----------------------------------------------
# 5. Вывести все ключи, которые есть в ОБОИХ СЛОВОРЯХ 
# Множества построенны поверх словарей, словари - быстрые
dict1 = {'a': 1, 'b': 2, 'c': 3}
dict2 = {'b': 4, 'c': 5, 'd': 6}

for key in dict1.keys() & dict2.keys():
  print(key)

# ----------------------------------------------
# 6. Два кортежа. Вывести все кортежи, сумма чисел которых равна 10
list5 = [(1, 9), (2, 8), (3, 7), (4, 6), (5, 5)]
for tup in list5:
  if sum(tup) == 10:
    print(tup)

# ----------------------------------------------
# Задачи поиска.
# 7. В списке чисел найти индекс первого вхождения заданного числа в список
list6 = [1, 2, 3, 4, 5, 6]
num = 3
print(list6.index(num))

# ----------------------------------------------
# 8. В списке строк найти все строки, содержащие заданную подстроку
list7 = ['apple', 'banana', 'orange', 'grape']
substr1 = 'an'
for string in list7:
  if substr1 in string:
    print(string)

# ----------------------------------------------
# 9. В строке найти все индексы задданого символа
string1 = 'hello world'
char1 = 'l'
for i, c in enumerate(string1):
  if c == char1:
    print(i)

# ----------------------------------------------
# 10. В списке найти все пары чисел, сумма которых равна заданному числу
list8 = [1, 2, 3, 4, 5, 6]
num1 = 6
for i in range(len(list8)):
  for j in range(i + 1, len(list8)):
    if list8[i] + list8[j] == num1:
      print(list8[i], list8[j])

# ----------------------------------------------
# 11. В списке строк найти все строки, начинающиеся с заданной подстроки
list9 = ['apple', 'banana', 'orange', 'grape']
substr2 = 'a'

for item in list9:
  if item.startswith(substr2):
    print(item)

# ----------------------------------------------
# ЗАДАЧИ НА СИНХРОНИЗАЦИЮ РАЗНЫХ ИСТОЧНИКОВ

# 12. В списках чисел удалите все дубликаты чисел и объедините испсиикх в один
list10 = [1, 2, 3, 4, 5]
list11 = [3, 4, 5, 6, 7]
list(set(list10 + list11))

# ----------------------------------------------
# 13. Два словаря объединить в один, при этом если ключи повторяются суммировать их значения
dict3 = {'a': 1, 'b': 2, 'c': 3}
dict4 = {'b': 4, 'c': 5, 'd': 6}
dict5 = {}

for key in dict3.keys() | dict4.keys():
  dict5[key] = dict3.get(key, 0) + dict4.get(key, 0)

print(dict5)

# ----------------------------------------------
# СВЯЗАННЫЕ СПИСКИ
# 14. Вывод, добавление в начало и конец
#my_list = ["Zero", ["First", ["Second", ["Third", ["Fourth", None]]]]]
my_list = None
my_list_end = None


while True: 
  user_input = input("Введи '< word' или '> word': ")
  cmd, word = user_input.split(" ") #['<', 'word']
  if my_list is None:
    my_list = [word, None]
    my_list_end = my_list
  else:
    if cmd == "<":
      #my_list.insert(0, word)
      my_list = [word, my_list]
    elif cmd == ">":
      #my_list.append(word)
      # node = my_list
      # while node[1] is not None:
      #   node = node[1]
      # node[1] = [word, None]
      my_list_end[1] = [word, None]
      my_list_end = my_list_end[1]
    else:
       print('Нет такой команды')
       continue
    
  print("[", end="")
  node = my_list
  while node is not None: 
    print(node[0], end=", " if node[1] is not None else "")
    node = node[1]
  print("]")
