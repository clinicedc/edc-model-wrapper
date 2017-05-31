import uuid

from urllib import parse
from django.test import TestCase, tag

from ..next_url_parser import NextUrlParser, NextUrlError, Keywords


class DummyObj:
    def __init__(self, a=None, b=None, c=None, d=None, pk=None):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.id = pk


@tag('url')
class TestKeywords(TestCase):

    def test_url_parser(self):
        obj = DummyObj(a=1, b=2)
        keywords = Keywords(objects=[obj], attrs=['a', 'b'])
        self.assertEqual(
            parse.urlencode(keywords, encoding='utf-8'), 'a=1&b=2')

    def test_url_parser_included_keys1(self):
        obj = DummyObj(a=1, b=2)
        keywords = Keywords(
            objects=[obj], attrs=['a', 'b'], include_attrs=['a', 'b'])
        self.assertEqual(
            parse.urlencode(keywords, encoding='utf-8'), 'a=1&b=2')

    def test_url_parser_included_keys2(self):
        obj = DummyObj(a=1, b=2)
        keywords = Keywords(
            objects=[obj], attrs=['a', 'b'], include_attrs=['a'])
        self.assertEqual(
            parse.urlencode(keywords, encoding='utf-8'), 'a=1')

    def test_url_parser_included_keys3(self):
        pk = uuid.uuid4()
        obj = DummyObj(a=1, b=None, pk=pk)
        keywords = Keywords(
            objects=[obj], attrs=['a', 'b', 'id'], include_attrs=['a', 'b', 'id'])
        self.assertEqual(
            parse.urlencode(keywords, encoding='utf-8'), f'a=1&b=&id={pk}')


@tag('url')
class TestNextUrlParser(TestCase):

    def test_url_parser(self):
        obj1 = DummyObj(a=1, b=2)
        obj2 = DummyObj(c=1, d=2)
        parser = NextUrlParser(url_name='example', url_args=['a', 'b'])
        self.assertEqual(parser.querystring(
            objects=[obj2, obj1]), 'next=example,a,b&a=1&b=2')

    def test_url_parser_no_name_raises(self):
        self.assertRaises(NextUrlError, NextUrlParser)
