from django.test import TestCase, tag  # noqa

from ...wrappers import ModelWrapper
from ..models import Example


class TestExampleWrappers(TestCase):
    def setUp(self):
        class ExampleModelWrapper(ModelWrapper):
            model = "edc_model_wrapper.example"
            next_url_name = "listboard_url"
            next_url_attrs = ["f1"]
            querystring_attrs = ["f2", "f3"]

        self.wrapper_cls = ExampleModelWrapper

    def test_model_wrapper_model_object(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(wrapper.object, model_obj)

    def test_model_wrapper_model_querystring(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertIn("f2=2&f3=3", wrapper.querystring)

    def test_model_wrapper_model_next_url(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertTrue(
            wrapper.href.split("next=")[1].startswith(
                "edc_model_wrapper:listboard_url,f1&f1=1&f2=2&f3=3"
            )
        )

    def test_example_href_add(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(
            wrapper.href,
            "/admin/edc_model_wrapper/example/add/?next=edc_model_wrapper:listboard_url,"
            "f1&f1=1&f2=2&f3=3",
        )

    def test_example_href_change(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        model_obj.save()
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(
            wrapper.href,
            f"/admin/edc_model_wrapper/example/{model_obj.pk}/change/?next=edc_model_"
            "wrapper:listboard_url,f1&f1=1&f2=2&f3=3",
        )

    def test_model_wrapper_admin_urls_add(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(
            wrapper.admin_url_name,
            "edc_model_wrapper_admin:edc_model_wrapper_example_add",
        )

    def test_model_wrapper_admin_urls_change(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        model_obj.save()
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(
            wrapper.admin_url_name,
            "edc_model_wrapper_admin:edc_model_wrapper_example_change",
        )

    def test_model_wrapper_history_url(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        model_obj.save()
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(
            wrapper.history_url,
            f"/admin/edc_model_wrapper/example/{str(model_obj.id)}/history/",
        )

    def test_model_wrapper_fields(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        model_obj.save()
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertIsNotNone(wrapper.f1)
        self.assertIsNotNone(wrapper.f2)
        self.assertIsNotNone(wrapper.f3)
        self.assertIsNotNone(wrapper.revision)
        self.assertIsNotNone(wrapper.hostname_created)
        self.assertIsNotNone(wrapper.hostname_modified)
        self.assertIsNotNone(wrapper.user_created)
        self.assertIsNotNone(wrapper.user_modified)
        self.assertIsNotNone(wrapper.created)
        self.assertIsNotNone(wrapper.modified)
