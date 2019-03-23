import uuid

from django.test import TestCase, tag
from urllib import parse

from ...parsers import Keywords
from ..models import ParentExample, Example, SuperParentExample


class DummyObj:
    def __init__(self, a=None, b=None, c=None, d=None, pk=None):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.id = pk


class TestKeywords(TestCase):
    def test_url_parser(self):
        obj = DummyObj(a=1, b=2)
        keywords = Keywords(objects=[obj], attrs=["a", "b"])
        self.assertEqual(parse.urlencode(keywords, encoding="utf-8"), "a=1&b=2")

    def test_url_parser_included_keys1(self):
        obj = DummyObj(a=1, b=2)
        keywords = Keywords(objects=[obj], attrs=["a", "b"], include_attrs=["a", "b"])
        self.assertEqual(parse.urlencode(keywords, encoding="utf-8"), "a=1&b=2")

    def test_url_parser_included_keys2(self):
        obj = DummyObj(a=1, b=2)
        keywords = Keywords(objects=[obj], attrs=["a", "b"], include_attrs=["a"])
        self.assertEqual(parse.urlencode(keywords, encoding="utf-8"), "a=1")

    def test_url_parser_included_keys3(self):
        pk = uuid.uuid4()
        obj = DummyObj(a=1, b=None, pk=pk)
        keywords = Keywords(
            objects=[obj], attrs=["a", "b", "id"], include_attrs=["a", "b", "id"]
        )
        self.assertEqual(parse.urlencode(keywords, encoding="utf-8"), f"a=1&b=&id={pk}")

    def test_url_parser_included_keys_url_kwargs(self):
        pk = uuid.uuid4()
        obj = DummyObj(a=1, b=None, pk=pk)
        keywords = Keywords(
            objects=[obj], attrs=["a", "b", "id"], include_attrs=["a", "b", "id"], a=100
        )
        self.assertEqual(
            parse.urlencode(keywords, encoding="utf-8"), f"a=100&b=&id={pk}"
        )

    def test_url_parser_model(self):
        example = Example.objects.create()
        obj = ParentExample.objects.create(example=example)
        keywords = Keywords(objects=[obj], attrs=["example"])
        self.assertEqual(
            parse.urlencode(keywords, encoding="utf-8"), f"example={str(example.pk)}"
        )

    def test_url_parser_model2(self):
        parent_example = ParentExample.objects.create()
        obj = SuperParentExample.objects.create(parent_example=parent_example)
        keywords = Keywords(objects=[obj], attrs=["parent_example"])
        self.assertEqual(
            parse.urlencode(keywords, encoding="utf-8"),
            f"parent_example={str(parent_example.pk)}",
        )
