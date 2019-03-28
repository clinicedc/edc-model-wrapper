from django.contrib import admin
from django.test import TestCase, tag  # noqa

from ...wrappers import (
    ModelWrapper,
    ModelWrapperObjectAlreadyWrapped,
    ModelWrapperModelError,
)
from ..models import Example, Appointment, SubjectVisit, ParentExample
from edc_dashboard.url_names import url_names


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    pass


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    pass


@admin.register(SubjectVisit)
class SubjectVisitAdmin(admin.ModelAdmin):
    pass


class TestModelWrapper(TestCase):
    @classmethod
    def setUpClass(cls):
        url_names.register("thenexturl", "thenexturl", "edc_model_wrapper")
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        url_names.registry.pop("thenexturl")
        super().tearDownClass()

    def test_model_wrapper(self):
        """Asserts can construct.
        """
        obj = Example()
        ModelWrapper(model_obj=obj, model_cls=Example, next_url_name="thenexturl")

    def test_model_wrapper_assumes_model_cls(self):
        """Asserts can construct.
        """
        obj = Example()
        wrapper = ModelWrapper(model_obj=obj, next_url_name="thenexturl")
        self.assertEqual(wrapper.model_cls, Example)

    def test_model_wrapper_raises_on_wrong_model_cls(self):
        """Asserts can construct.
        """
        obj = Example()
        self.assertRaises(
            ModelWrapperModelError,
            ModelWrapper,
            model_obj=obj,
            model_cls=ParentExample,
            next_url_name="thenexturl",
        )

    def test_model_wrapper_raises_on_wrong_model_cls2(self):
        """Asserts can construct.
        """
        obj = Example()
        self.assertRaises(
            ModelWrapperModelError,
            ModelWrapper,
            model_obj=obj,
            model_cls=ParentExample,
            next_url_name="thenexturl",
        )

    def test_model_wrapper_raises_on_wrong_model_not_string(self):
        """Asserts can construct.
        """
        obj = Example()
        self.assertRaises(
            ModelWrapperModelError,
            ModelWrapper,
            model_obj=obj,
            model=ParentExample,
            next_url_name="thenexturl",
        )

    def test_model_wrapper_adds_kwargs_to_self(self):
        obj = Example()
        wrapper = ModelWrapper(model_obj=obj, next_url_name="thenexturl", erik="silly")
        self.assertEqual(wrapper.erik, "silly")

    def test_model_wrapper_bool(self):
        """Asserts wrapper can be truth tested.

        If model is not persisted is False.
        """
        obj = Example()
        wrapper = ModelWrapper(
            model_obj=obj, model_cls=Example, next_url_name="thenexturl"
        )
        self.assertIsNone(wrapper.object.id)
        self.assertFalse(bool(wrapper))

    def test_model_wrapper_bool2(self):
        """Asserts wrapper can be truth tested.

        If model is persisted is True.
        """
        obj = Example.objects.create()
        wrapper = ModelWrapper(
            model_obj=obj, model_cls=Example, next_url_name="thenexturl"
        )
        self.assertTrue(bool(wrapper))

    def test_model_wrapper_meta(self):
        """Asserts wrapper maintains _meta.
        """
        obj = Example.objects.create()
        wrapper = ModelWrapper(
            model_obj=obj, model_cls=Example, next_url_name="thenexturl"
        )
        self.assertEqual(wrapper._meta.label_lower, "edc_model_wrapper.example")

    def test_model_wrapper_repr(self):
        """Asserts wrapper maintains _meta.
        """
        obj = Example.objects.create()
        wrapper = ModelWrapper(
            model_obj=obj, model_cls=Example, next_url_name="thenexturl"
        )
        self.assertTrue(repr(wrapper))

    def test_model_wrapper_wraps_once(self):
        """Asserts a wrapped model instance cannot be wrapped.
        """
        obj = Example()
        wrapper = ModelWrapper(
            model_obj=obj, model_cls=Example, next_url_name="thenexturl"
        )
        obj = wrapper.object
        self.assertRaises(
            ModelWrapperObjectAlreadyWrapped,
            ModelWrapper,
            model_obj=obj,
            model_cls=Example,
            next_url_name="thenexturl",
        )

    def test_model_wrapper_invalid_name_raises(self):
        """Asserts raises if model does not match model instance.
        """
        ModelWrapper(
            model_obj=Example(),
            model="edc_model_wrapper.example",
            next_url_name="thenexturl",
        )
        self.assertRaises(
            ModelWrapperModelError,
            ModelWrapper,
            model_obj=Example(),
            model="blah",
            next_url_name="thenexturl",
        )

    def test_model_wrapper_model_is_class1(self):
        """Asserts model returns as a class if passed label_lower.
        """
        wrapper = ModelWrapper(
            model_obj=Example(),
            model="edc_model_wrapper.example",
            next_url_name="thenexturl",
        )
        self.assertEqual(wrapper.model_cls, Example)
        self.assertEqual(wrapper.model, Example._meta.label_lower)

    def test_model_wrapper_model_is_class2(self):
        """Asserts model returns as a class if passed class.
        """
        wrapper = ModelWrapper(
            model_obj=Example(), model_cls=Example, next_url_name="thenexturl"
        )
        self.assertEqual(wrapper.model_cls, Example)
        self.assertEqual(wrapper.model, Example._meta.label_lower)
