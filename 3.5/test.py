from transpiler import *

if __name__ != '__main__':
    exit(1)

src = \
'''1 > модуля(5)'''
expected = \
'''1 > abs(5)'''
actual = transpile(src)
assert actual == expected
print("Test Passed!")
src = \
'''для числа в диапазоне(5):
    пропустить'''
expected = \
'''for number in range(5):
    pass'''
actual = transpile(src)
assert actual == expected
print("Test Passed!")
src = \
'''список_людей = [1, 2, 3]
для человека в списке_людей:
    вывести(человек.имя)'''
expected = \
'''list_of_people = [1, 2, 3]
for human in list_of_people:
    print(human.name)'''
actual = transpile(src)
assert actual == expected
print("Test Passed!")
src = \
'''список_людей = [1, 2, 3]
для человека в списке_людей:
    вывести(имя@человека)'''
expected = \
'''list_of_people = [1, 2, 3]
for human in list_of_people:
    print(human.name)'''
actual = transpile(src)
assert actual == expected
print("Test Passed!")
src = \
'''для индекса, числа в перечислении([1, 4, 9, 16]):
    вывести(индекс, число)'''
expected = \
'''for (index, number) in enumerate([1, 4, 9, 16]):
    print(index, number)'''
actual = transpile(src)
assert actual == expected
print("Test Passed!")
src = \
'''сумма(числа + индекса ** 2 для индекса, числа в перечислении([1, 8, 27, 64]))'''
expected = \
'''sum((number + index ** 2 for (index, number) in enumerate([1, 8, 27, 64])))'''
actual = transpile(src)
assert actual == expected
print("Test Passed!")
src = \
'''определить функцию(число_1, число_2):
    вернуть число_1 > числа_2'''
expected = \
'''def function(number_1, number_2):
    return number_1 > number_2'''
actual = transpile(src)
assert actual == expected
print("Test Passed!")
src = \
'''определить расщепить(строчка, разделитель=" "):
    разделённые_слова = []
    последний_индекс = 0
    для индекса, символа в перечислении(строчки):
        если символ == разделителю:
            привесить@разделённым_словам(строчку[последний_индекс:индекс])
            последний_индекс = индексу + 1
        иначе_если индекс + 1 == длине(строчки):
            привесить@разделённым_словам(строчку[последний_индекс:индекс + 1])
    вернуть разделённые_слова'''
expected = \
'''def split(line, delimiter=' '):
    divided_words = []
    last_index = 0
    for (index, symbol) in enumerate(line):
        if symbol == delimiter:
            divided_words.append(line[last_index:index])
            last_index = index + 1
        elif index + 1 == len(line):
            divided_words.append(line[last_index:index + 1])
    return divided_words'''
actual = transpile(src)
assert actual == expected
print("Test Passed!")
src = \
'''
из коллекций импортировать словарь_по_умолчанию

определить анаграмму(первая, вторая):
    первая = первой.в_нижнем_регистре().порезать()
    вторая = второй.в_нижнем_регистре().порезать()
    если длина(первой) != длине(второй):
        вернуть Ложь
    подсчёт = словарь_по_умолчанию(целое)
    для индекса в диапазоне(длины(первой)):
        подсчёт[первой[индекса]] += 1
        подсчёт[второй[индекса]] -= 1
    для числа в значениях@подсчёта():
        если число != 0:
            вернуть Ложь
    вернуть Истину'''
expected = \
'''from collections import defaultdict

def anagram(first, second):
    first = first.lower().strip()
    second = second.lower().strip()
    if len(first) != len(second):
        return False
    count = defaultdict(int)
    for index in range(len(first)):
        count[first[index]] += 1
        count[second[index]] -= 1
    for number in count.values():
        if number != 0:
            return False
    return True'''
actual = transpile(src)
assert actual == expected
print("Test Passed!")
src = \
'''определить детерминант(матрицы):
    если длина(матрицы) == 1:
        вернуть матрицу[0][0]
    вернуть сумму(числа * детерминант(минора(матрицы, 0, числа)) * (-1) ** числа для индекса, числа в перечислении(матрицы[0]))'''
expected = \
'''def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    return sum((number * determinant(minor(matrix, 0, number)) * (-1) ** number for (index, number) in enumerate(matrix[0])))'''
actual = transpile(src)
assert actual == expected
print("Test Passed!")
src = \
'''определить присоединить(разделитель, части):
    результат = ""
    для части в частях:
        если не это_экземпляр(часть, строки):
            вызвать Исключение()
        результат += часть + разделитель
    вернуть порезанный@результат(разделителем)'''
expected = \
'''def join(delimiter, part):
    result = ''
    for part in parts:
        if not isinstance(part, str):
            raise Exception()
        result += part + delimiter
    return result.strip(delimiter)'''
actual = transpile(src)
assert actual == expected
print("Test Passed!")
src = \
'''определить сравнить(а, б):
    если размер@а == размеру@б:
        вернуть ширину@а * высоту@б'''
expected = \
'''def compare(a, b):
    if a.size == b.size:
        return a.width * b.height'''
actual = transpile(src)
assert actual == expected
print("Test Passed!")
src = \
'''класс КомплексноеЧисло:
    определить __инициализацию__(меня):
        моя.ширина = 0
        моя.высота = 0'''
expected = \
'''class Complex_number:

    def __init__(me):
        my.width = 0
        my.height = 0'''
actual = transpile(src)
assert actual == expected
print("Test Passed!")
src = \
'''класс Человека:
    определить __инициализацию__(человека, именем):
        имя@человека = имя

васян = Человек('Васян')
стасян = Человек('Стасян')

список_людей = [васян, стасян]
для человека в списке_людей:
    вывести(имя@человека)'''
expected = \
'''class Human:

    def __init__(human, name):
        human.name = name
vasyan = Human('Васян')
stasyan = Human('Стасян')
list_of_people = [vasyan, stasyan]
for human in list_of_people:
    print(human.name)'''
actual = transpile(src)
assert actual == expected
print("Test Passed!")
src = \
'''для числа в диапазоне(5):
    вывести([1, 2, 3][числа])'''
actual = transpile(src)
expected = \
'''for number in range(5):
    print([1, 2, 3][number])'''
assert actual == expected
print("Test Passed!")
src = \
r'''класс Матрицы:
    определить __инициализацию__(матрицы, высотой, шириной):
        высота@матрицы = высоте
        ширина@матрицы = ширине
        числа@матрицы = [[0] * ширину для _ в диапазоне(высоты)]

    определить задать(матрицу, списком_значений):
        числа@матрицы = списку_значений

    определить __представление__(матрицы):
        результат = ''
        для индекса_1 в диапазоне(высоты@матрицы):
            если индекс_1:
                результат += '\n'
            результат += '['
            для индекса_2 в диапазоне(ширины@матрицы):
                если индекс_2:
                    результат += ', '
                результат += строку(числа@матрицы[индекс_1][индекс_2])
            результат += ']'
        вернуть результат

матрица = Матрице(3, 4)
задать@матрицу([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
вывести(матрицу)'''
expected = \
r'''class Matrix:

    def __init__(matrix, height, width):
        matrix.height = height
        matrix.width = width
        matrix.number = [[0] * width for _ in range(height)]

    def ask(matrix, list_values):
        matrix.number = list_values

    def __repr__(matrix):
        result = ''
        for index_1 in range(matrix.height):
            if index_1:
                result += '\n'
            result += '['
            for index_2 in range(matrix.width):
                if index_2:
                    result += ', '
                result += str(matrix.number[index_1][index_2])
            result += ']'
        return result
matrix = Matrix(3, 4)
matrix.ask([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
print(matrix)'''
actual = transpile(src)
assert actual == expected
print("Test Passed!")
print("------------------")
print("ALL TEST PASSED!")