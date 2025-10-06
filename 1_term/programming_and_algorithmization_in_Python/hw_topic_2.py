# Задание 1
# Дана переменная, в которой хранится слово из латинских букв. Напишите код, который выводит на экран:
#  среднюю букву, если число букв в слове нечётное;
#  две средних буквы, если число букв чётное.

# Пример работы программы:

# word = 'test'
# Результат: es
# word = 'testing'
# Результат: t

word = 'testings'
word_len = len(word)
if word_len % 2 == 0:
  print(word[word_len // 2 - 1] + word[word_len // 2])
else:
  print(word[word_len // 2])




# Задание 2 (не обязательное)
# Вы делаете MVP (минимально жизнеспособный продукт) dating-сервиса.
# У вас есть список юношей и девушек.
# Выдвигаем гипотезу: лучшие рекомендации получатся, если просто отсортировать имена по алфавиту и познакомить людей с одинаковыми индексами после сортировки. Но вы не будете никого знакомить, если кто-то может остаться без пары.

# Примеры работы программы:

# boys = ['Peter', 'Alex', 'John', 'Arthur', 'Richard']
# girls = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha']

# Результат
# Идеальные пары:
# Alex и Emma
# Arthur и Kate
# John и Kira
# Peter и Liza
# Richard и Trisha

# boys = ['Peter', 'Alex', 'John', 'Arthur', 'Richard', 'Michael']
# girls = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha']

# Результат: Внимание, кто-то может остаться без пары.

boys = ['Peter', 'Alex', 'John', 'Arthur', 'Richard']
girls = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha']

if len(boys) != len(girls):
  print('Внимание, кто-то может остаться без пары.')
else:
  boys.sort()
  girls.sort()

  print('Идеальные пары:')

  for index, value in enumerate(boys):
    print(value + ' и ' + girls[index])
