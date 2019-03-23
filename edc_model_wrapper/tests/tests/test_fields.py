from django.test import TestCase, tag

from ...wrappers import Fields, ModelWrapper
from ..models import Example, ParentExample


class TestFields(TestCase):
    def test_fields(self):
        model_obj = Example()
        self.assertEqual(Fields(model_obj=model_obj).model_obj, model_obj)

    def test_fields_repr(self):
        model_obj = Example()
        self.assertTrue(repr(Fields(model_obj=model_obj)))

    def test_fields_skips_example(self):
        class Wrapper:
            pass

        wrapper = Wrapper()
        fields = Fields(model_obj=ParentExample())
        self.assertNotIn("example", dict(fields.get_field_values_as_strings(wrapper)))

    def test_fields_rel(self):
        model_obj = Example.objects.create()
        wrapper = ModelWrapper(
            model_obj=model_obj, model_cls=Example, next_url_name="thenexturl"
        )
        fields = Fields(model_obj=model_obj)
        dct = fields.get_field_values_as_strings(wrapper)
        for k, v in dct:
            if k == "id":
                self.assertEqual(v, model_obj.pk)

    def test_fields_rel2(self):
        model_obj = ParentExample.objects.create()
        wrapper = ModelWrapper(
            model_obj=model_obj, model_cls=ParentExample, next_url_name="thenexturl"
        )
        fields = Fields(model_obj=model_obj)
        dct = fields.get_field_values_as_strings(wrapper)
        for k, v in dct:
            if k == "id":
                self.assertEqual(v, model_obj.pk)
