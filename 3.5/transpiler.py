import ast
import functools
import json
import keyword
import pathlib
import pymorphy2
import re
import requests
import urllib.parse

morph = pymorphy2.MorphAnalyzer()

keywords = {
    'Ложь': 'False', 'Ничего': 'None', 'Истина': 'True', 'и': 'and', 'как': 'as', 'утверждать': 'assert', 'асинхронный': 'async', 'в_ожидании': 'await', 'прервать': 'break', 'класс': 'class', 'продолжить': 'continue', 'определить': 'def', 'удалить': 'del', 'иначе_если': 'elif', 'иначе': 'else', 'ожидать': 'except', 'наконец': 'finally', 'для': 'for', 'из': 'from', 'глобальный': 'global', 'если': 'if', 'импортировать': 'import', 'в': 'in', 'является': 'is', 'лямбда': 'lambda', 'нелокальный': 'nonlocal', 'не': 'not', 'или': 'or', 'пропустить': 'pass', 'вызвать': 'raise', 'вернуть': 'return', 'попытаться': 'try', 'пока': 'while', 'с': 'with', 'произвести': 'yield',
}

buildins = {
    'модуль': 'abs', 'все': 'all', 'любой': 'any', '_2сс': 'bin', 'булево': 'bool', 'массив_байтов': 'bytearray', 'байты': 'bytes', 'вызываемый': 'callable', 'знаковый_код': 'chr', 'скомпилировать': 'compile', 'комплексное': 'complex', 'словарь': 'dict', 'список_атрибутов': 'dir', 'перечисление': 'enumerate', 'выполнить': 'eval', 'исполнить': 'exec', 'фильтровать': 'filter', 'плавающее': 'float', 'форматировать': 'format', 'хэш': 'hash', 'помощь': 'help', '_16сс': 'hex', 'идентификатор': 'id', 'ввести': 'input', 'целое': 'int', 'это_экземпляр': 'isinstance', 'это_подкласс': 'issubclass', 'список': 'list', 'отобразить': 'map', 'максимум': 'max', 'минимум': 'min', 'следующий': 'next', '_8сс': 'oct', 'открыть': 'open', 'числовой_код': 'ord', 'степень': 'pow', 'вывести': 'print', 'представление': 'repr', 'перевернутый': 'reversed', 'округлить': 'round', 'множество': 'set', 'ломтик': 'slice', 'отсортированный': 'sorted', 'строка': 'str', 'сумма': 'sum', 'родитель': 'super', 'кортеж': 'tuple', 'тип': 'type', 'переменные': 'vars', 'объединить': 'zip',

    'привесить': 'append', 'длина': 'len', 'в_нижнем_регистр': 'lower', 'порезать': 'strip', 'порезанный': 'strip', 'коллекции': 'collections', 'словарь_по_умолчание': 'defaultdict', 'значения': 'values'
}

magicks = {
    '__инициализация__': '__init__',
    '__представление__': '__repr__',
    '__сложение__': '__add__',
}

neutral = {
    'INFN': 'INFN',
    'NOUN': 'nomn',
    'PRTF': 'nomn',
    'VERB': 'INFN',
}

neutral_sing = {
    'NOUN': 'nomn,sing',
    'ADJF': 'nomn,sing',
}

def translate(s):
    def impl(s):
        if re.match(r'\d+', s):
            return s
        url = f'http://translate.google.com/m?tl=en&sl=ru&q={urllib.parse.quote(s)}'
        response = requests.get(url)
        data = response.text
        result = re.findall(r'(?s)class="(?:t0|result-container)">(.*?)<', data)[0]
        if result.lower().startswith('the '):
            result = result[4:]
        if result.lower().startswith('a '):
            result = result[2:]
        if result.lower().startswith('an '):
            result = result[3:]
        return result.lower()

    path = pathlib.Path('.cache')
    path.touch(exist_ok=True)
    if path.stat().st_size == 0:
        path.open('w').write('{}')
    data = json.load(path.open())
    if s not in data:
        data[s] = impl(s)
    json.dump(data, path.open('w'), ensure_ascii=False)
    return data[s]

def walk(d, tail=[]):
    for k, v in d.items():
        if isinstance(v, dict):
            yield from walk(v, tail + [k])
        else:
            yield [v, tail + [k]]

def inflect(s, constraints):
    parsed = morph.parse(s)
    for it in parsed:
        for c in walk(constraints):
            if set(c[1]) in it.tag:
                return it.inflect(set(c[0].split(','))).word
    return parsed[0].word

@functools.singledispatch
def tr(obj, constraints):
    return tr_impl(str(obj), constraints)

@tr.register(str)
def _(s, constraints):
    return tr_impl(s, constraints)

@tr.register(ast.arg)
def _(node, constraints):
    node.arg = tr(node.arg, constraints)
    return node

@tr.register(ast.Call)
def _(node, constraints):
    tr(node.func, constraints)
    for it in node.args:
        tr(it, constraints)
    return node

@tr.register(ast.Attribute)
def _(node, constraints):
    tr(node.value, constraints)
    node.attr = tr(node.attr, constraints)
    return node

@tr.register(ast.BinOp)
def _(node, constraints):
    tr(node.left, constraints)
    tr(node.right, constraints)
    return node

@tr.register(ast.Constant)
def _(node, constraints):
    return node

@tr.register(ast.comprehension)
def _(node, constraints):
    tr(node.target, constraints)
    tr(node.iter, constraints)
    return node

@tr.register(ast.GeneratorExp)
def _(node, constraints):
    tr(node.elt, constraints)
    for it in node.generators:
        tr(it, constraints)
    return node

@tr.register(ast.Name)
def _(node, constraints):
    node.id = tr(node.id, constraints)
    return node

@tr.register(ast.List)
def _(node, constraints):
    for it in node.elts:
        tr(it, constraints)
    return node

@tr.register(ast.Subscript)
def _(node, constraints):
    tr(node.value, constraints)
    if hasattr(node.slice, 'lower'):
        tr(node.slice.lower, constraints)
        tr(node.slice.upper, constraints)
    else:
        tr(node.slice, constraints)
    return node

@tr.register(ast.Tuple)
def _(node, constraints):
    for it in node.elts:
        tr(it, constraints)
    return node

@tr.register(ast.UnaryOp)
def _(node, constraints):
    tr(node.operand, constraints)
    return node

def get_capitalization(from_, to):
    if from_[0].isupper():
        return to.capitalize()
    return to

def tr_impl(s, constraints):
    if re.match('^_+$', s):
        return s
    if s.startswith('__') and s.endswith('__'):
        return '__' + get_capitalization(s[2:-2], translate(inflect(s[2:-2], constraints))) + '__'
    s = s.split('_')
    s[0] = get_capitalization(s[0], translate(inflect(s[0], constraints)))
    s[1:] = [get_capitalization(it, translate(inflect(it, {}))) for it in s[1:]]
    return '_'.join(s).replace(' ', '_')

def preprocess(lines):
    for line in lines:
        yield re.sub(r'\b(\w+)?@(\w+?)\b', r'\2.\1', line)

def transpile_lexems(lines):
    def impl(s):
        s = s.group()
        if s in keywords:
            return keywords[s]
        if (m := '__' + inflect(s[2:-2], neutral) + '__') in magicks:
            return magicks[m]
        if (b := inflect(s, neutral)) in buildins:
            return buildins[b]
        return s

    for line in lines:
        yield re.sub(r'\b\w+\b', impl, line)

class Transformer(ast.NodeTransformer):
    def visit_Attribute(self, node):
        tr(node, neutral)
        return node

    def visit_Call(self, node):
        tr(node, neutral)
        return node

    def visit_For(self, node):
        tr(node.target, {'NOUN': 'nomn,sing'})
        tr(node.iter, neutral)
        for it in node.body:
            self.visit(it)
        return node

    def visit_FunctionDef(self, node):
        node.name = tr(node.name, {'nomn': 'nomn', 'accs': 'nomn'})
        for it in node.args.args:
            tr(it, neutral_sing)
        for it in node.body:
            self.visit(it)
        return node

    def visit_ClassDef(self, node):
        node.name = tr(node.name, neutral_sing)
        for it in node.body:
            self.visit(it)
        return node

    def visit_Name(self, node):
        tr(node, {'NOUN': 'nomn'})
        return node

def transpile(src):
    result = src.splitlines()
    result = preprocess(result)
    result = transpile_lexems(result)
    result = '\n'.join(result)
    result = ast.parse(result)
    result = Transformer().visit(result)
    # print(ast.dump(result, indent=2))
    return ast.unparse(result)