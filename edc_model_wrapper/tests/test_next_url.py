from django.test import TestCase, tag

from ..parsers import NextUrlParser, NextUrlError
from .test_keywords import DummyObj


class TestNextUrlParser(TestCase):

    def test_url_parser(self):
        obj1 = DummyObj(a=1, b=2)
        obj2 = DummyObj(c=1, d=2)
        parser = NextUrlParser(url_name='example', url_args=['a', 'b'])
        self.assertEqual(parser.querystring(
            objects=[obj2, obj1]), 'example,a,b&a=1&b=2')

    def test_url_parser_no_name_raises(self):
        self.assertRaises(NextUrlError, NextUrlParser)
