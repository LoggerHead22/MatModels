import functools
import re


class Parser:
    def parse(self, s):
        raise NotImplementedError()

    def map(self, f):
        return MappedParser(self, f)

    def __and__(self, other):
        return SequenceParser(self, other)

    def __invert__(self):
        return ZeroOrMoreParser(self)

    def __or__(self, other):
        return AlternativeParser(self, other)

    def __gt__(self, other):
        return LookAheadParser(self, other)

    def __rshift__(self, other):
        return NegativeLookAheadParser(self, other)

    def __neg__(self):
        return OptionalParser(self)

def flatten(l):
    result = []
    for it in l:
        if isinstance(it, list):
            result.extend(flatten(it))
        else:
            result.append(it)
    return result

def filtered(l):
    return [it for it in l if it is not None]

def decayed(l):
    if isinstance(l, list):
        return l[0]
    return l

def composed(*fs):
    def impl(g, f):
        return lambda *args, **kwargs: g(f(*args, **kwargs))
    return functools.reduce(impl, fs)

class CharParser(Parser):
    def __init__(self, supply = None):
        self.supply = supply

    def __call__(self, supply):
        return CharParser(supply)

    def parse(self, s):
        if s:
            if not self.supply or s[0] == self.supply:
                return [s[0], s[1:]]
        return []

class StrParser(Parser):
    def __init__(self, supply):
        self.supply = supply

    def __call__(self, supply):
        return StrParser(supply)

    def parse(self, s):
        if s.startswith(self.supply):
            return [self.supply, s[len(self.supply):]]
        return []

class IntParser(Parser):
    def __init__(self, supply = None):
        self.supply = supply

    def __call__(self, supply):
        return IntParser(supply)

    def parse(self, s):
        if m := re.match(r'[+-]?\d+', s):
            if not self.supply or int(m.group(0)) == self.supply:
                return [int(m.group(0)), s[len(m.group(0)):]]
        return []

class PassParser(Parser):
    def __init__(self, underlying):
        self.underlying = underlying

    def __call__(self, underlying):
        return PassParser(underlying)

    def parse(self, s):
        if u := self.underlying.parse(s):
            return [None, u[1]]
        return []

class SequenceParser(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def parse(self, s):
        if l := self.left.parse(s):
            if r := self.right.parse(l[1]):
                return [[l[0], r[0]], r[1]]
        return []

class ZeroOrMoreParser(Parser):
    def __init__(self, underlying):
        self.underlying = underlying

    def parse(self, s):
        result = []
        tail = s
        while u := self.underlying.parse(tail):
            result.append(u[0])
            tail = u[1]
        if result:
            return [result, tail]
        return [[], s]

class AlternativeParser(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def parse(self, s):
        if l := self.left.parse(s):
            return l
        if r := self.right.parse(s):
            return r
        return []

class LookAheadParser(Parser):
    def __init__(self, underlying, look_ahead):
        self.underlying = underlying
        self.look_ahead = look_ahead

    def parse(self, s):
        if u := self.underlying.parse(s):
            if self.look_ahead.parse(u[1]):
                return u
        return []

class NegativeLookAheadParser(Parser):
    def __init__(self, underlying, look_ahead):
        self.underlying = underlying
        self.look_ahead = look_ahead

    def parse(self, s):
        if u := self.underlying.parse(s):
            if self.look_ahead.parse(u[1]) == []:
                return u
        return []

class MappedParser(Parser):
    def __init__(self, underlying, f):
        self.underlying = underlying
        self.f = f

    def parse(self, s):
        if u := self.underlying.parse(s):
            return [self.f(u[0]), u[1]]
        return []

class OptionalParser(Parser):
    def __init__(self, underlying):
        self.underlying = underlying

    def parse(self, s):
        if u := self.underlying.parse(s):
            return u
        return [None, s]

char_ =  CharParser()
str_ =   lambda x: StrParser(x)
int_ =   IntParser()
pass_ =  lambda x: PassParser(x)

