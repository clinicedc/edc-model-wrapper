from django.test import TestCase, tag

from edc_base.utils import get_utcnow

from .models import Example, ParentExample, ExampleLog, ExampleLogEntry
from .wrappers import ExampleModelWithLogWrapper, ParentExampleModelWithLogWrapper
from ..wrappers import ModelWrapper


@tag('me1')
class TestModelWithLogWrapper(TestCase):

    def setUp(self):

        class ExampleLogEntryModelWrapper(ModelWrapper):

            model = 'edc_model_wrapper.examplelogentry'
            next_url_attrs = {'edc_model_wrapper.examplelogentry': [
                'example_identifier', 'example_log']}
            querystring_attrs = {
                'edc_model_wrapper.examplelogentry': ['f2', 'f3']}
            url_attrs = ['example_identifier', 'example_log']
            url_namespace = 'edc-model-wrapper'

            @property
            def example_identifier(self):
                return self.object.example_log.example.example_identifier

            @property
            def survey(self):
                return 'survey_one'

#         class ExampleModelWithLogWrapper(ModelWithLogWrapper):
#
#             model_wrapper_class = ExampleModelWrapper
#             log_entry_model_wrapper_class = ExampleLogEntryModelWrapper

        self.example = Example.objects.create(
            example_identifier='123456-0', f1=5, f2=6)
        self.parent_example = ParentExample.objects.create(
            example=self.example)
        self.example_log = ExampleLog.objects.create(example=self.example)
        ExampleLogEntry.objects.create(example_log=self.example_log)
        ExampleLogEntry.objects.create(example_log=self.example_log)
        ExampleLogEntry.objects.create(example_log=self.example_log)
        self.example = Example.objects.get(id=self.example.id)

    @tag('2')
    def test_wrapper(self):
        self.wrapper = ExampleModelWithLogWrapper(self.example)

    def test_object_without_log(self):
        self.example.examplelog.delete()
        self.example = Example.objects.get(id=self.example.id)
        self.wrapped_object = ExampleModelWithLogWrapper(self.example)
        self.assertIsNotNone(self.wrapped_object.log_entry_model)
        self.assertIsNotNone(self.wrapped_object.log_model)
        self.assertIsNotNone(self.wrapped_object.log_model_names)

    def test_object_with_log_only(self):
        self.example.examplelog.examplelogentry_set.all().delete()
        self.example = Example.objects.get(id=self.example.id)
        self.wrapped_object = ExampleModelWithLogWrapper(self.example)
        self.assertIsNotNone(self.wrapped_object.log_entry_model)
        self.assertIsNotNone(self.wrapped_object.log_model)
        self.assertIsNotNone(self.wrapped_object.log_model_names)
        self.assertIsNotNone(self.wrapped_object.log)
        self.assertIsNotNone(self.wrapped_object.log_entry)
        self.assertTrue(self.wrapped_object.log_entry._mocked_object)

    def test_object_with_log_entry(self):
        self.assertIsNotNone(self.wrapped_object.log_entry_model)
        self.assertIsNotNone(self.wrapped_object.log_model)
        self.assertIsNotNone(self.wrapped_object.log_model_names)
        self.assertIsNotNone(self.wrapped_object.log)
        self.assertIsNotNone(self.wrapped_object.log_entry)
        self.assertTrue(self.wrapped_object.log_entry._mocked_object)

    def test_object_with_current_log_entry(self):
        self.wrapped_object = ExampleModelWithLogWrapper(
            self.example, report_datetime=get_utcnow())
        self.assertIsNotNone(self.wrapped_object.log_entry_model)
        self.assertIsNotNone(self.wrapped_object.log_model)
        self.assertIsNotNone(self.wrapped_object.log_model_names)
        self.assertIsNotNone(self.wrapped_object.log)
        self.assertIsNotNone(self.wrapped_object.log_entry)
        try:
            self.wrapped_object.log_entry._mocked_object
            self.fail('Unexpected got a mocked log entry object')
        except AttributeError:
            pass

        self.assertIn(
            'example_log={}'.format(self.example.examplelog.id),
            self.wrapped_object.log_entry.next_url)

        self.assertIn(
            'listboard_url',
            self.wrapped_object.log_entry.next_url.split('&')[0])

        self.assertIn(
            'example_log',
            self.wrapped_object.log_entry.next_url.split('&')[0])

        self.assertIn(
            'example_identifier',
            self.wrapped_object.log_entry.next_url.split('&')[0])

        self.assertIn(
            'example_identifier={}'.format(self.example.example_identifier),
            self.wrapped_object.log_entry.next_url)

    def test_object_with_different_parent_and_model(self):
        self.wrapped_object = ParentExampleModelWithLogWrapper(
            self.parent_example, report_datetime=get_utcnow())
        self.assertIsNotNone(self.wrapped_object.log_entry_model)
        self.assertIsNotNone(self.wrapped_object.log_model)
        self.assertIsNotNone(self.wrapped_object.log_model_names)
        self.assertIsNotNone(self.wrapped_object.log)
        self.assertIsNotNone(self.wrapped_object.log_entry)
        self.assertIsNotNone(self.wrapped_object.parent)
        self.assertEqual(self.wrapped_object.parent.id,
                         str(self.parent_example.example.id))
        try:
            self.wrapped_object.log_entry._mocked_object
            self.fail('Unexpected got a mocked log entry object')
        except AttributeError:
            pass

        self.assertIn(
            'example_log={}'.format(self.example.examplelog.id),
            self.wrapped_object.log_entry.next_url)

        self.assertIn(
            'listboard_url',
            self.wrapped_object.log_entry.next_url.split('&')[0])

        self.assertIn(
            'example_log',
            self.wrapped_object.log_entry.next_url.split('&')[0])

        self.assertIn(
            'example_identifier',
            self.wrapped_object.log_entry.next_url.split('&')[0])

        self.assertIn(
            'example_identifier={}'.format(self.example.example_identifier),
            self.wrapped_object.log_entry.next_url)
