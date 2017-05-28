from django.test import TestCase, tag

from edc_base_test.utils import get_utcnow

from .models import Example, ParentExample, ExampleLog, ExampleLogEntry
from .wrappers import ExampleModelWrapper, ExampleModelWithLogWrapper, ParentExampleModelWithLogWrapper


@tag('wrapper')
class TestWrapper(TestCase):

    def setUp(self):
        self.test_model = Example.objects.create(f1=5, f2=6)
        self.wrapped_object = ExampleModelWrapper(self.test_model)

    def test_model_wrapper_sets_original_object_attr(self):
        self.assertEqual(self.wrapped_object.example, self.test_model)

    def test_model_wrapper_urls(self):
        self.assertEqual(
            self.wrapped_object.add_url_name, 'edc-model-wrapper:admin:edc_model_wrapper_example_add')
        self.assertEqual(
            self.wrapped_object.change_url_name, 'edc-model-wrapper:admin:edc_model_wrapper_example_change')

    def test_model_wrapper_extra_querystring(self):
        self.assertIn(
            'f2={}'.format(self.test_model.f2),
            self.wrapped_object.extra_querystring)
        self.assertIn(
            'f3={}'.format(self.test_model.f3),
            self.wrapped_object.extra_querystring)

    def test_model_wrapper_next_url(self):
        self.assertEqual(
            self.wrapped_object.next_url, 'listboard_url,f1&f1=5')


@tag('me1')
class TestModelWithLogWrapper(TestCase):

    def setUp(self):
        self.example = Example.objects.create(
            example_identifier='123456-0', f1=5, f2=6)
        self.parent_example = ParentExample.objects.create(
            example=self.example)
        self.example_log = ExampleLog.objects.create(example=self.example)
        ExampleLogEntry.objects.create(example_log=self.example_log)
        ExampleLogEntry.objects.create(example_log=self.example_log)
        ExampleLogEntry.objects.create(example_log=self.example_log)
        self.example = Example.objects.get(id=self.example.id)
        self.wrapped_object = ExampleModelWithLogWrapper(self.example)

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
