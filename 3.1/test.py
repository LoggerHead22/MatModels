import unittest
from parser_c import *


class TestUtilities(unittest.TestCase):
    def test_flatten(self):
        self.assertEqual(flatten([1, 2, 3]), [1, 2, 3])
        self.assertEqual(flatten([1, [2, 3, 4], 5]), [1, 2, 3, 4, 5])
        self.assertEqual(flatten([1, [2, [3, 4, 5], 6], 7]), [1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(flatten([[1, 2], [[[3, 4, 5]]], 6, 7]), [1, 2, 3, 4, 5, 6, 7])

    def test_filtered(self):
        self.assertEqual(filtered([1, 2, 3]), [1, 2, 3])
        self.assertEqual(filtered([1, 2, None, 3]), [1, 2, 3])
        self.assertEqual(filtered([0, 1, False, 2, None, 3, '']), [0, 1, False, 2, 3, ''])

    def test_decayed(self):
        self.assertEqual(decayed([1]), 1)
        self.assertEqual(decayed(1), 1)

    def test_composed(self):
        self.assertEqual(composed(flatten)([1, [2], 3]), [1, 2, 3])
        self.assertEqual(composed(filtered, flatten)([1, [2, None], 3]), [1, 2, 3])
        self.assertEqual(composed(list, reversed, filtered, flatten)([1, [2, None], 3]), [3, 2, 1])

class TestParser(unittest.TestCase):
    def test_char_parser(self):
        self.assertEqual(char_.parse('foobarbaz'), ['f', 'oobarbaz'])
        self.assertEqual(char_.parse(''), [])
        self.assertEqual(char_('f').parse('foobarbaz'), ['f', 'oobarbaz'])
        self.assertEqual(char_('e').parse('foobarbaz'), [])

    def test_str_parser(self):
        self.assertEqual(str_('foo').parse('foobarbaz'), ['foo', 'barbaz'])
        self.assertEqual(str_('egg').parse('foobarbaz'), [])

    def test_int_parser(self):
        self.assertEqual(int_.parse('432'), [432, ''])
        self.assertEqual(int_.parse('+432'), [432, ''])
        self.assertEqual(int_.parse('-432'), [-432, ''])
        self.assertEqual(int_.parse('432foobarbaz'), [432, 'foobarbaz'])
        self.assertEqual(int_(432).parse('432foobarbaz'), [432, 'foobarbaz'])
        self.assertEqual(int_(76).parse('432foobarbaz'), [])

    def test_pass_parser(self):
        self.assertEqual(pass_(int_).parse('432'), [None, ''])
        self.assertEqual(pass_(int_).parse('432foobarbaz'), [None, 'foobarbaz'])
        self.assertEqual(pass_(int_).parse('foobarbaz'), [])

    def test_sequence_parser(self):
        self.assertEqual((int_ & int_).parse('432-76'), [[432, -76], ''])
        self.assertEqual((int_ & int_).parse('432-76foobarbaz'), [[432, -76], 'foobarbaz'])
        self.assertEqual((int_ & int_).parse('foo432barbaz'), [])
        self.assertEqual((int_ & int_).parse('432foobarbaz'), [])
        self.assertEqual((int_ & int_).parse('foobarbaz'), [])

    def test_zero_or_more_parser(self):
        self.assertEqual((~int_).parse('432'), [[432], ''])
        self.assertEqual((~int_).parse('432-76'), [[432, -76], ''])
        self.assertEqual((~int_).parse('432-76foobarbaz'), [[432, -76], 'foobarbaz'])
        self.assertEqual((~str_('bar')).parse('barbarbaz'), [['bar', 'bar'], 'baz'])
        self.assertEqual((~str_('egg')).parse('foobarbaz'), [[], 'foobarbaz'])

    def test_alternative_parser(self):
        self.assertEqual((int_ | str_('foo')).parse('432'), [432, ''])
        self.assertEqual((int_ | str_('foo')).parse('foo'), ['foo', ''])
        self.assertEqual((int_ | str_('foo')).parse('432foobarbaz'), [432, 'foobarbaz'])
        self.assertEqual((int_ | str_('egg')).parse('foobarbaz'), [])
        self.assertEqual((int_(432) | str_('432')).parse('432foobarbaz'), [432, 'foobarbaz'])
        self.assertEqual((str_('432') | int_(432)).parse('432foobarbaz'), ['432', 'foobarbaz'])

    def test_look_ahead_parser(self):
        self.assertEqual((int_ > str_('!')).parse('432!'), [432, '!'])
        self.assertEqual((int_ > str_('!')).parse('432'), [])
        self.assertEqual((int_ > str_('!')).parse('432foobarbaz!'), [])

    def test_negative_look_ahead_parser(self):
        self.assertEqual((int_ >> str_('!')).parse('432!'), [])
        self.assertEqual((int_ >> str_('!')).parse('432'), [432, ''])
        self.assertEqual((int_ >> str_('!')).parse('432foobarbaz!'), [432, 'foobarbaz!'])

    def test_mapped_parser(self):
        self.assertEqual((int_ & int_ & int_).parse('432-76-11'), [[[432, -76], -11], ''])
        self.assertEqual((int_ & int_ & int_).map(flatten).parse('432-76-11'), [[432, -76, -11], ''])

    def test_optional_parser(self):
        self.assertEqual((-int_).parse('432'), [432, ''])
        self.assertEqual((-int_).parse('foobarbaz'), [None, 'foobarbaz'])

if __name__ == '__main__':
    unittest.main()