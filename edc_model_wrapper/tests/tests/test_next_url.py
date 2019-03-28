from django.test import TestCase, tag

from ...parsers import NextUrlParser, NextUrlError


class DummyObj:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestNextUrlParser(TestCase):
    def test_url_parser(self):
        obj1 = DummyObj(f1=1, f2=2)
        obj2 = DummyObj(f3=1, f4=2)
        parser = NextUrlParser(url_name="listboard_url", url_args=["f1", "f2"])
        self.assertEqual(parser.querystring(objects=[obj2, obj1]), "f1,f2&f1=1&f2=2")

    def test_url_parser_no_name_raises(self):
        self.assertRaises(NextUrlError, NextUrlParser)

    def test_url_parser_reverse(self):
        obj1 = DummyObj(f2=1, f3=2)
        parser = NextUrlParser(url_name="listboard_url", url_args=["f2", "f3"])
        parser.reverse(model_wrapper=obj1, remove_namespace=True)
