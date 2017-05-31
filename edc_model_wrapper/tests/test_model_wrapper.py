from django.contrib import admin
from django.test import TestCase, tag

from ..wrappers import Fields, FieldWrapperError
from ..wrappers import ModelWrapper, ModelWrapperObjectAlreadyWrapped
from .models import Example, ParentExample


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    pass


@tag('fields')
class TestFields(TestCase):

    def test_fields_only_except_model(self):
        self.assertRaises(
            FieldWrapperError, Fields, model_obj=1, model=Example._meta.label_lower)

    def test_fields_only_except_models_with_name(self):
        self.assertRaises(
            FieldWrapperError, Fields, model_obj=Example(), model='blah')

    def test_fields(self):
        self.assertTrue(
            Fields(model_obj=Example(),
                   model=Example._meta.label_lower))
        self.assertTrue(
            Fields(model_obj=Example(), model=Example))

    def test_fields_skips_fk(self):
        class Wrapper:
            pass
        wrapper = Wrapper()
        fields = Fields(model_obj=ParentExample(), model=ParentExample)
        self.assertNotIn('fk', dict(fields.fields(wrapper)))


@tag('model_wrapper')
class TestModelWrapper(TestCase):

    def test_model_wrapper(self):
        """Asserts can construct.
        """
        obj = Example()
        ModelWrapper(
            model_obj=obj, model=Example,
            next_url_name='thenexturl')

    def test_model_wrapper_bool(self):
        """Asserts obj can be truth tested.

        If model is not persisted is False.
        """
        obj = Example()
        ModelWrapper(
            model_obj=obj, model=Example,
            next_url_name='thenexturl')
        self.assertFalse(obj is True)

    def test_model_wrapper_wraps_once(self):
        """Asserts a wrapped model instance cannot be wrapped.
        """
        obj = Example()
        wrapper = ModelWrapper(
            model_obj=obj, model=Example,
            next_url_name='thenexturl')
        obj = wrapper.object
        self.assertRaises(
            ModelWrapperObjectAlreadyWrapped,
            ModelWrapper, model_obj=obj, model=Example,
            next_url_name='thenexturl')

    def test_model_wrapper_invalid_name_raises(self):
        """Asserts raises if model does not match model instance.
        """
        ModelWrapper(model_obj=Example(),
                     model='edc_model_wrapper.example',
                     next_url_name='thenexturl')
        self.assertRaises(
            FieldWrapperError,
            ModelWrapper, model_obj=Example(), model='blah', next_url_name='thenexturl')


@tag('1')
class TestExampleWrappers(TestCase):

    def setUp(self):

        class ExampleModelWrapper(ModelWrapper):
            model = 'edc_model_wrapper.example'
            url_namespace = 'edc-model-wrapper'
            next_url_name = 'listboard_url'
            next_url_attrs = ['f1']
            querystring_attrs = ['f2', 'f3']
        self.wrapper_cls = ExampleModelWrapper

    def test_model_wrapper_model_object(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(wrapper.object, model_obj)

    def test_example_href(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(
            wrapper.href,
            '/admin/edc_model_wrapper/example/add/?next=edc-model-wrapper:listboard_url,f1&f1=1&f2=2&f3=3')

    def test_model_wrapper_admin_urls_add(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(
            wrapper.admin_url_name, 'edc-model-wrapper:admin:edc_model_wrapper_example_add')

    def test_model_wrapper_admin_urls_change(self):
        model_obj = Example(f1=1, f2=2, f3=3)
        model_obj.save()
        wrapper = self.wrapper_cls(model_obj=model_obj)
        self.assertEqual(
            wrapper.admin_url_name, 'edc-model-wrapper:admin:edc_model_wrapper_example_change')
